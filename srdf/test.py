#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler

def main():
    rospy.init_node("motion_test")
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    
    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    rospy.sleep(1.0)

    print("init_pose")
    arm.set_named_target("init") #  返り値：None
    a = arm.go() #  返り値：bool type

    print(a)

    if a:
        print("success")

    rospy.sleep(1.0)

    print("bow_pose")
    arm.set_named_target("bow")
    arm.go()

    print("init_pose")
    arm.set_named_target("init")
    a = arm.go()

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass