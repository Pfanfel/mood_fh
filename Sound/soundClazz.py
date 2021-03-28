import time
import queue
import threading
import pygame
import os,sys
import yaml
from itertools import cycle

class MopidyPlayer:
    playlists = {
        'Happy': 'SKAZKI (by polinaver)',
        'Angry': 'Mr. Robot Season 4 Soundtrack (by lascancionesdelatele.com)'
    }
    
    def __init__(self):
        from piripherals import MPD

        self.c = MPD()
        self.c.connect("localhost", 6600)
        #self.c.crossfade(1)

    def tick(self):
        pass
        
    def play(self, emotion):
        playlist = self.playlists.get(emotion)
        if playlist is not None:
            self.c.clear()
            self.c.load(playlist)
            self.c.shuffle()
            self.c.play()
    def close(self):
        print("Goodbye")
        self.c.stop()
        

class PygamePlayer:

    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_TRACKS = os.path.join(PATH_TO_SOURCE, "tracks")
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "emotionTracks.yaml")
    FADE_TIME_MS = 500 #Fuer fade in und fade out
    
    def __init__(self):
        '''
        Falls hier der Fehler:
        NotImplementedError: mixer module not available (ImportError: libSDL2_mixer-2.0.so.0: cannot open shared object file: No such file or directory)
        kommt muss folgendes package noch installiert werden:
        sudo apt install libsdl2-mixer-2.0-0 
        '''
        pygame.mixer.init()
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            print("Mixer not initialized, playing music not possible")
        else:
            print("Mixer Parameter: ")
            print(mixer_info)

        self.playlist = None

    def _update_playlist(self, emotion):
        '''
        Liefert eine Ringliste an Songs aus der Konfigurationsdatei
        '''
        with open(self.PATH_TO_CONFIG, "r") as t:
            config = yaml.safe_load(t)
        try:
            tracks = config[emotion]
        except KeyError:
            print(f'The Emotion "{emotion}"  does not exist')
            return None
        print(f'The Song list is: "{tracks}"')
        self.playlist = cycle(tracks)

    def _play_next_song(self):
        if self.playlist is not None:
            file_name = next(self.playlist)
            path = os.path.join(self.PATH_TO_TRACKS, file_name)
            print(f'Path to Next Song Track to play: "{path}"')
            pygame.mixer.music.fadeout(self.FADE_TIME_MS)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=0, start=0.0, fade_ms = self.FADE_TIME_MS)
    
    def tick(self):
        if not pygame.mixer.music.get_busy():
            self._play_next_song()

    def play(self, emotion):
        #Setze neue Playlist
        self._update_playlist(emotion)
        #Starte die Playlist
        self._play_next_song()
    
    def close(self):
        pass #TODO call close
        

class AudioThread(threading.Thread): #Erbt von Thread
    DELAY = 0.1
    def __init__(self, PlayerClass):
        super().__init__(daemon=True, name="audio_thread")#Ruft den threading.Thread Konstuktor auf
        self.queue = queue.Queue()
        self.player = PlayerClass()
        self.new_emotion = None
        self.emotion = None
        self.killed = threading.Event()#Zum synchronisieren, damit darauf gewartet werden kann. 


    def _handle_queue(self):
        try:
            while True: #Lauft bis eine Exception fliegt (queue leer)
                self.new_emotion = self.queue.get(block=False, timeout=None)
        except queue.Empty:
            pass


    def _tick(self):
        isPlaying = self.emotion is not None
        isNewSongRequested = self.new_emotion is not None


        if isNewSongRequested:
            print(f"Die Emotion lautet: {self.emotion}")
            print(f"Die neue Emotion lautet: {self.new_emotion}")
            if not isPlaying:
                self.player.play(self.new_emotion)
            elif self.new_emotion != self.emotion:
                self.player.play(self.new_emotion)

            self.emotion = self.new_emotion
            self.new_emotion = None
        self.player.tick()

    def _sleep(self):
        self.killed.wait(timeout=max(0, self.next_tick - time.time()))

    def run(self):
        try:
            while not self.killed.is_set():
                self.next_tick = time.time() + self.DELAY
                self._handle_queue()
                self._tick()
                self._sleep()
        finally:
            self.player.close()
    def send_emotion (self, emotion):
        self.queue.put(emotion)
    def kill(self):
        self.killed.set()

def main():
    try:
        audioThread = AudioThread(MopidyPlayer)
        audioThread.start()
    finally:
        audioThread.kill()

if __name__ == "__main__":
   main()
