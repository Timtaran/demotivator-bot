import asyncio
import uuid
from typing import Optional

from PIL import Image, ImageFont, ImageDraw
from aiogram import Bot
from aiogram.types import Animation, Video, PhotoSize

from settings import settings


class DemotivatorCreator:
    """
    Создает демотиватор со следующими параметрами: (на данный момент значения захардкодены)
    Разрешение: 714x746
    Размер медиа: 608x568 (с растяжением)
    Положение вотермарки: (54, 185) с центрированием по низу и середине
    """

    MAX_WIDTH = 600

    def __init__(self):
        self.base_font = ImageFont.truetype(settings.font_path, 58)
        self.multiline_font = self.base_font.font_variant(size=40)
        self.generate_base()

    # noinspection PyAttributeOutsideInit
    def generate_base(self):
        # Создаем базовое изображение
        self.base_image = Image.new("RGBA", (714, 746), (0, 0, 0, 255))

        # Создаем обводку
        base_image_draw = ImageDraw.Draw(self.base_image)
        base_image_draw.rectangle(
            ((48, 26), (669, 607)),
            fill=(0, 0, 0, 255),
            outline=(255, 255, 255),
            width=3,
        )
        base_image_draw.rectangle(((52, 32), (662, 600)), fill=(0, 0, 0, 0))

        # Создаем вотермарку
        watermark = Image.new("RGBA", (746, 714))
        image_draw = ImageDraw.Draw(watermark)
        font = self.base_font.font_variant(size=18)

        # "Прорезаем" обводку
        watermark_width = font.getlength(settings.watermark)
        left_edge = 556 - watermark_width / 2
        image_draw.rectangle(
            ((left_edge - 3, 42), (left_edge + watermark_width + 3, 53)), (0, 0, 0, 255)
        )

        # Рисуем саму вотермарку
        image_draw.text(
            (556, 54),
            settings.watermark,
            (255, 255, 255),
            font=font,
            anchor="mb",
            stroke_fill=(255, 255, 255),
            stroke_width=0.35,
        )
        watermark = watermark.rotate(90, expand=True)

        # Делаем маску чтобы вотермарка не выходила дальше нужного
        masked_watermark = Image.new("RGBA", (714, 746))
        masked_watermark.paste(watermark.crop((0, 0, 54, 714)), (0, 0, 54, 714))

        # Вставляем вотермарку
        self.base_image.alpha_composite(masked_watermark)

    async def create_demotivator(
        self, bot: Bot, media: Animation | Video | PhotoSize, text: str
    ) -> str:
        unique_video_id = uuid.uuid4().hex

        multiline = text.split("\n")
        image = self.base_image.copy()
        image_draw = ImageDraw.Draw(image)

        if len(multiline) == 1:
            self.text(image_draw, multiline[0])
        else:
            self.multiline_text(image_draw, multiline)

        image_path = f"/tmp/image{unique_video_id}.png"
        image.save(image_path, format="PNG")

        video_path = f"/tmp/video{unique_video_id}.{'.jpg' if isinstance(media, PhotoSize) else 'mp4'}"
        await bot.download(media.file_id, destination=video_path)

        output_path = f"/tmp/demotivator{unique_video_id}.mp4"

        cmd = [
            "ffmpeg",
            "-i",
            image_path,
            "-i",
            video_path,
            "-filter_complex",
            "[1:v]scale=608:568[vid];[0:v][vid]overlay=55:33",
            "-shortest",
            "-an",
            "-y",
            output_path,
        ]

        # Запускаем процесс
        process = await asyncio.create_subprocess_exec(
            *cmd,
        )
        await process.wait()

        return output_path

    def text(
        self,
        image_draw: ImageDraw.ImageDraw,
        text: str,
        y: int = 674,
        font: Optional[ImageFont.FreeTypeFont] = None,
    ):
        font = font if font else self.base_font

        text_width = image_draw.textlength(text, font=font)

        if text_width > self.MAX_WIDTH:
            font = font.font_variant(size=font.size * (self.MAX_WIDTH / text_width))

        image_draw.text(
            (357, y),
            text,
            (255, 255, 255),
            font=font,
            anchor="mm",
        )

    def multiline_text(self, image_draw: ImageDraw.ImageDraw, multiline: list[str]):
        self.text(image_draw, multiline[0], 647, self.base_font)
        self.text(image_draw, multiline[1], 702, self.multiline_font)
