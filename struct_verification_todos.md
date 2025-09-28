# Struct Verification Todo List

This document contains todo items for verifying that all struct fields are properly printed in the state view and documented in the report.

## Todo Format
- [ ] **Check struct printing**: Verify all fields are included in state view
  - [ ] **Add to report**: Document findings for this struct in the report file

---

## Field: `camera_alignment`

### `camera_alignment` (struct_jon_gui_data_camera_alignment)

- [ ] **Verify printing of `struct_jon_gui_data_camera_alignment`**
  - Check that all 10 fields are printed in state view:
    - `table_row` (int32)
    - `day_focus_target_pos` (int32)
    - `heat_focus_target_pos` (int32)
    - `day_zoom_target_pos` (int32)
    - `heat_zoom_target_pos` (int32)
    - `day_cross_hair_offset_ver` (int32)
    - `heat_cross_hair_offset_ver` (int32)
    - `day_cross_hair_offset_hor` (int32)
    - `heat_cross_hair_offset_hor` (int32)
    - `used` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_camera_alignment`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `colors`

### `colors` (struct_jon_gui_data_colors)

- [ ] **Verify printing of `struct_jon_gui_data_colors`**
  - Check that all 2 fields are printed in state view:
    - `menu` (struct_jon_gui_data_colors_menu)
    - `osd` (struct_jon_gui_data_colors_osd)
  - [ ] **Add report entry for `struct_jon_gui_data_colors`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.menu` (struct_jon_gui_data_colors_menu)

- [ ] **Verify printing of `struct_jon_gui_data_colors_menu`**
  - Check that all 3 fields are printed in state view:
    - `bg` (struct_jon_gui_data_colors_value)
    - `text` (struct_jon_gui_data_colors_value)
    - `focused` (struct_jon_gui_data_colors_value)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_menu`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.menu.bg` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.menu.focused` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.menu.text` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.osd` (struct_jon_gui_data_colors_osd)

- [ ] **Verify printing of `struct_jon_gui_data_colors_osd`**
  - Check that all 3 fields are printed in state view:
    - `main` (struct_jon_gui_data_colors_value)
    - `accent` (struct_jon_gui_data_colors_value)
    - `faded` (struct_jon_gui_data_colors_value)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_osd`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.osd.accent` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.osd.faded` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `colors.osd.main` (struct_jon_gui_data_colors_value)

- [ ] **Verify printing of `struct_jon_gui_data_colors_value`**
  - Check that all 4 fields are printed in state view:
    - `h` (int32)
    - `s` (int32)
    - `v` (int32)
    - `a` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_colors_value`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `compass`

### `compass` (struct_jon_gui_data_compass)

- [ ] **Verify printing of `struct_jon_gui_data_compass`**
  - Check that all 7 fields are printed in state view:
    - `azimuth` (int32)
    - `elevation` (int32)
    - `bank` (int32)
    - `offset` (int32)
    - `unnamed_1` (union_anon_4)
    - `unnamed_2` (union_anon_5)
    - `meteo` (struct_jon_gui_data_component_meteo)
  - [ ] **Add report entry for `struct_jon_gui_data_compass`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `compass.meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `compass.unnamed_1` (union_anon_4)

- [ ] **Verify printing of `union_anon_4`**
  - Check that all 2 fields are printed in state view:
    - `units_idx` (int32)
    - `units_idx_packed` (int32)
  - [ ] **Add report entry for `union_anon_4`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `compass.unnamed_2` (union_anon_5)

- [ ] **Verify printing of `union_anon_5`**
  - Check that all 2 fields are printed in state view:
    - `device_status` (int32)
    - `device_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_5`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `compass_calibration`

### `compass_calibration` (struct_jon_gui_data_compass_calibration)

- [ ] **Verify printing of `struct_jon_gui_data_compass_calibration`**
  - Check that all 6 fields are printed in state view:
    - `stage` (int32)
    - `final_stage` (int32)
    - `target_azimuth` (int32)
    - `target_elevation` (int32)
    - `target_bank` (int32)
    - `unnamed_1` (union_anon_6)
  - [ ] **Add report entry for `struct_jon_gui_data_compass_calibration`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `compass_calibration.unnamed_1` (union_anon_6)

