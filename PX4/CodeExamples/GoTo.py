import asyncio
from mavsdk import System

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

  print("Getting altitude at home location....")
  home = await anext(drone.telemetry.home())

  absolute_altitude = home.absolute_altitude_m
  absolute_latitude = home.latitude_deg
  absolute_longitude = home.longitude_deg


  flying_alt = absolute_altitude + 5.0
  print(f"Flight altitude is: {flying_alt}")

  print("Going to target 1 location...")
  await drone.action.goto_location(absolute_latitude + 10 * 1e-5, absolute_longitude, flying_alt, 0)
  await asyncio.sleep(5)

  print("Going to target 2 location...")
  await drone.action.goto_location(absolute_latitude + 10 * 1e-5, absolute_longitude + 10 * 1e-5, flying_alt, 0)
  await asyncio.sleep(5)

  print("Going to target 3 location...")
  await drone.action.goto_location(absolute_latitude, absolute_longitude + 10 * 1e-5, flying_alt, 0)
  await asyncio.sleep(5)

  print("Going to target 4 location...")
  await drone.action.goto_location(absolute_latitude, absolute_longitude, flying_alt, 0)
  await asyncio.sleep(5)


  print("Landing...")
  await drone.action.land()
  await asyncio.sleep(5)



asyncio.run(main())
