import redis.asyncio as redis
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict, List
from enum import IntEnum
import time
from functools import wraps
import re
from datetime import datetime
from ..config import config

class HealthErrorCode(IntEnum):
    NO_ERROR = 0
    CONNECTION_REFUSED = 1
    CONNECTION_LOST = 2
    AUTH_ERROR = 3
    TIMEOUT = 4
    PROTOCOL_ERROR = 5
    RECONNECTING = 6

@dataclass
class HealthMetric:
    """Individual health metric for a service"""
    service_path: str
    metric_type: str
    health: int
    cap: int
    last_updated: float = field(default_factory=time.time)

    def __eq__(self, other):
        """Compare metrics ignoring timestamp"""
        if not isinstance(other, HealthMetric):
            return NotImplemented
        return (self.service_path == other.service_path and
                self.metric_type == other.metric_type and
                self.health == other.health and
                self.cap == other.cap)

    def __str__(self):
        """String representation for logging"""
        return (f"{self.service_path}[{self.metric_type}] "
                f"health={self.health}/{self.cap} "
                f"({self.health_percentage:.1f}%) - {self.status}")

    @property
    def health_percentage(self) -> float:
        """Calculate health percentage"""
        return (self.health / self.cap * 100) if self.cap > 0 else 0.0

    @property
    def status(self) -> str:
        """Get status based on health percentage"""
        health_percent = self.health_percentage
        if health_percent >= 50:
            return "Healthy"
        elif health_percent >= 25:
            return "Warning"
        return "Critical"

@dataclass
class HealthStatus:
    """Health monitoring status"""
    connected: bool = False
    error_code: HealthErrorCode = HealthErrorCode.NO_ERROR
    reconnect_attempts: int = 0
    last_connected: float = field(default_factory=time.time)
    last_error_time: float = field(default_factory=time.time)
    uri: str = ""
    current_reconnect_delay: float = 1.0

    def __str__(self):
        """String representation for logging"""
        return (f"Connected: {self.connected}, Error: {self.error_code.name}, "
                f"Attempts: {self.reconnect_attempts}, URI: {self.uri}")


def ensure_initialized(func):
    """Decorator to ensure the system is initialized"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_initialized:
            raise RuntimeError("HealthMonitor must be initialized before use")
        return func(self, *args, **kwargs)
    return wrapper

class HealthMonitor:
    """Health monitoring system for tracking service health metrics"""

    _instance = None
    _instance_lock = None

    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.redis_config = config.redis_health
        self.is_initialized: bool = False
        self._stopping: bool = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._shutdown: Optional[asyncio.Event] = None
        self.status = HealthStatus()
        self._health_callback: Optional[Callable[[Dict[str, HealthMetric]], None]] = None
        self._health_metrics: Dict[str, HealthMetric] = {}

    async def initialize(self) -> None:
        """Initialize the health monitor"""
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
                    ssl=self.redis_config.ssl,
                    ssl_cert_reqs=self.redis_config.ssl_cert_reqs,
                    decode_responses=True,
                    socket_connect_timeout=self.redis_config.socket_connect_timeout,
                    socket_keepalive=self.redis_config.socket_keepalive,
                    health_check_interval=self.redis_config.health_check_interval,
                    retry_on_timeout=self.redis_config.retry_on_timeout
                )
                await r.ping()
                self.status = HealthStatus(
                    connected=True,
                    error_code=HealthErrorCode.NO_ERROR,
                    last_connected=time.time(),
                    uri=f"redis://{self.redis_config.host}:{self.redis_config.port}"
                )
                return r

            except redis.ConnectionError as e:
                self.status = HealthStatus(
                    connected=False,
                    error_code=HealthErrorCode.CONNECTION_REFUSED,
                    last_error_time=time.time(),
                    reconnect_attempts=retry_count + 1
                )
                retry_count += 1
                if retry_count >= max_retries:
                    raise
                await asyncio.sleep(self.redis_config.reconnect_interval)

    async def _fetch_health_metrics(self) -> Dict[str, HealthMetric]:
        """Fetch all health metrics from Redis"""
        metrics = {}
        key_regex = re.compile(r'(.*?):__healthpool__(.*?)_(cap|health)$')

        try:
            keys_pattern = "*:__healthpool__*_*"
            all_metrics = {}

            async for key in self.redis.scan_iter(match=keys_pattern):
                match = key_regex.match(key)
                if match:
                    service_path = match.group(1)
                    metric_type = match.group(2)
                    category = match.group(3)

                    metric_id = f"{service_path}[{metric_type}]"
                    if metric_id not in all_metrics:
                        all_metrics[metric_id] = {
                            "service_path": service_path,
                            "metric_type": metric_type
                        }

                    value = await self.redis.get(key)
                    all_metrics[metric_id][category] = int(value) if value else 0

            current_time = time.time()
            for metric_id, data in all_metrics.items():
                if "health" in data and "cap" in data:
                    metrics[metric_id] = HealthMetric(
                        service_path=data["service_path"],
                        metric_type=data["metric_type"],
                        health=data["health"],
                        cap=data["cap"],
                        last_updated=current_time
                    )

        except redis.RedisError:
            pass

        return metrics

    @ensure_initialized
    def set_health_callback(self, callback: Callable[[Dict[str, HealthMetric]], None]) -> None:
        """Set the callback for health updates"""
        self._health_callback = callback
        asyncio.create_task(self._check_and_update_monitoring())

    @ensure_initialized
    def clear_health_callback(self) -> None:
        """Clear the health callback"""
        self._health_callback = None
        asyncio.create_task(self._check_and_update_monitoring())

    @property
    def health_metrics(self) -> Dict[str, HealthMetric]:
        """Get the latest health metrics"""
        return self._health_metrics.copy()

    async def _check_and_update_monitoring(self) -> None:
        """Check if we need to start or stop monitoring based on callback presence"""
        if self._health_callback and not self._monitor_task:
            self._shutdown.clear()
            self._monitor_task = asyncio.create_task(self._monitor_health())
        elif not self._health_callback and self._monitor_task:
            await self.stop()

    async def _monitor_health(self) -> None:
        """Main health monitoring loop"""
        while not self._shutdown.is_set():
            try:
                if not self.redis:
                    self.redis = await self.connect_redis()

                new_metrics = await self._fetch_health_metrics()
                self._health_metrics = new_metrics

                if self._health_callback:
                    try:
                        self._health_callback(new_metrics)
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

_health_monitor_instance: Optional[HealthMonitor] = None
_instance_lock = None

async def get_health_monitor() -> HealthMonitor:
    """Get or create the global HealthMonitor instance"""
    global _health_monitor_instance
    global _instance_lock

    if _instance_lock is None:
        _instance_lock = asyncio.Lock()

    async with _instance_lock:
        if _health_monitor_instance is None:
            _health_monitor_instance = HealthMonitor()
            await _health_monitor_instance.initialize()
        return _health_monitor_instance

__all__ = [
    'HealthMonitor',
    'HealthStatus',
    'HealthMetric',
    'HealthErrorCode',
    'get_health_monitor'
]
