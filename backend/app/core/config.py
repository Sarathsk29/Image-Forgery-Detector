from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    api_v1_prefix: str = "/api"
    app_name: str = "Multi-Modal Digital Forgery Detection System"
    database_url: str = "sqlite:///./forensic.db"
    storage_backend: str = "local"
    local_storage_dir: str = "./uploads"
    local_artifact_dir: str = "./artifacts"
    max_upload_size_mb: int = 5
    allow_origin: str = "http://localhost:3000"
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None
    optional_ai_model_path: str | None = None
    tesseract_cmd: str | None = None

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

