
# Name:        Make_Map.py
# Purpose:     Make a single Map suitable for briefing, plans etc.
#              Not for creating DDP maps, see assignments script.
#
# Author:      Jon Pedder
#
# Created:     03/17/2013
# Copyright:   (c) SMSR 2013
# Use:          Run using Toolbox
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

# Import modules
import arcpy, os
import MapSARfunctions as mapsar
import SetMapElements as mapElms
# Set enviroment
from arcpy import env

arcpy.env.overwriteOutput = True

def layersOn(mxd, selectedParams):
    """ Requires an mxd as arg 1 and a list of values for arg 2 (to match the dict keys)
    returns no values, just turns on/off selected layers """

    frames = arcpy.mapping.ListDataFrames(mxd)
    for frame in frames:
        # Remove existing base_data layer
        for lyr in arcpy.mapping.ListLayers(mxd,'', frame):
            lyr.visible = False

    pls = 'Incident_Group','PLS_Subject_Information'
    found = 'Incident_Group','Subject_Found'
    assets = 'Incident_Assets',
    assignments = 'Assignments_Group','Assignments',
    teamstatus = 'Resource_Team_Status'
    clues = 'Clues_All'
    tracks = 'Routes'
    segments = 'Segments',
    boundary = 'Incident_Analysis','Search_Boundary'

    layerDict = {'PLS':pls,'Found':found,'Assets':assets,'Assignments':assignments,'Team_Status':teamstatus,'Clues':clues,'Tracks':tracks,'Segments':segments,'Boundary':boundary}
    for frame in frames:
        # Then loop through and turn on selected layers only
        for sp in selectedParams: # loop through the selection list
            if layerDict.has_key(sp): # iterate the dictionary of values
                for lyr in arcpy.mapping.ListLayers(mxd,'', frame): # for each item in the selected list, match the layer name
                    if 'Assignments_DDP' in lyr.name:
                            lyr.visible = False
                    elif 'Assignments_DDP' not in lyr.name:
                        for t in layerDict[sp]:
                            if t in lyr.name:
                                lyr.visible = True

    return


def populateAnalysisData(mxd):
    """ Saves current Incident_Analysis file to disk, loads lyr file from disk to target mxd"""
    import os
    # Gather information to copy over base_data

    # Define vars
    mxdlayer = "13 Incident_Analysis"
    LayerFile = "Incident_Analysis"
    LayerName = LayerFile + '.lyr'

    # Save base_data layer file to disk in c:\MapSAR\TempDir from current mxd.
    # If directory does not exist create it
    TempDir = r'c:\mapsar\Tools\Layer_Templates'
    baselayer = '{0}\{1}'.format(TempDir,LayerName)

    if os.path.exists(TempDir):
          arcpy.SaveToLayerFile_management(mxdlayer,baselayer,"RELATIVE")
    else:
          os.makedirs(TempDir)
          arcpy.SaveToLayerFile_management(mxdlayer,baselayer,"RELATIVE")

    # Check for existing Incident_Analysis layers in target. If present remove them
    frames = arcpy.mapping.ListDataFrames(mxd)
    for frame in frames:
         for lyr in arcpy.mapping.ListLayers(mxd, "", frame):
             if 'Analysis' in lyr.name:
                  arcpy.mapping.RemoveLayer(frame,lyr)

    # Check if the layer exists on disk and add to frames
    if os.path.isfile(baselayer):
        frames = arcpy.mapping.ListDataFrames(mxd)
        for frame in frames:
            addLayer = arcpy.mapping.Layer(baselayer)
            arcpy.mapping.AddLayer(frame, addLayer, "BOTTOM")
    else:
          # If not alert user of an error
          arcpy.AddMessage('{0} does not exist'.format(baselayer))


# Gather input parameters from user
# 0. TargetFile mxd - string
# 1. Folder to store pdf product - string
# 2. Name of saved map - string
# 3. Title of the Map - string
# 4. Map Scale MAIN - from value list- string
# 5. Map Scale INSET - from value list- string
# 6. Center map on - from value list - string
# 7. Values - from value list - string
# 8. PDF Quality - from value list - string
# 9. PDF Print speed - from value lilst - string
# 10. Use base data in current map - boolean
# 11. Layers to make visible

TargetFile = arcpy.GetParameterAsText(0)
PDFlocation = arcpy.GetParameterAsText(1)
aMapName = arcpy.GetParameterAsText(2)
aMapTitle = arcpy.GetParameterAsText(3)
aMapScaleMain = arcpy.GetParameterAsText(4)
aMapScaleInset = arcpy.GetParameterAsText(5)
aKeyvalue = arcpy.GetParameterAsText(6)
aSelectedvalue = arcpy.GetParameterAsText(7)
aDPI = arcpy.GetParameterAsText(8)
aQuality = arcpy.GetParameterAsText(9)
aBase_Data = arcpy.GetParameterAsText(10)
aLayers = arcpy.GetParameterAsText(11)


# BASE DATA COPY STARTS HERE#
 ############################
Targetmxd = arcpy.mapping.MapDocument(TargetFile)

