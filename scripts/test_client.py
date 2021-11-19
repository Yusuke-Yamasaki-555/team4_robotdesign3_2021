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

def main():
    rospy.init_node("test_client")
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)
    
    rospy.wait_for_service("bow") #  service_serverの開始を待つ
    rospy.wait_for_service("tilt_neck")
    
    bow = rospy.ServiceProxy('bow',SetBool) #  提供されているservice:bowをインスタンス化
    tilt_neck = rospy.ServiceProxy('tilt_neck', SetBool)
    # dislike
    happy_club = rospy.ServiceProxy('happy_club', SetBool)
    # happy_end

    bow_b = True
    bow_res = bow(bow_b) #  service:bowに入力。出力をresultに代入

    if bow_res.success:
        print(bow_res.message)
    elif not bow_res.sccess:
        print(bow_res.message)

    # テスト用コード
    arm.set_named_target("search_target")
    arm.go()
    # /テスト用コード

    tilt_neck_b = True
    tilt_neck_res = tilt_neck(tilt_neck_b)

    if tilt_neck_res.success:
        print(tilt_neck_res.message)
    elif not tilt_neck_res.sccess:
        print(tilt_neck_res.message)

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
    # /テスト用コード

    happy_club_b = True
    happy_club_res = happy_club(happy_club_b)

    if happy_club_res.success:
        print(happy_club_res.message)
    elif not happy_club_res.sccess:
        print(happy_club_res.message)


if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass