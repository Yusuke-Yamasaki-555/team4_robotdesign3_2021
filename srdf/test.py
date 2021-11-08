#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler

from copy import deepcopy

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

    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print(a)

    if a:
        print("success")

    rospy.sleep(1.0)

    print("bow")
    arm.set_named_target("bow")
    a = arm.go() #  モーションが終了したら、その結果がaに代入される

    if a:
        print("success")

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

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

    arm.set_max_velocity_scaling_factor(1.0) #  stand_by
    arm.set_max_acceleration_scaling_factor(0.35) #  stand_by
    print("stand_by")
    arm.set_named_target("stand_by")
    arm.go()

    # search_club → happy_club → 掴む姿勢
    #  """
    search_club = geometry_msgs.msg.Pose() #  棒を探す姿勢の定義
    search_club.position.x = 0
    search_club.position.y = 0.26
    search_club.position.z = 0.3
    qu1 = quaternion_from_euler(0, 3.14, 3.14)
    search_club.orientation.x = qu1[0]
    search_club.orientation.y = qu1[1]
    search_club.orientation.z = qu1[2]
    search_club.orientation.w = qu1[3]
    print("search_club")
    arm.set_pose_target(search_club)
    print(search_club)
    arm.go()

    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
    print("Current Pose:")
    print(current_pose)

    arm.set_max_velocity_scaling_factor(1.0) #  happy_club
    arm.set_max_acceleration_scaling_factor(1.0) #  happy_club
    print("happy_club")
    
    #  喜ぶ姿勢になる(happy_club) from SRDF
    arm.set_named_target("happy_club")
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",current_pose[0]) #  現在の第一関節z軸を維持
    arm.go()

    '''
    #  喜ぶ姿勢になる(happy_club) from pose_target
    happy_club = deepcopy(search_club)
    qu2 = quaternion_from_euler(0, 0.873, 1.57)
    happy_club.orientation.x = qu2[0]
    happy_club.orientation.y = qu2[1]
    happy_club.orientation.z = qu2[2]
    happy_club.orientation.w = qu2[3]
    arm.set_pose_target(happy_club)
    print(happy_club)
    arm.go()
    '''

    #  手を開閉させて喜ぶ(happy_club)
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    #  棒を掴む体勢に戻る
    print("search_club")
    arm.set_pose_target(search_club)
    print(search_club)
    arm.go()

    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()
    #  """

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    #  棒を離す動作
    print("release_club")
    arm.set_named_target("release_club")
    arm.go()

    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("bow")
    arm.set_named_target("bow")
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