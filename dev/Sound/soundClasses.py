import time
import queue
import threading
import os,sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Damit nicht immer die pygame Message kommt
import pygame
import yaml
import random
from piripherals import MPD

class MopidyPlayer:
    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")
    VOLUME_STEP = 10
    
    def __init__(self):
        '''
        Konstruktor, welcher einen Client erstellt, um mit dem mopidy Server zu kommunizieren.
        '''
        self.volume = 40
        self.c = MPD()
        self.c.connect("localhost", 6600)
        #self.c.crossfade(1) #Ist aufgrund eines Bugs bei mopidy-mpd nicht möglich.

    def tick(self):
        '''
        Tut nichts, da der MopidyPlayer nur Signale an den mopidy Server sendet, welcher die Musik abspielt.
        Existiert nur, um dasselbe Interface zu erfuellen wie der PygamePlayer.
        '''
        pass
        
    def play(self, emotion):
        '''
        Spielt eine Playlist gegeben einer Emotion im shuffle Modus.
        '''
        emotion = emotion.lower()
        playlist = self._load_playlist(emotion)
        if playlist is not None:
            self.c.clear()
            self.c.load(playlist)
            self.c.shuffle()
            self.c.play()
            print(self.c.status())

    def close(self):
        '''
        Raumt auf, wenn player gekillt wird.
        Muss stop() Signal an den mopidy Server senden, sonst spielt die Musik noch nachdem das
        Programm beendet wurde.  
        '''
        self.c.stop()

    def decrease_volume(self):
        '''
        Verringert die Lautstärke.
        '''
        if (self.volume - self.VOLUME_STEP >= 0):
            self.volume -= self.VOLUME_STEP
        else:
            print("Min volume")
        print(f"New Volume: {self.volume}")
        self.c.setvol(self.volume)
        print(self.c.status())

    def increase_volume(self):
        '''
        Erhoeht die Lautstärke.
        '''
        if (self.volume + self.VOLUME_STEP <= 100):
            self.volume += self.VOLUME_STEP
        else:
            print("Max volume")
        print(f"New Volume: {self.volume}")
        self.c.setvol(self.volume)
        print(self.c.status())

    def toggle_pause(self):
        '''
        Pausiert bzw. setzt den aktuell gespielten Song fort.
        '''
        self.c.toggle_play()

    def play_next_song(self):
        '''
        Spielt den naechsten Song in der Playlist ab.
        '''
        if (self.c.state() == "pause"):
            self.c.toggle_play()
        self.c.next()
        print("Last Song info: " + str(self.c.currentsong()))

    def _load_playlist(self, emotion):
        '''
        Liefert die Playlist aus der Konfigurationsdatei, welche ueber Spotify abgespielt werden soll
        '''
        with open(self.PATH_TO_CONFIG, "r") as t:
            config = yaml.safe_load(t)
        try:
            print(config)
            playlist = config['spotify_playlists'][emotion]
        except KeyError:
            print(f'The Emotion "{emotion}"  does not exist')
            return None
        print(f'The Playlist is: "{playlist}"')
        return playlist
        

