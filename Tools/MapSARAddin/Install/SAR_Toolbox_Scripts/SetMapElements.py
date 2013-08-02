#-------------------------------------------------------------------------------
# Name:        Set_Map_Elements
# Purpose:      Set Team Logo, Declination and mapScale bar
#
# Author:      Jon Pedder
#
# Created:     5/5/13
# Copyright:   (c) jp8 2013
# Licence:     <your licence>
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

import arcpy, os
from arcpy import env

arcpy.env.workspace

def getDataframe():
    """ get current mxd and dataframe returns mxd, frame"""
    try:
        mxd = arcpy.mapping.MapDocument('CURRENT')
        frame = arcpy.mapping.ListDataFrames(mxd,'MapSAR')[0]

        return(mxd,frame)

    except SystemExit as err:
            pass

def swapScalePositions(milesBar,milesList,kiloBar,kiloList):
    """ Swap positions of the Miles and Kilo scale bars based on Incident preferences"""
    milesBar.elementPositionX = kiloList[0]
    milesBar.elementPositionY = kiloList[1]
    milesBar.elementHeight = kiloList[2]
    milesBar.elementWidth = kiloList[3]

    kiloBar.elementPositionX = milesList[0]
    kiloBar.elementPositionY = milesList[1]
    kiloBar.elementHeight = milesList[2]
    kiloBar.elementWidth = milesList[3]

def setScaleBar(mxd,mapScale):
    """ Set the positions of the Miles and Kilo scale bars based on Incident preferences"""
    milesList = []
    kiloList = []
    elms = arcpy.mapping.ListLayoutElements(mxd,'MAPSURROUND_ELEMENT')

    # arcpy.AddMessage('mapScale = {0}'.format(mapScale))
    # read current element positions and populate lists
    for elm in elms:
        if 'Miles' in elm.name:
            milesBar = elm
            milesList.append(milesBar.elementPositionX)
            milesList.append(milesBar.elementPositionY)
            milesList.append(milesBar.elementHeight)
            milesList.append(milesBar.elementWidth)
        if 'Kilo' in elm.name:
            kiloBar = elm
            kiloList.append(kiloBar.elementPositionX)
            kiloList.append(kiloBar.elementPositionY)
            kiloList.append(kiloBar.elementHeight)
            kiloList.append(kiloBar.elementWidth)
    # arcpy.AddMessage('milesList[0] = {0} kiloList[0] = {1}'.format(milesList[0],kiloList[0]))
    if 'Miles' in mapScale:
        if milesList[1] < kiloList[1]:
            arcpy.AddMessage('Setting Miles')
            swapScalePositions(milesBar,milesList,kiloBar,kiloList)
    elif 'Kilometers' in mapScale:
        if kiloList[1] < milesList[1]:
            arcpy.AddMessage('Setting Kilos')
            swapScalePositions(milesBar,milesList,kiloBar,kiloList)

def setLogo(mxd,path):
    """ Set the teamlogo element to the value of path """
    # arcpy.AddMessage('Setting Logo')
    elms = arcpy.mapping.ListLayoutElements(mxd,"PICTURE_ELEMENT")
    for i in elms:
        if 'teamlogo' in i.name:
            i.sourceImage = path

def setDeclination(mxd,declination):
    """ Set the mapdec element to the value of declination """
    # arcpy.AddMessage('Setting Declination')
    elms = arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")
    for i in elms:
        if 'mapdec' in i.name:
            if declination != '':
                i.text = 'Magnetic Declination\n{0}'.format(declination)
            elif declination == '':
                i.text = ' '

def setMapElements(mxd):
    # Script starts here
    milesBar = None
    kiloBar = None
    fc = 'Incident_Information'
    field = ['MapUnit','Declination','logo']

    result = int(arcpy.GetCount_management(fc).getOutput(0))
    # arcpy.AddMessage('result is {0}'.format(result))

    if result == 0:
        arcpy.AddMessage('result is == 0')
        mapScale = 'Miles'
        setScaleBar(mxd,mapScale)
        declination = ''
        setDeclination(mxd,declination)
        path = ''

    elif result == 1:
        # arcpy.AddMessage('result is == 1')
        values = [row for row in arcpy.da.SearchCursor(fc, (field))]
        mapScale = values[0][0]
        declination = values[0][1]
        path = values[0][2]

        setScaleBar(mxd,mapScale)
        setDeclination(mxd,declination)

        if os.path.exists(path):
            setLogo(mxd,path)

if __name__ == '__main__':
    arcpy.AddMessage('Setting Map Properties')
    setMapElements('CURRENT')




