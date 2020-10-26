#!/usr/bin/python
import configparser
import time 
import subprocess
import os

import common_vars as cvar 


def switch_to_ap():
    # os.system('sudo ./raspiApWlanScripts/switchToAP.sh') 
    return

def switch_to_client(ssid, pw):
     # print(f'connecting to wifi with "{ssid}", "{pw}"')
    new_wpa_supplicant = [
        'country=GB',
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        '\n',
        'network={',
            f'\tssid="{ssid}"',
            f'\tpsk="{pw}"',
        '}'
    ]
    for new_line in new_wpa_supplicant:
        print(new_line)
    # wpa_supp_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
    # with open(wpa_supp_path, 'w') as wpa_file:
    #         wpa_file.write(new_line+'\n')

    # os.system('sudo ./raspiApWlanScripts/switchToAP.sh') 
    return 

def check_connection(check_address):´
    # 'ping' on *NIX has different returncodes depending on the address
    cmd = ['ping', '-c 1', check_address]
    ping = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    fail_counter = 0

    # see here for simpler way: https://stackoverflow.com/a/16808776
    while ping.poll() is None:
        # wait for ping command to finish
        time.sleep(1)


    print(f'return is {ping.returncode}')
    if ping.returncode == 0
        fail_counter += 1
        if fail_counter == 5
            print("Failed to establish wifi connection")
            return False
    else
        # we got a connection! update the status and connect to the server
        print(f'we got connection to "{check_address}"')
        return True
    return False

if __name__ == '__main__':
    print('Controller started, reading configuration.')
    # switch_to_ap()

    config = configparser.RawConfigParser()
    x = config.read(cvar.CONFIG_FILENAME)
    if len(x) == 0:
        config[cvar.CONFIG_SECTION] = {
            cvar.CONFIG_CURR_SSID: '',
            cvar.CONFIG_CURR_PW: '',
            cvar.CONFIG_SERVER_STATUS: 'no_conn'
        }
        cvar.write_config(config)
        print("Configuration no found, writing new.")

    # connect to WiFi 
    while(True):
        config.read(cvar.CONFIG_FILENAME)
        new_wifi = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
        new_pw = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
        if new_wifi != '' and new_pw != '':
            print("Got initial WiFi Creds, connecting!")
            switch_to_client(new_wifi, new_pw)
            config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_resp'
            cvar.write_config(config)
            break
        # print("no new pw, sleeping")
        time.sleep(2)

    '''
        TODO:
            * Verify connection check
            * Generic connection check
            * Generic properties handling
            * Verify "switch_to_ap()" path in main loop
            * button.py spawn
            * Script calling
            * wpa-supplicant updating
            * Connection of web.py when switching between AP and client
    '''

    # while(True):
    #     if check_wifi_connection():
    #         if check_server_connection():
    #             config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'ok'
    #             cvar.write_config(config)
    #             subprocess.run(["python3", "-u", "button.py"])
    #         else:
    #             config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_resp'
    #             switch_to_ap()
    #     else:
    #         config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_conn'
    #         switch_to_ap()
    #     cvar.write_config(config)
    #     sleep(5)


       


