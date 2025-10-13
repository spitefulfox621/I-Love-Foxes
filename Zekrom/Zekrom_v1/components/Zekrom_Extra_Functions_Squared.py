import os, random, aiohttp, asyncpraw

from components.Zekrom_Furfag import furfag

from datetime import datetime
from discord import Embed

class Zekrom_Extra_Functions_2:
    async def Webhook_Maker(author, body, fields, images, footer):
        author_name, author_url, author_icon_url = author
        body_title, body_title_url, body_description, body_colour = body
        image_url, image_thumbnail_url = images
        footer_text, footer_icon_url = footer

        embed = Embed(title=body_title,
                            url=body_title_url,
                            description=body_description,
                            colour=body_colour,
                            timestamp=datetime.now())

        embed.set_author(name=author_name,
                        url=author_url,
                        icon_url=author_icon_url)

        for field in fields:
            field_name, field_value, field_inline = field
            embed.add_field(name=field_name,
                value=field_value,
                inline=field_inline)

        embed.set_image(url=image_url)

        embed.set_thumbnail(url=image_thumbnail_url)

        embed.set_footer(text=footer_text,
                        icon_url=footer_icon_url)
        return embed