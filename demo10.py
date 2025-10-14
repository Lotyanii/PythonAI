import cv2
import numpy as np


class Detect:
    def __init__(self):
        # 创建级联分类器，用于检测人脸
        self.classifier = cv2.CascadeClassifier()
        # 加载特征文件
        # path = cv2.data.haarcascades + "haarcascade_eye.xml"
        path = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
        self.classifier.load(path)
        pass

    def detectFace(self, faceImg):
        # 检测人脸，返回包含人脸矩形区域的列表
        face_rects = self.classifier.detectMultiScale(faceImg)

        for rect in face_rects:
            x, y, w, h = rect
            cv2.rectangle(faceImg, (x, y), (x + w, y + h), (255, 0, 0), 2)
            pass

        return face_rects


if __name__ == '__main__':
    faceImg = cv2.imread("face.jpg")
    cap = cv2.VideoCapture(0)

    logo = cv2.imread("logo.jpg")

    detect = Detect()
    while cap.isOpened():
        ret, frame = cap.read()
        face_rects = detect.detectFace(frame)

        if len(face_rects) == 0: continue

        x, y, w, h = face_rects[0]
        lh, lw, lc = logo.shape
        ratio = lh / lw
        slw = w
        slh = int(ratio * w)
        slogo = cv2.resize(logo, (slw, slh))

        slogo_gray = cv2.cvtColor(slogo, cv2.COLOR_BGR2GRAY)

        # 阈值处理
        retval, slogo_binary = cv2.threshold(slogo_gray, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 查找轮廓
        contours, hierarchy = cv2.findContours(slogo_binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        # 生成一个背景是黑色的图像
        mask = np.zeros_like(slogo_binary)

        # 绘制轮廓
        cv2.drawContours(mask, contours, 1, 255, -1)

        if y - slh <= 0 or x <= 0: continue
        faceImg = cv2.resize(frame, (slw, slh))

        # 实现只绘制二值图的白色部分对应的图像
        for i in range(slh):
            for j in range(slw):
                if mask[i, j] == 255:
                    frame[y - slh + i, x + j] = slogo[i, j]

        cv2.imshow("face", frame)
        keycode = cv2.waitKey(50)

        if keycode == ord('q') or keycode == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()
