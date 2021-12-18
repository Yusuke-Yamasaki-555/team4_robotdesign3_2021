#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import actionlib
import moveit_commander
import rosnode
from math import sin, cos, radians
from std_srvs.srv import SetBool, SetBoolResponse
from team4_robotdesign3_2021.srv import SetInt32
from team4_robotdesign3_2021.msg import ActSignalFeedback, ActSignalResult, ActSignalAction
from tf.transformations import quaternion_from_euler
import geometry_msgs.msg
import random

sum_deg = 0

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
        vel = 0.5
        acc = 0.5
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:init")
        self.arm.set_named_target("init") #  SRDFからinitのステータスを読み込み
        self.arm.go()

    def stand_by(self):
        vel = 0.5
        acc = 0.5
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:stand_by")
        self.arm.set_named_target("stand_by") #  SRDFからholdのステータスを読み込み
        self.arm.go()

    def hold(self):
        vel = 0.5
        acc = 0.5
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:hold")
        self.arm.set_named_target("hold") #  SRDFからholdのステータスを読み込み
        self.arm.go()

class ImageProcessServer:
    def __init__(self):
        self.srv_search_club = rospy.ServiceProxy('img_search_club', SetBool)
        self.srv_search_target = rospy.ServiceProxy('img_search_target', SetBool)
        self.srv_adjusty = rospy.ServiceProxy('img_adjusty', SetInt32)
        self.srv_adjustx = rospy.ServiceProxy('img_adjustx', SetInt32)
        self.srv_remove_club = rospy.ServiceProxy('remove_club', SetInt32)
        self.srv_remove_target = rospy.ServiceProxy('remove_target', SetInt32)
        print('finished setting image server')
    
