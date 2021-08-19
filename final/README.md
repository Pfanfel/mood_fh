# Installationsanleitung

## Benötigte Komponenten
- Raspberry Pi 3B bzw. 3B+
    - 5V, 2.6A, 13W
---
- Arduino Uno (Rev 3)
    - 5V, 0.015A, 0.075W
---
- LED-Strip

    - IC-Typen WS2801
    - 3 Meter mit 32 LEDs pro Meter
    - 5V, 5.6A, 28W
- Kameramodul mit Flachbandkabel für den Raspberry Pi
---
- Infrarot Kit Fernbedienung mit Empfänger
    - VS1838B-Diode
    - 5V, 0.0015A, 0.005W
---
- Lautsprecher/Boxen
    - Kabelgebunden
        - Stromversorgung per USB Pinheader Buchse am Netzteil
        - Audioanschluss über AUX am Raspberry Pi
    - 5V, 3.2A, 16W
---
- Netzteil
    - aktuelles Setup: 5V, 10A
    - **Anmerkung:** Benötigte Stromstärke beträgt mehr als 10A
        - Empfehlung: Netzteil mit 15A, damit Lautsprecher kein extra Netzteil benötigen
---
- Terminal Block Adapter
    - DC 2,5 x 5,5mm Buchse
---
- Kabel zur Stromversorgung und Datenübertragung zwischen den Komponenten
    - z.B. Jumper Kabel
---
- USB Kabel zur Verbindung mit dem Arduino
    - USB-A auf USB-B
---
- Display zur Bedienung
    - z.B.
    - Displaygröße: 5 Zoll
    - Auflösung: 800x480
    - Optional Touchdisplay
    - 5V, 0.3A, 1.5W
---
- HDMI-zu-HDMI-Kabel für das Display
---
- Leistungsangaben
    - 5V, 11.7165A, 58.6W
    - >TODO: Gemessen: ...

## Pi aufsetzen und Grundeinrichtung vornehmen

1. Herunterladen und erstellen des <a href="https://www.raspberrypi.org/software/" target="_blank">Images</a>.

2. [Optional, falls kein Display vorhanden ist] <a href="https://blog.sebastian-martens.de/development/setup-raspberry-pi-without-external-monitor-and-keyboards/" target="_blank">Aktivieren</a> von SSH.  
Alternativ kann die Einrichtung direkt auf dem Pi vorgenommen werden.

4. Passwort ändern.

