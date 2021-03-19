mkdir build
cd build

cmake -G "Ninja" ^
    -D CMAKE_BUILD_TYPE="Release" ^
    -D CMAKE_INSTALL_PREFIX:FILEPATH=%LIBRARY_PREFIX% ^
    ..


ninja install