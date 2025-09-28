# src/lighthouse/__init__.py

from dataclasses import dataclass
from typing import Optional, Callable, Any, Dict, List
import logging
import asyncio
import atexit
from functools import wraps
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Import required lighthouse components
from .lighthouse_manager import LighthouseManager
from .lighthouse_messages import (
    LighthouseMessages,
    WebSocketStatus,
    WebSocketErrorCode,
    MessageType,
    CANFrame
)

@dataclass
class LighthouseConfig:
    """Configuration for the Lighthouse system"""
    websocket_uri: str = "ws://localhost:8089"
    max_can_frames: int = 1000
    reconnect_interval: float = 1.0
    log_dir: str = "/tmp/lighthouse/logs"
    max_log_size_mb: int = 10
    backup_count: int = 5
    enable_file_logging: bool = True

def ensure_initialized(func):
    """Decorator to ensure the system is initialized before method calls"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_initialized:
            raise RuntimeError("LighthouseSystem must be initialized before use")
        return func(self, *args, **kwargs)
    return wrapper

class LogCallbackHandler(logging.Handler):
    """Handler that routes log messages to registered callbacks"""
    def __init__(self, lighthouse_system):
        super().__init__()
        self.lighthouse_system = lighthouse_system

    def emit(self, record):
        try:
            log_debug = self.format(record)
            callbacks = self.lighthouse_system._callbacks.get("logs", [])
            for callback in callbacks:
                try:
                    callback(log_debug)
                except Exception:
                    pass  # Avoid recursion in logging
        except Exception:
            pass  # Handle errors silently to prevent recursion

class LighthouseSystem:
    """
    Singleton interface for the Lighthouse WebSocket communication system.
    Provides access to state updates and message handling through specific callback subscriptions.
    """

    _instance = None
    _instance_lock = None  # Will be initialized in the event loop

    def __init__(self):
        self.logger: Optional[logging.Logger] = None
        self.manager: Optional[LighthouseManager] = None
        self.is_initialized: bool = False
        self._stopping: bool = False
        self.config: Optional[LighthouseConfig] = None

        self._callbacks: Dict[str, List[Callable[[Any], None]]] = {
            "can_frames": [],
            "state": [],
            "websocket_status": [],
            "system_status": [],
            "temp_status": [],
            "logs": []
        }

        # Register cleanup on exit
        atexit.register(self._cleanup)

    def _setup_log_directory(self) -> str:
        """Create and setup the log directory."""
        log_dir = os.path.abspath(os.path.expanduser(self.config.log_dir))
        os.makedirs(log_dir, exist_ok=True)
        self.logger.debug(f"Setting up log directory at: {log_dir}")
        return log_dir

    def _create_internal_logger(self) -> None:
        """Creates and configures an internal logger with file output and callbacks."""
        self.logger = logging.getLogger("LighthouseSystem")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if self.config.enable_file_logging:
            log_dir = self._setup_log_directory()
            log_filename = f"lighthouse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_path = os.path.join(log_dir, log_filename)

            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=self.config.max_log_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.info(f"Log file created at: {os.path.abspath(log_path)}")
        else:
            self.logger.info("File logging disabled")

        callback_handler = LogCallbackHandler(self)
        callback_handler.setFormatter(formatter)
        self.logger.addHandler(callback_handler)

    async def initialize(
        self,
        logger: Optional[logging.Logger] = None,
        config: Optional[LighthouseConfig] = None
    ) -> None:
        """Initialize the Lighthouse system with optional logger and config."""
        if self.is_initialized:
            return

        if self._instance_lock is None:
            self._instance_lock = asyncio.Lock()

        async with self._instance_lock:
            if self.is_initialized:
                return

            self.config = config or LighthouseConfig()

            if logger:
                self.logger = logger
            else:
                self._create_internal_logger()

            # Setup manager
            self.manager = LighthouseManager(
                logger=self.logger,
                uri=self.config.websocket_uri
            )

            # Use the current event loop
            self._event_loop = asyncio.get_running_loop()

            # Register all subscribers
            self.manager.subscribe_all(self._handle_state_update)

            # Start the manager
            self.manager.start()
            self.is_initialized = True
            self.logger.info("LighthouseSystem initialized")

    @ensure_initialized
    def _handle_state_update(self, name: str, value: Any) -> None:
        """Propagate state updates to registered callbacks."""
        if name in self._callbacks:
            for callback in self._callbacks[name]:
                try:
                    callback(value)
                except Exception as e:
                    self.logger.error(f"Error in callback for '{name}': {e}", exc_info=True)

    @ensure_initialized
    def register_callback(self, update_type: str, callback: Callable[[Any], None]) -> None:
        """Register a callback for a specific type of update."""
        if update_type not in self._callbacks:
            self.logger.warning(f"Unknown update type '{update_type}'")
            return

        if callback not in self._callbacks[update_type]:
            self._callbacks[update_type].append(callback)
            if update_type == "logs":
                self.logger.info(f"New log subscriber registered")

    @ensure_initialized
    def unregister_callback(self, update_type: str, callback: Callable[[Any], None]) -> None:
        """Remove a callback for the specified update type."""
        if update_type in self._callbacks and callback in self._callbacks[update_type]:
            self._callbacks[update_type].remove(callback)
            if update_type == "logs":
                self.logger.info(f"Log subscriber unregistered")

    async def stop(self) -> None:
        """Stop the system gracefully."""
        if not self.is_initialized or self._stopping:
            return

        if self._instance_lock is None:
            self._instance_lock = asyncio.Lock()

        async with self._instance_lock:
            if self._stopping:
                return

            self._stopping = True
            try:
                if self.manager:
                    await self.manager.stop()
                    self.manager = None
                    self.is_initialized = False
                    if self.logger:
                        self.logger.info("LighthouseSystem stopped")
            finally:
                self._stopping = False

    def _cleanup(self) -> None:
        """Synchronous cleanup for atexit."""
        if not self.is_initialized:
            return

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(self.stop(), loop)
            else:
                loop.run_until_complete(self.stop())
        except Exception as e:
            if self.logger:
                self.logger.error(f"Cleanup error: {e}", exc_info=True)

# Module-level singleton instance
_lighthouse_instance: Optional[LighthouseSystem] = None
_instance_lock = None

async def get_lighthouse() -> LighthouseSystem:
    """Get or create the global LighthouseSystem instance"""
    global _lighthouse_instance
    global _instance_lock

    if _instance_lock is None:
        _instance_lock = asyncio.Lock()

    async with _instance_lock:
        if _lighthouse_instance is None:
            _lighthouse_instance = LighthouseSystem()
            await _lighthouse_instance.initialize()
        return _lighthouse_instance

# Export public interface
__all__ = [
    'LighthouseSystem',
    'LighthouseConfig',
    'get_lighthouse',
    'WebSocketStatus',
    'WebSocketErrorCode',
    'MessageType',
    'CANFrame'
]
