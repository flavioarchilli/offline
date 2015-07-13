from flask import (
    Blueprint,
    current_app,
    request,
    flash,
    redirect,
    url_for,
    render_template,
    abort,
    jsonify,
    g
)

import os
from glob import glob

from userSettings import *
from errorhandler import *
 
err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()

online_dq_bp = Blueprint('online_dq_bp', __name__,
                     template_folder='templates/online_dq_bp',
                     static_folder='static')

def check_auth():
    return current_app.auth

@online_dq_bp.route('/')
def online_dq():

    if current_app.auth:
         g.active_page = "online_dq_bp"
         settings.setOptionsFile(current_app.uid)
         err.setlogger(current_app.logger)
         page = render_template("online_dq.html",
                           LOAD_FROM_DB_FLAG = "false",
                           REFERENCE_STATE = settings.getReferenceState(),
                           USERNAME = current_app.username) 
    else:
         page = render_template("WelcomePage.html")
    return page

@online_dq_bp.route('/get_online_dq_filename')
def get_online_dq_filename():

    mypath = "/hist/Savesets/2015/DQ/DataQuality/"
    results = [y for x in os.walk(mypath) for y in glob(os.path.join(x[0], '*-EOR.root'))] 
    filenames = []
    for j in results:
        filenames.append(os.path.basename(j))
    d = dict(
        status_code = "OK",
        success = True,
        data = dict(
            root_filename = filenames,
            full_path = results
            )
        )
    return jsonify(d)

@online_dq_bp.route('/set_online_dq_filename')
def set_online_dq_filename():

    if check_auth() == "false":
        page = render_template("WelcomePage.html")
        return page

    filename = request.args.get('filename')
    print filename

    status_filename = False;

    if (os.path.isfile(filename)):
        status_filename = settings.setHistoROOTFileName(filename)        
    
    if status_filename == False:
        d = dict(
            success = False,
            status_code = 'ROOT_FILE_NOT_FOUND',
            data = dict(
                message = "ROOT File not found."
                )
            )
        return jsonify(d)
    else:
        d = dict(
            success = False,
            status_code = 'ROOT_FILE_FOUND',
            data = dict(
                message = "Reference File found."
                )
            )
        return jsonify(d)

@online_dq_bp.route('/set_online_dq_reference_filename')
def set_online_dq_reference_filename():

    if check_auth() == "false":
        page = render_template("WelcomePage.html")
        return page

    filename = request.args.get('filename')

    status_filename = False;
    if (os.path.isfile(filename)):
        status_filename = settings.setReferenceROOTFileName(filename)        
    
    if status_filename == False:
        d = dict(
            success = False,
            status_code = 'REFERENCE_FILE_NOT_FOUND',
            data = dict(
                message = "REFERENCE File not found."
                )
            )
        return jsonify(d)
    else:
        d = dict(
            success = False,
            status_code = 'REFERENCE_FILE_FOUND',
            data = dict(
                message = "Reference File found."
                )
            )
        return jsonify(d)

            
