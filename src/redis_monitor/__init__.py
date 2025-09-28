import redis.asyncio as redis
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Tuple, Dict
from enum import IntEnum
import time
from functools import wraps
from ..config import config

class RedisErrorCode(IntEnum):
    NO_ERROR = 0
    CONNECTION_REFUSED = 1
    CONNECTION_LOST = 2
    AUTH_ERROR = 3
    TIMEOUT = 4
    PROTOCOL_ERROR = 5
    RECONNECTING = 6

@dataclass
class RedisStatus:
    """Redis connection status"""
    connected: bool = False
    error_code: RedisErrorCode = RedisErrorCode.NO_ERROR
    reconnect_attempts: int = 0
    last_connected: float = field(default_factory=time.time)
    last_error_time: float = field(default_factory=time.time)
    uri: str = ""
    current_reconnect_delay: float = 1.0

def ensure_initialized(func):
    """Decorator to ensure the system is initialized"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_initialized:
            raise RuntimeError("RedisMonitor must be initialized before use")
        return func(self, *args, **kwargs)
    return wrapper

class RedisMonitor:
    """Redis monitoring system for tracking latest state"""

    _instance = None
    _instance_lock = None

    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.redis_config = config.redis_main
        self.is_initialized: bool = False
        self._stopping: bool = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._shutdown: Optional[asyncio.Event] = None

        # Status tracking
        self.status = RedisStatus()

        # Single callback for state updates
        self._state_callback: Optional[Callable[[Any], None]] = None

        # Pattern for state info
        self._state_pattern = 'logs:app:*state_server:*:info'

        # Track latest state
        self._latest_state = None

    async def initialize(self) -> None:
        """Initialize the Redis monitor"""
        if self.is_initialized:
            return

        if self._instance_lock is None:
            self._instance_lock = asyncio.Lock()

        async with self._instance_lock:
            if self.is_initialized:
                return

            self._shutdown = asyncio.Event()
            self.is_initialized = True

    async def connect_redis(self, max_retries=float('inf')) -> redis.Redis:
        """Establish Redis connection with retries"""
        retry_count = 0
        while True:
            try:
                r = redis.Redis(
                    host=self.redis_config.host,
                    port=self.redis_config.port,
                    db=self.redis_config.db,
                    username=self.redis_config.username,
                    password=self.redis_config.password,
                    decode_responses=True,
                    socket_connect_timeout=self.redis_config.socket_connect_timeout,
                    socket_keepalive=self.redis_config.socket_keepalive,
                    health_check_interval=self.redis_config.health_check_interval,
                    retry_on_timeout=self.redis_config.retry_on_timeout
                )
                await r.ping()
                self.status = RedisStatus(
                    connected=True,
                    error_code=RedisErrorCode.NO_ERROR,
                    last_connected=time.time(),
                    uri=f"redis://{self.redis_config.host}:{self.redis_config.port}"
                )
                return r

            except redis.ConnectionError:
                self.status = RedisStatus(
                    connected=False,
                    error_code=RedisErrorCode.CONNECTION_REFUSED,
                    last_error_time=time.time(),
                    reconnect_attempts=retry_count + 1
                )
                retry_count += 1
                if retry_count >= max_retries:
                    raise
                await asyncio.sleep(self.redis_config.reconnect_interval)

    async def _get_latest_stream_entry(self) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Get the newest entry from the newest matching stream"""
        try:
            # Get all matching keys and sort them (latest key will be the one we want)
            keys = [key async for key in self.redis.scan_iter(match=self._state_pattern)]
            if not keys:
                return None

            # Sort keys in descending order (newest first)
            latest_key = sorted(keys, reverse=True)[0]

            # Get latest entry from this stream
            entries = await self.redis.xrevrange(latest_key, count=1)
            if entries:
                entry_id, entry_data = entries[0]
                return latest_key, entry_id, entry_data

        except redis.RedisError:
            pass

        return None

    @ensure_initialized
    def set_state_callback(self, callback: Callable[[Any], None]) -> None:
        """Set the callback for state updates"""
        self._state_callback = callback
        asyncio.create_task(self._check_and_update_monitoring())

    @ensure_initialized
    def clear_state_callback(self) -> None:
        """Clear the state callback"""
        self._state_callback = None
        asyncio.create_task(self._check_and_update_monitoring())

    @property
    def latest_state(self) -> Any:
        """Get the latest state"""
        return self._latest_state

    async def _check_and_update_monitoring(self) -> None:
        """Check if we need to start or stop monitoring based on callback presence"""
        if self._state_callback and not self._monitor_task:
            self._shutdown.clear()
            self._monitor_task = asyncio.create_task(self._monitor_redis())
        elif not self._state_callback and self._monitor_task:
            await self.stop()

    async def _monitor_redis(self) -> None:
        """Main Redis monitoring loop"""
        while not self._shutdown.is_set():
            try:
                if not self.redis:
                    self.redis = await self.connect_redis()

                # Get the latest entry from the newest stream
                latest_entry = await self._get_latest_stream_entry()
                if latest_entry:
                    key, entry_id, entry_data = latest_entry
                    new_state = {
                        "key": key,
                        "id": entry_id,
                        "data": entry_data
                    }

                    if new_state != self._latest_state:
                        self._latest_state = new_state
                        if self._state_callback:
                            try:
                                self._state_callback(new_state)
                            except Exception:
                                pass

                await asyncio.sleep(self.redis_config.reconnect_interval)

            except redis.ConnectionError:
                if self.redis:
                    await self.redis.close()
                    self.redis = None
                await asyncio.sleep(self.redis_config.reconnect_interval)
            except Exception:
                await asyncio.sleep(self.redis_config.reconnect_interval)

    async def stop(self) -> None:
        """Stop the monitor gracefully"""
        if not self.is_initialized or self._stopping:
            return

        async with self._instance_lock:
            if self._stopping:
                return

            self._stopping = True
            try:
                self._shutdown.set()

                if self._monitor_task:
                    self._monitor_task.cancel()
                    try:
                        await self._monitor_task
                    except asyncio.CancelledError:
                        pass
                    self._monitor_task = None

                if self.redis:
                    await self.redis.close()
                    self.redis = None

                self.is_initialized = False
            finally:
                self._stopping = False

_redis_monitor_instance: Optional[RedisMonitor] = None
_instance_lock = None

async def get_redis_monitor() -> RedisMonitor:
    """Get or create the global RedisMonitor instance"""
    global _redis_monitor_instance
    global _instance_lock

    if _instance_lock is None:
        _instance_lock = asyncio.Lock()

    async with _instance_lock:
        if _redis_monitor_instance is None:
            _redis_monitor_instance = RedisMonitor()
            await _redis_monitor_instance.initialize()
        return _redis_monitor_instance

__all__ = [
    'RedisMonitor',
    'RedisStatus',
    'RedisErrorCode',
    'get_redis_monitor'
]
