import pygame
import os,sys
import yaml
import random
import time

from mutagen.mp3 import MP3

#--Konstanten--
TRACK_FOLDER = "tracks/"
EMOTION_TRACKS = "emotionTracks.yaml"
PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
PATH_TO_TRACKS = os.path.join(PATH_TO_SOURCE, TRACK_FOLDER)


def mp3Length(path):
    '''
    Liefert die laenge des Songs in sekunden nach "ID3 tag of mp3"
    '''
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None

def printMp3Length(length):
    if length is None:
        print("Song is not a .mp3")
    else:
        print("Duration sec: " + str(length))
        print("Duration min: " + str(int(length / 60)) + ':' + str(int(length % 60)))

def getSongList(emotion):
    '''
    Liefert eine Liste an Songs aus der Konfigurationsdatei
    '''
    with open(os.path.join(PATH_TO_SOURCE, EMOTION_TRACKS), "r") as t:
        dictionary = yaml.safe_load(t)
    try:
        tracks = dictionary[emotion]
    except KeyError:
        print("The Key " + emotion + "does not exist")
        return None
    print("The Song list is: " + str(tracks))
    return tracks


def main():
    print ("Path to Source: " + str(PATH_TO_SOURCE))
    print("Path to Tracks: " + PATH_TO_TRACKS)
    print("Type \"Angry\", \"Disgusted\", \"Fearful\", \"Happy\", \"Neutral\", \"Sad\" or \"Surprised\" for Song selection:")
    emotion = input()
    
    tracksToPlay = getSongList(emotion)
    if tracksToPlay is None:
        print("No Song avalible")
    else:
        trackToPlay = random.choice(tracksToPlay)
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
            pathToTrackToPlay = os.path.join(PATH_TO_TRACKS ,trackToPlay)
            print("Path to Track to play: "+ pathToTrackToPlay)
            #Die Dauer des Songs bestimmen
            durationOfTrackToPlay = mp3Length(pathToTrackToPlay)
            printMp3Length(durationOfTrackToPlay)
            pygame.mixer.music.load(pathToTrackToPlay)
            #Startet in den Song in einem eigenen Thead und kehrt sofort zurück
            pygame.mixer.music.play(loops=0, start=0.0, fade_ms = 2000)

            #Momentan noch blokierend, aber später im Programm muss nur der Song geladen und abgespielt werden, ohne zu blokieren.
            while pygame.mixer.music.get_busy() == True:
                continue

if __name__ == "__main__":
    main()
