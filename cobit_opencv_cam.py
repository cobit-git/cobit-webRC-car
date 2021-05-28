import cv2
import time
import numpy as np

class CobitOpenCVCam:
    # OpenCV and camera init
    def __init__(self):
        
        self.frame = None
        self.ret = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        self.jpeg = None
        
    def get_jpeg(self):
        return self.jpeg.tobytes()

    # send jpeg image
    def run(self):
        while True:
            ret, self.frame = self.cap.read()
            ret, self.jpeg = cv2.imencode('.jpg', self.frame)
        
           
    def set_lane_detect(self, value):
        self.lane_detect = value

    def get_lane_detect(self):
        return self.lane_detect

    def set_recording_status(self, value):
        print(value)
        self.recording = value

    def get_recording_status(self):
        return self.recording


if __name__ == '__main__':
    cam = CobitOpenCVCam()
    cam.update() 

