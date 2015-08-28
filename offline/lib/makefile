CXX           = g++
SOFLAGS       = -Wall -fPIC -shared -rdynamic -O3 -g

ROOTCFLAGS    = $(shell $(ROOTSYS)/bin/root-config --cflags)
ROOTLIBS      = $(shell $(ROOTSYS)/bin/root-config --libs)
ROOTINC      = -I$(shell $(ROOTSYS)/bin/root-config --incdir)

#BOOSTLIB      = -L/cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_76root6/Boost/1.55.0_python2.7/x86_64-slc6-gcc48-opt/lib 
#BOOSTINC      = -I/cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_76root6/Boost/1.55.0_python2.7/x86_64-slc6-gcc48-opt/include/boost-1_55/

PYTHONLIB     = -L/cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_76root6/Python/2.7.9.p1/x86_64-slc6-gcc48-opt/lib
PYTHONINC     = -I/cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_76root6/Python/2.7.9.p1/x86_64-slc6-gcc48-opt/include/python2.7/

#LIBS          = $(ROOTCFLAGS) $(BOOSTLIB) $(PYTHONLIB) $(ROOTLIBS) 
#INCS          = $(BOOSTINC) $(PYTHONINC)
LIBS          = $(ROOTCFLAGS) $(PYTHONLIB) $(ROOTLIBS) 
INCS          = $(PYTHONINC)
SOURCES       = $(shell echo *.cpp)
HEADERS       = $(shell echo *.h)
OBJECTS       = $(SOURCES:.cpp=.so)

TARGET        = libDQM.so

%.so:%.cpp
	$(CXX) $(SOFLAGS) $(LIBS) $(INCS) -o $@ $^

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(SOFLAGS) -o $@ $^ 

test: libHistograms.so test.C
	$(CXX) -g $(LIBS) $(INC) -o test.exe $^ 

clean:
	rm -f $(OBJECTS) $(TARGET)
