#-------------------------------------------------------------------------------
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
    layers = arcpy.mapping.ListDataFrames(mxd,'')[0]

    # Strip out base data to avoid issues with layer compatability
    for b in layers:
         if 'Base_Data_Group' in b.name:
            arcpy.mapping.RemoveLayer(layers,b)
    # Then set all layers to NOT visible (False)
    for l in layers:
        l.visible = False

    pls = 'Incident_Group','PLS_Subject_Information'
    found = 'Incident_Group','Subject_Found'
    assets = 'Incident_Assets',
    assignments = 'Assignments_Group','Assignments',
    teamstatus = 'Resource_Team_Status'
    clues = 'Clues_Group','Clues_All'
    tracks = 'GPS_Tracks_And_Routes','Routes'
    segments = 'Segments_Group','Segments',
    boundary = 'Incident_Analysis','Search_Boundary'

    layerDict = {'PLS':pls,'Found':found,'Assets':assets,'Assignments':assignments,'Team_Status':teamstatus,'Clues':clues,'Tracks':tracks,'Segments':segments,'Boundary':boundary}

    # Then loop through and turn on selected layers only
    for sp in selectedParams: # loop through the selection list
        if layerDict.has_key(sp): # iterate the dictionary of values
            for lyr in layers: # for each item in the selected list, match the layer name
                if 'Assignments_DDP' in lyr.name:
                        lyr.visible = False
                elif 'Assignments_DDP' not in lyr.name:
                    for t in layerDict[sp]:
                        if t in lyr.name:
                            lyr.visible = True

    return


# Gather input parameters from user
# 0. TargetFile mxd - string
# 1. Folder to store pdf product - string
# 2. Name of saved map - string
# 3. Title of the Map - string
# 4. Map Scale - from value list- string
# 5. Center map on - from value list - string
# 6. Values - from value list - string
# 7. PDF Quality - from value list - string
# 8. PDF Print speed - from value lilst - string
# 9. Use base data in current map - boolean

TargetFile = arcpy.GetParameterAsText(0)
PDFlocation = arcpy.GetParameterAsText(1)
aMapName = arcpy.GetParameterAsText(2)
aMapTitle = arcpy.GetParameterAsText(3)
aMapScale = arcpy.GetParameterAsText(4)
aKeyvalue = arcpy.GetParameterAsText(5)
aSelectedvalue = arcpy.GetParameterAsText(6)
aDPI = arcpy.GetParameterAsText(7)
aQuality = arcpy.GetParameterAsText(8)
aBase_Data = arcpy.GetParameterAsText(9)
aLayers = arcpy.GetParameterAsText(10)

# BASE DATA COPY STARTS HERE#
 ############################
Targetmxd = arcpy.mapping.MapDocument(TargetFile)

if(Targetmxd.isDDPEnabled):
    arcpy.AddMessage('\nPlease use a map that is NOT designed for Team Assignments\nMeaning an mxd that is not enabled with DataDrivenPages\n\nSelect from Basic_Maps, Briefing_Maps or Status_Maps\n')
elif('multiscale' in Targetmxd.tags):
    arcpy.AddMessage('\nPlease use a map that is NOT designed for Multiscale Maps\nPlease select a Standard Map Template from Basic_Maps, Briefing_Maps or Status_Maps\n')
else:
    # Set visable layers first, then populate base data
    selectedParams = aLayers.split(';')
    arcpy.AddMessage(selectedParams)
    layersOn(Targetmxd,selectedParams)

     # Gather information to copy over base_data and analysis data
    if 'Analysis' in selectedParams:
        mapsar.populateAnalysisData(Targetmxd)
    if aBase_Data == "true":
        # Populate the current base data to target mxd
        mapsar.populateBaseData(Targetmxd)

    # EXPORT MAP STARTS HERE #
    ##########################

    # Use parameters from user input
    MapTitle = aMapTitle
    MapName = aMapName
    MapLocation = PDFlocation + "/" + aMapName + ".pdf"

    arcpy.AddMessage("Centering Map")

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

    arcpy.AddMessage("Generating Map " + MapName)

    # arcpy.Addfieldelimiters here
    qField = arcpy.AddFieldDelimiters(MapFC, MapField)

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

    df = arcpy.mapping.ListDataFrames(Targetmxd, "MapSAR")[0]
    lyr = arcpy.mapping.ListLayers(Targetmxd, MapFC, df)[0]

    # Use the SelectLayerByAttribute tool to select the center and zoom to the selection
    arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", iQuery)

    # Zoom to the selected features
    # Set maps scale, if Auto allow for borders by * 1.2
    df.zoomToSelectedFeatures()
    if aMapScale == "AUTO":
      df.scale = df.scale * 1.1
    else:
      df.scale = aMapScale

    # Clear the selection for printing, so it's not highlighted
    arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

    # Export the map to a .pdf
    arcpy.mapping.ExportToPDF(Targetmxd,MapLocation, resolution=aDPI, image_quality=aQuality,georef_info="true")

    # Clear vars
    del Targetmxd, df, lyr, MapFC, MapField
