#-------------------------------------------------------------------------------
#      Export A FC to an Excel file
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
#   Script is ESRI's Table to Excel modified to work specificly with MapSAR
"""
Tool name: Table To Excel
Source: TableToExcel.py
Author: ESRI

Convert an table to a MS Excel spreadsheet.
"""

import arcpy
import os
import sys
import xlwt
import datetime

from arcpy import env

class clsField(object):
    """ Class to hold properties and behavior of the output fields
    """
    @property
    def alias(self):
        return self._field.aliasName

    @property
    def name(self):
        return self._field.name

    @property
    def domain(self):
        return self._field.domain

    @property
    def type(self):
        return self._field.type

    @property
    def length(self):
        return self._field.length

    def __init__(self, f, i, subtypes):
        """ Create the object from a describe field object
        """
        self.index = None
        self._field = f
        self.subtype_field = ''
        self.domain_desc = {}
        self.subtype_desc = {}
        self.index = i

        # Inception inspired dictionary in a dictionary
        for st_key, st_val in subtypes.iteritems():
            if st_val['SubtypeField'] == f.name:
                self.subtype_desc[st_key] = st_val['Name']
                self.subtype_field = f.name
            for k, v in st_val['FieldValues'].iteritems():
                if k == f.name:
                    if len(v) == 2:
                        if v[1]:
                            self.domain_desc[st_key]= v[1].codedValues
                            self.subtype_field = st_val['SubtypeField']

    def __repr__(self):
        """ Nice representation for debugging  """
        return '<clsfield object name={}, alias={}, domain_desc={}>'.format(self.name,
                                                                self.alias,
                                                                self.domain_desc)

    def updateValue(self, row, fields):
        """ Update value based on domain/subtypes """
        value = row[self.index]
        if self.subtype_field:
            subtype_val = row[fields.index(self.subtype_field)]
        else:
            subtype_val = 0

        if self.subtype_desc:
            value = self.subtype_desc[row[self.index]]

        if self.domain_desc:
            try:
                value = self.domain_desc[subtype_val][row[self.index]]
            except:
                pass # not all subtypes will have domain

        # Return the validated value
        return value

def get_field_defs(in_table, use_domain_desc):
    desc = arcpy.Describe(in_table)

    subtypes ={}
    if use_domain_desc:
        subtypes = arcpy.da.ListSubtypes(in_table)

    fields = []
    for i, field in enumerate([f for f in desc.fields
                                if f.type in ["Date","Double","Guid",
                                              "Integer","OID","Single",
                                              "SmallInteger","String"]]):
        fields.append(clsField(field, i, subtypes))

    return fields

def validate_sheet_name(sheet_name):
    """ Validate sheet name to excel limitations
         - 31 character length
         - there characters not allowed : \ / ? * [ ]
    """
    import re
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:31]

    # Replace invalid sheet character names with an underscore
    r = re.compile(r'[:\\\/?*\[\]]')
    sheet_name = r.sub("_", sheet_name)

    return sheet_name

def add_error(id, s=None):
    """ Return errors """

    arcpy.AddIDMessage("ERROR", id, s if s else None)
    if __name__ == '__main__':
        sys.exit(1)
    else:
        raise arcpy.ExecuteError, arcpy.GetIDMessage(id)


