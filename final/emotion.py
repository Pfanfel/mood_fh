import argparse
import os
import sys
import time
import cv2
import numpy as np
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     MaxPooling2D)
from tensorflow.keras.models import Sequential
from ringbuffer import RingBuffer
from emotionEnum import Emotion

class EmotionDetection:
    '''
    Diese Klasse ist zur Erkennung der Emotion verantwortlich.
    '''
    #--Konstanten--
    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_MODEL = os.path.join(PATH_TO_SOURCE, "model.h5")
    PATH_TO_HAARCASCADE = os.path.join(PATH_TO_SOURCE, "haarcascade_frontalface_default.xml")
    QUEUE_SIZE = 21

    def __init__(self):
        '''
        Initialisiert den Ringbuffer und das Model.
        '''
        # Erstellt einen RingBuffer, der die erkannten Emotionen,
        # welche in einem gewissen Zeitraum erkannt wurden, abspeichert.
        self.ring = RingBuffer(self.QUEUE_SIZE)
        # Erstellt das Model zur Erkennung der Emotionen im Gesicht.
        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu', input_shape=(48, 48, 1)))
        self.model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(7, activation='softmax'))
        self.model.load_weights(self.PATH_TO_MODEL)

        # Verhindert unnoetige Logging-Nachrichten.
        cv2.ocl.setUseOpenCL(False)

    def play(self):
        '''
        Startet die Gesichtserkennung und liefert nach erkannter Emotion diese als Return-Wert.
        '''
        # Faengt das Videosignal.
        cap = cv2.VideoCapture(0)
        # Zaehlt die Anzahl der erkannten Emotionen.
        emotionCount = 0
        while emotionCount < self.QUEUE_SIZE:
            ret, frame = cap.read()
            if not ret:
                return None
            # Findet digitale Bildmerkmale, die bei der Objekterkennung verwendet werden.
            facecasc = cv2.CascadeClassifier(self.PATH_TO_HAARCASCADE)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                # Passt das Bild an, damit das Model zur Emotionserkennung auf das Bild angewendet werden kann.
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(
                    cv2.resize(roi_gray, (48, 48)), -1), 0)
                # Wendet das Model auf das Bild an und versucht eine Emotion zu erkennen.
                prediction = self.model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                # Haengt die erkannte Emotion an den Ringbuffer an.
                self.ring.append(maxindex)
                emotionCount += 1
                cv2.putText(frame, str(Emotion(maxindex + 1)), (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # Videofeed
            cv2.namedWindow('EmotionDetection', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('EmotionDetection',cv2.WND_PROP_FULLSCREEN,1)
            cv2.imshow('EmotionDetection', cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC))
            cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        # Wenn eine Emotion erkannt wurde, wird diese returned.
        if emotionCount == self.QUEUE_SIZE:
            # + 1, da im Emotionsenum die 0 = None ist.
            returnvalue = self.ring.getMode() + 1
            return returnvalue
        # Bei Fehlverhalten default = neutral
        return 5