- [ ] **Verify printing of `union_anon_6`**
  - Check that all 2 fields are printed in state view:
    - `status` (int32)
    - `jon_gui_data_compass_calibrate_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_6`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `cv`

### `cv` (struct_jon_gui_data_cv)

- [ ] **Verify printing of `struct_jon_gui_data_cv`**
  - Check that all 10 fields are printed in state view:
    - `af_day_enabled` (int32)
    - `af_heat_enabled` (int32)
    - `tracking_day` (int32)
    - `tracking_heat` (int32)
    - `vampire_mode_enabled` (int32)
    - `stabilization_mode_enabled` (int32)
    - `recognition_mode_enabled` (int32)
    - `dumping` (int32)
    - `tracking_data_day` (struct_jon_gui_tracking_quad[10], array[10])
    - `tracking_data_heat` (struct_jon_gui_tracking_quad[10], array[10])
  - [ ] **Add report entry for `struct_jon_gui_data_cv`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_day[]` (struct_jon_gui_tracking_quad)

- [ ] **Verify printing of `struct_jon_gui_tracking_quad`**
  - Check that all 2 fields are printed in state view:
    - `p1` (union_jon_gui_tracking_point)
    - `p2` (union_jon_gui_tracking_point)
  - [ ] **Add report entry for `struct_jon_gui_tracking_quad`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_day[].p1` (union_jon_gui_tracking_point)

- [ ] **Verify printing of `union_jon_gui_tracking_point`**
  - Check that all 2 fields are printed in state view:
    - `fields` (struct_anon_38)
    - `packed` (uint32)
  - [ ] **Add report entry for `union_jon_gui_tracking_point`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_day[].p1.fields` (struct_anon_38)

- [ ] **Verify printing of `struct_anon_38`**
  - Check that all 3 fields are printed in state view:
    - `x` (uint32)
    - `y` (uint32)
    - `color_index` (uint32)
  - [ ] **Add report entry for `struct_anon_38`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_day[].p2` (union_jon_gui_tracking_point)

- [ ] **Verify printing of `union_jon_gui_tracking_point`**
  - Check that all 2 fields are printed in state view:
    - `fields` (struct_anon_38)
    - `packed` (uint32)
  - [ ] **Add report entry for `union_jon_gui_tracking_point`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_day[].p2.fields` (struct_anon_38)

- [ ] **Verify printing of `struct_anon_38`**
  - Check that all 3 fields are printed in state view:
    - `x` (uint32)
    - `y` (uint32)
    - `color_index` (uint32)
  - [ ] **Add report entry for `struct_anon_38`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_heat[]` (struct_jon_gui_tracking_quad)

- [ ] **Verify printing of `struct_jon_gui_tracking_quad`**
  - Check that all 2 fields are printed in state view:
    - `p1` (union_jon_gui_tracking_point)
    - `p2` (union_jon_gui_tracking_point)
  - [ ] **Add report entry for `struct_jon_gui_tracking_quad`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_heat[].p1` (union_jon_gui_tracking_point)

- [ ] **Verify printing of `union_jon_gui_tracking_point`**
  - Check that all 2 fields are printed in state view:
    - `fields` (struct_anon_38)
    - `packed` (uint32)
  - [ ] **Add report entry for `union_jon_gui_tracking_point`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_heat[].p1.fields` (struct_anon_38)

