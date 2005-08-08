#!/usr/bin/env python

###
# Copyright (C) 2002-2005, Tamer Fahmy <tamer@tammura.at>
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
from distutils.command.install import install
from distutils.core import setup
from distutils.extension import Extension
from distutils import sysconfig

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

PIVY_VERSION = "0.3.0"

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

    SWIG_SUPPRESS_WARNINGS = "-w302,306,307,312,389,361,362,467,503,509,510"
    SWIG_PARAMS = "-c++ -python -includeall -modern -D__PIVY__ " + \
                  "-I. -Ifake_headers -I%s %s -o %s_wrap.cpp " + \
                  "interfaces" + os.sep + "%s.i"

    SOGUI = ['soqt', 'soxt', 'sogtk', 'sowin']
    MODULES = {'coin'      : ('_coin',      'coin-config',      'pivy.'),
               'simvoleon' : ('_simvoleon', 'simvoleon-config', 'pivy.'),
               'soqt'      : ('gui._soqt',  'soqt-config',      'pivy.gui.'),
               'soxt'      : ('gui._soxt',  'soxt-config',      'pivy.gui.'),
               'sogtk'     : ('gui._sogtk', 'sogtk-config',     'pivy.gui.'),
               'sowin'     : ('gui._sowin', 'sowin-config',     'pivy.gui.')}

    SUPPORTED_SWIG_VERSIONS = ['1.3.25']
    SWIG_VERSION = ""
    SWIG_COND_SYMBOLS = []
    CXX_INCS = "-Iinterfaces "
    CXX_LIBS = ""
    if sys.platform == "win32":
        CXX_INCS += "-DPIVY_WIN32 "

    ext_modules = []
    py_modules = ['pivy.sogui']

    def do_os_popen(self, cmd):
        "return the output of a command in a single line"
        fd = os.popen(cmd)
        lines = fd.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        lines = " ".join(lines)
        fd.close()
        return lines

    def check_cmd_exists(self, cmd):
        "return the path of the specified command if it exists"
        print blue("Checking for %s..." % cmd),
        for path in os.environ['PATH'].split(os.path.pathsep):
            if os.path.exists(os.path.join(path, cmd)):
                print blue("'%s'" % os.path.join(path, cmd))
                return 1
        print red("not found.")
        return 0

    def check_python_version(self):
        "check the Python version"
        print blue("Python version...%s" % sys.version.split(" ")[0])
        if int(sys.version[0]) < 2:
            print red("Pivy only works with Python versions >= 2.0.")
            sys.exit(1)

    def check_coin_version(self):
        "check the Coin version"
        if sys.platform == "win32": return
        if not self.check_cmd_exists("coin-config"):
            sys.exit(1)
        print blue("Coin version..."),
        version = self.do_os_popen("coin-config --version")
        print blue("%s" % version)
        if not version.startswith('2.4'):
            print yellow("** Warning: Pivy has only been tested with Coin "
                         "versions 2.4.x.")

    def check_simvoleon_version(self):
        "return if SIMVoleon is available and check the version"
        if sys.platform == "win32": return
        if not self.check_cmd_exists("simvoleon-config"):
            del self.MODULES['simvoleon']
            return False

        print blue("SIMVoleon version..."),
        version = self.do_os_popen("simvoleon-config --version")
        print blue("%s" % version)
        if not version.startswith('2.0'):
            print yellow("** Warning: Pivy has only been tested with SIMVoleon "
                         "versions 2.0.x.")
        return True

    def check_gui_bindings(self):
        "check for availability of SoGui bindings and removes the not available ones"
        if sys.platform == "win32":
            print "Using SoWin by default for Windows builds!"
            self.MODULES = {'coin'  : ('_coin',  'coin-config', 'pivy.'),
                            'sowin' : ('gui._sowin', 'sowin-config', 'pivy.gui.')}
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
        "set the global variable SWIG_COND_SYMBOLS needed for conditional " + \
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
        "check for the swig version"
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

    def copy_and_swigify_headers(self, includedir, dirname, files):
        """Copy the header files to the local include directories. Add an
        #include line at the beginning for the SWIG interface files..."""

        for file in files:
            if not os.path.isfile(os.path.join(dirname, file)):
                continue

            if file[-2:] == ".i":
                file_i = os.path.join(dirname, file)
                file_h = os.path.join(dirname, file)[:-2] + ".h"

                if (not os.path.exists(file_h) and
                    os.path.exists(os.path.join(includedir, file_h))):
                    shutil.copyfile(os.path.join(includedir, file_h), file_h)
                    sys.stdout.write(' ' + turquoise(file_h))
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
                    else:
                        print blue("[") + red("failed") + blue("]")
                        sys.exit(1)
                    fd.close
            # fixes for SWIG 1.3.21 and upwards
            # (mostly workarounding swig's preprocessor "function like macros"
            # preprocessor bug when no parameters are provided which then results
            # in no constructors being created in the wrapper)
            elif file[-4:] == ".fix":
                sys.stdout.write(' ' + red(os.path.join(dirname, file)[:-4]))
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-4])
            # had to introduce this because windows is a piece of crap
            elif sys.platform == "win32" and file[-6:] == ".win32":
                sys.stdout.write(' ' + red(os.path.join(dirname, file)[:-6]))
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-6])

    def pivy_configure(self):
        "configure Pivy"
        print turquoise(self.PIVY_SNAKES)
        print blue("Platform...%s" % sys.platform)
        self.check_python_version()
        self.check_swig_version(self.SWIG)
        self.check_coin_version()
        self.get_coin_features()
        if self.SOGUI: self.check_gui_bindings()
        
        if self.check_simvoleon_version():
            if sys.platform == "win32":
                INCLUDE_DIR = os.getenv("SIMVOLEONDIR") + "\\include"
            else:
                INCLUDE_DIR = self.do_os_popen("simvoleon-config --includedir")

            sys.stdout.write(blue("Preparing") + green(" SIMVoleon ") + blue("headers:"))
            os.path.walk("VolumeViz", self.copy_and_swigify_headers,
                         INCLUDE_DIR)
            print green(".")

        if sys.platform == "win32":
            INCLUDE_DIR = os.getenv("COIN3DDIR") + "\\include"
        else:
            INCLUDE_DIR = self.do_os_popen("coin-config --includedir")

        sys.stdout.write(blue("Preparing") + green(" Inventor ") + blue("headers:"))
        os.path.walk("Inventor", self.copy_and_swigify_headers,
                     INCLUDE_DIR)
        print green(".")

    def swig_generate(self):
        "build all available modules"

        for module in self.MODULES:
            module_name = self.MODULES[module][0]
            config_cmd = self.MODULES[module][1]
            module_pkg_name = self.MODULES[module][2]
            mod_out_prefix = module_pkg_name.replace('.', os.sep) + module
            
            if sys.platform == "win32":
                INCLUDE_DIR = os.getenv("COIN3DDIR") + "\\include"
                CPP_FLAGS = "-I" + INCLUDE_DIR +  " " + \
                            "-I" + os.getenv("COIN3DDIR") + "\\include\\Inventor\\annex" + \
                            " /DSOWIN_DLL /DCOIN_DLL /wd4244 /wd4049"
                LDFLAGS_LIBS = os.getenv("COIN3DDIR") + "\\lib\\coin2.lib " + \
                               os.getenv("COIN3DDIR") + "\\lib\\sowin1.lib"
            else:
                INCLUDE_DIR = self.do_os_popen("coin-config --includedir")
                CPP_FLAGS = self.do_os_popen("%s --cppflags" % config_cmd)
                LDFLAGS_LIBS = self.do_os_popen("%s --ldflags --libs" % config_cmd)

            if not os.path.isfile(mod_out_prefix + "_wrap.cpp"):
                print red("\n=== Generating %s_wrap.cpp for %s ===\n" %
                          (mod_out_prefix, module))
                print blue(self.SWIG + " " + self.SWIG_SUPPRESS_WARNINGS + " " + self.SWIG_PARAMS %
                           (INCLUDE_DIR,
                            self.CXX_INCS,
                            mod_out_prefix, module))
                if os.system(self.SWIG + " " + self.SWIG_SUPPRESS_WARNINGS + " " + self.SWIG_PARAMS %
                             (INCLUDE_DIR,
                              self.CXX_INCS,
                              mod_out_prefix, module)):
                    print red("SWIG did not generate wrappers successfully! ** Aborting **")
                    sys.exit(1)
            else:
                print red("=== %s_wrap.cpp for %s already exists! ===" % (mod_out_prefix, module_pkg_name + module))

            self.ext_modules.append(Extension(module_name, [mod_out_prefix + "_wrap.cpp"],
                                              extra_compile_args=(self.CXX_INCS + CPP_FLAGS).split(),
                                              extra_link_args=(self.CXX_LIBS + LDFLAGS_LIBS).split()))
            self.py_modules.append(module_pkg_name + module)

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
    pivy_path = 'pivy' + os.sep
    gui_path = 'pivy' + os.sep + 'gui' + os.sep
    REMOVE_FILES = (pivy_path + '__init__.pyc', gui_path + '__init__.pyc',
                    pivy_path + 'coin_wrap.cpp',  pivy_path + 'coin.py',  pivy_path + 'coin.pyc',
                    pivy_path + 'simvoleon_wrap.cpp',  pivy_path + 'simvoleon.py',  pivy_path + 'simvoleon.pyc',
                    gui_path + 'soqt_wrap.cpp',  gui_path + 'soqt.py',  gui_path + 'soqt.pyc',
                    gui_path + 'sogtk_wrap.cpp', gui_path + 'sogtk.py', gui_path + 'sogtk.py',
                    gui_path + 'soxt_wrap.cpp',  gui_path + 'soxt.py',  gui_path + 'soxt.pyc',
                    gui_path + 'sowin_wrap.cpp', gui_path + 'sowin.py', gui_path + 'sowin.pyc',
                    pivy_path + 'sogui.pyc')

    def remove_headers(self, arg, dirname, files):
        "remove the coin headers from the pivy Inventor directory"
        for file in files:
            if not os.path.isfile(os.path.join(dirname, file)) or file[-2:] != ".h":
                continue
            sys.stdout.write(' ' + turquoise(os.path.join(dirname, file)))
            os.remove(os.path.join(dirname, file))

    def run(self):
        "the entry point for the distutils clean class"
        sys.stdout.write(blue("Cleaning headers:"))
        os.path.walk("Inventor", self.remove_headers, None)
        os.path.walk("VolumeViz", self.remove_headers, None)
        # remove the SWIG generated wrappers
        for wrapper_file in self.REMOVE_FILES:
            if os.path.isfile(wrapper_file):
                sys.stdout.write(' ' + turquoise(wrapper_file))
                os.remove(wrapper_file)
        print green(".")

        clean.run(self)

setup(name = "Pivy",
      version = PIVY_VERSION,
      description = "A Python binding for Coin",
      long_description = __doc__,
      author = "Tamer Fahmy",
      author_email = "tamer@tammura.at",
      download_url="http://www.tammura.at/subversion",
      url = "http://pivy.tammura.at/",
      cmdclass = {'build'   : pivy_build,
                  'clean'   : pivy_clean},
      ext_package = 'pivy',
      ext_modules = pivy_build.ext_modules,
      py_modules  = pivy_build.py_modules,
      packages = ['pivy', 'pivy.gui'],
      classifiers = filter(None, PIVY_CLASSIFIERS.split("\n")),
      license = "BSD License",
      platforms = ['Any']
      )
