cp ./config/*.* /lib/systemd/system/
touch web.log
touch controller.log
rm -rf status.ini
touch status.ini
pip3 install -r requirements.txt