- [ ] **Verify printing of `struct_anon_38`**
  - Check that all 3 fields are printed in state view:
    - `x` (uint32)
    - `y` (uint32)
    - `color_index` (uint32)
  - [ ] **Add report entry for `struct_anon_38`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_heat[].p2` (union_jon_gui_tracking_point)

- [ ] **Verify printing of `union_jon_gui_tracking_point`**
  - Check that all 2 fields are printed in state view:
    - `fields` (struct_anon_38)
    - `packed` (uint32)
  - [ ] **Add report entry for `union_jon_gui_tracking_point`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `cv.tracking_data_heat[].p2.fields` (struct_anon_38)

- [ ] **Verify printing of `struct_anon_38`**
  - Check that all 3 fields are printed in state view:
    - `x` (uint32)
    - `y` (uint32)
    - `color_index` (uint32)
  - [ ] **Add report entry for `struct_anon_38`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `debug`

### `debug` (struct_anon_41)

- [ ] **Verify printing of `struct_anon_41`**
  - Check that all 2 fields are printed in state view:
    - `values` (int32[20], array[20])
    - `display_debug` (int32)
  - [ ] **Add report entry for `struct_anon_41`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `gps`

### `gps` (struct_jon_gui_data_gps)

- [ ] **Verify printing of `struct_jon_gui_data_gps`**
  - Check that all 12 fields are printed in state view:
    - `longitude` (int32)
    - `latitude` (int32)
    - `height` (int32)
    - `manual_longitude` (int32)
    - `manual_latitude` (int32)
    - `manual_altitude` (int32)
    - `unnamed_1` (union_anon_9)
    - `unnamed_2` (union_anon_10)
    - `use_manual` (int32)
    - `unnamed_3` (union_anon_11)
    - `unnamed_4` (union_anon_12)
    - `meteo` (struct_jon_gui_data_component_meteo)
  - [ ] **Add report entry for `struct_jon_gui_data_gps`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.unnamed_1` (union_anon_9)

- [ ] **Verify printing of `union_anon_9`**
  - Check that all 2 fields are printed in state view:
    - `timestamp` (int64)
    - `unnamed_1` (struct_anon_8)
  - [ ] **Add report entry for `union_anon_9`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.unnamed_1.unnamed_1` (struct_anon_8)

- [ ] **Verify printing of `struct_anon_8`**
  - Check that all 2 fields are printed in state view:
    - `timestamp_low` (int32)
    - `timestamp_hi` (int32)
  - [ ] **Add report entry for `struct_anon_8`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.unnamed_2` (union_anon_10)

