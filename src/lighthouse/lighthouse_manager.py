import asyncio
import logging
from typing import Optional, Callable, Any
from contextlib import asynccontextmanager
import time

from websockets.client import connect as websockets_connect
from websockets.client import WebSocketClientProtocol
from websockets import exceptions as websockets_exceptions

from .lighthouse_messages import (
    LighthouseMessages,
    WebSocketStatus,
    WebSocketErrorCode
)

class LighthouseManager:
    """Manages WebSocket connection and message processing"""

    def __init__(self, logger: logging.Logger, uri: str = "ws://localhost:8089"):
        """Initialize the LighthouseManager."""
        self.logger = logger
        self.uri = uri
        self.messages = LighthouseMessages(logger)
        self.websocket: Optional[WebSocketClientProtocol] = None
        self._connection_task: Optional[asyncio.Task] = None
        self._shutdown = None  # Will be initialized in start()
        self._last_reconnect_time = 0
        self._min_reconnect_interval = 1.0  # 1 second reconnect interval
        self._max_reconnect_delay = 1.0     # No exponential backoff

        # Initialize websocket status
        self.messages.update_websocket_status(uri=uri)

    def subscribe_all(self, callback: Callable[[str, Any], None]) -> None:
        """Subscribe to all state changes."""
        self.messages.subscribe_all(callback)

    async def _wait_for_reconnect_timeout(self) -> None:
        """Wait for minimum reconnection interval if needed."""
        current_time = time.time()
        time_since_last_reconnect = current_time - self._last_reconnect_time

        if time_since_last_reconnect < self._min_reconnect_interval:
            delay = self._min_reconnect_interval - time_since_last_reconnect
            self.logger.debug(f"Waiting {delay:.1f}s before reconnection attempt")
            await asyncio.sleep(delay)

    async def connect(self) -> None:
        """Establish WebSocket connection."""
        try:
            await self._wait_for_reconnect_timeout()
            self._last_reconnect_time = time.time()

            self.websocket = await websockets_connect(self.uri)

            self.messages.update_websocket_status(
                connected=True,
                error_code=WebSocketErrorCode.NO_ERROR,
                last_connected=time.time(),
                current_reconnect_delay=self._min_reconnect_interval
            )

            self.logger.info(f"Connected to WebSocket server at {self.uri}")

        except ConnectionRefusedError:
            self.messages.update_websocket_status(
                connected=False,
                error_code=WebSocketErrorCode.ERROR_CONNECTION_REFUSED,
                last_error_time=time.time()
            )
            self.websocket = None
            raise
        except Exception as e:
            self.messages.update_websocket_status(
                connected=False,
                error_code=WebSocketErrorCode.ERROR_HANDSHAKE,
                last_error_time=time.time()
            )
            self.websocket = None
            self.logger.error(f"Failed to connect: {e}", exc_info=True)
            raise

    async def disconnect(self) -> None:
        """Close WebSocket connection."""
        if self.websocket:
            try:
                await self.websocket.close()
                self.logger.info("Closed WebSocket connection")
            except Exception as e:
                self.logger.error(f"Error closing connection: {e}", exc_info=True)
            finally:
                self.websocket = None
                self.messages.update_websocket_status(
                    connected=False,
                    error_code=WebSocketErrorCode.NO_ERROR
                )

    async def _handle_messages(self) -> None:
        """Handle incoming WebSocket messages."""
        while not self._shutdown.is_set() and self.websocket:
            try:
                message = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=0.5  # Shorter timeout for more responsive shutdown
                )
                self.messages.handle_message(message)

            except asyncio.TimeoutError:
                continue

            except websockets_exceptions.ConnectionClosed as e:
                if not self._shutdown.is_set():
                    self.messages.update_websocket_status(
                        connected=False,
                        error_code=WebSocketErrorCode.ERROR_CONNECTION_LOST,
                        last_error_time=time.time()
                    )
                    self.logger.warning(f"Connection closed: {e}")
                break

            except Exception as e:
                if not self._shutdown.is_set():
                    self.messages.update_websocket_status(
                        error_code=WebSocketErrorCode.ERROR_PROTOCOL,
                        last_error_time=time.time()
                    )
                    self.logger.error(f"Message handling error: {e}", exc_info=True)
                break

    async def _maintain_connection(self) -> None:
        """Maintain WebSocket connection with automatic reconnection."""
        while not self._shutdown.is_set():
            try:
                async with self._get_connection():
                    self.messages.update_websocket_status(
                        current_reconnect_delay=self._min_reconnect_interval
                    )
                    await self._handle_messages()

            except ConnectionRefusedError:
                await self._handle_connection_error(
                    self._min_reconnect_interval,
                    WebSocketErrorCode.ERROR_CONNECTION_REFUSED,
                    "Connection refused"
                )

            except Exception as e:
                await self._handle_connection_error(
                    self._min_reconnect_interval,
                    WebSocketErrorCode.ERROR_RECONNECTING,
                    f"Connection error: {e}"
                )

    async def _handle_connection_error(
        self,
        delay: float,
        error_code: WebSocketErrorCode,
        message: str
    ) -> None:
        """Handle connection errors and update status."""
        current_status = self.messages.state.websocket_status
        self.messages.update_websocket_status(
            connected=False,
            error_code=error_code,
            reconnect_attempts=current_status.reconnect_attempts + 1,
            last_error_time=time.time(),
            current_reconnect_delay=delay
        )
        self.logger.warning(f"{message}, retrying in {delay:.1f}s")
        await asyncio.sleep(delay)

    @asynccontextmanager
    async def _get_connection(self):
        """Context manager for WebSocket connection."""
        try:
            await self.connect()
            yield self
        finally:
            await self.disconnect()

    def start(self) -> None:
        """Start the connection manager."""
        if self._connection_task is not None:
            self.logger.warning("Connection manager already started")
            return

        if self._shutdown is None:
            self._shutdown = asyncio.Event()

        self._shutdown.clear()
        self._connection_task = asyncio.create_task(self._maintain_connection())
        self.logger.info("Connection manager started")

    async def stop(self) -> None:
        """Stop the connection manager."""
        if self._connection_task is None:
            return

        self._shutdown.set()

        try:
            await self.disconnect()
            if not self._connection_task.done():
                self._connection_task.cancel()
                try:
                    await self._connection_task
                except asyncio.CancelledError:
                    pass
        except Exception as e:
            self.logger.error(f"Error stopping connection manager: {e}", exc_info=True)
        finally:
            self._connection_task = None
            self.logger.info("Connection manager stopped")
