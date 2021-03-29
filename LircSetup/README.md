# LircSetup

In diesem Beispiel wird ein VS1838b Infrarot-Empfänger verwendet.
**Aufbau**
<img src="images/RaspberryPi_B+_Pins.png" width="300"><br>
<img src="images/RaspberryPi_B+_Setup.jpg" width="300"><br>
Der Empfänger ist über einen Controller an Pin 2,6 und 12 verbunden.

**Lirc installieren**
`$ sudo apt-get update`
`$ sudo apt-get install lirc`

**Folgende zeilen zu /etc/modules hinzufügen**
> lirc_dev
> gpio_ir gpio_in_pin=18 gpio_out_pin=17

Das virtual environment aktivieren

`source <enviroment_name>/bin/activate`

Der Name des environment sollte nun am Anfang der Kommandozeile stehen

`<enviroment_name> $`

Das virtual environment deaktivieren:

`deactivate`

## Die für das Programm notwendigen Packages installieren

`pip install -r requirements.txt`

## Aktualisieren der `requirements.txt`

Beim Hinzufügen von neuen Packages in das venv muss die requirements.txt aktualisiert werden

`pip freeze -l > requirements.txt # or --local instead of -l`
## Anforderungen

### Gesichtserkennung

Über die Kamera des PI’s soll die Umgebung laufend gefilmt werden. Dabei soll in dem Kamerabild ein Gesicht gesucht werden, um dessen Emotion zu erkennen.
Bei der Emotion handelt  es sich um ein Element aus einer vordefinierten Menge. Diese Emotion wird an ein weiteres Modul weitergereicht, welches sich um die Musik und Lichtstimmung im Raum kümmert.
Als zusätzliches Feature wäre denkbar ein Foto über eine Webseite hochzuladen, welche aus dem lokalen Netz heraus erreichbar wäre. Dieses könnte dann ebenfalls von dem Gesichtserkennungs-Modul verarbeitet werden.

### Musik

Wurde eine Stimmung erkannt, soll der PI aus einer vordefinierten Playlist einen zur Stimmung passenden Song auswählen und abspielen (über den internen Aux-Anschluss).
Zusätzlich wäre denkbar diese Songs über eine Python API aus Spotify Playlists, welche zu jeder Stimmung zugeordnet sind, abzuspielen.

### Licht

Das Licht wird an die erkannte Stimmung angepasst. Jede Stimmung bekommt dabei eine Farbe zugeordnet. Eine Erweiterung wären dann unterschiedliche Lichtprogramme, welche je nach erkannter Emotion eine passende Stimmung im Raum verbreiten sollen.

### Webserver (optional)

Bei genügend Zeit könnte das PI noch mit einem Webserver verbunden werden. Über diesen werden dann Bilder an das PI gesendet, in denen dann Emotionen erkannt werden können.
Dabei könnte der Ablauf folgendermaßen aussehen:
-Nimmt ein Bild, welches hochgeladen wird entgegen
-Speichert es lokal auf dem PI
-Übergibt es an das Gesichtserkennungs-Skript, welches darauf ein Gesicht sucht und (falls vorhanden) versucht eine Emotion zu erkennen
