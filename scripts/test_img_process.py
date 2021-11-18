#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
import rospy
from sensor_msgs.msg import Image
import cv2
from cv2 import aruco
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32, Bool, String, Int32
from math import fabs

class Image_process:
    def __init__(self, target_AR_id):
        self.target_AR_id = target_AR_id
        self.origin = ''
        self.eps = 10
        print(self.target_AR_id)
    
    def set_pub(self, topic_name):
        self.search_pub = rospy.Publisher(topic_name[0], Bool, queue_size=1)
        self.adjustX_pub = rospy.Publisher(topic_name[1], Int32, queue_size=1)
        self.adjustY_pub = rospy.Publisher(topic_name[2], Int32, queue_size=1)
    
    def set_sub(self, topic_name):
        self.rtn_img_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.rtn_img)
        self.search_sub = rospy.Subscriber(topic_name[0], String, self.search)
        self.adjustY_sub = rospy.Subscriber(topic_name[1], Int32, self.adjust_x)
        self.adjustY_sub = rospy.Subscriber(topic_name[2], Int32, self.adjust_y)

    
    def rtn_img(self, data):
        bridge = CvBridge()
        try:
            self.origin = bridge.imgmsg_to_cv2(data, 'passthrough')
            self.bgr = cv2.cvtColor(self.origin, cv2.COLOR_BGR2RGB)
            self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_RGB2GRAY)
            cv2.drawMarker(self.origin, position=(377, 227), color=(0, 0, 255), markerType=cv2.MARKER_STAR, markerSize=10)
            # height = int(self.origin.shape[0])
            # width = int(self.origin.shape[1])
            # resize_img = cv2.resize(self.bgr,(4*width/5, 4*height/5))
            cv2.imshow('window', self.origin)
            cv2.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr(e)
        
    def get_ar_info(self):
        # ARマーカー検知
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        try:
            corners, ids, _ = aruco.detectMarkers(self.gray, aruco_dict, parameters=parameters)
            id = ids[0] if ids else False
            c = corners[0][0] if corners else False
        except:
            pass
        return id, c
 
    def search(self, data):
        #ARマーカーがあるかどうか調べる
        rospy.loginfo(data.data)
        id, _= self.get_ar_info()
        if not id or id not in self.target_AR_id:
            self.search_pub.publish(False)
        else:
            self.target_AR_id.remove(id)
            rospy.loginfo(id)
            self.search_pub.publish(True)

        # return True(ある場合) or false(ない場合)
    def adjust_x(self, data):
        rospy.loginfo(data.data)
        _, c = self.get_ar_info()
        current_x = c[:, 0].mean()
        goal_x = data.data
        move = goal_x - current_x
        fabs_move = fabs(move)
        if fabs_move < self.eps:
            rtn = False
        elif move > 0:
            rtn = 1
        elif move < 0:
            rtn = -1
        self.adjustX_pub.publish(rtn)

    def adjust_y(self, data):
        _, c = self.get_ar_info()
        rospy.loginfo(data.data)
        current_y = c[:, 1].mean()
        goal_y = data.data
        move = goal_y - current_y
        if fabs(move) < self.eps:
            rtn = False
        elif move > 0:
            rtn = 1
        elif move < 0:
            rtn = -1
        self.adjustY_pub.publish(rtn)

def main():
    rospy.init_node('img_process', anonymous=1)
    rospy.loginfo('start')
    target = Image_process(target_AR_id = [3, 4, 10])
    club = Image_process(target_AR_id=[6])
    target.set_pub(target_pub_topic_name)
    club.set_pub(club_pub_topic_name)
    target.set_sub(target_sub_topic_name)
    club.set_sub(club_sub_topic_name)
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    target_pub_topic_name = ['search_target_report', 'adjustX_target_report', 'adjustY_target_report']
    club_pub_topic_name = ['search_club_report', 'adjustX_club_report', 'adjustY_club_report']
    target_sub_topic_name = ['search_target', 'adjustX_target', 'adjustY_target']
    club_sub_topic_name = ['search_club', 'adjustX_club', 'adjustY_club']
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)
