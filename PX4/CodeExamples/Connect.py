import asyncio
from mavsdk import System


async def main():
    drone = System()
    print("Connecting to drone...")
    await drone.connect(system_address="udp://:14540") # this is the default port

asyncio.run(main())
