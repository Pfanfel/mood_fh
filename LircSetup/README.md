# LircSetup  
  
  
In diesem Beispiel wird ein VS1838b Infrarot-Empfänger verwendet.  
  
**Aufbau:**  
  
<br>
<img src="images/RaspberryPi_B+_Pins.png" width="500">
<img src="images/RaspberryPi_B+_Setup.jpg" width="300"><br>
  
Der Empfänger ist über einen Controller an Pin 2,6 und 12 verbunden.  
  
**Lirc installieren.**  
`$ sudo apt-get update`  
`$ sudo apt-get install lirc`  
  
**Folgende Zeilen zu */etc/modules* hinzufügen.**  
> lirc_dev  
> gpio_ir gpio_in_pin=18 gpio_out_pin=17  
  
**Folgende Zeilen zu */etc/lirc/hardware.conf* hinzufügen.**  
> LIRCD_ARGS="--uinput --listen"  
> LOAD_MODULES=true  
> DRIVER="default"  
> DEVICE="/dev/lirc0"  
> MODULES="lirc_rpi"  
> LIRCD_CONF=""  
> LIRCMD_CONF=""  
  
**Folgende Zeile in */boot/config.txt* ändern.**  
> dtoverlay=gpio-ir,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up  
  
**Folgende Zeilen in */boot/config.txt* ändern.**  
> driver    = default  
> device    = /dev/lirc0  
  
**Lirc neu starten und Status prüfen, ob es läuft.**  
`$ sudo /etc/init.d/lircd stop`  
`$ sudo /etc/init.d/lircd start`  
`$ sudo /etc/init.d/lircd status`  
  
**Pi vor dem Testen neu starten.**  
`$ sudo reboot`  
  
**Testen, ob Lirc funktioniert.**  
`$ sudo /etc/init.d/lircd stop`  
`$ mode2 -d /dev/lirc0`  
> Using driver default on device /dev/lirc0  
> Trying device: /dev/lirc0  
> Using device: /dev/lirc0  
> pulse 9126  
> space 4478  
  
**Belegung der Fernbedienung aufnehmen.**  
Dafür einen Blick auf die vordefinierte Namensliste werfen.  
`$ sudo irrecord -l`  
  
Aufnahme starten und den Anweisungen folgen.  
`$ sudo irrecord -d /dev/lirc0 ~/lircd.conf`  
  
Prüfen, ob die erstellte Datei den richtigen Namen hat.  
`$ cd /home/pi`  
`$ find lircd.conf`  
  
Wenn *lircd.conf* nicht gefunden wurde, wurde die Namensgebung nicht übernommen.  
Die richtige *\*.conf* Datei muss gesucht und umbenannt werden.  
  
Beispiel für eine richtig erstellte *.conf*-Datei:  
  
> begin remote  
>   
> name  IR-Len  
> bits           32  
> flags SPACE_ENC|CONST_LENGTH  
> eps            30  
> aeps          100  
>   
> header       9106  4492  
> one           579  1659  
> zero          579   581  
> ptrail        583  
> repeat       9113  2225  
> gap          107884  
> toggle_bit_mask 0x0  
>   
>     begin codes  
>         KEY_0                    0x00FF6897  
>         KEY_1                    0x00FF30CF  
>         KEY_VOLUMEDOWN           0x00FFE01F  
>         KEY_2                    0x00FF18E7  
>         KEY_3                    0x00FF7A85  
>         KEY_4                    0x00FF10EF  
>         KEY_5                    0x00FF38C7  
>         KEY_6                    0x00FF5AA5  
>     end codes  
>     
> end remote  
  
Falls noch weitere Keycodes hinter den Codes stehen, müssen diese entfernt werden.  
  
Beispiel:  
  
>   
> begin codes  
>     KEY_0                    0x00FF6897 0x00000000  
> end codes  
>   
  
wird zu:  
  
>   
> begin codes  
>     KEY_0                    0x00FF6897  
> end codes  
>   
  
**Konfigurationsdatei in das LIRC Verzeichnis kopieren.**  
**Vorher ein Backup erstellen.**  
`$ sudo cp /etc/lirc/lircd.conf /etc/lirc/lircd_original.conf`  
`$ sudo cp ~/lircd.conf /etc/lirc/lircd.conf`  
  
**Rebooten und Lirc neu starten.**  
`$ sudo reboot`  
`$ sudo restart lircd`  
  
**Testen, ob alles funktioniert.**  
`$ irw`  
> 0000000000ff30cf 00 KEY_1 IR-Len  
> 0000000000ff30cf 01 KEY_1 IR-Len  
> 0000000000ff18e7 00 KEY_2 IR-Len  
> 0000000000ff18e7 01 KEY_2 IR-Len  
> 0000000000ff7a85 00 KEY_3 IR-Len  
> 0000000000ff7a85 01 KEY_3 IR-Len  
  
**Anschließend testweise ein Skript erstellen, welches auf Signale der Fernbedienung wartet.**  
**In diesem Beispiel wird irexec genutzt.**  
**Im Homeverzeichnis muss eine Konfigurationsdatei erstellt werden,**  
**in welcher zu übergebene Parameter festgelegt werden.**  
`$ sudo nano ~/.lircrc`  
  
> begin  
>     button = KEY_1  
>     prog   = irexec  
>     config = echo "KEY_1 pressed.";  
> end  
>   
> begin  
>     button = KEY_2  
>     button = KEY_3  
>     prog   = irexec  
>     config = echo "KEY_2, then KEY_3 pressed.";  
> end  
  
**Statt dem verwendeten echo ".." kann auch jeder andere Terminal Befehl verwendet werden (z.B. python skript.py).**  
**So lassen sich einfach Programme und Befehle auf Knopfdruck starten.**  
**Um auf IR Codes der Fernbedienung zu warten, muss das Programm gestartet werden.**  
`$ irexec`  
Die Ausgaben von echo ".." sollten direkt nach Tastendruck angezeigt werden.
