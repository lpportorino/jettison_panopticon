# src/views/state_view.py

import time
from textual.widgets import Tree
from enum import Enum
from typing import Dict, Set
from textual.widgets.tree import TreeNode

class StateView(Tree):
    """Display state updates using the Lighthouse system in a tree structure."""

    def __init__(self, lighthouse):
        """Initialize the state view with a root label."""
        super().__init__("System State")
        self.lighthouse = lighthouse
        self.expanded_nodes: Set[str] = set()
        self._node_paths: Dict[str, TreeNode] = {}
        self.root.expand()  # Start with root expanded
        self.expanded_nodes.add("")  # Root path is empty string
        self.fix_type_mapping = {
            0: "None",
            1: "1D",
            2: "2D",
            3: "3D",
            4: "Manual"
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
    def format_enum(value, enum_prefix):
        """Format enum values by removing the enum prefix."""
        if isinstance(value, Enum):
            enum_str = value.name
            clean_name = enum_str.replace(enum_prefix, '').replace('_', ' ').title()
            return clean_name
        return str(value)

    def add_component_node(self, parent: TreeNode, label: str, value, node_id=None):
        """Add a node with a formatted label and value."""
        node = parent.add_leaf(f"{label}: {value}")
        path = self._get_node_path(node, node_id=node_id or label)
        self._node_paths[path] = node
        return node

    def add_dict_to_tree(self, parent_node: TreeNode, data_dict, component_name=None, component_id=None):
        """Add a dictionary of values to the tree under a parent node."""
        if component_name:
            node = parent_node.add(component_name)
            path = self._get_node_path(node, node_id=component_id or component_name)
            self._node_paths[path] = node
            if path in self.expanded_nodes:
                node.expand()
            parent_node = node

        for key, value in data_dict.items():
            if isinstance(value, dict):
                # Recursive call for nested dictionaries
                self.add_dict_to_tree(parent_node, value, component_name=key, component_id=key)
            else:
                self.add_component_node(parent_node, key, value, node_id=key)

        return parent_node

    def expand_saved_nodes(self):
        """Expand all saved nodes after tree rebuild."""
        try:
            sorted_paths = sorted(self.expanded_nodes, key=lambda x: x.count('/'))
            for path in sorted_paths:
                node = self._node_paths.get(path)
                if node and not node.is_expanded:
                    try:
                        node.expand()
                    except Exception as e:
                        if self.lighthouse and self.lighthouse.logger:
                            self.lighthouse.logger.error(f"Error expanding node {path}: {e}")
        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error in expand_saved_nodes: {e}")

    def _get_node_path(self, node: TreeNode, node_id=None) -> str:
        """Get the full path of a node in the tree."""
        try:
            path_parts = []
            current = node
            while current is not None and current != self.root:
                label = str(current.label)
                if node_id and current == node:
                    label = node_id
                else:
                    if ':' in label:
                        label = label.split(':', 1)[0].strip()
                path_parts.append(label)
                current = current.parent
            return '/'.join(reversed(path_parts))
        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error getting node path: {e}")
            return ""

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion."""
        try:
            path = self._get_node_path(event.node)
            if not path:  # Root node
                return
            self.expanded_nodes.add(path)
        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error in node expansion: {e}")

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Handle node collapse."""
        try:
            path = self._get_node_path(event.node)
            if not path:  # Root node
                return
            self.expanded_nodes.discard(path)
        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error in node collapse: {e}")

    @staticmethod
    def normalize_value(value, min_value, max_value):
        """Normalize a value between min and max to 0.0 - 1.0"""
        if max_value <= min_value:
            return 0.0
        value = max(min(value, max_value), min_value)
        return (value - min_value) / (max_value - min_value)

    @staticmethod
    def get_meteo_info(meteo_data):
        """Extract meteo information."""
        return {
            "temperature": f"{meteo_data.temperature / 1000.0:.2f} °C",
            "humidity": f"{meteo_data.humidity / 1000.0:.2f} %",
            "pressure": f"{meteo_data.pressure / 1000.0:.2f} Pa"
        }

    @staticmethod
    def get_color_info(color_data):
        """Extract color information."""
        color_info = {}
        for attr_name in ['bg', 'text', 'focused', 'main', 'accent', 'faded']:
            if hasattr(color_data, attr_name):
                color_attr = getattr(color_data, attr_name)
                color_info[attr_name] = f"hsva({color_attr.h},{color_attr.s},{color_attr.v},{color_attr.a})"
        return color_info

    @staticmethod
    def get_tracking_data_info(tracking_data_array):
        """Extract tracking data information."""
        tracking_data_info = {}
        for idx, quad in enumerate(tracking_data_array):
            quad_info = {
                "p1": {
                    "x": quad.p1.fields.x,
                    "y": quad.p1.fields.y,
                    "color_index": quad.p1.fields.color_index
                },
                "p2": {
                    "x": quad.p2.fields.x,
                    "y": quad.p2.fields.y,
                    "color_index": quad.p2.fields.color_index
                }
            }
            tracking_data_info[f"quad_{idx}"] = quad_info
        return tracking_data_info

    def handle_state_update(self, state):
        """Update tree with new state data."""
        try:
            # Clear node paths and rebuild tree
            self._node_paths.clear()
            self.root.remove_children()

            # HEADER
            header_info = {
                "version": state.header.version,
                "state_update_counter": state.header.state_update_counter,
                "active_mode_id": self.format_enum(state.header.active_mode_id, "JON_GUI_DATA_MODE_"),
                "active_screen_id": self.format_enum(state.header.active_screen_id, "JON_GUI_SCREEN_")
            }
            self.add_dict_to_tree(self.root, header_info, component_name="header", component_id="header")

            # COMPASS
            compass_info = {
                "azimuth": state.compass.azimuth * 0.05625,
                "elevation": state.compass.elevation * 0.05625,
                "bank": state.compass.bank * 0.05625,
                "offset": state.compass.offset * 0.05625,
                "units_idx": self.format_enum(state.compass.units_idx, "JON_GUI_DATA_COMPASS_UNITS_"),
                "device_status": self.format_enum(state.compass.device_status, "JON_GUI_DATA_DEVICE_STATUS_"),
                "meteo": self.get_meteo_info(state.compass.meteo)
            }
            self.add_dict_to_tree(self.root, compass_info, component_name="compass", component_id="compass")

            # COMPASS CALIBRATION
            compass_calibration_info = {
                "stage": state.compass_calibration.stage,
                "final_stage": state.compass_calibration.final_stage,
                "target_azimuth": state.compass_calibration.target_azimuth * 0.05625,
                "target_elevation": state.compass_calibration.target_elevation * 0.05625,
                "target_bank": state.compass_calibration.target_bank * 0.05625,
                "status": self.format_enum(state.compass_calibration.status, "JON_GUI_DATA_COMPASS_CALIBRATE_STATUS_")
            }
            self.add_dict_to_tree(self.root, compass_calibration_info, component_name="compass_calibration", component_id="compass_calibration")

            # COLORS
            colors_info = {
                "menu": self.get_color_info(state.colors.menu),
                "osd": self.get_color_info(state.colors.osd)
            }
            self.add_dict_to_tree(self.root, colors_info, component_name="colors", component_id="colors")

            # TIME
            time_info = {
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(state.time.timestamp)),
                "manual_timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(state.time.manual_timestamp)),
                "zone_id": state.time.zone_id,
                "use_manual_time": bool(state.time.use_manual_time)
            }
            self.add_dict_to_tree(self.root, time_info, component_name="time", component_id="time")

            # GPS
            gps_info = {
                "Timestamp": state.gps.timestamp,
                "longitude": state.gps.longitude * 1e-6,
                "latitude": state.gps.latitude * 1e-6,
                "height": state.gps.height * 1e-3,
                "manual_longitude": state.gps.manual_longitude * 1e-6,
                "manual_latitude": state.gps.manual_latitude * 1e-6,
                "manual_altitude": state.gps.manual_altitude * 1e-3,
                "fix_type": str(self.fix_type_mapping.get(state.gps.fix_type, "Unknown")),
                "use_manual": bool(state.gps.use_manual),
                "units_idx": self.format_enum(state.gps.units_idx, "JON_GUI_DATA_GPS_UNITS_"),
                "device_status": self.format_enum(state.gps.device_status, "JON_GUI_DATA_DEVICE_STATUS_"),
                "meteo": self.get_meteo_info(state.gps.meteo)
            }
            self.add_dict_to_tree(self.root, gps_info, component_name="gps", component_id="gps")

            # LRF
            lrf_info = {
                "scanning": bool(state.lrf.scanning),
                "measuring": bool(state.lrf.measuring),
                "last_range_measured_val_1": state.lrf.last_range_measured_val_1 / 1000.0,
                "last_range_measured_val_2": state.lrf.last_range_measured_val_2 / 1000.0,
                "last_range_measured_val_3": state.lrf.last_range_measured_val_3 / 1000.0,
                "fog_mode_enabled": bool(state.lrf.fog_mode_enabled),
                "scanning_mode_freq": state.lrf.scanning_mode_freq,
                "measure_id": state.lrf.measure_id,
                "target_designator_status": self.format_enum(state.lrf.target_designator_status, "JON_GUI_DATA_LRF_TARGET_DESIGNATOR_STATUS_"),
                "error_bf": state.lrf.error_bf,
                "device_status": self.format_enum(state.lrf.device_status, "JON_GUI_DATA_DEVICE_STATUS_"),
                "meteo": self.get_meteo_info(state.lrf.meteo)
            }
            self.add_dict_to_tree(self.root, lrf_info, component_name="lrf", component_id="lrf")

            # MEDIA
            media_info = {
                "space_left_prc": state.media.space_left_prc / 1000.0
            }
            self.add_dict_to_tree(self.root, media_info, component_name="media", component_id="media")

            # SYSTEM
            system_info = {
                "enable_video_recording": bool(state.system.enable_video_recording),
                "recording_is_important": bool(state.system.recording_is_important),
                "disk_space_percent_taken": state.system.disk_space_percent_taken / 1000.0,
                "day_af_enable": bool(state.system.day_af_enable),
                "day_ae_enable": bool(state.system.day_ae_enable),
                "irf_enable": bool(state.system.irf_enable),
                "is_enable": bool(state.system.is_enable),
                "agc_mode": bool(state.system.agc_mode),
                "enable_zoom_sync": bool(state.system.enable_zoom_sync),
                "eth_enabled": bool(state.system.eth_enabled),
                "wifi_enabled": bool(state.system.wifi_enabled),
                "enable_continuous_zoom": bool(state.system.enable_continuous_zoom),
                "localization_id": self.format_enum(state.system.localization_id, "JON_GUI_DATA_SYSTEM_LOCALIZATION_"),
                "active_video_channel": self.format_enum(state.system.active_video_channel, "JON_GUI_DATA_VIDEO_CHANNEL_"),
                "active_thermal_color_filter_idx": self.format_enum(state.system.active_thermal_color_filter_idx, "JON_GUI_DATA_VIDEO_CHANNEL_HEAT_FILTER_"),
                "active_day_filter_idx": self.format_enum(state.system.active_day_filter_idx, "JON_GUI_DATA_VIDEO_CHANNEL_DAY_FILTER_"),
                "accumulator_stat_idx": self.format_enum(state.system.acccumulator_stat_idx, "JON_GUI_DATA_ACCUMULATOR_STATE_"),
                "sd_card_stat_idx": self.format_enum(state.system.sd_card_stat_idx, "JON_GUI_DATA_SD_CARD_STATE_"),
                "shutdown_timer_running": bool(state.system.shutdown_timer_running),
                "geodesic_mode_enabled": bool(state.system.geodesic_mode_enabled),
                "cur_video_rec_dir": {
                    "year": state.system.cur_video_rec_dir_year,
                    "month": state.system.cur_video_rec_dir_month,
                    "day": state.system.cur_video_rec_dir_day,
                    "hour": state.system.cur_video_rec_dir_hour,
                    "minute": state.system.cur_video_rec_dir_minute,
                    "second": state.system.cur_video_rec_dir_second
                },
                "low_disk_space": bool(state.system.low_disk_space),
                "no_disk_space": bool(state.system.no_disk_space)
            }
            self.add_dict_to_tree(self.root, system_info, component_name="system", component_id="system")

            # OSD
            osd_info = {
                "show_on_recording": bool(state.osd.show_on_recording),
                "crosshair_index": state.osd.crosshair_index,
                "crosshair_size_indx": state.osd.crosshair_size_indx,
                "faded_opa": state.osd.faded_opa,
                "fade_enabled": bool(state.osd.fade_enabled),
                "show_photo_indicator": bool(state.osd.show_photo_indicator),
                "disable_heat_osd": bool(state.osd.disable_heat_osd),
                "disable_day_osd": bool(state.osd.disable_day_osd),
                "pip_pos_id": self.format_enum(state.osd.pip_pos_id, "JON_GUI_DATA_OSD_PIP_POS_")
            }
            self.add_dict_to_tree(self.root, osd_info, component_name="osd", component_id="osd")

            # TARGETS
            targets_info = {
                "last_target": {},  # Expand as needed
                "target_viewer_current_target": {},  # Expand as needed
                "recorded_targets_count": state.targets.recorded_targets_count,
                "screenshot_state": self.format_enum(state.targets.screenshot_state, "JON_GUI_DATA_TARGETS_SCREENSHOT_STATE_")
            }
            self.add_dict_to_tree(self.root, targets_info, component_name="targets", component_id="targets")

            # CAMERA ALIGNMENT
            camera_alignment_info = {
                "table_row": state.camera_alignment.table_row,
                "day_focus_target_pos": state.camera_alignment.day_focus_target_pos,
                "heat_focus_target_pos": state.camera_alignment.heat_focus_target_pos,
                "day_zoom_target_pos": state.camera_alignment.day_zoom_target_pos,
                "heat_zoom_target_pos": state.camera_alignment.heat_zoom_target_pos,
                "day_cross_hair_offset_ver": state.camera_alignment.day_cross_hair_offset_ver,
                "heat_cross_hair_offset_ver": state.camera_alignment.heat_cross_hair_offset_ver,
                "day_cross_hair_offset_hor": state.camera_alignment.day_cross_hair_offset_hor,
                "heat_cross_hair_offset_hor": state.camera_alignment.heat_cross_hair_offset_hor,
                "used": bool(state.camera_alignment.used)
            }
            self.add_dict_to_tree(self.root, camera_alignment_info, component_name="camera_alignment", component_id="camera_alignment")

            # METEO
            meteo_info = {
                "internal_temperature": state.meteo.internal_temperature / 1000.0,
                "internal_humidity": state.meteo.internal_humidity / 1000.0,
                "internal_pressure": state.meteo.internal_pressure / 1000.0,
                "external_temperature": state.meteo.external_temperature / 1000.0,
                "external_humidity": state.meteo.external_humidity / 1000.0,
                "external_pressure": state.meteo.external_pressure / 1000.0
            }
            self.add_dict_to_tree(self.root, meteo_info, component_name="meteo", component_id="meteo")

            # LENS
            lens_info = {
                "day_focus_pos": state.lens.day_focus_pos,
                "day_focus_pos_min": state.lens.day_focus_pos_min,
                "day_focus_pos_max": state.lens.day_focus_pos_max,
                "day_focus_pos_normalized": self.normalize_value(state.lens.day_focus_pos, state.lens.day_focus_pos_min, state.lens.day_focus_pos_max),
                "day_zoom_table_index": state.lens.day_zoom_table_index,
                "day_zoom_table_max_index": state.lens.day_zoom_table_max_index,
                "day_glass_temperature": state.lens.day_glass_temperature / 1000.0,
                "day_glass_heater_enabled": bool(state.lens.day_glass_heater_enabled),
                "heat_zoom_table_index": state.lens.heat_zoom_table_index,
                "heat_zoom_table_max_index": state.lens.heat_zoom_table_max_index,
                "heat_focus_pos": state.lens.heat_focus_pos,
                "day_zoom_pos": state.lens.day_zoom_pos,
                "day_zoom_pos_min": state.lens.day_zoom_pos_min,
                "day_zoom_pos_max": state.lens.day_zoom_pos_max,
                "day_zoom_pos_normalized": self.normalize_value(state.lens.day_zoom_pos, state.lens.day_zoom_pos_min, state.lens.day_zoom_pos_max),
                "day_iris_pos": state.lens.day_iris_pos,
                "day_iris_pos_normalized": state.lens.day_iris_pos / 100.0,
                "day_meteo": self.get_meteo_info(state.lens.day_meteo),
                "heat_meteo": self.get_meteo_info(state.lens.heat_meteo),
                "heat_zoom_pos": state.lens.heat_zoom_pos,
                "day_zoom_x": state.lens.day_zoom_x,
                "heat_zoom_x": state.lens.heat_zoom_x,
                "heat_digital_zoom_level": state.lens.heat_digital_zoom_level,
                "day_digital_zoom_level": state.lens.day_digital_zoom_level,
                "day_crop": {
                    "top": state.lens.day_crop_top,
                    "bottom": state.lens.day_crop_bottom,
                    "left": state.lens.day_crop_left,
                    "right": state.lens.day_crop_right,
                },
                "heat_crop": {
                    "top": state.lens.heat_crop_top,
                    "bottom": state.lens.heat_crop_bottom,
                    "left": state.lens.heat_crop_left,
                    "right": state.lens.heat_crop_right,
                },
                "heat_dde_enabled": bool(state.lens.heat_dde_enabled),
                "heat_dde_level": state.lens.heat_dde_level,
                "heat_dde_max_level": state.lens.heat_dde_max_level,
                "device_status_day": self.format_enum(state.lens.device_status_day, "JON_GUI_DATA_DEVICE_STATUS_"),
                "device_status_heat": self.format_enum(state.lens.device_status_heat, "JON_GUI_DATA_DEVICE_STATUS_"),
                "fx_mode_day": self.format_enum(state.lens.fx_mode_day, "JON_GUI_DATA_FX_MODE_DAY_"),
                "fx_mode_heat": self.format_enum(state.lens.fx_mode_heat, "JON_GUI_DATA_FX_MODE_HEAT_"),
                "day_clahe_level": state.lens.day_clahe_level,
                "heat_clahe_level": state.lens.heat_clahe_level
            }
            self.add_dict_to_tree(self.root, lens_info, component_name="lens", component_id="lens")

            # ROTARY
            rotary_info = {
                "platform_azimuth": state.rotary.platform_azimuth * 0.01,
                "platform_elevation": state.rotary.platform_elevation * 0.01,
                "platform_bank": state.rotary.platform_bank * 0.01,
                "use_platform_positioning": bool(state.rotary.use_platform_positioning),
                "head_azimuth": state.rotary.head_azimuth * 0.01,
                "head_elevation": state.rotary.head_elevation * 0.01,
                "head_bank": state.rotary.head_bank * 0.01,
                "speed_azimuth": state.rotary.speed_azimuth,
                "speed_elevation": state.rotary.speed_elevation,
                "speed_bank": state.rotary.speed_bank,
                "set_azimuth": state.rotary.set_azimuth * 0.01,
                "set_elevation": state.rotary.set_elevation * 0.01,
                "set_speed_azimuth": state.rotary.set_speed_azimuth,
                "set_speed_elevation": state.rotary.set_speed_elevation,
                "set_azimuth_dir": state.rotary.set_azimuth_dir,
                "set_elevation_dir": state.rotary.set_elevation_dir,
                "set_azimuth_offset": state.rotary.set_azimuth_offset * 0.01,
                "is_scanning": bool(state.rotary.is_scanning),
                "is_scanning_paused": bool(state.rotary.is_scanning_paused),
                "device_status": self.format_enum(state.rotary.device_status, "JON_GUI_DATA_DEVICE_STATUS_"),
                "mode": self.format_enum(state.rotary.mode, "JON_GUI_DATA_ROTARY_MODE_"),
                "meteo": self.get_meteo_info(state.rotary.meteo)
            }
            self.add_dict_to_tree(self.root, rotary_info, component_name="rotary", component_id="rotary")

            # POWER
            power_info = {
                "meteo": self.get_meteo_info(state.power.meteo),
                "modules": {}
            }
            for i in range(8):
                module = getattr(state.power, f's{i}')
                module_info = {
                    "voltage": f"{module.voltage / 1000.0:.2f} V",
                    "current": f"{module.current / 1000.0:.2f} A",
                    "power": f"{module.power / 1000.0:.2f} W",
                    "is_alarm": bool(module.is_alarm),
                    "can_cmd_address": f"0x{module.can_cmd_address:X}",
                    "can_data_address": f"0x{module.can_data_address:X}",
                    "is_power_on": bool(module.is_power_on),
                    "can_device": self.format_enum(module.can_device, "JON_GUI_DATA_POWER_CAN_DEVICE_"),
                }
                power_info["modules"][f"Module {i}"] = module_info
            self.add_dict_to_tree(self.root, power_info, component_name="power", component_id="power")

            # CV
            cv_info = {
                "af_day_enabled": bool(state.cv.af_day_enabled),
                "af_heat_enabled": bool(state.cv.af_heat_enabled),
                "tracking_day": bool(state.cv.tracking_day),
                "tracking_heat": bool(state.cv.tracking_heat),
                "dumping": bool(state.cv.dumping),
                "tracking_data_day": self.get_tracking_data_info(state.cv.tracking_data_day),
                "tracking_data_heat": self.get_tracking_data_info(state.cv.tracking_data_heat),
                "vampire_mode_enabled" : bool(state.cv.vampire_mode_enabled),
                "stabilization_mode_enabled" : bool(state.cv.stabilization_mode_enabled),
            }
            self.add_dict_to_tree(self.root, cv_info, component_name="cv", component_id="cv")

            # DEBUG
            debug_info = {
                "values": {f"value_{idx}": value for idx, value in enumerate(state.debug.values)},
                "display_debug": bool(state.debug.display_debug)
            }
            self.add_dict_to_tree(self.root, debug_info, component_name="debug", component_id="debug")

            # Expand root node by default
            self.root.expand()
            self.expand_saved_nodes()

        except Exception as e:
            if self.lighthouse and self.lighthouse.logger:
                self.lighthouse.logger.error(f"Error formatting state data: {e}")
                import traceback
                self.lighthouse.logger.error(traceback.format_exc())
