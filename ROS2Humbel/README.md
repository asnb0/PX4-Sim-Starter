# ROS 2 Humble Installation Guide on Ubuntu 22.04

This guide explains how to install **ROS 2 Humble Hawksbill** on **Ubuntu 22.04 (Jammy)** using `apt` packages.  
It is based on the official ROS documentation:

**Official docs:** https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html  

---

## 📋 Table of Contents

1. [Overview](#1-overview)  
2. [System Requirements](#2-system-requirements)  
3. [Step 1 – Update System](#3-step-1--update-system)  
4. [Step 2 – Set Locale (UTF-8)](#4-step-2--set-locale-utf-8)  
5. [Step 3 – Add ROS 2 Repository](#5-step-3--add-ros-2-repository)  
6. [Step 4 – Install ROS 2 Humble](#6-step-4--install-ros-2-humble)  
7. [Step 5 – Environment Setup](#7-step-5--environment-setup)  
8. [Step 6 – Quick Test (Talker / Listener)](#8-step-6--quick-test-talker--listener)  

---

## 1. Overview

ROS 2 Humble is a **Long-Term Support (LTS)** release of ROS 2, officially targeting **Ubuntu 22.04**.  
This document is intended to be a **clean and clear reference** that you can share with students or reuse on multiple machines.

> ✅ **Goal:** After following this guide, you should be able to run `ros2` commands and launch demo nodes without issues.

---

## 2. System Requirements

- **OS:** Ubuntu 22.04 (Jammy) 64-bit  
- **Privileges:** User account with `sudo` access  
- **Internet:** Required to download packages from Ubuntu and ROS repositories  

> ⚠️ **Note:** Humble is officially supported **only** on Ubuntu 22.04. Using a different Ubuntu version may cause problems or require extra manual setup.

---

## 3. Step 1 – Update System

Before installing ROS 2, it is recommended to make sure your system is up to date.

```bash
sudo apt update
sudo apt upgrade
```
💡 Tip: It’s a good idea to reboot after a large upgrade:

```bash
sudo reboot
```

---

## 4. Step 2 – Set Locale (UTF-8)

ROS 2 tools expect the system to use a **UTF-8** locale.

Check current locale:

```bash
locale
```
If you don’t see UTF-8, configure it:
```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Verify again
locale
```
✅ You should now see en_US.UTF-8 (or another UTF-8 locale) in the output.

---
## 5. Step 3 – Add ROS 2 APT Repository

5.1 Enable the universe repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```
5.2 Install ros2-apt-source

This package configures the ROS 2 APT repository and keys automatically.
```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```
Then refresh the package list:

```bash
sudo apt update
```
---
## 6. Step 4 – Install ROS 2 Humble

Full ROS 2 environment with GUI tools (RViz, demos, etc.):

```bash
sudo apt install ros-humble-desktop
```
---
## 7. Step 5 – Environment Setup
append it to your ~/.bashrc:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
---
## 8. Step 6 – Quick Test (Talker / Listener)
Open two terminals.

Terminal 1 – C++ Talker

```bash
ros2 run demo_nodes_cpp talker
```
You should see output similar to:
[INFO] [talker]: Publishing: 'Hello World: 1'

Terminal 2 – Python Listener:
```bash
ros2 run demo_nodes_py listener
```
You should see:
[INFO] [listener]: I heard: 'Hello World: 1'

✅ If terminal 1 is publishing and terminal 2 is receiving messages, your ROS 2 installation is working correctly.

