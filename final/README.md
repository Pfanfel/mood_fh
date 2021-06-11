# Installationsanleitung

## PI aufsetzen

1. Herunterladen und erstellen des Images mit: <https://www.raspberrypi.org/software/>

2. Auf dem PI ssh aktivieren und mit diesem nach dieser Anleitung über SSH verbinden.
<https://blog.sebastian-martens.de/development/setup-raspberry-pi-without-external-monitor-and-keyboards/>
Alternativ kann die Einrichtung direkt auf dem PI vorgenommen werden.

3. Mit VNC auf den PI verbinden und die Locale einstellen

4. Passwort ändern, da Defaultpasswort mit einem geöffnetem SSH und VNC Zugang unsicher ist.

5. Updaten und rebooten

## Installation von Sound-Modul

### Projekt Klonen und Grundeinrichtung vornehmen

1. Mit `sudo raspi-config` die Konfiguration öffnen und unter `System Options (S) -> Audio (S2)` auswählen und den Audio Output auf `“1 Headphones”` stellen. Außerdem sollte hier auch schon die PI Kamera aktiviert werden, da diese später noch benötigt wird.

2. Repo clonen mit `git clone https://github.com/Pfanfel/mood_fh.git`

3. Erstellt ein Environment im aktuellen Verzeichniss:

    - Arch:
    
    `python -m venv <enviroment_name>`

    - Ubuntu:

        `sudo apt install python3-pip`, falls pip nicht vorhanden

        `pip3 install virtualenv`, falls virtualenv nicht vorhanden

        `python3 -m virtualenv <enviroment_name>`

    - Das virtual environment aktivieren mit `source <enviroment_name>/bin/activate`

        Der Name des environment sollte nun am Anfang der Kommandozeile stehen `<enviroment_name> $`

    - Zum deaktivieren des virtual environment kann der Befehl `deactivate` verwendet werden.

4. In dem venv die notwndigen Packages mit `pip install -r sound_requirements.txt` installieren.

5. Mit `chmod +x setup.sh` das script, welches zusätzlich den von pygame benötigten mixter runterläd auf ausführbar stellen und anschließend mit `./setup.sh` ausführen.

6. Mit `python main.py` im Sound Ordner kann das abspielen von lokaler Musik mit dem pygame-player getestet werden. (Player sollte dafür in der `soundConfig.yaml` auf pygame gesetzt sein)

### [Optional] Einrichten von Mopedy, um das abspielen von Musik über Spotify zu ermöglichen. Spotify Permium Account benötigt

1. Mopedy nach der folgenden Anleitung installieren: <https://docs.mopidy.com/en/latest/installation/raspberrypi/>
`mopidy.sh` script ausführen (ggf. mit `chmod +x` ausführbar machen)
Damit werden die Repos von Mopidy hinzugefügt und mopidy die spotify und die mpd Extention installiert.

2. mopidy in die video Gruppe hinzufügen `sudo adduser mopidy video`

3. Zum erstellen der Konfigutationsdatei muss `mopidy` einmal von der Kommandozeile ausgefuehrt werden

4. Die Konfigurationsdatei unter `/home/pi/.config/mopidy/mopidy.conf` öffen und  
`output = alsasink` unter `[audio]` auskommentieren/einfügen, damit nicht der HDMI Ausgang für den Sound genutzt wird.

5. Konfiguration vom Spotify vornehmen siehe: <https://github.com/mopidy/mopidy-spotify#configuration>
    - Details zur Konfiguration: <https://docs.mopidy.com/en/release-0.19/config/>
    - In der `/home/pi/.config/mopidy/mopidy.conf` den Username und das Passwort seines Spotify-Premium(!) Accounts eintragen
    - Die Authentifizierung wie hier beschrieben durchfüheren (Pop-Up öffen, bestätigen, id und secret  in die mopidy.conf eintragen): <https://mopidy.com/ext/spotify/#authentication>
    - Die auskommentieren Zeilen unter `[spotify]` einkommentieren

6. Mit `mopidy` den Server von der Kommandozeile aus straten und prüfen, ob der Login geklappt hat.
Im Debug output sollte die Zeile : `Logged into Spotify Web API as XYZ` erscheinen.

7. Mopidy beim hochfahren des PIs automatisch starten lassen. Genau beschieben unter : <https://docs.mopidy.com/en/latest/running/service/>

    - Die mopidy config von `/home/pi/.config/mopidy/mopidy.conf` nach `/etc/mopidy/mopidy.conf` mit `sudo cp /home/pi/.config/mopidy/mopidy.conf /etc/mopidy/mopidy.conf` verschieben, da beim autostart der service unter `mopidy` und nicht unter dem user `pi` gestartet wird.
    - Den `mopidy` User zu der video Gruppe hinzufügen mit `sudo usermod -aG video mopidy`, falls nicht schon vorher geschehen.
    - mopidy zum autostart hinzufuegen mit `sudo systemctl enable mopidy`
    - Überpruefen mit `sudo systemctl status mopidy`
    - Den PI rebooten und erneut mit `sudo systemctl status mopidy` prüfen, ob der service läuft.
    - Mit `sudo mopidyctl config` prüfen, ob die richtige Konfiguration geladen wurde (Spotify user und password vorhanden)

8. Den Audio-output für den `mopidy` User ändern, da dieser im defaultfall Ton über HDMI und nicht über Klinke abspielt.
    - Default auf den Kopfhörereingang setzen wie hier beschrieben: <https://www.alsa-project.org/wiki/Setting_the_default_device>
    - Da diese Datei momentan von Rasbian noch bei reboot gelöscht wird (Bug? <https://www.raspberrypi.org/forums/viewtopic.php?t=295008>), muss diese auf immutable gesetzt werden. `sudo chattr +i /etc/asound.conf`
    - Falls diese Datei ein Symlink ist, und dieser nicht auf immutable gesetzt werden kann, muss dieser mit `sudo rm -i /etc/asound.conf` aufgehoben, die Datei neu erstellt und danach wieder mit `sudo chattr +i /etc/asound.conf` auf immutable gesetzt werden.
    - Mit `sudo -u mopidy aplay /usr/share/sounds/alsa/Front_Center.wav` sollte der Ton nun auch unter dem `mopidy` User aus dem Klinkenstecker und mehr aus dem Monitor kommen, falls einer während des Vorgangs angeschlossen wurde.
    - Reboot

9. Mit `python main.py` und der `soundConfig.yaml` auf `spotify` kann nach dem ausführen mit `m.send("happy")` getestet werden, ob der Spotify-Player wie gewünscht funktioniert.

## Webcam-Emotion-Detection

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
python main.py
```
