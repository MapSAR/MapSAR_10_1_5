#-------------------------------------------------------------------------------
# Name:        updateLayers.py
# Purpose:     Remove layers from a directory of mxd files and add new layers from directory
#               TIP: Rename layers on disk to order teh layers in the mxd
#
# Author:      Jon Pedder
#
# Created:     16/08/2013
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
# ---------------------------------------------------------------------------

import arcpy, sys, os
from os.path import join, abspath
from os import walk


def removeLayers(mxd,file):
    arcpy.AddMessage('Removing Layers from '+file)
    frames = arcpy.mapping.ListDataFrames(mxd)
    for df in frames:
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            arcpy.mapping.RemoveLayer(df, lyr)

    del frames

def addLayers(mxd,layerList,Lroot,file):
    arcpy.AddMessage('Adding Layers to '+file)
    frames = arcpy.mapping.ListDataFrames(mxd)
    for df in frames:
        for l in layerList:
            layerPath = (join(Lroot, l))
            addLayer = arcpy.mapping.Layer(layerPath)
            arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

        df.scale = '1:24,000'

    del frames


def main():
    TargetDir = arcpy.GetParameterAsText(0)
    layerPath = arcpy.GetParameterAsText(1)
    defaultDB = arcpy.GetParameterAsText(2)

    # List all layer files in layerPath and sort the list
    layerList = []
    for layersRoot, layersDirs, layerFiles in walk(layerPath):
        for layer in layerFiles:
            if 'lyr' in layer:
                layerList.append(layer)

    layerList = sorted(layerList, key=lambda item: (int(item.partition(' ')[0])
        if item[0].isdigit() else float('inf'), item))

    arcpy.AddMessage('Target MXD Directory is {0} \n'.format(TargetDir))
    arcpy.AddMessage('Source Layers Directory is {0} \n'.format(layerPath))
    arcpy.AddMessage('layers are {0}'.format(layerList))

    # Walk through each mxd file, first remove all layers them populate with layers from layerList
    for root, dirs, files in walk(TargetDir):
        for file in files:
            abspath = (join(root, file))
            if 'mxd' in file:
                mxd = arcpy.mapping.MapDocument(abspath)
                removeLayers(mxd,file)
                addLayers(mxd,layerList,layersRoot,file)

                arcpy.AddMessage('Setting workspace and data path')
                arcpy.env.workspace = defaultDB
                mxd.findAndReplaceWorkspacePaths('',defaultDB)
                mxd.save()

if __name__ == '__main__':
    main()






