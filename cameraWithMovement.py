import cv2
import numpy
import time as time
import RPi.GPIO as GPIO

from flask import Flask, render_template, Response, stream_with_context, request

video = cv2.VideoCapture(0)

app = Flask('__name__')

def video_stream():
    print('stream worked')
    while True:
        ret, frame = video.read()
        if not ret:
            break 
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/camera')
def camera():
   return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace;  boundary=frame')


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DC_motor_1_1 = 4 
DC_motor_1_2 = 17
DC_motor_2_1 = 27
DC_motor_2_2 = 22
   

GPIO.setup(DC_motor_1_1, GPIO.OUT)
GPIO.setup(DC_motor_1_2, GPIO.OUT)
GPIO.setup(DC_motor_2_1, GPIO.OUT)
GPIO.setup(DC_motor_2_2, GPIO.OUT)





@app.route('/forward')
def forward():
    print('********forward was pressed*******')
    GPIO.output(DC_motor_1_1, GPIO.HIGH)
    GPIO.output(DC_motor_1_2, GPIO.LOW)
    GPIO.output(DC_motor_2_1,GPIO.HIGH)
    GPIO.output(DC_motor_2_2,GPIO.LOW)
    time.sleep(0.1)
    return "the car was moved forward"

@app.route('/backward')
def backward():
    print('********backward was pressed*******')
    GPIO.output(DC_motor_1_1, GPIO.LOW)
    GPIO.output(DC_motor_1_2, GPIO.HIGH)
    GPIO.output(DC_motor_2_1, GPIO.LOW)
    GPIO.output(DC_motor_2_2, GPIO.HIGH)
    time.sleep(0.1)
    return "the car was moved backward"

@app.route('/right')
def right():
    print('********right was pressed*******')
    GPIO.output(DC_motor_1_1, GPIO.LOW)
    GPIO.output(DC_motor_1_2, GPIO.LOW)
    GPIO.output(DC_motor_2_1, GPIO.HIGH)
    GPIO.output(DC_motor_2_2, GPIO.LOW)
    time.sleep(0.1)
    return "the car was moved right"

@app.route('/left')
def left():
    print('********left was pressed*******')
    GPIO.output(DC_motor_1_1, GPIO.HIGH)
    GPIO.output(DC_motor_1_2, GPIO.LOW)
    GPIO.output(DC_motor_2_1, GPIO.LOW)
    GPIO.output(DC_motor_2_2, GPIO.LOW)
    time.sleep(0.1)
    return "the car was moved left"


@app.route('/stop')
def stop():
    print('********stop was pressed*******')
    GPIO.output(DC_motor_1_1, GPIO.LOW)
    GPIO.output(DC_motor_1_2, GPIO.LOW)
    GPIO.output(DC_motor_2_1, GPIO.LOW)
    GPIO.output(DC_motor_2_2, GPIO.LOW)
    time.sleep(0.1)
    return "the car was stopped"





app.run(host='0.0.0.0', port='5000', debug=False)
