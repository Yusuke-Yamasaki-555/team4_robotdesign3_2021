#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler
import <サービスのメッセージファイル>
import <アクションのメッセージファイル>
import actionlib
"""

# def main():
"""
    この中でいつもの定型文を書く。
    node名：motion_process
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
    rospy.sleep(1.0)

    class Motion_Process_Serverのインスタンスを作成
    各サービスのインスタンスを作成

    while not rospy.is_shutdown():
        rospy.spin()   
"""

# class Preparation_motion(object):

    # def __init__(self):
"""
        pass
"""

"""
    このクラスでは、init , stand_by , hold をそれぞれ関数として持ち、class Motion_Process_Serverに提供する
    Serverにはならない
    各関数の最後：return 動作結果
"""

# class Motion_Process_Server(object):
    # __init__(self):
"""
        class Preparation_motionのインスタンス作成
        各Action_Serverの立ち上げ＆start
"""
    # def release_club_motion(self,<クライアントから送られるデータ名>):
    # def swing_club_motion(self,<クライアントから送られるデータ名>):
    # def search_club_motion(self,<クライアントから送られるデータ名>):
    # def search_target_motion(self,<クライアントから送られるデータ名>):
    # def check_target_motion(self,<クライアントから送られるデータ名>):

# if __init__=="__main__":
"""
    いつものように try except を組んで、main()を実行
"""