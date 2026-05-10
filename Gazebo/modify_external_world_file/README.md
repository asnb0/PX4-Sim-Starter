## Making Downloaded Gazebo Worlds Work with PX4 SITL

This folder demonstrates a **common issue when using Gazebo worlds downloaded from the internet with PX4 SITL**, and how to correctly fix it.

### 📂 Files in this folder

* **`forest.sdf`**
  A **reference world** taken directly from the PX4 repository.
  This world works correctly with PX4 **without any modification**.

* **`tugbot_warehouse(original).sdf`**
  The original warehouse world downloaded from
  [https://app.gazebosim.org](https://app.gazebosim.org/MovAi/fuel/worlds/tugbot_warehouse)
  This file **does NOT work correctly with PX4 SITL** when used as-is.

* **`tugbot_warehouse.sdf`**
  The **fixed version**, modified by comparing it with `forest.sdf` and adapting it to PX4 requirements.

---

## ❗ Why downloaded worlds often fail with PX4

Most worlds found online are designed for **general Gazebo simulation**, not for **PX4 flight control systems**. PX4 has **strict timing, sensor, and environment requirements** that many public worlds do not satisfy.

When running the original `tugbot_warehouse(original).sdf` with PX4, the following problems were observed:

### 🚨 Identified Issues

1. **Missing magnetic field**

   * The world does not define a `<magnetic_field>`
   * Result: PX4 magnetometer / compass does not work correctly → EKF issues

2. **Manual Gazebo system plugins**

   * The world explicitly declares Gazebo system plugins
   * This conflicts with PX4’s expected simulation setup

3. **Incorrect physics timing**

   * `<max_step_size>` is too large (`0.01`)
   * Sensors update too slowly for PX4’s EKF

4. **Missing atmosphere definition**

   * No `<atmosphere>` tag
   * Leads to incomplete environmental modeling

5. **Missing spherical coordinates**

   * PX4 expects a defined world frame (ENU) and Earth reference
   * Without it, navigation and orientation assumptions may break
  
6. **Mismatch naming**
   * The name of the world file must match the name written inside the file -> "<world_name='<name of the file>'>"


---

## ✅ How the world was fixed (step by step)

To make the downloaded world compatible with PX4, we **used `forest.sdf` as a reference** and applied the following changes.

---

### 1️⃣ Add a magnetic field (required for compass)

```xml
<magnetic_field>6e-06 2.3e-05 -4.2e-05</magnetic_field>
```

📌 Without this, PX4’s magnetometer will not behave correctly.

---

### 2️⃣ Fix physics timing for PX4 EKF

```xml
<physics type="ode">
  <max_step_size>0.004</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>250</real_time_update_rate>
</physics>
```

📌 PX4 requires **fast and stable sensor updates**.
Large step sizes (e.g. `0.01`) often cause arming and takeoff failures.

---

### 3️⃣ Remove manual Gazebo system plugins

All `<plugin>` entries that load Gazebo systems manually were **removed**, for example:

```xml
<plugin name="ignition::gazebo::systems::Physics" ... />
<plugin name="ignition::gazebo::systems::Sensors" ... />
```

📌 These plugins are commonly included in public worlds but can **conflict with PX4’s simulation assumptions**.

---

### 4️⃣ Add an atmosphere model

```xml
<atmosphere type="adiabatic"/>
```

📌 This ensures a complete and stable environment definition.

---

### 5️⃣ Add spherical coordinates (VERY IMPORTANT)

The following block was added **before the closing `</world>` tag**:

```xml
<spherical_coordinates>
  <surface_model>EARTH_WGS84</surface_model>
  <world_frame_orientation>ENU</world_frame_orientation>
  <latitude_deg>47.397971057728974</latitude_deg>
  <longitude_deg>8.546163739800146</longitude_deg>
  <elevation>0</elevation>
</spherical_coordinates>
```

📌 PX4 assumes:

* **ENU coordinate frame**
* **Earth-referenced environment**

This block is present in PX4 worlds such as `forest.sdf` and should always be added when adapting external worlds.

---

## 🧠 Key takeaway

> **If a Gazebo world works in Gazebo but fails in PX4, the problem is usually the world file — not PX4.**

When downloading a world from the internet, always check:

✔ Magnetic field
✔ Physics timing (`max_step_size = 0.004`)
✔ No manual system plugins
✔ Atmosphere definition
✔ Spherical coordinates (ENU + WGS84)

---

## 🚀 Running the fixed world with PX4

```bash
PX4_GZ_WORLD=tugbot_warehouse make px4_sitl gz_x500
```

Make sure:

* The world file name matches `PX4_GZ_WORLD`
* The `.sdf` file is in a Gazebo-searchable directory

---

###  Final note

This example shows a **real-world debugging workflow**:

1. World downloaded from Fuel ❌
2. Compare with PX4 reference world
3. Fix environment + physics + sensors
4. World works correctly with PX4 ✅

This is a **core skill** when working with PX4 + Gazebo.

---
