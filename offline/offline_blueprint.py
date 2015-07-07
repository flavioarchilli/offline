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

from userSettings import *
from errorhandler import *

err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()



import webmonitor 

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
         settings.setOptionsFile(webmonitor.auth.get_user_id())
         err.setlogger(current_app.logger)
         page = render_template("Overview.html",
                           LOAD_FROM_DB_FLAG = "false",
                           RUN_NMBR =  settings.getRunNmbr(),
                           VERSION = settings.getVersion(),
                           REFERENCE_STATE = settings.getReferenceState()) 
    else:
         page = render_template("home.html")
    return page



@offline_bp.route('/checkDBConnection')
def checkDBConnection():
    """
    Checks wether we can connect to the DB. Called via ajax on the set timeperiod, e.g. all 5 minutes and provides a visual feedback
    to the user.
    
    Returns a JSON string, indicating if we could connect successfully.
    """

    if check_auth() == "false":
        page = render_template("home.html")
        return page

    connection = current_app.config["HISTODB"]
    status = connection.checkDBConnection()
    if status == True:
        d =  dict(
            success = True,
            data = dict(
                message = "Connection established"
                )
            )
        return jsonify(d)
    else:
        d =  dict(
            success = True,
            message = "Connection established"
            )
        return jsonify(d)

@offline_bp.route('/menutree', methods=['GET'])		
def generateMenuTreeJSON():
    """
    Called by javascript via ajax call. Returns menu tree in json format.
    Receives two parameters during the ajax call:
	
    loadFromDBFlag: the tree is cached to increase the speed of the menu generation. If this string (!!) == "true", the menu is freshly
    read from the database. If loadFromDBFlag == "false" it is read from the cache file (if it exists)
    
    allNodesStandardState: When rereading from the database, this string determines if all nodes shall be opened or closed. Used by the
    "expand all" and "collapse all" button.
	
    """
    if check_auth() == "false":
        page = render_template("home.html")
        return page

    loadFromDBFlag = request.args.get('loadFromDBFlag')
    allNodesStandardState = request.args.get('allNodesStandardState')
    filterFlag = request.args.get('filterFlag')
    filterText = request.args.get('filter')
		

    menutree = generateMenu(loadFromDBFlag, allNodesStandardState, filterFlag, filterText)

    return menutree
    
@offline_bp.route('/menuTreeOpenOrCloseFolder', methods=['GET'])
def menuTreeOpenOrCloseFolder():
    """
    This method is called via ajax by javascript whenever a folder is opened or closed. The idea is to save this in the cache, so that
    when you reload the page or open anorther page, the tree state is persisted. This method receives to parameters via GET:
    id: The id of the node opened. This has to start with //F//, which denotes folders. After //F// the path follows, i.e. //FF///a/b/c
    action: Whether a node was closed or opened
    """

    if check_auth() == "false":
        page = render_template("home.html")
        return page

    id = request.args.get('id')
    action = request.args.get('action')
    
    # Event came from a folder
    if id.startswith("//F//"):
        folderName = id[5:]
    	
        # Contains the parts of the path, e.g. /a/b/c => [a, b, c]
        pathParts = list()
        # Root directory
        if folderName == "":
            folderName = "/"
            pathParts = [""]
        else:
            pathParts = folderName.split("/")
    	
        # Fetch structure from file
        treeCache = open("treeCache.pcl", "r")
        menuAsComplexObject = pickle.load(treeCache)
        treeCache.close()

        # Containes the root folder
        # we are moving outgoing from root folder to the folder, 
        # which shall have opened -> True
        currentFolder = menuAsComplexObject
    
    	#this loop iterates over the folders contained in the via AJAX Get given id attribute, e.g.
    	#/a/b/c
    	#over a then b then c
        i = 0


    	#in: pathParts, currentFolder
    	#out lookingAtPath, loo
        while i < len(pathParts):
            #just shortcut for pathParts[i]
            lookingAtPath = pathParts[i]
    	
    	    #this loop iterates over all all folders contained in the current root object, i.e.
    	    #/a/b/c
    	    #/a/u/v
    	    #/a/u/w
    	    #and looking for /a/u/v
    	    #iterate over "/" finding a, iterate over a finding u, then interate over u finding v
            j = 0
            while j < len(currentFolder):
    	        #just shortcut for currentFolder[j]
                lookingAtFolder = currentFolder[j]
    	    
    	        #if name of the folder matches the name of the via GET given path
                if lookingAtFolder["text"] == pathParts[i]:
    	            #something went wrong, reached leaf also expecting folder
                    if not "children" in lookingAtFolder:
                        raise Exception("Reached lead unexpectedly")
                    
    	            #next step would not be the last step, therefore make a further step down the folder hirachy
                    if not i+1 == len(pathParts):
                        currentFolder = lookingAtFolder["children"] 
                    #change state
    	            #close only last folder
                    else:
                        #change state
                        #close only last folder
                        if action == "close":
                            lookingAtFolder["state"]["opened"] = False
                            lookingAtFolder["icon"] = "glyphicon glyphicon-folder-close"
    	    		
                    #change state
                    #open all folders
                    if action == "open":
                        lookingAtFolder["state"]["opened"] = True
                        lookingAtFolder["icon"] = "glyphicon glyphicon-folder-open"
    	    		
                    break
                j+=1
            #END: while j < len(keysa)    
            i += 1
        #END while i < len(pathParts):

        #save changes
        treeCache = open("treeCache.pcl", "w")
        pickle.dump(menuAsComplexObject, treeCache)
        treeCache.close()
    	
        d = dict(
            success=True,
            data=folderName
            )

        return jsonify(d)
	
