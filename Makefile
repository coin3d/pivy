CXXFLAGS+= -I/usr/include/python

OPTS=-fPIC # -O2

all: pivy

###
# pivy
#
pivy: _pivy.so pivy.pyc

pivy.pyc: pivy.py
	python -c "import pivy"

_pivy.so: pivy_wrap.cxx
	g++ -shared $(OPTS) $(CXXFLAGS) `soqt-config --cppflags --ldflags --libs` \
	-o _pivy.so pivy_wrap.cxx 

wrap: pivy_wrap.cxx

pivy_wrap.cxx: pivy.i
	swig -v -c++ -python -includeall -D__PIVY__ -I. -I/usr/local/include \
             -Ifake_headers -o pivy_wrap.cxx pivy.i

cleanpivy:
	rm -f _pivy.so pivy_wrap.cxx pivy.py pivy.pyc

clean:
	rm -f *~ *.so pivy_wrap.cxx pivy.py pivy.pyc \
	      pivyQt_wrap.cxx pivyQt.py pivyQt.pyc
