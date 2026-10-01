from pathlib import Path
from pydantic_settings import (
    BaseSettings, SettingsConfigDict, TomlConfigSettingsSource,
)



# --- constantes del servidor ---
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
DEFAULT_LOG_FILE = "app_logs.txt"
DEFAULT_LOG_LEVEL = "INFO"
MAX_HEADERS = 16 * 1024
MAX_BODY = 1024 * 1024
VERSION = "0.2.0"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SMALILOG_",
        extra="ignore",
    )
    server_cmd: str = "smali-lsp"
    server_args: list[str] = ["mcp"]
    workspace: Path | None = None
    db_path: Path | None = None

    def resolved_db(self) -> Path:
        from platformdirs import user_data_dir
        if self.db_path:
            return self.db_path
        d = Path(user_data_dir("smalilog"))
        d.mkdir(parents=True, exist_ok=True)
        return d / "memory.sqlite3"

    @classmethod
    def settings_customise_sources(
        cls, settings_cls,
        init_settings, env_settings, dotenv_settings, file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            TomlConfigSettingsSource(settings_cls, toml_file="config.toml"),
            file_secret_settings,
        )

_settings: Settings | None = None
def settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

