import rclpy
from rclpy.node import Node
from rclpy.qos import QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy, QoSProfile


from sensor_msgs.msg import Image

from cv_bridge import CvBridge

import cv2


import pyrealsense2.pyrealsense2 as rs
import numpy as np

class RealsenseNode(Node):
    def __init__(self,QoSProf):
        super().__init__("realsesnse_node")

        self.pub = self.create_publisher(Image, "realsense_cam",qos_profile=QoSProf)
        self.bridge = CvBridge()

        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipe.start(self.config)
        print("success")

        self.timer = 0.05
        self.create_timer(self.timer, self.realsense_config1)

    def realsense_config1(self):
        frames = self.pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        self.msg = self.bridge.cv2_to_imgmsg(color_image,"bgr8")
        self.pub.publish(self.msg)        


def setQoSProfile() -> QoSProfile:
    qosProfileVar = QoSProfile(depth=2)
    qosProfileVar.durability = QoSDurabilityPolicy.VOLATILE
    qosProfileVar.reliability = QoSReliabilityPolicy.BEST_EFFORT
    qosProfileVar.history = QoSHistoryPolicy.KEEP_LAST
    
    return qosProfileVar 
    
def main():
    rclpy.init()

    node = RealsenseNode(setQoSProfile())
    
    rclpy.spin(node)
    node.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
