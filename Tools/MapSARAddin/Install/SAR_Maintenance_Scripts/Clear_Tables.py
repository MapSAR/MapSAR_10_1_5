#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:      Clear selected database featureclasses of data
#
# Author:      Jon Pedder
#
# Created:     5/4/13
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

def ClearData():
    """ Clears data from selected feature classes """
    fcList = {}
    fcList['Incident_Information'] = arcpy.GetParameter(1)
    fcList['Operation_Periods'] = arcpy.GetParameter(2)
    fcList['PLS_Subject_Information'] = arcpy.GetParameter(3)
    fcList['2 Incident_Assets'] = arcpy.GetParameter(4)
    fcList['Teams'] = arcpy.GetParameter(5)
    fcList['Team_Members'] = arcpy.GetParameter(6)
    fcList['Assignments'] = arcpy.GetParameter(7)
    fcList['Search_Segments'] = arcpy.GetParameter(8)
    fcList['Clues_Point'] = arcpy.GetParameter(9)

    for k in fcList.keys():
        if fcList[k] == True:
            arcpy.AddMessage('\nDeleting data from {0}\n'.format(k))
            with arcpy.da.UpdateCursor(k,'*') as cursor:
                for c in cursor:
                    arcpy.AddWarning('Deleting row {0}'.format(c))
                    cursor.deleteRow()


            # arcpy.DeleteFeatures_management(k)

if __name__ == '__main__':

   # Set enviroment
   import arcpy
   from arcpy import env
   ClearData()

