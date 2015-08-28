import cppyy
from ROOT import *

cppyy.gbl.gSystem.Load("libHistograms.so")
cppyy.gbl.gInterpreter.Declare

cppyy.gbl.gInterpreter.Declare('#include "libHistograms.h"')
f = TFile("histograms.root");
o = f.Get("histogram_0")

a = cppyy.gbl.getInfo(o)


d = eval(a)
print d
print d['key_data']['numberEntries']
