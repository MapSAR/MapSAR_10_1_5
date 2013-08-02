# Export A FC to a csv file
# Jon Pedder - MapSAR
#
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

import arcpy, csv
from arcpy import env
workspace = arcpy.env.workspace

# 0. destination Folder - Folder
# 1. From value list, select table - String
# 2. Destination file name - string
# 3. Overwrite file option - boolean
targetfolder = arcpy.GetParameterAsText(0)
selectTable = arcpy.GetParameterAsText(1)
targetfile = arcpy.GetParameterAsText(2)
overwrite = arcpy.GetParameterAsText(3)

# Set overwrite option to true, default is false
arcpy.env.overwriteOutput = False
if overwrite == "true":
    arcpy.env.overwriteOutput = True

# Build filename
filename = targetfolder+"/"+targetfile

# Select which FC will be exported and assign the fields to selectTable list
if selectTable == 'Assignments':
    fc = "Assignments"
    fields = ['Assignments.Assignment_Number','Assignments.Period','Assignments.Status','Assignments.Team_Name', "Assignments.Description", 'Assignments.Transportation', 'Assignments.Personal_Equipment','Assignments.Team_Equipment','Assignments.Comm_Instructions','Assignments.Debrief_location']
elif selectTable == 'Teams':
    fc = "Teams"
    fields = ["Team_Name","Team_Type","Status","Leader","Description","Radio_Call_Sign"]
elif selectTable == 'Team Members':
    fc = "Team_Members"
    # membersDict[eID] = [eName,eLeader,eRole,eInService,eCheck_In,eCheck_Out,eTeam_Name,eOriginating_Team,eSkills,eBody_Weight,eGear_Weight]
    fields = ["OBJECTID","Name","isLeader","Role","InService","Check_in","Check_Out","Team_Name","Originating_Team","Skills","Body_Weight","Gear_Weight"]
elif selectTable == 'Operational Periods':
    fc = "Operation_Periods"
    fields = ["Period", "Start_Date","End_Date","Weather","Incident_Name","Incident_Commander","Planning_Chief","Operations_Chief","Logistics_Chief","Air_Operations_Chief","Transportation_Chief","Safety_Message","Primary_Comms","Emergency_Comms"]
elif selectTable == 'Subject Information':
    fc = "PLS_Subject_Information"
    fields = ["Date","Victim_Number","Name","Incident_Name","Description","Gender","Age","Height","Weight","Hair_Color","Clothing","Other"]
elif selectTable == 'Reporting Party Information':
    fc = "RP"
    fields = ["Date_Time","Name","Cell_Phone","Land_Line","email","Relationship","Notes"]
else:
    # If nothing matched drop out
    Arcpy.Message("There is a problem with your selection")
    fc = ""
    fields = []


# Process: Export Feature Attribute to ASCII...
rows = arcpy.SearchCursor(fc)
arcpy.ExportXYv_stats(fc,fields, "COMMA", filename, "ADD_FIELD_NAMES")

