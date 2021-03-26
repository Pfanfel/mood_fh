import threading
import queue
import sound

g_queue = queue.Queue()

def setEmotion(emotion):
    g_queue.put(str(emotion))


def main():
    print("mit python -i ausfuehren und in der interaktiven Shell mit setEmotion(\"Happy\",\"Angry\" oder \"Sad\") die Emotion steuern")
    soundThread = threading.Thread(target=sound.threadMain,
                    args=(g_queue, ),
                    daemon=True,
                    name="sound module")
    soundThread.start()

if __name__ == "__main__":
    main()
