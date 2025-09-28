"""Configuration management for Panopticon.

Loads credentials from credentials.toml file or environment variables.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import toml
from dataclasses import dataclass, field


@dataclass
class RedisConfig:
    """Redis connection configuration."""
    host: str = "127.0.0.1"
    port: int = 8084
    db: int = 1
    username: Optional[str] = None
    password: Optional[str] = None
    ssl: bool = False
    ssl_cert_reqs: str = "none"
    reconnect_interval: float = 1.0
    socket_connect_timeout: int = 2
    socket_keepalive: bool = True
    health_check_interval: int = 2
    retry_on_timeout: bool = True


@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    host: str = "localhost"
    port: int = 8094
    database: str = "jettison"
    user: Optional[str] = None
    password: Optional[str] = None


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""
    reconnect_interval: float = 1.0
    socket_connect_timeout: int = 2
    socket_keepalive: bool = True
    health_check_interval: int = 2
    retry_on_timeout: bool = True


class Config:
    """Main configuration class."""

    def __init__(self):
        self.redis_main = RedisConfig()
        self.redis_health = RedisConfig()
        self.database = DatabaseConfig()
        self.monitoring = MonitoringConfig()
        self._load_config()

    def _find_config_file(self) -> Optional[Path]:
        """Find the credentials.toml file."""
        # Check multiple locations
        search_paths = [
            Path("credentials.toml"),
            Path.home() / ".config" / "panopticon" / "credentials.toml",
            Path("/etc/panopticon/credentials.toml"),
        ]

        # Also check if specified via environment variable
        if env_path := os.environ.get("PANOPTICON_CREDENTIALS"):
            search_paths.insert(0, Path(env_path))

        for path in search_paths:
            if path.exists():
                return path

        return None

    def _load_config(self):
        """Load configuration from file or environment variables."""
        config_file = self._find_config_file()

        if config_file:
            try:
                config_data = toml.load(config_file)
                self._apply_config(config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_file}: {e}", file=sys.stderr)
                self._load_from_env()
        else:
            print("Warning: No credentials.toml found, using environment variables", file=sys.stderr)
            self._load_from_env()

    def _apply_config(self, config_data: Dict[str, Any]):
        """Apply configuration from dictionary."""
        # Redis main configuration
        if "redis" in config_data and "main" in config_data["redis"]:
            redis_main = config_data["redis"]["main"]
            for key, value in redis_main.items():
                if hasattr(self.redis_main, key):
                    setattr(self.redis_main, key, value)

        # Redis health configuration
        if "redis" in config_data and "health" in config_data["redis"]:
            redis_health = config_data["redis"]["health"]
            for key, value in redis_health.items():
                if hasattr(self.redis_health, key):
                    setattr(self.redis_health, key, value)

        # Database configuration
        if "database" in config_data:
            for key, value in config_data["database"].items():
                if hasattr(self.database, key):
                    setattr(self.database, key, value)

        # Monitoring configuration
        if "monitoring" in config_data:
            for key, value in config_data["monitoring"].items():
                if hasattr(self.monitoring, key):
                    setattr(self.monitoring, key, value)

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Redis main
        self.redis_main.host = os.getenv("REDIS_MAIN_HOST", self.redis_main.host)
        self.redis_main.port = int(os.getenv("REDIS_MAIN_PORT", self.redis_main.port))
        self.redis_main.db = int(os.getenv("REDIS_MAIN_DB", self.redis_main.db))
        self.redis_main.username = os.getenv("REDIS_MAIN_USERNAME")
        self.redis_main.password = os.getenv("REDIS_MAIN_PASSWORD")

        # Redis health
        self.redis_health.host = os.getenv("REDIS_HEALTH_HOST", self.redis_health.host)
        self.redis_health.port = int(os.getenv("REDIS_HEALTH_PORT", self.redis_health.port))
        self.redis_health.db = int(os.getenv("REDIS_HEALTH_DB", self.redis_health.db))
        self.redis_health.username = os.getenv("REDIS_HEALTH_USERNAME")
        self.redis_health.password = os.getenv("REDIS_HEALTH_PASSWORD")

        # Database
        self.database.host = os.getenv("DB_HOST", self.database.host)
        self.database.port = int(os.getenv("DB_PORT", self.database.port))
        self.database.database = os.getenv("DB_NAME", self.database.database)
        self.database.user = os.getenv("DB_USER")
        self.database.password = os.getenv("DB_PASSWORD")


# Global configuration instance
config = Config()