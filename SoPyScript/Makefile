CXXFLAGS=-g -Wall
COIN_CXXFLAGS=`soqt-config --cppflags`
COIN_LDFLAGS=`soqt-config --libs --ldflags`

PYTHON_INCS=-I`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_inc()"`
PYTHON_LIBDIR=`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_lib()"`
PYTHON_LIBS=`python -c "import distutils.sysconfig;print distutils.sysconfig.get_config_vars()['BLDLIBRARY']"`
PIVY_RUNTIME=-L$(PYTHON_LIBDIR) -Wl,-R$(PYTHON_LIBDIR) -lpivy_runtime

%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_INCS) -o $@ $<

all: examin

examin: SoPyScript.o examin.o
	$(CXX) $(COIN_LDFLAGS) $(PYTHON_LIBS) $(PYTHON_LDFLAGS) $(PIVY_RUNTIME) -o $@ $^

SoPyScript.o: SoPyScript.h

.PHONY: clean
clean:
	-rm -f *~ *.o examin
