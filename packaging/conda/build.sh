mkdir -p build
cd build

echo "USE_QT6 is set ${USE_QT6}"

if [[ ${HOST} =~ .*linux.* && ${USE_QT6} = "0" ]]; then
  sed -i 's|_qt5gui_find_extra_libs(EGL.*)|_qt5gui_find_extra_libs(EGL "EGL" "" "")|g' $PREFIX/lib/cmake/Qt5Gui/Qt5GuiConfigExtras.cmake
  sed -i 's|_qt5gui_find_extra_libs(OPENGL.*)|_qt5gui_find_extra_libs(OPENGL "GL" "" "")|g' $PREFIX/lib/cmake/Qt5Gui/Qt5GuiConfigExtras.cmake
fi

PIVY_CPP_FLAGS='-std=c++1z '

cmake -G "Ninja" \
    -D CMAKE_BUILD_TYPE="Release" \
    -D CMAKE_INSTALL_PREFIX:FILEPATH=$PREFIX \
    -D Python_EXECUTABLE:FILEPATH=$PREFIX/bin/python \
    -D PIVY_USE_QT6:BOOL=$USE_QT6 \
    ..

ninja install
