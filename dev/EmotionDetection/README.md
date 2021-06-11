# Webcam-Emotion-Detection

## Setup:

**OpenCV installieren:**

```
sh install_opencv_dependencies.sh

```

Falls nach der Installation Probleme auftreten, kann auch dieser [guide](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/) benutzt werden.

**Folgende Zeile in _/boot/config.txt_ ändern:**

```
dtoverlay=gpio-ir,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up
```

Falls diese Zeile nicht vorhanden ist am Ende der Datei anhängen.

**TODO: Folgende Zeile in Crontab hinzufügen:**

```
sh /PFAD/setup_ir-keytable.sh
```

**Virtuelle Umgebung einrichten:**

```
virtualenv <enviroment_name> -p python3
```

**Aktivieren der virtuellen Umgebung:**

```
source <enviroment_name>/bin/activate
```

**Bilbiotheken installieren:**

```
pip install -r emotion_requirements.txt
```

**Programm starten:**

```
python mainTest.py
```
