import os
import ROOT


def add_file_extension(filename):
    """Add `.root` extension to `filename`, if it's not already present."""
    return (filename + '.root') if filename[-5:] != '.root' else filename


def tfile_path(filename):
    """Return the path to the TFile with `filename`."""
    here = os.path.dirname(__file__)
    return '{0}/static/files/{1}'.format(here, filename)


def data_for_object(obj):
    """Return a dictionary representing the data inside the object."""
    obj_class = obj.ClassName()
    d = {}
    d['type'] = obj_class[2:]
        
    if obj_class[0:3] == 'TH1' or obj_class[0:3] == 'TProfile':
        # For histograms, we provide
        #   binning: List of 2-tuples defining the (low, high) binning edges,
        #   values: List of bin contents, ith entry falling in the ith bin
        #   uncertainties: List of 2-tuples of (low, high) errors on the values
        #   axis_titles: 2-tuple of (x, y) axis titles
        xaxis = obj.GetXaxis()
        yaxis = obj.GetYaxis()
        nbins = xaxis.GetNbins()
        d['binning'] = [
            (xaxis.GetBinLowEdge(i), xaxis.GetBinUpEdge(i))
            for i in range(nbins)
        ]
        d['values'] = [obj.GetBinContent(i) for i in range(nbins)]
        d['uncertainties'] = [
            (obj.GetBinErrorLow(i), obj.GetBinErrorUp(i))
            for i in range(nbins)
        ]
        d['axis_titles'] = (xaxis.GetTitle(), yaxis.GetTitle())


    if obj_class[0:3] == 'TH2':
       #Same logic for 2D Histograms
        x_axis = obj.GetXaxis()
        num_xbins = x_axis.GetNbins()
        y_axis = obj.GetXaxis()
        num_ybins = y_axis.GetNbins()
       
       
        i = 1
        j = 1
        while i <= num_xbins:
            while j <= num_ybins:
                d['values'].append(obj.GetBinContent(i,j))
                d['xbinning'].append((x_axis.GetBinLowEdge(i), x_axis.GetBinUpEdge(i)))
                d['ybinning'].append((y_axis.GetBinLowEdge(j), y_axis.GetBinUpEdge(j)))
                d['uncertainties'].append([obj.GetBinErrorLow(i,j), obj.GetBinErrorUp(i,j)])

                i += 1
                j += 1
               
            d['axis_titles'] = (x_axis.GetTitle(), y_axis.GetTitle())

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
#    filename = tfile_path(add_file_extension(filename))
    filename = add_file_extension(filename)
    print ">>> get_key_from_file :: filename = {0}".format(filename)
    f = ROOT.TFile(filename)
    

    print f
    if f.IsZombie():
        return dict(
            success=False,
            message='Could not open file `{0}`'.format(filename)
        )
#    obj = None
# This method, opposed to TFile.Get, is more robust against odd key names
#    for key in f.GetListOfKeys():
#        print key
#        if key.GetName() == key_name:
#            print key_name
#            obj = key.ReadObj()
    obj = f.Get(key_name)
    if not obj:
        d = dict(
            success=False,
            message='Could not find key `{1}` in file `{0}`'.format(
                filename, key_name
            )
        )
    else:
        d = dict(
            success=True,
            data=dict(
                filename=filename,
                key_name=obj.GetName(),
                key_title=obj.GetTitle(),
                key_class=obj.ClassName(),
                key_data=data_for_object(obj)
            )
        )
    f.Close()
    return d
