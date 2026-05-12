import asyncio
from mavsdk import System

async def position(drone: System):
    async for position in drone.telemetry.position():
        print(f"--------[pos: {position} --------]" )
        await asyncio.sleep(1)

async def battery(drone: System):
    async for battery in drone.telemetry.battery():
        print(f"--------[ battery: {battery.remaining_percent}--------]")
        await asyncio.sleep(1)

async def in_air(drone: System):
    async for in_air in drone.telemetry.in_air():
        print(f"-------- is drone in air: [{in_air}--------]")
        await asyncio.sleep(1)

async def run():
    drone = System()

    print("Connecting to PX4...")
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    pos_task = asyncio.create_task(position(drone))
    bat_task = asyncio.create_task(battery(drone))
    air_task = asyncio.create_task(in_air(drone))

    print("Arming...")
    await drone.action.arm()

    async for armed in drone.telemetry.armed():
        print(f"armed: {armed}")
        if armed:
            print("Drone armed!")
            break
    print("Taking off...")
    await drone.action.takeoff()

    async for state in drone.telemetry.landed_state():
        print(f"after takeoff state: {state}")
        if state == state.IN_AIR:
            print("Drone took off!")
            break

    # Land
    print("Landing...")
    await drone.action.land()
    async for state in drone.telemetry.landed_state():
        print(f"after landing state: {state}")
        if state == state.ON_GROUND:
            print("Drone landed!")
            break

    pos_task.cancel()
    bat_task.cancel()
    air_task.cancel()
    # await asyncio.gather(pos_task, bat_task, air_task)

asyncio.run(run())

