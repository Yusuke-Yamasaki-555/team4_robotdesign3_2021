#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from re import A, M
import rospy
import moveit_commander
import rosnode
from math import pi, sin, cos
from std_msgs.msg import Float32, Bool, String, Int32
from tf.transformations import quaternion_from_euler
import geometry_msgs.msg
# from img_process import target_sub_topic_name, target_pub_topic_name, club_pub_topic_name, club_sub_topic_name


def radian(deg):
    return pi/180*deg

class Motion_process:
    def __init__(self, srdf_name):
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.arm.set_max_velocity_scaling_factor(0.1)
        self.arm.set_max_acceleration_scaling_factor(1.0)
        self.gripper = moveit_commander.MoveGroupCommander("gripper")
        self.srdf_name = srdf_name
    
    def set_pub(self, topic_name):
        self.search_pub = rospy.Publisher(topic_name[0], String, queue_size=1)
        self.adjustX_pub = rospy.Publisher(topic_name[1], Int32, queue_size=1)
        self.adjustY_pub = rospy.Publisher(topic_name[2], Int32, queue_size=1)
    
    def set_sub(self, topic_name):
        self.search_sub = rospy.Subscriber(topic_name[0], Bool, self.is_search)
        self.adjustY_sub = rospy.Subscriber(topic_name[1], Int32, self.adjustX)
        self.adjustY_sub = rospy.Subscriber(topic_name[2], Int32, self.adjustY)

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
        # print(arm_goal_pose)
        rospy.sleep(1.0)
    
    def is_search(self, data):
        global isSearch
        rospy.loginfo(f'result={data.data}')
        isSearch = data.data

    def adjustX(self, data):
        global moveX
        rospy.loginfo(data.data)
        moveX = data.data
    
    def adjustY(self, data):
        global moveY
        rospy.loginfo('start adjustment of y')
        moveY = data.data

    def search_target(self):
        global isSearch, moveX, moveY
        isSearch = False
        self.set_position('search_target')
        
        for deg in range(60, -90, -1):
            # self.gripper.set_joint_value_target([0.34, 0.34])
            # self.gripper.go()
            self.search_pub.publish('search')
            if isSearch:
                rospy.loginfo('Find')
                rospy.sleep(2.5)
                move = 0
                moveX, moveY = 1, 1
                while moveX:
                    self.adjustX_pub.publish(377)
                    move += 0.5*moveX
                    self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)-radian(move)}) #根本を回転
                    self.arm.go()
                rospy.sleep(1.0)
                deg -= move
                move = 0
                while moveY:
                    move += 0.5*moveY
                    self.adjustY_pub.publish(227)
                    self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.75-radian(move)}) #根本を回転
                    self.arm.go()
                rospy.sleep(1.0)
                self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.75})
                isSearch = False
            self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radian(deg)}) #根本を回転
            self.arm.go()
        self.arm.set_named_target("init")
        self.arm.go()
    
    def search_club(self):
        global isSearch, moveX, moveY
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
    target.set_pub(target_pub_topic_name)
    target.set_sub(target_sub_topic_name)
    club.set_pub(club_pub_topic_name)
    club.set_sub(club_sub_topic_name)
    club.grip_club()
    target.search_target()
    # club.search_club()
    
    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)

if __name__ == '__main__':
    moveX, moveY  = 1, 1
    target_sub_topic_name = ['search_target_report', 'adjustX_target_report', 'adjustY_target_report']
    club_sub_topic_name = ['search_club_report', 'adjustX_club_report', 'adjustY_club_report']
    target_pub_topic_name = ['search_target', 'adjustX_target', 'adjustY_target']
    club_pub_topic_name = ['search_club', 'adjustX_club', 'adjustY_club']
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)
