#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import rosnode


from std_srvs.srv import SetBool #  SetBoolは標準搭載のservice( 入力:bool data , 出力:bool success / string message )

def main():
    rospy.init_node("test_client")
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)
    
    rospy.wait_for_service("bow") #  service_serverの開始を待つ

    
    bow = rospy.ServiceProxy('bow',SetBool) #  提供されているservice:bowをインスタンス化

    bool = True
    result = bow(bool) #  service:bowに入力。出力をresultに代入

    if result.success:
        print(result.message)

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass