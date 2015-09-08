import sqlalchemy

from sqlalchemy     import *
from sqlalchemy.orm import sessionmaker

import os

class dataqualityDB:
    def __init__(self):
        print "Dataquality DQ connection initialised"
        self.address = 'oracle://' + os.environ["DQDBLOGIN"] + ':' \
                                   + os.environ["DQDBPWD"] + '@'   \
                                   + os.environ["DQDBTNS"]

        self.engine       = sqlalchemy.create_engine(self.address)
        self.engine.echo  = False
        self.conn         = self.engine.connect()
        self.metadata     = MetaData()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.createTables()

        self.insertRunHandler = None
        return
        
    def addOnlineDQFile(self, run, path):
        runFile = self._table('runFile')

        contextId = self.getContextId('OnlineDQ')
        if contextId == None:
            return

        handler      = runFile.insert()
        handler.bind = self.engine
        h            = handler.values(runNumber=run, contextId=contextId, path=path)

        result = h.execute()
        return

    def createTables(self):
        runTable     = Table('runs', self.metadata,
                             Column('runNumber', Integer, primary_key=True)
                             )
        
        contextTable = Table('context', self.metadata,
                             Column('contextId',   Integer, Sequence('context_id_seq'), primary_key=True),
                             Column('contextName', String(40), unique=True)
                             )
        runFileTable = Table('runFile', self.metadata,
                             Column('runFileId', Integer, Sequence('runFile_id_seq'), primary_key=True),
                             Column('runNumber', Integer, ForeignKey('runs.runNumber')),
                             Column('contextId', Integer, ForeignKey('context.contextId')),
                             Column('path', String(255)),
                             UniqueConstraint('runNumber', 'contextId', name='uix_1')
                             )

        refFileTable = Table('refFile', self.metadata,
                             Column('refFileId', Integer, Sequence('refFile_id_seq'), primary_key=True),
                             Column('path', String(255), unique=True)
                             )

        runRef = Table('runReference', self.metadata,
                       Column('refFileId', Integer, ForeignKey('refFile.refFileId')),
                       Column('runNumber', Integer, ForeignKey('runs.runNumber')),
                       Column('contextId', Integer, ForeignKey('context.contextId')),
                       UniqueConstraint('refFileId', 'runNumber', 'contextId', name='uix_3')
                       )

        runTable.create(self.engine,     checkfirst=True)
        contextTable.create(self.engine, checkfirst=True)
        runFileTable.create(self.engine, checkfirst=True)
        refFileTable.create(self.engine, checkfirst=True)
        runRef.create(self.engine,       checkfirst=True)

        return

    def dropTable(self, name):
        table = self._table(name)
        if table is not None:
            table.drop(self.engine, checkfirst=True)
        return

    def getContextId(self, name):
        context = self._table('context')
        session = self.session

        contextId = None
        name = session.query(context).filter_by(contextName=name)

        for s in name:
            contextId = s[0]

        return contextId

    def getReferenceId(self, path):
        refFile = self._table('refFile')
        session = self.session

        refId = None
        name = session.query(refFile).filter_by(path=path)

        for s in name:
            refId = s[0]

        return refId
        
    def getOnlineDQFile(self, runNumber):
        runFile = self._table('runFile')
        session = self.session

        path     = None
        contextId = self.getContextId('OnlineDQ')
        if contextId == None:
            return path

        filelist = session.query(runFile).filter_by(runNumber=runNumber,contextId=contextId)
        for s in filelist:
            path = s[3]

        return path

    def getOnlineDQRef(self, runNumber):
        ref = self.getRunRef(runNumber, 'OnlineDQ')
        return ref

    def getRunRef(self, runNumber, context ):
        runRef  = self._table('runReference')
        session = self.session

        path     = None
        contextId = self.getContextId(context)
        if contextId == None:
            return path

        refFileId = -1
        filelist  = session.query(runRef).filter_by(runNumber=runNumber,contextId=contextId)

        for s in filelist:
            refFileId = s[0]

        if refFileId < 0:
            return path

        refFile  = self._table('refFile')
        filelist = session.query(refFile).filter_by(refFileId=refFileId)

        for s in filelist:
            path = s[1]

        return path

    def insertContext(self, name):
        context = self._table('context')
        if context is None:
            return False

        session = self.session

        count = session.query(context).filter_by(contextName=name).count()
        if count:
            return True

        handler      = context.insert()
        handler.bind = self.engine
        h            = handler.values(contextName=name)

        result = h.execute()
        return True

    def insertReferenceFile(self, path):
        ref     = self._table('refFile')
        session = self.session

        handler      = ref.insert()
        handler.bind = self.engine
        h            = handler.values(path=path)

        result = h.execute()
        return

    def insertRun(self, runNumber):
        runs    = self._table('runs')
        session = self.session

        count = session.query(runs).filter_by(runNumber=int(runNumber)).count()
        if count:
            return False

        handler      = runs.insert()
        handler.bind = self.engine
        h            = handler.values(runNumber=int(runNumber))

        result = h.execute()
        return True

    def setOnlineDQRef(self, runNumber, refPath):
        refId     = self.getReferenceId(refPath)
        contextId = self.getContextId('OnlineDQ')

        runRef = self._table('runReference')

        handler      = runRef.insert()
        handler.bind = self.engine
        h            = handler.values(runNumber=int(runNumber),
                                      contextId=contextId,
                                      refFileId=refId)
        result = h.execute()
        return

    def updateOnlineDQRef(self, runNumber, refPath):
        refId     = self.getReferenceId(refPath)
        contextId = self.getContextId('OnlineDQ')

        runRef = self._table('runReference')

        handler      = runRef.update()
        handler.bind = self.engine
        h            = handler.where(runNumber=int(runNumber),contextId=contextId).values(refFileId=refId)

        result       = h.execute()
        return

    def _table(self, name):
        retVal = None
        for t in self.metadata.sorted_tables:
            if t.name == name:
                retVal = t
                break
        return retVal
