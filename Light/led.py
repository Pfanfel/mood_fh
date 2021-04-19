import time
import random
import board
import adafruit_ws2801
import sys
#import colorsys
#import math 

from pynput import keyboard
from enum import Enum

odata = board.MOSI
oclock = board.SCLK
numleds = 96
bright = 1.0
leds = adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
)


# Enum fuer verschiedene Emotionen 
class Emotion(Enum):
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
# Anzahl der LEDs
n_leds = len(leds)


# Sorgt dafuer, dass die entspr. LEDs beleuchtet werden, abhaengig von
# der uebergebenen Emotion
def illuminateLights():
    # jeder Emotion wird eine Funktion fuer die Beleuchtung zugeordnet
    switcher = {
        Emotion.NEUTRAL: illuminateNeutral,
        Emotion.HAPPY: illuminateHappy,
        Emotion.SAD: illuminateSad,
        Emotion.ANGRY: illuminateAngry,
        Emotion.DISGUSTED: illuminateDisgusted,
        Emotion.FEARFUL: illuminateFearful,
        Emotion.SURPRISED: illuminateSurprised
    }
    # entspr. Funktion je nach Emotion aufrufen
    switcher[emotion]()

# Funktion, um das Licht fuer die neutrale Emotion anzupassen
def illuminateNeutral():
    #leds.fill((138, 30, 0))
    tailCircleAnimation(wait=0.01)


# Funktion, um das Licht fuer die glueckliche Emotion anzupassen
def illuminateHappy():
    #leds.fill((224, 80, 0))
    rainbowCycle()
    leds.show()
    
# Funktion, um das Licht fuer die traurige Emotion anzupassen
def illuminateSad():
    leds.fill((80, 0, 224))
    leds.show()

# Funktion, um das Licht fuer die wuetende Emotion anzupassen
def illuminateAngry():
    leds.fill((224, 0, 0))
    leds.show()

# Funktion, um das Licht fuer die angewiderte Emotion anzupassen
def illuminateDisgusted():
    leds.fill((180, 0, 50))
    leds.show()

# Funktion, um das Licht fuer die aengstliche Emotion anzupassen
def illuminateFearful():
    leds.fill((0, 150, 20))
    leds.show()

# Funktion, um das Licht fuer die ueberraschte Emotion anzupassen
def illuminateSurprised():
    leds.fill((50, 50, 120))
    leds.show()

# Callback fuer einen Tastendruck
def on_release(key):
    # Beleuchtung der LEDs wird beendet
    if key == keyboard.Key.esc:
        global notFinish 
        notFinish = False
        # Stop listener
        return False
    # beim Druck der Leertaste wird zur naechsten Emotion gewechselt
    if key == keyboard.Key.space:
        global emotionChanged
        emotionChanged = True
        
        global emotion
        if emotion.value == 7:
            emotion = Emotion.NEUTRAL
        else:
            emotion = Emotion(emotion.value + 1)
        
        print(emotion)
        return True



listener = keyboard.Listener(
    on_release=on_release)
listener.start()

#######################################################

# Funktion, um alle LEDs auszuschalten
def clear():
    for i in range(n_leds):
        leds[i] = (0, 0, 0)

# Ueberprueft, ob alle LEDs ausgeschaltet sind
def allBlack():
    allBlack = True
    i = 0
    while allBlack and i < n_leds:
        if leds[i] != (0,0,0):
            allBlack = False
        i += 1
    return allBlack

 
#Funktion zur Animation eines "Schweifes"
def tailCircleAnimation(wait=0.01):
    lightingLeds = 9
    leds[0] = (138, 30, 0)
    i = 1
    while (not allBlack()) and notFinish:
        if i < n_leds:
            leds[i] = (138, 30, 0)
            
        if i >= lightingLeds:
            idx = min(n_leds - 1, i - lightingLeds)
            step = 5
            while idx >= 0:
                value = leds[idx]
                r = int(max(0, value[0] - step))
                g = int(max(0, value[1] - step))
                b = int(max(0, value[2] - step))
                leds[idx] = ( r, g, b )
                idx -= 1
        
        leds.show()
        if wait > 0:
            time.sleep(wait)
        i += 1

 # Define the wheel function to interpolate between different hues.
def wheel(pos):
    value = (0,0,0)
    if pos < 85:
        value = (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        value = (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        value = (0, pos * 3, 255 - pos * 3)
    return value

def rainbowCycle(wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(n_leds):
            leds[i] = wheel(((i * 256 // n_leds) + j) % 256) 
        leds.show()
        if wait > 0:
            time.sleep(wait)

######################### MAIN LOOP ##############################

while notFinish:
    # LEDs beleuchten 
    illuminateLights()
    clear()
    

leds.deinit()
sys.exit()
