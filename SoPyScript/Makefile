PYTHON_FLAGS=-I`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_inc()"`
CXXFLAGS=-g -Wall
COIN_CXXFLAGS=`soqt-config --libs --cppflags --ldflags`
PIVY_RUNTIME=-L/usr/lib/python2.3/site-packages -Wl,-R/usr/lib/python2.3/site-packages -lpivy_runtime

all: examin

examin: SoPyScript.o examin.cpp
	$(CXX) $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_FLAGS) $(PIVY_RUNTIME) -lpython2.3 -o examin SoPyScript.o examin.cpp

SoPyScript.o: SoPyScript.h SoPyScript.cpp sopyscript_wrap.cxx
	$(CXX) $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_FLAGS) -c SoPyScript.cpp

sopyscript_wrap.cxx: SoPyScript.i
	swig -w302,306,307,312,389,361,362,503,509,510 -noruntime -v -c++ -python -includeall -D__PIVY__ -I.. -I../fake_headers -I/usr/local/include -I/usr/include -interface _sopyscript -o sopyscript_wrap.cxx SoPyScript.i
	$(CXX) $(CXXFLAGS) $(COIN_CXXFLAGS) $(PYTHON_FLAGS) $(PIVY_RUNTIME) -shared sopyscript_wrap.cxx -o _sopyscript.so

clean:
	rm -f *~ *.o sopyscript_wrap.cxx
