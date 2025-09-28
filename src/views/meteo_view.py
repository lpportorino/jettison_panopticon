from textual.widgets import Tree

class MeteoView(Tree):
    """Display consolidated meteorological data from all sensors in a tree structure."""

    def __init__(self, lighthouse):
        """Initialize the meteo view with a root label."""
        super().__init__("Meteorological Data")
        self.lighthouse = lighthouse
        self.root.expand()
        self.last_temp_status = None

    def on_mount(self):
        """Called when the widget is mounted."""
        super().on_mount()
        # Use the lighthouse provided via constructor
        self.lighthouse.register_callback("state", self.handle_state_update)
        self.lighthouse.register_callback("temp_status", self.handle_temp_update)
        self.show_root = True
        self.guide_depth = 4

    def on_unmount(self):
        """Called when the widget is unmounted."""
        self.lighthouse.unregister_callback("state", self.handle_state_update)
        self.lighthouse.unregister_callback("temp_status", self.handle_temp_update)

    def handle_temp_update(self, temp_status):
        """Store temperature status for the next tree update."""
        self.last_temp_status = temp_status

    def add_meteo_node(self, parent, station_name, meteo_data):
        """Add a meteorological station node with its data."""
        station_node = parent.add(station_name)
        station_node.expand()

        if hasattr(meteo_data, 'temperature'):
            temperature = meteo_data.temperature / 1000.0  # Convert int32 to float
            self.add_component_node(station_node, "Temperature", f"{temperature:.2f} °C")
        if hasattr(meteo_data, 'humidity'):
            humidity = meteo_data.humidity / 1000.0  # Convert int32 to float
            self.add_component_node(station_node, "Humidity", f"{humidity:.2f} %")
        if hasattr(meteo_data, 'pressure'):
            pressure = meteo_data.pressure / 1000.0  # Convert int32 to float
            self.add_component_node(station_node, "Pressure", f"{pressure:.2f} Pa")

        return station_node

    @staticmethod
    def add_component_node(parent, label, value):
        """Add a node with a formatted label and value."""
        node = parent.add_leaf(f"{label}: {value}")
        return node

    def add_system_sensor_node(self, parent_node, sensor_name, temperature, humidity, pressure):
        """Add a system sensor node with temperature, humidity, and pressure."""
        sensor_node = parent_node.add(sensor_name)
        sensor_node.expand()
        self.add_component_node(sensor_node, "Temperature", f"{temperature:.2f} °C")
        self.add_component_node(sensor_node, "Humidity", f"{humidity:.2f} %")
        self.add_component_node(sensor_node, "Pressure", f"{pressure:.2f} Pa")

    def handle_state_update(self, state):
        """Update tree with new meteorological data from all stations."""
        try:
            # Clear and rebuild tree
            self.root.remove_children()

            # System Meteo (Internal/External)
            system_node = self.root.add("System Sensors")
            system_node.expand()

            # Orin Temperature Sensors
            if self.last_temp_status:
                orin_node = system_node.add("Orin")
                orin_node.expand()
                readings = self.last_temp_status.readings[:self.last_temp_status.num_active_sensors]
                for reading in readings:
                    if reading.valid:
                        sensor_name = reading.name.decode('utf-8').strip('\x00')
                        temperature = reading.temperature  # Already in double
                        self.add_component_node(orin_node, sensor_name, f"{temperature:.2f} °C")

            # Component Sensors
            components_node = self.root.add("Component Sensors")
            components_node.expand()

            # List of components
            components = [
                ("Compass", state.compass.meteo),
                ("GPS", state.gps.meteo),
                ("LRF", state.lrf.meteo),
                ("Rotary", state.rotary.meteo),
                ("Power", state.power.meteo),
            ]

            for component_name, meteo_data in components:
                self.add_meteo_node(components_node, component_name, meteo_data)

            # Lens
            lens_node = components_node.add("Lens")
            lens_node.expand()
            # Day and Heat Lens Meteo
            lens_components = [
                ("Day", state.lens.day_meteo),
                ("Day Glass", state.lens.day_glass_heater_meteo),
                ("Heat", state.lens.heat_meteo),
            ]
            for lens_name, meteo_data in lens_components:
                self.add_meteo_node(lens_node, lens_name, meteo_data)

            # Add Day Glass Temperature
            if hasattr(state.lens, 'day_glass_temperature'):
                day_glass_temp = state.lens.day_glass_temperature / 1000.0  # Convert int32 to float
                self.add_component_node(lens_node, "Day Glass Temperature", f"{day_glass_temp:.2f} °C")

        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error formatting meteo data: {e}")
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