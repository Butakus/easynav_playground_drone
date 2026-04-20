# EasyNav Playground Drone

## Installation

```bash
cd <easynav-workspace>
vcs import --recursive src < easynav_playground_drone/thirdparty.repos
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install 
```

## Usage

```bash
ros2 launch easynav_playground_drone playground_drone.launch.py
```

or

```bash
ros2 launch easynav_playground_drone playground_drone.launch.py world:=<path-to-world>
```
