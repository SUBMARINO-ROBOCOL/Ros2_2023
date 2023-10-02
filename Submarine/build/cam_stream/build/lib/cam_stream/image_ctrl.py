import rclpy
from rclpy.node import Node
from rclpy.qos import QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy, QoSProfile

from sensor_msgs.msg import Image

from cv_bridge import CvBridge

import cv2

import show_img
import cam_boton
import Codigo_ranas
import imgCrop


class ImageCtrlNode(Node):
    
    def __init__(self, camIndx, QoSProf):
        name = str(camIndx)
        if(camIndx<0):
            name="realsense"
        
        super().__init__("imageCtrl_"+name)
        
        self.algos = [self.showImgAlgo, self.redSquareAlgo, self.conteoRanasAlgo, self.cropFrame]
        
        self.cropSize = None

        topic_subscription_name = None

        if camIndx<0:
            topic_subscription_name = "realsense_cam"
        else:
            topic_subscription_name = "camera_"+str(camIndx)


        self.camIndx = camIndx
        self.bridge = CvBridge()


        excutionFunction = self.algoMenuSelector()

        self.sub = self.create_subscription(Image, topic_subscription_name, excutionFunction, qos_profile=QoSProf) 
    
    def algoMenuSelector(self):
        
        menu="Choose one of the following alrogithms:"
        for i in range(len(self.algos)):
            menu+="\n" + str(i+1) +". " +str(self.algos[i].__name__)

        print(menu)

        algoIndx = int(input())-1

        return self.algos[algoIndx]

        

    def showImgAlgo(self,msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        show_img.showImg(img)

    def redSquareAlgo(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        cam_boton.red_box(img)

    def conteoRanasAlgo(self, msg):
        
        img = self.bridge.imgmsg_to_cv2(msg)
        Codigo_ranas.main(img)      

    def cropFrame(self, msg):
        if self.cropSize == None:
            self.cropSize = int(input("Select a cropSize: "))

        frame = self.bridge.imgmsg_to_cv2(msg) 
        imgCrop.crop(frame,self.cropSize)




def getCamSubscription():
    return int(input("\nChoose a camera to subscribe: "))

def setQoSProfile() -> QoSProfile:
    
    qosProfileVar = QoSProfile(depth=2)
    qosProfileVar.durability = QoSDurabilityPolicy.VOLATILE
    qosProfileVar.reliability = QoSReliabilityPolicy.BEST_EFFORT
    qosProfileVar.history = QoSHistoryPolicy.KEEP_LAST

    return qosProfileVar
    
    

def main():
    rclpy.init()

    camIndx = getCamSubscription()
    node = ImageCtrlNode(camIndx, setQoSProfile())
    
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()