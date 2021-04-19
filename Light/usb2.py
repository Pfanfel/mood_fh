import serial
import RPi.GPIO as GPIO
import time

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600
def blink(pin):

	GPIO.output(pin,GPIO.HIGH)  
	time.sleep(1)  
	GPIO.output(pin,GPIO.LOW)  
	time.sleep(1)  
	return

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
while True:

	#read_ser=ser.read()
	#temp = int(read_ser)
	#print(temp)
	print("Hallo")
	
	print("Senden")
		#blink(11)

	ser.write('5'.encode('ascii'))
	#read_ser=ser.readline()
	#temp = read_ser
	#print(temp)
