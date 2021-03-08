#! /usr/bin/python3
### BEGIN INIT INFO
# Provides:          web.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
# import the Flask class from the flask module
from flask import (
     Flask, render_template, request, url_for, flash, redirect
)

import configparser
config = configparser.RawConfigParser()

import common_vars as cvar

## main doc: https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/

# create the application object
app = Flask(__name__)
app.secret_key = b'd02c4c4cde7ae76252540d116a40f23a' # hello github crawler!


@app.route('/info', methods=('GET', 'POST'))
def wifi():
    print('page route')
    if len(config.read(cvar.CONFIG_FILENAME)) == 0:
        print('\tno config read, going back to /')
        flash('no config read yet')
        return redirect('/')

    if request.method == 'POST':
        print('\tgot wifi post')
        new_ssid = request.form['ssid']
        new_pw = request.form['pw']
        new_addr = request.form['address']
        new_port = request.form['port']

        if not new_ssid:
            print('\tno wifi ssid')
            flash('wifi ssid is required.')
        elif not new_pw:
            print('\tno wifi pw')
            flash('wifi pw is required.')
        elif not new_addr: 
            print('\tno server addr')
            flash('server addr is required.')
        elif not new_port: 
            print('\tno server port')
            flash('server port is required.')
        else:
            # write to status.ini file
            print('\twrote new wifi config')
            flash('new config written, attempting to connect...')
            config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID] = new_ssid
            config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW] = new_pw
            config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR] = new_addr
            config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT] = new_port
            cvar.write_config(config)

    page_properties = {}
    page_properties['config_ssid'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
    page_properties['config_pw'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]
    page_properties['config_server_address'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
    page_properties['config_server_port'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]

    return render_template('info.html', page_properties=page_properties)

@app.route('/')
def default():
    '''
        1) Read the config file
        2) determine what the 'status' is
        3) render info template
    '''
    print('root route')
    x = config.read(cvar.CONFIG_FILENAME)
    if len(x) > 0 and x[0] == cvar.CONFIG_FILENAME:
        print("\tconfig file was read")
        curr_status = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS]
        if curr_status == 'no_conn':
            print('\tno wifi connection')
        elif curr_status == 'no_resp':
            print('\tno server connection')
        elif curr_status == 'ok':
            print('\tserver connection is ok')

        return redirect('/info')
    else:
        flash('no config file created yet')
        print(f'x was {x} , filename was {cvar.CONFIG_FILENAME}')
    
    return render_template('index.html', my_vars=my_vars)  # render a template

def main():
    app.run(debug=True,host= '0.0.0.0')
    app.add_url_rule('/', endpoint='index')

# start the server with the 'run()' method
if __name__ == '__main__':
    print("Web Server setting up")
    main()
