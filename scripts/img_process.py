#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
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

class Img_process:
    #target_AR_id: 検出するARマーカーのid
    def __init__(self, target_AR_id):
        #初期化
    
    def rtn_img(self):
        #画像を受信、OpenCV形式に変換
        # bridge = CvBridge()
        # try:
        #     self.origin = bridge.imgmsg_to_cv2(self.data, "passthrough")
        
        # except CvBridgeError as e:
        #     self.origin = False
    #ARマーカーの情報を返す関数
    def rtn_ar_info(self):
        
    def search(self):
        #ARマーカーがあるかどうか調べる
        # return True(ある場合) or false(ない場合)
    def adjust(self):
        #動作料を計算
        #retun 動作量


def main():
    #sub-pub or server-clientを宣言
    #オブジェクト生成


if __name__ == "__main__":
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
