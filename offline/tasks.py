import os
import cppyy
import ROOT
ROOT.std.__file__ = 'dummy'

cppyy.gbl.gSystem.Load("lib/libHistograms.so")
cppyy.gbl.gInterpreter.Declare('#include <offline/lib/libHistograms.h>')

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
            for j in range(ynbins):
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


def get_key_from_file(filename, key_name):
    """Return the object, stored under `key_name`, in `filename`.

    Keyword arguments:
    filename -- Name of file with full path, e.g. `/a/b/my_file.root`
    key_name -- Name of key object is stored as
    """
    filename = add_file_extension(filename)
    f = ROOT.TFile(filename)

#    if f.IsZombie():
#        return dict(
#            success=False,
#            message='Could not open file `{0}`'.format(filename)
#        )
#    obj = f.Get(key_name)
#    if not obj:
#        d = dict(
#            success=False,
#            message='Could not find key `{1}` in file `{0}`'.format(
#                filename, key_name
#            )
#        )
#    else: 
#        d = dict(
#            success=True,
#            data=dict(
#                filename=filename,
#                key_name=obj.GetName(),
#                key_title=obj.GetTitle(),
#                key_class=obj.ClassName(),
#                key_data=data_for_object(obj, filename)
#            )
#        )

#        key_dict = eval(cppyy.gbl.getInfo(obj))
#
#        key_dict['filename'] = filename
#        d = dict(
#            success=True,
#            data=key_dict
#            )

    d = eval(cppyy.gbl.getDictionary(f,key_name))
#    d['data']['filename'] = filename

        
    f.Close()
    return d
