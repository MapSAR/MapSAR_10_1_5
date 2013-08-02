# Import A FC from a csv file
# Options for Update, Append and Overwrite
# Jon Pedder - MapSAR
# Updated 6/25/13 @ 2:00pm
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

import arcpy, csv, datetime, sys, string

from arcpy import env

# 0. File to import - File
# 1. Table to import to - string value list
# 2. Operation - string value list
sourceFile = arcpy.GetParameterAsText(0)
targetTable = arcpy.GetParameterAsText(1)
operation = arcpy.GetParameterAsText(2)
inputTimeFormat = arcpy.GetParameterAsText(3)

def f_assignments(op):
    f = open(sourceFile,'rb')
    inputreader = csv.DictReader(f, dialect='excel')
    # iterate list of dictionaries and convert all keys to uppercase
    reader = [{k.upper(): v for k, v in r.iteritems()} for r in inputreader]

    if op == "UPDATE":
        for row in reader:
            eAssignment = row['ASSIGNMENTS.ASSIGNMENT_NUMBER']
            ePeriod = row['ASSIGNMENTS.PERIOD']
            eStatus = row['ASSIGNMENTS.STATUS']
            eTeam = row['ASSIGNMENTS.TEAM_NAME']
            eDescription = row['ASSIGNMENTS.DESCRIPTION']
            eTransportation = row['ASSIGNMENTS.TRANSPORTATION']
            eEquipment = row['ASSIGNMENTS.PERSONAL_EQUIPMENT']
            eTEquipment = row['ASSIGNMENTS.TEAM_EQUIPMENT']
            eRadio = row['ASSIGNMENTS.COMM_INSTRUCTIONS']
            eDebrief = row['ASSIGNMENTS.DEBRIEF_LOCATION']

            arcpy.AddMessage('Processing Assignment # '+ eAssignment +" "+eTeam)

           # Select FC "Excel_Importer", in Hidden Layers. This layer has no joins so easier to work with
            fc1="Excel_Importer"

            # Query each assignment number from import to Assignments FC for a match
            query = '"Assignment_Number" = ' + str(eAssignment)
            iAssignment = arcpy.UpdateCursor(fc1,query)

            # Initialize i var, then loop through the selcted assignment and write values to each FC field

            i = None

            for i in iAssignment:
                if ePeriod <> "NULL":
                    i.Period = int(ePeriod)
                i.Status  = eStatus
                i.Team_Name  = eTeam
                i.Description = eDescription
                i.Transportation = eTransportation
                i.Personal_Equipment = eEquipment
                i.Team_Equipment = eTEquipment
                i.Comm_Instructions = eRadio
                i.Debrief_location = eDebrief

                # Write the eVar to FC row
                iAssignment.updateRow(i)

        del row
        del f

def f_teams(op):
    f = open(sourceFile,'rb')
    inputreader = csv.DictReader(f, dialect='excel')
    # iterate list of dictionaries and convert all keys to uppercase
    reader = [{k.upper(): v for k, v in r.iteritems()} for r in inputreader]

    if op == "UPDATE":

        for row in reader:
            eTeamName = row["TEAM_NAME"]
            eTeamType = row["TEAM_TYPE"]
            eTeamStatus = row["STATUS"]
            eTeamLeader = row["LEADER"]
            eTeamDescription = row["DESCRIPTION"]
            eTeamRadio = row["RADIO_CALL_SIGN"]

            arcpy.AddMessage('Processing Team # '+ eTeamName)

           # Select FC "Teams"
            fc="Teams"

            # Query each assignment number from import to Assignments FC for a match
            iField = arcpy.AddFieldDelimiters(fc, "Team_Name")
            iQuery = "%s = '%s'" % (iField, eTeamName)
            iTeam = arcpy.UpdateCursor(fc,iQuery)

            # Initialize i var, then loop through the selcted assignment and write values to each FC field

            i = None

            for i in iTeam:
                i.Team_Type  = eTeamType
                i.Status  = eTeamStatus
                i.Leader = eTeamLeader
                i.Description = eTeamDescription
                i.Radio_Call_Sign = eTeamRadio

                # Write the eVar to FC row
                iTeam.updateRow(i)

        del row, i
    elif op == "APPEND" or op == "OVERWRITE ALL":
        # Select FC "Teams"
        fc="Teams"
        iTeams = arcpy.InsertCursor(fc)

        if op == "OVERWRITE ALL":
            arcpy.AddMessage("Deleting all records from Teams")
            arcpy.DeleteRows_management(fc)

        # Read in each row in the CSV file
        for row in reader:
            eTeamName = row["TEAM_NAME"]
            eTeamType = row["TEAM_TYPE"]
            eTeamStatus = row["STATUS"]
            eTeamLeader = row["LEADER"]
            eTeamDescription = row["DESCRIPTION"]
            eTeamRadio = row["RADIO_CALL_SIGN"]

            arcpy.AddMessage("Processing "+eTeamName)
            # Write values to fields using insert cursor
            row = iTeams.newRow()
            row.Team_Name  = eTeamName
            row.Team_Type  = eTeamType
            row.Status  = eTeamStatus
            row.Leader = eTeamLeader
            row.Description = eTeamDescription
            row.Radio_Call_Sign = eTeamRadio
            iTeams.insertRow(row)

        del reader, row, iTeams

