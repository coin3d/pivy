cmake_minimum_required(VERSION 3.18)
project(pivy)


option(DISABLE_SWIG_WARNINGS "if on no swig warnings are shown" OFF)
option(PIVY_USE_QT6 "Prefer Qt6 over Qt5 if available" OFF)

find_package(SWIG 4.0.0 REQUIRED)
include(${SWIG_USE_FILE})

find_package(Coin CONFIG REQUIRED)
find_package(SoQt CONFIG)

if (SoQt_FOUND)
    if (PIVY_USE_QT6)
        find_package(Qt6 COMPONENTS Core Widgets Gui REQUIRED)
    else (PIVY_USE_QT6)
        find_package(Qt5 COMPONENTS Core Widgets Gui REQUIRED)
    endif (PIVY_USE_QT6)
endif()

find_package(Python REQUIRED COMPONENTS Interpreter Development)

# SWIGIFY HEADERS
# doing this with the origin python functions

execute_process(COMMAND ${Python_EXECUTABLE} -c
"import sys; sys.path.append('${CMAKE_SOURCE_DIR}'); \
import install_helpers; install_helpers.swigify('${CMAKE_SOURCE_DIR}', '${Coin_INCLUDE_DIR}');")


# copy the python module
include(TargetCopyFiles.cmake)

add_custom_target(pivy ALL)
add_copy_directory(pivy ${CMAKE_SOURCE_DIR}/pivy
    DESTINATION ${CMAKE_BINARY_DIR}/pivy
    PATTERN *.py
)

add_subdirectory(interfaces)

install(DIRECTORY
    ${CMAKE_BINARY_DIR}/pivy
    DESTINATION ${Python_SITEARCH}
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "*.so"
    PATTERN "*.dylib"
    PATTERN "*.dll"
    PATTERN "*.pyd"
    )
