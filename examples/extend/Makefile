OPTS=-shared -fPIC # -O2
# comment out the next line for MacOS X
# OPTS=-bundle -bundle_loader `which python`

PIVY_ROOT=../..

CXXFLAGS+= -I`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_inc()"`
PYTHON_LIBDIR=`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_lib()"`
PIVY_RUNTIME=-L$(PYTHON_LIBDIR) -Wl,-R$(PYTHON_LIBDIR) -lpivy_runtime

all: shapescale

shapescale: _shapescale.so shapescale.pyc

shapescale.pyc: shapescale.py
	python -c "import shapescale"

_shapescale.so: shapescale_wrap.cpp
	g++ $(OPTS) $(CXXFLAGS) `coin-config --cppflags --ldflags --libs` \
            $(PIVY_RUNTIME) -o _shapescale.so shapescale_wrap.cpp ShapeScale.cpp

wrap: shapescale_wrap.cpp

shapescale_wrap.cpp: shapescale.i
	swig -v -noruntime -c++ -python -includeall -D__PIVY__ \
	     -I. -I${PIVY_ROOT} -I${PIVY_ROOT}/fake_headers \
	     -I/usr/local/include -I/usr/include -o shapescale_wrap.cpp shapescale.i

cleanshapescale:
	rm -f _shapescale.so shapescale_wrap.cpp shapescale.py shapescale.pyc

clean:
	rm -f *~ *.so shapescale_wrap.cpp shapescale.py shapescale.pyc
