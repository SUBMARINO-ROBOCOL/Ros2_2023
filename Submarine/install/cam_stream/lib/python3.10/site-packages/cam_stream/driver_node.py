import rclpy
from rclpy.node import Node
from rclpy.qos import QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy, QoSProfile

from sensor_msgs.msg import Image

from cv_bridge import CvBridge

import cv2

class DriverNode(Node):

    def __init__(self, camIndex, wantColor, QoSProf):
        super().__init__('driver_node_'+str(camIndex))

        self.camIndex = camIndex
        self.wantColor = wantColor
        self.bridge = CvBridge()
        self.camera = cv2.VideoCapture(camIndex)
        self.publisher = self.create_publisher(Image, 'camera_'+str(camIndex), qos_profile=QoSProf)

        timer_period = 0.05  # seconds

        if self.wantColor:
            callbackFunction = self.colorConfig
        else:
            callbackFunction = self.blackNWhiteConfig

        self.timer = self.create_timer(timer_period, callbackFunction)


    def colorConfig(self):
        check, frame = self.camera.read()
        if check:
            frame = cv2.resize(frame, (640,480))
            msg = self.bridge.cv2_to_imgmsg(frame,'bgr8')
            self.publisher.publish(msg)

    def blackNWhiteConfig(self):
        check, frame = self.camera.read()
        if check:
            frame = cv2.resize(frame, (640,480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            msg = self.bridge.cv2_to_imgmsg(frame,'mono8')
            self.publisher.publish(msg)


def getCamIndexes():
        index = 0
        arr = []
        while index < 10:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
        return arr

def printCamIndexes(arr):
        if (len(arr)>0):
            print("\nThe following camera indexes were detected: ")
            msg = ""
            for i in arr:
                msg += str(i)+", "
            print(msg[:-2])

            return True
        else:
             print("\nNo cameras available")
             return False
    
def setCamIndx():
    return int(input("Select a camIndex: "))

def isColor():
     return input("want color? (Y/N): ").upper()=="Y"

def isRealSense():
     return input("is RealSense? (Y/N): ").upper()=="Y"

def setQoSProfile() -> QoSProfile:
    qosProfileVar = QoSProfile(depth=2)
    qosProfileVar.durability = QoSDurabilityPolicy.VOLATILE
    qosProfileVar.reliability = QoSReliabilityPolicy.BEST_EFFORT
    qosProfileVar.history = QoSHistoryPolicy.KEEP_LAST
    
    return qosProfileVar 
    

def main():
    rclpy.init()

    if(printCamIndexes(getCamIndexes())):
        wantColor = False
        camIndex = setCamIndx()
        wantColor = isColor()
        
        node = DriverNode(camIndex, wantColor, setQoSProfile())
        
        rclpy.spin(node)
        node.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()


#https://blog.misterblue.com/2021/2021-05-29-ros2-sending-image
#ros2 run rqt_image_view rqt_image_view
#https://docs.ros.org/en/foxy/Concepts/About-RQt.html
#sudo apt install ros-foxy-rqt*