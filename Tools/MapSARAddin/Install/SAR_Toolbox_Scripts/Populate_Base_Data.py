######################################################################################
# Save Base_Data from current mxd to disk as C:\MapSAR\Tools\Base_Layer.lyr
# then populate that base data to either to a single target or directory of mxd files.
#
# Jon Pedder
# MapSAR 3/11/13
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
######################################################################################

# Import classes
import arcpy, sys, os
from os.path import join, abspath
from os import walk
from arcpy import env
import MapSARfunctions as mapsar

# Set enviroment and overwrite option to true
arcpy.env.overwriteOutput = True

# Gather user input parameters
# TargetFile is a single mxd that will receive the base data
# TargetDir is the folder set of templates that will receive the saved base data
TargetDir = None
TargetFile = None
TargetFile = arcpy.GetParameterAsText(0)
TargetDir = arcpy.GetParameterAsText(1)

# Define vars
mxdlayer = "14 Base_Data_Group"
LayerFile = "C:\MapSAR\TempDir\Base_Layer"
LayerName = LayerFile + '.lyr'


##
##
### Save base_data layer file to disk in c:\MapSAR\TempDir from current mxd.
### If directory does not exist create it
##if os.path.exists('c:\MapSAR\TempDir'):
##        arcpy.SaveToLayerFile_management(mxdlayer,LayerFile,"RELATIVE")
##else:
##        os.makedirs('c:\MapSAR\TempDir')
##        arcpy.SaveToLayerFile_management(mxdlayer,LayerFile,"RELATIVE")
##
### Message to user
##arcpy.AddMessage("Base Data Saved as "+ LayerFile)

# Check to see if we're processing a single file or a directory of files
if TargetFile > "":
        # Message to user
        arcpy.AddMessage("Target File is True = " +TargetFile)
        mxd = arcpy.mapping.MapDocument(TargetFile)
        mapsar.populateBaseData(mxd)

elif TargetDir != "":
        arcpy.AddMessage("Target Directory is true")

        for root, dirs, files in walk(TargetDir):
            for file in files:
                abspath = (join(root, file))
                mxd = arcpy.mapping.MapDocument(abspath)
                arcpy.AddMessage('Processing file '+abspath)
                # Loop for each file in the mxd collection
                for df in arcpy.mapping.ListDataFrames(mxd):
                    mapsar.populateBaseData(mxd)

# Clear vars and release files
del TargetFile, TargetDir, mxd
