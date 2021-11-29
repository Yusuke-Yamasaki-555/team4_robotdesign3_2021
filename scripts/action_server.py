#!/usr/bin/env python3

import rospy
from rospy.exceptions import ROSInterruptException
from team4_robotdesign3_2021.msg import ActSignalResult, ActSignalFeedback, ActSignalAction
import rosnode
import actionlib

def cb(goal):
    if goal.BoolIn == True:
        print(goal.Int32In)
        print(goal.StrIn)
        result = ActSignalResult()
        feedback = ActSignalFeedback()
        sum = 0
        for i in range(0, 100, 1):
            feedback.BoolFB = True
            sum += i
            feedback.Int32FB = i
            if feedback.Int32FB % 10 == 0:
                server.publish_feedback(feedback)
                rospy.sleep(0.001)
        result.Int32Res = sum
        result.BoolRes = True
        server.set_succeeded(result=result)

if __name__ == "__main__":
    try:
        rospy.init_node("action_server")
        server = actionlib.SimpleActionServer('action_server', ActSignalAction, cb, False)    #'timer'という名で，TimerActionというアクションの型　do_timerを実行．サーバの自動起動を無効にするためFalseを指定
        server.start()  #サーバ生成後，明示的にサーバを開始する
        rospy.spin()
    except ROSInterruptException as e:
        print("e")
        rospy.logerr(e)