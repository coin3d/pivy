#!/usr/bin/env python

###
# Copyright (C) 2002-2004, Tamer Fahmy <tamer@tammura.at>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# Pivy distutils setup script.
#

"""Pivy is an Open Inventor binding for Python. Open Inventor is an object
oriented 3D toolkit which presents a programming model based on a 3D scene
database. It was developed by Silicon Graphics.

The binding has been interfaced to Coin - a 3D graphics library with an C++
Application Programming Interface based on the Open Inventor 2.1 API.

Pivy has been developed by Tamer Fahmy and is made available under a
BSD-style license.
"""

###
# Setup file for the Pivy distribution.
#
import os, shutil, sys

from distutils.command.build import build
from distutils.command.clean import clean
from distutils.core import setup
from distutils.extension import Extension
from distutils.sysconfig import get_python_lib

# if we are on a Gentoo box salute the chap and output stuff in nice colors
# Gentoo is Python friendly, so be especially friendly to them! ;)
try:
    from output import green, blue, turquoise, red, yellow
    print red("Oooh, it's a Gentoo! Nice nice! tuhtah salutes you! :)")
except:
    def red(text): return text
    def green(text): return text
    def blue(text): return text
    def turquoise(text): return text
    def yellow(text): return text

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None


PIVY_CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Multimedia :: Graphics
Topic :: Multimedia :: Graphics :: 3D Modeling
Topic :: Multimedia :: Graphics :: 3D Rendering
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
"""

PIVY_VERSION = "0.1.2"

class pivy_build(build):
    PIVY_SNAKES = r"""
                            _____
                        .-'`     '.                                     
                     __/  __       \                                   
                    /  \ /  \       |    ___                          
                   | /`\| /`\|      | .-'  /^\/^\                   
                   | \(/| \(/|      |/     |) |)|                     
                  .-\__/ \__/       |      \_/\_/__..._             
          _...---'-.                /   _              '.               
         /,      ,             \   '|  `\                \           
        | ))     ))           /`|   \    `.       /)  /) |             
        | `      `          .'       |     `-._         /               
        \                 .'         |     ,_  `--....-'               
         `.           __.' ,         |     / /`'''`                     
           `'-.____.-' /  /,         |    / /                           
               `. `-.-` .'  \        /   / |                           
                 `-.__.'|    \      |   |  |-.                         
                    _.._|     |     /   |  |  `'.                       
              .-''``    |     |     |   /  |     `-.                    
           .'`         /      /     /  |   |        '.                  
         /`           /      /     |   /   |\         \               
        /            |      |      |   |   /\          |               
       ||            |      /      |   /     '.        |                
       |\            \      |      /   |       '.      /              
       \ `.           '.    /      |    \        '---'/               
        \  '.           `-./        \    '.          /                
         '.  `'.            `-._     '.__  '-._____.'--'''''--.         
           '-.  `'--._          `.__     `';----`              \       
              `-.     `-.          `.''```                     ;        
                 `'-..,_ `-.         `'-.                     /         
                        '.  '.           '.                 .'          


                            ~~~ HISSSSSSSSSS ~~~
                           Welcome to Pivy %s!
                 Building Pivy has never been so much fun!

    """ % PIVY_VERSION

    pivy_header_include = """\
#ifdef __PIVY__
%%include %s
#endif

"""

    SWIG = ((sys.platform == "win32" and "swig.exe") or "swig")
    SWIG_SUPPRESS_WARNINGS = "-w302,306,307,312,389,361,362,503,509,510"
    SWIG_PARAMS = "-noruntime -v -c++ -python -includeall " + \
                  "-D__PIVY__ -I. -Ifake_headers -I%s %s -o %s_wrap.cpp interfaces" + os.sep + "%s.i"

    SOGUI = ['SoQt', 'SoXt', 'SoGtk', 'SoWin']
    MODULES = {'pivy'  : ('_pivy',  'coin-config'),
               'SoQt'  : ('_soqt',  'soqt-config'),
               'SoXt'  : ('_soxt',  'soxt-config'),
               'SoGtk' : ('_sogtk', 'sogtk-config'),
               'SoWin' : ('_sowin', 'sowin-config')}

    SUPPORTED_SWIG_VERSIONS = ['1.3.21', '1.3.22']
    SWIG_VERSION = ""
    SWIG_COND_SYMBOLS = []
    CXX_INCS = ""
    CXX_LIBS = ""
    if sys.platform == "win32":
        CXX_INCS = "-DPIVY_WIN32 "

    ext_modules=[]
    py_modules=['sogui']

    def do_os_popen(self, cmd):
        "returns the output of a command in a single line."
        fd = os.popen(cmd)
        lines = fd.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        lines = " ".join(lines)
        fd.close()
        return lines

    def check_cmd_exists(self, cmd):
        "returns the path of the specified command if it exists."
        print blue("Checking for %s..." % cmd),
        for path in os.environ['PATH'].split(os.path.pathsep):
            if os.path.exists(os.path.join(path, cmd)):
                print blue("'%s'" % os.path.join(path, cmd))
                return 1
        print red("not found.")
        return 0

    def check_python_version(self):
        "checks the Python version."
        print blue("Python version...%s" % sys.version.split(" ")[0])
        if int(sys.version[0]) < 2:
            print red("Pivy only works with Python versions >= 2.0.")
            sys.exit(1)

    def check_coin_version(self):
        "checks the Coin version."
        if sys.platform == "win32": return
        if not self.check_cmd_exists("coin-config"):
            sys.exit(1)
        print blue("Coin version..."),
        version = self.do_os_popen("coin-config --version")
        print blue("%s" % version)
        if not version.startswith('2.3'):
            print yellow("** Warning: Pivy has only been tested with Coin "
                         "versions 2.3.x.")

    def check_gui_bindings(self):
        "checks for availability of SoGui bindings and removes the not available ones."
        if sys.platform == "win32":
            print "Using SoWin by default for Windows builds!"
            self.MODULES = {'pivy'  : ('_pivy',  'coin-config'),
                            'SoWin' : ('_sowin', 'sowin-config')}
            return            
        for gui in self.SOGUI:
            gui_config_cmd = self.MODULES[gui][1]
            if not self.check_cmd_exists(gui_config_cmd):
                del self.MODULES[gui]
            else:
                print blue("Checking for %s version..." % gui),
                version = self.do_os_popen("%s --version" % gui_config_cmd)
                print blue("%s" % version)

    def get_coin_features(self):
        "sets the global variable SWIG_COND_SYMBOLS needed for conditional " + \
        "wrapping"
        if sys.platform == "win32": return
        print blue("Checking for Coin features..."),
        if not os.system("coin-config --have-feature 3ds_import"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_3DS_IMPORT")
            print green("3ds import "),

        if not os.system("coin-config --have-feature vrml97"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_VRML97")
            print green("vrml97 "),

        if not os.system("coin-config --have-feature sound"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_SOUND")
            print green("sound "),

        if not os.system("coin-config --have-feature superglu"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_SUPERGLUE")
            print green("superglu "),

        if not os.system("coin-config --have-feature threads"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_THREADS")
            print green("threads "),

        if not os.system("coin-config --have-feature threadsafe"):
            self.SWIG_COND_SYMBOLS.append("-DHAVE_FEATURE_THREADSAFE")
            print green("threadsafe "),

        print

    def check_swig_version(self, swig):
        "checks for the swig version."
        global SWIG_VERSION
        if not self.check_cmd_exists(swig):
            sys.exit(1)
        print blue("Checking for SWIG version..."),
        fd = os.popen4("%s -version" % swig)[1]
        version = fd.readlines()[1].strip().split(" ")[2]
        fd.close()
        print blue("%s" % version)
        SWIG_VERSION = version
        if not version in self.SUPPORTED_SWIG_VERSIONS:
            print yellow("Warning: Pivy has only been tested with the following " + \
                         "SWIG versions: %s." % " ".join(self.SUPPORTED_SWIG_VERSIONS))

    def copy_and_swigify_coin_headers(self, coin_includedir, dirname, files):
        """there are times where a function simply has to do what a function
        has to do. indeed, tralala..."""

        for file in files:
            if not os.path.isfile(os.path.join(dirname, file)):
                continue

            if file[-2:] == ".i":
                file_i = os.path.join(dirname, file)
                file_h = os.path.join(dirname, file)[:-2] + ".h"
                
                if not os.path.exists(file_h) and \
                   os.path.exists(os.path.join(coin_includedir, file_h)):
                    print blue("Copying ") + turquoise(os.path.join(coin_includedir, file_h)),
                    print blue("to ") + turquoise(file_h)
                    shutil.copyfile(os.path.join(coin_includedir, file_h), file_h)
                    print blue("Pivyizing ") + turquoise(file_h),
                    fd = open(file_h, 'r+')
                    contents = fd.readlines()

                    ins_line_nr = -1
                    for line in contents:
                        ins_line_nr += 1
                        if line.find("#include ") != -1:
                            break

                    if ins_line_nr != -1:
                        contents.insert(ins_line_nr, self.pivy_header_include % (file_i))
                        fd.seek(0)
                        fd.writelines(contents)
                        print blue("[") + green("done") + blue("]")
                    else:
                        print blue("[") + red("failed") + blue("]")
                    fd.close
            # fixes for SWIG 1.3.21 and upwards
            # (mostly workarounding swig's preprocessor "function like macros"
            # preprocessor bug when no parameters are provided which then results
            # in no constructors being created in the wrapper)
            elif file[-4:] == ".fix":
                print red("Fixing ") + turquoise(os.path.join(dirname, file)),
                print blue("to ") + turquoise(os.path.join(dirname, file)[:-4])
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-4])
            # had to introduce this because windows is a piece of crap
            elif sys.platform == "win32" and file[-6:] == ".win32":
                print red("Fixing ") + turquoise(os.path.join(dirname, file)),
                print blue("to ") + turquoise(os.path.join(dirname, file)[:-6])
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-6])
        
        if sys.platform == "win32":
            # copy coin2.dll and sowin1.dll to pivy directory
            shutil.copy(os.getenv("COIN3DDIR") + "\\bin\coin2.dll", ".")
            shutil.copy(os.getenv("COIN3DDIR") + "\\bin\sowin1.dll", ".")

    def pivy_configure(self):
        "configures Pivy"
        print turquoise(self.PIVY_SNAKES)
        print blue("Platform...%s" % sys.platform)
        self.check_python_version()
        self.check_coin_version()
        if self.SOGUI: self.check_gui_bindings()
        self.get_coin_features()
        self.check_swig_version(self.SWIG)

        if sys.platform == "win32":
            INCLUDE_DIR = os.getenv("COIN3DDIR") + "\\include"
        else:
            INCLUDE_DIR = self.do_os_popen("coin-config --includedir")

        os.path.walk("Inventor", self.copy_and_swigify_coin_headers,
                     INCLUDE_DIR)

    def swig_generate(self):
        "build all available modules and the runtime library"

        if not os.path.isfile("pivy_runtime_wrap.cpp"):
            print red("\n=== Generating pivy_runtime_wrap.cpp ===")
            print blue(self.SWIG   + " -runtime -v -c++ -python -interface libpivy_runtime -o pivy_runtime_wrap.cpp interfaces" + os.sep + "pivy_runtime.i")
            if os.system(self.SWIG + " -runtime -v -c++ -python -interface libpivy_runtime -o pivy_runtime_wrap.cpp interfaces" + os.sep + "pivy_runtime.i"):
                print red("SWIG did not generate runtime wrapper successfully! ** Aborting **")
                sys.exit(1)

            extra_compile_args=None
            if sys.platform == "win32":
                extra_compile_args = ["/DSWIG_GLOBAL", "/MT"]
            self.ext_modules.append(Extension("libpivy_runtime",
                                              ["pivy_runtime_wrap.cpp"],
                                              extra_compile_args=extra_compile_args))
        else:
            print red("=== pivy_runtime_wrap.cpp already exists! ===")

        self.py_modules.append("pivy_runtime")
        
        for module in self.MODULES.keys():
            module_name = self.MODULES[module][0]
            config_cmd = self.MODULES[module][1]

            if sys.platform == "win32":
                INCLUDE_DIR = os.getenv("COIN3DDIR") + "\\include"
                CPP_FLAGS = "-I" + INCLUDE_DIR +  " " + \
                            "-I" + os.getenv("COIN3DDIR") + "\\include\\Inventor\\annex" + \
                            " /DSOWIN_DLL /DCOIN_DLL /wd4244 /wd4049 /MT"
                LDFLAGS_LIBS = os.getenv("COIN3DDIR") + "\\lib\\coin2.lib" + " " + \
                               os.getenv("COIN3DDIR") + "\\lib\\sowin1.lib"
            else:
                INCLUDE_DIR = self.do_os_popen("coin-config --includedir")
                CPP_FLAGS = self.do_os_popen("%s --cppflags" % config_cmd)
                LDFLAGS_LIBS = self.do_os_popen("%s --ldflags --libs" % config_cmd)
                
            if not os.path.isfile(module.lower() + "_wrap.cpp"):
                print red("\n=== Generating %s_wrap.cpp for %s ===\n" % (module.lower(), module))
                print blue(self.SWIG + " " + self.SWIG_SUPPRESS_WARNINGS + " " + self.SWIG_PARAMS %
                           (INCLUDE_DIR,
                            self.CXX_INCS,
                            module.lower(),
                            module.lower()))
                if os.system(self.SWIG + " " + self.SWIG_SUPPRESS_WARNINGS + " " + self.SWIG_PARAMS %
                             (INCLUDE_DIR,
                              self.CXX_INCS,
                              module.lower(), module.lower())):
                    print red("SWIG did not generate wrappers successfully! ** Aborting **")
                    sys.exit(1)
            else:
                print red("=== %s_wrap.cpp for %s already exists! ===" % (module.lower(),
                                                                            module))

            runtime_library_dirs = []
            libraries = ['pivy_runtime']
            if sys.platform == "win32":
                library_dirs = [self.build_temp + os.path.sep + (self.debug and 'Debug' or 'Release')]
            else:
                library_dirs = [os.getcwd() + os.path.sep + self.build_lib]
                runtime_library_dirs = [get_python_lib()]

            self.ext_modules.append(Extension(module_name, [module.lower() + "_wrap.cpp"],
                                              library_dirs=library_dirs,
                                              runtime_library_dirs=runtime_library_dirs,
                                              libraries=libraries,
                                              extra_compile_args=(self.CXX_INCS + CPP_FLAGS).split(),
                                              extra_link_args=(self.CXX_LIBS + LDFLAGS_LIBS).split()))
            self.py_modules.append(module.lower())

    def run(self):
        "the entry point for the distutils build class"
        if sys.platform == "win32" and not os.getenv("COIN3DDIR"):
            print "Please set the COIN3DDIR environment variable to your Coin root directory! ** Aborting **"
            sys.exit(1)
        
        self.pivy_configure()
        self.swig_generate()

        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class pivy_clean(clean):
    WRAPPER_FILES = ('pivy_runtime_wrap.cpp',
                     'pivy_wrap.cpp',
                     'soqt_wrap.cpp',
                     'sogtk_wrap.cpp',
                     'soxt_wrap.cpp',
                     'sowin_wrap.cpp')

    def remove_coin_headers(self, arg, dirname, files):
        "remove the coin headers from the pivy Inventor directory"

        for file in files:
            if not os.path.isfile(os.path.join(dirname, file)) or file[-2:] != ".h":
                continue
            print blue("removing %s" % os.path.join(dirname, file))
            os.remove(os.path.join(dirname, file))
        
    def run(self):
        "the entry point for the distutils clean class"
        os.path.walk("Inventor", self.remove_coin_headers, None)
        # remove the SWIG generated wrappers
        for wrapper_file in self.WRAPPER_FILES:
            if os.path.isfile(wrapper_file):
                print blue("removing %s" % wrapper_file)
                os.remove(wrapper_file)
        clean.run(self)

data_files = None
if sys.platform == "win32":
    data_files = [('.', ['coin2.dll', 'sowin1.dll'])]

setup(name = "Pivy",
      version = PIVY_VERSION,
      description = "A Python binding for Coin/Open Inventor",
      long_description = __doc__,
      author = "Tamer Fahmy",
      author_email = "tamer@tammura.at",
      download_url="http://www.tammura.at/cvs.html",
      url = "http://pivy.tammura.at/",
      cmdclass = {'build' : pivy_build,
                  'clean' : pivy_clean},
      ext_modules = pivy_build.ext_modules,
      py_modules  = pivy_build.py_modules,
      classifiers = filter(None, PIVY_CLASSIFIERS.split("\n")),
      license = "BSD License",
      platforms = ['Any'],
      data_files = data_files
      )
