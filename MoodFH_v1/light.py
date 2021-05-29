import serial
import time
import sys

from pynput import keyboard
from enum import Enum

# ACM-Nummer fuer Arduino mit ls /dev/tty/ACM* ermitteln
ser=serial.Serial("/dev/ttyACM0",9600)  

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
    
# Angabe, ob die LEDs an-/ausgeschaltet sein sollen 
finish = False 

# aktuelle Emotion
emotion = Emotion.NEUTRAL

# Angabe, ob Animation an-/ausgeschaltet sein soll
animationOn = False

# Callback fuer einen Tastendruck
def on_release(key):
	# Markierung, dass globale Variable veraendert werden soll
    global emotion
    
    # Beleuchtung der LEDs wird beendet
    if key == keyboard.Key.alt:
        emotion = Emotion.NONE
        return True
        
    # Beim Druck der Leertaste wird zur naechsten Emotion gewechselt
    if key == keyboard.Key.space:
		# Wenn letzte Emotion an war, vorne wieder anfangen
        if emotion.value == 7:
            emotion = Emotion.NEUTRAL
        else:
            emotion = Emotion(emotion.value + 1)
        
        print(emotion)
        return True
        
    # Angabe, dass das Programm beendet wird
    if key == keyboard.Key.esc:
        global finish
        finish = True
        
        # Stop listener
        return False
        
    # Beim Druck der Shifttaste wird zur Animation/Farbe gewechselt
    if key == keyboard.Key.shift:
        global animationOn
        # Setzen, ob Animation an oder aus ist
        if (animationOn):
            animationOn = False
        else:
            animationOn = True
            
        print(animationOn)
        return True

# Listener fuer Tastatur erstellen und aktivieren
listener = keyboard.Listener(
    on_release=on_release)
listener.start()

# Programm laeuft, solange es nicht beendet wird
while not(finish):

    # TODO
    if(ser.in_waiting >0):
        line = ser.readline()
        print(line) 
        
    # Aktuelle Emotion an den Arduino uebermitteln
    ser.write(('b\'' + str(emotion.value) + '\'').encode('ascii'))
    
    # Aktuelle Angabe ueber Animation an den Arduino uebermitteln
    if (animationOn):
        ser.write(('T').encode('ascii'))
    else:
        ser.write(('F').encode('ascii'))
    
sys.exit()
