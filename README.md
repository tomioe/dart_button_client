# Deploying

1. Install Raspbian Stretch Lite

1. Copy the AP/Client scripts from forked repo (see https://raspberrypi.stackexchange.com/questions/93311/switch-between-wifi-client-and-access-point-without-reboot
and https://github.com/tomioe/raspiApWlanScripts/)

1. Copy the python scripts over

1. Configure systemd (see below)

# systemd

Config from: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd

Place files in "config" in `/lib/systemd/system/`.

Make sure to `chmod 644 *.service` all service files.

Configure systemd with `sudo systemctl daemon-reload` and `sudo systemctl enable *.service`, reboot once done. 
