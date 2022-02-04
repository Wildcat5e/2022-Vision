import cv2
from vision import CircleFinder

finder = CircleFinder()

for i in range(10):
    while True:
        circles = finder.find()
        if circles is None:
            continue
        out = finder.image.copy()
        for (x, y, r) in circles:
            cv2.circle(img=out, center=(x, y), radius=r, color=(0, 0, 255), thickness=4)
            cv2.rectangle(img=out, pt1=(x - 5, y - 5), pt2=(x + 5, y + 5), color=(255, 0, 0), thickness=-1)
        cv2.imshow(winname='Contours', mat=out)
        cv2.waitKey(delay=0)
        break

finder.capture.release()
