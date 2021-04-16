import threading
import queue
import code
import yaml
import os
from soundClasses import AudioThread, MopidyPlayer, PygamePlayer

class MainTest:

    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")

    def __init__ (self):
        playertype = self._load_playertype()
        self.audioThread = self._create_audio_thread(playertype)

    def start_audio_thread(self):
        if self.audioThread is not None:
            self.audioThread.start()
        else:
            print('Could not create audio thread')

    def send(self, emotion):
        self.audioThread.send_emotion(emotion)

    def kill_audio_thread(self):
        self.audioThread.kill()
        self.audioThread.join()

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
        elif (playertype == 'mopidy'):
            return AudioThread(MopidyPlayer)
        else:
            print('Valid playertypes in config are: "pygame" and "mopidy"')
            return None


if __name__ == "__main__":
    try:
        m = MainTest()
        m.start_audio_thread()
        print("mit python ausfuehren und in der interaktiven Shell mit m.send(\"<Emotion>\") die Emotion steuern")
        code.interact(local=globals()) #Startet die interactive shell zum testen.
    finally:
        m.kill_audio_thread()
