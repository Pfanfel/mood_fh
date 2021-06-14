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

1. Herunterladen und erstellen des Images mit: <https://www.raspberrypi.org/software/>

2. [Optional, falls kein Display vorhanden ist] Auf dem Pi SSH aktivieren und mit diesem nach dieser Anleitung über SSH verbinden.
<https://blog.sebastian-martens.de/development/setup-raspberry-pi-without-external-monitor-and-keyboards/>
Alternativ kann die Einrichtung direkt auf dem Pi vorgenommen werden.

4. Passwort ändern.

5. System aktualisieren.
   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Raspberry Pi neu starten.
   ```
   sudo reboot
   ```

7. Konfiguration öffnen.
   - `sudo raspi-config`
   - unter `System Options (S) -> Audio (S2)` auswählen und den Audio Output auf `“1 Headphones”` stellen
   - Kamera des Pi's aktivieren

8. Repository clonen mit `git clone https://github.com/Pfanfel/mood_fh.git`

9. Virtuelle Umgebung im aktuellen Verzeichnis erstellen:

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

    - Der Name der Umgebung sollte nun am Anfang der Kommandozeile stehen 
	 ```
     <enviroment_name> $
	 ```

    - Zum Deaktivieren der virtuellen Umgebung kann dieser Befehl verwendet werden:
	 ```
     $ deactivate
	 ```

10. Die notwendigen Packages können mit 
    ```
	pip install -r requirements.txt
	``` 
	installiert werden.

## Installation des Sound-Moduls

> TODO: Fehler kontrollieren

- Installation notwendiger Librarys
  - Skript ausführbar machen
    ```
    $ chmod +x setup.sh
    ```
  - Skript ausführen
    ```
    $ ./setup.sh
    ```
    Falls nach der Installation Probleme bei OpenCV auftreten, kann auch dieser [guide](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/) benutzt werden.

### [Optional] Einrichten von Mopidy, um das Abspielen von Musik über Spotify zu ermöglichen. 

> Hierbei wird ein **Spotify Permium Account** benötigt

1. Mopidy nach der folgenden Anleitung installieren: <https://docs.mopidy.com/en/latest/installation/raspberrypi/>.

2. Mopidy in die video Gruppe hinzufügen
    ```
    $ sudo adduser mopidy video
    ```

3. Zum Erstellen der Konfigutationsdatei muss Mopidy einmal von der Kommandozeile aus ausgeführt werden
    ```
    $ mopidy
    ```

4. Konfiguration anpassen:
   - Die Konfigurationsdatei unter `/home/pi/.config/mopidy/mopidy.conf` öffen
   -  `output = alsasink` unter `[audio]` einkommentieren/einfügen, damit nicht der HDMI Ausgang für den Sound genutzt wird.

5. Konfiguration vom Spotify vornehmen siehe: <https://github.com/mopidy/mopidy-spotify#configuration>
    - Details zur Konfiguration: <https://docs.mopidy.com/en/release-0.19/config/>
    - In der `/home/pi/.config/mopidy/mopidy.conf` den Username und das Passwort seines Spotify-Premium(!) Accounts eintragen
    - Die Authentifizierung wie hier beschrieben durchfüheren (Pop-Up öffen, bestätigen, id und secret  in die mopidy.conf eintragen): <https://mopidy.com/ext/spotify/#authentication>
    - Die auskommentieren Zeilen unter `[spotify]` einkommentieren

6. Mit `mopidy` den Server von der Kommandozeile aus starten und prüfen, ob der Login geklappt hat.
Im Debug output sollte die Zeile : `Logged into Spotify Web API as XYZ` erscheinen.

