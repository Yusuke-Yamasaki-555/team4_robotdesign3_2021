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
    
    arm.set_max_velocity_scaling_factor(0.5) #  bow
    arm.set_max_acceleration_scaling_factor(0.35) #  bow

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
    a = arm.go() #  モーションが終了したら、その結果がaに代入される

    if a:
        print("success")

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    arm.set_max_velocity_scaling_factor(0.5) #  search_target
    arm.set_max_acceleration_scaling_factor(0.5) #  search_target

    print("search_target")
    arm.set_named_target("search_target")
    arm.go()

    arm.set_max_velocity_scaling_factor(1.0) #  emotions_stand_by
    arm.set_max_acceleration_scaling_factor(1.0) #  emotions_stand_by

    print("emotions_stand_by")
    arm.set_named_target("emotions_stand_by")
    arm.go()

    arm.set_max_velocity_scaling_factor(1.0) #  tilt_neck & rev_tilt_neck
    arm.set_max_acceleration_scaling_factor(1.0) #  tilt neck & rev_tilt_neck

    print("tilt_neck")
    arm.set_named_target("tilt_neck")
    arm.go()

    print("rev_tilt_neck")
    arm.set_named_target("rev_tilt_neck")
    arm.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    arm.set_max_velocity_scaling_factor(0.05) #  hold
    arm.set_max_acceleration_scaling_factor(1.0) #  hold

    print("hold")
    arm.set_named_target("hold")
    arm.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass