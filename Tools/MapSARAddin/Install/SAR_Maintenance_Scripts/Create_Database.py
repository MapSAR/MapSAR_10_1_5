
# Takes an original database and makes a copy reprojecting the database and
# MXD files to the desired spatial reference
#
# Description: Input database and map templates
# Copies and converts them to the desired spatial reference
# Jon Pedder - MapSAR
# version - 8/5/13
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
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, sys, os, distutils
from arcpy import env
from os.path import join, abspath
from os import walk
from distutils.core import setup

# Get parameters from user input
# 0. Input folder to walk to look for all mxd files - folder
# 1. Input database - file
# 2. Folder to store the new database and mxd files - folder
# 3. Spatial reference selection

MXDFolder = arcpy.GetParameterAsText(0)
InputDatabase = arcpy.GetParameterAsText(1)
OutputFolder = arcpy.GetParameterAsText(2)
newSpatialReference = arcpy.GetParameterAsText(3)
# Set Vars and overwrite option to true
arcpy.env.overwriteOutput = True
arcpy.env.workspace = InputDatabase

OutputDatabase = "SAR_Default.gdb"
OutputWorkspace = '{0}\\{1}'.format(OutputFolder,OutputDatabase)

def createDatabase():

    arcpy.AddMessage("Creating database, processing features and tables")
    # Create a new database
    arcpy.CreateFileGDB_management(OutputFolder, OutputDatabase,'CURRENT')

    # Copy FC's to the new database
    dsList = arcpy.ListDatasets()
    fcList = arcpy.ListFeatureClasses()
    tables = arcpy.ListTables()

    # Project the datasets and featureclasses and write to target db
    projectDS = ['{0}\\{1}'.format(InputDatabase,str(ds)) for ds in dsList]
    arcpy.BatchProject_management(projectDS, OutputWorkspace,newSpatialReference)
    projectFC = ['{0}\\{1}'.format(InputDatabase,str(fc)) for fc in fcList]
    arcpy.BatchProject_management(projectFC, OutputWorkspace,newSpatialReference)

    # Copy Tables to the new database
    arcpy.TableToGeodatabase_conversion(tables, OutputWorkspace)

def createMXD():
    arcpy.AddMessage("Creating MapSAR mxd's")
    distutils.file_util.copy_file(MXDFolder+'/'+'MapSAR.mxd',OutputFolder+'/'+'MapSAR.mxd')
    distutils.file_util.copy_file(MXDFolder+'/'+'MapSAR_Basic.mxd',OutputFolder+'/'+'MapSAR_Basic.mxd')

    # Copy map template folders and files
    arcpy.AddMessage("Building template folders and Templates")
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Export',OutputFolder+'/'+'Export')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Layer_Templates',OutputFolder+'/'+'Layer_Templates')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Map_Templates',OutputFolder+'/'+'Map_Templates')

    # Walk through the folder structure, look at each mxd, set it's new spatial reference
    # and adjust the source data path to match the new database.
    arcpy.AddMessage('Seting spatial reference on mxd files')
    for root, dirs, files in walk(OutputFolder):
         for file in files:
                abspath = (join(root, file))
                if abspath.find(".mxd")>0:
                    arcpy.AddMessage('Setting Spatial Reference on file {0}'.format(abspath))
                    mxd = arcpy.mapping.MapDocument(abspath)
                    # Update the data source to point to the new database
                    mxd.findAndReplaceWorkspacePaths(InputDatabase,OutputWorkspace)
                    for df in arcpy.mapping.ListDataFrames(mxd):
                        df.spatialReference = newSpatialReference
                    mxd.save()
                    del mxd

def createFolders():
    arcpy.AddMessage('Copying directory structures')
    # Create other directory structures
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Base_Data',OutputFolder+'/'+'Base_Data')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Backups',OutputFolder+'/'+'Backups')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Documents',OutputFolder+'/'+'Documents')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Products',OutputFolder+'/'+'Products')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Incident_data',OutputFolder+'/'+'Incident_data')
    distutils.dir_util.copy_tree(MXDFolder+'/'+'Report_Templates_rlf',OutputFolder+'/'+'Report_Templates_rlf')

# Run functions
createDatabase()
createMXD()
createFolders()