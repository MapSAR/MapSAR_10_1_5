#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      SMSR
#
# Created:     06/04/2013
# Copyright:   (c) SMSR 2013
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
#-------------------------------------------------------------------------------

import arcpy, sys, os
from os.path import join, abspath
from os import walk

TargetDir = arcpy.GetParameterAsText(0)

for root, dirs, files in walk(TargetDir):
    for file in files:
        abspath = (join(root, file))
        if 'mxd' in file:
            mxd = arcpy.mapping.MapDocument(abspath)
            arcpy.AddMessage('Processing file '+abspath)
            frames = arcpy.mapping.ListDataFrames(mxd)
            for frame in frames:
                frame.credits = 'Sierra Madre Search & Rescue Team www.smsr.org'
                frame.description = 'MapSAR Template v10.1.6'

            mxd.credits = 'Sierra Madre Search & Rescue Team www.smsr.org'
            mxd.summary = 'Mapping Template for Search And Rescue. \n MapSAR Template v10.1.6'
            mxd.description = 'MapSAR wilderness search and rescue GIS data model and related python scripting Copyright (C) 2013  - Jon Pedder & SMSR \
            This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,\
            either version 3 of the License, or (at your option) any later version.\
            This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\
            See the GNU General Public License for more details. GNU General Public License ee <http://www.gnu.org/licenses/>.'

            if 'MultiScale' in file:
                mxd.tags = 'SAR, Template, Data Model, MapSAR, Rescue, SMSR, multiscale'
            else:
                mxd.tags = 'SAR, Template, Data Model, MapSAR, Rescue, SMSR'

            mxd.hyperlinkBase = 'http://www.mapsar.net'
            mxd.author = 'Jon Pedder'

            mxd.save()
