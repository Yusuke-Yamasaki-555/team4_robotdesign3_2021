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

    print("server:emotions Ready")
    rospy.spin()  # 無限ループ

class Preparation_motion:  # Emotions_Serverから呼び出される、基本動作の関数をまとめたクラス
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    def init(self):  # 棒立ちの動作
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:init")
        self.arm.set_named_target("init") #  SRDFからinitのステータスを読み込み
        self.arm.go() #  
        
    def emotions_stand_by(self):  # 棒立ちの動作
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:emotions_stand_by")
        self.arm.set_named_target("emotions_stand_by")
        self.arm.go() #  動作の実行

class Emotions_Server: 
    preparation = Preparation_motion()  # このクラス内で使えるように、Preparation_motionをインスタンス化

    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

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
                print("server:Start bow")
                print("==server:bow")
                self.arm.set_named_target("bow")
                self.arm.go()
                self.preparation.init() #  class:Preparation_motion内のinit関数を実行
                resp.message = "client:Success bow_motion"
                resp.success = True
                print("server:Finish bow_motion")
            except:
                resp.message = "client:Failure bow_motion"
                resp.success = False
        return resp
            
    def tilt_neck_motion(self,data):  # 首を傾げる動作
        """
        この関数では、tile_neck をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
       動作を行う(test.py参照)
        動作の完了報告を返す
        """
        global vel, acc
        vel = 1.0
        acc = 0.35

        self.arm.set_max_velocity_scaling_factor(vel)
        self.arm.set_max_acceleration_scaling_factor(acc)

        # お辞儀の動作の処理
        resp = SetBoolResponse()
        if data.data == True:
            try:
                print("server:Start tilt_neck")
                self.preparation.emotions_stand_by() #  class:Preparation_motion内のemotions_stand_by関数を実行
                rospy.sleep(0.5)
                acc = 1.0
                self.arm.set_max_acceleration_scaling_factor(acc)
                print("==server:tilt_neck")
                self.arm.set_named_target("tilt_neck")
                self.arm.go()
                print("==server:rev_tilt_neck")
                self.arm.set_named_target("rev_tilt_neck")
                self.arm.go()
                resp.message = "client:Success tilt_neck"
                resp.success = True
                print("server:Finish tilt_neck")
            except:
                resp.message = "client:Failure tilt_neck"
                resp.success = False
        return resp


    # def dislike_motion(self,<クライアントから送られるデータ名>):
"""
        この関数では、dislike をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
"""

    # def happy_club_motion(self,<クライアントから送られるデータ名>):
"""
        この関数では、happy_club をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
"""

    # def happy_end_motion(self,<クライアントから送られるデータ名>):
"""
        この関数では、happy_end をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
"""

if __name__ == '__main__':
    """
    いつものように try except を組んで、main()を実行
    """
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass