import pygame
import os,sys

#--Konstanten--
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
TRACK_FOLDER = "tracks/"
TRACKS_PATH = os.path.join(APP_FOLDER, TRACK_FOLDER)
#print("TRACKS_PATH: " + TRACKS_PATH)

# dictionary which assigns each label an emotion (alphabetical order)
# emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
#                 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

#TODO Auslagern in eine Konfigurations-Datei json oder yaml
emotionTracks = {"Happy": "Ketsa - Good Vibe.mp3",
                "Sad" : "applause-1.wav",
                "Angry": "Simon Panrucker - Angry Dance.mp3"}

print("Type \"Happy\", \"Angry\" or \"Sad\" for Song selection:")
emotion = input()
trackToPlay = emotionTracks[emotion]

pygame.mixer.init()
pygame.mixer.music.load(TRACKS_PATH + trackToPlay)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy() == True:
    continue

