#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
from tf.transformations import quaternion_from_euler
from math import pi
from std_msgs.msg import Float32, Bool, String, Float32MultiArray

def ros_setup(node_name):
    rospy.init_node(node_name)
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)
    return arm, gripper

arm, gripper = ros_setup(node_name="pose_groupstate_example")

def radian(deg):
    return pi/180*deg

def set_position():
    print("set")
    arm.set_named_target("search_target")
    arm.go()
    rospy.sleep(1.0)

FinishFlag = False

#画像処理の結果をもとに動く
def search(data):
    global FinishFlag
    if data.data == False:
        rospy.loginfo("False")
    elif data.data == True:
        rospy.loginfo("True")
        
        FinishFlag = True

def adjust(data):
    global FinishFlag
    rospy.sleep(2.5)
    arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":data.data})
    arm.go()
    rospy.loginfo("finish adjust")

def main():
    global FinishFlag
    node_names = ["search", "adjust"]
    set_position()
    for deg in range(-120, 120, 1):
        arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)}) #根本を回転
        arm.go()
        pub.publish("search")
        if FinishFlag == True:
            rospy.loginfo("Find")
            FinishFlag = False
            rospy.sleep(5)
            gripper.set_joint_value_target([0.9, 0.9])
            gripper.go()
            gripper.set_joint_value_target([0.7, 0.7])
            gripper.go()
    arm.set_named_target("init")
    arm.go()

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('search', String, queue_size=1)
        pub2 = rospy.Publisher('adjust', String, queue_size=1)
        sub = rospy.Subscriber("search_report", Bool, search)
        sub2 = rospy.Subscriber("adjust_report", Float32, adjust)
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
