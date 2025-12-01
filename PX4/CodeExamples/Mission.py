import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan


async def main():
    drone = System()
    print("Connecting to drone...")
    await drone.connect(system_address="udp://:14540")

    print("Arming drone...")
    await drone.action.arm()
    await asyncio.sleep(5)

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    home = await anext(drone.telemetry.home())

    absolute_latitude = home.latitude_deg
    absolute_longitude = home.longitude_deg

    flying_alt = 5.0
    print(f"Flight altitude is: {flying_alt}")

    # Define mission waypoints
    mission_items = [
        MissionItem(absolute_latitude + 10 * 1e-5, absolute_longitude , flying_alt, 5.0, True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    float('nan'), float('nan'), float('nan'), float('nan'),
                    float('nan'),MissionItem.VehicleAction.NONE),
        MissionItem( absolute_latitude + 10 * 1e-5 , absolute_longitude + 10 * 1e-5  , flying_alt, 5.0, True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    float('nan'), float('nan'), float('nan'), float('nan'),
                    float('nan'), MissionItem.VehicleAction.NONE),

        MissionItem(absolute_latitude, absolute_longitude + 10 * 1e-5, flying_alt, 5.0, True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    float('nan'), float('nan'), float('nan'), float('nan'),
                    float('nan'), MissionItem.VehicleAction.NONE),

        MissionItem(absolute_latitude, absolute_longitude, flying_alt, 5.0, True,
                    float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                    float('nan'), float('nan'), float('nan'), float('nan'),
                    float('nan'), MissionItem.VehicleAction.NONE)
    ]

    mission_plan = MissionPlan(mission_items)

    print("Uploading mission...")
    await drone.mission.upload_mission(mission_plan)
    await asyncio.sleep(2)

    print("Starting mission...")
    await drone.mission.start_mission()
    await asyncio.sleep(2)

    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print("-- Mission completed!")
            break

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)

asyncio.run(main())
