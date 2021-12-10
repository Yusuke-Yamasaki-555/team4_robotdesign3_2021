#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
import rospy
from sensor_msgs.msg import Image
import cv2
from cv2 import aruco
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from std_srvs.srv import SetBool, SetBoolResponse
from team4_robotdesign3_2021.srv import SetInt32, SetInt32Response

class Image_process:
    def __init__(self, target_AR_id):
        self.target_AR_id = target_AR_id
        self.eps = 5
        self.pre_c = []
        print(self.target_AR_id)
        self.rtn_img_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.rtn_img)

    def rtn_img(self, data):
        bridge = CvBridge()
        try:
            origin = bridge.imgmsg_to_cv2(data, 'passthrough')
            self.bgr = cv2.cvtColor(origin, cv2.COLOR_BGR2RGB)
            self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_RGB2GRAY)
            cv2.drawMarker(origin, position=(377, 227), color=(0, 0, 255), markerType=cv2.MARKER_STAR, markerSize=10)
            cv2.imshow('window', origin)
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
            c = corners[0][0] if corners else self.pre_c
            self.pre_c = c
        except:
            pass
        return id, c

    def search(self, data):
        resp = SetBoolResponse()
        #ARマーカーがあるかどうか調べる
        id, _= self.get_ar_info()
        if not id or id not in self.target_AR_id:
            resp.message = ''
            resp.success = False
        else:
            rospy.loginfo(id)
            # self.target_AR_id.remove(id)
            str_id  = str(id)
            str_id = str_id.strip('[]')
            print(f'idididid = {str_id}')
            resp.message = f'end, {str_id}' if len(self.target_AR_id) == 1 else f'not, {str_id}'
            print(f'len={resp.message}')
            resp.success = True 
        return resp
    
    def remove_id(self, data):
        resp = SetInt32Response()
        self.target_AR_id.remove(data.int32In)
        print(f'remain id = {self.target_AR_id}')
        resp.int32Out = data.int32In
        return resp

        # return True(ある場合) or false(ない場合)
    def adjust_x(self, data):
        resp = SetInt32Response()
        # rospy.loginfo(data.int32In)
        _, c = self.get_ar_info()
        current_x = int(c[:, 0].mean())
        goal_x = data.int32In
        move = goal_x - current_x
        resp.int32Out = 0 if abs(move) < self.eps else int(abs(move)/move)
        return resp

    def adjust_y(self, data):
        resp = SetInt32Response()
        _, c = self.get_ar_info()
        # rospy.loginfo(data.int32In)
        current_y = int(c[:, 1].mean())
        goal_y = data.int32In
        move = goal_y - current_y
        resp.int32Out = 0 if abs(move) < self.eps else int(abs(move)/move)
        return resp

def main():
    rospy.init_node('img_process', anonymous=1)
    rospy.loginfo('start')
    adjust = Image_process(target_AR_id=[3, 4, 6, 10])
    target = Image_process(target_AR_id=[4, 10])
    club = Image_process(target_AR_id=[6])
    check = Image_process(target_AR_id=[3, 4, 10])
    img_search_club_server = rospy.Service('img_search_club', SetBool, club.search)
    img_search_target_server = rospy.Service('img_search_target', SetBool, target.search)
    img_remove_club_id = rospy.Service('remove_club', SetInt32, club.remove_id)
    img_remove_target_id = rospy.Service('remove_target', SetInt32, target.remove_id)
    img_adjustx_server = rospy.Service('img_adjustx', SetInt32, adjust.adjust_x)
    img_adjusty_server = rospy.Service('img_adjusty', SetInt32, adjust.adjust_y)
    # img_check_target_server = rospy.Service('img_check_target', SetBool, check.search)

    print('finished setting')
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)