###
# Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
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

import os
import distutils.sysconfig

SetOption('implicit_cache', 1)

opts = Options('custom.py')
opts.AddOptions(BoolOption('warnings', 'compilation with -Wall', 0),
                BoolOption('debug', 'debug output and symbols', 0))

env = Environment(ENV = os.environ,
                  options = opts,
                  tools=['default'])

Help(opts.GenerateHelpText(env))

if env['debug']:
    env.Append(CCFLAGS = (str(Platform()) == 'win32') and ['/Zi'] or ['-g'])
else:
    env.Append(CCFLAGS = (str(Platform()) == 'win32') and ['/O2'] or ['-O2'])

if str(Platform()) != 'win32' and env['warnings']:
    env.Append(CCFLAGS = '-Wall')

env.Append(CPPPATH = [distutils.sysconfig.get_python_inc()])
env.Append(SWIGFLAGS = '-runtime -python -noproxy')
env.Append(LINKFLAGS = distutils.sysconfig.get_config_vars()['LINKFORSHARED'])

if str(Platform()) == 'darwin':
    env.Append(LINKFLAGS = '-install_name ' + distutils.sysconfig.get_python_lib() + '/libpivy_runtime.dylib')

pivy_runtime = env.SharedLibrary('pivy_runtime',
                                 'interfaces/pivy_runtime.i')

install = env.Alias('install',
                    env.Install(distutils.sysconfig.get_python_lib(),
                                pivy_runtime))
env.Depends(install, pivy_runtime)