def table_to_excel(in_table, output, fields):
    """ Writes a table to an XLS file """

    use_field_alias=False
    use_domain_desc=False

    # fields = get_field_defs(in_table, use_domain_desc)

    arcpy.env.overwriteOutput = True


    if int(arcpy.GetCount_management(in_table)[0]) > 65535:
        # Input table exceeds the 256 columns limit of the .xls file format.
        add_error(1531)

    elif len(fields) > 255:
        # Input table exceeds the 65535 rows limit of the .xls file format.
        add_error(1530)

    # Make spreadsheet
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(validate_sheet_name(os.path.splitext(os.path.basename(output))[0]))

    # Add first (header) row
    header_style = xlwt.easyxf("font: bold on; align: horiz center; pattern: pattern solid, fore-colour 0x16;")

    for index, field in enumerate(fields):
        worksheet.write(0, index, field.name, header_style)
        if field.type == 'String':
            worksheet.col(index).width = min(50, field.length)*256
        else:
            worksheet.col(index).width = 16*256

    # Freeze panes
    worksheet.set_panes_frozen(True)
    worksheet.set_horz_split_pos(1)
    worksheet.set_remove_splits(True)

    # Set cell format/styles for data types
    styleDefault = xlwt.XFStyle()

    styleDate = xlwt.XFStyle()
    styleDate.num_format_str = 'YYYY-MM-DD'

    styleTime = xlwt.XFStyle()
    styleTime.num_format_str = 'h:mm'

    styleDateTime = xlwt.XFStyle()
    styleDateTime.num_format_str = 'YYYY-MM-DD h:mm'

    styleInt = xlwt.XFStyle()
    styleInt.num_format_str = '0'

    field_names = [i.name for i in fields]
    # Loop through input records

    with arcpy.da.SearchCursor(in_table, field_names) as cursor:
        row_index = 1
        for row in cursor:
            for col_index, value in enumerate(row):

                #if (fields[col_index].domain_desc or fields[col_index].subtype_desc):
                    #value = fields[col_index].updateValue(row, field_names)

                if isinstance(value, datetime.datetime):
                    if (value.hour == 0) and (value.minute == 0):
                        style = styleDate
                    elif (value.year == 1899) and (value.month == 12) and (value.day == 30):
                        style = styleTime
                        value = (value-datetime.datetime(1899, 12,30,0,0,0)).total_seconds()/86400.0
                    else:
                        style = styleDateTime

                elif isinstance(value, int):
                    style = styleInt

                else:
                    style = styleDefault

                # write to the cell
                worksheet.write(row_index, col_index, value, style)
            row_index+=1

    workbook.save(output)

def set_fc(targetTable):
    """ set correct FC based on user input """
    if targetTable == 'Assignments':
        fc = 'Assignments'
        fList = ['Assignments.OBJECTID', 'Assignments.Assignment_Number','Assignments.Display', 'Assignments.Period', 'Assignments.Status','Assignments.Team_Name',\
        'Assignments.Description', 'Assignments.Transportation', 'Assignments.Personal_Equipment','Assignments.Team_Equipment', 'Assignments.Comm_Instructions', 'Assignments.DeBrief_Location']

    elif targetTable == 'Teams':
        fc = 'Teams'
        fList = ['OBJECTID','Team_Name', 'Team_Type', 'Status', 'Leader', 'Description', 'Radio_Call_Sign']

    elif targetTable == 'Team Members':
        fc = 'Team_Members'
        fList = ['OBJECTID', 'Name', 'isLeader', 'Role', 'InService', 'Check_In', 'Check_Out', 'Team_Name', 'Originating_Team', 'Skills', 'Body_Weight', 'Gear_Weight']

    elif targetTable == 'Operational Periods':
        fc = "Operation_Periods"
        fList = ['OBJECTID','Period', 'Start_Date', 'End_Date', 'Weather', 'Incident_Name', 'Incident_Commander', 'Planning_Chief','Operations_Chief', 'Logistics_Chief', \
        'Air_Operations_Chief', 'Transportation_Chief', 'Safety_Message', 'Primary_Comms', 'Emergency_Comms']

    elif targetTable == 'Subject Information':
        fc = "PLS_Subject_Information"
        fList = ['OBJECTID','Display', 'Date', 'Victim_Number', 'Name', 'Incident_Name', 'Description', 'Gender', 'Age', 'Height, Weight', 'Hair_Color', 'Clothing', 'Other']

    # Return field objects rather than strings
    listFields = arcpy.ListFields(fc)
    fields = []
    for field in listFields:
        if field.name in fList:
            fields.append(field)

    return fc, fields

if __name__ == "__main__":
    targetTable = arcpy.GetParameterAsText(0)
    targetFile = arcpy.GetParameterAsText(1)

    fc, fields = set_fc(targetTable)
    table_to_excel(fc,targetFile,fields)