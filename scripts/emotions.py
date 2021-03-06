#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler

from std_srvs.srv import SetBool, SetBoolResponse #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message )

# グローバル変数
vel = 1.0  # set_max_velocity_scaling_factorの引数
acc = 1.0  # set_max_acceleration_scaling_factorの引数

def main():  # このnodeの玄関
    """
    この中でいつもの定型文を書く。
    node名：emotions
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
    rospy.sleep(1.0)
    class Emotions_Serverのインスタンスを作成
    各サービスのインスタンスを作成
    while not rospy.is_shutdown():
        rospy.spin()   
    """ 
    rospy.init_node("emotions")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    server = Emotions_Server()  # Emotions_Serverのインスタンス化
    bow = rospy.Service("bow", SetBool, server.bow_motion)  # bow のservice開始
    tilt_neck = rospy.Service("tilt_neck", SetBool, server.tilt_neck_motion)
    dislike = rospy.Service('dislike', SetBool, server.dislike_motion)
    happy_club = rospy.Service("happy_club", SetBool, server.happy_club_motion)
    happy_end = rospy.Service("happy_end", SetBool, server.happy_end_motion)

    print("server:emotions Ready\n")
    rospy.spin()  # 無限ループ

class Preparation_motion:  # Emotions_Serverから呼び出される、基本動作の関数をまとめたクラス
    def __init__(self):
        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.gripper = moveit_commander.MoveGroupCommander("gripper")

    def init(self):  # 棒立ちの動作
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:init")
        self.arm.set_named_target("init") #  SRDFからinitのステータスを読み込み
        self.arm.go() #  
        
    def stand_by(self):
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:stand_by")
        self.arm.set_named_target("stand_by")
        self.arm.go() #  動作の実行

    def emotions_stand_by(self):
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:emotions_stand_by")
        self.arm.set_named_target("emotions_stand_by")
        self.arm.go() #  動作の実行


