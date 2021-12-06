#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from math import sin, cos, radians
import random


import actionlib
from std_srvs.srv import SetBool, SetBoolResponse #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message ) release_club用
from team4_robotdesign3_2021.srv import SetInt32
from team4_robotdesign3_2021.msg import ActSignalAction, ActSignalGoal, ActSignalFeedback, ActSignalResult

# グローバル変数
vel = 1.0  # set_max_velocity_scaling_factorの引数
acc = 1.0  # set_max_acceleration_scaling_factorの引数

def main():
    global search_club_server, search_target_server, swing_club # actionのインスタンスをグローバル化

    rospy.init_node("motion_process")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    server = Motion_Process_Server()  # Motino_Process_Serverのインスタンス化

    # img_processのサーバを待つ
    rospy.wait_for_service("img_search_club")
    rospy.wait_for_service("img_adjustx_club")
    rospy.wait_for_service("img_adjusty_club")
    rospy.wait_for_service("img_search_target")
    rospy.wait_for_service("img_adjustx_target")
    rospy.wait_for_service("img_adjusty_target")
    
    # ここで、各サーバを立ち上げ、及び開始
    release_club = rospy.Service('release_club', SetBool, server.release_club_motion)
    search_club_server = actionlib.SimpleActionServer('search_club', ActSignalAction, server.search_club, False)
    search_target_server = actionlib.SimpleActionServer('search_target', ActSignalAction, server.search_target, False)
    swing_club = actionlib.SimpleActionServer('swing_club', ActSignalAction, server.swing_club_motion, False)

    search_club_server.start()
    search_target_server.start()
    swing_club.start()

    print("server:motion_process Ready\n")
    
    """# Test Code
    goal = ActSignalGoal
    goal.BoolIn = True
    goal.Int32In = 0
    goal.StrIn = "a"
    server.search_club(goal)
    server.search_target(goal)
    server.swing_club_motion(goal)
    """# /Test Code
    rospy.spin()  # 無限ループ 


class Preparation_motion:  # Motion_Process_Serverから呼び出される、基本動作の関数をまとめたクラス
    """
    このクラスでは、init , stand_by , hold をそれぞれ関数として持ち、class Motion_Process_Serverに提供する
    Serverにはならない
    各関数の最後：return 動作結果
    """
    def __init__(self):
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.gripper = moveit_commander.MoveGroupCommander("gripper")

    def init(self):  # 棒立ちの動作
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:init")
        self.arm.set_named_target("init") #  SRDFからinitのステータスを読み込み
        self.arm.go()

    # def stand_by

    def hold(self):  # 
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:hold")
        self.arm.set_named_target("hold") #  SRDFからholdのステータスを読み込み
        self.arm.go()

class ImageProcessServer:
    def __init__(self):
        self.srv_search_club = rospy.ServiceProxy('img_search_club', SetBool)
        self.srv_adjustx_club = rospy.ServiceProxy('img_adjustx_club', SetInt32)
        self.srv_adjusty_club = rospy.ServiceProxy('img_adjustxy_club', SetInt32)
        self.srv_search_target = rospy.ServiceProxy('img_search_target', SetBool)
        self.srv_adjustx_target = rospy.ServiceProxy('img_adjustx_target', SetInt32)
        self.srv_adjusty_target = rospy.ServiceProxy('img_adjusty_target', SetInt32)

