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

@offline_bp.route('/setReferenceState')	
def changeReferenceState():
     if check_auth() == "false":
        page = render_template("WelcomePage.html")
        return page
 
     state = request.args.get('state')
     
     settings.setReferenceState(state)

     d = dict(
         success = True,
         data = dict(
             message = "Set State:"+ str(state)
             )
         )
     return jsonify(d)
     	
 			
@offline_bp.route('/setRecoVersion')	
def storeVersion():
    """
    Called by javascript via ajax call. Save the RecoVersion, and together with the runNmbr creates the path to the ROOT and
    reference file and saves it.
    
    """
    if check_auth() == "false":
        page = render_template("WelcomePage.html")
        return page
    bkClient = current_app.config["BKKDB"]
    #save recoVersion
    #here called full path, because it is like /Real Data/Reco14 und not just Reco13
    fullPath = request.args.get('recoVersion')
    settings.setVersion(fullPath)
    runNmbr = settings.getRunNmbr()
    	
    #extract just the recoVersion, i.e. Reco14
    fullPathParts = fullPath.split("/")
    recoVersion = fullPathParts[2]
    	
    #create histo-file path
    prodId = bkClient.getProcessId(runNmbr, fullPath)
    configversion = bkClient.getInformation(runNmbr)["configversion"]
    lfn = bkClient.MakeRunLFN(runNmbr, configversion, prodId)
    status1 = settings.setHistoROOTFileName(lfn)
    	
    #create reference-file path
    referenceFileName = bkClient.makeReferenceROOTFileName(recoVersion, runNmbr)
    status2 = settings.setReferenceROOTFileName(referenceFileName)

    if status1 != True:
        d = dict(
            success = False,
            StatusCode = 'ROOT_FILE_NOT_FOUND',
            data = dict(
                message = "ROOT File not found."
                )
            )

        return jsonify(d)
    elif status2 != True:

        d = dict(
            success = False,
            StatusCode = 'REFERENCE_FILE_NOT_FOUND',
            data = dict(
                message = "Reference File not found."
                )
            )
        return jsonify(d)
    else:
        
        d = dict(
            success = True,
            StatusCode = 'ROOT_AND_REFERENCE_FOUND',
            data = dict(
                message = "ROOT File and Reference File found."
                )
            )
        return jsonify(d)

		
@offline_bp.route('/setRunNumber')	
def storeRunNmbr():
    """
    Called by javascript via ajax call to set the run number.
    
    """
    if check_auth() == "false":
        page = render_template("WelcomePage.html")
        return page
    bkClient = current_app.config["BKKDB"]
    #retrieve the run number as GET argument
    runNmbr = int(request.args.get('runNmbr'))
    #and store it 
    settings.setRunNmbr(runNmbr)
    	
    #look if we have set a recoversion previousls
    recoVersionFullpath = settings.getVersion()
    	
    #now get a list of possible recos for this runNmbr
    recos = bkClient.getListOfRecos(runNmbr)
    	
    #to save if our previous recoVersion is still valid for this runNmbr. If this is the case -> keep it
    #otherwise (e.g. we have Reco11, but this runNmbr just allows Reco12, Reco13), see
    # if selectedRecoVersion == "":
    selectedRecoVersion = ""
    
    #if there are any
    if recos != None and len(recos) > 0:
        #save our results for the json output in this list
        result = list()
        #iterate over this list
        for reco in recos:
    	#split into two parts: the visible one "Reco..." and the full path e.g. "/Real Data/Reco..."
            recoParts = reco.split("/")
    			
    	#append it
    	result.append([ reco, recoParts[2] ])
    		
    	#if our previous recoVersion is the one we are looking at
    	if recoVersionFullpath == reco:
    	    #save this information
                selectedRecoVersion = reco
    		
        #previous Reco Version is not allowed for this runNmbr, throw away rootFiles
        if selectedRecoVersion == "":
            settings.setVersion("")
            settings.setReferenceROOTFileName("")
            settings.setHistoROOTFileName("")
            settings.actualROOTFile = None
            settings.actualROOTReferenceFile = None
            

        d = dict(
            success = True,
            StatusCode = 'RUN_NMBR_OK',
            data = dict(
                message = "Set Run Numbr"+ str(runNmbr),
                listOfRecos = result,
                selectedRecoVersion = selectedRecoVersion
                )
            )
        return jsonify(d)

    #otherwise: show errormessage->wrong runNmbr and discard previouls informations
    else:
        settings.setVersion("")
        settings.setReferenceROOTFileName("")
        settings.setHistoROOTFileName("")
        settings.actualROOTFile = None
        settings.actualROOTReferenceFile = None

        d = dict(
            success = False,
            StatusCode = 'NO_RECOS_FOUND_FOR_RUN_NMBR',
            data = dict(
                message = "Run Numbr "+ str(runNmbr)+" not found!",
                )
            )
        return jsonify(d)

    


