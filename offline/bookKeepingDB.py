import DIRAC
from DIRAC.Core.Base import Script

#just do it!!
Script.parseCommandLine(ignoreErrors=True)

from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

import pprint
import os
from config import *


def bookKeepingDB():

    class BookkeepingDB:
    
        def __init__(self):
            self.bkClient = BookkeepingClient()
            self.tfClient = TransformationClient()
#            self.err = err
            
            
        def MakeRunLFN(self, runNmbr, cfgVersion, prodId):
            try:
                padding = "%08d" % int(prodId)
    
                lfn = LFN_FORMAT_STRING  %(
                    cfgVersion, runNmbr, runNmbr, padding)
                
                return lfn
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None     
            
        def getTCK(self, runNmbr):
            try:
                print runNmbr
                res = self.getRunsMetadata(runNmbr)
                
                pprint.pprint(res)
                
                if res != None and hasattr(res, 'Value') \
                        and hasattr(res['Value'], runNmbr) \
                        and hasattr(res['Value'][runNmbr], "TCK"):
                    return res['Value'][runNmbr]["TCK"]
                else:
                    return None
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
            
            
        def getRunsMetadata(self, runNmbr):
            try:
                res = self.tfClient.getRunsMetadata(int(runNmbr))
                if res['OK']:
                    return res
                else:
                    return None
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
    
        def getInformation(self, run):
            try:
                res = self.bkClient.getRunInformations(run)
    
                if res['OK']:
                    result = dict()
                
                    val = res['Value']
            
                    result = {"runstart": val.get('RunStart', 'Unknown'), "runend": val.get('RunEnd', 'Unknown'),
                        "configname": val.get('Configuration Name', 'Unknown'), "configversion": val.get('Configuration Version', 'Unknown'),
                        "fillnb" : val.get('FillNumber', 'Unknown'), "datataking" : val.get('DataTakingDescription', 'Unknown'),
                        "datataking" : val.get('DataTakingDescription', 'Unknown'), "processing" : val.get('ProcessingPass', 'Unknown'),
                        "stream" : val.get('Stream', 'Unknown'), "fullstat" : val.get('FullStat', 'Unknown'), 
                        "nbofe" : val.get('Number of events', 'Unknown'), "nboff" : val.get('Number of file', 'Unknown'),
                        "fsize" : val.get('File size', 'Unknown')
            
                    }
            
                    return result
                else:
                    self.errorMessage("error in bkClient Connection")
                    return None
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
                
        def getListOfRecos(self, runNmbr):
            try:
                d = {'RunNumber' : runNmbr}
        
                res = self.bkClient.getRunAndProcessingPass(d)
        
                results = list()
        
                if res['OK'] == True:
                    recosList = res["Value"]
            
                    for recoEntry in recosList:
                        recoPath = recoEntry[1]
                
                        if recoEntry[0] == runNmbr \
                            and recoPath.count("/") == 2 \
                            and "Reco" in recoPath :
                    
                            results.append(recoPath)
            
                    return results
                else:
                    pprint.pprint(res)
                    self.errorMessage("error in bkClient Connection")
                    return None
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
            
        def getProcessId(self, runNmbr, recoVersion):
            try:
                d = {'RunNumber' : runNmbr,
                'ProcessingPass':  recoVersion}
        
                res = self.bkClient.getProductionsFromView(d)
        
                if res["OK"] == True:
                    return res["Value"][0][0]
                else:
                    self.errorMessage("error in bkClient Connection")
                    return None
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
                
        #recoVersion is just Reco13 and not the full path!!
        def makeReferenceROOTFileName(self, recoVersion, runNmbr):
            try:
                basePath = REFERENCE_BASE_PATH + recoVersion +"/"
            
                #nasty stuff!!
                #the problem is tck retrieved from db
                #0x790038
                #but in the file it looks like
                #TCK_0x00760037_1.root
                #so do padding here
                tck = self.getTCK(runNmbr)
                
                #sometimes no tck set, then take default file
                if tck != None:
                    tckDecimal = int(tck, 0)
                    tckHexPaddedFileName = "TCK_0x" + str(format(tckDecimal, '08x')) + "_"
            
                #if we have multiple files like
                #TCK_0x00790038_1.root
                #TCK_0x00790038_2.root
                #we want the file with the highest subindex, so in this example _2
                possibleTCKList = list()
            
                #store all possible files
                for file in os.listdir(basePath):
                    if tck != None \
                    and file.endswith(".root") \
                    and file != "default_1.root" \
                    and tckHexPaddedFileName in file:
                        possibleTCKList.append(file)
    
                #if we haven't foun anything, look for the default files and choose the one with the highest index
                if len(possibleTCKList) == 0:
            
                    #store all possible files
                    for file in os.listdir(basePath):
                        if file.endswith(".root") \
                        and "default_" in file:
                            possibleTCKList.append(file)
            
                #now sort this list, to find the highest subindex               
                possibleTCKList.sort()
    
                return basePath+possibleTCKList.pop()
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None

    return BookkeepingDB() 
