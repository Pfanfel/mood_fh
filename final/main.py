#!/home/pi/Documents/mood_fh/final/moodvenv/bin/python3
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
    Kuemmert sich um das Starten der Sound- und Light-Threads, sowie die Signalverarbeitung der IR-Fernbedienung.
    '''
    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")

    def __init__ (self):
        '''
        Initialisiert alle Threads, die Emotionserkennung und das InputDevice.
        '''
        playertype = self._load_playertype()

        self.audioThread = self._create_audio_thread(playertype)

        self.lightThread = LightThread()

        self.emotionDetection = EmotionDetection()

        self.dev = self._getInputDevice()
        if self.dev == None:
            print("Kein IR-Device gefunden!")

        # Switch fuer die IR-Inputs
        self.switcher = {
                "KEY_NUMERIC_0" : self._toggleAnimation,
                "KEY_PLAYPAUSE" : self._togglePause,
                "KEY_NEXT" : self._nextSong,
                "KEY_NUMERIC_2" : self._volumeUp,
                "KEY_NUMERIC_1" : self._volumeDown,
                "KEY_CHANNELDOWN" : self._detectEmotion
            }

    def _getInputDevice(self):
        '''
        Liefert das Input Device (IR-Diode)
        '''
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == 'gpio_ir_recv':
                return device
        return None

    def _start_loop(self):
        '''
        Mainloop des Programs. Empfaengt IR-Signale und ruft entsprechende Methoden auf. 
        '''
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1:
                    func = self.switcher.get(str(data.keycode), "nothing")
                    if func != "nothing":
                        func()

    def _start_audio_thread(self):
        '''
        Startet den AudioThread.
        '''
        if self.audioThread is not None:
            self.audioThread.start()
        else:
            print('Could not create audio thread')

    def _start_light_thread(self):
        '''
        Startet den LightThread.
        '''
        if self.lightThread is not None:
            self.lightThread.start()
        else:
            print('Could not create light thread')

    def _send_audio(self, emotion):
        '''
        Sendet ein Signal an den AudioThread.
        '''
        self.audioThread.send_emotion(emotion)

    def _send_light(self, emotion):
        '''
        Sendet ein Signal an den LightThread.
        '''
        self.lightThread.send_emotion(emotion)

    def _load_playertype(self):
        '''
        Liest den Musikplayer aus der Config-Datei.
        '''
        with open(self.PATH_TO_CONFIG, "r") as t:
            config = yaml.safe_load(t)
        try:
            player = config['player_type']
        except KeyError:
            #TODO: Weiter behandeln oder reicht das?
            print('The Playerfield does not exist in config')
        player = player.lower()
        return player

    def _create_audio_thread(self, playertype):
        '''
        Erstellt den AudioThread abhaenging vom ausgewaehlten Musikplayer.
        '''
        if (playertype == 'pygame'):
            return AudioThread(PygamePlayer)
        elif (playertype == 'spotify'):
            return AudioThread(MopidyPlayer)
        else:
            print('Valid playertypes in config are: "pygame" and "mopidy"')
            return None

#---------------------------- Input Methodenaufrufe --------------------

    def _toggleAnimation(self):
        '''
        Sendet ein toggleAnimation Signal an den LightThread.
        '''
        self._send_light("toggleAnimation")

    def _togglePause(self):
        '''
        Sendet ein togglePause Signal an den Light- und AudioThread.
        '''
        self._send_audio("toggle")
        self._send_light("togglePause")

    def _nextSong(self):
        '''
        Sendet ein Signal an den AudioThread, um das naechste Lied zu starten.
        '''
        self._send_audio("next")

    def _volumeUp(self):
        '''
        Sendet ein Signal an den AudioThread, um die Lautstaerke zu erhoehen.
        '''
        self._send_audio("+")

    def _volumeDown(self):
        '''
        Sendet ein Signal an den AudioThread, um die Lautstaerke zu verringern.
        '''
        self._send_audio("-")

    def _detectEmotion(self):
        '''
        Startet die Emotionserkennung und sendet bei erkannter Emotion diese an die Threads.
        '''
        emotion = self.emotionDetection.play()
        self._send_audio(emotion)
        self._send_light(emotion)


#-----------------------------------------------------------------------

    def _kill_threads(self):
        '''
        Killt alle Threads.
        '''
        self.audioThread.kill()
        self.lightThread.kill()
        self.audioThread.join()
        self.lightThread.join()

if __name__ == "__main__":
    '''
    Startet die Threads und die Loop fuer die IR-Signale.
    '''
    m = Main()
    try:
        m._start_audio_thread()
        m._start_light_thread()
        m._start_loop()
    finally:
        m._kill_threads()
