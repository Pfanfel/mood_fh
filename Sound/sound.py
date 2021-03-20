import pygame
import os,sys
import yaml
import random

#--Konstanten--
TRACK_FOLDER = "tracks/"
EMOTION_TRACKS = "emotionTracks.yaml"
PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
PATH_TO_TRACKS = os.path.join(PATH_TO_SOURCE, TRACK_FOLDER)

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
    print("Die Liste an Songs lautet: " + str(tracks))
    return tracks


def main():
    print ("Path to Source: " + str(PATH_TO_SOURCE))
    print("Path to Tracks: " + PATH_TO_TRACKS)
    print("Test over SSH")
    print("Type \"Angry\", \"Disgusted\", \"Fearful\", \"Happy\", \"Neutral\", \"Sad\" or \"Surprised\" for Song selection:")
    emotion = input()
    
    tracksToPlay = getSongList(emotion)
    if(tracksToPlay is None):
        print("No Song avalible")
    else:
        trackToPlay = random.choice(tracksToPlay)
        '''
        Falls hier der Fehler:
        NotImplementedError: mixer module not available (ImportError: libSDL2_mixer-2.0.so.0: cannot open shared object file: No such file or directory)
        kommt muss das das package noch installiert werden:
        sudo apt install libsdl2-mixer-2.0-0 
        '''
        pygame.mixer.init()
        print("Path to Track to play: "+ os.path.join(PATH_TO_TRACKS ,trackToPlay))
        pygame.mixer.music.load(os.path.join(PATH_TO_TRACKS ,trackToPlay))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            continue

if __name__ == "__main__":
    main()
