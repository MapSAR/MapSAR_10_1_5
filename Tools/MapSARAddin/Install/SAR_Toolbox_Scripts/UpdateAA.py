#      Update values used with Attrubute Assistant
#      Options for Update, Append and Overwrite
#      Jon Pedder - MapSAR
#      Updated 6/25/13 @ 2:00pm
#
#     Licence:
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

# Import modules

import arcpy
from arcpy import env

def updateAAvalues():

    # Team Members
    fc = 'Team_Members'
    fields = ['Total_Weight', 'Body_Weight','Gear_Weight']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    with arcpy.da.UpdateCursor(fc,fields ) as rows:
        for row in rows:
            if row[2] > 0 and row[2] > 0:
                row[0] = row[1] + row[2]
            rows.updateRow(row)

    # Teams
    fc = 'Teams'
    fields = ['Status', 'Team_Available','Team_Name']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    with arcpy.da.UpdateCursor(fc,fields ) as rows:
        for row in rows:
            if row[0] != 'Unavailable':
                row[1] = row[2]
            else:
                row[1] = '<NULL>'
            rows.updateRow(row)


    # Periods
    fc = 'Operation_Period'
    fields = ['PeriodText', 'Period']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    with arcpy.da.UpdateCursor(fc,fields ) as rows:
        for row in rows:
            row[0] = row[1]
            rows.updateRow(row)

    # Clues
    fc = 'Clues_Point'
    fields = ['Clue_Number', 'Clue_NumText']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    with arcpy.da.UpdateCursor(fc,fields ) as rows:
        for row in rows:
            if row[0] > 0:
                row[1] = str(row[0])
            else:
                row[1] = '<NULL>'
            rows.updateRow(row)

    # Assignments
    fc = 'Assignments'
    arcpy.AddMessage('Updating {0} values'.format(fc))
    rows = arcpy.UpdateCursor(fc)
    for row in rows:
        row.setValue('AssignNumText', str(row.getValue('Assignment_Number')))
        row.setValue('Mileage', row.getValue('SHAPE_Length') * 0.00062137119) / 2
        rows.updateRow(row)

def main():
    updateValues()

if __name__ == '__main__':
    main()
