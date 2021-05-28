import RPi.GPIO as IO
import time

'''
Cobit car motor setup 

motor 1  Right motor 
    PWM pin = 19 (GPIO no 35)       IA1 
    Direction pin = 13 (GPIO no 33) IB1

motor 2 Left motor 
    PWM pin = 12 (GPIO no 32)       IA2
    Dirction pin = 16 (GPIO no 36)  IB2

'''

class CobitCarMotorL9110():

    def __init__(self):
        self.motor1_r_pwmPin = 19
        self.motor1_r_dirPin = 13
        self.motor2_l_pwmPin = 12
        self.motor2_l_dirPin = 16
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(self.motor1_r_pwmPin, IO.OUT)
        IO.setup(self.motor1_r_dirPin, IO.OUT)
        IO.setup(self.motor2_l_pwmPin, IO.OUT)
        IO.setup(self.motor2_l_dirPin, IO.OUT)
        self.motor1_pwm = IO.PWM(self.motor1_r_pwmPin, 100)
        self.motor1_pwm.start(0)
        self.motor2_pwm = IO.PWM(self.motor2_l_pwmPin, 100)
        self.motor2_pwm.start(0)


    def motor_move_forward(self, speed):
        if speed > 100:
            speed = 100
        #self.motor1_pwm.stop()
        #self.motor2_pwm.stop()
        #self.motor1_pwm = IO.PWM(self.motor1_r_pwmPin, 100)
        #self.motor2_pwm = IO.PWM(self.motor2_l_pwmPin, 100)
        #self.motor1_pwm.start(0)
        #self.motor2_pwm.start(0)
        self.motor1_pwm.ChangeDutyCycle(int(speed))
        self.motor2_pwm.ChangeDutyCycle(int(speed))
        
    def motor_stop(self):
        self.motor1_pwm.ChangeDutyCycle(0)
        self.motor1_pwm.stop()
        IO.output(self.motor1_r_dirPin, False) 
        IO.output(self.motor1_r_pwmPin, False)
        self.motor2_pwm.ChangeDutyCycle(0)
        self.motor2_pwm.stop()
        IO.output(self.motor2_l_dirPin, False) 
        IO.output(self.motor2_l_pwmPin, False)
        
    def motor_move_backward(self, speed):
        if speed > 100:
            speed = 100
        self.motor1_pwm.stop()
        self.motor1_pwm = IO.PWM(self.motor1_r_dirPin, 100)
        self.motor1_pwm.start(0)
        self.motor1_pwm.ChangeDutyCycle(speed)
        self.motor2_pwm.stop()
        self.motor2_pwm = IO.PWM(self.motor2_l_dirPin, 100)
        self.motor2_pwm.start(0)
        self.motor2_pwm.ChangeDutyCycle(speed)
        

if __name__ == '__main__':

    cobit_motor = CobitCarMotorL9110()
    while True:
        cobit_motor.motor_move_forward(30)
        time.sleep(2)
        cobit_motor.motor_stop()
        time.sleep(2)
        
        cobit_motor.motor_move_backward(30)
        time.sleep(2)
        cobit_motor.motor_stop()
        time.sleep(2)





