#!/usr/bin/python2.7

import os
import sys, traceback
from config import *

from sqlalchemy import Column, ForeignKey, Integer, String, Float, SmallInteger, Boolean, SmallInteger, create_engine, func, distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref, composite, configure_mappers
from sqlalchemy.dialects.oracle import FLOAT,  VARCHAR2
import sqlalchemy.types as types

import pprint

#from errorhandler import *

Base = declarative_base()

def histogramDB_declaration():
    
    class SHOWHISTO(Base):
        __tablename__ = "SHOWHISTO"
            
        SHID = Column(Integer, primary_key = True)
        PAGE = Column(String(350))
        PAGEFOLDER= Column(String(300))
        HISTO = Column(String(12), ForeignKey('HISTOGRAM.HID')) #Reference to HISTOGRAM.HID
    
    
    class HISTOGRAMSET(Base):
        __tablename__ = "HISTOGRAMSET"
        
        HSID = Column(Integer, primary_key = True)
        #NHS = Column(Integer, autoincrement = False)
        HSTITLE = Column(String(100))
        #Algorithm = Column(String(100))
        #HistogramSetName = Column(String(200), unique=True)
        #Type = Column(String(10))
        #TaskName = Column(String(200))
        #Nanalysis = Column(Integer)
        #Description = Column(String(4000))
        #Documentation = Column(String(100))
        #HSDisplay = Column(String(10))
        
    class HISTOGRAM(Base):
        __tablename__ = "HISTOGRAM"
        
        #Unique histogram identifier given by
        #Taskname/Algorithmname/HistogramName
        NAME = Column(String(130), primary_key = True)
        
        #string of max length 12: HSID/IHS
        HID = Column(String(12), unique=True)
        
        Subname = Column(String(50))
        
        DISPLAY = Column(Integer, ForeignKey('DISPLAYOPTIONS.DOID'))
        
        showhistos = relationship("SHOWHISTO")
    
    
    class DISPOPT(types.UserDefinedType):
        def __init__(self, LABEL_X=None, LABEL_Y=None, LABEL_Z=None, YMIN=None, YMAX=None, STATS=None, FILLSTYLE=None, 
            FILLCOLOR=None, LINESTYLE=None, LINECOLOR=None, LINEWIDTH=None, DRAWOPTS=None, XMIN=None, XMAX=None, ZMIN=None, 
            ZMAX=None, LOGX=None, LOGY=None, LOGZ=None, TIMAGE=None, REF=None, REFRESH=None, TIT_X_SIZE=None, TIT_X_OFFS=None, 
            TIT_Y_SIZE=None, TIT_Y_OFFS=None, TIT_Z_SIZE=None, TIT_Z_OFFS=None, LAB_X_SIZE=None, LAB_X_OFFS=None, LAB_Y_SIZE=None, 
            LAB_Y_OFFS=None, LAB_Z_SIZE=None, LAB_Z_OFFS=None, GRIDX=None, GRIDY=None, THETA=None, PHI=None, CNTPLOT=None, 
            DRAWPATTERN=None, STAT_X_SIZE=None, STAT_X_OFFS=None, STAT_Y_SIZE=None, STAT_Y_OFFS=None, HTIT_X_SIZE=None, 
            HTIT_X_OFFS=None, HTIT_Y_SIZE=None, HTIT_Y_OFFS=None, NDIVX=None, NDIVY=None, MARKERSIZE=None, MARKERCOLOR=None, 
            MARKERSTYLE=None, NORM=None, TICK_X=None, TICK_Y=None, MARGIN_TOP=None, MARGIN_BOTTOM=None, MARGIN_LEFT=None, 
            MARGIN_RIGHT=None, PADCOLOR=None, STATTRANSP=None, REFDRAWOPTS=None, SPAREI1=None, SPAREI2=None, SPAREF1=None, 
            SPAREF2=None, SPARES=None, NOTITLE=None, SHOWTITLE=None):
         
            self.LABEL_X = LABEL_X
            self.LABEL_Y = LABEL_Y
            self.LABEL_Z = LABEL_Z
            self.YMIN = YMIN
            self.YMAX = YMAX
            self.STATS = STATS
            self.FILLSTYLE = FILLSTYLE
            self.FILLCOLOR = FILLCOLOR
            self.LINESTYLE = LINESTYLE
            self.LINECOLOR = LINECOLOR
            self.LINEWIDTH = LINEWIDTH
            self.DRAWOPTS = DRAWOPTS
            self.XMIN = XMIN
            self.XMAX = XMAX
            self.ZMIN = ZMIN
            self.ZMAX = ZMAX
            self.LOGX = LOGX
            self.LOGY = LOGY
            self.LOGZ = LOGZ
            self.TIMAGE = TIMAGE
            self.REF = REF
            self.REFRESH = REFRESH
            self.TIT_X_SIZE = TIT_X_SIZE
            self.TIT_X_OFFS = TIT_X_OFFS
            self.TIT_Y_SIZE = TIT_Y_SIZE
            self.TIT_Y_OFFS = TIT_Y_OFFS
            self.TIT_Z_SIZE = TIT_Z_SIZE
            self.TIT_Z_OFFS = TIT_Z_OFFS
            self.LAB_X_SIZE = LAB_X_SIZE
            self.LAB_X_OFFS = LAB_X_OFFS
            self.LAB_Y_SIZE = LAB_Y_SIZE
            self.LAB_Y_OFFS = LAB_Y_OFFS
            self.LAB_Z_SIZE = LAB_Z_SIZE
            self.LAB_Z_OFFS = LAB_Z_OFFS
            self.GRIDX = GRIDX
            self.GRIDY = GRIDY
            self.THETA = THETA
            self.PHI = PHI
            self.CNTPLOT = CNTPLOT
            self.DRAWPATTERN = DRAWPATTERN
            self.STAT_X_SIZE = STAT_X_SIZE
            self.STAT_X_OFFS = STAT_X_OFFS
            self.STAT_Y_SIZE = STAT_Y_SIZE
            self.STAT_Y_OFFS = STAT_Y_OFFS
            self.HTIT_X_SIZE = HTIT_X_SIZE
            self.HTIT_X_OFFS = HTIT_X_OFFS
            self.HTIT_Y_SIZE = HTIT_Y_SIZE
            self.HTIT_Y_OFFS = HTIT_Y_OFFS
            self.NDIVX = NDIVX
            self.NDIVY = NDIVY
            self.MARKERSIZE = MARKERSIZE
            self.MARKERCOLOR = MARKERCOLOR
            self.MARKERSTYLE = MARKERSTYLE
            self.NORM = NORM
            self.TICK_X = TICK_X
            self.TICK_Y = TICK_Y
            self.MARGIN_TOP = MARGIN_TOP
            self.MARGIN_BOTTOM = MARGIN_BOTTOM
            self.MARGIN_LEFT = MARGIN_LEFT
            self.MARGIN_RIGHT = MARGIN_RIGHT 
            self.PADCOLOR = PADCOLOR
            self.STATTRANSP = STATTRANSP
            self.REFDRAWOPTS = REFDRAWOPTS
            self.SPAREI1 = SPAREI1
            self.SPAREI2 = SPAREI2
            self.SPAREF1 = SPAREF1
            self.SPAREF2 = SPAREF2
            self.SPARES = SPARES
            self.NOTITLE = NOTITLE
            self.SHOWTITLE = SHOWTITLE
    
    
        def get_col_spec(self):
            return "DISPOPT(%s)" % ','.join([self.LABEL_X, self.LABEL_Y, self.LABEL_Z, self.YMIN, self.YMAX, self.STATS, 
                self.FILLSTYLE, self.FILLCOLOR, self.LINESTYLE, self.LINECOLOR, self.LINEWIDTH, self.DRAWOPTS, self.XMIN, 
                self.XMAX, self.ZMIN, self.ZMAX, self.LOGX, self.LOGY, self.LOGZ, self.TIMAGE, self.REF, self.REFRESH, 
                self.TIT_X_SIZE, self.TIT_X_OFFS, self.TIT_Y_SIZE, self.TIT_Y_OFFS, self.TIT_Z_SIZE, self.TIT_Z_OFFS, 
                self.LAB_X_SIZE, self.LAB_X_OFFS, self.LAB_Y_SIZE, self.LAB_Y_OFFS, self.LAB_Z_SIZE, self.LAB_Z_OFFS, 
                self.GRIDX, self.GRIDY, self.THETA, self.PHI, self.CNTPLOT, self.DRAWPATTERN, self.STAT_X_SIZE, self.STAT_X_OFFS, 
                self.STAT_Y_SIZE, self.STAT_Y_OFFS, self.HTIT_X_SIZE, self.HTIT_X_OFFS, self.HTIT_Y_SIZE, self.HTIT_Y_OFFS, 
                self.NDIVX, self.NDIVY, self.MARKERSIZE, self.MARKERCOLOR, self.MARKERSTYLE, self.NORM, self.TICK_X, self.TICK_Y, 
                self.MARGIN_TOP, self.MARGIN_BOTTOM, self.MARGIN_LEFT, self.MARGIN_RIGHT, self.PADCOLOR, self.STATTRANSP, 
                self.REFDRAWOPTS, self.SPAREI1, self.SPAREI2, self.SPAREF1, self.SPAREF2, self.SPARES, self.NOTITLE, self.SHOWTITLE])
    
        def bind_processor(self, dialect):
            def process(value):
                return value
            return process
    
        def result_processor(self, dialect, coltype):
            def process(value):
                return value
            return process
    
        
    class DISPLAYOPTIONS(Base):
        __tablename__ = "DISPLAYOPTIONS"
        
        DOID = Column(Integer, primary_key = True)
        
        OPT = Column(DISPOPT)
        
        histogramms = relationship("HISTOGRAM")
        
        
    class HistoDBconnection:
        