class Emotions_Server: 
    def __init__(self):
        self.preparation = Preparation_motion()  # このクラス内で使えるように、Preparation_motionをインスタンス化

        self.arm = moveit_commander.MoveGroupCommander("arm")
        self.gripper = moveit_commander.MoveGroupCommander("gripper")

    def bow_motion(self, data):  # お辞儀をする動作（data:clientからの入力データ）
        # グローバル変数のvelとaccの値を、お辞儀用の値にする
        global vel, acc
        vel = 0.5
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # お辞儀の動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                print("server:Reset pose")
                self.preparation.init()

                print("server:Start bow")
                print("==server:bow")
                self.arm.set_named_target("bow")
                self.arm.go()

                self.preparation.init() #  class:Preparation_motion内のinit関数を実行

                resp.message = "client:Success bow_motion\n"
                resp.success = True
                print("server:Finish bow_motion\n")
            except:
                resp.message = "client:Failure bow_motion\n"
                resp.success = False
        
        print("server:emotions Ready\n")
        return resp
            
    def tilt_neck_motion(self,data):  # 首を傾げる動作
        global vel, acc
        vel = 1.0
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # 首を傾げる動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                # current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得

                print("server:Start tilt_neck")
                self.preparation.emotions_stand_by() #  class:Preparation_motion内のemotions_stand_by関数を実行
                rospy.sleep(0.5)

                acc = 1.0
                self.arm.set_max_acceleration_scaling_factor(acc)

                print("==server:tilt_neck")
                self.arm.set_named_target("tilt_neck")
                self.arm.set_joint_value_target({"crane_x7_shoulder_fixed_part_pan_joint":0}) #根本を回転
                self.arm.go()
                
                rospy.sleep(0.3)

                print("==server:rev_tilt_neck")
                self.arm.set_named_target("rev_tilt_neck")
                self.arm.go()

                self.preparation.stand_by()
                # self.arm.set_joint_value_target(current_pose)
                # self.arm.go()

                resp.message = "client:Success tilt_neck\n"
                resp.success = True
                print("server:Finish tilt_neck\n")
            except:
                resp.message = "client:Failure tilt_neck\n"
                resp.success = False

        print("server:emotions Ready\n")
        return resp

    def dislike_motion(self,data):
        """
        この関数では、dislike をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
        global vel, acc
        vel = 1.0
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # 首を傾げる動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                # current_pose_init = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得

                print("server:Start dislike")
                self.preparation.emotions_stand_by() #  class:Preparation_motion内のemotions_stand_by関数を実行
                rospy.sleep(0.5)
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()
                print("==server:dislike_1")
                self.arm.set_named_target("dislike_1")
                current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()
                # ここのif文は関数にするべき
                if current_pose[0] >= 0.01:
                    z_axis_1 = current_pose[0] - 0.559
                    flag = True
                else:
                    z_axis_1 = current_pose[0] + 0.559
                    flag = False
                
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
                self.arm.go()
                print("==server:dislike_2")
                self.arm.set_named_target("dislike_2")
                current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()
                # ここのif文は関数にするべき
                if flag:
                    z_axis_1 = current_pose[0] - 0.559
                else:
                    z_axis_1 = current_pose[0] + 0.559
                
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
                self.arm.go()
                print("==server:dislike_3")
                self.arm.set_named_target("dislike_3")
                current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()
                    
                # ここのif文は関数にするべき
                if flag:
                    z_axis_1 = current_pose[0] - 0.559
                else:
                    z_axis_1 = current_pose[0] + 0.559
                
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
                self.arm.go()
                print("==server:dislike_4")
                self.arm.set_named_target("dislike_4")
                current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()

                # ここのif文は関数にするべき
                if flag:
                    z_axis_1 = current_pose[0] - 0.559
                else:
                    z_axis_1 = current_pose[0] + 0.559
                
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
                self.arm.go()
                print("==server:dislike_5")
                self.arm.set_named_target("dislike_5")
                current_pose = self.arm.get_current_joint_values() #  現在の各関節の角度の値をリストで取得
                self.gripper.set_joint_value_target([0.2, 0.2])
                self.gripper.go()

                # ここのif文は関数にするべき
                if flag:
                    z_axis_1 = current_pose[0] - 0.559
                else:
                    z_axis_1 = current_pose[0] + 0.559
                
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",z_axis_1) #  現在の第一関節z軸+-deg34        
                self.arm.go()

                self.preparation.stand_by()
                # self.arm.set_joint_value_target(current_pose_init)
                # self.arm.go()

                resp.message = "client:Success dislike\n"
                resp.success = True
                print("server:Finish dislike\n")
            except:
                resp.message = "client:Failure dislike\n"
                resp.success = False

        print("server:emotions Ready\n")
        return resp

    def happy_club_motion(self,data):
        """
        この関数では、happy_club をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
        global vel, acc
        vel = 0.5
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        resp = SetBoolResponse()
        if data.data == True:
            try:
                current_pose = self.arm.get_current_joint_values()

                print("server:Start happy_club")
                print("==server:current_pose")
                print(current_pose)
                print("")

                print("==server:happy_club")
                self.arm.set_named_target("happy_club")
                self.arm.set_joint_value_target("crane_x7_shoulder_fixed_part_pan_joint",current_pose[0]) #  現在の第一関節z軸を維持
                self.arm.go()
            # 手を開閉させて喜ぶ(happy_club)
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                self.arm.set_joint_value_target(current_pose)
                self.arm.go()

                resp.message = "client:Success happy_club_motion\n"
                resp.success = True
                print("server:Finish happy_club_motion\n")
            except:
                resp.message = "client:Failure happy_club_motion\n"
                resp.success = False
        
        print("server:emotions Ready\n")
        return resp

    def happy_end_motion(self,data):
        """
        この関数では、happy_end をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
        global vel, acc
        vel = 1.0
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # 首を傾げる動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                current_pose = self.arm.get_current_joint_values()

                print("server:Start happy_end")
                print("===server:Open gripper")
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()

                print("==server:happy_end_1")
                self.arm.set_named_target("happy_end_1")
                self.arm.go()

                print("==server:happy_end_init")
                self.arm.set_named_target("happy_end_init")
                self.arm.go()

                print("==server:happy_end_2")
                self.arm.set_named_target("happy_end_2")
                self.arm.go()

                print("==server:happy_end_init")
                self.arm.set_named_target("happy_end_init")
                self.arm.go()

                # print("==server:happy_end_3")
                # self.arm.set_named_target("happy_end_3")
                # self.arm.go()

                # print("==server:happy_end_init")
                # self.arm.set_named_target("happy_end_init")
                # self.arm.go()

                # print("==server:happy_end_-rotate")
                # self.arm.set_named_target("happy_end_-rotate")
                # self.arm.go()

                # print("==server:happy_end_+rotate")
                # self.arm.set_named_target("happy_end_+rotate")
                # self.arm.go()

                # print("==server:happy_end_init")
                # self.arm.set_named_target("happy_end_init")
                # self.arm.go()

                print("==server:Close gripper")
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                print("==server:Open gripper")
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()
                
                print("==server:Close gripper")
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                print("==server:Open gripper")
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()

                print("==server:Close gripper")
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                print("==server:Open gripper")
                self.gripper.set_joint_value_target([0.8, 0.8])
                self.gripper.go()

                print("==server:Close gripper")
                self.gripper.set_joint_value_target([0.015, 0.015])
                self.gripper.go()

                print("==server:init_pose")
                # self.arm.set_named_target("init")
                self.arm.set_joint_value_target(current_pose)
                self.arm.go()

                resp.message = "client:Success happy_end\n"
                resp.success = True
                print("server:Finish happy_end\n")
            except:
                resp.message = "client:Failure happy_end\n"
                resp.success = False

        print("server:emotions Ready\n")
        return resp


if __name__ == '__main__':
    """
    いつものように try except を組んで、main()を実行
    """
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass