#!/usr/bin/env python

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
#     range_centre_right.data = msg.ranges[178]
#     range_centre.data = msg.ranges[356]
#     range_centre_left.data = msg.ranges[534]
#     range_left.data = msg.ranges[713]


def distance_info(msg):
    global regions_
    regions_ = {
        'range_right': min(min(msg.ranges[0:143]), 10),
        'range_centre_right': min(min(msg.ranges[144:287]), 10),
        'range_centre': min(min(msg.ranges[288:431]), 10),
        'range_centre_left': min(min(msg.ranges[432:575]), 10),
        'range_left': min(min(msg.ranges[576:713]), 10),
    }


def position_info(msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)


def main():
    rospy.init_node("controller", anonymous=True)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, distance_info)
    rospy.Subscriber("/odom", Odometry, position_info)

    # distance = 1 T2 - distance = 0.9 T3
    distance = 1

    twist = Twist()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0

    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0

    while not rospy.is_shutdown():

        if regions_['range_centre'] > 3 and regions_['range_right'] > 3 and regions_['range_left'] > 3 and \
                regions_['range_centre_left'] > 3 and regions_['range_centre_right'] > 3:
            print("Finish")
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            break

        if regions_['range_centre'] > distance and regions_['range_centre_left'] > distance and regions_[
            'range_centre_right'] > distance:
            state_description = 'case 1 - nothing'
            twist.linear.x = -0.1
            twist.linear.y = -0.1
            twist.angular.z = 0.0
        elif regions_['range_centre'] < distance < regions_['range_centre_left'] and regions_[
            'range_centre_right'] > distance:
            state_description = 'case 2 - range_centre'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            # -0.3 T2, 0.3 T3/T1
            twist.angular.z = 0.3
        elif regions_['range_centre'] > distance > regions_[
            'range_centre_right'] and regions_['range_centre_left'] > distance:
            state_description = 'case 3 - range_centre_right'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = 0.3
        elif regions_['range_centre'] > distance > regions_['range_centre_left'] and regions_[
            'range_centre_right'] > distance:
            state_description = 'case 4 - range_centre_left'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = -0.3
        elif regions_['range_centre'] < distance < regions_['range_centre_left'] and regions_[
            'range_centre_right'] < distance:
            state_description = 'case 5 - range_centre and range_centre_right'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = 0.3
        elif regions_['range_centre'] < distance < regions_[
            'range_centre_right'] and regions_['range_centre_left'] < distance:
            state_description = 'case 6 - range_centre and range_centre_left'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = -0.3
        elif regions_['range_centre'] < distance and regions_['range_centre_left'] < distance and regions_[
            'range_centre_right'] < distance:
            state_description = 'case 7 - range_centre and range_centre_left and range_centre_right'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = -0.3
        elif regions_['range_centre'] > distance > regions_['range_centre_left'] and regions_[
            'range_centre_right'] < distance:
            state_description = 'case 8 - range_centre_left and range_centre_right'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = -0.3
        else:
            state_description = 'unknown'
            rospy.loginfo(regions_)

        # centre_left and centre = 1 for T2 and 1.4 for T3
        # left = 2 T3, 2.5 T2
        if 2.5 < regions_['range_left'] < 4.5 and regions_['range_centre_left'] > 1 and regions_['range_centre'] > 1:
            state_description = 'turn_left'
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = 0.5

        print(state_description)
        pub.publish(twist)


if __name__ == "__main__":
    main()
