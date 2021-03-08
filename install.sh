#!/bin/bash

# check if running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

echo "Copying files to init.d"
cp /app/web.py /etc/init.d/
cp /app/controller.py /etc/init.d/
chmod +x /etc/init.d/web.py
chmod +x /etc/init.d/controller.py
update-rc.d web.py defaults
update-rc.d controller.py defaults

echo "Creating empty config logs"
touch web.log
touch controller.log

echo "Installing python req's"
rm -rf status.ini
pip3 install -r requirements.txt

echo "Installing AP & Wlan scripts"
sudo chmod 777 ./ApWlanScripts/*.sh
# run script that allows for easy switching between AP and WLAN
# since we set the WLAN through web interface, no need to set -s[sid] and -p[assword]
./ApWlanScripts/_setup_wlan_and_AP_modes.sh -s a -p a -a Dartbutton -r dartbutton