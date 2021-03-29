# Installation vom mopidy (NOCH IN ARBEIT NOCHT NICHT AUF EINEM FRISCHEN PI GESTESTET)

1. `mopidy.sh` script ausführen (ggf. mit `chmod +x` ausführbar machen)

2. Konfiguration vornehmen siehe: https://github.com/mopidy/mopidy-spotify#configuration
    * Details zur Konfiguration: https://docs.mopidy.com/en/release-0.19/config/
    * Zum erstellen der Konfigutationsdatei muss `mopidy` einmal von der Kommandozeile ausgefuehrt werden
    * In der `/home/pi/.config/mopidy/mopidy.conf` den Username und das Passwort seines Spotify-Premium(!) Accounts eintragen
    * Die Authentifizierung wie hier beschrieben durchfüheren (Pop-Up öffen, bestätigen, id und secret  in die mopidy.conf eintragen): https://mopidy.com/ext/spotify/#authentication
    
3. Mopidy beim hochfahren des PIs automatisch starten lassen
    * mopidy zum autostart hinzufuegen mit `sudo dpkg-reconfigure mopidy`
    * Die mopidy config von `/home/pi/.config/mopidy/mopidy.conf` nach `/etc/mopidy/mopidy.conf` verschieben, da beim autostart der service unter `root` und nicht unter dem user `pi` gestartet wird.
    * Den `mopidy` User zu der video Gruppe hinzufügen mit `usermod -aG video mopidy`
    * Überpruefen mit `sudo service mopidy status`
    * Den PI rebooten und erneut mit `sudo service mopidy status` prüfen, ob der service läuft.
    * Mit `sudo su` als root anmelden
    * Mit 'mopidy config' prüfen, ob die richtige Konfiguration geladen wurde (Spotify user und password vorhanden)