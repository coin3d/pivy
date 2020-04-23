project(pivy)
cmake_minimum_required(VERSION 3.14)

FIND_PACKAGE(SWIG 4.0.0 REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(Coin CONFIG REQUIRED)
FIND_PACKAGE(SoQt CONFIG)

OPTION(WRAP_SOQT "wrap the soqt library" OFF)

if (SoQt_LIBRARY_DIRS)
    MESSAGE(STATUS "try to find qt")
    FIND_PACKAGE(Qt5 COMPONENTS Core Widgets Gui REQUIRED)
    SET(WRAP_SOQT ON)
endif()

FIND_PACKAGE(PythonInterp REQUIRED)
FIND_PACKAGE(PythonLibs REQUIRED)


SET(CMAKE_EXECUTE_PROCESS_COMMAND_ECHO STDOUT)


# SWIGIFY HEADERS
# doing this with the origin python functions

MESSAGE(STATUS ${CMAKE_SOURCE_DIR})
EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c
"import sys; sys.path.append('${CMAKE_SOURCE_DIR}'); \
import install_helpers; install_helpers.swigify('${CMAKE_SOURCE_DIR}', '${Coin_INCLUDE_DIR}');")


# copy the python module
include(TargetCopyFiles.cmake)

add_custom_target(pivy ALL)
add_copy_directory(pivy ${CMAKE_SOURCE_DIR}/pivy
    DESTINATION ${CMAKE_BINARY_DIR}/pivy
    GLOB *.py
)


# find python install destination

EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c
  "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
  OUTPUT_VARIABLE python_libs OUTPUT_STRIP_TRAILING_WHITESPACE )

ADD_SUBDIRECTORY(interfaces)

INSTALL(DIRECTORY
    ${CMAKE_BINARY_DIR}/pivy
    DESTINATION ${python_libs}
    PATTERN "*.py"
    )
