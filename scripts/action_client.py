#!/usr/bin/env python3
from math import trunc
import rospy
from rospy.exceptions import ROSInterruptException
from std_srvs.srv import SetBool #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message )
import actionlib
from team4_robotdesign3_2021.msg import ActSignalAction, ActSignalGoal

def search_fb(feedback):
    print(feedback.Int32FB, feedback.BoolFB)
    # if feedback.Int32FB%45 == 0:
    # search_club_srv.cancel_goal()

def search_club(start_deg):
    goal = ActSignalGoal()
    goal.Int32In = start_deg
    goal.BoolIn = True
    search_club_srv.send_goal(goal, feedback_cb=search_fb)
    search_club_srv.wait_for_result()
    result = search_club_srv.get_result()
    end_deg = result.Int32Res
    finish = result.BoolRes
    print(result.Int32Res, result.BoolRes)
    return end_deg, finish

# def search_target_fb(feedback):
#     print(feedback.Int32FB, feedback.BoolFB)

def search_target(start_deg):
    goal = ActSignalGoal()
    goal.Int32In = start_deg
    goal.BoolIn = True
    search_target_srv.send_goal(goal, feedback_cb=search_fb)
    search_target_srv.wait_for_result()
    result = search_target_srv.get_result()
    end_deg = result.Int32Res
    finish = result.BoolRes
    print(result.StrRes)
    swing = True if result.StrRes == 'swing' else False
    print(end_deg, finish, swing)
    return end_deg, finish, swing

def check_target(start_deg):
    goal = ActSignalGoal()
    goal.Int32In = start_deg
    goal.BoolIn = True
    search_target_srv.send_goal(goal, feedback_cb=search_fb)
    search_target_srv.wait_for_result()
    result = search_target_srv.get_result()
    end = result.Int32Res
    all_end = result.BoolRes
    print(end, all_end, result.StrRes)
    return end, all_end

def test():
    pass
    # client = actionlib.SimpleActionClient('action_server', ActSignalAction)
    # client.wait_for_server()
    # goal = ActSignalGoal()
    # goal.Int32In = 5
    # goal.StrIn = 'sent'
    # goal.BoolIn = True
    # client.send_goal(goal, feedback_cb=fb_cb)
    # client.wait_for_result()
    # result = client.get_result()
    # value = result.Int32Res
    # judge = result.BoolRes
    # print(value, judge)

def main():
    rospy.init_node('action_client')
    global search_club_srv, search_target_srv
    search_club_srv = actionlib.SimpleActionClient('search_club', ActSignalAction)
    search_target_srv = actionlib.SimpleActionClient('search_target', ActSignalAction)
    search_club_srv.wait_for_server()
    search_target_srv.wait_for_server()
    start_deg = 0
    # while True:
    #     end_deg, finish = search_club(start_deg)
    #     if finish:
    #         break
    #     start_deg = end_deg
    
    # start_deg = 0
    while True:
        end_deg, finish, swing = search_target(start_deg=start_deg)
        if swing:
            print('swing')
            #swing server
            #check target server
        else: 
            print('dislike')
        if finish:
            break
        start_deg = end_deg

if __name__ == "__main__":
    try:
        if not rospy.is_shutdown():
            main()
    
    except ROSInterruptException as e:
        rospy.logerr(e)
