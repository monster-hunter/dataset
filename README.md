# dataset

Dataset collected with Intel RealSense camera on NVIDIA Jetson Thor.

## Dataset Contents

- `2026-01-29.zip` — RGB image frames captured on 2026-01-29

## Jetson Thor + RealSense Setup

### Problem: Color Images Not Received (Depth Works Fine)

On **NVIDIA Jetson Thor** (ARM architecture), the Intel RealSense camera's color stream defaults to **MJPEG** encoding. MJPEG hardware decoding is not properly supported on Jetson's ARM platform through the standard UVC driver, which causes:

- ✅ Depth stream works correctly
- ❌ Color (RGB) stream produces no frames

### Root Cause

The `realsense2_camera` ROS 2 driver uses MJPEG as the default color encoding for higher efficiency on x86 systems. On ARM/Jetson platforms this decoding path is not available via the kernel UVC driver, so color frames are silently dropped.

### Fix

Set the color stream format to `rgb8` (or `bgr8`/`yuyv` as alternatives) instead of the default MJPEG encoding.

#### Option 1 — Use the provided launch file

```bash
ros2 launch launch/rs_jetson_launch.py
```

The `launch/rs_jetson_launch.py` file already sets `color_format:=rgb8` as the default.

To override resolution or format at runtime:

```bash
ros2 launch launch/rs_jetson_launch.py \
    color_width:=1280 color_height:=720 color_fps:=30 color_format:=rgb8
```

#### Option 2 — Use the provided config file

Pass `config/realsense_jetson.yaml` as parameters when launching the RealSense node:

```bash
ros2 run realsense2_camera realsense2_camera_node \
    --ros-args --params-file config/realsense_jetson.yaml
```

#### Option 3 — Inline launch argument

If you use the upstream `realsense2_camera` launch file directly, add `color_format:=rgb8`:

```bash
ros2 launch realsense2_camera rs_launch.py \
    color_width:=640 color_height:=480 color_fps:=30 color_format:=rgb8
```

### Additional Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Color stream blank / no frames | MJPEG not decoded on ARM | Set `color_format:=rgb8` |
| Both streams drop intermittently | USB bandwidth saturation | Use a dedicated USB 3.2 port; avoid sharing the controller with other devices |
| Color works in `realsense-viewer` but not ROS 2 | ROS 2 driver parameter issue | Use the config/launch files above |
| No streams at all | Insufficient USB power | Use a powered USB hub or the Jetson barrel jack power supply |

### Verified Configuration

| Component | Version |
|-----------|---------|
| Hardware | NVIDIA Jetson Thor |
| Camera | Intel RealSense D455 / D555 |
| ROS 2 | Humble / Iron |
| librealsense | ≥ 2.54.0 |
| realsense2_camera | ≥ 4.51.1 |