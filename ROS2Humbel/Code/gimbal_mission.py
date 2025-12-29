import asyncio 

from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
import gz_camera_to_frame
import threading
from mavsdk.telemetry import LandedState


async def show_camera_stream():
    import cv2
    async for frame in gz_camera_to_frame.get_frames():
        # Process the frame (for example, display it using OpenCV)
        cv2.imshow("Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def run():
    drone = System() 

    await drone.connect(system_address="udp://:14540")
    print("Drone connected")
    
    threading.Thread(target=asyncio.run, args=(show_camera_stream(),), daemon=True).start()

    mission_items = []

    home = await anext(drone.telemetry.home())
    ab_lat = home.latitude_deg
    ab_lon = home.longitude_deg

    # add Mission Items
    mission_items.append(MissionItem(ab_lat + 50 * 1e-5,ab_lon, 20 , 10, True, 
                                     -45, 0, MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))
    
    mission_items.append(MissionItem(ab_lat + 50 * 1e-5,ab_lon + 50 * 1e-5 , 20 , 10, True, 
                                     -45, 0, MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))
    
    mission_items.append(MissionItem(ab_lat,ab_lon + 50 * 1e-5 ,  20 , 10, True, 
                                     -45, 0, MissionItem.CameraAction.NONE, 
                                     float('nan'), float('nan'), 10, 2,
                                    float('nan'), MissionItem.VehicleAction.NONE))
    
    mission_items.append(MissionItem(ab_lat,ab_lon, 20 , 10, True, 
                                     -45, 0, MissionItem.CameraAction.NONE, 
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

    async for landed in drone.telemetry.landed_state():
        if landed == LandedState.ON_GROUND:
            print("Drone landed")
            break

asyncio.run(run())
