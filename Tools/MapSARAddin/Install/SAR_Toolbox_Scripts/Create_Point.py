#-------------------------------------------------------------------------------
# Name:        Create_Point.py
# Purpose:
#
# Author:      Jon Pedder
#
# Created:     3/17/13
# Copyright:   (c) SMSR 2013
# Use:          Create a new feature from user input UTM values
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

def set_fc(targetTable,value):

    """ set correct FC based on user input, add field names to fields list """
    if targetTable == 'Cell Tower':
        fc = 'hidden_pings'
        fields = ['SHAPE','Display','UTM_E','UTM_N','Description']

    elif targetTable == 'Team Status':
        fc = 'hidden_status'
        fields = ['SHAPE','Display','Location_Easting','Location_Northing','Assignment','Status','Comments']

    elif targetTable == 'Asset':
        fc = "hidden_assets"
        fields = ['SHAPE','Display','utm_e','utm_n','Assets','Description']

    elif targetTable == 'Clue':
        fc = "hidden_clues"
        fields = ['SHAPE','Display','UTM_Easting','UTM_Northing','Assignment','Relevancy','Object']

    elif targetTable == 'Found':
        fc = "hidden_found"
        fields = ['SHAPE','Display','UTM_Easting','UTM_Northing','Description']

    elif targetTable == 'PLS':
        fc = "hidden_pls"
        fields = ['SHAPE','Display','utm_easting','utm_northing','Description']

    return fc, fields

def insetPoint(fc,x,y,fields,values,sr):
    """ Inserts values into point class and zooms to the new feature """
    # Add values to fc
    rows = arcpy.InsertCursor(fc,sr)
    row = rows.newRow()
    for i in range(len(fields)):
        row.setValue(fields[i],values[i])
    rows.insertRow(row)
    del row, rows

    # center map at current extent to new feature
    mxd = arcpy.mapping.MapDocument('CURRENT')
    df = arcpy.mapping.ListDataFrames(mxd, "MapSAR")[0]
    lyr = arcpy.mapping.ListLayers(mxd, fc, df)[0]

    xField = arcpy.AddFieldDelimiters(fc,fields[2])
    yField = arcpy.AddFieldDelimiters(fc,fields[3])
    iQuery = '{0} = {1} AND {2} = {3}'.format(xField,x,yField,y)
    arcpy.AddMessage(iQuery)

    arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", iQuery)
    result = int(arcpy.GetCount_management(lyr).getOutput(0))

    if result == 0:
        arcpy.AddWarning('Opps, no records returned to pan to extent')
    else:
        arcpy.AddMessage('{0} records returned, zooming to new feature'.format(result))

        df.panToExtent(lyr.getSelectedExtent())
        arcpy.RefreshActiveView()
    del mxd, df, lyr


def main():
    targetTable = arcpy.GetParameterAsText(0)
    assignNum = arcpy.GetParameterAsText(1)
    x = arcpy.GetParameterAsText(2)
    y = arcpy.GetParameterAsText(3)
    value = arcpy.GetParameterAsText(4)
    description = arcpy.GetParameterAsText(5)
    sr = arcpy.GetParameterAsText(6)

    pt = arcpy.PointGeometry(arcpy.Point(x,y))

    # point object, display true, utm e, utm n, value for symbology, comment or description
    # Assets uses int for domain so needs custom code
    if targetTable == "Asset":
        assetDict = {'Helibase':2,'Road Block':3,'ICP':1,'Radio Relay':4,'Staging':6,'Helispot':7,'Hasty LZ':8\
            ,'Hazard':9,'Medical Station':5,'Aerial Hazard':10,'Aerial Operations':11,'Airbase':12,'Camp':13,'Fire Vehical Base':14\
            ,'Helipad':15,'IPP':16,'Medical Evacualtion Station':17,'Trail Block':18,'GIS':19}
        value = int(assetDict[value])

    # Accomodate assignment number for team status and clues
    if targetTable == "Clue" or targetTable == "Team Status":
        values = [pt,1,x,y,assignNum,value,description]
    elif targetTable == "PLS" or targetTable == "Found" or targetTable == "Cell Tower":
        values = [pt,1,x,y,description]
    else:
        values = [pt,1,x,y,value,description]

    fc,fields = set_fc(targetTable,value)

    insetPoint(fc,x,y,fields,values,sr)

if __name__ == '__main__':
    main()
