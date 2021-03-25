# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

### Based on example from
### https://github.com/adafruit/Adafruit_CircuitPython_DotStar/tree/master/examples

import time
import random
import board
import adafruit_ws2801
import sys

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

class Emotion(Enum):
    NEUTRAL = 1
    HAPPY = 2
    SAD = 3
    ANGRY = 4
    DISGUSTED = 5
    FEARFUL = 6
    SURPRISED = 7
    

notFinish = True 
emotion = Emotion.NEUTRAL


def on_release(key):
    if key == keyboard.Key.esc:
        global notFinish 
        notFinish = False
        # Stop listener
        return False
    if key == keyboard.Key.space:
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
n_leds = len(leds)
while notFinish:
    if emotion == Emotion.NEUTRAL:
        leds.fill((138, 30, 0))
    elif emotion == Emotion.HAPPY:
        leds.fill((224, 80, 0))
    elif emotion == Emotion.SAD:
        leds.fill((80, 0, 224))
    elif emotion == Emotion.ANGRY:
        leds.fill((224, 0, 0))
    elif emotion == Emotion.DISGUSTED:
        leds.fill((180, 0, 50))
    elif emotion == Emotion.FEARFUL:
        leds.fill((0, 150, 20))
    elif emotion == Emotion.SURPRISED:
        leds.fill((50, 50, 120))
        #for idx in range(n_leds):
         #   leds[idx] = (224, 210, 188)
    leds.show()
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
