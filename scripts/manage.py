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
    global search_club, search_target, swing_club, check_target, arm, gripper

    rospy.init_node("manage")
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.loginfo("Waiting rviz...")
        rospy.sleep(1.0)
    rospy.loginfo("Started rviz")

#===== emotions =====
    # """
    bow = rospy.ServiceProxy('bow', SetBool)
    release_club = rospy.ServiceProxy('release_club', SetBool)
    dislike = rospy.ServiceProxy('dislike', SetBool)
    happy_end = rospy.ServiceProxy('happy_end', SetBool)
    remove_target = rospy.ServiceProxy('remove_target_id', SetBool)
    remain_target = rospy.ServiceProxy('remain_target', SetBool)
    # """
#===== /emotions =====

#===== action =====
    # """
    search_club = actionlib.SimpleActionClient('search_club', ActSignalAction)
    search_target = actionlib.SimpleActionClient('search_target', ActSignalAction)
    swing_club = actionlib.SimpleActionClient('swing_club', ActSignalAction)
    check_target = actionlib.SimpleActionClient('check_target', ActSignalAction)
    
    # """
#===== /action =====

#===== waiting_server =====
    rospy.loginfo("Wait all server...")
    # """ manageで使うserver
    search_club.wait_for_server()
    search_target.wait_for_server()
    swing_club.wait_for_server()
    check_target.wait_for_server()

    # """
    wait_srvs = ['dislike', 'release_club', 'remove_target_id', 'remain_target', 'bow', 'happy_end']
    position = [-30, 30]
    for srv in wait_srvs:
        rospy.wait_for_service(srv)
    rospy.loginfo("Start all server")
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
    # お辞儀
    # # """
    # bow_b = True
    # print("go bow")
    # bow_res = bow(bow_b)
    # check_service(bow_res)
    # # """

    # # 棒を探す(search_club)
    # # """
    # start_deg = 45
    # goal = set_goal(True, start_deg, "server:Start search_club")
    # search_club.send_goal(goal, feedback_cb=feedback_search_club)
    # search_club.wait_for_result()
    # result = search_club.get_result()
    # if result.BoolRes:
    #     print("client:Success swing_club")
    # elif not result.BoolRes:
    #     print("client:Failure swing_club")
    # """
    all_end = False
    # num = 0
    # start_deg = position[0]
    while True:
        while True:
        # 印を探す
            # """
            goal = set_goal(True, start_deg, "server:Start search_target")
            search_target.send_goal(goal, feedback_cb=feedback_search_target)
            search_target.wait_for_result()
            result = search_target.get_result()
            preempt = result.BoolRes
            if preempt:
                all_end = True
                break
            start_deg = result.Int32Res
            motion = result.StrRes
            print(motion)
            if result.BoolRes:
                print("client:Success search_target")
            elif not result.BoolRes:
                print("client:Failure search_target")
            # 印のIDから動作判断
            if motion == 'swing':
                goal = set_goal(True, 0, 'swing_club')
                swing_club.send_goal(goal, feedback_cb=feedback_swing_club)
                swing_club.wait_for_result()
                result = swing_club.get_result()
                if result.BoolRes:
                    print("client:Success swing_club")
                elif not result.BoolRes:
                    print("client:Failure swing_club")
                # 印を確認する
                goal = set_goal(result.BoolRes, start_deg, "server:Start check_target")
                check_target.send_goal(goal, feedback_cb=feedback_check_target)
                check_target.wait_for_result()
                result = check_target.get_result()
                if result.BoolRes:
                    # num += 1
                    # start_deg = position[num]
                    remove = remove_target(True)
                    break
                

            elif motion == 'dislike':
                emotion = dislike(True)
                # start_deg = position[num]
                remove = remove_target(True)
                # num += 1
                break

            else:
                print('not')
                break
        remain = remain_target(True)
        if not remain.success or all_end:
            print('search target finish')
            break
        
    # 棒を離す
    # """
    release_club_b = True
    print("go release_club")
    release_club_res = release_club(release_club_b)
    check_service(release_club_res)
    # # """

    # # 最後の喜び表現
    # # """
    happy_end_b = True
    print("go happy_end")
    happy_end_res = happy_end(happy_end_b)
    check_service(happy_end_res)
    # # """

    # # お辞儀
    # # """
    bow_b = True
    print("go bow")
    bow_res = bow(bow_b)
    check_service(bow_res)
    # """

    print("all finish")
#===== /main_process =====

#===== check_service =====
def check_service(srv_res):
    if srv_res.success:
        print(srv_res.message)
    elif not srv_res.success:
        print(srv_res.message)
#===== /check_service =====

#===== set_goal =====
def set_goal(bool, int, str):
    goal = ActSignalGoal()
    goal.BoolIn = bool
    goal.Int32In = int
    goal.StrIn = str
    return goal
#===== /set_goal =====

#===== feedback群 =====
# """
def feedback_search_club(feedback):
    if feedback.BoolFB:
        print("==client:Confirmed search_club")
    else:
        if feedback.Int32FB == 180:
            search_club.cancel_goal()

def feedback_search_target(feedback):
    if feedback.BoolFB:
        print("==client:Confirmed serach_target")
        if feedback.Int32FB == 0: # sample(嫌なやつを見つけた時)
            search_target.cancel_goal()
    else:
        if feedback.Int32FB == 180:
            search_target.cancel_goal()

def feedback_swing_club(feedback):
    if feedback.BoolFB:
        print("==client:Confirmed swing_set_club")
    else:
        swing_club.cancel_goal()

def feedback_check_target(feedback):
    if not feedback.BoolFB:
        print("==client:Confirmed check_target")
    else:
        check_target.cancel_goal()
# """
#===== /feedback群 =====


if __name__ == '__main__': # ここも、ちょっちイジっても良い鴨。test_motion_process(だったか)に習って
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)