- [ ] **Verify printing of `union_anon_10`**
  - Check that all 2 fields are printed in state view:
    - `fix_type` (int32)
    - `fix_type_packed` (int32)
  - [ ] **Add report entry for `union_anon_10`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.unnamed_3` (union_anon_11)

- [ ] **Verify printing of `union_anon_11`**
  - Check that all 2 fields are printed in state view:
    - `units_idx` (int32)
    - `units_packed` (int32)
  - [ ] **Add report entry for `union_anon_11`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `gps.unnamed_4` (union_anon_12)

- [ ] **Verify printing of `union_anon_12`**
  - Check that all 2 fields are printed in state view:
    - `device_status` (int32)
    - `device_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_12`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `header`

### `header` (struct_jon_gui_data_header)

- [ ] **Verify printing of `struct_jon_gui_data_header`**
  - Check that all 5 fields are printed in state view:
    - `version` (int32)
    - `state_update_counter` (int32)
    - `system_monotonic_time_us` (uint64)
    - `unnamed_1` (union_anon_13)
    - `unnamed_2` (union_anon_14)
  - [ ] **Add report entry for `struct_jon_gui_data_header`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `header.unnamed_1` (union_anon_13)

- [ ] **Verify printing of `union_anon_13`**
  - Check that all 2 fields are printed in state view:
    - `active_mode_id` (int32)
    - `active_mode_id_packed` (int32)
  - [ ] **Add report entry for `union_anon_13`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `header.unnamed_2` (union_anon_14)

- [ ] **Verify printing of `union_anon_14`**
  - Check that all 2 fields are printed in state view:
    - `active_screen_id` (int32)
    - `active_screen_id_packed` (int32)
  - [ ] **Add report entry for `union_anon_14`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `lens`

### `lens` (struct_jon_gui_data_lens)

- [ ] **Verify printing of `struct_jon_gui_data_lens`**
  - Check that all 40 fields are printed in state view:
    - `day_focus_pos` (int32)
    - `day_focus_pos_min` (int32)
    - `day_focus_pos_max` (int32)
    - `day_zoom_table_index` (int32)
    - `day_zoom_table_max_index` (int32)
    - `heat_zoom_table_index` (int32)
    - `heat_zoom_table_max_index` (int32)
    - `heat_focus_pos` (int32)
    - `day_zoom_pos` (int32)
    - `day_glass_temperature` (int32)
    - `day_glass_heater_enabled` (int32)
    - `day_meteo` (struct_jon_gui_data_component_meteo)
    - `day_glass_heater_meteo` (struct_jon_gui_data_component_meteo)
    - `heat_meteo` (struct_jon_gui_data_component_meteo)
    - `day_zoom_pos_min` (int32)
    - `day_zoom_pos_max` (int32)
    - `heat_zoom_pos` (int32)
    - `day_zoom_x` (int32)
    - `heat_zoom_x` (int32)
    - `day_iris_pos` (int32)
    - `day_crop_top` (int32)
    - `day_crop_bottom` (int32)
    - `day_crop_left` (int32)
    - `day_crop_right` (int32)
    - `heat_iris_pos` (int32)
    - `heat_crop_top` (int32)
    - `heat_crop_bottom` (int32)
    - `heat_crop_left` (int32)
    - `heat_crop_right` (int32)
    - `heat_dde_enabled` (int32)
    - `heat_dde_level` (int32)
    - `heat_dde_max_level` (int32)
    - `day_digital_zoom_level` (int32)
    - `heat_digital_zoom_level` (int32)
    - `day_clahe_level` (int32)
    - `heat_clahe_level` (int32)
    - `unnamed_1` (union_anon_15)
    - `unnamed_2` (union_anon_16)
    - `unnamed_3` (union_anon_17)
    - `unnamed_4` (union_anon_18)
  - [ ] **Add report entry for `struct_jon_gui_data_lens`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.day_glass_heater_meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.day_meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.heat_meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.unnamed_1` (union_anon_15)

- [ ] **Verify printing of `union_anon_15`**
  - Check that all 2 fields are printed in state view:
    - `device_status_day` (int32)
    - `device_status_day_packed` (int32)
  - [ ] **Add report entry for `union_anon_15`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.unnamed_2` (union_anon_16)

- [ ] **Verify printing of `union_anon_16`**
  - Check that all 2 fields are printed in state view:
    - `device_status_heat` (int32)
    - `device_status_heat_packed` (int32)
  - [ ] **Add report entry for `union_anon_16`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.unnamed_3` (union_anon_17)

- [ ] **Verify printing of `union_anon_17`**
  - Check that all 2 fields are printed in state view:
    - `fx_mode_day` (int32)
    - `fx_mode_day_packed` (int32)
  - [ ] **Add report entry for `union_anon_17`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lens.unnamed_4` (union_anon_18)

- [ ] **Verify printing of `union_anon_18`**
  - Check that all 2 fields are printed in state view:
    - `fx_mode_heat` (int32)
    - `fx_mode_heat_packed` (int32)
  - [ ] **Add report entry for `union_anon_18`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `lrf`

### `lrf` (struct_jon_gui_data_lrf)

- [ ] **Verify printing of `struct_jon_gui_data_lrf`**
  - Check that all 13 fields are printed in state view:
    - `scanning` (int32)
    - `measuring` (int32)
    - `refining` (int32)
    - `last_range_measured_val_1` (int32)
    - `last_range_measured_val_2` (int32)
    - `last_range_measured_val_3` (int32)
    - `fog_mode_enabled` (int32)
    - `scanning_mode_freq` (int32)
    - `measure_id` (int32)
    - `unnamed_1` (union_anon_19)
    - `error_bf` (int32)
    - `unnamed_2` (union_anon_20)
    - `meteo` (struct_jon_gui_data_component_meteo)
  - [ ] **Add report entry for `struct_jon_gui_data_lrf`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lrf.meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lrf.unnamed_1` (union_anon_19)

- [ ] **Verify printing of `union_anon_19`**
  - Check that all 2 fields are printed in state view:
    - `target_designator_status` (int32)
    - `target_designator_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_19`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `lrf.unnamed_2` (union_anon_20)

- [ ] **Verify printing of `union_anon_20`**
  - Check that all 2 fields are printed in state view:
    - `device_status` (int32)
    - `device_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_20`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `media`

### `media` (struct_jon_gui_data_media)

- [ ] **Verify printing of `struct_jon_gui_data_media`**
  - Check that all 1 fields are printed in state view:
    - `space_left_prc` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_media`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `meteo`

### `meteo` (struct_jon_gui_data_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_meteo`**
  - Check that all 6 fields are printed in state view:
    - `internal_temperature` (int32)
    - `internal_humidity` (int32)
    - `internal_pressure` (int32)
    - `external_temperature` (int32)
    - `external_humidity` (int32)
    - `external_pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `osd`

### `osd` (struct_jon_gui_data_osd)

- [ ] **Verify printing of `struct_jon_gui_data_osd`**
  - Check that all 9 fields are printed in state view:
    - `show_on_recording` (int32)
    - `crosshair_index` (int32)
    - `crosshair_size_indx` (int32)
    - `faded_opa` (int32)
    - `fade_enabled` (int32)
    - `show_photo_indicator` (int32)
    - `disable_heat_osd` (int32)
    - `disable_day_osd` (int32)
    - `unnamed_1` (union_anon_21)
  - [ ] **Add report entry for `struct_jon_gui_data_osd`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `osd.unnamed_1` (union_anon_21)

- [ ] **Verify printing of `union_anon_21`**
  - Check that all 2 fields are printed in state view:
    - `pip_pos_id` (int32)
    - `pip_pos_id_packed` (int32)
  - [ ] **Add report entry for `union_anon_21`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `power`

### `power` (struct_jon_gui_data_power)

- [ ] **Verify printing of `struct_jon_gui_data_power`**
  - Check that all 9 fields are printed in state view:
    - `s0` (struct_jon_gui_data_power_module_state)
    - `s1` (struct_jon_gui_data_power_module_state)
    - `s2` (struct_jon_gui_data_power_module_state)
    - `s3` (struct_jon_gui_data_power_module_state)
    - `s4` (struct_jon_gui_data_power_module_state)
    - `s5` (struct_jon_gui_data_power_module_state)
    - `s6` (struct_jon_gui_data_power_module_state)
    - `s7` (struct_jon_gui_data_power_module_state)
    - `meteo` (struct_jon_gui_data_component_meteo)
  - [ ] **Add report entry for `struct_jon_gui_data_power`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s0` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s0.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s1` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s1.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s2` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s2.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s3` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s3.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s4` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s4.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s5` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s5.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s6` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s6.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s7` (struct_jon_gui_data_power_module_state)

- [ ] **Verify printing of `struct_jon_gui_data_power_module_state`**
  - Check that all 8 fields are printed in state view:
    - `voltage` (int32)
    - `current` (int32)
    - `power` (int32)
    - `is_alarm` (int32)
    - `can_cmd_address` (int32)
    - `can_data_address` (int32)
    - `is_power_on` (int32)
    - `unnamed_1` (union_anon_24)
  - [ ] **Add report entry for `struct_jon_gui_data_power_module_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `power.s7.unnamed_1` (union_anon_24)

- [ ] **Verify printing of `union_anon_24`**
  - Check that all 2 fields are printed in state view:
    - `can_device` (int32)
    - `can_device_packed` (int32)
  - [ ] **Add report entry for `union_anon_24`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Root Structure

### Main Structure (struct_jon_gui_state)

- [ ] **Verify printing of `struct_jon_gui_state`**
  - Check that all 18 fields are printed in state view:
    - `header` (struct_jon_gui_data_header)
    - `compass` (struct_jon_gui_data_compass)
    - `compass_calibration` (struct_jon_gui_data_compass_calibration)
    - `colors` (struct_jon_gui_data_colors)
    - `time` (struct_jon_gui_data_time)
    - `gps` (struct_jon_gui_data_gps)
    - `lrf` (struct_jon_gui_data_lrf)
    - `media` (struct_jon_gui_data_media)
    - `system` (struct_jon_gui_data_system)
    - `osd` (struct_jon_gui_data_osd)
    - `targets` (struct_jon_gui_data_targets)
    - `camera_alignment` (struct_jon_gui_data_camera_alignment)
    - `meteo` (struct_jon_gui_data_meteo)
    - `lens` (struct_jon_gui_data_lens)
    - `rotary` (struct_jon_gui_data_rotary)
    - `power` (struct_jon_gui_data_power)
    - `cv` (struct_jon_gui_data_cv)
    - `debug` (struct_anon_41)
  - [ ] **Add report entry for `struct_jon_gui_state`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `rotary`

### `rotary` (struct_jon_gui_data_rotary)

- [ ] **Verify printing of `struct_jon_gui_data_rotary`**
  - Check that all 33 fields are printed in state view:
    - `platform_azimuth` (int32)
    - `platform_elevation` (int32)
    - `platform_bank` (int32)
    - `use_platform_positioning` (int32)
    - `head_azimuth` (int32)
    - `head_elevation` (int32)
    - `head_bank` (int32)
    - `speed_azimuth` (int32)
    - `speed_elevation` (int32)
    - `speed_bank` (int32)
    - `set_azimuth` (int32)
    - `set_elevation` (int32)
    - `set_speed_azimuth` (int32)
    - `set_speed_elevation` (int32)
    - `set_azimuth_dir` (int32)
    - `set_elevation_dir` (int32)
    - `set_azimuth_offset` (int32)
    - `is_scanning` (int32)
    - `is_scanning_paused` (int32)
    - `scan_target` (int32)
    - `scan_target_max` (int32)
    - `scan_cur_target_azimuth` (int32)
    - `scan_cur_target_elevation` (int32)
    - `scan_cur_target_day_zoom_table_index` (int32)
    - `scan_cur_target_heat_zoom_table_index` (int32)
    - `scan_cur_target_linger` (int32)
    - `scan_cur_target_speed` (int32)
    - `unnamed_1` (union_anon_22)
    - `unnamed_2` (union_anon_23)
    - `meteo` (struct_jon_gui_data_component_meteo)
    - `rotary_init` (int32)
    - `pan_init` (int32)
    - `tilt_init` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_rotary`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `rotary.meteo` (struct_jon_gui_data_component_meteo)

- [ ] **Verify printing of `struct_jon_gui_data_component_meteo`**
  - Check that all 3 fields are printed in state view:
    - `temperature` (int32)
    - `humidity` (int32)
    - `pressure` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_component_meteo`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `rotary.unnamed_1` (union_anon_22)

- [ ] **Verify printing of `union_anon_22`**
  - Check that all 2 fields are printed in state view:
    - `device_status` (int32)
    - `device_status_packed` (int32)
  - [ ] **Add report entry for `union_anon_22`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `rotary.unnamed_2` (union_anon_23)

- [ ] **Verify printing of `union_anon_23`**
  - Check that all 2 fields are printed in state view:
    - `mode` (int32)
    - `mode_packed` (int32)
  - [ ] **Add report entry for `union_anon_23`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `system`

### `system` (struct_jon_gui_data_system)

