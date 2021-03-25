import threading
import queue
import sound

g_queue = queue.Queue()

def setEmotion(emotion):
    g_queue.put(emotion)


def main():
    soundThread = threading.Thread(target=sound.threadMain,
                    args=(g_queue, ),
                    daemon=True,
                    name="Sound module")
    soundThread.start()

if __name__ == "__main__":
    main()
