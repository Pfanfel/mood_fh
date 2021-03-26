# Installation vom mopidy

1. `mopidy.sh` script ausführen (ggf. mit `chmod +x` ausführbar machen)
2. Konfiguration vornehmen siehe: https://github.com/mopidy/mopidy-spotify#configuration
    * Details zur Konfiguration: https://docs.mopidy.com/en/release-0.19/config/
    * Zum erstellen der Konfigutationsdatei muss `mopidy` einmal so ausgefuehrt werden
    * In der `/home/pi/.config/mopidy/mopidy.conf` den Username und das Passwort seines Spotify-Premium(!) Accounts eintragen
    * Die Authentifizierung wie hier beschrieben durchfüheren (Pop-Up öffen, bestätigen, id und secret eintragen): https://mopidy.com/ext/spotify/#authentication
    * requrements.txt aktualisieren um mpd nutzen zu können, um aus python heraus mit dem Server kommunizieren zu können
    * `mopidy` zum autostart hinzufuegen mit `sudo dpkg-reconfigure mopidy`
    * Überpruefen mit `sudo service mopidy status`