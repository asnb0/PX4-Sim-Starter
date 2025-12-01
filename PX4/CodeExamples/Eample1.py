import asyncio

from mavsdk import System
from mavsdk.action import OrbitYawBehavior



async def pos_target(drone: System, target_min: float, target_max: float):
    async for position in drone.telemetry.position():
        if position.relative_altitude_m > target_min and position.relative_altitude_m < target_max:
            print(f"Reached target altitude: {position.relative_altitude_m} m")
            break

async def battery_checker(drone: System):
    async for battery in drone.telemetry.battery():
        if battery.remaining_percent < 20:
            print("Battery low! Returning to launch...")
            await drone.action.return_to_launch()
            break

async def hold_at_pos(drone: System, target: float):
    async for position in drone.telemetry.position():
        if target < position.relative_altitude_m:
            print(f"Holding position at {target}m ")
            await drone.action.hold()
            break

async def run():

    drone = System()

    await drone.connect(system_address="udp://:14540")
    

    async for state in drone.core.connection_state():
        if state.is_connected: 
            print(f"drone connected.")
            asyncio.create_task(battery_checker(drone)) # start battery checker task
            break
    
    home = await anext(drone.telemetry.home())
    # arming the drone
    await drone.action.arm()

    async for armed in drone.telemetry.armed():
        if armed:
            print("Drone armed")
            break 

    print("Taking off...")
    await drone.action.set_takeoff_altitude(20)
    await drone.action.takeoff()
    await pos_target(drone, target_min= 19.5,target_max= 20)

    await drone.action.goto_location(home.latitude_deg + 20 * 1e-5, home.longitude_deg + 50* 1e-5, home.absolute_altitude_m+ 20, 0)

    await asyncio.sleep(20)

    await drone.action.do_orbit(30.0, 10.0, OrbitYawBehavior.HOLD_FRONT_TANGENT_TO_CIRCLE ,home.latitude_deg + 20 * 1e-5,home.longitude_deg + 50* 1e-5,home.absolute_altitude_m+ 20 )
    await asyncio.sleep(60)


    print("Landing... / RTL")
    # await drone.action.land()
    await drone.action.return_to_launch()
    await pos_target(drone, target_min= 0,target_max= 0.1)

    in_air = await anext(drone.telemetry.in_air())
    landed_state = await anext(drone.telemetry.landed_state())
    print(f"Drone landed at home location: Lat {home.latitude_deg}, Lon {home.longitude_deg} ,",
           "and the in air stat is {in_air}, and the landed state is: {landed_state}")
    
    

    
asyncio.run(run())
