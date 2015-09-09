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
import cppyy
import ROOT
ROOT.std.__file__ = 'dummy'

cppyy.gbl.gSystem.Load("offline/lib/libHistograms.so")
cppyy.gbl.gInterpreter.Declare('#include <offline/lib/libHistograms.h>')
 
err = errorhandler()
settings = userSettings(err)
settings.readInHistoRootFileIfPossible()
settings.readInReferenceRootFileIfPossible()

tasks_bp = Blueprint('tasks_bp', __name__,
                     template_folder='templates/tasks_bp',
                     static_folder='static')



def add_file_extension(filename):
    """Add `.root` extension to `filename`, if it's not already present."""
    return (filename + '.root') if filename[-5:] != '.root' else filename


def tfile_path(filename):
    """Return the path to the TFile with `filename`."""
    here = os.path.dirname(__file__)
    return '{0}/static/files/{1}'.format(here, filename)




@tasks_bp.route('/get_key_from_file', methods=['POST'])
@requires_auth()
def get_key_from_file():
    """Return the object, stored under `key_name`, in `filename`.

    Keyword arguments:
    filename -- Name of file with full path, e.g. `/a/b/my_file.root`
    key_name -- Name of key object is stored as
    """
    json_data = request.get_json()
    
    is_reference = json_data['is_reference']
    filename = json_data['filename']
    key_name = json_data['key_name']

    
    settings.setOptionsFile(get_info('uid'))
    f = ROOT.TFile(filename)

    d = eval(cppyy.gbl.getDictionary(f,key_name))
    
    f.Close()
    return jsonify(d)


@tasks_bp.route('/get_keys_from_list', methods=['POST'])
@requires_auth()
def get_keys_from_list():
    """Return the object, stored under `key_name`, in `filename`.

    Keyword arguments:
    filename -- Name of file with full path, e.g. `/a/b/my_file.root`
    key_name -- Name of key object is stored as
    """
    json_data = request.get_json()

    d = dict()
    d['elements'] = list()
    settings.setOptionsFile(get_info('uid'))
    fn = settings.getHistoROOTFileName()
    rfn = settings.getReferenceROOTFileName()
# open root file stored in the root database
    f = ROOT.TFile(fn)
# open reference root file stored in the root database
    rf = ROOT.TFile(rfn)

    for values in json_data.itervalues():
        for k in values:
            subd = dict()
            subd["index"] = k["index"]
            if fn != k["file"]: 
                fn = k["file"]
                settings.setHistoROOTFileName(fn)
                f = ROOT.TFile(fn)
            print "histogram :>>>>>: ",k["histogram"]
            subd["data"] = eval(cppyy.gbl.getDictionary(f,k["histogram"]))
            if rfn != k["referenceFile"]: 
                rfn = k["referenceFile"]
                settings.setReferenceROOTFileName(rfn)
                rf = ROOT.TFile(rfn)
            subd["refdata"] = eval(cppyy.gbl.getDictionary(rf,k["reference"]))
            d['elements'].append(subd)

    f.Close()
    rf.Close()

    return jsonify(d)
