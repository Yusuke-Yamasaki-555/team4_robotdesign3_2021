#!/usr/bin/env python3
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
from re import search
from sys import exec_prefix
import cv_bridge
import rospy
from rospy.core import logerr
from sensor_msgs.msg import Image
import numpy as np
import cv2
from cv2 import aruco, waitKey
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32, Bool, String
from math import asin

AR_id = [1, 2, 3, 4, 10]

def rtn_ar_info(img):
    bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)
    
    # ARマーカー検知
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    try:
        id = ids[0]
    
    except:
        id = False
    return corners, id
    
def search(data):
    if data.data == "search":
        def accept_img(data):
            bridge = CvBridge()
            try:
                origin = bridge.imgmsg_to_cv2(data, "passthrough")
            
            except CvBridgeError as e:
                logerr(e)
            _, id = rtn_ar_info(img=origin)
            cv2.imshow("window2", origin)
            waitKey(1)
            if not id or id not in AR_id:
                pub.publish(False)
            
            else:
                AR_id.remove(id)
                rospy.loginfo(id)
                pub.publish(True)
        sub = rospy.Subscriber("/camera/color/image_raw", Image, accept_img)
    
def adjust(data):
    if data.data == "adjust":
        def accept_img(data):
            bridge = CvBridge()
            try:
                origin = bridge.imgmsg_to_cv2(data, "passthrough")
            
            except CvBridgeError as e:
                logerr(e)
            corners, id = rtn_ar_info()
            # 検知箇所を画像にマーキング
            markers = aruco.drawDetectedMarkers(origin.copy(), corners, id)
            current_x, current_y = 0, 0
            cv2.imshow("window2", markers)
            waitKey(1)

            # 検知したidの4点取得
            c = corners[0][0]
            current_x = c[:, 0].mean()
            current_y = c[:, 1].mean()
            print(f"id={id}")
            print(f"中心座標: {current_x, current_y}")
            goal_x, goal_y = 337, 227
            move_x = goal_x - current_y
            k = 0.12 / 210.5
            conv_x = k * move_x
            radius = 0.5-0.172
            move_x = asin(conv_x / radius)
            # move_y = goal_y - current_y
            pub2.publish(move_x)
        sub = rospy.Subscriber("/camera/color/image_raw", Image, accept_img)
    
    
def main():
    rospy.init_node("search", anonymous=1)
    rospy.loginfo('start')
    sub1 = rospy.Subscriber("search", String, search)
    sub2 = rospy.Subscriber("adjust", String, adjust)
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher("search_report", Bool, queue_size=1)
    pub2 = rospy.Publisher("adjust_report", Float32, queue_size=1)
    try:
        main()
    
    except:
        rospy.loginfo("faild")
