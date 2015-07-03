#try to import faster version first
try:
   import cPickle as pickle
except:
   import pickle
   
import os.path
from config import *
import ROOT
#import pprint

class userSettings:
	def __init__(self, userid = "1" ):
		self.actualROOTFile = None
		self.actualROOTReferenceFile = None
                self.OptionsFileName = "sessions/" + userid + "options.tcl" 
	
	def initFile(self):
		try:
			if not (os.path.exists(self.OptionsFileName) and os.path.isfile(self.OptionsFileName)):
				options = dict()
				options["runNmbr"] = "0"
				options["version"] = ""
				options["histoRootFile"] = ""
				options["referenceRootFile"] = ""
				options["referenceState"] = "deactivated"
	
				optionsFile = open(self.OptionsFileName, "w")
				pickle.dump(options, optionsFile)
				optionsFile.close()
		except Exception as inst:
			self.err.rethrowException(inst)
			return None
		
	def setReferenceState(self,state):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
	
			options["referenceState"] = state
	
			optionsFile = open(self.OptionsFileName, "w")
			pickle.dump(options, optionsFile)
			optionsFile.close()
		except Exception as inst:
			self.err.rethrowException(inst)

	def getReferenceState(self):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
	
			return options["referenceState"]
		except Exception as inst:
			self.err.rethrowException(inst)
			return None
		
	def setHistoROOTFileName(self,rootFile):
		try:
			self.initFile()
			#if we want to store a new file name
			if (rootFile != self.getHistoROOTFileName()):
				optionsFile = open(self.OptionsFileName, "r")
				options = pickle.load(optionsFile)
				optionsFile.close()
	
				options["histoRootFile"] = rootFile
	
				optionsFile = open(self.OptionsFileName, "w")
				pickle.dump(options, optionsFile)
				optionsFile.close()
			
				return self.readInHistoRootFileIfPossible()
			#we the new file name is the same as the old file name
			else:
				#check if the old file was loaded successfully
				return (self.actualROOTFile != None)	
			
		except Exception as inst:
			self.err.rethrowException(inst)
			return False
			
	def readInHistoRootFileIfPossible(self):
		try:
			rootFile = self.getHistoROOTFileName()
			
			if rootFile != None and rootFile != "":
				#open ROOT file
				
				#print "rootFile:"+rootFile
				
				self.actualROOTFile = ROOT.TFile.Open(rootFile)
				
				#pprint.pprint(self.actualROOTFile)
				
				#print "End: rootFile"
				return True
				
		except Exception as inst:
			self.err.rethrowException(inst)
			self.actualROOTReferenceFile = None
			return False
	

	def getHistoROOTFileName(self):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
	
			return options["histoRootFile"]
		except Exception as inst:
			self.err.rethrowException(inst)
			return None
	
	def setReferenceROOTFileName(self,rootFile):
		try:
			self.initFile()
			#if we want to store a new file name
			if rootFile != self.getReferenceROOTFileName():
				optionsFile = open(self.OptionsFileName, "r")
				options = pickle.load(optionsFile)
				optionsFile.close()
	
				options["referenceRootFile"] = rootFile
	
				optionsFile = open(self.OptionsFileName, "w")
				pickle.dump(options, optionsFile)
				optionsFile.close()
			
				return self.readInReferenceRootFileIfPossible()
			#we the new file name is the same as the old file name
			else:
				#check if the old file was loaded successfully
				return (self.actualROOTReferenceFile != None)
		except Exception as inst:
			self.err.rethrowException(inst)
			return False
			
	def readInReferenceRootFileIfPossible(self):
		try:
			referenceFile = self.getReferenceROOTFileName()
			if referenceFile != None and referenceFile != "":
				#open ROOT file
				
				#print "referenceFile:"+referenceFile
				
				self.actualROOTReferenceFile = ROOT.TFile.Open(referenceFile)
				
				#pprint.pprint(self.actualROOTReferenceFile)
				
				#print "End: referenceFile"
				return True
				
		except Exception as inst:
			self.err.rethrowException(inst)
			self.actualROOTReferenceFile = None
			return False
	

	def getReferenceROOTFileName(self):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
			
			
	
			return options["referenceRootFile"]
		except Exception as inst:
			self.err.rethrowException(inst)
			return None

	def setVersion(self,version):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
	
			options["version"] = version
	
			optionsFile = open(self.OptionsFileName, "w")
			pickle.dump(options, optionsFile)
			optionsFile.close()
			
			
		except Exception as inst:
			self.err.rethrowException(inst)

	def getVersion(self):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
			
			
	
			return options["version"]
		except Exception as inst:
			self.err.rethrowException(inst)
			return None

	def setRunNmbr(self,runNmbr):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
	
			options["runNmbr"] = runNmbr
	
			optionsFile = open(self.OptionsFileName, "w")
			pickle.dump(options, optionsFile)
			optionsFile.close()
			
			
		except Exception as inst:
			self.err.rethrowException(inst)

	def getRunNmbr(self):
		try:
			self.initFile()
	
			optionsFile = open(self.OptionsFileName, "r")
			options = pickle.load(optionsFile)
			optionsFile.close()
			
			
	
			return options["runNmbr"]
		except Exception as inst:
			self.err.rethrowException(inst)
			return None