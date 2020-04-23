set(disable_warnings "-w302,306,307,312,314,325,361,362,467,389,503,509,510")

# coin.i

SET_PROPERTY(SOURCE coin.i PROPERTY CPLUSPLUS ON)
SET_PROPERTY(SOURCE coin.i PROPERTY OUTPUT_DIR ${CMAKE_BINARY_DIR}/pivy)
SET_PROPERTY(SOURCE coin.i PROPERTY SWIG_FLAGS "-includeall")
SET_PROPERTY(SOURCE coin.i APPEND PROPERTY SWIG_FLAGS "-py3")
SET_PROPERTY(SOURCE coin.i APPEND PROPERTY SWIG_FLAGS "-D__PIVY__")
SET_PROPERTY(SOURCE coin.i APPEND PROPERTY SWIG_FLAGS ${disable_warnings})

# remember: the order of the includes is important!
# swig needs the generated headers first (these headers are replacing the origin Inventor headers)
SET_PROPERTY(SOURCE coin.i PROPERTY INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}")
SET_PROPERTY(SOURCE coin.i APPEND PROPERTY INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}/fake_headers")
SET_PROPERTY(SOURCE coin.i APPEND PROPERTY INCLUDE_DIRECTORIES "${Coin_INCLUDE_DIR}")

swig_add_library(coin
    LANGUAGE python
    OUTPUT_DIR ${CMAKE_BINARY_DIR}/pivy
    SOURCES coin.i)

link_directories(${Coin_LIB_DIR})


target_include_directories(coin
    PRIVATE
    ${Coin_INCLUDE_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/interfaces
    )

set_target_properties(coin PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/pivy")
target_link_libraries(coin Coin)
install(TARGETS coin DESTINATION ${python_libs}/pivy)


if (WRAP_SOQT)
    # soqt.i

    SET_PROPERTY(SOURCE soqt.i PROPERTY CPLUSPLUS ON)
    SET_PROPERTY(SOURCE soqt.i PROPERTY OUTPUT_DIR ${CMAKE_BINARY_DIR}/pivy)
    SET_PROPERTY(SOURCE soqt.i PROPERTY SWIG_FLAGS "-includeall")
    SET_PROPERTY(SOURCE soqt.i APPEND PROPERTY SWIG_FLAGS "-py3")
    SET_PROPERTY(SOURCE soqt.i APPEND PROPERTY SWIG_FLAGS "-D__PIVY__")
    SET_PROPERTY(SOURCE soqt.i APPEND PROPERTY SWIG_FLAGS ${disable_warnings})

    # remember: the order of the includes is important!
    # swig needs the generated headers first (these headers are replacing the origin Inventor headers)
    SET_PROPERTY(SOURCE soqt.i PROPERTY INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}")
    SET_PROPERTY(SOURCE soqt.i APPEND PROPERTY INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}/fake_headers")
    SET_PROPERTY(SOURCE soqt.i APPEND PROPERTY INCLUDE_DIRECTORIES "${SoQt_INCLUDE_DIRS}")


    swig_add_library(soqt
        LANGUAGE python
        OUTPUT_DIR ${CMAKE_BINARY_DIR}/pivy/gui
        SOURCES soqt.i)

    link_directories(${SoQt_LIBRARY_DIRS})


    target_include_directories(soqt
        PRIVATE
        ${SoQt_INCLUDE_DIRS}
        ${Qt5Gui_INCLUDE_DIRS}
        ${Qt5Widgets_INCLUDE_DIRS}
        ${PYTHON_INCLUDE_DIRS}
        ${CMAKE_SOURCE_DIR}/interfaces
        )

    target_link_libraries(soqt SoQt)
    set_target_properties(soqt PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/pivy/gui")
    install(TARGETS soqt DESTINATION ${python_libs}/pivy/gui)
endif(WRAP_SOQT)
