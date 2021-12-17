#!/usr/bin/env python3
#画像の中心座標は(x, y) = 640, 480, 目標座標は(x, y) = 377, 227
import rospy
from sensor_msgs.msg import Image
import cv2
from cv2 import aruco
from cv_bridge import CvBridge, CvBridgeError

def cb(data):
    bridge = CvBridge()
    try:
        frame = bridge.imgmsg_to_cv2(data, "passthrough")
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # ARマーカー検知
            aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
            parameters =  aruco.DetectorParameters_create()
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            
            # 検知箇所を画像にマーキング
            frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            cv2.drawMarker(frame_markers, position=(377, 227), color=(0, 0, 255), markerType=cv2.MARKER_STAR, markerSize=10)

            cv2.imshow('window', frame_markers)
            cv2.waitKey(1)
            for i in range(len(ids)):
                # 検知したidの4点取得
                c = corners[i][0]
                print(f"id={ids[i]}")
                print(f"中心座標: {c[:, 0].mean(), c[:, 1].mean()}")
        except:
            cv2.imshow('window', frame)
            cv2.waitKey(1)
    except CvBridgeError as e:
        rospy.logerr(e)

def main():
    rospy.init_node("img_process", anonymous=1)
    rospy.loginfo('start')
    sub = rospy.Subscriber("/camera/color/image_raw", Image, cb)

    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    try:
        main()
    
    except:
        rospy.loginfo("faild")