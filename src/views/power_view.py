# src/views/power_view.py

from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from typing import Dict

class PowerView(Tree):
    """Display power-related state updates in a tree structure."""

    def __init__(self, lighthouse):
        """Initialize the power view with a root label."""
        super().__init__("Power Status")
        self.lighthouse = lighthouse
        self._node_paths: Dict[str, TreeNode] = {}
        self.root.expand()
        self.can_device_mapping = {
            0: "None",
            1: "Compass",
            2: "GPS",
            3: "Day Camera",
            4: "Heat Camera",
            5: "Heat Core",
            6: "LRF",
            7: "Orin"
        }

    def on_mount(self):
        """Called when the widget is mounted."""
        super().on_mount()
        # Use the lighthouse provided via constructor
        self.lighthouse.register_callback("state", self.handle_state_update)
        self.show_root = True
        self.guide_depth = 4

    def on_unmount(self):
        """Called when the widget is unmounted."""
        self.lighthouse.unregister_callback("state", self.handle_state_update)

    @staticmethod
    def add_component_node(parent: TreeNode, label: str, value) -> TreeNode:
        """Add a node with a formatted label and value."""
        node = parent.add_leaf(f"{label}: {value}")
        return node

    def add_dict_to_tree(self, parent_node: TreeNode, data_dict: Dict, component_name: str = None):
        """Add a dictionary of values to the tree under a parent node."""
        if component_name:
            node = parent_node.add(component_name)
            parent_node = node
            node.expand()  # Always expand all nodes

        for key, value in data_dict.items():
            if isinstance(value, dict):
                # Recursive call for nested dictionaries
                self.add_dict_to_tree(parent_node, value, component_name=key)
            else:
                self.add_component_node(parent_node, key, value)

        return parent_node

    def handle_state_update(self, state):
        """Update tree with new power state data."""
        try:
            # Clear and rebuild tree
            self._node_paths.clear()
            self.root.remove_children()

            # Build power information dictionary
            power_info = {
                "Meteo": {
                    "Temperature": f"{state.power.meteo.temperature / 1000.0:.2f} °C",
                    "Humidity": f"{state.power.meteo.humidity / 1000.0:.2f} %",
                    "Pressure": f"{state.power.meteo.pressure / 1000.0:.2f} Pa"
                },
                "Modules": {}
            }

            # Add module states
            for i in range(8):
                module = getattr(state.power, f's{i}')
                module_info = {
                    "Voltage": f"{module.voltage / 1000.0:.2f} V",
                    "Current": f"{module.current / 1000.0:.2f} A",
                    "Power": f"{module.power / 1000.0:.2f} W",
                    "Is Alarm": bool(module.is_alarm),
                    "CAN Cmd Address": f"0x{module.can_cmd_address:X}",
                    "CAN Data Address": f"0x{module.can_data_address:X}",
                    "Is Power On": bool(module.is_power_on),
                    "CAN Device": self.can_device_mapping.get(module.can_device, "Unknown"),
                }
                power_info["Modules"][f"Module {i}"] = module_info

            # Add power info to tree
            self.add_dict_to_tree(self.root, power_info)

            # Ensure root is expanded
            self.root.expand()

        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error formatting power state data: {e}")
                import traceback
                self.lighthouse.logger.error(traceback.format_exc())

    # Override these methods to prevent collapse
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion."""
        pass

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Prevent node collapse by re-expanding."""
        if event.node is not self.root:
            event.node.expand()
