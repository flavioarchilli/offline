import sqlalchemy
from sqlalchemy     import Table, Column
from sqlalchemy     import Integer, Sequence, String
from sqlalchemy     import ForeignKey, UniqueConstraint
from sqlalchemy     import MetaData
from sqlalchemy     import exc, desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from os import environ 

Base = declarative_base()

context_data_file = Table('context_data_file', Base.metadata,
                      Column('contextId',  Integer, ForeignKey('context.contextId'),    nullable = False),
                      Column('dataFileId', Integer, ForeignKey('data_file.dataFileId'), nullable = False)
                      )

run_data_file = Table('run_data_file', Base.metadata,
                      Column('runNumber',  Integer, ForeignKey('run.runNumber'),        nullable = False),
                      Column('dataFileId', Integer, ForeignKey('data_file.dataFileId'), nullable = False)
                      )
context_ref_file = Table('context_ref_file', Base.metadata,
                      Column('contextId',  Integer, ForeignKey('context.contextId'),       nullable = False),
                      Column('refFileId', Integer, ForeignKey('reference_file.refFileId'), nullable = False)
                      )

run_ref_file = Table('run_ref_file', Base.metadata,
                      Column('runNumber',  Integer, ForeignKey('run.runNumber'),           nullable = False),
                      Column('refFileId', Integer, ForeignKey('reference_file.refFileId'), nullable = False)
                      )

class Context(Base):
    __tablename__ = 'context'

    contextId   = Column(Integer, Sequence('contextId_seq'), primary_key=True)
    contextName = Column(String(40), unique=True, nullable=False)

    dataFiles = relationship('DataFile',
                             secondary=context_data_file,
                             backref=backref('contexts', uselist=True)
                             )

    refFiles = relationship('ReferenceFile',
                            secondary=context_ref_file,
                            backref=backref('contexts', uselist=True),
                            uselist=True
                            )

    def __repr__(self):
        return "<Context(contextName='%s)'>" %(self.contextName)

class Run(Base):
    __tablename__ = 'run'

    runNumber = Column(Integer, primary_key=True)
    fillId    = Column(Integer, ForeignKey('fill.id'), nullable=True)

    dataFile = relationship('DataFile',
                            secondary=run_data_file,
                            backref=backref('run', uselist=False)
                            )

    refFiles = relationship('ReferenceFile',
                            secondary=run_ref_file,
                            backref=backref('runs', uselist=True),
                            uselist=True
                            )

    def __repr__(self):
        return "<Run(runNumber='%s')>" %(str(self.runNumber))

class Fill(Base):
    __tablename__ = 'fill'

    id   = Column(Integer, primary_key=True)
    runs = relationship(Run, backref=backref('fill'), uselist=True)

    def __repr__(self):
        return "<Fill(number='%s')>" %(str(self.id))

 
class DataFile(Base):
    __tablename__ = 'data_file'

    dataFileId   = Column(Integer, Sequence('datafile_id_seq'), primary_key=True)
    dataFilePath = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return "<DataFile(dataFilePath='%s')>" %(self.dataFilePath)
    
class ReferenceFile(Base):
     __tablename__ = 'reference_file'
 
     refFileId   = Column(Integer, Sequence('refFile_id_seq'), primary_key=True)
     refFilePath = Column(String(255), unique=True, nullable=False)
 
     def __repr__(self):
         return "<ReferenceeFile(refFilePath='%s')>" %(self.refFilePath)