class PygamePlayer:

    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_TRACKS = os.path.join(PATH_TO_SOURCE, "tracks")
    PATH_TO_CONFIG = os.path.join(PATH_TO_SOURCE, "soundConfig.yaml")
    FADE_TIME_MS = 500 #Fuer fade in und fade out genutzt (fade dauert also FADE_TIME_MS*2)
    VOLUME_STEP = 10 #Sollte %100 == 0 sein
    
    def __init__(self):
        '''
        Konstruktor fuer den PygamePlayer.
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
        self.volume = 40
        self.paused = False
    
    def tick(self):
        '''
        Prueft ob der aktuelle Song zuende ist und spielt ggf. den naechsten.
        '''
        if not self.paused and not pygame.mixer.music.get_busy():
            self.play_next_song()

    def play(self, emotion):
        '''
        Spielt eine Playlist gegeben einer Emotion ab.
        '''
        emotion = emotion.lower()
        #Setze neue Playlist
        self._update_playlist(emotion)
        #Starte die Playlist
        self.play_next_song()

    def decrease_volume(self):
        '''
        Verringert die Lautstärke.
        '''
        if (self.volume - self.VOLUME_STEP >= 0):
            self.volume -= self.VOLUME_STEP
        else:
            print("Min volume")
        print(f"New Volume: {self.volume}")
        pygame.mixer.music.set_volume(self.volume/100.0)
    

    def increase_volume(self):
        '''
        Erhoeht die Lautstärke.
        '''
        if (self.volume + self.VOLUME_STEP <= 100):
            self.volume += self.VOLUME_STEP
        else:
            print("Max volume")
        print(f"New Volume: {self.volume}")
        pygame.mixer.music.set_volume(self.volume/100.0)

    def toggle_pause(self):
        '''
        Pausiert bzw. setzt den aktuell gespielten Song fort.
        '''
        self.paused = not self.paused
        print("Pause State :" + str(self.paused))
        if (self.paused):
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def close(self):
        '''
        Raumt auf, wenn player gekillt wird.
        '''
        pygame.mixer.quit()

    def play_next_song(self):
        '''
        Spielt einen zufaelligen Song aus der aktuellen playlist
        '''
        if self.playlist is not None:
            file_name = random.choice(self.playlist)
            path = os.path.join(self.PATH_TO_TRACKS, file_name)
            print(f'Path to Next Song Track to play: "{path}"')
            if self.paused:
                self.toggle_pause()
            else:
                pygame.mixer.music.fadeout(self.FADE_TIME_MS)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume/100.0)
            pygame.mixer.music.play(loops=0, start=0.0, fade_ms = self.FADE_TIME_MS)

    def _update_playlist(self, emotion):
        '''
        Liefert eine Liste an Songs (Playlist) aus der Konfigurationsdatei
        '''
        with open(self.PATH_TO_CONFIG, "r") as t:
            config = yaml.safe_load(t)
        try:
            tracks = config['pygame_playlists'][emotion]
        except KeyError:
            print(f'The Emotion "{emotion}"  does not exist')
            return None
        print(f'The Song list is: "{tracks}"')
        self.playlist = tracks
        

class AudioThread(threading.Thread): #Erbt von Thread
    #--Konstanten--
    DELAY = 0.1

    def __init__(self, PlayerClass):
        '''
        Konstruktor, welcher eine Klasse uebergeben bekommt, welche in dem Thread laufen soll.
        '''
        super().__init__(daemon=True, name="audio_thread")#Ruft den threading.Thread Konstuktor auf
        self.queue = queue.Queue()
        self.player = PlayerClass()
        self.new_emotion = None
        self.emotion = None
        self.killed = threading.Event()#Zum synchronisieren, damit darauf gewartet werden kann. 

    def run(self):
        '''
        Main-Methode des Threads.
        Lauft solange dieser ein kill Event bekommt.
        '''
        try:
            while not self.killed.is_set():
                self.next_tick = time.time() + self.DELAY
                self._handle_queue()
                self._tick()
                self._sleep()
        finally:
            self.player.close()

    
    def kill(self):
        self.killed.set()

    def _handle_queue(self):
        '''
        Kuemmert sich um die Nachrichten, welche aus der queue kommen und beachtet nur die letze.
        '''
        try:
            while True: #Lauft bis eine Exception fliegt (queue leer)
                msg = self.queue.get(block=False, timeout=None)
                if(msg == "+"):
                    self.player.increase_volume()
                elif(msg == "-"):
                    self.player.decrease_volume()
                elif(msg == "toggle"):
                    self.player.toggle_pause()
                elif(msg  == "next"):
                    self.player.play_next_song()
                else:
                    self.new_emotion = msg
        except queue.Empty:
            pass

    def _tick(self):
        '''
        Prueft in regelmaessigen abstaenden, ob eine neue Nachricht in der queue liegt.
        '''
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
        '''
        Schlaeft einen bestimmten Zeitintervall bis zum naechsten tick.
        '''
        self.killed.wait(timeout=max(0, self.next_tick - time.time()))



    #----Methode zum testen-----
    def send_emotion (self, emotion):
        self.queue.put(emotion)



def main():
    try:
        audioThread = AudioThread(MopidyPlayer)
        audioThread.start() #Kehrt hier nicht mehr zurueck, wenn direkt ausgefuehrt.
    finally:
        audioThread.kill()

if __name__ == "__main__":
   main()