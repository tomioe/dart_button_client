CONFIG_FILENAME = 'status.ini'
CONFIG_SECTION = 'MAIN'
CONFIG_CURR_SSID = 'curr_ssid'
CONFIG_CURR_PW = 'curr_pw'
CONFIG_SERVER_STATUS = 'server_status'
CONFIG_SERV_ADDR='server_address'
CONFIG_SERV_PORT='server_port'

def write_config(cparser):
    with open(CONFIG_FILENAME, 'w+') as configfile:
        cparser.write(configfile)
    