def read_members():
    """ Read in fields from members.csv file """
    f = open(sourceFile,'rb')
    inputreader = csv.DictReader(f, dialect='excel')
    # iterate list of dictionaries and convert all keys to uppercase
    reader = [{k.upper(): v for k, v in r.iteritems()} for r in inputreader]

    # Parse Date/Time format
    keyVal = [x.strip() for x in inputTimeFormat.split('-')]
    timeDict ={'0':'%m/%d/%Y %H:%M','1':'%m/%d/%Y %I:%M%p','2':'%m/%d/%Y %I:%M %p','3':'%m/%d/%y %H:%M', '4':'%m/%d/%y %I:%M%p', '5':'%m/%d/%y %I:%M %p'}

    membersDict={}
    for row in reader:
        try:
            eID = int(row["OBJECTID"])
            eName = row["NAME"]
            if "NULL".upper() or None in row["ISLEADER"]:
                eLeader = int(0)
            else:
                eLeader = int(row["ISLEADER"])

            eRole = row["ROLE"]

            eInService = row["INSERVICE"]
            # Set Boolean field values
            if eInService == "TRUE":
                eInService  = 1
            if eInService == "FALSE":
                eInService  = 0
            if eInService == "NULL":
                eInService  = 0

            if row["CHECK_IN"] != "NULL":
                if row["CHECK_IN"] != None:
                    if row["CHECK_IN"] != "":
                        eCheck_In = datetime.datetime.strptime(row["CHECK_IN"],timeDict[keyVal[0]])
            else:
                eCheck_In = None

            if row["CHECK_OUT"] != "NULL":
                if row["CHECK_OUT"] != None:
                    if row["CHECK_OUT"] != "":
                        eCheck_Out = datetime.datetime.strptime(row["CHECK_OUT"],timeDict[keyVal[0]])
            else:
                eCheck_Out = None

            eTeam_Name = row["TEAM_NAME"]
            eOriginating_Team = row["ORIGINATING_TEAM"]
            eSkills = row["SKILLS"]
            eBody_Weight = row["BODY_WEIGHT"]
            eGear_Weight = row["GEAR_WEIGHT"]

            # Set int values from strings if there are values greater than nothing
            if eBody_Weight != "NULL":
                eBody_Weight = int(eBody_Weight)
            if eGear_Weight != "NULL":
                eGear_Weight = int(eGear_Weight)
            if eBody_Weight != "NULL" and eGear_Weight <> "NULL":
                eTotal_Weight = eBody_Weight+eBody_Weight

            arcpy.AddMessage("Reading Team Member {0}".format(eName))
            membersDict[eID] = [eName,eLeader,eRole,eInService,eCheck_In,eCheck_Out,eTeam_Name,eOriginating_Team,eSkills,eBody_Weight,eGear_Weight,eTotal_Weight]
        except:
            arcpy.AddWarning(arcpy.GetMessages(2))

        for k in membersDict.keys():
            for i in membersDict[k]:
                if i == 'NULL':
                    zapNull = membersDict[k].index(i)
                    membersDict[k][zapNull]=''

    del reader, inputreader,f

    return(membersDict)

