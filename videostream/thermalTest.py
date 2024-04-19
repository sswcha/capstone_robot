# thermalTest.py

import time
import board
import busio
import adafruit_mlx90640
import cv2
import numpy as np
from flask import Flask, render_template, Response, stream_with_context, request

WIDTH = 32
HEIGHT = 24
PRINT_TEMPS = True;
PRINT_ASCII = False;

# cv2 text
# FPS text configuration
TXT_POSITION = (30,60)
TXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TXT_HEIGHT = 1.5
TXT_COLOR = (255,120,0)
TXT_WEIGHT = 3
txt = "test"

# FUNCTION DEFINITIONS //////////////////////////////////////////////////////////
def temp_to_rbg(temp, min_temp, max_temp):
	# rbg range, hot <--> cold
	min_rgb = np.array([0, 0, 255])
	max_rgb = np.array([255, 0, 0])
	
	normalized_temp = (temp - min_temp) / (max_temp-min_temp)
	
	rgb = (1 - normalized_temp) * min_rgb + normalized_temp * max_rgb
	
	return rgb.astype(int)
	
def generate_rgb_array(temp, min_temp, max_temp):
	
	rgb_array = np.zeros((HEIGHT, WIDTH, 3), dtype=int)
	
	incr = 0
	for i in range(HEIGHT):
		for j in range(WIDTH):
			rgb_array[i, j] = temp_to_rbg(temp[incr], min_temp, max_temp)
			incr = incr + 1
	return rgb_array
# //////////////////////////////////////////////////////////////////////////////


i2c = busio.I2C(board.SCL, board.SDA)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr found")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

#frame = [0] * 768 # 32 x 24 pixels
frame = np.zeros(768)
#print(frame)
while True:
	stamp = time.monotonic()
	try:
		mlx.getFrame(frame)
		frame = frame.astype(int)
		frame = 9/5*frame+32
		#print(frame)
	except ValueError:
		continue
	#print("Read 8 frames in %0.2f s" % (time.monotonic() - stamp))
	max_temp = np.max(frame)
	min_temp = np.min(frame)
	rgb_frame = generate_rgb_array(frame, min_temp, max_temp)
	resize = 20
	rgb_frame = cv2.resize(rgb_frame.astype(np.uint8), (WIDTH*resize, HEIGHT*resize))
	txt = max_temp
	cv2.putText(rgb_frame, "max: "+str(int(txt)), TXT_POSITION, TXT_FONT, TXT_HEIGHT, TXT_COLOR, TXT_WEIGHT)
	cv2.imshow("Thermal", cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
	if cv2.waitKey(1) == ord('q'):
		break
cv2.destroyAllWindows()
	


	
	
