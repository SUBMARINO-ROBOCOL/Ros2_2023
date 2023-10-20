import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import random


class MinimalPublisher(Node):

    def __init__(self, id):
        super().__init__("a"+str(id))
        self.publisher_ = self.create_publisher(Twist, 'twist_'+str(id) , 10)
        timer_period = 0.0001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = float(random.randint(0,100))
        msg.linear.y = float(random.randint(0,100))
        msg.linear.z = float(random.randint(0,100))
        msg.angular.z = float(random.randint(0,100))
        self.publisher_.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(input())

    rclpy.spin(minimal_publisher)



    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()