class Motion_Process_Server(object):
    def __init__(self):
        self.preparation = Preparation_motion()  # このクラス内で使えるように、Preparation_motionをインスタンス化
        self.img_srv = ImageProcessServer()
        self.tilt = rospy.ServiceProxy('tilt_neck', SetBool)
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.gripper = moveit_commander.MoveGroupCommander("gripper")
    # __init__(self):
    """
        class Preparation_motionのインスタンス作成
        各Action_Serverの立ち上げ＆start
    """
    def set_position(self, srdf_name):
        print("set")
        self.arm.set_named_target(srdf_name)
        self.arm.go()
        rospy.sleep(1.0)

    def release_club_motion(self,data):
        """
        この関数では、release_club をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
        global vel, acc
        vel = 0.5
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # お辞儀の動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                print("server:Start release_club")
                print("==server:release_club")
                self.arm.set_named_target("release_club")
                self.arm.go()

                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()

                self.preparation.init() #  class:Preparation_motion内のinit関数を実行

                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                resp.message = "client:Success release_club_motion\n"
                resp.success = True
                print("server:Finish release_club_motion\n")
            except:
                resp.message = "client:Failure release_club_motion\n"
                resp.success = False
        
        print("server:motion_process Ready\n")
        return resp
            

    def swing_club_motion(self,goal):
        """
        この関数では、swing_club をする動作をActionとして提供する
        swing_set_club
            動作の速度＆加速度の比率を定義
            動作を行う(test.py参照)
            動作の完了報告をfeedback
        swing_club
            動作の速度＆加速度の比率を定義
            動作を行う(test.py参照)
                ここで、印に当てるか外すかを決めてから、動作を行う
            動作の完了報告を返す
        """
        global vel, acc
        vel = 0.05
        acc = 0.15
        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        result = ActSignalResult()
        feedback = ActSignalFeedback()
        if goal.BoolIn == True:
            print(goal.StrIn) # "server:Start swing_club"
            print("==server:swing_set_club")
            self.arm.set_named_target("swing_set_club")
            # test code
            # self.arm.set_named_target("swing_club")
            # /test code
            current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
            z_axis_1 = current_pose[0] - 0.698 # deg40
            self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
            feedback.BoolFB = self.arm.go()
            feedback.Int32FB = 0

            swing_club.publish_feedback(feedback)
            rospy.sleep(1.0)
            if swing_club.is_preempt_requested():
                self.preparation.init()
                result.BoolRes = False
                swing_club.set_preempted(result)
                return

            vel = 1.0
            acc = 1.0
            self.arm.set_max_velocity_scaling_factor(vel)
            self.arm.set_max_acceleration_scaling_factor(acc)

            print("==server:swing_club")
            rand = random.randint(0, 10)
            # test_code
            rand = 10
            # /test_code
            self.arm.set_named_target("swing_club")
            if rand <= 7: # 成功パターン
                z_axis_1 = current_pose[0] + 0.611 # deg35
            else: # 失敗パターン
                z_axis_1 = current_pose[0] - 0.262 # deg15              
            self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
            self.arm.go()

        result.BoolRes = True
        result.Int32Res = 0
        swing_club.set_succeeded(result)

        print("server:motion_process Ready\n")
            
    def search_club(self, goal):
        global vel, acc
        vel = 0.1
        acc = 1.0
        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        if goal.BoolIn == True:
            feedback = ActSignalFeedback()
            result = ActSignalResult()
            print('called')
            self.set_position('search_club')
            sum_deg = 0
            current_deg = 0
            deg = goal.Int32In
            while True:
                self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg)}) #根本を回転
                self.arm.go()
                sum_deg += 1
                emotion = self.tilt(True) if sum_deg % 45 == 0 else self.tilt(False)
                print(emotion.success, emotion.message)
                search_res = self.img_srv.srv_search_club(True)
                feedback.BoolFB = search_res.success
                feedback.Int32FB = sum_deg
                search_club_server.publish_feedback(feedback)
                if search_club_server.is_preempt_requested():
                    result.Int32Res = sum_deg
                    result.BoolRes = False
                    result.StrRes = 'not'
                    search_club_server.set_preempted(result)

                if search_res.success:
                    result.StrRes = 'find'
                    result.BoolRes = True
                    print(f'deg = {deg}')
                    rospy.loginfo('Find_c')
                    move = 0
                    while True:
                        moveX = self.img_srv.srv_adjustx_club(377)
                        move += 0.5*moveX.int32Out
                        self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg-move)}) #根本を回転
                        self.arm.go()
                        if moveX.int32Out == 0:
                            current_deg = radians(deg-move)
                            move = 0
                            break
                    self.grip_club(current_deg = current_deg)
                    rospy.loginfo("grip")
                    break
                deg += 1
            result.Int32Res = sum_deg
            search_club_server.set_succeeded(result=result)
    
    def grip_club(self, current_deg):
        ABS_CLUB_POSITION = 0.25
        CLUB_Z_POSITION = 0.065 + 0.02
        arm_goal_pose = self.arm.get_current_pose().pose
        self.gripper.set_joint_value_target([0.9, 0.9])
        self.gripper.go()
        rospy.sleep(1.0)
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = ABS_CLUB_POSITION * cos(current_deg)
        target_pose.position.y = ABS_CLUB_POSITION * sin(current_deg)
        target_pose.position.z = CLUB_Z_POSITION
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
        
    def search_target(self, goal):
        global vel, acc
        vel = 0.1
        acc = 1.0
        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        feedback = ActSignalFeedback()
        result = ActSignalResult()
        if goal.BoolIn:
            print('called')
            sum_deg = 0
            current_deg = 0
            deg = goal.Int32In
            self.set_position('search_target')
            while True:
                self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg)}) #根本を回転
                self.arm.go()
                sum_deg += 1
                emotion = self.tilt(True) if sum_deg % 45 == 0 else self.tilt(False)
                print(emotion.success, emotion.message)
                search_res = self.img_srv.srv_search_target(True)
                feedback.BoolFB = search_res.success
                feedback.Int32FB = sum_deg
                search_target_server.publish_feedback(feedback)
                if search_target_server.is_preempt_requested():
                    print('preempt')
                    emotion = self.tilt(True)
                    result.Int32Res = sum_deg
                    result.BoolRes = False
                    result.StrRes = 'not'
                    search_target_server.set_preempted(result)
                
                if search_res.success:
                    search_res_msg = search_res.message.split(', ')
                    search_finish, AR_id = search_res_msg[0], search_res_msg[1]
                    print(f'ARid={search_res_msg[1]}')
                    result.BoolRes = True if search_finish == 'end' else False
                    result.StrRes = 'not' if AR_id == '[10]' else 'swing'
                    rospy.loginfo(f'Find_t, res={result.StrRes}')
                    rospy.sleep(1.0)
                    move = 0
                    while True:
                        moveX = self.img_srv.srv_adjustx_target(377)
                        rospy.loginfo(moveX)
                        if moveX.int32Out == 0:
                            current_deg = int(deg-move)
                            move = 0
                            break
                        move += 0.5*moveX.int32Out
                        self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg-move)}) #根本を回転
                        self.arm.go()
                    rospy.sleep(1.0)

                    while True:
                        moveY = self.img_srv.srv_adjusty_target(227)
                        rospy.loginfo(moveY)
                        if not moveY.int32Out:
                            move = 0
                            break
                        move += 0.5*moveY.int32Out
                        self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.66-radians(move)}) #根本を回転
                        self.arm.go()
                    rospy.sleep(1.0)
                    break
                deg += 1
            print('finish process')
            result.Int32Res = current_deg
            search_target_server.set_succeeded(result=result)
            print('sent result')

    # def check_target(self,<クライアントから送られるデータ名>):
    """
        check_targetをactionとして提供
        check_targetから印を探す
        印の状態をfeedback(中止命令が来る)
        if 中止命令が来た→emotions:tilt_neck を実行後、終了
        完了報告をresult
    """

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)