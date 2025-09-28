from time import strftime, localtime
from textual.widgets import SelectionList, Tree, Switch, Label
from textual import on
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical
from textual.app import ComposeResult
from textual.widgets.selection_list import Selection

class CANMessageTree(Tree):
    """Display CAN messages in a tree structure."""

    def __init__(self):
        """Initialize an empty CAN message tree."""
        super().__init__("CAN Messages")
        self.auto_expand = True  # Automatically expand each node on addition
        self.show_guides = True
        self.guide_depth = 2

    def on_mount(self):
        """Ensure the root node is expanded when the tree is first displayed."""
        self.root.expand()  # Expand the root on mount

    def add_expanded_node(self, label, data=None):
        """Adds a node and ensures it's expanded."""
        node = self.root.add(label, data)
        node.expand()  # Ensure each node is expanded
        return node

    @staticmethod
    def add_expanded_leaf(parent, label, data=None):
        """Adds a leaf node under a parent and ensures it's expanded."""
        leaf = parent.add_leaf(label, data)
        leaf.expand()  # Ensure leaf nodes are also expanded
        return leaf

class CANView(Vertical):
    """Display CAN frames using the Lighthouse system."""

    DEFAULT_CSS = """
    CANView {
        height: 100%;
        width: 100%;
    }

    #controls {
        dock: top;
        height: 3;
        padding: 1;
        background: $panel;
        border-bottom: solid $primary;
    }

    Switch {
        dock: bottom;
        background: $boost;
        margin: 1 0;
    }

    Label {
        dock: bottom;
        padding: 0 1;
    }

    SelectionList {
        dock: left;
        width: 30%;
        min-width: 20;  /* Minimum width to prevent wrapping issues */
        border: solid $primary;
        height: 100%;
        overflow-x: hidden;  /* Prevent horizontal scrolling */
    }

    Tree {
        dock: right;
        width: 70%;
        height: 100%;
        border: solid $primary;
    }

    #container {
        height: 100%;
    }
    """

    # Reactive attributes
    frames = reactive([])
    detected_ids = reactive(set())
    selected_ids = reactive(set())
    paused = reactive(False)

    def __init__(self, lighthouse) -> None:
        """Initialize the CAN view."""
        super().__init__()
        self.max_frames = 100
        self.lighthouse = lighthouse

        # CAN ID mappings with command/response pairs
        self.can_pairs = {
            "Compass": {
                "cmd": 0x304,
                "rsp": 0x314,
                "name": "CAN_ID_COMPASS_CONTROL"
            },
            "Compass Data": {
                "cmd": 0x305,
                "rsp": 0x315,
                "name": "CAN_ID_COMPASS"
            },
            "GPS Ctrl": {  # Shortened name
                "cmd": 0x202,
                "rsp": 0x212,
                "name": "CAN_ID_GPS_CONTROL"
            },
            "GPS Data": {
                "cmd": 0x203,
                "rsp": 0x213,
                "name": "CAN_ID_GPS_DATA"
            },
            "LRF Ctrl": {  # Shortened name
                "cmd": 0x200,
                "rsp": 0x210,
                "name": "CAN_ID_LRF_CONTROL"
            },
            "LRF Data": {
                "cmd": 0x201,
                "rsp": 0x211,
                "name": "CAN_ID_LRF_DATA"
            },
            "Day Cam": {  # Shortened name
                "cmd": 0x500,
                "rsp": 0x510,
                "name": "CAN_ID_CAM_DAY"
            },
            "D_G_H Ctrl": {  # New shortened name for Day Glass Heater Control
                "cmd": 0x205,
                "rsp": 0x215,
                "name": "CAN_ID_CAM_DAY_GLASS_HEAT_CONTROL"
            },
            "D_G_H Data": {  # New shortened name for Day Glass Heater Data
                "cmd": 0x206,
                "rsp": 0x216,
                "name": "CAN_ID_CAM_DAY_GLASS_HEAT_DATA"
            },
            "Therm Ctrl": {  # Shortened name
                "cmd": 0x300,
                "rsp": 0x310,
                "name": "CAN_ID_CAM_HEAT_CONTROL"
            },
            "Therm Cam": {  # Shortened name
                "cmd": 0x301,
                "rsp": 0x311,
                "name": "CAN_ID_CAM_HEAT"
            }
        }

        # Create mappings for quick lookups
        self.id_to_name = {}
        self.id_groups = {}
        for group_name, ids in self.can_pairs.items():
            self.id_to_name[ids["cmd"]] = ids["name"]
            self.id_to_name[ids["rsp"]] = ids["name"]
            self.id_groups[ids["cmd"]] = group_name
            self.id_groups[ids["rsp"]] = group_name

        self.sent_ids = {pair["cmd"] for pair in self.can_pairs.values()}
        self.received_ids = {pair["rsp"] for pair in self.can_pairs.values()}

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        # Create the controls section
        with Horizontal(id="controls"):
            yield Switch(value=False, id="pause")

        # Create main container
        with Horizontal(id="container"):
            # Create selection list with grouped IDs
            selections = []
            for group_name, ids in self.can_pairs.items():
                selections.append(Selection(
                    group_name,  # Using already shortened names from can_pairs
                    (ids["cmd"], ids["rsp"]),
                    True  # Initially selected
                ))

            selection_list = SelectionList(*selections, id="selection")
            message_tree = CANMessageTree()

            yield selection_list
            yield message_tree

            # Add label and toggle switch for pausing
            yield Label("Pause", id="pause-label")  # Shortened label
            yield Switch(value=False, id="toggle-pause")

    def on_mount(self):
        """Called when the widget is mounted."""
        self.lighthouse.register_callback("can_frames", self.handle_can_update)
        # Initialize selected IDs with all known IDs
        self.selected_ids = {
            id_ for pair in self.can_pairs.values()
            for id_ in (pair["cmd"], pair["rsp"])
        }

    def on_unmount(self):
        """Called when the widget is unmounted."""
        self.lighthouse.unregister_callback("can_frames", self.handle_can_update)

    def handle_can_update(self, new_frames):
        """Update display with new CAN frames."""
        if not new_frames or self.paused:
            return

        try:
            # Update frames list with new frames
            self.frames.extend(new_frames)
            self.frames = self.frames[-self.max_frames:]
            self.refresh_display()
        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error updating CAN frames: {e}")

    @on(SelectionList.SelectedChanged)
    def handle_selection(self, event: SelectionList.SelectedChanged) -> None:
        """Handle changes in the SelectionList selection."""
        try:
            if not hasattr(event, 'selection_list') or not event.selection_list:
                if self.lighthouse and self.lighthouse.logger:
                    self.lighthouse.logger.warning("Invalid selection event received")
                return

            # Safely extract selected IDs
            selected_ids = set()
            for selection in event.selection_list.selected:
                if isinstance(selection, (tuple, list)) and len(selection) == 2:
                    selected_ids.update(selection)

            if selected_ids:
                self.selected_ids = selected_ids
                self.refresh_display()
            else:
                if self.lighthouse and self.lighthouse.logger:
                    self.lighthouse.logger.warning("No valid IDs found in selection")

        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error handling selection: {e}")

    @on(Switch.Changed, "#pause")
    def handle_pause_change(self, event: Switch.Changed) -> None:
        """Handle changes to the pause switch."""
        self.paused = event.value

    @on(Switch.Changed, "#toggle-pause")
    def toggle_pause(self, event: Switch.Changed) -> None:
        """Toggle the pause state using the additional switch."""
        self.paused = event.value

    def get_direction_arrow(self, can_id: int) -> str:
        """Get the direction arrow for a CAN ID."""
        if can_id in self.sent_ids:
            return "→"  # Outgoing message
        elif can_id in self.received_ids:
            return "←"  # Incoming message
        return "?"  # Unknown direction

    def refresh_display(self) -> None:
        """Refresh the display with filtered frames."""
        try:
            message_tree = self.query_one(CANMessageTree)
            message_tree.clear()

            # Filter and group frames
            if self.selected_ids:
                filtered_frames = [
                    frame for frame in self.frames
                    if frame.can_id in self.selected_ids
                ]
            else:
                filtered_frames = self.frames

            # Group frames by their type
            for frame in filtered_frames:
                can_id = frame.can_id
                group_name = self.id_groups.get(can_id, "Unknown")
                is_response = can_id in self.received_ids
                msg_type = "Rsp" if is_response else "Cmd"  # Shortened
                direction = self.get_direction_arrow(can_id)

                timestamp = strftime('%H:%M:%S', localtime(frame.timestamp))
                frame_type = "FD" if frame.frame_type else "CAN"  # Shortened

                # Create main node for this message with condensed format
                msg_node = message_tree.add_expanded_node(
                    f"{timestamp} {direction} {group_name} {msg_type}"
                )

                # Add details as child nodes
                message_tree.add_expanded_leaf(msg_node, f"ID: 0x{can_id:X}")
                message_tree.add_expanded_leaf(msg_node, f"Type: {frame_type}")
                message_tree.add_expanded_leaf(msg_node, f"DLC: {frame.can_dlc}")

                # Add data bytes in hex
                data_str = ' '.join(f'{b:02X}' for b in frame.data[:frame.can_dlc])
                message_tree.add_expanded_leaf(msg_node, f"Data: {data_str}")

        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error refreshing display: {e}")
