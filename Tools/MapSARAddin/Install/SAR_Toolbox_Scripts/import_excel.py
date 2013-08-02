#-------------------------------------------------------------------------------
#      Import A FC from an Excel file
#      Options for Update, Append and Overwrite
#      Jon Pedder - MapSAR
#      Created 6/25/13 @ 2:00pm
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
import datetime, xlrd, os

import MapSARfunctions
arcpy.env.workspace

def updateAAvalues():
    """ Manually updates values created with Attribute Assistant """
    import arcpy
    from arcpy import env
    workspace = arcpy.env.workspace

    # Team Members
    fc = 'Team_Members'
    fields = ['Total_Weight', 'Body_Weight','Gear_Weight']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    try:
        with arcpy.da.UpdateCursor(fc,fields ) as rows:
            for row in rows:
                row[0] = row[1] + row[2]
                rows.updateRow(row)
        del rows,row
    except:
        arcpy.AddWarning('Passing on {0} due to error'.format(fc))

    # Teams
    fc = 'Teams'
    fields = ['Status', 'Team_Available','Team_Name']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    try:
        with arcpy.da.UpdateCursor(fc,fields ) as rows:
            for row in rows:
                if row[0] != 'Unavailable':
                    row[1] = row[2]
                else:
                    row[1] = '<NULL>'
                rows.updateRow(row)
        del rows,row, fc, fields
    except:
        arcpy.AddWarning('Passing on {0} due to error'.format(fc))


    # Periods
    fc = 'Operation_Period'
    fields = ['PeriodText', 'Period']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    try:
        with arcpy.da.UpdateCursor(fc,fields ) as rows:
            for row in rows:
                row[0] = row[1]
                rows.updateRow(row)
        del rows,row, fc, fields
    except:
        arcpy.AddWarning('Passing on {0} due to error'.format(fc))

    # Clues
    fc = 'Clues_Point'
    fields = ['Clue_Number','Clue_NumText']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    try:
        with arcpy.da.UpdateCursor(fc,fields) as rows:
            for row in rows:
                if row[0] != None:
                    row[1] = str(row[0])
                    rows.updateRow(row)
        del rows,row, fc, fields
    except:
        arcpy.AddWarning('Passing on {0} due to error'.format(fc))

    # Assignments
    fc = 'hidden_assignments'
    fields = ['Assignment_Number','AssignNumText','Mileage','SHAPE_Length']
    arcpy.AddMessage('Updating {0} values'.format(fc))
    try:
        with arcpy.da.UpdateCursor(fc,fields) as rows:
            for row in rows:
                if row[0] != None:
                    row[1] = str(row[0])
                row[2] = (row[3] * 0.00062137119) / 2
                rows.updateRow(row)
        del rows,row, fc, fields
    except:
        arcpy.AddWarning('Passing on {0} due to error'.format(fc))

def set_fc(targetTable):
    """ set correct FC based on user input """
    if targetTable == 'Assignments':
        fc = 'Assignments'
    elif targetTable == 'Teams':
        arcpy.AddMessage("Called Teams import")
        fc = 'Teams'
    elif targetTable == 'Team Members':
        fc = 'Team_Members'
    elif targetTable == 'Operational Periods':
        fc = "Operation_Periods"
    elif targetTable == 'Subject Information':
        fc = "PLS_Subject_Information"

    return fc

def exceptionReport(importError,action):
    """ write import errors to a file in teh same directory as teh target file """
    myPath = os.path.dirname(in_excel)
    recordErrors = "{0}\{1}_{2}_import_errors.txt".format(myPath,targetTable,action)
    if os.path.exists(recordErrors):
        errfile = open(recordErrors, "a")
        errfile.write(importError)
        errfile.close()
    else:
        errfile = open(recordErrors, "w")
        errfile.write('{0}\n'.format(importError))
        errfile.close()

def open_spreadsheet(in_excel, sheet_name):
    """ Open the excel file, return worksheet and workbook. """
    try:
        workbook = xlrd.open_workbook(in_excel)
        worksheet = workbook.sheet_by_index(0)
        return worksheet, workbook

    except Exception as err:
        arcpy.AddError(err)
        if __name__ == '__main___':
            sys.exit()
        else:
            raise

