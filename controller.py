#!/usr/bin/python
import configparser
import time 
import subprocess
import os
import platform

import common_vars as cvar 


def switch_to_ap():
    if platform.system().lower() != "windows":
        os.system('sudo ./raspiApWlanScripts/switchToAP.sh') 
    return

def switch_to_client(ssid, pw):
    print(f'connecting to wifi with "{ssid}", "{pw}"')
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
    
    if platform.system().lower() != "windows":
        wpa_supp_path = '/etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
        with open(wpa_supp_path, 'w') as wpa_file:
            for new_line in new_wpa_supplicant:
                wpa_file.write(new_line+'\n')
                print(f'writing:\t{new_line}')
        os.system('sudo ./raspiApWlanScripts/switchToWlan.sh') 
        time.sleep(10)
    else:
        for new_line in new_wpa_supplicant:
            print(new_line)
    return 

def check_connection(check_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', check_address), shell=True)
    except:
        return False
    return True

def wait_for_config(cparser):
    print('!waiting to config!')
    while(True):
        cparser.read(cvar.CONFIG_FILENAME)
        new_wifi = cparser[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
        new_pw = cparser[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
        new_addr = cparser[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
        new_port = cparser[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]
        if new_wifi != '' and new_pw != '' and new_addr != '' and new_port != '':
            print("Got config, connecting!")
            cparser[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_resp'
            cvar.write_config(cparser)
            return True
        time.sleep(2)

if __name__ == '__main__':
    print('Controller started, reading configuration.')
    switch_to_ap()

    ctr_config = configparser.RawConfigParser()
    x = ctr_config.read(cvar.CONFIG_FILENAME)
    if len(x) == 0:
        ctr_config[cvar.CONFIG_SECTION] = {
            cvar.CONFIG_CURR_SSID: '',
            cvar.CONFIG_CURR_PW: '',
            cvar.CONFIG_SERV_ADDR: '',
            cvar.CONFIG_SERV_PORT: '',
            cvar.CONFIG_SERVER_STATUS: 'no_conn'
        }
        cvar.write_config(ctr_config)
        if platform.system().lower() != "windows":
            os.system('sudo chmod 777 '+cvar.CONFIG_FILENAME) 
        print("Configuration no found, writing new.")

    # connect to WiFi 
    if wait_for_config(ctr_config):
        print("wait over, switch to client")
        ctr_config.read(cvar.CONFIG_FILENAME)
        new_wifi = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
        new_pw = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
        new_addr = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
        new_port = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]
        switch_to_client(new_wifi, new_pw)

    '''
        TODO:
            * Verify connection check       ok
            * Generic connection check      ok
            * Verify "switch_to_ap()" path in main loop     ok
            * Script calling        ok
            * button.py spawn       ok
            * wpa-supplicant updating   ok
            * Connection of web.py when switching between AP and client     ok (single page)
            * Generic properties handling   
    '''

    main_loop_wait = False
    while(True):
        print('main loop')

        if main_loop_wait:
            print('\tmainloop waiting for new config')

        if main_loop_wait and wait_for_config(ctr_config):
            print('\tmainloop got config, back to Wlan')
            ctr_config.read(cvar.CONFIG_FILENAME)
            new_wifi = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
            new_pw = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
            new_addr = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
            new_port = ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]
            switch_to_client(new_wifi, new_pw)

        # assume gateway is always at .1 of wifi addr
        gateway_ip = new_addr[:new_addr.rfind('.')]+'.1'
        print(f'trying for gateway {gateway_ip}')
        if check_connection(gateway_ip):
            print('\twe got gateway connection')
            if check_connection('192.168.1.11'):
                print('\twe got server connection')
                ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'ok'
                cvar.write_config(ctr_config)
                python_prog = "python" + ('3' if platform.system().lower() != "windows" else '')
                subprocess.run([python_prog + " ./button.py"], shell=True)
            else:
                print('\tno server connection, clearing server config')
                ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_resp'
                cvar.clear_parameter(ctr_config, cvar.CONFIG_SERV_ADDR)
                cvar.clear_parameter(ctr_config, cvar.CONFIG_SERV_PORT)
                main_loop_wait = True
        else:
            print('\tno gateway connection, clearing wifi config')
            ctr_config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS] = 'no_conn'
            cvar.clear_parameter(ctr_config, cvar.CONFIG_CURR_SSID)
            cvar.clear_parameter(ctr_config, cvar.CONFIG_CURR_PW)
            main_loop_wait = True

        cvar.write_config(ctr_config)

        if main_loop_wait:
            print('\tback to ap')
            switch_to_ap()

        time.sleep(5)

       


