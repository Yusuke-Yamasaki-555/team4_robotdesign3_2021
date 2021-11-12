#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs
import rosnode
from tf.transformations import quaternion_from_euler

from std_srvs.srv import SetBool, SetBoolResponse 

def main():
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

    bow = rospy.Service("bow", SetBool, Emotions_Server.bow_motion)

    print("Node:emotions Ready")
    rospy.spin()

class Preparation_motion(object):
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    """
    このクラスでは、init , stand_by , emotions_stand_by をそれぞれ関数として持ち、class Emotions_Serverに提供する
    Service_Serverにはならない
    各関数の最後：return 動作結果
    """
    def init(self):
        print("init_pose")
        self.arm.set_named_target("init")
        self.arm.go()

class Emotions_Server(object): 
    preparation = Preparation_motion

    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    def bow_motion(self,data):
        """
        この関数では、bow をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
        動作を行う(test.py参照)
        動作の完了報告を返す
        """
        resp = SetBoolResponse()
        if data.data:
            try:
                print("bow")
                self.arm.set_named_target("bow")
                self.arm.go()
                self.preparation.init()
                resp.message = "Success"
                resp.success = True
            except:
                resp.message = "Failure"
                resp.success = False
        print("finish bow")
        return resp
            
    # def tilt_neck_motion(self,<クライアントから送られるデータ名>):
"""
        この関数では、tile_neck をする動作をServiceとして提供する
        動作の速度＆加速度の比率を定義
       動作を行う(test.py参照)
        動作の完了報告を返す
"""

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