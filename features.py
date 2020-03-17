import cv2
import numpy as np
import imutils

class ImageFeatures:
    def __init__(self, bins):
        self.bins = bins
    def getFeatures(self, image):        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []        
        (h, w) = image.shape[:2]
        (cw, ch) = (int(w * 0.5), int(h * 0.5))
        segments = [(0, cw, 0, ch), (cw, w, 0, ch), (cw, w, ch, h),
            (0, cw, ch, h)]

        for (startW, endW, startH, endH) in segments:            
            segmentMask = np.zeros(image.shape[:2], dtype = "uint8")
            cv2.rectangle(segmentMask, (startW, startH), (endW, endH), 255, -1)          
            hist = self.histogram(image, segmentMask)
            features.extend(hist)
        return features
    
    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
            [0, 180, 0, 256, 0, 256])
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        else:
            hist = cv2.normalize(hist, hist).flatten()
        return hist