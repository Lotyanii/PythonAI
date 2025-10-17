import cv2

cap = cv2.VideoCapture("D:/test.mp4")

cv2.namedWindow("test")

cv2.resizeWindow("test", 640, 480)

while True:
    ret, frame = cap.read()
    cv2.imshow("test", frame)
    cv2.waitKey(1)
    if ord('q') == cv2.waitKey(0):
        break

cap.release()
cv2.destroyAllWindows()


