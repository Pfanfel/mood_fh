import serial
import time
import os
import queue
import threading
from emotionEnum import Emotion

'''
    Stellt einen Thread bereit, um das Licht-Modul zu steuern
'''
class LightThread(threading.Thread): #Erbt von Thread
    
    # Delay bis zum naechten Tick (an den Arduino)
    DELAY = 0.1
    
    '''
        Konstruktor, welcher eine Klasse uebergeben bekommt, welche in dem Thread laufen soll.
    '''
    def __init__(self):
        # Ruft den threading.Thread Konstuktor auf
        super().__init__(daemon=True, name="light_thread")
        
        # ACM-Nummer fuer Arduino mit ls /dev/tty/ACM* ermitteln
        self.ser=serial.Serial("/dev/ttyACM0",9600)
        
        self.queue = queue.Queue()
        self.animationOn = False
        self.emotion = Emotion.NEUTRAL
        self.pause = False
        # Zum synchronisieren, damit darauf gewartet werden kann
        self.killed = threading.Event()

    '''
        Main-Methode des Threads.
        Lauft solange dieser kein kill Event bekommt.
    '''
    def run(self):
        try:
            # Solange fortfuehren, bis Thread beendet werden soll
            while not self.killed.is_set():
                self.next_tick = time.time() + self.DELAY
                # Nachrichten der queue verarbeiten
                self._handle_queue()
                self._tick()
                # Wartet ein best. Zeitintervall
                self._sleep()
        finally:
            self._arduino_stop()

    '''
        Markieren, dass Thread beendet werden soll.
    '''
    def kill(self):
        self.killed.set()
        
    '''
        Verarbeitet die Nachrichten aus der queue und beachtet dabei nur die Letzte.
    '''
    def _handle_queue(self):
        try:
            # Lauft bis eine Exception fliegt (queue leer)
            while True:
                # Letztes ELement aus der queue holen
                msg = self.queue.get(block=False, timeout=None)
                # Pruefen, ob Animation an-/ausgeschaltet werden soll
                if(msg == "toggleAnimation"):
                    self.pause = False
                    self.animationOn = not self.animationOn
                # Pruefen, ob Pausiert werden soll
                elif(msg == "togglePause"):
                    self.pause = not self.pause
                # Emotion abspeichern
                else:
                    self.emotion = Emotion(msg)
        except queue.Empty:
            pass

    '''
        Prueft in regelmaessigen abstaenden, ob eine neue Nachricht in der queue liegt.
    '''
    def _tick(self):
        # Aktuelle Emotion an den Arduino uebermitteln, mit Hilfe des Emotionswertes
        if(self.pause):
            self.ser.write(('b\'' + str(Emotion.NONE.value) + '\'').encode('ascii'))
        else:
            self.ser.write(('b\'' + str(self.emotion.value) + '\'').encode('ascii'))
        
        # Aktuelle Angabe ueber Animation an den Arduino uebermitteln
        if (self.animationOn):
            self.ser.write(('T').encode('ascii'))
        else:
            self.ser.write(('F').encode('ascii'))
            
    '''
        Schlaeft ein bestimmtes Zeitintervall lang bis zum naechsten tick.
    '''        
    def _sleep(self):
        self.killed.wait(timeout=max(0, self.next_tick - time.time()))
        
    '''
        Fuegt die ermittelte Emotion der Queue hinzu.
    '''
    def send_emotion (self, emotion):
        self.queue.put(emotion)

    '''
        Schaltet den LED-Streifen aus.
    '''
    def _arduino_stop(self):
        for i in range(0,100):
            # Dem Arduino uebermitteln, dass keine Farben mehr angezeigt werden sollen
            self.ser.write(('b\'' + str(Emotion.NONE.value) + '\'').encode('ascii'))
