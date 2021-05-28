#!/usr/bin/env python
from threading import Thread
import json
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2

from adafruit_servokit import ServoKit
from cobit_opencv_cam import CobitOpenCVCam
from cobit_car_motor_l9110 import CobitCarMotorL9110

def gen_frames():  # generate frame by frame from camera
   
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + cam.get_jpeg() + b'\r\n')  # concat frame one by one and show result

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)

angle = 0.0
throttle = 0.0

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/video_feed',methods = ['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.event
def my_event(message):
    global angle, throttle
    data = json.loads(message)
    angle = float(data['angle']) * 100 + 90
    throttle = float(data['throttle']) * 100 
    print(str(angle)+"  "+str(throttle))
    vc.motor_control(angle, throttle)
   

@socketio.event
def my_connect(message):
    print(message)

class vehicle_control:

    def __init__(self):
        self.motor = CobitCarMotorL9110()
        self.servo = ServoKit(channels=16)
        self.servo_offset = 20 
        self.servo.servo[0].angle = 90 + self.servo_offset

    def motor_control(self, angle, throttle):
        if throttle >= 0 and throttle <= 100:
            self.motor.motor_move_forward(int(throttle))
        if angle >= 30 and angle <= 150:
            self.servo.servo[0].angle = angle + self.servo_offset

    def servo_control(self, angle):
        if angle > 30 and angle < 150:
            self.servo.servo[0].angle = angle

    def throttle_control(self, throttle):
        self.motor.motor_move_forward(throttle)

if __name__ == '__main__':
    cam = CobitOpenCVCam()
    t = Thread(target=cam.run, args=())
    t.daemon = True
    t.start()
    vc = vehicle_control()

    socketio.run(app, host='192.168.254.30', port=5000)
