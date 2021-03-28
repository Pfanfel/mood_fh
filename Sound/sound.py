import pygame
import os,sys
import yaml
import time
from itertools import cycle

#--Konstanten--
TRACK_FOLDER = "tracks/"
EMOTION_TRACKS = "emotionTracks.yaml"
PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
PATH_TO_TRACKS = os.path.join(PATH_TO_SOURCE, TRACK_FOLDER)

#--Globale Variablen--
g_currentEmotion = None
g_currentPlaylist = None


def getSongList(emotion):
    '''
    Liefert eine Ringliste an Songs aus der Konfigurationsdatei
    '''
    with open(os.path.join(PATH_TO_SOURCE, EMOTION_TRACKS), "r") as t:
        dictionary = yaml.safe_load(t)
    try:
        tracks = dictionary[emotion]
    except KeyError:
        print("The Key " + emotion + "does not exist")
        return None
    print("The Song list is: " + str(tracks))
    return cycle(tracks)

def getPathToNextSong(cycleSongList):
    nextSong = next(cycleSongList)
    pathToNextSong = os.path.join(PATH_TO_TRACKS ,nextSong)
    print("Path to Next Song Track to play: " + pathToNextSong)
    return pathToNextSong

def setCurrentEmotion():
    global g_currentEmotion
    print("Type \"Angry\", \"Disgusted\", \"Fearful\", \"Happy\", \"Neutral\", \"Sad\" or \"Surprised\" for Song selection:")
    g_currentEmotion = input()

def setCurrentPlaylist():
    global g_currentPlaylist
    g_currentPlaylist = getSongList(g_currentEmotion)

def main():
    init()
    #Anscheindend wird das gebraucht um pygame.event.get() aufrufen zu koennen
    pygame.display.init()
    screen = pygame.display.set_mode ( ( 420 , 240 ) )

    print("Path to Source: " + str(PATH_TO_SOURCE))
    print("Path to Tracks: " + str(PATH_TO_TRACKS))

    setCurrentEmotion()
    setCurrentPlaylist()
    

    if g_currentPlaylist is None:
        print("No Song avalible")
    else:
        pathToNextRandomSong = getPathToNextSong(g_currentPlaylist)
        pygame.mixer.music.load(pathToNextRandomSong)
        pygame.mixer.music.queue (getPathToNextSong(g_currentPlaylist)) # Queue the 2nd song
        pygame.mixer.music.set_endevent ( pygame.USEREVENT )    # Setup the end track event
        #Startet in den Song in einem eigenen Thead und kehrt sofort zurueck
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms = 2000)
        
        #Momentan noch mit der pygame eventloop, sollte aber noch geandert werden, damit kein Fenster benoetigt wird
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:    # A track has ended
                    pygame.mixer.music.queue ( getPathToNextSong(g_currentPlaylist) ) # Q


def init():
    '''
    Falls hier der Fehler:
    NotImplementedError: mixer module not available (ImportError: libSDL2_mixer-2.0.so.0: cannot open shared object file: No such file or directory)
    kommt muss folgendes package noch installiert werden:
    sudo apt install libsdl2-mixer-2.0-0 
    '''
    pygame.mixer.init()
    
    if pygame.mixer.get_init() is None:
        print("Mixer not initialized, playing music not possible")
    else:
        print("Mixer Parameter: ")
        print(pygame.mixer.get_init())

def playNextSong():
    pathToNextSong = getPathToNextSong(g_currentPlaylist)
    pygame.mixer.music.load(pathToNextSong)
    pygame.mixer.music.play(loops=0, start=0.0, fade_ms = 0)


def threadMain(queue):
    global g_currentEmotion
    global g_currentPlaylist
    init()
    while True:
        handleQueue(queue)
        handleState()
        handle
        if pygame.mixer.get_busy():
            time.sleep(0.1)
        else:
            if not queue.empty():
                #TODO alle holen und nur die letze beruecksichtigen
                emotionInQueue = queue.get(block=False, timeout=None)
                print("New Emotion recieved: " + emotionInQueue)
               #Nur wenn neue Emption kommt neue Playlist setzen
                if (g_currentEmotion != emotionInQueue):
                    g_currentEmotion = emotionInQueue
                    setCurrentPlaylist()
                    playNextSong()

    # while True:
    #     print (str(g_currentPlaylist))
    #     emotionInQueue = None
    #     try:
    #         emotionInQueue = queue.get(block=False, timeout=None)
    #     except: #Es fliegt eine Empty exception, wenn nichts in der queue
    #         time.sleep(1)
    #     else:
    #         print("New Emotion recieved: " + emotionInQueue)
    #         #Wenn neue Emotion kommit -> Neustarten, ansonsten weiterspielen
    #         if (g_currentEmotion != emotionInQueue):
    #             g_currentEmotion = emotionInQueue
    #             setCurrentPlaylist()
    #             playNextSong()
    #     if pygame.mixer.get_busy():
    #         time.sleep(1)
    #     else:
    #         if g_currentPlaylist is not None:
    #             playNextSong()
            

            

if __name__ == "__main__":
    main()