- [ ] **Verify printing of `struct_jon_gui_data_system`**
  - Check that all 31 fields are printed in state view:
    - `enable_video_recording` (int32)
    - `recording_is_important` (int32)
    - `disk_space_percent_taken` (int32)
    - `day_af_enable` (int32)
    - `day_ae_enable` (int32)
    - `day_air_enable` (int32)
    - `heat_af_enable` (int32)
    - `heat_filter_value` (int32)
    - `irf_enable` (int32)
    - `is_enable` (int32)
    - `agc_mode` (int32)
    - `enable_zoom_sync` (int32)
    - `eth_enabled` (int32)
    - `wifi_enabled` (int32)
    - `enable_continuous_zoom` (int32)
    - `shutdown_timer_running` (int32)
    - `geodesic_mode_enabled` (int32)
    - `unnamed_1` (union_anon_25)
    - `unnamed_2` (union_anon_26)
    - `unnamed_3` (union_anon_27)
    - `unnamed_4` (union_anon_28)
    - `unnamed_5` (union_anon_29)
    - `unnamed_6` (union_anon_30)
    - `cur_video_rec_dir_year` (int32)
    - `cur_video_rec_dir_month` (int32)
    - `cur_video_rec_dir_day` (int32)
    - `cur_video_rec_dir_hour` (int32)
    - `cur_video_rec_dir_minute` (int32)
    - `cur_video_rec_dir_second` (int32)
    - `low_disk_space` (int32)
    - `no_disk_space` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_system`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_1` (union_anon_25)

- [ ] **Verify printing of `union_anon_25`**
  - Check that all 2 fields are printed in state view:
    - `localization_id` (int32)
    - `localization_id_packed` (int32)
  - [ ] **Add report entry for `union_anon_25`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_2` (union_anon_26)

- [ ] **Verify printing of `union_anon_26`**
  - Check that all 2 fields are printed in state view:
    - `active_video_channel` (int32)
    - `active_video_channel_packed` (int32)
  - [ ] **Add report entry for `union_anon_26`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_3` (union_anon_27)

- [ ] **Verify printing of `union_anon_27`**
  - Check that all 2 fields are printed in state view:
    - `active_thermal_color_filter_idx` (int32)
    - `active_thermal_color_filter_packed` (int32)
  - [ ] **Add report entry for `union_anon_27`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_4` (union_anon_28)

- [ ] **Verify printing of `union_anon_28`**
  - Check that all 2 fields are printed in state view:
    - `active_day_filter_idx` (int32)
    - `active_day_filter_packed` (int32)
  - [ ] **Add report entry for `union_anon_28`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_5` (union_anon_29)

- [ ] **Verify printing of `union_anon_29`**
  - Check that all 2 fields are printed in state view:
    - `acccumulator_stat_idx` (int32)
    - `acccumulator_stat_idx_packed` (int32)
  - [ ] **Add report entry for `union_anon_29`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `system.unnamed_6` (union_anon_30)

- [ ] **Verify printing of `union_anon_30`**
  - Check that all 2 fields are printed in state view:
    - `sd_card_stat_idx` (int32)
    - `sd_card_stat_idx_packed` (int32)
  - [ ] **Add report entry for `union_anon_30`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `targets`

### `targets` (struct_jon_gui_data_targets)

- [ ] **Verify printing of `struct_jon_gui_data_targets`**
  - Check that all 4 fields are printed in state view:
    - `last_target` (struct_jon_gui_data_target_spec)
    - `target_viewr_current_target` (struct_jon_gui_data_target_spec)
    - `recorded_targets_count` (int32)
    - `screenshot_state` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_targets`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.last_target` (struct_jon_gui_data_target_spec)

- [ ] **Verify printing of `struct_jon_gui_data_target_spec`**
  - Check that all 18 fields are printed in state view:
    - `target_id` (int32)
    - `target_index` (int32)
    - `uuid` (int32[4], array[4])
    - `target_longitude` (int32)
    - `target_latitude` (int32)
    - `target_height` (int32)
    - `observer_id` (int32)
    - `unnamed_1` (union_anon_31)
    - `observer_longitude` (int32)
    - `observer_latitude` (int32)
    - `observer_azimuth` (int32)
    - `observer_elevation` (int32)
    - `observer_altitude` (int32)
    - `distance_a` (int32)
    - `distance_b` (int32)
    - `has_range` (int32)
    - `session_id` (int32)
    - `unnamed_2` (union_anon_32)
  - [ ] **Add report entry for `struct_jon_gui_data_target_spec`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.last_target.unnamed_1` (union_anon_31)

- [ ] **Verify printing of `union_anon_31`**
  - Check that all 2 fields are printed in state view:
    - `observer_timestamp` (int64)
    - `observer_timestamp_packed` (int64)
  - [ ] **Add report entry for `union_anon_31`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.last_target.unnamed_2` (union_anon_32)

