#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import rosnode

# テストの為
from tf.transformations import quaternion_from_euler
import geometry_msgs
# /テストの為

from std_srvs.srv import SetBool #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message )
import actionlib
from team4_robotdesign3_2021.msg import ActSignalAction, ActSignalResult, ActSignalFeedback, ActSignalGoal

#===== global =====
# """
search_club = None
search_target = None
swing_club = None
check_target = None
# """
#===== /global =====

def main():
    """
    この中でいつもの定型文を書く。
    node名：manage
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")
    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)

    ここで、すべてのserverの開始を待つ


    ここで、動作の順にaction & serviceを呼び出して処理をする

    bow
    search_club
        if feedbackされてきた状態(回数)が一定を超えた
            中止命令

    while 指定の色リストが全て処理されるまでループ(色はARマーカーと対応させる)
        while check_clubの結果が良になるまでループ
            search_target
                if feedbackされてきた状態(回数)が一定を超えた
                    中止命令
            swing_club
            check_club
                if feedbackされてきた状態から、印が残っていると判断された

    release_club
    happy_end
    bow
    """
    global search_club, search_target, swing_club, check_target 

    rospy.init_node("manage")
    # arm = moveit_commander.MoveGroupCommander("arm")
    # gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.loginfo("Waiting rviz...")
        rospy.sleep(1.0)
    rospy.loginfo("Started rviz")
#===== emotions =====
    """
    bow = rospy.ServiceProxy('bow', SetBool)
    release_club = rospy.ServiceProxy('release_club', SetBool)
    happy_end = rospy.ServiceProxy('happy_end', SetBool)
    """
#===== /emotions =====
#===== action =====
    """
    search_club = actionlib.SimpleActionClient('search_club', ActSignalAction)
    search_target = actionlib.SimpleActionClient('search_target', ActSignalAction)
    swing_club = actionlib.SimpleActionClient('swing_club', ActSignalAction)
    check_target = actionlib.SimpleActionClient('check_target', ActSignalAction)
    # """
#===== /action =====
#===== waiting_server =====
    """ manageで使うserver
    
    search_club.wait_for_server()
    search_target.wait_for_server()
    swing_club.wait_for_server()
    check_target.wait_for_server()

    rospy.wait_for_service("bow")
    rospy.wait_for_service("release_club")
    rospy.wait_for_service("happy_end")
    # """
    """ manage以外で使うserver
    　　(server待ちで一連動作を止めたくない。manageで全serverの開始を待つ)
    　　(各呼び出し元nodeでも一応待っても良いかも)

    # node:emotions
    rospy.wait_for_service("tilt_neck")
    rospy.wait_for_service("dislike")
    rospy.wait_for_service("happy_club")

    # node:img_process(adjust系の意義はどうなのか？)
    rospy.wait_for_service("img_search_club")
    rospy.wait_for_service("img_adjustx_club")
    rospy.wait_for_service("img_adjusty_club")
    rospy.wait_for_service("img_search_target")
    rospy.wait_for_service("img_adjustx_target")
    rospy.wait_for_service("img_adjusty_target")
    # rospy.wait_for_service("<check_target系>")
    # """
#===== waiting_server =====
#===== main_process =====
    """ ここで、動作の順にaction & serviceを呼び出して処理をする
    bow
    search_club
        if feedbackされてきた状態(回数)が一定を超えた
            中止命令

    # このループはちょっと雑だから、後々手直し必要
    while 指定のARマーカーリストが全て処理されるまでループ
        while check_targetの結果が良になるまでループ
            search_target
                if feedbackされてきた状態(回数)が一定を超えた
                    中止命令
            swing_club
            check_club
                if feedbackされてきた状態から、印が残っていると判断された

    release_club
    happy_end
    bow
    # """
#===== /main_process =====


#===== feedback群 ===== ココはclassにしても良いかも
"""
def feedback_search_club(feedback):

def feedback_search_target(feedback):

def feedback_swing_club(feedback):
    if feedback.BoolFB:
        print("==client:Confirmed swing_set_club")
    else:
        swing_club.cancel_goal()

def feedback_check_target(feedback):

# """
#===== /feedback群 =====


if __name__ == '__main__': # ここも、ちょっちイジっても良い鴨。test_motion_process(だったか)に習って
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass