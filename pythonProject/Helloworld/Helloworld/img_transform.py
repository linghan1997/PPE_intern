import cv2

src = cv2.imread("C:\\Users\\YXu35\\PycharmProjects\pythonProject\\Helloworld\\static\\upfile\\187346752efda5cf8b02415f78474023.jpeg", 1)
print(src.shape)
img = 255 - src
cv2.imshow("img", img)