#!/bin/sh
sudo apt install libsdl2-mixer-2.0-0
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
sudo apt update
sudo apt install -y mopidy
sudo apt install -y mopidy-spotify
sudo apt install -y mopidy-mpd