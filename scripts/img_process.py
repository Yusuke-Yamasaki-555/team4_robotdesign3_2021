#! /usr/bin/env python3
# -*- coding: utf-8 -*-
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

#倒す物体に取り付けられているARマーカーのidを宣言
target_AR_id = [1, 2, 3, 4, 10]

#棒のARマーカーを宣言
club_AR_id = 6

#画像を受け取る。Img_processに継承
class Accept_img:
    def __init__(self):
        # self.origin = origin
        # 初期化
    
    def rtn_img(self):
        #画像を受信、OpenCV形式に変換
        #return 変換後の画像
        # bridge = CvBridge()
        # try:
        #     self.origin = bridge.imgmsg_to_cv2(self.data, "passthrough")
        
        # except CvBridgeError as e:
        #     self.origin = False
        
        # return self.origin

#メインの画像処理
class Img_process(Accept_img):
    def __init__(self):
        #初期化
    def search(self):
        #ARマーカーがあるかどうか調べる
        # return True(ある場合) or false(ない場合)
    def adjust(self):
        #動作料を計算
        #retun 動作量

#ARマーカーの情報を返す関数
def rtn_ar_info(img):
    print("hello")

"""仮のコード
    #ARマーカーがあるかどうか判定し、結果をmotion_processに返す
def search(data):
    print("hello")
    #画像を取得、opencv形式に変換し、返す
    def accept_img(data):
        print("hello")

#根本の回転角度を計算して、それをmotion_processに返す
def adjust(data):
    print("hello")
    #画像を取得、opencv形式に変換し、返す
    def accept_img(data):
        print("hello")

"""
def main():
    #sub-pub or server-clientを宣言
    #オブジェクト生成


if __name__ == "__main__":
    if __name__ == '__main__':
        try:
            if not rospy.is_shutdown():
                main()
        except rospy.ROSInterruptException:
            pass
