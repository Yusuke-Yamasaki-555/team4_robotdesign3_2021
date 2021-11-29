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

#===== action =====
# """
swing_club = actionlib.SimpleActionClient('swing_club', ActSignalAction)
# """
#===== /action =====

def main():
    rospy.init_node("test_client")
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)
    
#===== emotions =====
    """
    rospy.wait_for_service("bow") #  service_serverの開始を待つ
    rospy.wait_for_service("tilt_neck")
    rospy.wait_for_service("dislike")
    rospy.wait_for_service("happy_club")
    rospy.wait_for_service("happy_end")
    
    bow = rospy.ServiceProxy('bow',SetBool) #  提供されているservice:bowをインスタンス化
    tilt_neck = rospy.ServiceProxy('tilt_neck', SetBool)
    dislike = rospy.ServiceProxy('dislike', SetBool)
    happy_club = rospy.ServiceProxy('happy_club', SetBool)
    happy_end = rospy.ServiceProxy('happy_end', SetBool)
    """
#===== /emotions =====
#===== action =====
    # """
    swing_club.wait_for_server()
    # """
#===== /action =====

#===== motion_process =====
    # """
    rospy.wait_for_service("release_club")

    release_club = rospy.ServiceProxy('release_club', SetBool)
    # """
#===== /motion_process =====

#===== bow =====
    """
    bow_b = True
    bow_res = bow(bow_b) #  service:bowに入力。出力をresultに代入

    if bow_res.success:
        print(bow_res.message)
    elif not bow_res.success:
        print(bow_res.message)
    # """
#===== tilt_neck =====
    """
    # テスト用コード
    arm.set_named_target("search_target")
    arm.go()
    # /テスト用コード

    tilt_neck_b = True
    tilt_neck_res = tilt_neck(tilt_neck_b)

    if tilt_neck_res.success:
        print(tilt_neck_res.message)
    elif not tilt_neck_res.success:
        print(tilt_neck_res.message)
    # """
#===== dislike =====
    """
    # テスト用コード
    arm.set_named_target("search_target")
    arm.go()
    # /テスト用コード

    dislike_b = True
    dislike_res = dislike(dislike_b)

    if dislike_res.success:
        print(dislike_res.message)
    elif not dislike_res.success:
        print(dislike_res.message)
    # """
#===== happy_club =====
    """
    # テスト用コード
    search_club = geometry_msgs.msg.Pose() #  棒を探す姿勢の定義
    search_club.position.x = 0
    search_club.position.y = 0.26
    search_club.position.z = 0.3
    qu1 = quaternion_from_euler(0, 3.14, 3.14)
    search_club.orientation.x = qu1[0]
    search_club.orientation.y = qu1[1]
    search_club.orientation.z = qu1[2]
    search_club.orientation.w = qu1[3]
    print("search_club")
    arm.set_pose_target(search_club)
    print(search_club)
    arm.go()

    rospy.sleep(1.0)
    # /テスト用コード

    happy_club_b = True
    happy_club_res = happy_club(happy_club_b)

    if happy_club_res.success:
        print(happy_club_res.message)
    elif not happy_club_res.success:
        print(happy_club_res.message)
    # """
#===== happy_end =====
    """
    # テスト用コード
    arm.set_named_target("init")
    arm.go()
    # /テスト用コード

    happy_end_b = True
    happy_end_res = happy_end(happy_end_b) #  service:bowに入力。出力をresultに代入

    if happy_end_res.success:
        print(happy_end_res.message)
    elif not happy_end_res.success:
        print(happy_end_res.message)
    # """
#===== release_club =====
    """
    release_club_b = True
    release_club_res = release_club(release_club_b)

    if release_club_res.success:
        print(release_club_res.message)
    elif not release_club_res.success:
        print(release_club_res.message)
    # """
#===== swing_club =====
    # """
    # テスト用コード
    arm.set_named_target("init")
    arm.go()
    # /テスト用コード
    goal = ActSignalGoal()
    goal.BoolIn = True
    goal.StrIn = "server:Start swing_club"

    swing_club.send_goal(goal, feedback_cb = feedback_swing_club)
    swing_club.wait_for_result()

    if swing_club.get_result.BoolRes:
        print("client:Success swing_club")
    elif not swing_club.get_result.BoolRes:
        print("client:Failure swing_club")
    # """


def feedback_swing_club(feedback):
    if feedback.BoolFB:
        print("==client:Confirmed swing_set_club")
    else:
        swing_club.cancel_goal()


if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass