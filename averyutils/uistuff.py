from averyutils import avery_logger
_log = avery_logger
try:
    import threading, time, os, asyncio
    import tkinter as tk
    from PIL import Image, ImageTk
except ImportError as e:
    print(e.name, "is not installed")
    _log.error(f"{e.name} not installed")

# WARNING! BUGGY!


_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever,daemon=True).start()

async def _display_gif(filepath: str, loop: bool=False, title: str = "", fdelay: int = 80):
    # Create the Tkinter window
    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)

    # Load the GIF frames using Pillow
    img = Image.open(os.path.abspath(filepath))
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(img.copy())
            frames.append(frame)
            img.seek(len(frames))  # Go to next frame
    except EOFError:
        pass  # End of sequence

    label = tk.Label(root)
    label.pack()

    def update_frame(index=0):
        frame = frames[index]
        label.config(image=frame)
        next_index = (index + 1) % len(frames) if loop else index + 1
        if loop or next_index < len(frames):
            root.after(fdelay, update_frame, next_index)
        else:
            root.quit()
            root.destroy()
    update_frame()
    while True:
        try:
            root.winfo_exists()
            root.update()
        except tk.TclError:
            break
        except Exception as e:
            _log.error(f"update thread error: {e}")


def display_gif(*args, **kwargs):
    return _loop.create_task(_display_gif(*args, **kwargs))