- [ ] **Verify printing of `union_anon_32`**
  - Check that all 2 fields are printed in state view:
    - `observer_fix_type` (int32)
    - `observer_fix_type_packed` (int32)
  - [ ] **Add report entry for `union_anon_32`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.target_viewr_current_target` (struct_jon_gui_data_target_spec)

- [ ] **Verify printing of `struct_jon_gui_data_target_spec`**
  - Check that all 18 fields are printed in state view:
    - `target_id` (int32)
    - `target_index` (int32)
    - `uuid` (int32[4], array[4])
    - `target_longitude` (int32)
    - `target_latitude` (int32)
    - `target_height` (int32)
    - `observer_id` (int32)
    - `unnamed_1` (union_anon_31)
    - `observer_longitude` (int32)
    - `observer_latitude` (int32)
    - `observer_azimuth` (int32)
    - `observer_elevation` (int32)
    - `observer_altitude` (int32)
    - `distance_a` (int32)
    - `distance_b` (int32)
    - `has_range` (int32)
    - `session_id` (int32)
    - `unnamed_2` (union_anon_32)
  - [ ] **Add report entry for `struct_jon_gui_data_target_spec`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.target_viewr_current_target.unnamed_1` (union_anon_31)

- [ ] **Verify printing of `union_anon_31`**
  - Check that all 2 fields are printed in state view:
    - `observer_timestamp` (int64)
    - `observer_timestamp_packed` (int64)
  - [ ] **Add report entry for `union_anon_31`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `targets.target_viewr_current_target.unnamed_2` (union_anon_32)

- [ ] **Verify printing of `union_anon_32`**
  - Check that all 2 fields are printed in state view:
    - `observer_fix_type` (int32)
    - `observer_fix_type_packed` (int32)
  - [ ] **Add report entry for `union_anon_32`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

## Field: `time`

### `time` (struct_jon_gui_data_time)

- [ ] **Verify printing of `struct_jon_gui_data_time`**
  - Check that all 4 fields are printed in state view:
    - `unnamed_1` (union_anon_34)
    - `unnamed_2` (union_anon_36)
    - `zone_id` (int32)
    - `use_manual_time` (int32)
  - [ ] **Add report entry for `struct_jon_gui_data_time`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `time.unnamed_1` (union_anon_34)

- [ ] **Verify printing of `union_anon_34`**
  - Check that all 2 fields are printed in state view:
    - `timestamp` (int64)
    - `unnamed_1` (struct_anon_33)
  - [ ] **Add report entry for `union_anon_34`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `time.unnamed_1.unnamed_1` (struct_anon_33)

- [ ] **Verify printing of `struct_anon_33`**
  - Check that all 2 fields are printed in state view:
    - `timestamp_low` (int32)
    - `timestamp_hi` (int32)
  - [ ] **Add report entry for `struct_anon_33`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `time.unnamed_2` (union_anon_36)

- [ ] **Verify printing of `union_anon_36`**
  - Check that all 2 fields are printed in state view:
    - `manual_timestamp` (int64)
    - `unnamed_1` (struct_anon_35)
  - [ ] **Add report entry for `union_anon_36`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

### `time.unnamed_2.unnamed_1` (struct_anon_35)

- [ ] **Verify printing of `struct_anon_35`**
  - Check that all 2 fields are printed in state view:
    - `manual_timestamp_low` (int32)
    - `manual_timestamp_hi` (int32)
  - [ ] **Add report entry for `struct_anon_35`**
    - Document which fields are correctly printed
    - Note any missing or incorrectly formatted fields
    - Add recommendations for fixes if needed

---

## Summary Statistics

- Total structures to verify: 96
- Total todo items: 192 (2 per struct)

## Completion Tracking

- [ ] All struct printing verified
- [ ] All report entries added
- [ ] Final review completed