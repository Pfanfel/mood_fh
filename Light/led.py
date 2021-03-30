# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

### Based on example from
### https://github.com/adafruit/Adafruit_CircuitPython_DotStar/tree/master/examples

import time
import random
import board
import adafruit_ws2801
import sys
#import colorsys
#import math 

from pynput import keyboard
from enum import Enum

### Example for a Feather M4 driving 25 12mm leds
odata = board.MOSI
oclock = board.SCLK
numleds = 96
bright = 1.0
leds = adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
)

"""
 Enum fuer verschiedene Emotionen 
"""
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

"""
 Sorgt dafuer, dass die entspr. LEDs beleuchtet werden, abhaengig von
 der uebergebenen Emotion
"""
def illuminateLights(emotion, leds):
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
    switcher[emotion](leds)

"""
 Funktion, um das Licht fuer die neutrale Emotion anzupassen
"""
def illuminateNeutral(leds):
    leds.fill((138, 30, 0))
     """
    for idx in range(n_leds):
        if idx % 2 == 0:
            leds[idx] = (138, 30, 0)
        else:
            leds[idx] = (int(0.05 * 138) , int(0.05 * 30), 0)
 
    #for idx in range(n_leds):
    #leds[idx] = (random_color(), random_color(), random_color())
   
    deg = 0.0
    value = 0.0
    for idx in range(n_leds):
        leds[idx] = (0,0,0)
        deg = float((sys.maxint/n_leds)*idx)/(float(sys.maxint)) * 360.0
        value = pow(math.sin(math.radians(deg)), 8)
        
        if value >= 0.0:
            hsv = colorsys.rgb_to_hsv(leds[idx][0], leds[idx][1], leds[idx][2])
             
            leds[idx] += 
    """

"""
 Funktion, um das Licht fuer die glueckliche Emotion anzupassen
"""
def illuminateHappy(leds):
    leds.fill((224, 80, 0))

"""
 Funktion, um das Licht fuer die traurige Emotion anzupassen
"""
def illuminateSad(leds):
    leds.fill((80, 0, 224))

"""
 Funktion, um das Licht fuer die wuetende Emotion anzupassen
"""
def illuminateAngry(leds):
    leds.fill((224, 0, 0))

"""
 Funktion, um das Licht fuer die angewiderte Emotion anzupassen
"""
def illuminateDisgusted(leds):
    leds.fill((180, 0, 50))
    
"""
 Funktion, um das Licht fuer die aengstliche Emotion anzupassen
"""
def illuminateFearful(leds):
    leds.fill((0, 150, 20))

"""
 Funktion, um das Licht fuer die ueberraschte Emotion anzupassen
"""
def illuminateSurprised(leds):
    leds.fill((50, 50, 120))

"""
 Callback fuer einen Tastendruck
"""
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


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_release=on_release)
listener.start()

######################### HELPERS ##############################

# a random color 0 -> 224
def random_color():
    return random.randrange(0, 7) * 32


######################### MAIN LOOP ##############################

while notFinish:
    # LEDs beleuchten 
    illuminateLights(emotion, leds)
        #for idx in range(n_leds):
         #   leds[idx] = (224, 210, 188)
    leds.show()
    # fill each led with a random color
    #for idx in range(n_leds):
    #    leds[idx] = (random_color(), random_color(), random_color())

    # show all leds in led string
    #leds.show()

    time.sleep(0.25)
    

leds.deinit()
sys.exit()

#sudo /etc/init.d/ntp stop
#sudo timedatectl set-time "2021-03-24 12:10:00"
#sudo /etc/init.d/ntp start
#sudo reboot

#Farben
#Orange/Rot -> 224, 30, 2
#Orange/Gelb -> 138 30 0 (neutral?)
#Warmgelb -> 224, 80, 0 (happy)
