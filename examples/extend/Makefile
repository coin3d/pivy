CXXFLAGS+= -I`python -c "import distutils.sysconfig;print distutils.sysconfig.get_python_inc()"`

OPTS=-shared -fPIC # -O2
# comment out the next line for MacOS X
# OPTS=-bundle -bundle_loader `which python`

PIVY_ROOT=../../..

all: shapescale

shapescale: _shapescale.so shapescale.pyc

shapescale.pyc: shapescale.py
	python -c "import shapescale"

_shapescale.so: shapescale_wrap.cxx
	g++ $(OPTS) $(CXXFLAGS) `coin-config --cppflags --ldflags --libs` -lswigpy \
	    ShapeScale.cpp -o _shapescale.so shapescale_wrap.cxx 

wrap: shapescale_wrap.cxx

shapescale_wrap.cxx: shapescale.i
	swig -v -c -c++ -python -includeall -D__PIVY__ -I. -I${PIVY_ROOT} \
		-I${PIVY_ROOT}/fake_headers -I/usr/local/include \
		-o shapescale_wrap.cxx shapescale.i

cleanshapescale:
	rm -f _shapescale.so shapescale_wrap.cxx shapescale.py shapescale.pyc

clean:
	rm -f *~ *.so shapescale_wrap.cxx shapescale.py shapescale.pyc
