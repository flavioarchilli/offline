import os

# Application name, used in page titles etc.
APP_NAME = 'Offline DQM'

# Description, shown in the <meta> tag
APP_DESCRIPTION = 'An example app based on the WebMonitor.'

# List of emails to send ERROR messages to
ADMINS = ['flavio.archilli@cern.ch']

# Mappings of parent paths to their default children
# The key represents the visited path, the value is the page that's served
# For the dict below, a visited path of `examples` will show the
# `examples/table` page, as an example
DEFAULT_CHILDREN = {
    '': 'presenter/histoDB',
#    "histoDB" : "histoDB/histoDB"
#    "histoDB" : "histoDB/Overview"
}

#Format string to generate LFN used in bookkeeping
LFN_FORMAT_STRING = 'root://castorlhcb.cern.ch//castor/cern.ch/grid/lhcb/LHCb/%s/HIST/%s/BrunelDaVinci_%s_%s_Hist.root?svcClass=lhcbdisk'

#base path to generate path to reference in afs used in bookkeeping
REFERENCE_BASE_PATH = "/afs/cern.ch/lhcb/group/dataquality/ROOT/REFERENCE/FULL/"

#constants from the former presenter, regarding the normalisation of references
s_Area = "AREA";
s_Entries = "ENTR";
s_NoReference = "NOREF";
s_NoNormalization = "NONE";

#contains the path to the histoDB, used in DBdeclaration.py
HISTODB_PATH = os.environ["HISTODB_PATH"]