def f_members(op):
    """ Import team members from csv file """

    fc="Team_Members"
    membersDict = read_members()

    if op == "UPDATE":
        rows = arcpy.UpdateCursor(fc)

        for row in rows:
            ID = row.OBJECTID

            if membersDict.has_key(ID):
                try:
                    arcpy.AddMessage("Updating team member {0}".format(membersDict[ID][0]))

                    row.Name  = membersDict[ID][0]
                    row.isLeader = membersDict[ID][1]
                    row.Role = membersDict[ID][2]
                    row.InService = membersDict[ID][3]
                    row.Check_In = membersDict[ID][4]
                    row.Check_Out = membersDict[ID][5]
                    row.Team_Name = membersDict[ID][6]
                    row.Originating_Team = membersDict[ID][7]
                    row.Skills = membersDict[ID][8]
                    row.Body_Weight = membersDict[ID][9]
                    row.Gear_Weight = membersDict[ID][10]
                    row.Total_Weight = membersDict[ID][11]
                except:
                    arcpy.AddWarning(arcpy.GetMessages(2))

            rows.updateRow(row)

        del rows

    elif op == "APPEND" or op == "OVERWRITE ALL":

        if op == "OVERWRITE ALL":
            arcpy.AddMessage("Deleting all records from Team Members")
            arcpy.DeleteRows_management(fc)

        rows = arcpy.InsertCursor(fc)

        # Read in each row in the CSV file
        for memberKey in membersDict.iterkeys():

            arcpy.AddMessage("Adding team member {0}".format(membersDict[memberKey]))

            row = rows.newRow()
            # Write values to fields using insert cursor
            row.Name  = membersDict[memberKey][0]
            row.isLeader = membersDict[memberKey][1]
            row.Role = membersDict[memberKey][2]
            row.InService = membersDict[memberKey][3]
            row.Check_In = membersDict[memberKey][4]
            row.Check_Out = membersDict[memberKey][5]
            row.Team_Name = membersDict[memberKey][6]
            row.Originating_Team = membersDict[memberKey][7]
            row.Skills = membersDict[memberKey][8]
            row.Body_Weight = membersDict[memberKey][9]
            row.Gear_Weight = membersDict[memberKey][10]
            row.Total_Weight = membersDict[memberKey][11]

            # Insert row
            rows.insertRow(row)

        del row, rows

def f_subject(op):
    f = open(sourceFile,'rb')
    inputreader = csv.DictReader(f, dialect='excel')
    # iterate list of dictionaries and convert all keys to uppercase
    reader = [{k.upper(): v for k, v in r.iteritems()} for r in inputreader]

    if op == "UPDATE":
        for row in reader:
            eDate = row["DATE"]
            eSubject = row["VICTIM_NUMBER"]
            eName = row["NAME"]
            eIncidentName = row["INCIDENT_NAME"]
            eDescription = row["DESCRIPTION"]
            eGender = row["GENDER"]
            eAge = row["AGE"]
            eHeight = row["HEIGHT"]
            eHair = row["HAIR_COLOR"]
            eClothing = row["CLOTHING"]
            eOther = row["OTHER"]

            arcpy.AddMessage('Processing Subject '+ eName)

           # Select FC "PLS_Subject_Information"
            fc="PLS_Subject_Information"

            # Query each subject number from import to FC for a match
            # iField = arcpy.AddFieldDelimiters(fc, "Victim_Number")
            # iQuery = "%s = '%s'" % (iField, eSubject)
            iQuery = '"Victim_Number" = ' + str(eSubject)
            iSubject = arcpy.UpdateCursor(fc,iQuery)

            # Initialize i var, then loop through the selcted assignment and write values to each FC field

            i = None

            for i in iSubject:

                # Need to write date / time parser
                # i.Date  = eDate

                i.Name = eName
                i.Incident_Name = eIncidentName
                i.Description = eDescription
                i.Gender = eGender
                i.Age = eAge
                i.Height = eHeight
                i.Hair_Color = eHair
                i.Clothing = eClothing
                i.Other = eOther

                # Write the eVar to FC row
                iSubject.updateRow(i)

        del row, i

