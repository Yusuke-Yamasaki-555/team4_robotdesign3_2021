#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler

# import actionlib
# import <サービスのメッセージファイル> 
from std_srvs.srv import SetBool, SetBoolResponse #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message ) release_club用
# import <アクションのメッセージファイル>

# グローバル変数
vel = 1.0  # set_max_velocity_scaling_factorの引数
acc = 1.0  # set_max_acceleration_scaling_factorの引数

def main():
    rospy.init_node("motion_process")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    server = Motion_Process_Server()  # Motino_Process_Serverのインスタンス化

    release_club = rospy.Service('release_club', SetBool, server.release_club_motion)
    # ここで、各サーバを立ち上げ、及び開始

    print("server:motion_process Ready\n")
    rospy.spin()  # 無限ループ 


class Preparation_motion:  # Motion_Process_Serverから呼び出される、基本動作の関数をまとめたクラス
    """
    このクラスでは、init , stand_by , hold をそれぞれ関数として持ち、class Motion_Process_Serverに提供する
    Serverにはならない
    各関数の最後：return 動作結果
    """
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    def init(self):  # 棒立ちの動作
        self.arm.set_max_velocity_scaling_factor(vel) #  グローバルに設定されたfactorで動作
        self.arm.set_max_acceleration_scaling_factor(acc)

        print("==server:init")
        self.arm.set_named_target("init") #  SRDFからinitのステータスを読み込み
        self.arm.go()

    # def stand_by

    # def hold

class Motion_Process_Server(object):
    preparation = Preparation_motion()  # このクラス内で使えるように、Preparation_motionをインスタンス化

    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    # __init__(self):
    """
        class Preparation_motionのインスタンス作成
        各Action_Serverの立ち上げ＆start
    """
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
        
        print("server:emotions Ready\n")
        return resp
            

    # def swing_club_motion(self,<クライアントから送られるデータ名>):
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
    # def search_club(self,<クライアントから送られるデータ名>):
    """
        search_clubをactionとして提供
        while service:search_clubを使って、棒を探す(第一関節ｚ軸を一周する範囲を探す)
            if
                見つかった→見つかったことを今の状態(回数)と一緒にfeedback
        　      見つからなかった→見つからなかったことを今の状態(回数)と一緒にfeedback(一定の回数に達すると、manageから中止命令が来る)
            if
                中止命令が来た→emotions:tilt_neck を実行後、終了
        emotions:happy_club
        棒を掴む(test.py参照)
        Preparation_motion:hold
        完了報告をresult
    """
    # def search_target(self,<クライアントから送られるデータ名>):
    """
        search_targetをactionとして提供
        while service:search_targetを使って、印を探す(第一関節ｚ軸を一周する範囲を探す)
            if
                見つかった→見つかったことを今の状態(回数)と一緒にfeedback
        　      見つからなかった→見つからなかったことを今の状態(回数)と一緒にfeedback(一定の回数に達すると、manageから中止命令が来る)
            if
                中止命令が来た→emotions:tilt_neck を実行後、終了
        if
            嫌いなやつだった→emotions:dislike
        完了報告をresult(嫌いなやつだったかどうかでresultを変える)
    """
    # def check_target(self,<クライアントから送られるデータ名>):
    """
        check_targetをactionとして提供
        check_targetから印を探す
        印の状態をfeedback(中止命令が来る)
        if 中止命令が来た→emotions:tilt_neck を実行後、終了
        完了報告をresult
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
