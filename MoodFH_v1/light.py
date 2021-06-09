import serial
import time
import os
import queue
import threading
from emotionEnum import Emotion

class LightThread(threading.Thread): #Erbt von Thread
    #--Konstanten--
    DELAY = 0.1

    def __init__(self):
        '''
        Konstruktor, welcher eine Klasse uebergeben bekommt, welche in dem Thread laufen soll.
        '''
        super().__init__(daemon=True, name="light_thread")#Ruft den threading.Thread Konstuktor auf
        
        # ACM-Nummer fuer Arduino mit ls /dev/tty/ACM* ermitteln
        self.ser=serial.Serial("/dev/ttyACM0",9600)
        
        self.queue = queue.Queue()
        self.animationOn = False
        self.emotion = Emotion.NEUTRAL
        self.pause = False
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
            self._arduino_stop()

    
    def kill(self):
        self.killed.set()

    def _handle_queue(self):
        '''
        Kuemmert sich um die Nachrichten, welche aus der queue kommen und beachtet nur die letze.
        '''
        try:
            while True: #Lauft bis eine Exception fliegt (queue leer)
                msg = self.queue.get(block=False, timeout=None)
                if(msg == "false"):
                    self.pause = False
                    self.animationOn = False
                elif(msg == "true"):
                    self.pause = False
                    self.animationOn = True
                elif(msg == "toggle"):
                    self.pause = not self.pause
                else:
                    self.emotion = msg
        except queue.Empty:
            pass

    def _tick(self):
        '''
        Prueft in regelmaessigen abstaenden, ob eine neue Nachricht in der queue liegt.
        '''
        # Aktuelle Emotion an den Arduino uebermitteln
        if(self.pause):
            self.ser.write(('b\'' + str(Emotion.NONE.value) + '\'').encode('ascii'))
        else:
            self.ser.write(('b\'' + str(self.emotion.value) + '\'').encode('ascii'))
        
        # Aktuelle Angabe ueber Animation an den Arduino uebermitteln
        if (self.animationOn):
            self.ser.write(('T').encode('ascii'))
        else:
            self.ser.write(('F').encode('ascii'))
        
    def _sleep(self):
        '''
        Schlaeft einen bestimmten Zeitintervall bis zum naechsten tick.
        '''
        self.killed.wait(timeout=max(0, self.next_tick - time.time()))
        
    def send_emotion (self, emotion):
        self.queue.put(emotion)

    def _arduino_stop(self):
        '''
        Schaltet den LED-Streifen aus.
        '''
        for i in range(0,100):
            self.ser.write(('b\'' + str(Emotion.NONE.value) + '\'').encode('ascii'))
