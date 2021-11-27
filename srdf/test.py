#!/usr/bin/env python3
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

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    rospy.sleep(1.0)

#===== bow =====
    """
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("bow") #  bow
    arm.set_named_target("bow")
    arm.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()
    # """
#===== search_club =====
    """
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

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
    # """
#===== happy_club =====(search_clubとセット)
    """
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    #  喜ぶ姿勢になる(happy_club) from SRDF
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
    arm.set_named_target("happy_club")
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",current_pose[0]) #  現在の第一関節z軸を維持
    print("happy_club")
    arm.go()

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
    # """
#===== search_target =====
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("search_target")
    arm.set_named_target("search_target")
    arm.go()
    # """
#===== emotions_stand_by =====(search_targetとセット)
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(1.0)
    arm.set_max_acceleration_scaling_factor(1.0)

    print("emotions_stand_by")
    arm.set_named_target("emotions_stand_by")
    arm.go()
    # """
#===== tilt_neck =====(search_targetとセット)
    """
    print("tilt_neck")
    arm.set_named_target("tilt_neck")
    arm.go()

    print("rev_tilt_neck")
    arm.set_named_target("rev_tilt_neck")
    arm.go()

    print("search_target")
    arm.set_named_target("search_target")
    arm.go()
    # """
#===== dislike =====(search_targetとセット)
    """
    gripper.set_joint_value_target([1.0, 1.0])
    gripper.go()

    arm.set_max_velocity_scaling_factor(1.0)
    arm.set_max_acceleration_scaling_factor(1.0)

    print("emotions_stand_by")
    arm.set_named_target("emotions_stand_by")
    arm.go()

    arm.set_max_velocity_scaling_factor(1.0)
    arm.set_max_acceleration_scaling_factor(0.5)

    print("dislike_1")
    arm.set_named_target("dislike_1")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
       
    # ここのif文は関数にするべき
    if current_pose[0] >= 0.01:
        z_axis_1 = current_pose[0] - 0.559
        flag = True
    else:
        z_axis_1 = current_pose[0] + 0.559
        flag = False
    
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()
    print("dislike_2")
    arm.set_named_target("dislike_2")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得

    # ここのif文は関数にするべき
    if flag:
        z_axis_1 = current_pose[0] - 0.559
    else:
        z_axis_1 = current_pose[0] + 0.559
     
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()
    print("dislike_3")
    arm.set_named_target("dislike_3")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
        
    # ここのif文は関数にするべき
    if flag:
        z_axis_1 = current_pose[0] - 0.559
    else:
        z_axis_1 = current_pose[0] + 0.559
     
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()
    print("dislike_4")
    arm.set_named_target("dislike_4")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得

    # ここのif文は関数にするべき
    if flag:
        z_axis_1 = current_pose[0] - 0.559
    else:
        z_axis_1 = current_pose[0] + 0.559
     
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()
    print("dislike_5")
    arm.set_named_target("dislike_5")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得

    # ここのif文は関数にするべき
    if flag:
        z_axis_1 = current_pose[0] - 0.559
    else:
        z_axis_1 = current_pose[0] + 0.559
     
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()

    print("search_target")
    arm.set_named_target("search_target")
    arm.go()
    # """
#===== hold =====
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("hold")
    arm.set_named_target("hold")
    arm.go()
    # """
#==== swing_club =====(holdとセット)
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.05)
    arm.set_max_acceleration_scaling_factor(0.15)

    print("swing_set_club")
    arm.set_named_target("swing_set_club")
    current_pose = arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
    z_axis_1 = current_pose[0] - 0.873
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()

    arm.set_max_velocity_scaling_factor(1.0)
    arm.set_max_acceleration_scaling_factor(0.5)

    print("swing_club")
    arm.set_named_target("swing_club")
    z_axis_1 = current_pose[0] + 0.873
    arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
    arm.go()
    # """
#===== stand_by =====
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("stand_by")
    arm.set_named_target("stand_by")
    arm.go()
    # """
#===== release_club =====
    """
    gripper.set_joint_value_target([0.5, 0.5])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.5)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    print("release_club")
    arm.set_named_target("release_club")
    arm.go()

    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()
    # """
#==== happy_end =====
    """
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    arm.set_max_velocity_scaling_factor(1.0)
    arm.set_max_acceleration_scaling_factor(0.35)

    print("init_pose")
    arm.set_named_target("init")
    arm.go()

    # init → gripper_open → happy_end_1 → happy_end_init → happy_end_2 → happy_end_init 
    #  → happy_end_3　→ happy_end_init → happy_end_-rotate → happy_end_+lotate → happy_end_init 
    #    → gripper_close → gripper_open → gripper_close → gripper_open → gripper_close → gripper_open → gripper_close

    print("Open gripper")
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

    print("happy_end_1")
    arm.set_named_target("happy_end_1")
    arm.go()

    print("happy_end_init")
    arm.set_named_target("happy_end_init")
    arm.go()

    print("happy_end_2")
    arm.set_named_target("happy_end_2")
    arm.go()

    print("happy_end_init")
    arm.set_named_target("happy_end_init")
    arm.go()

    print("happy_end_3")
    arm.set_named_target("happy_end_3")
    arm.go()

    print("happy_end_init")
    arm.set_named_target("happy_end_init")
    arm.go()

    print("happy_end_-rotate")
    arm.set_named_target("happy_end_-rotate")
    arm.go()

    print("happy_end_+rotate")
    arm.set_named_target("happy_end_+rotate")
    arm.go()

    print("happy_end_init")
    arm.set_named_target("happy_end_init")
    arm.go()

    print("Close gripper")
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print("Open gripper")
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()
    
    print("Close gripper")
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print("Open gripper")
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

    print("Close gripper")
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print("Open gripper")
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

    print("Close gripper")
    gripper.set_joint_value_target([0.015, 0.015])
    gripper.go()

    print("init_pose")
    arm.set_named_target("init")
    arm.go()
    # """

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass