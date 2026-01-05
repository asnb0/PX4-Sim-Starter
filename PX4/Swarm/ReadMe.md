# Running Swarm Using PX4
---
This guide demonstrates how to run **three PX4 drones** using **Gazebo (gz sim)** and **MAVSDK**.  
You will need **three terminals** — one for each PX4 instance.
---
## Before starting, make sure you have:

- **PX4-Autopilot** cloned and built (`make px4_sitl_default`)
- **Gazebo (gz sim)** installed and configured
- **MAVSDK** and **QGroundControl** ready (optional, for testing)
- **Ports not already in use**

---

## Step 1: Launch the First Drone

Open the **first terminal** and start the first PX4 instance:

```bash
PX4_SYS_AUTOSTART=4001 PX4_SIM_MODEL=gz_x500 PX4_SIM_MAVSDK_UDP_PORT=14540 PX4_SIM_QGC_UDP_PORT=14550 ./build/px4_sitl_default/bin/px4 -i 0
```

This spawns **Drone #1** at the default position `(0, 0, 0)`.

---

## Step 2: Launch the Second Drone

In the **second terminal**, start the second PX4 instance with a different MAVSDK and QGC port:

```bash
PX4_GZ_STANDALONE=1 PX4_SYS_AUTOSTART=4001 PX4_GZ_MODEL_POSE="0,1,0" PX4_SIM_MAVSDK_UDP_PORT=14541 PX4_SIM_QGC_UDP_PORT=14551 ./build/px4_sitl_default/bin/px4 -i 1
```

This spawns **Drone #2** at position `(0, 1, 0)`.

---

## Step 3: Launch the Third Drone

In the **third terminal**, start the third PX4 instance:

```bash
PX4_GZ_STANDALONE=1 PX4_SYS_AUTOSTART=4001 PX4_GZ_MODEL_POSE="0,2,0" PX4_SIM_MAVSDK_UDP_PORT=14542 PX4_SIM_QGC_UDP_PORT=14552 ./build/px4_sitl_default/bin/px4 -i 2
```

This spawns **Drone #3** at position `(0, 2, 0)`.

---

## NOW Connect Using MAVSDK

You can now control each drone programmatically using MAVSDK-Python or MAVSDK-C++.

Example connection strings:

| Drone | MAVSDK Connection | QGC Connection |
|--------|-------------------|----------------|
| Drone #1 | `udp://:14540` | `udp://:14550` |
| Drone #2 | `udp://:14541` | `udp://:14551` |
| Drone #3 | `udp://:14542` | `udp://:14552` |
