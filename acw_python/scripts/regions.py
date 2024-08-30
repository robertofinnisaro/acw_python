#!/usr/bin/env python3

import math

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from tf.transformations import euler_from_quaternion

range_left = Float32()
range_right = Float32()
range_centre = Float32()
range_centre_left = Float32()
range_centre_right = Float32()


regions_ = {
    'range_right': 0,
    'range_centre_right': 0,
    'range_centre': 0,
    'range_centre_left': 0,
    'range_left': 0,
}


# def distance_info(msg):
#     range_right.data = msg.ranges[0]
#     range_centre_right.data = msg.ranges[45]
#     range_centre.data = msg.ranges[90]
#     range_centre_left.data = msg.ranges[135]
#     range_left.data = msg.ranges[179]

    

def distance_info(msg):
    global regions_
    regions_ = {
        'range_right': min(min(msg.ranges[0:143]), 10),
        'range_centre_right': min(min(msg.ranges[144:287]), 10),
        'range_centre': min(min(msg.ranges[288:431]), 10),
        'range_centre_left': min(min(msg.ranges[432:575]), 10),
        'range_left': min(min(msg.ranges[576:713]), 10),
    }


def main():
    rospy.init_node("controller", anonymous=True)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, distance_info)
    
    twist = Twist()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0

    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0

    while not rospy.is_shutdown():
        # print(range_right.data)
        print(regions_.get('range_right'))
    

if __name__ == "__main__":
    main()
