import threading
import queue
import code
from soundClazz import AudioThread, MopidyPlayer, PygamePlayer

#Je nachdem was getestet
audioThread = AudioThread(PygamePlayer)
# audioThread = AudioThread(MopidyPlayer)
def send(emotion):
    audioThread.send_emotion(emotion)

def kill():
    audioThread.kill()
    audioThread.join()

def main():
    print("mit python ausfuehren und in der interaktiven Shell mit send(\"Happy\") oder \"Angry\" oder \"Sad\" die Emotion steuern")
    audioThread.start()


if __name__ == "__main__":
    try:
        main()
        code.interact(local=globals()) #Nur zum interactiv testen
    finally:
        kill()
