# Installationsanleitung

## Benötigte Komponenten
- Raspberry Pi 3B bzw. 3B+
- Kameramodul für den Raspberry Pi
- Terminal Block Adapter
   - DC 2,5 x 5,5mm Buchse
- Netzteil
   - in dem aktuellen Setup wurde ein Netzteil mit 5 Volt und 10 Ampere verwendet
- LED-Strip
    - IC-Typen WS2801
    - +5V Versorgung
    - 28 Watt
    - 3 Meter mit 32 LEDs pro Meter
- Arduino Uno (Rev 3)
- Kabel zur Stromversorgung und Datenübertragung zwischen den Komponenten
   > TODO: Kabel aufschreiben

- Lautsprecher/Boxen
   - 16 Watt
   - Kabelgebunden
     - mit Stromversorgung per USB und Anschluss über AUX
   > TODO Stromversorung nochmal abklären
   
- Display zur Bedienung
   - 1,5 Watt 
   - Displaygröße: 5 Zoll
   - Auflösung: 800x480
   - Optional Touchdisplay

- Infrarot-Fernbedienung
  > TODO Angaben (Link) fehlt
 
- USB Kabel zur Verbindung mit dem Arduino
   - USB-A auf USB-B

- HDMI-zu-HDMI-Kabel für das Display

> TODO: Leistungsangaben (Watt und so) kontrollieren

## PI aufsetzen und Grundeinrichtung vornehmen

1. Herunterladen und erstellen des Images mit: <https://www.raspberrypi.org/software/>

2. Auf dem PI SSH aktivieren und mit diesem nach dieser Anleitung über SSH verbinden.
<https://blog.sebastian-martens.de/development/setup-raspberry-pi-without-external-monitor-and-keyboards/>
Alternativ kann die Einrichtung direkt auf dem PI vorgenommen werden.

3. Mit VNC auf den PI verbinden und die Locale einstellen
   > TODO: genauer formulieren

4. Passwort ändern, da Defaultpasswort mit einem geöffnetem SSH und VNC Zugang unsicher ist.

5. System aktualisieren
   ```
   sudo apt update
   ```

   gefolgt von

   ```
   sudo apt upgrade
   ```

6. Raspberry PI neu starten
   ```
   sudo reboot
   ```

7. **Konfiguration öffnen**
   - `sudo raspi-config`
   - unter `System Options (S) -> Audio (S2)` auswählen und den Audio Output auf `“1 Headphones”` stellen
   - Kamera des PI's aktivieren

8. Repository clonen mit `git clone https://github.com/Pfanfel/mood_fh.git`
   > TODO oder die final URL

9. **Virtuelle Umgebung im aktuellen Verzeichnis erstellen:**

    - Arch:
    ```
	python -m venv <enviroment_name>
	```

    - Ubuntu:

        ```
		sudo apt install python3-pip      # falls pip nicht vorhanden
        pip3 install virtualenv           # falls virtualenv nicht vorhanden

        python3 -m virtualenv <enviroment_name>
		```
    - Virtuelle Umgebung aktivieren:
	 ```
	 source <enviroment_name>/bin/activate
	 ```

    - Der Name des environment sollte nun am Anfang der Kommandozeile stehen `<enviroment_name> $`

    - Zum Deaktivieren des virtual environment kann der Befehl `deactivate` verwendet werden.

10. Die notwendigen Packages können mit 
    ```
	pip install -r requirements.txt
	``` 
	installieren werden.

## Installation des Sound-Moduls

> TODO: Fehler kontrollieren

- pygame benötigt den zusätzlichen mixter
  - Skript ausführbar machen mittels `chmod +x setup.sh`
  - mit `./setup.sh`kann dieses ausgeführt werden

> TODO: es gibt keinen Sound-Ordner mehr
- Mit `python main.py` im Sound Ordner kann das abspielen von lokaler Musik mit dem pygame-player getestet werden. (Player sollte dafür in der `soundConfig.yaml` auf pygame gesetzt sein)

### [Optional] Einrichten von Mopedy, um das Abspielen von Musik über Spotify zu ermöglichen. 

> Hierbei wird ein **Spotify Permium Account** benötigt

1. Mopedy nach der folgenden Anleitung installieren: <https://docs.mopidy.com/en/latest/installation/raspberrypi/>
und das Skript `mopidy.sh` ausführen (ggf. mit `chmod +x` ausführbar machen)
> TODO: Satzbau?

 Damit werden die Repositories von Mopidy hinzugefügt und mopidy die spotify und die mpd Extention installiert.

2. mopidy in die video Gruppe hinzufügen `sudo adduser mopidy video`

3. Zum Erstellen der Konfigutationsdatei muss `mopidy` einmal von der Kommandozeile aus ausgeführt werden

4. Konfiguration anpassen:
   - Die Konfigurationsdatei unter `/home/pi/.config/mopidy/mopidy.conf` öffen
   -  `output = alsasink` unter `[audio]` auskommentieren/einfügen, damit nicht der HDMI Ausgang für den Sound genutzt wird.

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

**Programm starten:**

```
python main.py
```

> TODO: Readme zur Fernbedienung??



## Einrichtung des Lichtmoduls

### Einrichtung des Arduino
- Download der [FastLED-Library](http://https://github.com/FastLED/FastLED "FastLED-Library") zur Steuerung des LED-Strips

- Installation der Arduino IDE 
    - [Installation unter Windows](https://www.arduino.cc/en/guide/windows "Installation unter Windows")
    - [Installation unter Linux](https://www.arduino.cc/en/Guide/Linux "Installation unter Linux")

- Einbinden der Bibliothek:
    - `Sketch -> Bibliothek einbinden -> .ZIP Bibliothek hinzufügen`

- Unter `Werkzeuge -> Board` muss der Arduino Uno ausgewählt sein
- Unter `Werkzeuge -> Port` muss der passende Port ausgewählt sein (meist /dev/ttyACM0 unter Linux)
- Hochladen

Die Installation der IDE kann entweder auf einem externen PC erfolgen, in dem der Arduino per USB verbunden wird oder direkt auf dem Raspberry Pi (ebenfalls über Verbindung mit USB)

### Hardware

```
Hier soll das Bild hin z.B.
```

- Arduino Pin 13 an CI (Steueruhrdatensignaleingang bzw. Clock) des LED-Strip (Grün)
- Arduino Pin 11 an DI (Steuerdatensignaleingang bzw. Data) des LED-Strip (Blau)
- 5V Versorgung des Arduino per USB-Schnittstelle des Raspberry Pi
- Ground vom Arduino zum Netzteil
- von Pi:
    - Ground (Pin 6) zum Netzteil (Weiß)
    - 5V (Pin 2) zum Netzteil (Rot)
- vom LED-Strip
    - Ground zum Netzteil (Weiß oder Schwarz)
    - 5V zum Netzteil (Rot)

### Installation

> Wichtig: Kontrollieren, ob ACM stimmt (auf PI Seite)
