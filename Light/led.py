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
    #leds.fill((138, 30, 0))
    rainbow_cycle_successive(leds, wait=0.01)
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
    #leds.fill((224, 80, 0))
    rainbow_cycle(leds, wait=0.0001)

"""
 Funktion, um das Licht fuer die traurige Emotion anzupassen
"""
def illuminateSad(leds):
    #leds.fill((80, 0, 224))
    brightness_decrease(leds)

"""
 Funktion, um das Licht fuer die wuetende Emotion anzupassen
"""
def illuminateAngry(leds):
   #leds.fill((224, 0, 0))
   #leds.show()
   appear_from_back(leds)

"""
 Funktion, um das Licht fuer die angewiderte Emotion anzupassen
"""
def illuminateDisgusted(leds):
    #leds.fill((180, 0, 50))
    for i in range(3):
        blink_color(leds, blink_times = 1, color=(255, 0, 0))
        blink_color(leds, blink_times = 1, color=(0, 255, 0))
        blink_color(leds, blink_times = 1, color=(0, 0, 255))
    
"""
 Funktion, um das Licht fuer die aengstliche Emotion anzupassen
"""
def illuminateFearful(leds):
    #leds.fill((0, 150, 20))
    rainbow_colors(leds)

"""
 Funktion, um das Licht fuer die ueberraschte Emotion anzupassen
"""
def illuminateSurprised(leds):
    #leds.fill((50, 50, 120))
    brightness_decrease(leds)

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
    
def clear():
    for i in range(n_leds):
        leds[i] = (0, 0, 0)

def allBlack():
    allBlack = True
    i = 0
    while allBlack and i < n_leds:
        if leds[i] != (0,0,0):
            allBlack = False
        i += 1
    return allBlack

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
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(leds, wait=0.01):
    #leds[0] = wheel(0)
    
    leds[0] = (138, 30, 0)
    i = 1
    while (not allBlack()) and notFinish:
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        if i < n_leds:
            #leds[i] = wheel(((i * 256 // n_leds)) % 256) 
            leds[i] = (138, 30, 0)
        if i >= 9:
            idx = min(n_leds - 1, i - 9)
            step = 5
            #offset = random.randrange(0, 10)
            offset = 0
            while idx >= 0:
                value = leds[idx]
                r = int(max(0, value[0] - step - offset))
                g = int(max(0, value[1] - step - offset))
                b = int(max(0, value[2] - step - offset))
                leds[idx] = ( r, g, b )
                idx -= 1
            #ledsBehind.append(leds[i - 9])
            #step = 1
            #for led in ledsBehind:
              #  value = led
               # r = int(max(0, value[0] - step))
               # g = int(max(0, value[1] - step))
               # b = int(max(0, value[2] - step))
              #  led = ( r, g, b )
        leds.show()
        if wait > 0:
            time.sleep(wait)
        i += 1
 
def rainbow_cycle(leds, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(n_leds):
            leds[i] = wheel(((i * 256 // n_leds) + j) % 256) 
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(leds, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(n_leds):
            leds[i] = wheel(((256 // n_leds + j)) % 256) 
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(leds, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(n_leds):
            value = leds[i]
            r = int(max(0, value[0] - step))
            g = int(max(0, value[1] - step))
            b = int(max(0, value[2] - step))
            leds[i] = ( r, g, b )
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(leds, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        clear()
        for j in range(2):
            for k in range(n_leds):
                leds[k] = color
            leds.show()
            time.sleep(0.08)
            clear()
            leds.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(leds, color=(255, 0, 0)):
    pos = 0
    for i in range(n_leds):
        for j in reversed(range(i, n_leds)):
            clear()
            # first set all pixels at the begin
            for k in range(i):
                leds[k] = color
            # set then the pixel at position j
            leds[j] = color
            leds.show()
            time.sleep(0.02)
            
 

######################### MAIN LOOP ##############################

while notFinish:
    # LEDs beleuchten 
    illuminateLights(emotion, leds)
    clear()
        #for idx in range(n_leds):
         #   leds[idx] = (224, 210, 188)
    #leds.show()
    # fill each led with a random color
    #for idx in range(n_leds):
    #    leds[idx] = (random_color(), random_color(), random_color())

    # show all leds in led string
    #leds.show()

    #time.sleep(0.25)
    

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
