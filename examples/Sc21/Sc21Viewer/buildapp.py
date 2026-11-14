#!/usr/bin/env python
# SPDX-License-Identifier: ISC

from bundlebuilder import buildapp 
    
buildapp(
    mainprogram = "Sc21Viewer.py",
    resources = ["English.lproj" ],
    nibname = "MainMenu",
)   
