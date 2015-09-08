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


def data_for_object(obj,filename):
    """Return a dictionary representing the data inside the object."""
    obj_class = obj.ClassName()
    d = {}
    d['type'] = obj_class[1:]
    d['numberEntries'] = obj.GetEntries()
    d['integral'] = obj.Integral()
    d['mean'] = "{:.4g}".format(obj.GetMean())
    d['RMS'] = "{:.4g}".format(obj.GetRMS())
    d['skewness'] = "{:.4g}".format(obj.GetSkewness())
    d['values'] = list()
    d['uncertainties'] = list()
    d['nbins'] = ""
    MyDisplayName = obj.GetName().split("/")[-1]
    d['key_name'] = MyDisplayName
    xaxis = obj.GetXaxis()
    yaxis = obj.GetYaxis()
    d['axis_titles'] = (xaxis.GetTitle(), yaxis.GetTitle())
    d['run_number'] = filename#.split("-")[1]
    if obj_class[0:3] == 'TH1' or obj_class[0:3] == 'TPr':        
        # For histograms, we provide
        #   binning: List of 2-tuples defining the (low, high) binning edges,
        #   values: List of bin contents, ith entry falling in the ith bin
        #   uncertainties: List of 2-tuples of (low, high) errors on the values
        #   axis_titles: 2-tuple of (x, y) axis titles

        d['binning'] =  list()

        nbins = xaxis.GetNbins()
        d['nbins'] = nbins
        
        for i in range(nbins):
            d['values'].append(obj.GetBinContent(i))
            d['binning'].append((xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i)))
            d['uncertainties'].append((obj.GetBinErrorLow(i), obj.GetBinErrorUp(i)))

    if obj_class[0:3] == 'TH2':
       #Same logic for 2D Histograms
        d['xbinning'] =  list()
        d['ybinning'] =  list()

        xnbins = xaxis.GetNbins()
        ynbins = yaxis.GetNbins()
       
        for i in range(xnbins):
            for j in range(xnbins):
                d['values'].append(obj.GetBinContent(i,j))
                d['xbinning'].append((xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i)))
                d['ybinning'].append((yaxis.GetBinLowEdge(j), yaxis.GetBinUpEdge(j)))
                d['uncertainties'].append((obj.GetBinErrorLow(i,j), obj.GetBinErrorUp(i,j)))
               

    return d


def list_file(filename):
    """Return a list of keys, as strings, in `filename`.

    Keyword arguments:
    filename -- Name of file with full path, e.g. `/a/b/my_file.root`
    """
    f = ROOT.TFile(filename)
    if f.IsZombie():
        d = dict(
            success=False,
            message='Could not open file `{0}`'.format(filename)
        )
    else:
        d = dict(
            success=not f.IsZombie(),
            data=dict(
                filename=filename,
                keys=[key.GetName() for key in f.GetListOfKeys()]
            )
        )
    f.Close()
    return d



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
    print ">>>> get_info('uid') : ", get_info('uid')
    print ">>>> ROOT file : ", settings.getHistoROOTFileName()
    print ">>>> ROOT reference file : ",settings.actualROOTReferenceFile
    f = ROOT.TFile(filename)

    d = eval(cppyy.gbl.getDictionary(f,key_name))
    
    print d
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
            subd["data"] = eval(cppyy.gbl.getDictionary(f,k["histogram"]))
            if rfn != k["referenceFile"]: 
                rfn = k["referenceFile"]
                settings.setReferenceROOTFileName(rfn)
                rf = ROOT.TFile(rfn)
            subd["refdata"] = eval(cppyy.gbl.getDictionary(rf,k["reference"]))
            d['elements'].append(subd)


    print d
#    is_reference = json_data['is_reference']
#    filename = json_data['filename']
#    key_name = json_data['key_name']
#
#    
#    settings.setOptionsFile(get_info('uid'))
#    print ">>>> get_info('uid') : ", get_info('uid')
#    print ">>>> ROOT file : ", settings.getHistoROOTFileName()
#    print ">>>> ROOT reference file : ",settings.actualROOTReferenceFile
#    f = ROOT.TFile(filename)
#
#    d = eval(cppyy.gbl.getDictionary(f,key_name))
#    
#    print d
#    f.Close()
    return jsonify(d)