def generateMenu(loadFromDBFlag = True, allNodesStandardState = "closed", filterFlag = "false", filterText = None):
    """
    Returns the JSON String for the tree menu.
    
    Receives two parameters:

    loadFromDBFlag: the tree is cached to increase the speed of the menu generation. If this string (!!) == "true", the menu is freshly
    read from the database. If loadFromDBFlag == "false" it is read from the cache file (if it exists)
    
    allNodesStandardState: When rereading from the database, this string determines if all nodes shall be opened or closed. Used by the
    "expand all" and "collapse all" button.


    WARNING: to be reviewed 
    """

    if check_auth() == "false":
        page = render_template("home.html")
        return page

    connection = current_app.config["HISTODB"]

    # loadFromDBFlag == "false" and not False because it is sent by json by javascript!
    # if we are reading it from the file and this file also exists
    if loadFromDBFlag == "false" and filterFlag == "false" and os.path.exists("treeCache.pcl") and os.path.isfile("treeCache.pcl"):

        treeCache = open("treeCache.pcl", "r")
        
        menuAsComplexObject = pickle.load(treeCache)
        menuAsJSONString = json.dumps(menuAsComplexObject)
    	
        treeCache.close()
    	
        return menuAsJSONString
    # Get it freshly from the database
    else:

        menuAsComplexObject = generateMenuRecursion(connection.generateMenuList(filterText), "", allNodesStandardState)
        menuAsJSONString = json.dumps(menuAsComplexObject)

        # Save database content for further uses in cache
        treeCache = open("treeCache.pcl", "w")
        pickle.dump(menuAsComplexObject, treeCache)
        treeCache.close()
        
        return menuAsJSONString


# Generates tree menu in the left side bar prepared for json format
# loadFromDBFlag == True: load tree freshly from database
# loadFromDBFlag == False: load tree from cache 
def generateMenuRecursion(processedInputList, priorPath="", allNodesStandardState="closed"):
    """
    Recursive methode processing the processed database output (stored in processedInputList) to s python structure with just needs
    to be jsonified to have the correct response to the ajax menu call.
    
    Receives three parameters:
    
    processedInputList: After fetching a list of PAGES from the DB, this list has to be prepocessed, which is done in
    DBdeclaration.py:makeMenuList() and which is automatically called by DBdeclaration.py:generateMenuList(). So you want to call
    this function with generateMenuRecursion(processedInputList = connection.generateMenuList(), ...
    
    priorPath: Used by the recursion internally to set up the right ids, considering the corresponding root elements.
    
    allNodesStandardState: When rereading from the database, this string determines if all nodes shall be opened or closed. Used by the
    "expand all" and "collapse all" button.
    """

    try:
        output = list()
        #Standard behavior, as normally tree is presented with all folders closed.
        stdIcon = "glyphicon glyphicon-folder-close"
        stdStateOpenend = False
	#if we want instead an all open tree
        if allNodesStandardState == "opened":
            stdIcon = "glyphicon glyphicon-folder-open"
            stdStateOpenend = True	
	
        #now go through every item in the preprocessed input list
        for item in processedInputList:
            #this string denotes that the root element is a leaf, i.e. we doesn't have any children
	    #note returning NONE
            if item == "end":
                return None
	    	
            #if our item is not a string, we assume it is a dictionary
            else:
                #and iterate over keys and corresponding values
                for key, value in item.iteritems():
                    #and look into the children of each key
                    children = generateMenuRecursion(value, priorPath + key + "/", allNodesStandardState)
	    		
                    entry = dict()
                    
                    #when returning NONE: this key has no children, i.e. is a leaf
                    if children == None:
                        entry["text"] = key
                        entry["id"] = priorPath + key
                        entry["icon"] = "glyphicon glyphicon-file"
                    #otherwise it is a folder
                    else:
                        entry["text"] = key
                        entry["id"] = "//F//"+priorPath + key
                        entry["icon"] = stdIcon
	    	    #and we save the cildren
                        entry["children"] = children
	    	    #and consider if all nodes shall be opened or closed
                        entry["state"] = {"opened" : stdStateOpenend, "selected": False}
                #END: for key, value in item.iteritems():
                        
                #we save our generated output
                output.append(entry)	
            #END: else
        return output
    except Exception as inst:
        print inst
