import asyncio 

from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def run():
    drone = System() 

    await drone.connect(system_address="udp://:14540")
    print("Drone connected")

    mission_items = []

    home = await anext(drone.telemetry.home())
    ab_lat = home.latitude_deg
    ab_lon = home.longitude_deg

    # add firts Mission Item
    mission_items.append(MissionItem(ab_lat + 50 * 1e-5,ab_lon, 20 , 10, True, 
                                     float('nan'), float('nan'), MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))
    
    # add second Mission Item
    mission_items.append(MissionItem(ab_lat + 20 * 1e-5,ab_lon + 20 * 1e-5 , 20 , 10, True, 
                                     float('nan'), float('nan'), MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))

    mission_items.append(MissionItem(ab_lat + 40 * 1e-5,ab_lon + 40 * 1e-5 , 20 , 10, True, 
                                     float('nan'), float('nan'), MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))
    

    await drone.mission.set_return_to_launch_after_mission(True)
    mission_plan = MissionPlan(mission_items)

    await drone.mission.upload_mission(mission_plan)

    await drone.action.arm()

    async for armed in drone.telemetry.armed():
        if armed:
            print("Drone armed")
            break

    await drone.mission.start_mission()

    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print("Mission completed")
            break

    

asyncio.run(run())
