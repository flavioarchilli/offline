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
from webmonitor.auth import requires_auth
from webmonitor.auth import get_info
 
err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()

histogramDB_tree_menu = Blueprint('histogramDB_tree_menu', __name__,
                                  template_folder='templates/histogramDB_tree_menu',
                                  static_folder='static')

            


@histogramDB_tree_menu.route('/checkDBConnection')
@requires_auth()
def checkDBConnection():
    """
    Checks wether we can connect to the DB. Called via ajax on the set timeperiod, e.g. all 5 minutes and provides a visual feedback
    to the user.
    
    Returns a JSON string, indicating if we could connect successfully.
    """

    settings.setOptionWithTree(get_info('uid'))

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

@histogramDB_tree_menu.route('/menutree', methods=['GET'])		
@requires_auth()
def generateMenuTreeJSON():
    """
    Called by javascript via ajax call. Returns menu tree in json format.
    Receives two parameters during the ajax call:
	
    loadFromDBFlag: the tree is cached to increase the speed of the menu generation. If this string (!!) == "true", the menu is freshly
    read from the database. If loadFromDBFlag == "false" it is read from the cache file (if it exists)
    
    allNodesStandardState: When rereading from the database, this string determines if all nodes shall be opened or closed. Used by the
    "expand all" and "collapse all" button.
	
    """
    settings.setOptionWithTree(get_info('uid'))

    loadFromDBFlag = request.args.get('loadFromDBFlag')
    allNodesStandardState = request.args.get('allNodesStandardState')
    filterFlag = request.args.get('filterFlag')
    filterText = request.args.get('filter')
		

    menutree = generateMenu(loadFromDBFlag, allNodesStandardState, filterFlag, filterText)

    return menutree
    
@histogramDB_tree_menu.route('/menuTreeOpenOrCloseFolder', methods=['GET'])
@requires_auth()
def menuTreeOpenOrCloseFolder():
    """
    This method is called via ajax by javascript whenever a folder is opened or closed. The idea is to save this in the cache, so that
    when you reload the page or open anorther page, the tree state is persisted. This method receives to parameters via GET:
    id: The id of the node opened. This has to start with //F//, which denotes folders. After //F// the path follows, i.e. //FF///a/b/c
    action: Whether a node was closed or opened
    """

    settings.setOptionWithTree(get_info('uid'))
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
        menuAsComplexObject = settings.readTree()

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
        settings.storeTree(menuAsComplexObject)    	
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

    settings.setOptionWithTree(get_info('uid'))

    connection = current_app.config["HISTODB"]

    # loadFromDBFlag == "false" and not False because it is sent by json by javascript!
    # if we are reading it from the file and this file also exists
    if loadFromDBFlag == "false" and filterFlag == "false" and settings.checkTreeCache():

        
        menuAsComplexObject = settings.readTree()
        menuAsJSONString = json.dumps(menuAsComplexObject)
    	
    	
        return menuAsJSONString
    # Get it freshly from the database
    else:

        menuAsComplexObject = generateMenuRecursion(connection.generateMenuList(filterText), "", allNodesStandardState)
        menuAsJSONString = json.dumps(menuAsComplexObject)

        # Save database content for further uses in cache
        settings.storeTree(menuAsComplexObject)

        
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
	
@histogramDB_tree_menu.route('/Histo<path>')
@histogramDB_tree_menu.route('/Histo')
@requires_auth()
def Histo(path=""):
    settings.setOptionWithTree(get_info('uid'))        
    connection = current_app.config["HISTODB"]
    g.active_page = "Histo"
#    if path == "":
    path = request.args.get('path')
    
    histosContained = connection.getHistosInPath(path)

    print histosContained
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
        print ">>>>>>>>>>> histoname: %s"%histo.NAME
        histogramName = histo.NAME.split("/", 1)[1]
        histogramShowName = histo.NAME.split("/")[-1]
        histogramLabelId = "LABEL_FOR_" + histogramName
        histogramDisplayOptions = "OPTIONS_FOR_" + histogramShowName
        histogramTitle = histo.NAME
        HID = histo.HID
        
        #if opt is available read it out (we are doing an OUTER JOIN, so expect NULL values for OPT!!)
        labelX = "NONAME"
        labelY = "NONAME"
        ref = "NOREF"
        if hasattr(histo, 'OPT'):
            if hasattr(histo.OPT, 'LABEL_X'):
                labelX = histo.OPT.LABEL_X
                print "labelX >>>> ",labelX
            if hasattr(histo.OPT, 'LABEL_Y'):
                labelY = histo.OPT.LABEL_Y
            if hasattr(histo.OPT, 'REF'):
                ref = histo.OPT.REF
        else: 
            print "labelX <<<< ",labelX
            labelX = "NOOPT"
            labelY = "NOOPT"

    		
        #save into template
        columns += render_template("histoCell.html", 
                                   DATA_FILE = settings.getHistoROOTFileName(), 
                                   HISTOGRAM_NAME = histogramName, 
                                   HISTOGRAM_SHOW = histogramShowName, 
                                   REFERENCE_NAME = histogramName,
                                   REFERENCE_DATA_FILE = settings.getReferenceROOTFileName(),
                                   HISTOGRAM_LABEL_ID = histogramLabelId,
                                   HISTOGRAM_DISPLAY_OPTIONS = histogramDisplayOptions,
                                   HISTOGRAM_HID = HID,
                                   HISTOGRAM_LABEL_X = labelX,
                                   HISTOGRAM_LABEL_Y = labelY,
                                   REFERENCE_NORMALISATION = ref,
                                   HTML_HISTO_ID = "Histo_"+str(i),
                                   HISTO_CENTER_X = histo.CENTER_X,
                                   HISTO_CENTER_Y = histo.CENTER_Y,
                                   HISTO_SIZE_X = histo.SIZE_X,
                                   HISTO_SIZE_Y = histo.SIZE_Y,
                                   HISTO_SHOW_TITLE= histogramTitle)
        
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
                           REFERENCE_STATE = settings.getReferenceState(),
                           USERNAME = get_info('username'))

    d = dict( 
        success = True,
        html = page 
        )

    return jsonify(d)
