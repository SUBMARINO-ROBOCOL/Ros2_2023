import rclpy

from TestPub import MinimalPublishera



def main(args=None):
    rclpy.init(args=args)

    for i in range(10):

        minimal_publisher = MinimalPublisher(1)

        rclpy.spin(minimal_publisher)
        print(1)
        s

if __name__ == '__main__':
    main()