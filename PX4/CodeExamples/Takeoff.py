import asyncio
from mavsdk import System

async def run():
   drone = System()
   print("Connecting to PX4...")
   await drone.connect(system_address="udp://:14540")
   print("drone connected")

   print("Arming...")
   await drone.action.arm()
   print("Drone armed!")

   # Takeoff
   print("Taking off...")
   await drone.action.takeoff()
   await asyncio.sleep(10)

   # Land
   print("Landing...")
   await drone.action.land()
   print("Drone landed!")



asyncio.run(run())
