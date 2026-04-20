# EasyNav Playground Drone

## Pre-requisites

```bash
pip3 install kconfiglib
```

## Installation

```bash
cd <easynav-workspace>
vcs import --recursive src < src/easynav_playground_drone/thirdparty.repos
cd <easynav-workspace>/src
git submodule update --recursive
cd <easynav-workspace>
.src/ThirdParty/robots/drone/PX4-Autopilot/Tools/setup/ubuntu.sh
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
