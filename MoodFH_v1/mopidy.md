# Installation vom mopidy für wiedergabe über Spotify. 

1. Mopedy nach der folgenden Anleitung installieren: https://docs.mopidy.com/en/latest/installation/raspberrypi/
`mopidy.sh` script ausführen (ggf. mit `chmod +x` ausführbar machen)
Damit werden die Repos von Mopidy hinzugefügt und mopidy die spotify und die mpd Extention installiert.

2. mopidy in die video Gruppe hinzufügen `sudo adduser mopidy video`

3. Zum erstellen der Konfigutationsdatei muss `mopidy` einmal von der Kommandozeile ausgefuehrt werden

4. Die Konfigurationsdatei unter `/home/pi/.config/mopidy/mopidy.conf` öffen und  
`output = alsasink` unter `[audio]` auskommentieren/einfügen, damit nicht der HDMI Ausgang für den Sound genutzt wird.

5. Konfiguration vom Spotify vornehmen siehe: https://github.com/mopidy/mopidy-spotify#configuration
    * Details zur Konfiguration: https://docs.mopidy.com/en/release-0.19/config/
    * In der `/home/pi/.config/mopidy/mopidy.conf` den Username und das Passwort seines Spotify-Premium(!) Accounts eintragen
    * Die Authentifizierung wie hier beschrieben durchfüheren (Pop-Up öffen, bestätigen, id und secret  in die mopidy.conf eintragen): https://mopidy.com/ext/spotify/#authentication
    * Die auskommentieren Zeilen unter `[spotify]` einkommentieren

6. Mit `mopidy` den Server von der Kommandozeile aus straten und prüfen, ob der Login geklappt hat.
Im Debug output sollte die Zeile : `Logged into Spotify Web API as XYZ` erscheinen.
    
7. Mopidy beim hochfahren des PIs automatisch starten lassen. Genau beschieben unter : https://docs.mopidy.com/en/latest/running/service/
    
    * Die mopidy config von `/home/pi/.config/mopidy/mopidy.conf` nach `/etc/mopidy/mopidy.conf` mit `sudo cp /home/pi/.config/mopidy/mopidy.conf /etc/mopidy/mopidy.conf` verschieben, da beim autostart der service unter `mopidy` und nicht unter dem user `pi` gestartet wird.
    * Den `mopidy` User zu der video Gruppe hinzufügen mit `sudo usermod -aG video mopidy`, falls nicht schon vorher geschehen.
    * mopidy zum autostart hinzufuegen mit `sudo systemctl enable mopidy`
    * Überpruefen mit `sudo systemctl status mopidy`
    * Den PI rebooten und erneut mit `sudo systemctl status mopidy` prüfen, ob der service läuft.
    * Mit `sudo mopidyctl config` prüfen, ob die richtige Konfiguration geladen wurde (Spotify user und password vorhanden)

8. Den Audio-output für den `mopidy` User ändern, da dieser im defaultfall Ton über HDMI und nicht über Klinke abspielt.
    * Default auf den Kopfhörereingang setzen : https://www.alsa-project.org/wiki/Setting_the_default_device
    * Da diese Datei momentan von Rasbian noch bei reboot gelöscht wird (Bug? https://www.raspberrypi.org/forums/viewtopic.php?t=295008), muss diese auf immutable gesetzt werden. `sudo chattr +i /etc/asound.conf`
    * Falls diese Datei ein Symlink ist, und dieser nicht auf immutable gesetzt werden kann, muss dieser mit `sudo rm -i /etc/asound.conf` aufgehoben, die Datei neu erstellt und danach wieder mit `sudo chattr +i /etc/asound.conf` auf immutable gesetzt werden.
    * Mit `sudo -u mopidy aplay /usr/share/sounds/alsa/Front_Center.wav` sollte der Ton nun auch unter dem `mopidy` User aus dem Klinkenstecker und mehr garnicht oder aus dem Monitor kommen, falls einer angeschlossen wurde.
    * Reboot

9. Mit `python mainTest.py` und der `soundConfig.yaml` auf `spotify` kann nach dem ausführen mit `m.send("happy")` getestet werden, ob der Spotify-Player wie gewünscht funktioniert. 
