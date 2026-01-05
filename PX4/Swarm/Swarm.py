#!/usr/bin/env python3
import asyncio, math, time
from typing import Tuple
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError
from mavsdk.telemetry import LandedState

ALT_REL=5.0; SETPOINT_HZ=15.0; POS_TOL=2.0; TIMEOUT=240.0
AFTER_TAKEOFF_SEC=2.0; SYNC_WAIT_SEC=6.0
PATH_NE=[(20,0),(20,60),(0,60),(0,0)]

def ne_from(hlat,hlon,lat,lon):
   dy=(lat-hlat)*111320.0
   dx=(lon-hlon)*111320.0*math.cos(math.radians(hlat))
   return dy,dx

async def wait_health(d):
   async for h in d.telemetry.health():
       if h.is_local_position_ok and h.is_home_position_ok: return
       await asyncio.sleep(0.1)

async def wait_in_air(d):
   async for s in d.telemetry.landed_state():
       if s==LandedState.IN_AIR: return
       await asyncio.sleep(0.05)

async def prime_offboard(d,alt):
   sp=PositionNedYaw(0,0,-alt,0)
   for _ in range(12):
       await d.offboard.set_position_ned(sp); await asyncio.sleep(0.06)
   await d.offboard.start()

async def pos_worker(d,store,stop_evt):
   try:
       async for p in d.telemetry.position():
           store["pos"]=p
           if stop_evt.is_set(): break
   except Exception as e:
       store["pos_err"]=e

async def goto_ne(d,store,hlat,hlon,n,e,alt):
   tgt=PositionNedYaw(n,e,-alt,0); t=time.time(); dt=1/SETPOINT_HZ
   while True:
       await d.offboard.set_position_ned(tgt)
       p=store.get("pos")
       if p:
           cn,ce=ne_from(hlat,hlon,p.latitude_deg,p.longitude_deg)
           if math.hypot(cn-n,ce-e)<=POS_TOL: return True
       if time.time()-t>TIMEOUT: return False
       await asyncio.sleep(dt)

async def fly_one(name,addr,form_n,form_e,sync_t0, grpc_port):
   # لكل طيّارة منفذ gRPC خاص (يمنع التضارب بين mavsdk_server instances)
   d=System(port=grpc_port)
   print(f"[{name}] Connecting {addr} (gRPC:{grpc_port})")
   await d.connect(system_address=addr)

   print(f"[{name}] Waiting health..."); await wait_health(d)
   w=max(0, sync_t0-time.time()); print(f"[{name}] Sync in {w:.1f}s"); await asyncio.sleep(w)

   home=await anext(d.telemetry.home()); hlat,hlon=home.latitude_deg,home.longitude_deg
   print(f"[{name}] Arm & takeoff")
   await d.action.set_takeoff_altitude(ALT_REL); await d.action.arm(); await d.action.takeoff()
   await wait_in_air(d); await asyncio.sleep(AFTER_TAKEOFF_SEC)

   print(f"[{name}] Start Offboard")
   try: await prime_offboard(d,ALT_REL)
   except OffboardError:
       await asyncio.sleep(0.5); await prime_offboard(d,ALT_REL)

   store={"pos":None}; stop=asyncio.Event(); t=asyncio.create_task(pos_worker(d,store,stop))
   try:
       for i,(n,e) in enumerate(PATH_NE,1):
           n+=form_n; e+=form_e
           print(f"[{name}] WP{i}: N{n} E{e}")
           await goto_ne(d,store,hlat,hlon,n,e,ALT_REL)
   finally:
       stop.set(); t.cancel()
       try: await t
       except: pass
       try: await d.offboard.stop()
       except: pass
       await d.action.land(); await asyncio.sleep(1.5)

async def main():
   t0=math.ceil(time.time()+SYNC_WAIT_SEC)
   tasks = [
       fly_one("LEADER","udp://:14540",0.0,  0.0,t0, 50051),
       fly_one("LEFT",  "udp://:14541",0.0,-12.0,t0, 50052),
       fly_one("RIGHT", "udp://:14542",0.0, 12.0,t0, 50053),
   ]
   try:
       results = await asyncio.gather(*tasks, return_exceptions=True)
       for r in results:
           if isinstance(r,Exception): print("[WARN]", r)
   except asyncio.CancelledError:
       pass

if __name__=="__main__":
   asyncio.run(main())

  
