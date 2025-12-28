
# Gazebo (GZ) Simulation Guide

This section covers running PX4 simulations using the modern Gazebo (GZ) simulator (formerly Ignition). We cover standard execution, performance optimization, and advanced workflow setups.

---

## 📋 Table of Contents

1. [Standard Launch](#1-standard-launch)  
2. [Performance: Headless Mode](#2-performance-headless-mode)  
3. [Custom Spawn Points (Environment Variables)](#3-custom-spawn-points-environment-variables)  
4. [Multi-Vehicle Simulation](#5-multi-vehicle-simulation)  
5. [Custom Worlds & Models](#6-custom-worlds--models)  
6. [Debugging & Physics Settings](#7-debugging--physics-settings)  

---

## 1. Standard Launch

The most common way to start a simulation is using the `make` command from the root of the `PX4-Autopilot` directory. This compiles the code, launches the Gazebo GUI, and spawns the drone.

**Syntax:**

```bash
make px4_sitl gz_[model]_[world]
```
>    **Note:** Don't close the gazebo's window, close the gazebo terminal by clicking ' Ctrl + c'

**Common Examples:**

```bash
# Run a standard x500 quadcopter in the default world
make px4_sitl gz_x500

# Or a model with a camera
make px4_sitl gz_x500_mono_cam_balylands
```

> **Note:** If you do not specify a world, it defaults to the empty or default plane world.

---


## 3. Custom Spawn Points (Environment Variables)

By default, PX4 spawns the drone at a predefined coordinate (often Zurich). To test autonomous missions in specific locations (e.g., matching a real-world test site), you can override the home location using environment variables.

**Variables to set:**

- `PX4_HOME_LAT`: Latitude  
- `PX4_HOME_LON`: Longitude  
- `PX4_HOME_ALT`: Altitude (AMSL)

**Example Command:**

```bash
# Spawns the drone at specific coordinates
PX4_HOME_LAT=24.7136 PX4_HOME_LON=46.6753 PX4_HOME_ALT=600 make px4_sitl gz_x500
```
> **Note:** There is alot of other Environment Variables, see [Usage/Configuration Options](https://docs.px4.io/main/en/sim_gazebo_gz/#usage-configuration-options)
---


## 4. Multi-Vehicle Simulation

Running multiple drones is essential for swarm testing. PX4 provides a script to handle instance creation (assigning unique ports and MAVLink IDs to each drone).

```bash
ARGS ./build/px4_sitl_default/bin/px4 [-i <instance>]
```

**For the first drone:** lunch the drone with the world:

```bash
PX4_SYS_AUTOSTART=4001 PX4_SIM_MODEL=gz_x500 PX4_SIM_MAVSDK_UDP_PORT=14540 PX4_SIM_QGC_UDP_PORT=14550 ./build/px4_sitl_default/bin/px4 -i 0
```
**For the other drones:** launch them with `PX4_GZ_STANDALONE=1`:
```bash
PX4_GZ_STANDALONE=1 PX4_SYS_AUTOSTART=4001 PX4_GZ_MODEL_POSE="0,2,0" PX4_SIM_MAVSDK_UDP_PORT=14542 PX4_SIM_QGC_UDP_PORT=14552 ./build/px4_sitl_default/bin/px4 -i 2
```
**Key Considerations:**

- **Instance IDs:** Drone 1 will use MAVLink ID 1 (Port 14550), Drone 2 uses ID 2 (Port 14551), etc.  
- **QGroundControl:** Will automatically detect all instances if they are on localhost.
  
---

## 5. Custom Worlds & Models

To use your own assets, you need to tell Gazebo where to look for them.

### A. Environment Variables for Resources

If you have a folder named `my_simulation` containing `models/` and `worlds/`, export the path:

```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/path/to/my_simulation/models:/path/to/my_simulation/worlds
```

### B. Creating a Custom World

Create an `.sdf` file (e.g., `desert.sdf`). To launch PX4 inside this world:

```bash
make px4_sitl gz_x500_desert
```

> **Note:** The build system looks for `desert.sdf` in the recognized resource paths.

---

## 6. Debugging & Physics Settings

### GZ Debugging Tools

When the Gazebo GUI is open, use the **Component Inspector** (right-side panel) to:

- **View Collisions:** See the actual physical hitboxes (often different from the visual mesh).  
- **View Center of Mass:** Verify your drone is balanced.  
- **Apply Forces:** Manually push the drone to test PID stability.

### Physics Settings (Lockstep)

PX4 and Gazebo run in **Lockstep**.

- **How it works:** PX4 pauses the simulation clock until it receives sensor data from Gazebo.  
- **Symptom:** If your computer is slow, the simulation will appear to "lag" or run in slow motion, but the physics will remain accurate.  
- **Debugging:** If you suspect Lockstep is hiding issues, you can disable it in the `.sdf` plugin settings (not recommended for general flight).

### Real Time Factor (RTF)

Look at the bottom of the Gazebo window.

- **RTF = 1.0:** Simulation is running at real-world speed.  
- **RTF < 1.0:** Simulation is running slower than real-time (computer is struggling).  
- **RTF > 1.0:** Simulation is fast-forwarding (common in Headless mode).
  
### Command-Line Debugging (gz Tools)
**For deep inspection without the GUI, you can use the command-line tools:**

- `gz topic -e [topic_name]`: Echo the data being published on a Gazebo topic (e.g., sensor readings, model states). This is the equivalent of rostopic echo in ROS.
- `gz topic -l`: List all active Gazebo topics being published by the simulator.
- `gz stats`: Prints detailed simulation statistics, including the current RTF, iteration rate, and time step, which is useful for logging performance over time.
- 
---
