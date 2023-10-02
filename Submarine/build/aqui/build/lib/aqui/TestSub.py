import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import random


class TestPub(Node):

    def __init__(self):
        super().__init__('b1')
       
        self.subscription = self.create_subscription(Twist,'a1', self.listener_callback,10)


    def listener_callback(self, msg):
        pass

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = TestPub()

    rclpy.spin(minimal_publisher)



    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()