class Motion_process:
    def __init__(self):
        self.preparation = Preparation_motion()
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.gripper = moveit_commander.MoveGroupCommander("gripper")
        self.img_srv = ImageProcessServer()
        self.tilt = rospy.ServiceProxy('tilt_neck', SetBool)
        self.happy_club = rospy.ServiceProxy('happy_club', SetBool)
        self.delta_deg = 31
        self.AR_id = 0
        self.goalx_coord = 377
        self.t_goaly_coord = 227
        self.c_goaly_coord = 160 #simulator: 160, actual machine:
        self.result = ActSignalResult()
        self.feedback = ActSignalFeedback()

    def release_club_motion(self,data):
        """
        この関数では、release_club をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
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
        vel = 0.05
        acc = 0.15
        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        
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
            self.feedback.BoolFB = self.arm.go()
            self.feedback.Int32FB = 0

            swing_club.publish_feedback(self.feedback)
            rospy.sleep(1.0)
            if swing_club.is_preempt_requested():
                self.preparation.init()
                self.result.BoolRes = False
                swing_club.set_preempted(self.result)
                return

            vel = 1.0
            acc = 1.0
            self.arm.set_max_velocity_scaling_factor(vel)
            self.arm.set_max_acceleration_scaling_factor(acc)

            print("==server:swing_club")
            # rand = random.randint(0, 10)
            # test_code
            if goal.Int32In == 0:
                rand = 10
            else:
                rand = 0
            # /test_code
            self.arm.set_named_target("swing_club")
            if rand <= 7: # 成功パターン
                z_axis_1 = current_pose[0] + 0.611 # deg35
            else: # 失敗パターン
                z_axis_1 = current_pose[0] - 0.262 # deg15              
            self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
            self.arm.go()
            self.arm.set_joint_value_target({"crane_x7_lower_arm_revolute_part_joint":0})
            self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint": radians(-90)})
            self.arm.set_joint_value_target({"crane_x7_shoulder_revolute_part_tilt_joint": radians(0)})
            self.arm.go()
        self.result.BoolRes = True
        self.result.Int32Res = 0
        swing_club.set_succeeded(self.result)

        print("server:motion_process Ready\n")
    def set_position(self, srdf_name):
        print("set")
        self.arm.set_named_target(srdf_name)
        self.arm.go()
        rospy.sleep(1.0)

    def search_target(self, goal):
        global sum_deg
        if goal.BoolIn:
            global target_id
            self.arm.set_max_velocity_scaling_factor(0.5)
            self.arm.set_max_acceleration_scaling_factor(0.5)
            if goal.BoolIn:
                print('called')
                current_deg = 0
                deg = goal.Int32In
                self.set_position('search_target')
                while True:
                    self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg)}) #根本を回転
                    self.arm.go()
                    rospy.sleep(1.0)
                    sum_deg += self.delta_deg
                    search_res = self.img_srv.srv_search_target(True)
                    self.feedback.BoolFB = search_res.success
                    self.feedback.Int32FB = sum_deg
                    search_target_server.publish_feedback(self.feedback)
                    if search_target_server.is_preempt_requested():
                        print('preempt')
                        rospy.sleep(0.5)
                        emotion = self.tilt(True)
                        self.result.Int32Res = deg
                        self.result.BoolRes = True #中止のときTrue
                        self.result.StrRes = 'not'
                        search_target_server.set_preempted(self.result)
                        return None
                    
                    if search_res.success:
                        search_res_msg = search_res.message.split(', ')
                        _, target_id = search_res_msg[0], int(search_res_msg[1])
                        self.result.BoolRes = False
                        self.result.StrRes = 'dislike' if target_id == 10 else 'swing'
                        rospy.loginfo(f'Find_t, res={self.result.StrRes}')
                        rospy.sleep(0.1)
                        move = 0
                        while True:
                            moveX = self.img_srv.srv_adjustx(self.goalx_coord)
                            rospy.loginfo(moveX)
                            if moveX.int32Out == 0:
                                current_deg = int(deg-move)
                                move = 0
                                break
                            move += 1.5*moveX.int32Out
                            self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg-move)}) #根本を回転
                            self.arm.go()

                        while True:
                            moveY = self.img_srv.srv_adjusty(self.t_goaly_coord)
                            rospy.loginfo(moveY)
                            if not moveY.int32Out:
                                move = 0
                                break
                            move += 1.5*moveY.int32Out
                            self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint":-1.88-radians(move)})
                            self.arm.set_joint_value_target({"crane_x7_shoulder_revolute_part_tilt_joint": 0.43-radians(move)})
                            self.arm.go()
                        break
                    deg += self.delta_deg
                print('finish process')
                self.result.Int32Res = current_deg - 3
                search_target_server.set_succeeded(result=self.result)
                print('sent result')
            
    def search_club(self, goal):
        if goal.BoolIn:
            self.arm.set_max_velocity_scaling_factor(0.5)
            self.arm.set_max_acceleration_scaling_factor(0.5)
            print('called')
            self.set_position('search_club')
            sum_deg = 0
            deg = goal.Int32In
            while True:
                self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg)}) #根本を回転
                self.arm.go()
                sum_deg += self.delta_deg
                search_res = self.img_srv.srv_search_club(True)
                self.feedback.BoolFB = search_res.success
                self.feedback.Int32FB = sum_deg
                search_club_server.publish_feedback(self.feedback)
                if search_club_server.is_preempt_requested():
                    emotion = self.tilt(True)
                    self.result.Int32Res = deg
                    self.result.BoolRes = False
                    self.result.StrRes = 'not'
                    search_club_server.set_preempted(self.result)
                    return None

                if search_res.success:
                    search_res_msg = search_res.message.split(', ')
                    self.AR_id = int(search_res_msg[1])
                    self.result.StrRes = 'find'
                    self.result.BoolRes = True
                    print(f'deg = {deg}')
                    rospy.loginfo('Find_c')
                    move = 0
                    while True:
                        moveX = self.img_srv.srv_adjustx(self.goalx_coord)
                        move += moveX.int32Out*2
                        self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(deg-move)}) #根本を回転
                        self.arm.go()
                        if moveX.int32Out == 0:
                            current_deg = radians(deg-move)
                            move = 0
                            break
                    while True:
                        moveY = self.img_srv.srv_adjusty(self.c_goaly_coord)
                        move -= moveY.int32Out*2
                        self.arm.set_joint_value_target({"crane_x7_upper_arm_revolute_part_rotate_joint": -1.88+radians(move)})
                        self.arm.set_joint_value_target({"crane_x7_shoulder_revolute_part_tilt_joint": 0.26-radians(move)})
                        self.arm.go()
                        if moveY.int32Out == 0:
                            move = 0
                            break
                    emotion = self.happy_club(True)
                    self.grip_club(current_deg=current_deg)
                    rospy.loginfo("grip")
                    self.preparation.stand_by()
                    rospy.loginfo("stand_by")
                    self.preparation.hold()
                    rospy.loginfo("hold")
                    remove = self.img_srv.srv_remove_club(self.AR_id)
                    print(f'removed id = {remove.int32Out}')
                    break
                deg += self.delta_deg
            self.result.Int32Res = sum_deg
            search_club_server.set_succeeded(result=self.result)
    
    def grip_club(self, current_deg):
        CLUB_Z_POSITION = 0.065 + 0.02
        arm_goal_pose = self.arm.get_current_pose().pose
        self.gripper.set_joint_value_target([0.9, 0.9])
        self.gripper.go()
        rospy.sleep(1.0)
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = arm_goal_pose.position.x + 0.005 * cos(current_deg)
        target_pose.position.y = arm_goal_pose.position.y + 0.005 * sin(current_deg)
        target_pose.position.z = CLUB_Z_POSITION
        # q = quaternion_from_euler(-3.14, 0.0, 0.0) #下向き
        target_pose.orientation.x = arm_goal_pose.orientation.x
        target_pose.orientation.y = arm_goal_pose.orientation.y
        target_pose.orientation.z = arm_goal_pose.orientation.z
        target_pose.orientation.w = arm_goal_pose.orientation.w
        # target_pose.orientation.x = q[0]
        # target_pose.orientation.y = q[1]
        # target_pose.orientation.z = q[2]
        # target_pose.orientation.w = q[3]
        self.arm.set_pose_target(target_pose)
        self.arm.go()
        self.gripper.set_joint_value_target([0.2, 0.2])
        self.gripper.go()
        self.arm.set_joint_value_target({"crane_x7_lower_arm_revolute_part_joint":0})
        self.arm.set_joint_value_target({"crane_x7_wrist_joint":-1.57})
        self.arm.go()
    
    def check_target(self, goal):
        if goal.BoolIn:
            self.arm.set_max_velocity_scaling_factor(0.5)
            self.arm.set_max_acceleration_scaling_factor(0.5)
            self.set_position('search_target')
            self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":radians(goal.Int32In)}) #根本を回転
            self.arm.go()
            rospy.sleep(2)
            search_res = self.img_srv.srv_search_target(True)
            search_res_msg = search_res.message.split(', ')
            judge = search_res_msg[0]
            self.feedback.BoolFB = search_res.success
            self.feedback.Int32FB = goal.Int32In
            check_target_server.publish_feedback(self.feedback)
            rospy.sleep(0.1)
            print(f'self.AR_id = {target_id}')
            #倒せていない場合は中断
            if check_target_server.is_preempt_requested():
                emotion = self.tilt(True)
                self.result.BoolRes = False
                self.result.StrRes = 'not'
                check_target_server.set_preempted(self.result)
                return None
            #
            if search_res.success and target_id != 10:
                rospy.loginfo('remain')
                self.result.BoolRes = False
                self.result.StrRes = 'remain'
            else:
                rospy.loginfo('completed')
                self.result.BoolRes = True
                self.result.StrRes = 'completed'
            check_target_server.set_succeeded(result=self.result)
    
    def remove_target(self, data):
        if data.data:
            resp = SetBoolResponse()
            remove = self.img_srv.srv_remove_target(target_id)
            print(f'removed ID: {target_id}')
            resp.message = 'removed'
            resp.success = True
            return resp

def main():
    global search_club_server, search_target_server, check_target_server, swing_club
    rospy.init_node("motion_process", anonymous=1)
    motion_server = Motion_process()
    wait_servers = ['img_search_club', 'img_search_target', 'img_adjustx', 'img_adjusty', 'tilt_neck', 'remove_club', 'remove_target']
    for server in wait_servers:
        rospy.wait_for_service(server)
    release_club = rospy.Service('release_club', SetBool, motion_server.release_club_motion)
    remove_target = rospy.Service('remove_target_id', SetBool, motion_server.remove_target)
    search_club_server = actionlib.SimpleActionServer('search_club', ActSignalAction, motion_server.search_club, False)
    search_target_server = actionlib.SimpleActionServer('search_target', ActSignalAction, motion_server.search_target, False)
    check_target_server = actionlib.SimpleActionServer('check_target', ActSignalAction, motion_server.check_target, False)
    swing_club = actionlib.SimpleActionServer('swing_club', ActSignalAction, motion_server.swing_club_motion, False)
    search_club_server.start()
    search_target_server.start()
    check_target_server.start()
    swing_club.start()
    print('finished server setting')
    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)
