#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import moveit_commander
import rosnode
from math import pi, sin, cos
from std_srvs.srv import SetBool
from team4_robotdesign3_2021.srv import SetInt32
from team4_robotdesign3_2021.msg import ActSignalActionGoal, ActSignalFeedback, ActSignalResult
from tf.transformations import quaternion_from_euler
import geometry_msgs.msg


def radian(deg):
    return pi/180*deg

class Motion_process:
    def __init__(self, srdf_name):
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.arm.set_max_velocity_scaling_factor(0.1)
        self.arm.set_max_acceleration_scaling_factor(1.0)
        self.gripper = moveit_commander.MoveGroupCommander("gripper")
        self.srdf_name = srdf_name

    # def release_club_motion(self,<クライアントから送られるデータ名>):

    # この関数では、release_club をする動作をServiceとして提供する
    # 動作の速度＆加速度の比率を定義
    # 動作を行う(test.py参照)
    # 動作の完了報告を返す

    # def swing_club_motion(self,<クライアントから送られるデータ名>):

    # この関数では、swing_club をする動作をActionとして提供する
    # swing_set_club
    #     動作の速度＆加速度の比率を定義
    #     動作を行う(test.py参照)
    #     動作の完了報告をfeedback
    # swing_club
    #     動作の速度＆加速度の比率を定義
    #     動作を行う(test.py参照)
    #         ここで、印に当てるか外すかを決めてから、動作を行う
    #     動作の完了報告を返す

    def set_position(self, srdf_name):
        print("set")
        arm_goal_pose = self.arm.get_current_pose().pose
        self.arm.set_named_target(srdf_name)
        self.arm.go()
        rospy.sleep(1.0)

    def search_target(self):
        self.set_position('search_target')
        for deg in range(-90, 60, 1):
            search_res = srv_search_target(True)
            if search_res.success:
                rospy.loginfo('Find')
                rospy.sleep(1.0)
                move = 0
                while True:
                    moveX = srv_adjustx_target(377)
                    rospy.loginfo(moveX)
                    if moveX.int32Out == 0:
                        break
                    move += 0.5*moveX.int32Out
                    self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)-radian(move)}) #根本を回転
                    self.arm.go()
                rospy.sleep(1.0)
                deg -= move
                move = 0
                while True:
                    moveY = srv_adjusty_target(227)
                    rospy.loginfo(moveY)
                    if not moveY.int32Out:
                        break
                    move += 0.5*moveY.int32Out
                    self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.75-radian(move)}) #根本を回転
                    self.arm.go()
                rospy.sleep(1.0)
            self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)}) #根本を回転
            self.arm.go()
        self.arm.set_named_target("init")
        self.arm.go()
    
    def search_club(self):
        isSearch = False
        self.set_position('hold')
        self.gripper.go()
        move = 0
        for deg in range(0, -110, -1):
            # self.gripper.set_joint_value_target([0.33, 0.33])
            # self.gripper.go()
            self.search_pub.publish('search')
            if isSearch:
                rospy.loginfo('Find')
                while moveX:
                    self.adjustX_pub.publish(337)
                    move += 0.5*moveX
                    self.arm.set_joint_value_target({"crane_x7_wrist_joint":radian(deg-move)})
                    self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)-radian(move)}) #根本を回転
                    self.arm.go()
                    deg -= move
                    move = 0
                while moveY:
                    self.adjustY_pub.publish(150)
                    move += 0.005*moveY
                    arm_goal_pose = self.arm.get_current_pose().pose
                    target_pose = geometry_msgs.msg.Pose()
                    target_pose.position.x = arm_goal_pose.position.x
                    target_pose.position.y = arm_goal_pose.position.y - move
                    target_pose.position.z = arm_goal_pose.position.z
                    q = quaternion_from_euler(0, 0.0, 0)
                    target_pose.orientation.x = q[0]#arm_goal_pose.orientation.x
                    target_pose.orientation.y = q[1]#arm_goal_pose.orientation.y
                    target_pose.orientation.z = q[2]#arm_goal_pose.orientation.z
                    target_pose.orientation.w = q[3]#arm_goal_pose.orientation.w
                    self.arm.set_pose_target( target_pose )
                    self.arm.go()
                    move = 0
                break
            move = 0
            moveX, moveY = 1, 1
            self.arm.set_joint_value_target({"crane_x7_wrist_joint":radian(0+deg)})
            self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)}) #根本を回転
            self.arm.go()
            
        # self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.75})
        isSearch = False
            
        # self.arm.set_named_target("init")
        # self.arm.go()
    
    def grip_club(self):
        # rospy.loginfo(data.data)
        rospy.sleep(1.0)
        self.set_position("hold")
        arm_goal_pose = self.arm.get_current_pose().pose
        self.gripper.set_joint_value_target([0.9, 0.9])
        self.gripper.go()
        rospy.sleep(1.0)
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = arm_goal_pose.position.x
        target_pose.position.y = 0.25
        target_pose.position.z = 0.065+0.02
        target_pose.orientation.x = arm_goal_pose.orientation.x
        target_pose.orientation.y = arm_goal_pose.orientation.y
        target_pose.orientation.z = arm_goal_pose.orientation.z
        target_pose.orientation.w = arm_goal_pose.orientation.w
        self.arm.set_pose_target( target_pose )
        self.arm.go()
        self.gripper.set_joint_value_target([0.3, 0.3])
        self.gripper.go()
        self.arm.set_joint_value_target({"crane_x7_lower_arm_revolute_part_joint":0})
        self.arm.set_joint_value_target({"crane_x7_wrist_joint":-1.57})
        self.arm.go()
        self.set_position('search_target')

def main():
    rospy.init_node("motion_process", anonymous=1)
    target = Motion_process("target")
    club = Motion_process("club")
    servers = ['search_club', 'adjustx_club', 'adjusty_club', 'search_target', 'adjustx_target', 'adjusty_target']
    for server in servers:
        rospy.wait_for_service(server)
    # club.grip_club()
    target.search_target()
    # club.search_club()
    
    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)

if __name__ == '__main__':
    srv_search_club = rospy.ServiceProxy('search_club', SetBool)
    srv_adjustx_club = rospy.ServiceProxy('adjustx_club', SetInt32)
    srv_adjusty_club = rospy.ServiceProxy('adjustxy_club', SetInt32)
    srv_search_target = rospy.ServiceProxy('search_target', SetBool)
    srv_adjustx_target = rospy.ServiceProxy('adjustx_target', SetInt32)
    srv_adjusty_target = rospy.ServiceProxy('adjusty_target', SetInt32)
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)
