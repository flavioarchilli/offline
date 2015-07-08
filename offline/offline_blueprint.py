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

import pickle
import os
import json
from glob import glob
import webmonitor 


from userSettings import *
from errorhandler import *
 
err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()

offline_bp = Blueprint('offline_bp', __name__,
                     template_folder='templates/offline_bp',
                     static_folder='static')

def check_auth():
    return webmonitor.auth.check_user_account()
            

@offline_bp.route('/')
@offline_bp.route('/Overview')
def loginner():
    if webmonitor.auth.check_user_account() != "false":
         g.active_page = "menu"
         settings.setOptionsFile(webmonitor.auth.get_info("uid"))
         err.setlogger(current_app.logger)
         page = render_template("Overview.html",
                           LOAD_FROM_DB_FLAG = "false",
                           RUN_NMBR =  settings.getRunNmbr(),
                           VERSION = settings.getVersion(),
                           REFERENCE_STATE = settings.getReferenceState(),
                           USERNAME = webmonitor.auth.get_info("username")) 
    else:
         page = render_template("WelcomePage.html")
    return page

@offline_bp.route('/ConfirmQuit')
def exiter():
     page = render_template("ConfirmQuit.html",
                           USERNAME = webmonitor.auth.get_info("username"),
                           PROJECTNAME = 'DQM')
     return page

# New Monitoring
@offline_bp.route('/hlt2')
def hlt2():
    if webmonitor.auth.check_user_account() != "false":
         g.active_page = "menu"
         settings.setOptionsFile(webmonitor.auth.get_info("uid"))
         err.setlogger(current_app.logger)
         page = render_template("hlt2.html",
                           LOAD_FROM_DB_FLAG = "false",
                           REFERENCE_STATE = settings.getReferenceState(),
                           USERNAME = webmonitor.auth.get_info("username")) 
    else:
         page = render_template("WelcomePage.html")
    return page

@offline_bp.route('/get_hlt2_filename')
def get_hlt2_filename():

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



    


