#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     12/04/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logging
import json
import base64
import time
import pickle


from logins import *# logins.py - contains a list of account dicts

# FLASK magic
from flask import Flask
from flask import request
app = Flask(__name__)





@app.route('/')
def hello():
    """Ensure server works"""
    return 'Disco server running.\r\n'


@app.route('/_fa_disco/api/get_secrets', methods = ["POST", "GET"])
def serve_furaffinity_logins():
    """Serve FA passwords"""
    global FURAFFINITY_LOGIN_DETAILS# I don't know why but we need this here
    # Get a username/password pair
    # Sort the list by last used
    FURAFFINITY_LOGIN_DETAILS = sorted(FURAFFINITY_LOGIN_DETAILS, key=lambda k: k['last_used'])# http://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    account = FURAFFINITY_LOGIN_DETAILS[0]
    account['last_used'] = time.time()

    # Encode the login details
    login_data = {
        'username':account['username'],
        'password':base64.b64encode(account['password'].encode('ascii')).decode('ascii')
        }

    json_to_send = json.dumps(login_data)
    return json_to_send


@app.route('/_fa_disco/api/user_discovery', methods = ["POST", "GET"])
def serve_furaffinity_discovery():
    """Accept FA user discovery"""
    if request.method == 'POST':
        data = request.form
        logging.debug('serve_furaffinity_discovery() got data: %s' % (data))
        print('serve_furaffinity_discovery() got data: %s' % (data))
        with open('discovered.txt', 'a') as f:
            #f.write(data)
            pickle.dump(data, f)

        return 'Accepted discovery.\r\n'
    else:
        abort(403)



@app.route('/_fa_disco/api/user_private_discovery', methods = ["POST", "GET"])
def serve_furaffinity_private_discovery():
    """Accept FA user discovery"""
    if request.method == 'POST':
        data = request.form
        logging.debug('serve_furaffinity_discovery() got data: %s' % (data))
        print('serve_furaffinity_discovery() got data: %s' % (data))
        with open('private_discovered.txt', 'a') as f:
            #f.write(data)
            pickle.dump(data, f)

        return 'Accepted discovery.\r\n'
    else:
        abort(403)



def main():
    try:
        logging.basicConfig(level=logging.DEBUG)
        app.debug = True
        app.run(host='0.0.0.0')# Let anyone anywhere access this, easier to be insecure.
    except Exception, e:# Log fatal exceptions
        logging.critical('Unhandled exception!')
        logging.exception(e)
    return


if __name__ == '__main__':
    main()
