# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a ROS (Robot Operating System) catkin package containing a URDF model of a humanoid robot named "simstl装配另存". The URDF was auto-generated using the SolidWorks to URDF Exporter (sw_urdf_exporter).

## Build Commands

```bash
# Build the package (from catkin workspace root)
catkin_make

# Or using catkin build
catkin build simstl装配另存
```

## Running the Robot

```bash
# Visualize in RViz with joint state publisher GUI
roslaunch simstl装配另存 display.launch

# Spawn in Gazebo simulation
roslaunch simstl装配另存 gazebo.launch
```

## Package Structure

- `urdf/simstl装配另存.urdf` - Main robot description file defining links, joints, and kinematic chain
- `meshes/` - STL mesh files for each robot link (visual and collision geometry)
- `launch/display.launch` - RViz visualization with joint_state_publisher_gui
- `launch/gazebo.launch` - Gazebo simulation spawner
- `config/joint_names_*.yaml` - Controller joint name configuration

## Robot Architecture

The humanoid has a pelvis-centered kinematic tree with:
- **Legs**: 6 DOF each (hip pitch/roll/yaw, knee, ankle pitch/roll)
- **Torso**: waist yaw/roll, torso joint
- **Arms**: shoulder pitch/roll/yaw, elbow, wrist roll/pitch/yaw
- **Head**: single head joint

All joints are defined as `continuous` type (unlimited rotation). The base link is `pelvis_link`.
