#!/usr/bin/env python3
import asyncio
import threading
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

# Convert ROS Image → cv2 frame
bridge = CvBridge()

def ros_image_to_cv2(msg: Image, encoding: str = "bgr8"):
    try:
        return bridge.imgmsg_to_cv2(msg, desired_encoding=encoding)
    except Exception as e:
        print(f"[ERROR] Failed to convert image: {e}")
        return None

# ROS2 subscriber node that stores the latest frame
class _CameraNode(Node):
    def __init__(self, topic_name='/world/baylands/model/x500_gimbal_0/link/camera_link/sensor/camera/image'):
        super().__init__('async_camera_node')
        self._frame = None
        self._lock = threading.Lock()
        self.subscription = self.create_subscription(
            Image, topic_name, self._callback, 10)

    def _callback(self, msg):
        frame = ros_image_to_cv2(msg)
        if frame is not None:
            with self._lock:
                self._frame = frame

    def get_latest_frame(self):
        with self._lock:
            return None if self._frame is None else self._frame.copy()

# Async wrapper
class AsyncCameraInterface:
    def __init__(self, topic_name='/world/baylands/model/x500_gimbal_0/link/camera_link/sensor/camera/image'):
        self.topic_name = topic_name
        self._node = None
        self._thread = None

    def start(self):
        # Start ROS2 node in background thread
        def _ros_spin():
            rclpy.init()
            self._node = _CameraNode(self.topic_name)
            rclpy.spin(self._node)
            self._node.destroy_node()
            rclpy.shutdown()

        self._thread = threading.Thread(target=_ros_spin, daemon=True)
        self._thread.start()

    async def get_frame(self):
        """Async call to get the most recent frame"""
        while True:
            if self._node:
                frame = self._node.get_latest_frame()
                if frame is not None:
                    return frame
            await asyncio.sleep(0.01)  # non-blocking wait


async def get_frames(CameraInterface='/world/baylands/model/x500_gimbal_0/link/camera_link/sensor/camera/image'):
    """
        thin function will take the camera topic name as input 
        and yield cv2 frames asynchronously.
    """
    cam = AsyncCameraInterface(CameraInterface)
    cam.start()

    while True:
        frame = await cam.get_frame()
        if frame is None:
            await asyncio.sleep(0.01)
            continue
        yield frame 

