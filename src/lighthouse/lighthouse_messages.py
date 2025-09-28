import asyncio
from enum import IntEnum
from dataclasses import dataclass, field
import struct
import logging
from typing import Optional, List, Any, Callable
import time

class MessageType(IntEnum):
    """Message types for Lighthouse communication"""
    CAN_FRAME = 0
    STATE_UPDATE = 1
    STATUS_UPDATE = 2
    TEMP_UPDATE = 3

    @classmethod
    def from_byte(cls, byte_value: int) -> 'MessageType':
        """Convert a byte value to MessageType enum"""
        try:
            return cls(byte_value)
        except ValueError:
            raise ValueError(f"Invalid message type value: {byte_value}")

@dataclass
class WebSocketErrorCode(IntEnum):
    NO_ERROR = 0
    ERROR_CONNECTION_REFUSED = 1
    ERROR_CONNECTION_LOST = 2
    ERROR_INVALID_URI = 3
    ERROR_TIMEOUT = 4
    ERROR_HANDSHAKE = 5
    ERROR_PROTOCOL = 6
    ERROR_RECONNECTING = 7

@dataclass
class WebSocketStatus:
    """WebSocket connection status"""
    connected: bool = False
    error_code: int = 0
    reconnect_attempts: int = 0
    last_connected: float = field(default_factory=time.time)
    last_error_time: float = field(default_factory=time.time)
    uri: str = ""
    messages_received: int = 0
    messages_sent: int = 0
    bytes_received: int = 0
    bytes_sent: int = 0
    current_reconnect_delay: float = 1.0

@dataclass
class CANFrame:
    """CAN frame message"""
    frame_type: int
    can_id: int
    can_dlc: int
    data: bytes
    timestamp: float = field(default_factory=time.time)

@dataclass
class LighthouseState:
    """Container for all Lighthouse state"""
    state: Any = None
    can_status: Any = None
    state_status: Any = None
    temp_status: Any = None
    system_status: Any = None
    can_frames: List[CANFrame] = field(default_factory=list)
    websocket_status: WebSocketStatus = field(default_factory=WebSocketStatus)
    last_update: float = field(default_factory=time.time)

class LighthouseMessages:
    """Handles message parsing and state management"""

    def __init__(self, logger: logging.Logger, max_can_frames: int = 1000):
        """Initialize the LighthouseMessages handler."""
        self.logger = logger
        self.state = LighthouseState()
        self.max_can_frames = max_can_frames
        self._callbacks: List[Callable[[str, Any], None]] = []

        # Message handler mapping
        self._handlers = {
            MessageType.CAN_FRAME: self._handle_can_frame,
            MessageType.STATE_UPDATE: self._handle_state_update,
            MessageType.STATUS_UPDATE: self._handle_status_update,
            MessageType.TEMP_UPDATE: self._handle_temp_update
        }

        # Batch notification setup with asyncio
        self.batch_interval = 1.0  # 1sec
        self._latest_updates = {}
        self._batching_task = asyncio.create_task(self._send_latest_updates_loop())

    async def _send_latest_updates_loop(self):
        """Asynchronous loop to send updates every batch interval."""
        while True:
            await asyncio.sleep(self.batch_interval)
            self._send_latest_updates()

    def subscribe_all(self, callback: Callable[[str, Any], None]) -> None:
        """Subscribe to all state changes."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def _store_latest(self, update_type: str, data: Any) -> None:
        """Store only the latest update for each type."""
        self._latest_updates[update_type] = data

    def _send_latest_updates(self):
        """Send the latest update of each type."""
        for update_type, data in self._latest_updates.items():
            self._notify_subscribers(update_type, data)
        self._latest_updates.clear()  # Clear after notifying

    def _notify_subscribers(self, name: str, value: Any) -> None:
        """Notify subscribers of state changes."""
        for callback in self._callbacks:
            try:
                callback(name, value)
            except Exception as e:
                self.logger.error(f"Error in subscriber callback: {e}", exc_info=True)

    def update_websocket_status(self, **updates) -> None:
        """Update WebSocket status with new values."""
        try:
            current_dict = self.state.websocket_status.__dict__.copy()
            current_dict.update(updates)
            self.state.websocket_status = WebSocketStatus(**current_dict)
            self._store_latest('websocket_status', self.state.websocket_status)
        except Exception as e:
            self.logger.error(f"Error updating WebSocket status: {e}", exc_info=True)

    def handle_message(self, message: bytes) -> None:
        """Parse and handle a WebSocket message."""
        if not message:
            return

        try:
            msg_type = MessageType.from_byte(message[0])
            payload = message[1:]

            # Update received message stats
            current_status = self.state.websocket_status
            self.update_websocket_status(
                messages_received=current_status.messages_received + 1,
                bytes_received=current_status.bytes_received + len(message)
            )

            handler = self._handlers.get(msg_type)
            if handler:
                handler(payload)
            else:
                self.logger.error(f"Unknown message type: {msg_type}")

        except ValueError as e:
            self.logger.error(f"Invalid message type: {e}")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}", exc_info=True)

    def _handle_can_frame(self, payload: bytes) -> None:
        """Handle CAN frame message."""
        try:
            frame_type = payload[0]
            can_id, can_dlc = struct.unpack_from('<IB', payload, 1)
            data = payload[6:6+can_dlc]
            frame = CANFrame(frame_type=frame_type, can_id=can_id, can_dlc=can_dlc, data=data)

            frames = self.state.can_frames.copy()
            frames.append(frame)
            if len(frames) > self.max_can_frames:
                frames = frames[-self.max_can_frames:]

            self.state.can_frames = frames
            self._store_latest('can_frames', frames)
        except Exception as e:
            self.logger.error(f"Error handling CAN frame: {e}", exc_info=True)

    def _handle_state_update(self, payload: bytes) -> None:
        """Handle state update message."""
        try:
            from c_data_python_bindings.lighthouse_bindings import jon_gui_state
            new_state = jon_gui_state.from_buffer_copy(payload)
            self.state.state = new_state
            self._store_latest('state', new_state)
        except Exception as e:
            self.logger.error(f"Error handling state update: {e}", exc_info=True)

    def _handle_status_update(self, payload: bytes) -> None:
        """Handle system status update message."""
        try:
            from c_data_python_bindings.lighthouse_bindings import SystemStatus
            status = SystemStatus.from_buffer_copy(payload)
            self.state.system_status = status
            self._store_latest('system_status', status)
        except Exception as e:
            self.logger.error(f"Error handling status update: {e}", exc_info=True)

    def _handle_temp_update(self, payload: bytes) -> None:
        """Handle temperature update message."""
        try:
            from c_data_python_bindings.lighthouse_bindings import TempHandlerStatus
            temp_status = TempHandlerStatus.from_buffer_copy(payload)
            self.state.temp_status = temp_status
            self._store_latest('temp_status', temp_status)
        except Exception as e:
            self.logger.error(f"Error handling temp update: {e}", exc_info=True)
