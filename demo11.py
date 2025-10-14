# 1. 前景和背景的分离
# 二值图
# 2. 通过二值图查找轮廓
# 3. 根据轮廓,获取外接的最大的矩形区域
# 4. 根据区域上的,某一点p0(x0,y0)
# 5. 绘制一条线的区域范围:
# 如果p0点穿过线的范围,就统计一辆车

import cv2
import numpy as np

cap = cv2.VideoCapture("car.mp4")

# 没有bgsegm用createBackgroundSubtractorMOG2替代createBackgroundSubtractorMOG
bgSegMog = cv2.createBackgroundSubtractorMOG2()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(5, 5))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("no frame")
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame_binary = cv2.threshold(frame_gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # 前后背景分离
    mask = bgSegMog.apply(frame_gray)

    erode_mask = cv2.erode(mask, kernel)
    dilate_mask = cv2.dilate(erode_mask, kernel)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(dilate_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 获取轮廓的外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        if w < 90 or h < 90:
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("mask", dilate_mask)
    cv2.imshow("frame", frame)

    cv2.waitKey(30)
