# this is a modified combination of code from 
# https://stackoverflow.com/questions/2957116/make-2-functions-run-at-the-same-time
# https://www.instructables.com/Raspberry-Pi-LED-Blink/
# https://wiki.python.org/moin/UdpCommunication
# https://raspberrypi.stackexchange.com/questions/53778/how-to-detect-state-of-gpio-pin-in-python

from threading import Thread
import sys
import time     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
import serial

# Set up serial connection with arduino -----------------------------------
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("Serial connected to Arduino")

# Tx & Rx IP addresses and ports ------------------------------------------
UDP_TX_IP = "127.0.0.1"
UDP_TX_PORT = 3000
UDP_RX_IP = "127.0.0.1"
UDP_RX_PORT = 3001

print("UDP target IP: %s" % UDP_TX_IP)
print("UDP target port: %s" % UDP_TX_PORT)

sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sockRX.bind((UDP_RX_IP, UDP_RX_PORT))

# set up GPIO pins -------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(26,GPIO.OUT) 
GPIO.output(26,GPIO.LOW)
GPIO.setup(20,GPIO.OUT) 
GPIO.output(20,GPIO.LOW)
GPIO.setup(21,GPIO.OUT) 
GPIO.output(21,GPIO.HIGH)
GPIO.setup(16,GPIO.OUT) 
GPIO.output(16,GPIO.HIGH)



def newclient(): # read GPIO pins and report it to the server
     if GPIO.input(26):
          sockTX.sendto(bytes('{"GPIO26T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
     if GPIO.input(20):
          sockTX.sendto(bytes('{"GPIO20T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
     if GPIO.input(21):
          sockTX.sendto(bytes('{"GPIO21T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
     if GPIO.input(16):
          sockTX.sendto(bytes('{"GPIO16T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
    
def one(): # not really needed right now, original example
     while True: # Run forever
          MESSAGE = '{"D22":1}'
          #print("transmit message: ", MESSAGE)
          sockTX.sendto(bytes('{"A1":80}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          time.sleep(10)                  # Sleep for 1 second
          #MESSAGE = '{"D22":0}'
          #print("transmit message: ", MESSAGE)
          #sockTX.sendto(bytes(MESSAGE, "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          sockTX.sendto(bytes('{"A1":20}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          time.sleep(10)                  # Sleep for 1 second
               
def two(): # Listen for arrow key commands from the server and send to Arduino over serial
     while True:
          time.sleep(0.001)
          data, addr = sockRX.recvfrom(1024) # buffer size is 1024 bytes
          JsonStr = data.decode('utf_8')
          print(JsonStr)
          if (JsonStr.find('{"NewClient":1}') != -1):
               newclient()
          elif (JsonStr.find('{"ArrowUp":1}') != -1):
               ser.write("U\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowDown":1}') != -1):
               ser.write("D\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowLeft":1}') != -1):
               ser.write("L\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowRight":1}') != -1):
               ser.write("R\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowLifted":0}') != -1):
               ser.write("S\n".encode('utf-8'))
          # added to test:
          elif (JsonStr.find('{"ArrowUp":0}') != -1):
               ser.write("S\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowDown":0}') != -1):
               ser.write("S\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowLeft":0}') != -1):
               ser.write("S\n".encode('utf-8'))
          elif (JsonStr.find('{"ArrowRight":0}') != -1):
               ser.write("S\n".encode('utf-8'))

# threading to run the loops in parallel
newclient()
p1 = Thread(target = one)
p2 = Thread(target = two)

p1.start()
p2.start()


#If you leave leave following the code out, Ctrl-C to terminate the program may not work.
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Closed serial comm with arduino")
    ser.close()
         

