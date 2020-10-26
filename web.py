#!/usr/bin/python
import configparser
config = configparser.RawConfigParser()

import common_vars as cvar

# import the Flask class from the flask module
from flask import (
     Flask, render_template, request, url_for, flash, redirect
)

## main doc: https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/

# create the application object
app = Flask(__name__)
app.secret_key = b'd02c4c4cde7ae76252540d116a40f23a' # hello github crawler!

'''
    TODO:
        * Generic route for wifi / server
'''


@app.route('/server', methods=('GET', 'POST'))
def server():
    print('server route')
    if len(config.read(cvar.CONFIG_FILENAME)) == 0:
        print('\tno config read, going back to /')
        flash('no config read yet')
        return redirect('/')


    if request.method == 'POST':
        print('\tgot server post')
        new_server_addr = request.form['server']
        new_server_port = request.form['port']
        error = None

        if not new_server_addr or not new_server_port:
            print('\terror in entered data')
            error = 'address & port is required.'

        if error is not None:
            flash(error)
        else:
            # write to status.ini file
            config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR] = new_server_addr
            config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT] = new_server_port
            cvar.write_config(config)
            print('\twrote new server config')
            flash('new wifi config written, attempting to connect...')

    server_properties = {}
    server_properties['config_server_address'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
    server_properties['config_server_port'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]


    return render_template('server.html', server_properties=server_properties)
    

@app.route('/wifi', methods=('GET', 'POST'))
def wifi():
    print('wifi route')
    if len(config.read(cvar.CONFIG_FILENAME)) == 0:
        print('\tno config read, going back to /')
        flash('no config read yet')
        return redirect('/')

    if request.method == 'POST':
        print('\tgot wifi post')
        new_ssid = request.form['ssid']
        new_pw = request.form['pw']
        error = None

        if not new_ssid or not new_pw:
            print('\terror in entered data')
            error = 'ssid and pw is required.'

        if error is not None:
            flash(error)
        else:
            # write to status.ini file
            print('\twrote new wifi config')
            flash('new wifi config written, attempting to connect...')
            config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID] = new_ssid
            config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW] = new_pw
            cvar.write_config(config)

    wifi_properties = {}
    wifi_properties['config_ssid'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_SSID]
    wifi_properties['config_pw'] = config[cvar.CONFIG_SECTION][cvar.CONFIG_CURR_PW]


    return render_template('wifi.html', wifi_properties=wifi_properties)

@app.route('/')
def default():
    '''
        1) Read the config file
        2) determine what the 'status' is
        3) server template based on this value
    '''
    print('root route')
    x = config.read(cvar.CONFIG_FILENAME)
    if len(x) > 0 and x[0] == cvar.CONFIG_FILENAME:
        print("\tconfig file was read")
        curr_status = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS]
        if curr_status == 'no_conn':
            print('\twe\'ve got no wifi connection')
            return redirect('/wifi')
        elif curr_status == 'no_resp'
            print('\twe\'ve got no server connection')
            return redirect('/server')
        elif curr_status == 'ok':
            print('\tserver connection is ok')
            return redirect('/server')
    else:
        flash('no config file created yet')
        print(f'x was {x} , filename was {cvar.CONFIG_FILENAME}')
    
    return render_template('index.html', my_vars=my_vars)  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')
    app.add_url_rule('/', endpoint='index')
