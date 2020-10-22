import configparser
import time 
import subprocess

import common_vars as cvar 




def write_status(variable, new_value):
    a = variable

# read up on AP's:
# https://www.instructables.com/Using-a-Raspberry-PI-Zero-W-As-an-Access-Point-and/
# https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md
def switch_to_ap():
    c = 'sss'
    # stop ...?
    # start ...???

# Default client connection: 
# https://raspberrypihq.com/how-to-add-wifi-to-the-raspberry-pi/
def switch_to_client(wifi, pw):
    print(f'connecting to wifi with "{wifi}", "{pw}"')
    # stop DNSMASQ and HOSTAPD
    # write to /etc/ {...}
    # 'sudo service networking reload'

# start the server with the 'run()' method
if __name__ == '__main__':
    # switch_to_ap()
    config = configparser.RawConfigParser()
    config[cvar.CONFIG_SECTION] = {
        cvar.CONFIG_CURR_WIFI: '',
        cvar.CONFIG_CURR_PW: '',
        cvar.CONFIG_SERVER_STATUS: 'no_conn'
    }

    with open(cvar.CONFIG_FILENAME, 'w+') as configfile:
        config.write(configfile)

    while(True):
        config.read(cvar.CONFIG_FILENAME)
        new_wifi = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_WIFI]
        new_pw = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
        if new_wifi != '' and new_pw != '':
            print("new pw, abort!")
            break
        # print("no new pw, sleeping")
        time.sleep(2)
        
    switch_to_client(new_wifi, new_pw)

'''
    while(True):
        cmd = ['ping', '-n 1', 'www.google.com']
        ping = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        while ping.poll() is None:
            # wait for ping to finish
            time.sleep(1)

        print(f'return is {ping.returncode}')
'''