#        def __init__(self, errorhandler):
#            self.err = errorhandler

        def __init__(self):
            configure_mappers()
            engine = create_engine(os.environ["HISTODB_PATH"])
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)                
            self.session = DBSession()

        def connectToDB(self):
#
            """
            Sets up the connection to the database and initialises a connection check.
            """
            try:
#                configure_mappers()
#                engine = create_engine(HISTODB_PATH)
#                Base.metadata.bind = engine
#                DBSession = sessionmaker(bind=engine)
#                
#                self.session = DBSession()
                return self.checkDBConnection()
                
            except Exception as inst:
#                self.err.rethrowException(inst)
                print inst
                return False
                
        def checkDBConnection(self):
            """
            Checks DB connectivity.
            """
            try:
                #this checks DB Connection
                self.session.connection()
                
                return True
            except Exception as inst:
#                self.err.rethrowException(inst)
                print inst
                return False
            
        def generateMenuList(self, filterText=None):
            """
            Queries the DB for the list of PAGEs to be displayed. Uses DISTINCT because DB contains
            /a/b -> Histo #1
            /a/b -> Histo #2
            /a/c ...
            entries for each histogram to be displayed per page. When we are just looking for PAGEs, we want to see
            /a/b
            /a/c
            
            this list is then split by "/" and gets \n and \r removed. The return is produced by makeMenuList, transforming this list into
            a tree like python structure.
            try:
            """
            try:
                menu = list()
                if filterText != None:
                    menu = self.session.query(distinct(SHOWHISTO.PAGE).label("PAGE")).filter(SHOWHISTO.PAGE.ilike("%"+filterText+"%")).order_by(SHOWHISTO.PAGE).all()
                    print menu
                #else:
                #       menu = self.session.query(distinct(SHOWHISTO.PAGE).label("PAGE")).order_by(SHOWHISTO.PAGE).all()
                else:
                    menu = self.session.query(SHOWHISTO, HISTOGRAM).join(HISTOGRAM).limit(10).all()
                    print menu
                treeList = []
                i = 0
                while i < len(menu):
                    treeList.append(menu[i].PAGE.rstrip('\n').rstrip('\r').split('/'))
                    i += 1
                    
                return self.makeMenuList(treeList)

            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
            
        def makeMenuList(self,menu):
            """
            Called by generateMenuList above and receives the preprocessed list of PAGEs as a parameter, i.e. a list
            [
            [, a, b]
            [, a, c]
            ]
    
            and return a tree like python structure. Webmonitor:generateMenuRecursion then generates the JSON string out of
            this return value.
            """
            try:
                l = list()
    
                #index of current line < len(menu)
                line = 0
    
                #keep in mind the last folder name and the line index, when this name firt occurred
                lastValue = None
                startLine = 0
    
                # as long as we have elements in the loop
                while line < len(menu):
                    #access current line
                    parts = menu[line]
    
                    # if we encounter a tree leaf and last node was also a tree leaf
                    # we just add this leaf and don't care for children
                    if len(menu[line]) == 1 and line == startLine:
                        #append leaf to list
                        lastValue = parts[0]
                        l.append({lastValue: ["end"]})
        
                        #assume that line is not the last line, if so, ignore the exception, while loop will terminate afterwards
                        try:
                            lastValue = menu[line+1][0]
                        except:
                            pass
            
                        #for further processing: ignore leaf, as it has already been appended to the list
                        line += 1
                        startLine = line
                        #continue while loop
                        continue    
                    # if we encounter a tree leaf and last node was not a tree leaf
                    # we first care for the prior nodes and then just add this leaf
                    elif len(menu[line]) == 1 and line != startLine:
                        # look now into the children of a
                        # recursion would get in the example
                        # /b
                        # /c
                        # because /a is thrown away each iteration
                        children = self.makeMenuList(menu[startLine:line])
                        #assuming that there is an entry in the list corresponding to last value
                        #why try?
                        #because 
                        #/1
                        #/a/b
                        #would go wrong
                        try:
                            l[len(l) -1][lastValue].extend(children)
                        #in case this entry is not there: add it!
                        except:
                            l.append({lastValue: children})
        
                        #append leaf to list
                        lastValue = parts[0]
                        l.append({lastValue: ["end"]})
        
                        #assume that line is not the last line, if so, ignore the exception, while loop will terminate afterwards
                        try:
                            lastValue = menu[line+1][0]
                        except:
                            pass
            
                        #for further processing: ignore leaf, as it has already been appended to the list
                        line += 1
                        startLine = line
                        #continue while loop
                        continue
                
                
                    # if we are in the first loop, initialise variables
                    elif lastValue == None:
                        #save folder name
                        lastValue = parts[0]
                        startLine = 0
                        #start with root entry
                        dictionary = {lastValue: list()}
                        l.append(dictionary)
                    #we have encountered a folder name, deviating from the folder name we had before
                    #example
                    #/a/b
                    #/a/c
                    #/e/d
                    #remark: / is no more present due to split("/")!
                    elif  lastValue != parts[0]:
                        # look now into the children of a
                        # recursion would get in the example
                        # /b
                        # /c
                        # because /a is thrown away each iteration
                        children = self.makeMenuList(menu[startLine:line])
                        #assuming that there is an entry in the list corresponding to last value
                        #why try?
                        #because 
                        #/1
                        #/a/b
                        #would go wrong
                        try:
                            l[len(l) -1][lastValue].extend(children)
                        #in case this entry is not there: add it!
                        except:
                            l.append({lastValue: children})
        
                        #start remembering the new folder
                        lastValue = parts[0]
                        startLine = line
                        dictionaryNew = {lastValue: list()}
                        l.append(dictionaryNew)
                
                        lastWasLeafFlag = False
    
                    #throw away first column of current line
                    menu[line] = menu[line][1:]
                    #increase line index
                    line += 1
    
                #do the same as in loop, because the last line might not have been added yet.
                if startLine < line:
                    children = self.makeMenuList(menu[startLine:line])
                    try:
                        l[len(l) -1][lastValue].extend(children)
                    except:
                        l.append({lastValue: children})
    
                return l
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None
        
        def getHistosInPath(self, path):
            """
            Returns a list of HISTOGRAM.NAMEs for contained in each path. i.e.
            for the path /a/b
            you can find several entries in the DB, each corresponding to one histogramm, which can be retreived by a JOIN from SHOWHISTO 
            to HISTOGRAM via SHID
            so for 
            /a/b SHID=1
            /a/b SHID=2
            we can find two histograms to be displayed.
            """
            try:
                return self.session.query(SHOWHISTO.SHID, HISTOGRAM.NAME, HISTOGRAM.DISPLAY, SHOWHISTO.PAGE, HISTOGRAM.HID, DISPLAYOPTIONS.OPT).\
                    join(HISTOGRAM, HISTOGRAM.HID == SHOWHISTO.HISTO).\
                    outerjoin(DISPLAYOPTIONS, DISPLAYOPTIONS.DOID == HISTOGRAM.DISPLAY).\
                    filter(SHOWHISTO.PAGE == path).\
                    order_by(HISTOGRAM.NAME).\
                    all()
            except Exception as inst:
#                self.err.rethrowException(inst)
                return None

    return HistoDBconnection();

            
#if __name__ == '__main__':
#    #Setup Error handling and logging
#    err = errorhandler(None)
#    connection = HistoDBconnection(err)
#    dbStatus = connection.connectToDB()
#    print dbStatus
