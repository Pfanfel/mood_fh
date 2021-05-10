import serial
import RPi.GPIO as GPIO
import time
import sys

from pynput import keyboard
from enum import Enum

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# Enum fuer verschiedene Emotionen 
class Emotion(Enum):
    NONE = 0
    NEUTRAL = 1
    HAPPY = 2
    SAD = 3
    ANGRY = 4
    DISGUSTED = 5
    FEARFUL = 6
    SURPRISED = 7
    
# Angabe, ob die LEDs ausgeschaltet werden sollen 
notFinish = True 
# aktuelle Emotion
emotion = Emotion.NEUTRAL
animationOn = False

# Callback fuer einen Tastendruck
def on_release(key):
    global emotion
    # Beleuchtung der LEDs wird beendet
    if key == keyboard.Key.esc:
        emotion = Emotion.NONE
        ser.write(('b\'' + str(emotion.value) + '\'').encode('ascii'))
        global notFinish 
        notFinish = False
        # Stop listener
        return False
    # beim Druck der Leertaste wird zur naechsten Emotion gewechselt
    if key == keyboard.Key.space:
        if emotion.value == 7:
            emotion = Emotion.NEUTRAL
        else:
            emotion = Emotion(emotion.value + 1)
        
        print(emotion)
        return True
        
    if key == keyboard.Key.shift:
        global animationOn
        if (animationOn):
            animationOn = False
        else:
            animationOn = True
        print(animationOn)

listener = keyboard.Listener(
    on_release=on_release)
listener.start()

while notFinish:

    if(ser.in_waiting >0):
        line = ser.readline()
        print(line) 
    ser.write(('b\'' + str(emotion.value) + '\'').encode('ascii'))
    
    if (animationOn):
        ser.write(('T').encode('ascii'))
    else:
        ser.write(('F').encode('ascii'))
    
sys.exit()
