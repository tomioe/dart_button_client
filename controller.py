import configparser
import time 
import subprocess
import os

import common_vars as cvar 


def switch_to_ap():

    '''
        manual mode didn't work, see below...
    '''

    # os.system('switchToAP.sh') 
    return

def switch_to_client(ssid, pw):
    # print(f'connecting to wifi with "{ssid}", "{pw}"')
    # # stop DNSMASQ and HOSTAPD
    # os.system('sudo systemctl stop dnsmasq')
    # os.system('sudo systemctl stop hostapd')
    # os.system('sudo systemctl disable hostapd')
    
    # os.system('sudo ifdown wlan0')
    # new_wpa_supplicant = [
    #     'country=GB',
    #     'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
    #     'update_config=1',
    #     'network={',
    #         f'\tssid="{ssid}"',
    #         f'\tpsk="{copenhell2019}"',
    #     '}'
    # ]
    # wpa_supp_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
    # with open(wpa_supp_path, w) as wpa_file:
    #     for new_line in new_wpa_supplicant:
    #         wpa_file.write(new_line+'\n')
    # os.system('sudo ifup wlan0')
    # os.system('sudo service networking reload')

    '''
        turns out dongle doesn't support AP mode.
        use forked github scripts.
    '''

    # os.system('./setup_wlan_and_AP_modes.sh -s <station mode SSID> -p <station mode password> -a <AP mode SSID> -r <AP mode password>')
    # time.sleep(15) # tune this based on setup time
    # os.system('switchToWlan.sh')

    return 

def initiate_config(cparser):
    x = cparser.read(cvar.CONFIG_FILENAME)
    if len(x) == 0:
        cparser[cvar.CONFIG_SECTION] = {
            cvar.CONFIG_CURR_SSID: '',
            cvar.CONFIG_CURR_PW: '',
            cvar.CONFIG_SERVER_STATUS: 'no_conn'
        }
        cvar.write_config(config)
        print("wrote new config file")


if __name__ == '__main__':
    ### TODO: Make this more loop friendly

    # switch_to_ap()
    config = configparser.RawConfigParser()
    #initiate_config(config)
    x = cparser.read(cvar.CONFIG_FILENAME)
    if len(x) == 0:
        cparser[cvar.CONFIG_SECTION] = {
            cvar.CONFIG_CURR_SSID: '',
            cvar.CONFIG_CURR_PW: '',
            cvar.CONFIG_SERVER_STATUS: 'no_conn'
        }
        cvar.write_config(config)
        print("wrote new config file")

    # connect to WiFi if we have SSID/PW
    while(True):
        config.read(cvar.CONFIG_FILENAME)
        new_wifi = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
        new_pw = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
        if new_wifi != '' and new_pw != '':
            print("Got new WiFi Creds, connecting!")
            # config[status] = "no_resp"
            break
        # print("no new pw, sleeping")
        time.sleep(2)
    
    config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_resp'
    cvar.write_config(config)
    # connect to wifi network

'''
    while(True):
        cmd = ['ping', '-c 1', 'www.google.com']
        ping = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        fail_counter = 0
        while ping.poll() is None:
            # wait for ping command to finish
            time.sleep(1)


        print(f'return is {ping.returncode}')
        if ping.returncode == 0
            fail_counter++
            if fail_counter == 5
                print("failed to establish wifi connection")
                config[status] = "no_conn"
                switch_to_ap()
        else
            # we got a connection! update the status and connect to the server
            break
'''