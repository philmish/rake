import os
from pydantic import BaseSettings, Field


class RakeSettingsBase(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 3001


class RakeSettingsEnvFile(RakeSettingsBase):
    
    class Config:
        env_file=".env"


class RakeSettingsEnvVar(RakeSettingsBase):
    host: str = Field(default_factory=lambda: os.environ.get("RAKE_HOST"))
    port: int = Field(default_factory=lambda: os.environ.get("RAKE_PORT"))
