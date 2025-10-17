import cv2

cv2.namedWindow("TEST", cv2.WINDOW_NORMAL)

cv2.resizeWindow("TEST", 800, 600)

img = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow("TEST", img)
print(cv2.waitKey(0))


