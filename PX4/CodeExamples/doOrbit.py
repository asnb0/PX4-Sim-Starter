import asyncio

from mavsdk import System 
from mavsdk.action import OrbitYawBehavior

import math

async def wait_one_orbit(drone: System,
                         center_lat: float,
                         center_lon: float,
                         radius_m: float,
                         circle_tolerance_m: float = 1.0,
                         start_tolerance_deg: float = 10 * 1e-6):
    """
    1) Wait until drone reaches the orbit circle (≈ orbit started)
    2) Record that as start point
    3) Wait until it comes back to that point (one full orbit)
    """

    def distance_m(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # 1) Wait until we are on the orbit circle (radius from center)
    print("Waiting for drone to reach orbit circle...")
    async for position in drone.telemetry.position():
        d = distance_m(center_lat, center_lon,
                       position.latitude_deg, position.longitude_deg)
        if abs(d - radius_m) <= circle_tolerance_m:
            start_lat = position.latitude_deg
            start_lon = position.longitude_deg
            print(f"Orbit started near: {start_lat}, {start_lon}")
            break

    # 2) Wait until it LEAVES that start region (so we don't immediately trigger completion)
    async for position in drone.telemetry.position():
        if (abs(position.latitude_deg - start_lat) > start_tolerance_deg or
            abs(position.longitude_deg - start_lon) > start_tolerance_deg):
            print("Left start point, orbit in progress...")
            break

    # 3) Now reuse the idea of pos_target: wait until it comes back
    print("Waiting for drone to come back to start of orbit (one full round)...")
    async for position in drone.telemetry.position():
        if (abs(position.latitude_deg - start_lat) <= start_tolerance_deg and
            abs(position.longitude_deg - start_lon) <= start_tolerance_deg):
            print("One full orbit completed!")
            break


# async def pos_target(drone: System, target_lat: float, target_lon: float):
#     async for position in drone.telemetry.position():
#         if (abs(position.latitude_deg - target_lat) <= 10 * 1e-6) and (abs(position.longitude_deg 
#                                                                            - target_lon) <= 10 * 1e-6):
#             print(f"Reached start location: {target_lat, target_lon}")
#             break  

async def pos_htarget(drone: System, target_min: float, target_max: float):
    async for position in drone.telemetry.position():
        if position.relative_altitude_m > target_min and position.relative_altitude_m < target_max:
            print(f"Reached target altitude: {position.relative_altitude_m} m")
            break


async def run():
    drone = System()
    print("Connected to PX4...")
    await drone.connect(system_address="udp://:14540")
    print("drone connected")

    print("Getting altitude at home location....")
    home = await anext(drone.telemetry.home())

    absolute_altitude = home.absolute_altitude_m
    absolute_latitude = home.latitude_deg
    absolute_longitude = home.longitude_deg

    flying_alt = absolute_altitude + 5.0
    print(f"Flight altitude is: {flying_alt}")
    
    print("Arming...")
    await drone.action.arm()
    print("Drone armed!")


    # Takeoff
    print("taking off...")
    await drone.action.set_takeoff_altitude(5) #Default Takeoff altitude set to 10 meter
    await drone.action.takeoff()

    await pos_htarget(drone, target_min= 4.8,target_max= 5.2)

   
    radius_m = 5
    center_lat = absolute_latitude + 10 * 1e-5
    center_lon = absolute_longitude + 10 * 1e-5

    await drone.action.do_orbit(
        radius_m,
        2,  # velocity_ms
        OrbitYawBehavior.HOLD_FRONT_TANGENT_TO_CIRCLE,
        center_lat,
        center_lon,
        flying_alt
    )

    # Wait for exactly one orbit based on position + math
    await wait_one_orbit(drone, center_lat, center_lon, radius_m)

    # After one orbit → RTL
    await drone.action.return_to_launch()


    # # Land
    # print("Landing...")
    # await drone.action.land()
    # async for state in drone.telemetry.landed_state():
    #     if state == state.ON_GROUND: 
    #         print("Drone landed!")
    #         break
    
asyncio.run(run())