5. System aktualisieren.
   ```
   $ sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Raspberry Pi neu starten.
   ```
   $ sudo reboot
   ```

7. Einstellungen in der Konfiguration.
   ```
   $ sudo raspi-config
   ```
   - `System Options (S) -> Audio (S2)`  
   -> Audio-Output = `“1 Headphones”`
   - Kamera des Pi's aktivieren

8. Repository clonen.
    ```
    $ git clone https://github.com/Pfanfel/mood_fh.git
    ```

9. Virtuelle Umgebung im aktuellen Verzeichnis erstellen.

    - **Arch:**
        ```
	    $ python -m venv <enviroment_name>
	    ```
    - **Ubuntu:**
        ```
	    $ sudo apt install python3-pip      # falls pip nicht vorhanden
        $ pip3 install virtualenv           # falls virtualenv nicht vorhanden

        $ python3 -m virtualenv <enviroment_name>
	    ```
    - Virtuelle Umgebung aktivieren.
	    ```
	    $ source <enviroment_name>/bin/activate
	    ```
        Der Name der Umgebung sollte nun am Anfang der Kommandozeile stehen.
	    ```
        <enviroment_name> $
	    ```

    - Folgender Befehl dient zum Deaktivieren der virtuellen Umgebung.
	    ```
        <enviroment_name> $ deactivate
	    ```

10. Die notwendigen Packages installieren.
    ```
	<enviroment_name> $ pip install -r requirements.txt
	```
## Installation des Sound-Moduls und OpenCV
  - Skript ausführbar machen
    ```
    $ chmod +x setup.sh
    ```
  - Skript ausführen
    ```
    $ ./setup.sh
    ```
    Falls nach der Installation Probleme bei OpenCV auftreten, kann auch dieser <a href="https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/" target="_blank">guide</a> benutzt werden.

## [Optional] Einrichten von Mopidy, um das Abspielen von Musik über Spotify zu ermöglichen.
> Hierbei wird ein **Spotify Permium Account** benötigt!
1. Mopidy <a href="https://docs.mopidy.com/en/latest/installation/raspberrypi/" target="_blank">installieren</a>.

2. Mopidy in die "video"-Gruppe hinzufügen.
    ```
    $ sudo adduser mopidy video
    ```
3. Mopidy von der Kommandozeile aus ausführen um _mobidy.conf_ zu erstellen.
    ```
    $ mopidy
    ```
4. Folgende Zeile in _/home/pi/.config/mopidy/mopidy.conf_ anpassen.
    - Unter `[audio]`:  
    `output = alsasink` einkommentieren/einfügen, damit der HDMI-Ausgang nicht genutzt wird.
5. <a href="https://github.com/mopidy/mopidy-spotify#configuration" target="_blank">Konfiguration</a> von Spotify.
    - <a href="https://docs.mopidy.com/en/release-0.19/config/" target="_blank">Details</a> zur Konfiguration
    - In _/home/pi/.config/mopidy/mopidy.conf_ den Username und das Passwort des **Spotify-Premium** Accounts eintragen
    - <a href="https://mopidy.com/ext/spotify/#authentication" target="_blank">Authentifizierung</a> durchfüheren 
    - Die auskommentieren Zeilen unter `[spotify]` einkommentieren

6. Den Server starten und prüfen, ob der Login geklappt hat.
    ```
    $ mopidy
    ```
    Im Debug-Output sollte die Zeile : `Logged into Spotify Web API as XYZ` erscheinen.
7. Mopidy <a href="https://docs.mopidy.com/en/latest/running/service/" target="_blank">on boot</a> starten lassen.
    - Die Datei _mopidy-conf_ verschieben.
        ```
        $ sudo cp /home/pi/.config/mopidy/mopidy.conf /etc/mopidy/mopidy.conf
        ```
        Da beim Autostart der Service unter `mopidy` und nicht unter dem User `pi` gestartet wird.
    - Den Mopidy-User zur "video"-Gruppe hinzufügen, falls nicht schon vorher geschehen.
        ```
        $ sudo usermod -aG video mopidy
        ```
    - Mopidy zum Autostart hinzufügen.
        ```
        $ sudo systemctl enable mopidy
        ```
    - Prüfen ob Mobidy zum Autostart hinzugefügt wurde.
        ```
        $ sudo systemctl status mopidy
        ```
    - Den Pi rebooten und erneut mit vorherigem Aufruf prüfen.
    - Prüfen ob richtige Konfigurationsdatei geladen wurde.
        ```
        $ sudo mopidyctl config
        ```

8. Den Audio-Output für den Mopidy-User ändern, da dieser im Defaultfall Ton über HDMI und nicht über Klinke abspielt.
    - Default auf den Kopfhörereingang <a href="https://www.alsa-project.org/wiki/Setting_the_default_device" target="_blank">setzen</a>
    - Da diese Datei momentan von Raspbian noch beim rebooten gelöscht wird (siehe <a href="https://www.raspberrypi.org/forums/viewtopic.php?t=295008" target="_blank">hier</a>), muss diese auf immutable gesetzt werden.
        ```
        $ sudo chattr +i /etc/asound.conf
        ```
    - Falls diese Datei ein Symlink ist, und nicht auf immutable gesetzt werden kann, muss dieser aufgehoben werden.
        ```
        $ sudo rm -i /etc/asound.conf
        ```
        Anschließend müssen die beiden ersten Schritte wiederholt werden.
    - Testen, ob der Ton unter dem Mopidy-User über die Klinke kommt.
        ```
        $ sudo -u mopidy aplay /usr/share/sounds/alsa/Front_Center.wav
        ```
    - Reboot
        ```
        $ sudo reboot
        ```

## Webcam-Emotion-Detection

1. Folgende Zeile in _/boot/config.txt_ ändern oder anhängen:
    ```
    dtoverlay=gpio-ir,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up
    ```
    **Wichtig:** Datenkabel des IR-Moduls muss mit dem Pin GPIO18 verbunden werden!
2. Die _key.conf_ nach _/etc/init.d_ verschieben:
    ```
    $ sudo mv /Pfad/Zum/Programm/key.conf /etc/init.d
    ```
    <img src="images\key_mapping.jpg" width="350">
3. Folgende Zeile an das Ende der Crontab-Datei hinzufügen:
    ```
    $ sudo crontab -e
    ```
    ```
    @reboot sudo ir-keytable -p nec
    @reboot sudo ir-keytable -c -w /etc/init.d/key.conf
    ```
## Einrichtung des Lichtmoduls

### Einrichtung des Arduino

- Zunächst muss der Arduino mit dem Raspberry Pi per USB-A Kabel verbunden werden. Dieser erhält die Stromversorgung über die USB-Schnittstelle.

- Download der <a href="https://github.com/FastLED/FastLED" target="_blank">FastLED-Library</a> zur Steuerung des LED-Strips

- Installation der Arduino IDE 
    - <a href="https://www.arduino.cc/en/guide/windows" target="_blank">Installation unter Windows</a>
    - <a href="https://www.arduino.cc/en/Guide/Linux" target="_blank">Installation unter Linux</a>
- _light.ino_ aus dem "arduino"-Verzeichnis mit der Arduino IDE öffnen
- Einbinden der Bibliothek:
    - `Sketch -> Bibliothek einbinden -> .ZIP Bibliothek hinzufügen`

- Unter `Werkzeuge -> Board` muss der Arduino Uno ausgewählt sein
- Unter `Werkzeuge -> Port` muss der passende Port ausgewählt sein (meist /dev/ttyACM0 unter Linux)
- Hochladen auswählen

Alternativ kann die Installation der IDE auch auf einem externen PC erfolgen, in dem der Arduino per USB verbunden wird. 
Der Arduino muss anschließend wie beschrieben mit dem Raspberry Pi verbunden werden.

### Hardware

Aufbau der Komponenten
<img src="images\Mood_FH_Fritzing.jpg" width="500">


>TODO: durch neue Kabelage evtl. überarbeiten
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

> Wichtig: Kontrollieren, ob ACM stimmt (auf Pi Seite)

## [Optional] Einrichten eins Systemd-Services, um das Programm on Boot im Hintergrund starten zu lassen.
Dieses <a href="https://github.com/torfsen/python-systemd-tutorial" target="_blank">Tutorial</a> wurde bei dem Projekt verwendet.
1. Erstellen einer _servicename.service_-Datei in _~/.config/systemd/user/_, sodass Pfad = _~/.config/systemd/user/servicename.service_ ist.
2. Folgenden Inhalt in die Datei einfügen:
    ```
    [Unit]
    Description=Description of the service

    [Service]
    # Command to execute when the service is started
    ExecStart=/usr/bin/python path/to/your/main.py
    Restart=on-failure

    [Install]
    # Command to start the service on boot
    WantedBy=default.target
    ```
Nun wird Systemd den Service finden.
1. Finden des Services:
    ```
    $ systemctl --user list-unit-files | grep servicename
    ```
2. Starten des Services:
    ```
    $ systemctl --user start servicename
    ```
    Eventuell muss vorher der _user-daemon_ neu geladen werden.
    ```
    $ systemctl --user daemon-reload
    ```
3. Um zu prüfen, ob der Service läuft:
    ```
    $ systemctl --user status servicename
    ```
4. Stoppen des Services:
    ```
    $ systemctl --user stop servicename
    ```
5. Aktivieren des Services, um ihn beim Booten automatisch zu starten:
    ```
    $ systemctl --user enable servicename
    ```
6. Um Autostart zu deaktivieren:
    ```
    $ systemctl --user disable servicename
    ```
7. Um zu prüfen, ob der Service aktiviert ist:
    ```
    $ systemctl --user list-unit-files | grep servicename
    ```

## Known Bugs.
1. Beim Starten des PI's muss einmal die Emotionserkennung gestartet werden, sodass das Programm abstürzt und neu startet. Dies hängt eventuell mit OpenCV zusammen. Allerdings wurde hier keine Lösung gefunden.
2. Wenn Emotionen mit gleicher Häufigkeit erkannt werden stürzt das Programm ab.