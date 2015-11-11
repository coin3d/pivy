###
# Copyright (c) 2002-2009 Kongsberg SIM
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import os, shutil
import distutils.sysconfig, os

SWIG_SUPPRESS_WARNINGS = "-w302,306,307,312,389,361,362,467,503,509,510"
includedir='/export/home/tamer/Projects/coin/bininclib/include/'

SOGUI = ('Qt', 'Xt', 'Gtk', 'Win')
MODULES = {'Coin'      : ('#pivy'+os.sep+'_coin',               'Inventor'),
           'SIMVoleon' : ('#pivy'+os.sep+'_simvoleon',          'VolumeViz'),
           'SoQt'      : ('#pivy'+os.sep+'gui'+os.sep+'_soqt',  'Qt'),
           'SoXt'      : ('#pivy'+os.sep+'gui'+os.sep+'_soxt',  'Win'),
           'SoGtk'     : ('#pivy'+os.sep+'gui'+os.sep+'_sogtk', 'Gtk'),
           'SoWin'     : ('#pivy'+os.sep+'gui'+os.sep+'_sowin', 'Win')}

def copy_and_swigify_header(target, source, env):
    """Copy the header files to the local include directories. Add an
    #include line at the beginning for the SWIG interface files."""

    pivy_header_include = "\n#ifdef __PIVY__\n%%include %s\n#endif\n"

    nr = -1
    for header in target:
        nr += 1
        file_h = str(header)
        file_i = str(source[nr])
        if not os.path.isfile(os.path.join(includedir, file_h)):
            target.remove(target[nr])
            source.remove(source[nr])
        else:
            shutil.copyfile(os.path.join(includedir, file_h), file_h)
            fd = open(str(header), 'r+')
            contents = fd.readlines()
            # insert right after #ifndef/#define header include protection
            contents.insert(2, pivy_header_include % (file_i))
            fd.seek(0)
            fd.writelines(contents)
            fd.close


bld_swigify = Builder(action = Action(copy_and_swigify_header,
                                      "Fixing header files for the following " +
                                      "swig interface files:\n\n${CHANGED_SOURCES}\n\n"),
                      suffix = '.h',
                      src_suffix = '.i')

dist_vars = distutils.sysconfig.get_config_vars('CC', 'CXX', 'OPT', 'BASECFLAGS',
                                                'CCSHARED', 'LDSHARED', 'SO')

for i in range(len(dist_vars)):
    if dist_vars[i] is None:
        dist_vars[i] = ""
(cc, cxx, opt, basecflags, ccshared, ldshared, so_ext) = dist_vars

env = Environment(ENV = os.environ,

                  CC=cxx,
                  CPPPATH=[distutils.sysconfig.get_python_inc()],
                  CPPFLAGS=basecflags + " " + opt,

                  SHLINK=ldshared,
                  SHLINKFLAGS=[],
                  SHLIBPREFIX="",
                  SHLIBSUFFIX=so_ext,

                  SWIGFLAGS = Split('-c++ -python  -includeall -modern -D__PIVY__') +
                  [SWIG_SUPPRESS_WARNINGS] + ['-I'+str(Dir('#')),
                                              '-I'+str(Dir('#fake_headers'))],
                  SWIGOUTDIR = 'pivy',

                  BUILDERS = {'SWIGIFY' : bld_swigify},
                  tools=['default', 'suncc'])

if str(Platform()) == 'win32':
    env['SHLIBSUFFIX'] = '.pyd'

swig_interfaces = {'Coin': [], 'Qt' : [], 'Win' : []}

# gather a list of all swig interface files in the header override subdirectories
swig_interfaces['Coin'] += Glob('#Inventor'+os.path.sep+'*.i')
for dirpath, dirnames, files in os.walk(str(Dir('#Inventor'))):
    for dirname in swig_interfaces:
        if dirname in dirnames:
            swig_interfaces[dirname] += Glob('#'+os.path.join(dirpath, dirname, '*.i'))
            dirnames.remove(dirname)
    for dirname in dirnames:
        swig_interfaces['Coin'] += Glob('#'+os.path.join(dirpath, dirname, '*.i'))

# print [str(name) for name in swig_interfaces['Coin']]

###
# Coin
#
coin_env = env.Clone()

coin_env.ParseConfig('pkg-config Coin --cflags --libs')
coin_env.Append(SWIGFLAGS = ['-I'+includedir])
coin_env.Append(SWIGFLAGS = ['-I'+str(Dir('#interfaces'))])

swigged_headers = coin_env.SWIGIFY([str(name)[:-2] for name in swig_interfaces['Coin']],
                                   [str(name)[:-2] for name in swig_interfaces['Coin']])

coin_wrapper = coin_env.CXXFile(['#interfaces/coin.i'])
coin_env.SharedLibrary('#pivy/_coin', coin_wrapper[0])
coin_env.Depends(coin_wrapper, swig_interfaces['Coin'])
coin_env.Depends(coin_wrapper, swigged_headers, )

###
# SoQt
#
soqt_env = env.Clone()

soqt_env.ParseConfig('pkg-config SoQt --cflags --libs')
soqt_env.Append(SWIGFLAGS = ['-I'+includedir])
soqt_env.Append(SWIGFLAGS = ['-I'+str(Dir('#interfaces'))])

swigged_qt_headers = soqt_env.SWIGIFY([str(name)[:-2] for name in swig_interfaces['Qt']],
                                      [str(name)[:-2] for name in swig_interfaces['Qt']])

soqt_wrapper = soqt_env.CXXFile(['#interfaces/soqt.i'])
soqt_env.SharedLibrary('#pivy/gui/_soqt', soqt_wrapper[0])
soqt_env.Depends(soqt_wrapper, swig_interfaces['Qt'])
soqt_env.Depends(soqt_wrapper, swigged_qt_headers)
