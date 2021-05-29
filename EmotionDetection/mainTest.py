#!/home/pi/Documents/mood_fh/EmotionDetection/emotionvenv/bin/python3
import code
from emotionClass import EmotionDetection
from evdev import InputDevice, categorize, ecodes
import evdev
import os

emotionDetection = EmotionDetection()
PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
PATH_TO_TEXTFILE = os.path.join(PATH_TO_SOURCE, "emotion.txt")

def animationOff():
    print("Animation Off")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Animation Off")
    f.close()

def animationOn():
    print("Animation On")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Animation On")
    f.close()

def soundOff():
    print("Sound Off")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Sound Off")
    f.close()

def soundOn():
    print("Sound On")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Sound On")
    f.close()

def togglePause():
    print("Toggle Pause")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Toggle Pause")
    f.close()

def nextSong():
    print("Next Song")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Next Song")
    f.close()

def volumeUp():
    print("Volume Up")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Volume Up")
    f.close()

def volumeDown():
    print("Volume Down")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Volume Down")
    f.close()

def detectEmotion():
    print("Emotionserkennung gestartet!")
    f = open(PATH_TO_TEXTFILE, "a")
    f.write("Emotionserkennung gestartet!")
    f.close()
    emotionDetection.play()

def kill():
    emotionDetection.kill()

switcher = {
        "KEY_NUMERIC_0" : animationOff,
        "KEY_DELETE" : animationOn,
        "KEY_ENTER" : soundOff,
        "KEY_CHANNEULUP" : soundOn,
        "KEY_CHANNELDOWN" : togglePause,
        "KEY_NUMERIC_3" : nextSong,
        "KEY_NUMERIC_4" : volumeUp,
        "KEY_NUMERIC_5" : volumeDown,
        "KEY_NUMERIC_6" : detectEmotion
    }

def main():
    # Select input device
    dev = InputDevice('/dev/input/event0')
    # Start event loop
    for event in dev.read_loop():
        # Key event
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            # Button down (not up) event
            if data.keystate == 1:
                func = switcher.get(str(data.keycode), "nothing")
                if func != "nothing":
                    func()
    # TODO: VLLT WECHSELT DEVICE NACH JEDEM BOOT
    #devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    #for device in devices:
    #    print(device.path, device.name, device.phys)

if __name__ == "__main__":
    try:
        main()
    finally:
        kill()
