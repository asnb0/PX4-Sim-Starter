import asyncio
from mavsdk import System

async def battery_checker(drone: System):
    print("Checking battery...")
    async for battery in drone.telemetry.battery():
        if battery.remaining_percent < 30:
            print(f"battery low returning to home")
            await drone.action.return_to_launch()


async def run():
    drone = System()

    print("Connecting to PX4...")
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break


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

    await asyncio.create_task(battery_checker(drone))

    print("Landing...")
    await drone.action.land()
    async for state in drone.telemetry.landed_state():
        print(f"after landing state: {state}")
        if state == state.ON_GROUND:
            print("Drone landed!")
            break

asyncio.run(run())

