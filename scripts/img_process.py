#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
import rospy
from sensor_msgs.msg import Image
import cv2
from cv2 import aruco
from cv_bridge import CvBridge, CvBridgeError
from std_srvs.srv import SetBool, SetBoolResponse
from team4_robotdesign3_2021.srv import SetInt32, SetInt32Response

class Image_process:
    def __init__(self, target_AR_id):
        self.target_AR_id = target_AR_id
        self.origin = ''
        self.eps = 10
        print(self.target_AR_id)
        self.rtn_img_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.rtn_img)

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
        resp = SetBoolResponse()
        id, _= self.get_ar_info()
        if not id or id not in self.target_AR_id:
            resp.message = ''
            resp.success = False
        else:
            self.target_AR_id.remove(id)
            rospy.loginfo(id)
            resp.message = str(id)
            resp.success = True
        return resp
        # return True(ある場合) or false(ない場合)
    def adjust_x(self, data):
        rospy.loginfo(data.int32In)
        resp = SetInt32Response()
        _, c = self.get_ar_info()
        current_x = c[:, 0].mean()
        goal_x = data.int32In
        move = goal_x - current_x
        resp.int32Out = 0 if abs(move) < self.eps else int(abs(move)/move)
        return resp


    def adjust_y(self, data):
        _, c = self.get_ar_info()
        rospy.loginfo(data.int32In)
        resp = SetInt32Response()
        current_y = c[:, 1].mean()
        goal_y = data.int32In
        move = goal_y - current_y
        resp.int32Out = 0 if abs(move) < self.eps else int(abs(move)/move)
        return resp

def main():
    rospy.init_node('img_process', anonymous=1)
    rospy.loginfo('start')
    target = Image_process(target_AR_id = [3, 4, 10])
    club = Image_process(target_AR_id=[6])
    search_club_server = rospy.Service('search_club', SetBool, club.search)
    adjustx_club_server = rospy.Service('adjustx_club', SetInt32, club.adjust_x)
    adjusty_club_server = rospy.Service('adjusty_club', SetInt32, club.adjust_y)
    search_target_server = rospy.Service('search_target', SetBool, target.search)
    adjustx_target_server = rospy.Service('adjustx_target', SetInt32, target.adjust_x)
    adjusty_target_server = rospy.Service('adjusty_target', SetInt32, target.adjust_y)
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logerr(e)
