#-------------------------------------------------------------------------------
# Name:        Make_Assignment_Maps
# Purpose:     Export Assignment Maps to Adobe PDF files.
#              Export Task Assignment form to FDF file (Use with PDF Template)
# Author:      Jon Pedder
#
# Created:     3/11/13
# Copyright:   (c) SMSR 2013
# Of Note:     Original FDF file concept, credit Don Ferguson
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

import arcpy
import Make_Assignments_Tasks as tasks
import MapSARfunctions as mapsar
import SetMapElements as mapElms

# Set enviroment
from arcpy import env

# Gather input parameters from user
# 0. SourceFile must be DDP enabled - string
# 1. Folder to store pdf product - string
# 2. Select ALL or SELECTION - string
# 3. PageRange (1,2,5-7 etc) - string
# 4. Map scale
# 5. Include the Task form - boolean

TargetFile = arcpy.GetParameterAsText(0)
mxd = arcpy.mapping.MapDocument(TargetFile)

PDFlocation = arcpy.GetParameterAsText(1)
aSelection = arcpy.GetParameterAsText(2)
Printpages = arcpy.GetParameterAsText(3)
if Printpages != '':
    PageRange = mapsar.getPrintRange(Printpages)
aMapScale = arcpy.GetParameterAsText(4)
aTask = arcpy.GetParameterAsText(5)
aLayers = arcpy.GetParameterAsText(6)
aKML = arcpy.GetParameterAsText(7)
# Set Vars and overwrite option to true
arcpy.env.overwriteOutput = True

def layersOn(mxd, aSelectedLayers):
    """ Requires an mxd as arg 1 and a list of values for arg 2 (to match the dict keys)
    returns no values, just turns on/off selected layers """
    layers = arcpy.mapping.ListDataFrames(mxd,'')[0]

    # Strip out base data and analysis to avoid issues with layer compatability
    for b in layers:
         if 'Base_Data_Group' in b.name:
            arcpy.mapping.RemoveLayer(layers,b)
    # Then set all layers to NOT visible (False)
    for l in layers:
        l.visible = False

    pls = 'Incident_Group','PLS_Subject_Information'
    assets = 'Incident_Assets',
    assignments = 'Assignments_Group','Assignments',
    teamstatus = 'Resource_Team_Status'
    clues = 'Clues_Group','Clues_All'
    tracks = 'GPS_Tracks_And_Routes','Routes'
    segments = 'Segments_Group','Segments',
    boundary = 'Incident_Analysis','Search_Boundary'
    analysis = 'Incident_Analysis'

    layerDict = {'PLS':pls,'Assets':assets,'Assignments':assignments,'Team Status':teamstatus,'Clues':clues,'Tracks':tracks,'Segments':segments,'Boundary':boundary,'Analysis':analysis}

    # Then loop through and turn on selected layers only
    for sp in aSelectedLayers: # loop through the selection list
        if layerDict.has_key(sp): # iterate the dictionary of values
            for lyr in layers: # for each item in the selected list, match the layer name
                if 'Assignments_DDP' in lyr.name:
                        lyr.visible = False
                elif 'Assignments_DDP' not in lyr.name:
                    for t in layerDict[sp]:
                        if t in lyr.name:
                            lyr.visible = True

    return

def doDDP(aSelection, pageNum, aTask,PDFlocation,mxd):
    """ Input aSelection, pageNum, aTask, mxd """
    try:
        # Get current date and time from system
        now = datetime.datetime.now()
        todaydate = now.strftime("%m-%d-%Y")
        todaytime = now.strftime("%H.%M %p")

        # For 10.2 compatibility removed quotes from query
        # iQuery = '"Assignments.Assignment_Number" = {0}'.format(pageNum)

        iQuery = 'Assignments.Assignment_Number = {0}'.format(pageNum)

        ddp = mxd.dataDrivenPages
        indexLayer = ddp.indexLayer
        arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION",iQuery)

        # Set Team Logo, Declination and Scale Bar
        mapElms.setMapElements(mxd)

        arcpy.AddMessage("Creating Map for Assignment # {0} : {1}\Assignment_Map_{2}.pdf".format(str(pageNum), PDFlocation, str(pageNum)))

        # Set map scale
        df = arcpy.mapping.ListDataFrames(mxd, "MapSAR")[0]
        df.scale = aMapScale

        ddp.exportToPDF('{0}/Team_Assignment_Map_{1}.pdf'.format(PDFlocation,pageNum), "SELECTED")
        if aTask == 'true':
            aRows = arcpy.SearchCursor(indexLayer)
            tasks.assignmentExport(PDFlocation, aSelection, aRows)

    except:
        arcpy.AddWarning('There is no assignment # {0} in the system'.format(pageNum))

def exportKML(Assignments_KML,aMapScale):
    # Local variables:
    try:
        Assignments = "3 Assignments_Group\\Assignments"

        arcpy.AddMessage('Exporting GPS file to {0}'.format(Assignments_KML))

        # Process: Layer To KML
        scale = int(aMapScale.split(':')[1])
        arcpy.LayerToKML_conversion(Assignments, Assignments_KML, scale, "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
    except:
        err = arcpy.GetMessages()
        arcpy.AddWarning('Unable to produce GPS assignments\nError {0}'.format(err))

# Check that DDP is enabled on the mxd. If not exit with an error
if(mxd.isDDPEnabled):

    # First check selected layers and turn them on
    aSelectedLayers = aLayers.split(';')
    layersOn(mxd,aSelectedLayers)
    # Populate the current analysis and base data to target mxd
    mapsar.populateBaseData(mxd)

    # Print the DDP assignment
    # Check the selection parameter aSelection, process either the SELECTION or ALL assignments
    if aSelection == "SELECTION":
        arcpy.AddMessage("Assignments Selected are  " + str(sorted(PageRange)))
        for p in sorted(PageRange):
            doDDP(aSelection,p,aTask,PDFlocation,mxd)

    if aSelection == "ALL":
        fc = "Assignments"
        arcpy.SelectLayerByAttribute_management (fc, "CLEAR_SELECTION")
        PageRange = [row[0] for row in arcpy.da.SearchCursor(fc, ("Assignments.Assignment_Number"))]
        arcpy.AddMessage("Assignments Selected are  " + str(sorted(PageRange)))
        for p in sorted(PageRange):
            doDDP(aSelection,p,aTask,PDFlocation,mxd)

    if aKML == 'true':
        Assignments_KML = '{0}/Team_Assignments_GPS.kmz'.format(PDFlocation)
        exportKML(Assignments_KML, aMapScale)

    # Clear the selection and refresh the active view
    arcpy.SelectLayerByAttribute_management("Assignments", "CLEAR_SELECTION")
    arcpy.RefreshActiveView()

else:
  arcpy.AddMessage("Select another template, " + SourceFile + " doesn't have DDP enabled")

del mxd
