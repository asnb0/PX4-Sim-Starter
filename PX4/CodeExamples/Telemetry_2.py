import asyncio
from mavsdk import System

async def position(drone: System):
    async for position in drone.telemetry.position():
        print(f"pos: {position}")

async def battery(drone: System):
    async for battery in drone.telemetry.battery():
        print(f"battery: {battery.remaining_percent}")

async def in_air(drone: System):
    async for in_air in drone.telemetry.in_air():
        print(in_air)

async def run():
    drone = System()
    print("Connecting to PX4...")
    await drone.connect(system_address="udp://:14540")
    print("drone connected")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    asyncio.create_task(position(drone))
    asyncio.create_task(battery(drone))
    asyncio.create_task(in_air(drone))

    await asyncio.sleep(20)

asyncio.run(run())

