import threading
import queue
import code
from soundClasses import AudioThread, MopidyPlayer, PygamePlayer

#-----Je nachdem was getestet werden soll------

# audioThread = AudioThread(PygamePlayer)
audioThread = AudioThread(MopidyPlayer)

def send(emotion):
    audioThread.send_emotion(emotion)

def kill():
    audioThread.kill()
    audioThread.join()

def main():
    print("mit python ausfuehren und in der interaktiven Shell mit send(\"<Emotion>\") die Emotion steuern")
    audioThread.start()


if __name__ == "__main__":
    try:
        main()
        code.interact(local=globals()) #Startet die interactive shell zum testen.
    finally:
        kill()
