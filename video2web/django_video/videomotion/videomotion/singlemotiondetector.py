import numpy as np
import imutils
import cv2


class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        self.accumWeight = accumWeight

        self.bg = None

    def update(self, image):
        # initialize the background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # update the background model by accumulating the weighted average
        # output = (1-alpha)*bg + alpha*image
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):
        # tVal: The threshold value used to mark a particular pixel as motion or not
        # compute the absolute difference between the background model
        # and the image passed in, then threshold the delta image
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        # cv2.threshold returns two values: threshold T and thresholded image
        # T is useful when using dynamic threshold like Otsu's method
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # perform a series of erosions and dilations to remove small blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # initialize the bounding box
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        if len(cnts) == 0:
            return None

        for c in cnts:
            # find the minimum rectangular of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x+w), max(maxY, y + h))

        return (thresh, (minX, minY, maxX, maxY))
