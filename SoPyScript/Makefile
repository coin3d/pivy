PYTHON_FLAGS=-I`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_inc()"`
CXXFLAGS=-g -Wall
COIN_CXXFLAGS=`soqt-config --libs --cppflags --ldflags`
PIVY_RUNTIME=-L/usr/lib/python2.3/site-packages -Wl,-R/usr/lib/python2.3/site-packages -lpivy_runtime

all: examin

examin: SoPyScript.o examin.cpp
	$(CXX) $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_FLAGS) $(PIVY_RUNTIME) -lpython2.3 -o examin SoPyScript.o examin.cpp

SoPyScript.o: SoPyScript.h SoPyScript.cpp
	$(CXX) $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_FLAGS) -c SoPyScript.cpp

clean:
	rm -f *~ *.o
