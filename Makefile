CXXFLAGS+= -I/usr/local/include/python2.1

OPTS=-fPIC -O2


all: pivy

###
# pivy
#
pivy: pivycmodule.so

pivycmodule.so: pivy_wrap.cxx
	g++ -shared $(OPTS) $(CXXFLAGS) `sogtk-config --cppflags --ldflags --libs` \
	-o pivycmodule.so pivy_wrap.cxx 

wrap: pivy_wrap.cxx

pivy_wrap.cxx: pivy.i
	swig -v -python -shadow -c++ -includeall -D__PIVY__ -I. -I/usr/local/include \
             -Ifake_headers -o pivy_wrap.cxx pivy.i

cleanpivy:
	rm -f pivycmodule.so pivy_wrap.cxx pivy.py pivy.pyc

###
# pivyGtk
#
pivyGtk: pivyGtkcmodule.so

pivyGtkcmodule.so: pivycmodule.so pivyGtk_wrap.cxx
	g++ -shared $(OPTS) $(CXXFLAGS) `sogtk-config --cppflags --ldflags --libs` \
	-o pivyGtkcmodule.so pivyGtk_wrap.cxx 

wrapGtk: pivyGtk_wrap.cxx

pivyGtk_wrap.cxx: pivyGtk.i
	swig -v -python -shadow -c++ -Ifake_headers \
		 -o pivyGtk_wrap.cxx pivyGtk.i

cleanpivyGtk:
	rm -f pivyGtkc.so pivyGtk_wrap.cxx pivyGtk.py pivyGtk.pyc

clean:
	rm -f *~ *.so pivy_wrap.cxx pivy.py pivy.pyc \
	      pivyGtk_wrap.cxx pivyGtk.py pivyGtk.pyc
