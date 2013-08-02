# Change the spatial reference of a folder full of mxd files
#
# Jon Pedder
# MapSAR
# 12/20/12
#
# Licence:
#     MapSAR wilderness search and rescue GIS data model and related python scripting
#     Copyright (C) 2012  - Jon Pedder & SMSR
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------


import arcpy, sys, os
from os.path import join, abspath
from os import walk

# Get parameters from user input
# 0. Folder containing mxd to change spatial reference - Folder
# 1. Spatial Reference - Spatial Reference
ptargetFolder = arcpy.GetParameterAsText(0)
pSR = arcpy.GetParameterAsText(1)

# Get list of mxd files from the selected directory

for root, dirs, files in walk(ptargetFolder):
    for file in files:
        abspath = (join(root, file))
        filename = abspath.find(".mxd")
        if filename >0:
            mxd = arcpy.mapping.MapDocument(abspath)
            arcpy.AddMessage('Processing file '+abspath)
            for df in arcpy.mapping.ListDataFrames(mxd):
                df.spatialReference = pSR
            mxd.save()

    del mxd