#       err.rethrowException(inst)
        return None
	
@offline_bp.route('/Histo<path>')
@offline_bp.route('/Histo')
def Histo(path=""):
    if check_auth() == "false":
        page = render_template("home.html")
        return page
    connection = current_app.config["HISTODB"]
    g.active_page = "Histo"
    if path == "":
        path = request.args.get('path')
    
    histosContained = connection.getHistosInPath(path)
    rows = ""
    columns = ""
    i = 0

    while i < len(histosContained):
        histo = histosContained[i]
        
        if i != 0 and (i % 2) == 0:
            rows += render_template("histoRow.html", COLUMNS = columns)
            columns = ""
        #end if	
    	
        #read out histogram
        dataFile = "BrunelDaVinci_FULL_121752_00019821.root"
        histogramName = histo.NAME.split("/", 1)[1]
        histogramLabelId = "LABEL_FOR_" + histogramName
        histogramDisplayOptions = "OPTIONS_FOR_" + histogramName
        histogramTitle = histo.NAME
        HID = histo.HID
        
        #if opt is available read it out (we are doing an OUTER JOIN, so expect NULL values for OPT!!)
        labelX = ""
        labelY = ""
        ref = ""
        if hasattr(histo, 'OPT'):
            if hasattr(histo.OPT, 'LABEL_X'):
                labelX = histo.OPT.LABEL_X
            if hasattr(histo.OPT, 'LABEL_Y'):
                labelY = histo.OPT.LABEL_Y
            if hasattr(histo.OPT, 'REF'):
                ref = histo.OPT.REF
    		
        #save into template
        columns += render_template("histoCell.html", 
                                   DATA_FILE = settings.getHistoROOTFileName(), 
                                   HISTOGRAM_NAME = histogramName, 
                                   REFERENCE_NAME = histogramName,
                                   REFERENCE_DATA_FILE = settings.getReferenceROOTFileName(),
                                   HISTOGRAM_LABEL_ID = histogramLabelId,
                                   HISTOGRAM_DISPLAY_OPTIONS = histogramDisplayOptions,
                                   HISTOGRAM_HID = HID,
                                   HISTOGRAM_LABEL_X = labelX,
                                   HISTOGRAM_LABEL_Y = labelY,
                                   REFRENCE_NORMALISATION = ref,
                                   HTML_HISTO_ID = "Histo_"+str(i),
                                   HISTO_TITLE= histogramTitle)
    		
        i += 1
    if columns != "":
        rows += render_template("histoRow.html", COLUMNS = columns)
        columns = ""
    		
    recoVersionParts = settings.getVersion().split("/")
    visiblePart = ""
    if len(recoVersionParts) > 2:
        visiblePart = recoVersionParts[2]
    		
    	
    page = render_template("Histo.html", PATH = path, 
                               HISTOS_CONTAINED = str(histosContained), 
                               HISTO_PLOTS = rows,  
                               LOAD_FROM_DB_FLAG = "false",
                               RUN_NMBR = settings.getRunNmbr(),
                               VERSION_FULL = settings.getVersion(),
                               VERSION_VISIBLE = visiblePart,
                               REFERENCE_STATE = settings.getReferenceState())


    return page

@offline_bp.route('/setReferenceState')	
def changeReferenceState():
     if check_auth() == "false":
        page = render_template("home.html")
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
        page = render_template("home.html")
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
        page = render_template("home.html")
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

    


