#!/usr/bin/env python3
# -*- coding: utf-8 -*-]

import rospy
import moveit_commander
import rosnode

from std_srvs.srv import SetBool

def main():
    rospy.init_node("test_client")
    arm = moveit_commander.MoveGroupCommander("arm")
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if "rviz" in s]) == 0:
        rospy.sleep(1.0)
    
    rospy.wait_for_service("bow")

    
    bow = rospy.ServiceProxy("bow",SetBool)
    bow(True)

    if bow.success:
        print("finish")

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass