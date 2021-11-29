#!/usr/bin/env python3

from logging import RootLogger
import rospy
from rospy.exceptions import ROSInterruptException
from team4_robotdesign3_2021.msg import ActSignalAction, ActSignalFeedback, ActSignalGoal
import actionlib

def fb_cb(feedback):
    print(feedback.BoolFB, feedback.Int32FB)

def main():
    client = actionlib.SimpleActionClient('action_server', ActSignalAction)
    client.wait_for_server()
    goal = ActSignalGoal()
    goal.Int32In = 5
    goal.StrIn = 'sent'
    goal.BoolIn = True
    client.send_goal(goal, feedback_cb=fb_cb)
    client.wait_for_result()
    result = client.get_result()
    value = result.Int32Res
    judge = result.BoolRes
    print(value, judge)

if __name__ == "__main__":
    rospy.init_node('action_client')
    try:
        main()
    
    except ROSInterruptException as e:
        rospy.logerr(e)