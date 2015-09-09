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
                           RUN_NMBR =  settings.getRunNmbr(),                             
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

            
@online_dq_bp.route('/set_run_number')
@requires_auth()	
def set_run_number():
    """
    Called by javascript via ajax call to set the run number.
    
    """
    # set database reference 
    dataqualityDB = current_app.config["DQDB"]
    
    #set current option file
    settings.setOptionsFile(get_info('uid'))

    #retrieve the run number as GET argument
    rn = int(request.args.get('runnumber'))
    #and store it 
    settings.setRunNmbr(rn)
    

    fn = dataqualityDB.getOnlineDQFile(rn)
    settings.setHistoROOTFileName(fn)
 
    rfn = dataqualityDB.getOnlineDQRef(rn)    
    settings.setReferenceROOTFileName(rfn)
           
    if (fn == None and rfn == None):
          
          d = dict(
                success = False,
                StatusCode = 'ROOT_AND_REFERENCE_NOT_FOUND',
                data = dict(
                      message = "ROOT File not found."
                      )
                )
          return jsonify(d)

    elif (fn != None and rfn != None):
          d = dict(
                success = True,
                StatusCode = 'ROOT_AND_REFERENCE_FOUND',
                data = dict(
                      message = "ROOT File and Refernce File found."
                      )
                )
          return jsonify(d)

    elif (fn != None):
          d = dict(
                success = True,
                StatusCode = 'ROOT_FILE_FOUND_NO_REF',
                data = dict(
                      message = "ROOT File and found but Reference File."
                      )
                )
          return jsonify(d)

    else:
          d = dict(
                success = False,
                StatusCode = 'ROOT_FILE_NOT_FOUND',
                data = dict(
                      message = "ROOT File not found."
                      )
                )
          return jsonify(d)



@online_dq_bp.route('/change_reference_state')
@requires_auth()	
def change_reference_state():

    state = request.args.get('state')
    
    settings.setReferenceState(state)

    d = dict(
          success = True,
          data = dict(
                message = "Set State:"+ str(state)
                )
          )
    return jsonify(d)


@online_dq_bp.route('/get_next_runnumber')
@requires_auth()
def get_next_runnumber():
      
    rn = request.args.get('runnumber')
    # set database reference 
    dataqualityDB = current_app.config["DQDB"]
     
    nrn = dataqualityDB.nextOnlineDQRun(rn);
    
     
    if (nrn != None):
          d = dict(
                success = True,
                data = dict(
                      runnumber = nrn,
                      )
                )
          return jsonify(d)
    else:
          d = dict(
                success = False,
                data = dict(
                      runnumber = 0,
                      )
                )
          return jsonify(d)

@online_dq_bp.route('/get_previous_runnumber')
@requires_auth()
def get_previous_runnumber():
      
    rn = request.args.get('runnumber')
    # set database reference 
    dataqualityDB = current_app.config["DQDB"]
     
    prn = dataqualityDB.prevOnlineDQRun(rn);
     
    if (prn != None):
          d = dict(
                success = True,
                data = dict(
                      runnumber = prn,
                      )
                )
          return jsonify(d)
    else:
          d = dict(
                success = False,
                data = dict(
                      runnumber = 0,
                      )
                )
          return jsonify(d)
