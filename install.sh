#!/bin/bash

# check if running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

echo "Copying unit files to systemd"
cp ./config/*.* /lib/systemd/system/
echo "Creating empty config logs"
touch web.log
touch controller.log
echo "Installing python req's"
rm -rf status.ini
pip3 install -r requirements.txt

echo "Install AP & Wlan scripts"
sudo chmod 777 ./ApWlanScripts/*.sh
# run script that allows for easy switching between AP and WLAN
# since we set the WLAN through web interface, no need to set -s[sid] and -p[assword]
./ApWlanScripts/_setup_wlan_and_AP_modes.sh -s "" -p "" -a Dartbutton -r dartbutton
echo "Run 'sudo reboot now'"