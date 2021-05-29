import threading
import queue
import code
import yaml
import os
import evdev
from evdev import InputDevice, categorize, ecodes
from emotionClass import EmotionDetection
from soundClasses import AudioThread, MopidyPlayer, PygamePlayer
from light import LightThread

class MainTest:

    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")
    PATH_TO_TEXTFILE = os.path.join(PATH_TO_SOURCE, "emotion.txt")

    def __init__ (self):
        playertype = self._load_playertype()
        # Create AudioThread
        self.audioThread = self._create_audio_thread(playertype)
        # Create LightThread
        self.lightThread = LightThread()
        # Create EmotionDetection instance
        self.emotionDetection = EmotionDetection()
        # Select input device
        self.dev = InputDevice('/dev/input/event2')
        
        # TODO: VLLT WECHSELT DEVICE NACH JEDEM BOOT
        #devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        #for device in devices:
        #    print(device.path, device.name, device.phys)
        
        # Create switcher for ir-inputs
        self.switcher = {
                "KEY_NUMERIC_0" : self.animationOff,
                "KEY_DELETE" : self.animationOn,
                "KEY_ENTER" : self.soundOff,
                "KEY_CHANNEULUP" : self.soundOn,
                "KEY_CHANNELDOWN" : self.togglePause,
                "KEY_NUMERIC_3" : self.nextSong,
                "KEY_NUMERIC_4" : self.volumeUp,
                "KEY_NUMERIC_5" : self.volumeDown,
                "KEY_NUMERIC_6" : self.detectEmotion
            }

    def start_audio_thread(self):
        if self.audioThread is not None:
            self.audioThread.start()
        else:
            print('Could not create audio thread')

    def start_light_thread(self):
        if self.lightThread is not None:
            self.lightThread.start()
        else:
            print('Could not create light thread')

    def start_loop(self):
        # Start event loop
        for event in self.dev.read_loop():
            # Key event
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                # Button down (not up) event
                if data.keystate == 1:
                    print(str(data.keycode))
                    func = self.switcher.get(str(data.keycode), "nothing")
                    if func != "nothing":
                        func()
    
    def send_audio(self, emotion):
        self.audioThread.send_emotion(emotion)
        
    def send_light(self, emotion):
        self.lightThread.send_emotion(emotion)
        
    def kill_threads(self):
        self.audioThread.kill()
        self.lightThread.kill()
        self.audioThread.join()
        self.lightThread.join()

    def _load_playertype(self):
        with open(self.PATH_TO_CONFIG, "r") as t:
            config = yaml.safe_load(t)
            print(config)
        try:
            player = config['player_type']
        except KeyError:
            print('The Playerfield does not exist in config')
            #TODO: Weiter behandeln oder reicht das?
        print(f'The loaded playertype is: "{player}"')
        player = player.lower()
        return player

    def _create_audio_thread(self, playertype):
        if (playertype == 'pygame'):
            return AudioThread(PygamePlayer)
        elif (playertype == 'spotify'):
            return AudioThread(MopidyPlayer)
        else:
            print('Valid playertypes in config are: "pygame" and "mopidy"')
            return None

#---------------------------- Input Methodenaufrufe --------------------

    def animationOff(self):
        print("Animation Off")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Animation Off")
        f.close()
        self.send_light("false")
        
    def animationOn(self):
        print("Animation On")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Animation On")
        f.close()
        self.send_light("true")
        
        # TODO rausnehmen (auch aus der key.conf)
    def soundOff(self):
        print("Sound Off")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Sound Off")
        f.close()

    def soundOn(self):
        print("Sound On")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Sound On")
        f.close()

    def togglePause(self):
        print("Toggle Pause")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Toggle Pause")
        f.close()
        self.send_audio("toggle")
        self.send_light("toggle")

    def nextSong(self):
        print("Next Song")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Next Song")
        f.close()
        self.send_audio("next")

    def volumeUp(self):
        print("Volume Up")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Volume Up")
        f.close()
        self.send_audio("+")

    def volumeDown(self):
        print("Volume Down")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Volume Down")
        f.close()
        self.send_audio("-")

    def detectEmotion(self):
        print("Emotionserkennung gestartet!")
        f = open(self.PATH_TO_TEXTFILE, "a")
        f.write("Emotionserkennung gestartet!")
        f.close()
        emotion = self.emotionDetection.play()
        print(emotion)
        self.send_audio(emotion)
        self.send_light(emotion)


#-----------------------------------------------------------------------

if __name__ == "__main__":
    try:
        m = MainTest()
        m.start_audio_thread()
        m.start_light_thread()
        m.start_loop()
        print("mit python ausfuehren und in der interaktiven Shell mit m.send(\"<Emotion>\") die Emotion steuern")
        code.interact(local=globals()) #Startet die interactive shell zum testen.
    finally:
        m.kill_threads()
