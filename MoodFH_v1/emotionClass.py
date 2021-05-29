#!/home/pi/Documents/mood_fh/EmotionDetection/emotionvenv/bin/python3
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

class EmotionDetection:

    PATH_TO_SOURCE = os.path.abspath(os.path.dirname( __file__ ))
    PATH_TO_MODEL = os.path.join(PATH_TO_SOURCE, "model.h5")
    PATH_TO_HAARCASCADE = os.path.join(PATH_TO_SOURCE, "haarcascade_frontalface_default.xml")
    PATH_TO_TEXTFILE = os.path.join(PATH_TO_SOURCE, "emotion.txt")
    QUEUE_SIZE = 20

    def __init__(self):
        # create RingBuffer
        self.ring = RingBuffer(self.QUEUE_SIZE)
        # create model
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
        # create EmotionDict
        self.emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                             3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        # prevents openCL usage and unnecessary logging messages
        cv2.ocl.setUseOpenCL(False)

    def play(self):
        # start the webcam feed
        cap = cv2.VideoCapture(0)
        # counts the predicted emotions
        emotionCount = 0
        while emotionCount < self.QUEUE_SIZE:
            # Find haar cascade to draw bounding box around face
            ret, frame = cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier(self.PATH_TO_HAARCASCADE)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(
                    cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = self.model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                self.ring.append(maxindex)
                emotionCount += 1
                cv2.putText(frame, self.emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('EmotionDetection', frame)
            cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
        if emotionCount == self.QUEUE_SIZE:
            print("Emotion erkannt: ")
            f = open(self.PATH_TO_TEXTFILE, "a")
            f.write("Emotion erkannt: ")
            f.write(self.emotion_dict[self.ring.getMode()])
            f.close()
            print(self.emotion_dict[self.ring.getMode()])
            return self.emotion_dict[self.ring.getMode()]
        return None
