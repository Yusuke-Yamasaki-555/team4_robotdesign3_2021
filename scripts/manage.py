#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
import rospy
import moveit_commander
import rosnode

import <サービスのメッセージファイル>
import <アクションのメッセージファイル>
import actionlib
"""

# def main():
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

    while 指定の色リストが全て処理されるまでループ
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

# if __name__=="__main__":
"""
    いつものように try except を組んで、main()を実行
"""