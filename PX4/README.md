# 🛩 PX4 Simulation Using jMAVSim on Ubuntu 22.04

This guide walks you through installing **PX4 Autopilot** with **jMAVSim** on a native Ubuntu 22.04 system.

---

## ✅ 1. Update Your System

Before installing anything, update your packages:

```bash
cd
sudo apt update && sudo apt upgrade -y
```

---

## 📦 2. Install Required Dependencies

### Install Ant:
```bash
sudo apt install ant -y
```

### Install JDK 11 (required for jMAVSim):
```bash
sudo apt install openjdk-11-jdk -y
```

### ✔ Verify Java Version  
You must be using **Java 11**:

```bash
java -version
```

If needed, select the correct version:

```bash
sudo update-alternatives --config java
```

---

## 🔄 3. Clone the PX4-Autopilot Repository

Clone PX4 with all submodules:

```bash
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
```

---

## ⚙️ 4. Run the PX4 Installation Script

Navigate into the repository:

```bash
cd ~/PX4-Autopilot
```

Run the setup script:

```bash
bash ./Tools/setup/ubuntu.sh
```

Test the simulation:

```bash
make px4_sitl jmavsim
```

### If it works, you're done ✅  
If not, continue with the next steps below.

---

## 🔧 5. Clean Build Environment

```bash
cd ~/PX4-Autopilot
make distclean
make clean
```

Run the setup script again:

```bash
bash ./Tools/setup/ubuntu.sh
```

---

## 🚀 6. Run jMAVSim

```bash
cd ~/PX4-Autopilot
make px4_sitl jmavsim
```

And that is it, enjoy the flight! 🛫

---
