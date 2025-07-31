import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time

class CranePlusCommander(Node):
  def __init__(self):
    super().__init__('crane_plus_commander')

    self.arm_pub = self.create_publisher(JointTrajectory,
        '/crane_plus_arm_controller/joint_trajectory', 10)
    self.gripper_pub = self.create_publisher(JointTrajectory,
        '/crane_plus_gripper_controller/joint_trajectory', 10)

    time.sleep(1.0)

    # Open
    grip_msg = JointTrajectory()
    grip_msg.joint_names = ['crane_plus_joint_hand']
    point = JointTrajectoryPoint()
    point.positions = [-0.3]  # -0.3=Open, 0.4=Close
    point.time_from_start.sec = 1
    grip_msg.points.append(point)

    self.get_logger().info('Sending gripper command (open)...')
    self.gripper_pub.publish(grip_msg)

    time.sleep(2.0)

    arm_msg = JointTrajectory()
    arm_msg.joint_names = [
      'crane_plus_joint1',
      'crane_plus_joint2',
      'crane_plus_joint3',
      'crane_plus_joint4'
    ]
    point = JointTrajectoryPoint()
    point.positions = [1.57, -1.2, 1.0, -0.2]
    point.time_from_start.sec = 2
    arm_msg.points.append(point)

    self.get_logger().info('Sending arm trajectory...')
    self.arm_pub.publish(arm_msg)

    time.sleep(2.0)

    # Close
    point.positions = [0.4]
    grip_msg.points = [point]
    self.get_logger().info('Sending gripper command (close)...')
    self.gripper_pub.publish(grip_msg)

def main():
  rclpy.init()
  node = CranePlusCommander()
  rclpy.spin_once(node, timeout_sec=0)
  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()
