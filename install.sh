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
sudo chmod 777 ./ApWlanScripts/*.sh
./ApWlanScripts/_setup_wlan_and_AP_modes.sh -s "Gates of Hell" -p copenhell2019 -a Dartbutton -r dartbutton
pip3 install -r requirements.txt