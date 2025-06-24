from pydantic import SecretStr

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    bot_token: SecretStr
    watermark: str = ""
    font_path: str = "/app/media/font.ttf"
    is_private: bool = False
    admin_ids: list[int] = lambda: []
    debug_mode: bool = False


settings = Settings()
