#!/usr/bin/env python

###
# Pivy configure, build and install script.
#

"""Pivy is an Open Inventor binding for Python. Open Inventor is an object
oriented 3D toolkit which presents a programming model based on a 3D scene
database. It was developed by Silicon Graphics.

The binding has been interfaced to Coin - a 3D graphics library with an C++
Application Programming Interface based on the Open Inventor 2.1 API.

Pivy has been developed by Tamer Fahmy and is made available under a
BSD-style license.
"""

import os, sys
# from distutils.core import setup
# from distutils.extension import Extension
import distutils.sysconfig

VERSION = "0.1a"

CXX="g++"
ELF_OPTS="-shared -fPIC -O2"
DARWIN_OPTS="-bundle -bundle_loader %s" % sys.executable

SWIG="swig"
SWIG_SUPPRESS_WARNINGS="-w389,362,503,510"
SWIG_PARAMS=SWIG_SUPPRESS_WARNINGS + " -v -c++ -python -includeall -D__PIVY__ " + \
             "-I. -I/usr/local/include -Ifake_headers %s -o pivy_wrap.cxx pivy.i"
MODULE_NAME="_pivy.so"

SUPPORTED_SWIG_VERSIONS = ['1.3.17', '1.3.18']
SWIG_COND_SYMBOLS = []
CXX_INCS = "-I" +  distutils.sysconfig.get_python_inc() + " "
CXX_LIBS = ""

config_log = None

def write_log(msg):
    """outputs messages to stdout and to a log file."""
    sys.stdout.write(msg)
    config_log.write(msg)

def do_os_popen(cmd):
    """returns the output of a command in a single line."""
    fd = os.popen(cmd)
    lines = fd.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    lines = " ".join(lines)
    fd.close()
    return lines

def check_cmd_exists(cmd):
    """returns the path of the specified command if it exists."""
    write_log("Checking for %s..." % cmd)
    for path in os.environ['PATH'].split(':'):
        if os.path.exists(os.path.join(path, cmd)):
            write_log("'%s'\n" % os.path.join(path, cmd))
            return 1
    write_log("not found.\n")
    return 0

def check_python_version():
    """checks the Python version."""
    write_log("Python version...%s\n" % sys.version.split(" ")[0])
    if int(sys.version[0]) < 2:
        write_log("Pivy only works with Python versions >= 2.0.\n")
        sys.exit(1)

def check_coin_version():
    """checks the Coin version."""
    if not check_cmd_exists("coin-config"):
        sys.exit(1)
    write_log("Coin version...")
    version = do_os_popen("coin-config --version")
    if not version.startswith('2.0'):
        write_log("Warning: Pivy %s has only been tested with Coin versions 2.0.x.\n" % VERSION)
    write_log("%s\n" % version)

def check_gui_bindings(SoGui, sogui_config):
    """checks for availability of SoGui bindings and retrieves the compiler flags and libs."""
    global CXX_INCS, CXX_LIBS
    
    if not check_cmd_exists(sogui_config):
        return 0

    write_log("Checking for %s version..." % SoGui)
    version = do_os_popen("%s --version" % sogui_config)
    write_log("%s.\n" % version)

    CXX_INCS += do_os_popen("%s --cppflags" % sogui_config)
    CXX_LIBS += do_os_popen("%s --ldflags --libs" % sogui_config)

    return 1

def get_coin_features():
    """sets the global variable SWIG_COND_SYMBOLS needed for conditional wrapping"""
    global SWIG_COND_SYMBOLS

    write_log("Checking for Coin features...")
    if not os.system("coin-config --have-feature 3ds_import"):
        SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_3DS_IMPORT")
        write_log("3ds import ")

    if not os.system("coin-config --have-feature vrml97"):
        SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_VRML97")
        write_log("vrml97 ")

    if not os.system("coin-config --have-feature sound"):
        SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_SOUND")
        write_log("sound ")

    if not os.system("coin-config --have-feature superglu"):
        SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_SUPERGLUE")
        write_log("superglu ")

    if not os.system("coin-config --have-feature threads"):
        SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_THREADS")
        write_log("threads ")

    if not os.system("coin-config --have-feature threadsafe"):
        HAVE_FEATURE.append("-DHAVE_FEATURE_THREADSAFE")
        write_log("threadsafe ")

    write_log("\n")

def check_compiler_version(compiler):
    """checks for the compiler version."""
    if not check_cmd_exists(compiler):
        sys.exit(1)
    fd = os.popen("%s --version" % compiler)
    for line in fd.readline():
        write_log(line)
    fd.close()
    
def check_swig_version(swig):
    """checks for the swig version."""
    if not check_cmd_exists(swig):
        sys.exit(1)
    write_log("Checking for SWIG version...")        
    fd = os.popen("%s -version 2>&1" % swig)
    version = fd.readlines()[1].strip().split(" ")[2]
    fd.close()
    write_log("%s\n" % version)
    if not version in SUPPORTED_SWIG_VERSIONS:
        write_log("Warning: Pivy has only been tested with the following SWIG versions: %s.\n" % " ".join(SUPPORTED_SWIG_VERSIONS))

def configure():
    """configures Pivy"""
    global CXX, SWIG
    
    write_log("Platform...%s\n" % sys.platform)
    check_python_version()
    check_coin_version()
    check_gui_bindings("SoQt", "soqt-config")
    get_coin_features()
    check_compiler_version(CXX)
    check_swig_version(SWIG)

def build():
    """build Pivy"""
    write_log(SWIG + " " + SWIG_PARAMS % CXX_INCS + "\n")
    if not os.system(SWIG + " " + SWIG_PARAMS % CXX_INCS):
        OPTS = ""
        if sys.platform.startswith("linux"):
            OPTS=ELF_OPTS
        elif sys.platform.startswith("darwin"):
            OPTS=DARWIN_OPTS
        write_log(" ".join((CXX, OPTS, CXX_INCS, CXX_LIBS, "-o%s pivy_wrap.cxx" % MODULE_NAME)) + "\n")
        if not os.system(" ".join((CXX, OPTS, CXX_INCS, CXX_LIBS, "-o%s pivy_wrap.cxx" % MODULE_NAME))):
            write_log("Importing pivy.py..." + "\n")
            import pivy

def cleanup():
    if config_log:
        config_log.close()

if __name__ == "__main__":
    sys.exitfunc = cleanup
    config_log = open("config.log", 'w')
    configure()
    build()
    
###
# distutils setup
##setup(name = "Pivy",
##      version = "0.1",
##      description = "An Open Inventor Python binding",
##      long_description = __doc__,
##      author = "Tamer Fahmy",
##      author_email = "tamer@tammura.at",
##      maintainer = "Tamer Fahmy",
##      maintainer_email = "tamer@tammura.at",      
##      url = "http://pivy.tammura.at/",
##      ext_modules = [Extension("_pivy",
##                               ["pivy_wrap.cxx"],
##                               include_dirs=["/opt/qt/include"],
##                               define_macros=SWIG_COND_SYMBOLS,
##                               extra_compile_args=[pivy_incs],
##                               extra_link_args=[pivy_libs + "-lstdc++"])
##                     ],
##      py_modules = ["pivy"])