def f_periods(op):
    f = open(sourceFile,'rb')
    inputreader = csv.DictReader(f, dialect='excel')
    # iterate list of dictionaries and convert all keys to uppercase
    reader = [{k.upper(): v for k, v in r.iteritems()} for r in inputreader]

    if op == "UPDATE":
        for row in reader:
            ePeriod = row["PERIOD"]
            eStart_Date = row["START_DATE"]
            eEnd_Date = row["END_DATE"]
            eWeather = row["WEATHER"]
            eIncident_Name = row["INCIDENT_NAME"]
            eCommander = row["INCIDENT_COMMANDER"]
            ePlanning_Chief = row["PLANNING_CHIEF"]
            eOperations_Chief = row["OPERATIONS_CHIEF"]
            eLogistics_Chief = row["LOGISTICS_CHIEF"]
            eAir_Ops_Chief = row["AIR_OPERATIONS_CHIEF"]
            eTransportation_Chief = row["TRANSPORTATION_CHIEF"]
            eSafety = row["SAFETY_MESSAGE"]
            ePrimary_Coms = row["PRIMARY_COMMS"]
            eEmergency_Coms = row["EMERGENCY_COMMS"]

            arcpy.AddMessage('Processing Operational Period '+ ePeriod)

           # Select FC "Operation_Period"
            fc="Operation_Period"

            # Query each Op period number from import to Operational period FC for a match
            iQuery = '"PERIOD" = ' + str(ePeriod)
            iPeriod = arcpy.UpdateCursor(fc,iQuery)

            # Initialize i var, then loop through the selected periods and write values to each FC field

            i = None

            for i in iPeriod:
                if ePeriod <> "NULL":
                    i.Period  = int(ePeriod)
                    i.PeriodText = ePeriod
                i.Start_Date = datetime.datetime.strptime(eStart_Date, inputTimeFormat)
                i.End_Date = datetime.datetime.strptime(eEndDate, inputTimeFormat)
                i.Weather = eWeather
                i.Incident_Name = eIncident_Name
                i.Incident_Commander = eIncident_Commander
                i.Planning_Chief = ePlanning_Chief
                i.Operations_Chief = eOperations_Chief
                i.Logistics_Chief = eLogistics_Chief
                i.Air_Operations_Chief = eAir_Ops_Chief
                i.Transportation_Chief = eTransportation_Chief
                i.Safety_Message = eSafety
                i.Primary_Comms = ePrimary_Coms
                i.Emergency_Comms = eEmergency_Coms

                # Write the eVar to FC row
                iPeriod.updateRow(i)

        del row, i
    elif op == "APPEND" or op == "OVERWRITE ALL":
        # Select FC "Operation_Period"
        fc="Operation_Period"

        if op == "OVERWRITE ALL":
            arcpy.AddMessage("Deleting all records from Operation Periods")
            arcpy.DeleteRows_management(fc)

        iPeriod = arcpy.InsertCursor(fc)

        # Read in each row in the CSV file
        for row in reader:
            ePeriod = row["PERIOD"]
            eStart_Date = row["START_DATE"]
            eEnd_Date = row["END_DATE"]
            eWeather = row["WEATHER"]
            eIncident_Name = row["INCIDENT_NAME"]
            eCommander = row["INCIDENT_COMMANDER"]
            ePlanning_Chief = row["PLANNING_CHIEF"]
            eOperations_Chief = row["OPERATIONS_CHIEF"]
            eLogistics_Chief = row["LOGISTICS_CHIEF"]
            eAir_Ops_Chief = row["AIR_OPERATIONS_CHIEF"]
            eTransportation_Chief = row["TRANSPORTATION_CHIEF"]
            eSafety = row["SAFETY_MESSAGE"]
            ePrimary_Coms = row["PRIMARY_COMMS"]
            eEmergency_Coms = row["EMERGENCY_COMMS"]

            arcpy.AddMessage('Processing Operational Period '+ ePeriod)

            # Write values to fields using insert cursor
            row = iPeriod.newRow()

            if ePeriod <> "NULL":
                row.Period  = int(ePeriod)
                row.PeriodText = ePeriod
            row.Start_Date = datetime.datetime.strptime(eStart_Date, inputTimeFormat)
            row.End_Date = datetime.datetime.strptime(eEnd_Date, inputTimeFormat)
            row.Weather = eWeather
            row.Incident_Name = eIncident_Name
            row.Incident_Commander = eCommander
            row.Planning_Chief = ePlanning_Chief
            row.Operations_Chief = eOperations_Chief
            row.Logistics_Chief = eLogistics_Chief
            row.Air_Operations_Chief = eAir_Ops_Chief
            row.Transportation_Chief = eTransportation_Chief
            row.Safety_Message = eSafety
            row.Primary_Comms = ePrimary_Coms
            row.Emergency_Comms = eEmergency_Coms

            # Insert row
            iPeriod.insertRow(row)

        del reader, row, iPeriod

# Main clause which triggers import function for each feature class.
# Select which FC will be imported and assign the fields to selectTable list
if targetTable == 'Assignments':
    arcpy.AddMessage("Called Assignments import")
    f_assignments(operation)

elif targetTable == 'Teams':
    arcpy.AddMessage("Called Teams import")
    f_teams(operation)

elif targetTable == 'Team Members':
    f_members(operation)

elif targetTable == 'Operational Periods':
    fc = "Operation_Periods"
    f_periods(operation)

elif targetTable == 'Subject Information':
    fc = "PLS_Subject_Information"
    f_subject(operation)

else:
    # If nothing matched drop out
    Arcpy.Message("There is a problem with your selection")
    fc = ""
    fields = []


