"""
voicemessage handler for Reshiram\n
made by Risumies <3
"""

import discord
import os
import io
import base64
from pydub import AudioSegment
from discord.http import HTTPClient
import json

# made by risumies <33333
class DiscordAudioFile:
    ALLOWED_FORMATS = {
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
    }

    def __init__(self, file: discord.File):
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in DiscordAudioFile.ALLOWED_FORMATS:
            raise ValueError("Wrong file format buddy")

        # _ indicates that this shouldnt be accessed, but if you ever really had to, go ahead
        self._file = file
        self.ext = ext
        self.mime = DiscordAudioFile.ALLOWED_FORMATS[ext]
        self.size = DiscordAudioFile.get_file_size(file)
        self.filename = file.filename
        self.fp = file.fp
        self.duration, self.waveform = DiscordAudioFile.get_audio_info(file.fp)

    def read(self) -> bytes:
        self._file.reset()
        try:
            return self._file.fp.read()
        finally:
            self._file.reset()

    @staticmethod
    def get_file_size(file: discord.File) -> int:
        original_pos = file.fp.tell()

        file.fp.seek(0, io.SEEK_END)
        size = file.fp.tell()

        file.fp.seek(original_pos)

        return size

    @staticmethod
    def get_audio_info(file_path: str) -> tuple[float, str]:
        audio: AudioSegment = AudioSegment.from_file(file_path)

        # Normalize audio format
        audio = audio.set_sample_width(2)  # Force 16-bit
        audio = audio.set_frame_rate(32000)  # Match your WAV sample rate
        audio = audio.set_channels(1)  # Ensure mono

        # debugging artifact
        # print(f"Format info for {file_path}:")
        # print(f"Frame rate: {audio.frame_rate}Hz")
        # print(f"Sample width: {audio.sample_width} bytes")
        # print(f"Channels: {audio.channels}")
        # print(f"Frame count: {len(audio.get_array_of_samples())}")

        duration_secs = len(audio) / 1000.0

        samples = audio.get_array_of_samples()
        channels = audio.channels  # prob not needed now that the channels are set to 1
        samples_per_channel = len(samples) // channels

        bucket_size = samples_per_channel // 256
        waveform = []

        max_possible_amplitude = 32768  # 2^15 (exponentiation not binary carrotting)

        for i in range(256):
            start = i * bucket_size * channels
            end = start + bucket_size * channels
            chunk = samples[start:end]

            max_amp = max(abs(sample) for sample in chunk)
            normalized = int(min(255, (max_amp / max_possible_amplitude) * 255))

            waveform.append(normalized)

        # print(waveform)
        return duration_secs, base64.b64encode(bytes(waveform)).decode()

class VoiceMessageManager:
    def __init__(self, bot_http_client: HTTPClient):
        self.http = bot_http_client
        self._setup_extensions()

    async def send_voice_message(self, file: discord.File, channel: discord.TextChannel):
        MAX_FILE_SIZE = 10 * 1024 * 1024
        audio_file = DiscordAudioFile(file)

        if audio_file.size > MAX_FILE_SIZE:
            raise ValueError("too big lol")

        message_data = await self._send_voice_message_request(audio_file, channel.id)

        return discord.Message(state=channel._state, channel=channel, data=message_data)

    async def _send_voice_message_request(self, audio: DiscordAudioFile, channel_id: int):
        route = discord.http.Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)

        form = [
            {
                "name": "payload_json",
                "value": json.dumps({
                    "flags": 1 << 13,
                    "attachments": [{
                        "id": 0,
                        "filename": audio.filename,
                        "duration_secs": audio.duration,
                        "waveform": audio.waveform
                    }]
                }),
                "content_type": "application/json"
            },
            {
                "name": "files[0]",
                "value": audio.read(),
                "filename": audio.filename,
                "content_type": audio.mime
            }
        ]

        return await self.http.request(route, form=form, files=None)

    # monkey patch! so that you could call `channel.send_voice_message(...) instead`
    def _setup_extensions(self):
        async def send_voice_message(channel: discord.TextChannel, file: discord.File) -> discord.Message:
            return await self.send_voice_message(file, channel)

        if not hasattr(discord.TextChannel, 'send_voice_message'):
            discord.TextChannel.send_voice_message = send_voice_message