class dataqualityDB:
    def __init__(self):
        self.address = 'oracle://' + environ["DQDBLOGIN"] + ':' \
                                   + environ["DQDBPWD"] + '@'   \
                                   + environ["DQDBTNS"]

        self.engine       = sqlalchemy.create_engine(self.address)
        self.engine.echo  = False
        self.conn         = self.engine.connect()
        self.base         = Base()

        self.base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.onlineDQContextName = 'OnlineDQ'
        return
        
    def addOnlineDQFile(self, run, path):
        dataFile     = self.insertDataFile(path)
        dataFile.run = run
        
        hasOnlineDQ = False
        for c in dataFile.contexts:
            if c.contextName == self.onlineDQContextName:
                hasOnlineDQ = True

        if not hasOnlineDQ:
            context = self.getContext(self.onlineDQContextName)
            dataFile.contexts.append(context)

        self.session.add(dataFile)
        return dataFile

    def addOnlineDQRefFile(self, run, path):
        refFile = self.insertRefFile(path)

        hasRun = False
        for r in refFile.runs:
            if r.runNumber == run.runNumber:
                hasRun = True
                break
                
        
        hasOnlineDQ = False
        for c in refFile.contexts:
            if c.contextName == self.onlineDQContextName:
                hasOnlineDQ = True
                break

        if not hasRun:
            refFile.runs.append(run)

        if not hasOnlineDQ:
            context = self.getContext(self.onlineDQContextName)
            refFile.contexts.append(context)

        self.session.add(refFile)
        return refFile

    def commit(self):
        self.session.commit()
        return

    def create_all(self):
        self.base.metadata.create_all(bind=self.engine)
        print self.base.metadata.tables.keys()
        return

    def drop_all(self):
        self.commit()
        self.base.metadata.drop_all(bind=self.engine)
        return

    def drop_table(self, table):
        smt = "DROP TABLE \"%s\"" %(table)
        s = self.conn.execute(smt)
        for r in s:
            print r
        return

    def rollback(self):
        self.session.rollback()
        return

    def getContext(self, name):
        return self.session.query(Context).filter_by(contextName=name).first()

    def getContextId(self, name):
        contextId = None

        s = self.session.query(Context).filter_by(contextName=name)
        for r in s:
            contextId = r.contextId
        return contextId
    
    def getOnlineDQFile(self, runNumber):
        ref = self.getRunFileData(runNumber, self.onlineDQContextName)
        return ref

    def getOnlineDQRef(self, runNumber):
        ref = self.getRunFileRef(runNumber, self.onlineDQContextName)
        return ref

    def getRun(self, runNumber):
        run = self.session.query(Run).filter_by(runNumber=runNumber).first()
        return run

    def getRunFileData(self, runNumber, contextName):
        dataFilePath = None

        dataFile = self.session.query(DataFile).\
            filter(DataFile.run.has(runNumber=runNumber)).\
            filter(DataFile.contexts.any(contextName=contextName)).first()

        if dataFile:
            dataFilePath = dataFile.dataFilePath

        return dataFilePath

    def getRunFileRef(self, runNumber, contextName):
        refFilePath = None

        refFile = self.session.query(ReferenceFile).\
            filter(ReferenceFile.runs.any(runNumber=runNumber)).\
            filter(ReferenceFile.contexts.any(contextName=contextName)).first()

        if refFile:
            refFilePath = refFile.refFilePath

        return refFilePath


    def insertContext(self, name):
        context = self.session.query(Context).filter_by(contextName=name).first()
 
        if context:
            return context
        else:
            context = Context(contextName=name)
            self.session.add(context)
            return context

    def insertDataFile(self, path):
        dataFile = self.session.query(DataFile).filter_by(dataFilePath=path).first()

        if dataFile:
            return dataFile
        else:
            dataFile = DataFile(dataFilePath=path)
            self.session.add(dataFile)
            return dataFile

    def insertFill(self, fillId):
        fill = self.session.query(Fill).filter_by(id=fillId).first()

        if fill:
            return fill
        else:
            fill = Fill(id=fillId)
            self.session.add(fill)
            return fill

    def insertRefFile(self, path):
        refFile = self.session.query(ReferenceFile).filter_by(refFilePath=path).first()

        if refFile:
            return refFile
        else:
            refFile = ReferenceFile(refFilePath=path)
            self.session.add(refFile)
            return refFile

    def insertRun(self, runNumber, fillId):
        run = self.getRun(runNumber)

        if run:
            return run
        else:
            fill = self.insertFill(fillId)
            run  = Run(runNumber=runNumber, fillId=fillId)
            self.session.add(run)
            return run

    def nextOnlineDQRun(self, runNumber):
        nextRun = None
        for row in self.session.query(Run).\
                    filter(Run.runNumber>runNumber).\
                    order_by(Run.runNumber).limit(1):
            nextRun = row.runNumber
        return nextRun

    def prevOnlineDQRun(self, runNumber):
        prevRun = None
        for row in self.session.query(Run).\
                        filter(Run.runNumber<runNumber).\
                        order_by(desc(Run.runNumber)).limit(1):
            prevRun = row.runNumber
        return prevRun

    def updateOnlineDQRef(self, runNumber, refPath):
        refId     = self.getReferenceId(refPath)
        contextId = self.getContextId('OnlineDQ')

        runRef = self._table('runReference')

        handler      = runRef.update()
        handler.bind = self.engine
        h            = handler.where(runNumber=int(runNumber),contextId=contextId).values(refFileId=refId)

        result       = h.execute()
        return

