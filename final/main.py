#!/home/pi/Documents/mood_fh/MoodFH_v1/moodvenv/bin/python3
import threading
import queue
import code
import yaml
import os
import evdev
from evdev import InputDevice, categorize, ecodes
from emotion import EmotionDetection
from soundClasses import AudioThread, MopidyPlayer, PygamePlayer
from light import LightThread

class Main:
    '''
    Einstiegspunkt des Programms, welcher bei Boot des PIs ausgefuehrt werden soll.
    Kuemmert sich um das starten der Sound- und Light-Threads, sowie die Signalverarbeitung der IR-Fernbedienung.
    '''

    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")

    def __init__ (self):
        playertype = self._load_playertype()
        # Create AudioThread
        self.audioThread = self._create_audio_thread(playertype)
        # Create LightThread
        self.lightThread = LightThread()
        # Create EmotionDetection instance
        self.emotionDetection = EmotionDetection()
        # Select input device
        self.dev = InputDevice('/dev/input/event6')
        
        # TODO: VLLT WECHSELT DEVICE NACH JEDEM BOOT
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            print(device.path, device.name, device.phys)
        
        # Create switcher for ir-inputs
        self.switcher = {
                "KEY_NUMERIC_0" : self.toggleAnimation,
                "KEY_PLAYPAUSE" : self.togglePause,
                "KEY_NEXT" : self.nextSong,
                "KEY_NUMERIC_2" : self.volumeUp,
                "KEY_NUMERIC_1" : self.volumeDown,
                "KEY_CHANNELDOWN" : self.detectEmotion
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
        print(f'The loaded playertype is: {player}')
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

    def toggleAnimation(self):
        self.send_light("toggleAnimation")

    def togglePause(self):
        self.send_audio("toggle")
        self.send_light("togglePause")

    def nextSong(self):
        self.send_audio("next")

    def volumeUp(self):
        self.send_audio("+")

    def volumeDown(self):
        self.send_audio("-")

    def detectEmotion(self):
        emotion = self.emotionDetection.play()
        self.send_audio(emotion)
        self.send_light(emotion)


#-----------------------------------------------------------------------

if __name__ == "__main__":
    try:
        m = Main()
        m.start_audio_thread()
        m.start_light_thread()
        m.start_loop()
    finally:
        m.kill_threads()
