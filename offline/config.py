import os

from offline import histogramDB_declaration
from offline import bookKeepingDB

# Application name, used in page titles etc.
APP_NAME = 'LHCb DQM'

# Description, shown in the <meta> tag
APP_DESCRIPTION = 'An example app based on the WebMonitor.'

# List of emails to send ERROR messages to
ADMINS = ['flavio.archilli@cern.ch','denis.derkach@cern.ch']

# Mappings of parent paths to their default children
# The key represents the visited path, the value is the page that's served
# For the dict below, a visited path of `examples` will show the
# `examples/table` page, as an example
DEFAULT_CHILDREN = {
    '/' : 'offline_bp/',
#    '': 'home',
}

# Format string to generate LFN used in bookkeeping
LFN_FORMAT_STRING = 'root://castorlhcb.cern.ch//castor/cern.ch/grid/lhcb/LHCb/%s/HIST/%s/BrunelDaVinci_%s_%s_Hist.root?svcClass=lhcbdisk'

# Base path to generate path to reference in afs used in bookkeeping
REFERENCE_BASE_PATH = "/afs/cern.ch/lhcb/group/dataquality/ROOT/REFERENCE/FULL/"

# Constants from the former presenter, regarding the normalisation of references
s_Area = "AREA";
s_Entries = "ENTR";
s_NoReference = "NOREF";
s_NoNormalization = "NONE";

# Contains the path to the histoDB, used in DBdeclaration.py
HISTODB_PATH = os.environ["HISTODB_PATH"]

HISTODB = histogramDB_declaration.histogramDB_declaration()
BKKDB = bookKeepingDB.bookKeepingDB()

# Debug mode
DEBUG = True