def cell_value(cell, datemode):
    """ Check each value for cortrect format and return appropraite value and format """
    if cell.ctype == xlrd.XL_CELL_DATE:
         datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
         if datetuple[3:] == (0, 0, 0):
             return datetime.date(datetuple[0], datetuple[1], datetuple[2])
         return datetime.datetime(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

def read_rows(workbook,worksheet):
    """ workbook,worksheet,fieldList - Reads in spreafdsheet rows and returns data"""
    valueList = []
    fieldList = worksheet.row_values(0)
    for row in range(2,worksheet.nrows):
        # create dictionary of the row values
        values = [ cell_value(c, workbook.datemode) for c in worksheet.row(row) ]
        data = dict(zip(fieldList, values))
        valueList.append(data)
    return valueList

def write_data(fc,data,action):
    arcpy.AddMessage('FC is {0}'.format(fc))
    # If the list has no rows, warn and exit
    if len(data) == 0:
        arcpy.AddIDMessage('WARNING', 117)
        return

    # Read in FC field names
    fc_fields = [f.name for f in arcpy.ListFields(fc)]
    arcpy.AddMessage('fc_fields are {0}'.format(fc_fields))
    # Append or Overwrite
    if action == 'APPEND' or action == 'OVERWRITE ALL':

        if action == 'OVERWRITE ALL':
            # whack all records in fc
            cursor = arcpy.UpdateCursor(fc)
            for row in cursor:
                cursor.deleteRow(row)
            del cursor,row

        rows = arcpy.InsertCursor(fc)
        for row in range(len(data)):
            try:
                lineItem = data[row]
                row = rows.newRow()
                for l in lineItem.keys():
                    print l,lineItem[l]
                    arcpy.AddMessage('Field {0}, Value {1}'.format(l, lineItem[l]))
                    if l != 'OBJECTID':
                        print l,lineItem[l]
                        row.setValue(l,lineItem[l])
                rows.insertRow(row)
            except:
                errors = 'Error appending data to OBJECTID {0} for Field {1}, with value {2}'.format(int(lineItem['OBJECTID']),l, lineItem[l])
                arcpy.AddWarning(errors)
                exceptionReport(errors,action)
    # Update
    elif action == 'UPDATE':
        mxd = arcpy.mapping.MapDocument('CURRENT')
        df = arcpy.mapping.ListDataFrames(mxd, "MapSAR")[0]
        lyr = arcpy.mapping.ListLayers(mxd, fc, df)[0]

        FieldID = arcpy.AddFieldDelimiters(fc,'OBJECTID')

        for i in range(len(data)):
            lineItem = data[i]
            query = '{0} = {1}'.format(FieldID,int(lineItem['OBJECTID']))
            arcpy.SelectLayerByAttribute_management (lyr, "NEW_SELECTION",query)

            result = int(arcpy.GetCount_management(fc).getOutput(0))
            if result == 1:
                try:
                    rows = arcpy.UpdateCursor(fc)
                    for row in rows:
                        for l in lineItem.keys():
                            arcpy.AddMessage('Updating Field {0}'.format(lineItem))
                            if l != 'OBJECTID':
                                if not (lineItem[l] is None):
                                    row.setValue(l,lineItem[l])
                        rows.updateRow(row)
                    del rows, row
                except:
                    errors = 'Error updating data to OBJECTID {0} for Field {1}, with value {2}'.format(int(lineItem['OBJECTID']),l, lineItem[l])
                    arcpy.AddWarning(errors)
                    exceptionReport(errors,action)

        del mxd,df,lyr

def main():
    in_excel = arcpy.GetParameterAsText(0)
    targetTable = arcpy.GetParameterAsText(1)

    action = arcpy.GetParameterAsText(2)
    #sheet_num = arcpy.GetParameterAsText(3)
    sheet_num = 0

    worksheet, workbook = open_spreadsheet(in_excel, sheet_num)
    data = read_rows(workbook,worksheet)

    fc = set_fc(targetTable)
    arcpy.AddMessage('table is ' + fc)
    write_data(fc,data,action)
    del data, workbook, worksheet, fc

    # Update any calculated fielf values and update domains
    updateAAvalues()
    arcpy.AddMessage('Updating Value Lists')
    MapSARfunctions.updateValueLists('script')

if __name__ == '__main__':
    main()
