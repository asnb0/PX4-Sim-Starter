import asyncio
from mavsdk import System
from mavsdk.core import ConnectionState


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

    async for connection in drone.core.connection_state():
        print(f"is the drone connected: {connection.is_connected}")
        if connection.is_connected:
            print(f"drone connected")
            break

    home = await anext(drone.telemetry.home())
    print(f"drone home {home}")

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


asyncio.run(run())

