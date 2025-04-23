import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
from std_msgs.msg import String

class GazeboPublisher(Node):
    def __init__(self):
        super().__init__('gazebo_publisher')
        self.publisher_ = self.create_publisher(Twist, '/diff_drive/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/diff_drive/scan', self.callback, 10)

    def callback(self, msg: LaserScan):
        front = msg.ranges[0] # What is infront of the robot, useful for corners.
        left = msg.ranges[1] # Exact 90 degree left scan

        self.get_logger().info(f"Front distance: {front:.2f} meters, Left distance: {left:.2f} meters.")
        if front < 3.0:
            self.publish(0.0, -0.5)
        elif left >= 3.0:
            self.publish(0.3, 0.15)
        elif left <= 1.3:
            self.publish(0.3, -0.15)
        else:
            self.publish(0.3, 0.0)



    def publish (self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.publisher_.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    gazebo_publisher = GazeboPublisher()
    rclpy.spin(gazebo_publisher)

    gazebo_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
