from typing import Literal

from cryptography.fernet import Fernet
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class CryptSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CRYPT__", frozen=True, extra="forbid")

    key: bytes = Field(
        default=Fernet.generate_key(),
        description="The main application host",
        repr=False,
    )


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UVICORN__", frozen=True, extra="forbid"
    )

    host: str = Field(..., description="The main application host", min_length=3)
    port: int = Field(..., description="The main application port", ge=1024, le=65535)

    workers: int = Field(default=1, description="Count of uvicorn workers", ge=0)


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TELEGRAM__", frozen=True, extra="forbid"
    )

    api_id: int = Field(..., description="Telegram app api id", repr=False)
    api_hash: str = Field(..., description="Telegram app api hash", repr=False)

    use_proxy: bool = Field(..., description="Use or not proxy")


class ProxySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROXY__", frozen=True, extra="ignore")
    scheme: Literal["socks4", "socks5", "http"] = Field(
        description="telegram supported proxy scheme", default="socks5"
    )
    hostname: str = Field(description="proxy hostname", default="localhost")
    port: int = Field(description="proxy port", ge=1024)


class RedisCacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS__", frozen=True, extra="ignore")

    db: int = Field(default=0, description="redis database number.")
    username: str = Field(..., description="redis user's name.")
    password: str = Field(..., description="redis user's password.", repr=False)
    host: str = Field(default="redis", description="redis database host.")
    port: int = Field(default=6379, description="redis database port.", ge=1024)
    expire: int = Field(default=10 * 60, description="time to expire.")


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PROJECT__", frozen=True, extra="forbid"
    )

    title: str = Field(..., description="The project's title", min_length=3)
    description: str = Field(..., description="The project's description", min_length=3)

    api_v1: str = Field(default="/api/v1", description="The api v1 string")


class Settings:
    uvcorn: UvicornSettings = UvicornSettings()
    project: ProjectSettings = ProjectSettings()
    telegram: TelegramSettings = TelegramSettings()
    redis: RedisCacheSettings = RedisCacheSettings()
    proxy: ProxySettings = ProxySettings()
    crypt: CryptSettings = CryptSettings()


settings = Settings()
