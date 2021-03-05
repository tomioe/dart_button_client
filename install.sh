#!/bin/bash

# check if running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

cp ./config/*.* /lib/systemd/system/
touch web.log
touch controller.log
rm -rf status.ini
pip3 install -r requirements.txt

sudo chmod 777 ./ApWlanScripts/*.sh
# run script that allows for easy switching between AP and WLAN
# since we set the WLAN through web interface, no need to set -s[sid] and -p[assword]
./ApWlanScripts/_setup_wlan_and_AP_modes.sh -s "" -p "" -a Dartbutton -r dartbutton