7. Mopidy beim Hochfahren des Pi's automatisch starten lassen. Genau beschrieben unter: <https://docs.mopidy.com/en/latest/running/service/>

    - Die mopidy config von `/home/pi/.config/mopidy/mopidy.conf` nach `/etc/mopidy/mopidy.conf` mit `sudo cp /home/pi/.config/mopidy/mopidy.conf /etc/mopidy/mopidy.conf` verschieben, da beim Autostart der Service unter `mopidy` und nicht unter dem User `pi` gestartet wird.
    - Den `mopidy` User zu der "video"-Gruppe hinzufügen mit `sudo usermod -aG video mopidy`, falls nicht schon vorher geschehen.
    - mopidy zum Autostart hinzufügen mit `sudo systemctl enable mopidy`
    - Überprüfen mit `sudo systemctl status mopidy`
    - Den Pi rebooten und erneut mit `sudo systemctl status mopidy` prüfen, ob der Service läuft.
    - Mit `sudo mopidyctl config` prüfen, ob die richtige Konfiguration geladen wurde (Spotify User und Password vorhanden)

8. Den Audio-Output für den `mopidy` User ändern, da dieser im Defaultfall Ton über HDMI und nicht über Klinke abspielt.
    - Default auf den Kopfhörereingang setzen wie hier beschrieben: <https://www.alsa-project.org/wiki/Setting_the_default_device>
    - Da diese Datei momentan von Raspbian noch bei reboot gelöscht wird (siehe: <https://www.raspberrypi.org/forums/viewtopic.php?t=295008>), muss diese auf immutable gesetzt werden. `sudo chattr +i /etc/asound.conf`
    - Falls diese Datei ein Symlink ist, und dieser nicht auf immutable gesetzt werden kann, muss dieser mit `sudo rm -i /etc/asound.conf` aufgehoben, die Datei neu erstellt und danach wieder mit `sudo chattr +i /etc/asound.conf` auf immutable gesetzt werden.
    - Mit dem Befehl `sudo -u mopidy aplay /usr/share/sounds/alsa/Front_Center.wav` kann getestet werden, ob der Ton auch unter dem `mopidy` User aus dem Klinkenstecker und nicht mehr aus dem Monitor kommt.
    - Reboot

## Webcam-Emotion-Detection

**Folgende Zeile in _/boot/config.txt_ ändern oder anhängen:**
```
dtoverlay=gpio-ir,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up
```
**Wichtig:** Datenkabel des IR-Moduls muss mit dem Pin GPIO18 verbunden werden!

**Die _key.conf_ nach _/etc/init.d_ verschieben:**
```
$ sudo mv /Pfad/Zum/Programm/key.conf /etc/init.d
```
>TODO: Foto mit Mappings

**Folgende Zeile an das Ende der Crontab-Datei hinzufügen:**
```
$ sudo crontab -e
```
```
@reboot sudo ir-keytable -p nec
@reboot sudo ir-keytable -c -w /etc/init.d/key.conf
```

## Einrichtung des Lichtmoduls

### Einrichtung des Arduino
- Download der [FastLED-Library](http://https://github.com/FastLED/FastLED "FastLED-Library") zur Steuerung des LED-Strips

- Installation der Arduino IDE 
    - [Installation unter Windows](https://www.arduino.cc/en/guide/windows "Installation unter Windows")
    - [Installation unter Linux](https://www.arduino.cc/en/Guide/Linux "Installation unter Linux")
- _light.ino_ aus dem "arduino"-Verzeichnis mit der Arduino IDE öffnen
- Einbinden der Bibliothek:
    - `Sketch -> Bibliothek einbinden -> .ZIP Bibliothek hinzufügen`

- Unter `Werkzeuge -> Board` muss der Arduino Uno ausgewählt sein
- Unter `Werkzeuge -> Port` muss der passende Port ausgewählt sein (meist /dev/ttyACM0 unter Linux)
- Hochladen auswählen

Die Installation der IDE kann entweder auf einem externen PC erfolgen, in dem der Arduino per USB verbunden wird oder direkt auf dem Raspberry Pi (ebenfalls über Verbindung mit USB).

### Hardware

```
TODO: Hier soll das Bild hin z.B.
```
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