if('multiscale' in Targetmxd.tags):
    # Set visable layers first, then populate base data
    selectedParams = aLayers.split(';')
    arcpy.AddMessage(selectedParams)
    layersOn(Targetmxd,selectedParams)

    if 'Analysis' in selectedParams:
        populateAnalysisData(Targetmxd)

    # Use parameters from user input
    MapTitle = aMapTitle
    MapName = aMapName
    MapLocation = PDFlocation + "/" + aMapName + ".pdf"

    # Populate the current base data to target mxd and frames
    if aBase_Data == "true":
        arcpy.AddMessage('Loading base data')

        mxdlayer = " 14 Base_Data_Group"
        LayerFile = "Base_Layer"
        LayerName = LayerFile + '.lyr'

        # Save base_data layer file to disk in c:\MapSAR\TempDir from current mxd.
        # If directory does not exist create it
        TempDir = r'c:\mapsar\Tools\Layer_Templates'
        baselayer = '{0}\{1}'.format(TempDir,LayerName)

        if os.path.exists(TempDir):
              arcpy.SaveToLayerFile_management(mxdlayer,baselayer,"RELATIVE")
        else:
              os.makedirs(TempDir)
              arcpy.SaveToLayerFile_management(mxdlayer,baselayer,"RELATIVE")

        # Check for existing Base_Data layers in target. If present remove them
        frames = arcpy.mapping.ListDataFrames(Targetmxd)
        for frame in frames:
            # Remove existing base_data layer
            for lyr in arcpy.mapping.ListLayers(Targetmxd,'*Base_Data*', frame):
                if 'Base_Data' in lyr.name:
                    arcpy.mapping.RemoveLayer(frame,lyr)

            # Check if the layer exists on disk
            if os.path.isfile(baselayer):
                addLayer = arcpy.mapping.Layer(baselayer)
                arcpy.mapping.AddLayer(frame, addLayer, "BOTTOM")
                addLayer.visible = True
            else:
                # If not alert user of an error
                arcpy.AddMessage(baselayer +' does not exist')

    # Add text elements to the map
    for elm in arcpy.mapping.ListLayoutElements(Targetmxd, "TEXT_ELEMENT","MapTitle"):
    	elm.text = "<BOL> " + MapTitle + "</BOL>"

    for elm in arcpy.mapping.ListLayoutElements(Targetmxd, "TEXT_ELEMENT","MapName"):
    	elm.text = MapName

    # Set Team Logo, Declination and Scale Bar
    mapElms.setMapElements(Targetmxd)

    # Load dictionary of fetaure and field names
    DcenterOn = mapsar.initializeDcenterOn()

    # Build SQL query to get selection to center map around
    # Keys = PLS,Single Asset,Single Clue,Single Assignment,Single Segment,All Assignments,All Segments
    intList = ['Single Asset','Single Clue','Single Assignment','All Assignments']
    strList = ['Single Segment','PLS','All Segments']

    # Determine Featureclass and field name
    # Tuple format - Feature class, display text, Layername, (Optional fields - field 1, field 2)
    MapFC = DcenterOn[aKeyvalue][2]
    MapField = DcenterOn[aKeyvalue][3]

    # arcpy.Addfieldelimiters here. Code revised for 10.2 compatability
    # qField = arcpy.AddFieldDelimiters(MapFC, MapField)
    if MapFC != 'Assignments':
        qField = arcpy.AddFieldDelimiters(MapFC, MapField)
    else:
        qField = MapField

    # Check if the selection is all features or single feature
    # If it's all features
    if aKeyvalue.startswith('All'):
        # Check if the selection is an number or string
        if aKeyvalue in intList:
            iQuery = ('{0} > 0').format(qField)
        elif aKeyvalue in strList:
            iQuery = ("{0} > ''").format(qField)
    # If it's a single feature
    elif not aKeyvalue.startswith('All'):
        # Check if the selection is an number or...
        if aKeyvalue in intList:
            # Pull search value from selection
             if '-' in aSelectedvalue:
                queryVal = aSelectedvalue.split('-')
                iQuery = ('{0} = {1}').format(qField,int(queryVal[0]))
             elif '-' not in aSelectedvalue:
                iQuery = ('{0} = {1}').format(qField,int(aSelectedvalue))
        # Check if the selection is an number or string
        elif aKeyvalue in strList:
            # Pull search value from selection
            if '-' in aSelectedvalue:
                queryVal = aSelectedvalue.split('-')
                iQuery = ("{0} = '{1}'").format(qField,queryVal[0])
            elif '-' not in aSelectedvalue:
                iQuery = ("{0} = '{1}'").format(qField,aSelectedvalue)

    # Zoom to the selected features
    # Use the SelectLayerByAttribute tool to select the center and zoom to the selection

    # center and set scales
    dframes = arcpy.mapping.ListDataFrames(Targetmxd)
    for frame in dframes:
        # Set map scale
        lyr = arcpy.mapping.ListLayers(Targetmxd,MapFC,frame)
        arcpy.SelectLayerByAttribute_management(lyr[0], "NEW_SELECTION",iQuery)
        frame.panToExtent(lyr[0].getSelectedExtent())

        if 'Main' in frame.name:
            frame.scale = aMapScaleMain
        elif 'Inset' in frame.name:
            frame.scale = aMapScaleInset

        # clear selection so highlights don't print
        arcpy.SelectLayerByAttribute_management(lyr[0], "CLEAR_SELECTION")

    arcpy.AddMessage("Exporting map {0}".format(MapName))

    # Export the map to a .pdf
    Targetmxd.save()
    arcpy.mapping.ExportToPDF(Targetmxd,MapLocation, resolution = aDPI, image_quality = aQuality,georef_info = "false")

    # Clear vars
    del Targetmxd, lyr, MapFC, MapField
else:
    arcpy.AddMessage('\nPlease select a map from the Multi_Scale_Maps templates\n')
