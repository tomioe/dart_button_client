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

@app.route('/wifi', methods=('GET', 'POST'))
def create():
    if len(config.read(cvar.CONFIG_FILENAME)) == 0:
        flash('no config read yet')
        return redirect('/')

    if request.method == 'POST':
        new_ssid = request.form['ssid']
        new_pw = request.form['pw']
        error = None

        if not new_ssid or not new_pw:
            error = 'ssid and pw is required.'

        if error is not None:
            flash(error)
        else:
            # write to status.ini file
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
    my_vars = {}

    x = config.read(cvar.CONFIG_FILENAME)
    if len(x) > 0 and x[0] == cvar.CONFIG_FILENAME:
        print("we got a match ladies and gentlemen")
        curr_status = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERVER_STATUS]
        if curr_status == 'no_conn':
            return redirect('/wifi')
        elif curr_status == 'no_resp' or curr_status == 'ok':
            return redirect('/status')
    else:
        flash('no config file created yet')
        print(f'x was {x} , filename was {cvar.CONFIG_FILENAME}')
    # #     return redirect('')
    # # except:
    # #     print("no config file")
    # #     flash('no config file created yet')



    # hidden_data = ''
    # with open('my_local_file.txt', 'r') as local_file:
    #     hidden_data = local_file.readline()
    #     print(f'Hidden stuff: {hidden_data}')

    # my_vars['hidden_data'] = hidden_data
    
    return render_template('index.html', my_vars=my_vars)  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
    app.add_url_rule('/', endpoint='index')