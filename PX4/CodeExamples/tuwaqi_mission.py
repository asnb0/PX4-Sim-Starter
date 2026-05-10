# Objective: Designing the Tuwaiq logo in QGround Control

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan


async def create_mission(lat, lon):
    mission = MissionItem(lat,lon,5,4,True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                     3, float('nan'), 0, 0,
                    float('nan'),MissionItem.VehicleAction.NONE)
    return mission

async def pos_htarget(drone: System, target_min: float, target_max: float):
    async for pos in drone.telemetry.position():
        if pos.relative_altitude_m >= target_min and pos.relative_altitude_m <=  target_max:
            print("Drone reached default takeoff altitude!")
            break

async def battery_checker(drone: System):
    async for battery in drone.telemetry.battery():
        if battery.remaining_percent < 20:
            print("Battery low! Returning to launch...")
            await drone.action.return_to_launch()
            break

async def main():
    t_drone = System()
    print("Connecting to PX4...")
    await t_drone.connect(system_address="udp://:14540")
    async for con in t_drone.core.connection_state():
        if con.is_connected:
            print("Tuwaiq Drone is connected")
            battery_task = asyncio.create_task(battery_checker(t_drone)) # Start checking for the battery status
            # We assigned the create_task() to a variable "battery_task", so we can stop the task later!
            break


    home = await anext(t_drone.telemetry.home())
    h_lat = home.latitude_deg
    h_lon = home.longitude_deg
    fly_alt = 5

    mission_items = []

    mission_items.append(MissionItem(h_lat + 10*1e-5,h_lon,fly_alt,4,True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    3, float('nan'), 0, 0,
                    float('nan'),MissionItem.VehicleAction.NONE))
    
    mission_items.append(MissionItem(h_lat + 20*1e-5,h_lon + 20*1e-5,fly_alt,4,True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    3, float('nan'), 0, 0,
                    float('nan'),MissionItem.VehicleAction.NONE))
    
    mission_items.append(MissionItem(h_lat + 30*1e-5,h_lon + 20*1e-5,fly_alt,4,True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                     3, float('nan'), 0, 0,
                    float('nan'),MissionItem.VehicleAction.NONE))
    
    mission_items.append(await create_mission(h_lat + 30*1e-5, h_lon + 30*1e-5))
    mission_items.append(await create_mission(h_lat + 20*1e-5, h_lon + 30*1e-5))
    mission_items.append(await create_mission(h_lat + 20*1e-5, h_lon + 40*1e-5))
    mission_items.append(await create_mission(h_lat + 10*1e-5, h_lon + 40*1e-5))
    mission_items.append(await create_mission(h_lat + 10*1e-5, h_lon + 50*1e-5))
    mission_items.append(await create_mission(h_lat, h_lon + 50*1e-5))
    mission_items.append(await create_mission(h_lat, h_lon + 40*1e-5))
    mission_items.append(await create_mission(h_lat + 10*1e-5, h_lon + 40*1e-5))
    mission_items.append(await create_mission(h_lat + 10*1e-5, h_lon + 30*1e-5))
    mission_items.append(await create_mission(h_lat + 20*1e-5, h_lon + 30*1e-5))
    mission_items.append(await create_mission(h_lat + 20*1e-5, h_lon + 20*1e-5))
    mission_items.append(await create_mission(h_lat + 10*1e-5, h_lon + 20*1e-5))
    mission_items.append(await create_mission(h_lat , h_lon))

    
    mission_plan = MissionPlan(mission_items)

    await t_drone.action.set_return_to_launch_altitude(5)
    await t_drone.mission.set_return_to_launch_after_mission(True)

    await t_drone.mission.upload_mission(mission_plan)
    await asyncio.sleep(2)

    print("Arming...")
    await t_drone.action.arm()
    async for armed in t_drone.telemetry.armed():
        if armed:
            print("Drone armed")
            break

    print("Taking off...")
    await t_drone.action.set_takeoff_altitude(5)
    await t_drone.action.takeoff()
    await pos_htarget(t_drone, 4.8, 5.2)


    print("Starting the mission")
    await t_drone.mission.start_mission()
    await asyncio.sleep(2)

    async for mission_progress in t_drone.mission.mission_progress():
        print(f"Mission progress: {(mission_progress.current/mission_progress.total)*100}%")
        if mission_progress.current == mission_progress.total:
            print("Mission completed!")
            break
    # Check if the drone has landed
    async for state in t_drone.telemetry.landed_state():
        if state == state.ON_GROUND:
            print("Drone landed!")
            break
            
    battery_task.cancel() # After the drone is returned and landed, we stop the background task (battery_checker)!
asyncio.run(main())
