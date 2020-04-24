cmake_minimum_required(VERSION 3.14)
project(pivy)


option(DISABLE_SWIG_WARNINGS "if on no swig warnings are shown" OFF)

find_package(SWIG 4.0.0 REQUIRED)
include(${SWIG_USE_FILE})

find_package(Coin CONFIG REQUIRED)
find_package(SoQt CONFIG)

if (SoQt_FOUND)
    find_package(Qt5 COMPONENTS Core Widgets Gui REQUIRED)
endif()

find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

# SWIGIFY HEADERS
# doing this with the origin python functions

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c
"import sys; sys.path.append('${CMAKE_SOURCE_DIR}'); \
import install_helpers; install_helpers.swigify('${CMAKE_SOURCE_DIR}', '${Coin_INCLUDE_DIR}');")


# copy the python module
include(TargetCopyFiles.cmake)

add_custom_target(pivy ALL)
add_copy_directory(pivy ${CMAKE_SOURCE_DIR}/pivy
    DESTINATION ${CMAKE_BINARY_DIR}/pivy
    PATTERN *.py
)


# find python install destination

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c
  "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
  OUTPUT_VARIABLE python_libs OUTPUT_STRIP_TRAILING_WHITESPACE )

add_subdirectory(interfaces)

install(DIRECTORY
    ${CMAKE_BINARY_DIR}/pivy
    DESTINATION ${python_libs}
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "*.so"
    PATTERN "*.dylib"
    PATTERN "*.dll"
    PATTERN "*.pyd"
    )
