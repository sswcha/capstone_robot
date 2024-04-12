import cv2
import time
from flask import Flask, render_template, Response, stream_with_context, request
from picamera2 import Picamera2

# initialize flask server
app = Flask('__name__')

# set up pi camera -----------------------------------------------------
# Video Resolution
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Configure and start raspi camera v2
pi_cam = Picamera2()
pi_cam.preview_configuration.main.size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
pi_cam.preview_configuration.main.format = "RGB888"
pi_cam.preview_configuration.controls.FrameRate = 30
pi_cam.preview_configuration.align()
pi_cam.configure("preview")
pi_cam.start()

fps = 0
# FPS text configuration
FPS_POSITION = (30,60)
FPS_FONT = cv2.FONT_HERSHEY_SIMPLEX
FPS_HEIGHT = 1.5
FPS_COLOR = (0,0,255)
FPS_WEIGHT = 3
# ----------------------------------------------------------------------

def video_stream():
    while True:
        frame = pi_cam.capture_array()
        cv2.putText(frame, str(int(fps))+' FPS', FPS_POSITION, FPS_FONT, FPS_HEIGHT, FPS_COLOR, FPS_WEIGHT)
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')
        
@app.route('/camera')
def camera():
    return render_template('camera.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
app.run(host='192.168.8.243', port='5000', debug=False)

