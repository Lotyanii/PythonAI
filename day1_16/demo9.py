import cv2 as cv
import numpy as np

cv.namedWindow("test")

cv.moveWindow("test", 50, 50)

cv.resizeWindow("test", 640, 480)

testimg = cv.imread("test.png")

h, w, c = testimg.shape

testimg[:, 0:10] = (255, 0, 0)
testimg[:, w - 10:w] = (0, 255, 0)
testimg[0:10, :] = (0, 0, 255)
testimg[h - 10:h, :] = (0, 255, 255)

test2 = cv.imread("test2.png")

h1, w1, c1 = test2.shape
testimg[10:h1 + 10, 10:w1 + 10] = test2
def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(event, x, y, flags, param)
        xc, yc = x, y
    if event == cv.EVENT_LBUTTONUP:
        print(event, x, y, flags, param)
        xc2, yc2 = x, y
        cv.line(param, (xc, yc), (xc2, yc2), (0, 0, 255), 2)
        cv.imshow("test", param)
    pass

# test = np.full((100, 100, 3), (255, 0, 0), np.uint8)


cv.setMouseCallback("test", onMouse, testimg)

cv.imshow("test", testimg)
cv.waitKey(0)


