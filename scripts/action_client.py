#!/usr/bin/env python3
from math import trunc
import rospy
from rospy.exceptions import ROSInterruptException
from std_srvs.srv import SetBool #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message )
import actionlib
from team4_robotdesign3_2021.srv import SetInt32
from team4_robotdesign3_2021.msg import ActSignalAction, ActSignalGoal

def search_club_fb(feedback):
    print(feedback.Int32FB, feedback.BoolFB)
    if feedback.Int32FB%180 == 0:
        search_club_srv.cancel_goal()

def search_target_fb(feedback):
    print(feedback.Int32FB, feedback.BoolFB)
    if feedback.Int32FB%180 == 0:
        search_target_srv.cancel_goal()

def check_fb(feedback):
    print(feedback.Int32FB, feedback.BoolFB)

def swing_fb(feedback):
    print(feedback.Int32FB, feedback.BoolFB)

def search_club(start_deg):
    goal = ActSignalGoal()
    goal.Int32In = start_deg
    goal.BoolIn = True
    search_club_srv.send_goal(goal, feedback_cb=search_club_fb)
    search_club_srv.wait_for_result()
    result = search_club_srv.get_result()
    end_deg = result.Int32Res
    finish = result.BoolRes
    print(result.Int32Res, result.BoolRes)
    return end_deg, finish

def search_target(start_deg):
    goal = ActSignalGoal()
    goal.Int32In = start_deg
    goal.BoolIn = True
    search_target_srv.send_goal(goal, feedback_cb=search_target_fb)
    search_target_srv.wait_for_result()
    result = search_target_srv.get_result()
    end_deg = result.Int32Res
    finish = result.BoolRes
    print(result.StrRes)
    motion = result.StrRes
    print(end_deg, finish, motion)
    return end_deg, motion

def check_target(check_deg):
    goal = ActSignalGoal()
    goal.Int32In = check_deg
    goal.BoolIn = True
    check_target_srv.send_goal(goal, feedback_cb=check_fb)
    check_target_srv.wait_for_result()
    result = check_target_srv.get_result()
    end = True if result.Int32Res == 1 else False
    all_end = result.BoolRes
    print(end, all_end, result.StrRes)
    return end

def swing_club():
    goal = ActSignalGoal()
    goal.Int32In = 0
    goal.StrIn = 'swing club'
    goal.BoolIn = True
    swing_srv.send_goal(goal, feedback_cb=swing_fb)
    swing_srv.wait_for_result()
    result = swing_srv.get_result()
    value = result.Int32Res
    judge = result.BoolRes
    return True

def main():
    rospy.init_node('action_client')
    global search_club_srv, search_target_srv, check_target_srv, swing_srv
    wait_srvs = ['dislike', 'release_club', 'remove_target_id', 'remain_target', 'bow', 'happy_end']
    for srv in wait_srvs:
        rospy.wait_for_service(srv)
    print('finished emotions server')
    dislike = rospy.ServiceProxy('dislike', SetBool)
    release = rospy.ServiceProxy('release_club', SetBool)
    bow = rospy.ServiceProxy('bow', SetBool)
    happy_end = rospy.ServiceProxy('happy_end', SetBool)
    remove_target = rospy.ServiceProxy('remove_target_id', SetBool)
    remain_target = rospy.ServiceProxy('remain_target', SetBool)
    search_club_srv = actionlib.SimpleActionClient('search_club', ActSignalAction)
    search_target_srv = actionlib.SimpleActionClient('search_target', ActSignalAction)
    check_target_srv = actionlib.SimpleActionClient('check_target', ActSignalAction)
    swing_srv = actionlib.SimpleActionClient('swing_club', ActSignalAction)
    search_club_srv.wait_for_server()
    search_target_srv.wait_for_server()
    check_target_srv.wait_for_server()
    swing_srv.wait_for_server()
    print('finished waiting server')
    print('start')
    # motion = bow(True)
    # start_deg = 45
    # while True:
    #     end_deg, finish = search_club(start_deg)
    #     if finish:
    #         break
    #     start_deg = end_deg
    
    start_deg = -90
    end = False
    all_end = False
    while True:
        while True:
            end_deg, motion = search_target(start_deg=start_deg)
            start_deg = end_deg
            if motion == 'swing':
                print('swing')
                judge = swing_club()
                end, all_end = check_target(check_deg=start_deg)
                if end:
                    remove = remove_target(True)
                    break
            elif motion == 'dislike':
                emotion = dislike(True)
                remove = remove_target(True)
                print('dislike')
                break
            else:
                print('not')
                break
        remain = remain_target(True)
        if not remain.success:
            print('search target finished')
            break
    # motion = release(True)
    # emotion = happy_end(True)

if __name__ == "__main__":
    try:
        if not rospy.is_shutdown():
            main()
    
    except ROSInterruptException as e:
        rospy.logerr(e)
