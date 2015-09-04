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
from webmonitor.auth import requires_auth
from webmonitor.auth import get_info
from userSettings import *
from errorhandler import *
 
err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()

online_dq_bp = Blueprint('online_dq_bp', __name__,
                     template_folder='templates/online_dq_bp',
                     static_folder='static')


@online_dq_bp.route('/')
@requires_auth()
def online_dq():
      g.active_page = "online_dq_bp"
      settings.setOptionsFile(get_info('uid'))
      err.setlogger(current_app.logger)
      blueprint_list = current_app.create_bplist()
      page = render_template("online_dq.html",
                           LOAD_FROM_DB_FLAG = "false",
                           REFERENCE_STATE = settings.getReferenceState(),
                           USERNAME = get_info('username'),
                           PROJECTFULLLIST = current_app.create_bplist(),
                           PROJECTNAME = 'Online DQM') 
      return page

@online_dq_bp.route('/get_online_dq_filename')
@requires_auth()
def get_online_dq_filename():
    settings.setOptionsFile(get_info('uid'))
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
@requires_auth()
def set_online_dq_filename():

    settings.setOptionsFile(get_info('uid'))
    filename = request.args.get('filename')

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
@requires_auth()
def set_online_dq_reference_filename():
    settings.setOptionsFile(get_info('uid'))

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

            
