#-------------------------------------------------------------------------------
# Name:        Write Incident Info
# Purpose:
#
# Author:      SMSR
#
# Created:     04/05/2013
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
import arcpy
import MapSARfunctions as MapSAR

def updateIncident():
    """write int information to Incident_Information FC"""
    try:
        arcpy.AddMessage('\nUpdating Incident Information\n')

        Date_Prepared = arcpy.GetParameterAsText(0)
        End_Date = arcpy.GetParameterAsText(1)
        Incident_Name = arcpy.GetParameterAsText(2)
        General_Objectives = arcpy.GetParameterAsText(3)
        MapUnit = arcpy.GetParameterAsText(4)
        Declination = arcpy.GetParameterAsText(5)
        teamlogo = arcpy.GetParameterAsText(6)

        fc = 'Incident_Information'
        field = ['Date_Prepared','End_Date','Incident_Name','General_Objectives','MapUnit','Declination','logo']

        result = int(arcpy.GetCount_management(fc).getOutput(0))
        if result == 0:
            rows = arcpy.InsertCursor(fc)
            for i in range(1):
                row = rows.newRow()
                row.Date_Prepared = Date_Prepared
                if End_Date != '': row.End_Date = End_Date
                row.Incident_Name = Incident_Name
                row.General_Objectives = General_Objectives
                row.MapUnit = MapUnit
                if Declination != None: row.Declination = Declination
                if teamlogo != None: row.logo = teamlogo
                rows.insertRow(row)
            del rows

        elif result == 1:
            with arcpy.da.UpdateCursor(fc,field) as cursor:
                for row in cursor:
                    row[0] = Date_Prepared
                    if End_Date != '': row[1] = End_Date
                    row[2] = Incident_Name
                    row[3] = General_Objectives
                    row[4] = MapUnit
                    if Declination != None: row[5] = Declination
                    if teamlogo != None: row[6] = teamlogo
                    cursor.updateRow(row)

        del row

        try:
            MapSAR.updateValueLists('script')
        except:
            pass
        return(MapUnit,teamlogo)

    except SystemExit as err:
        pass

if __name__ == '__main__':
    updateIncident()
