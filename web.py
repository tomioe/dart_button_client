import configparser
config = configparser.RawConfigParser()

import common_vars as cvar

# import the Flask class from the flask module
from flask import (
     Flask, render_template, request, url_for
)

## main doc: https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/

# create the application object
app = Flask(__name__)

@route('/wifi', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        new_wifi = request.form['new_wifi']
        new_pw = request.form['new_pw']
        error = None

        if not new_wifi or not new_pw:
            error = 'ssid and pw is required.'

        if error is not None:
            flash(error)
        else:
            # write to status.ini file
            flash('new wifi config written')

    return render_template('wifi.html')

@app.route('/')
def default():
    try:
        config.read(cvar.CONFIG_FILENAME)
    except:
        flash('no config file created yet')
    # hidden_data = ''
    # with open('my_local_file.txt', 'r') as local_file:
    #     hidden_data = local_file.readline()
    #     print(f'Hidden stuff: {hidden_data}')

    # my_vars = {}
    # my_vars['hidden_data'] = hidden_data
    
    '''
        1) Read the config file
        2) determine what the 'status' is
        3) server template based on this value
    '''

    return render_template('index.html', my_vars=my_vars)  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
    app.add_url_rule('/', endpoint='index')