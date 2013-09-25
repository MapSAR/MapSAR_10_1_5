########################################################################
# Jon Pedder
# MapSAR - 2/20/13
# Export assignments to Adobe FDF files. Use with ICS Form 204 template
#
# Original script and FDF file concept, credit to Don Ferguson
# modified for MapSAR by Jon Pedder
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
########################################################################

import arcpy, datetime
import MapSARfunctions as mapsar

# Set enviroment
from arcpy import env

def readPeriods(Period):
    """ # loops through operation periods and reads values into vars based on Op number pVar for Period
    # pList = [0] Weather, [1] Incident_Commander, [2] Planning_Chief, [3] Operations_Chief, [4] Logistics_Chief,
    [5] Air_Ops_Chief, [6] Safety_Message, [7] Primary_Comms, [8] Emergency_Comms, [9] Start_Date """
    if Period:
        iField = arcpy.AddFieldDelimiters("Operation_Period", "Period")
        iQuery = "{0} = {1}".format(iField, Period)
        rowPeriod = arcpy.SearchCursor("Operation_Period", iQuery)
        pList = []
        x = None
        for p in rowPeriod:
            pList = [p.Weather, p.Incident_Commander, p.Planning_Chief, p.Operations_Chief, \
                     p.Logistics_Chief, p.Air_Operations_Chief, p.Safety_Message, p.Primary_Comms, p.Emergency_Comms, p.Start_Date]
        return(pList)

def readTeams(Team):
    """     # loops through Teams and reads values into vars based on Team name tList for Team
    # tList = [0] Team_Type, [1] radio_Call_Sign """
    if Team:
        iField = arcpy.AddFieldDelimiters("Teams", "Team_Name")
        iQuery = "{0} = '{1}'".format(iField, Team)
        rowTeam = arcpy.SearchCursor("Teams", iQuery)
        tList = []
        t = None
        for t in rowTeam:
            tList = [t.Team_Type, t.radio_Call_Sign]
        return(tList)

def readTeamMembers(Team):
    """ Loop through team members FC reads in the field values to
    # mDict is a dictionary using role as the Key and the mList tuple for field values
    # mList Fields read: [0] Name, [1] Role, [2] Team_Name, [3] Originating_Team, [4] Skills, [5] Total_Weight """
    if Team:
        fcTM = "Team_Members"
        qTeam = "{0} = '{1}'".format(arcpy.AddFieldDelimiters(fcTM,"Team_Name"),Team)
        members = arcpy.SearchCursor(fcTM,qTeam)

        memNum = 0
        vRole = ""
        mList = []
        mDict = {}

        for m in members:
            if m.isLeader == 1:
                vRole = "Team Leader"
            else:
                memNum += 1
                vRole = "{0}.{1}".format("Team Member",memNum)
            mList = [m.Name, m.Role, m.Team_Name, m.Originating_Team, m.Skills, m.Total_Weight]
            mDict[vRole] = mList;
        return(mDict)

def readIncident():
    """ Reads information from the Incident_Information FC """
    # Pull data from Incident_Information FC
    iRows = arcpy.SearchCursor("Incident_Information")
    # iList = [0] Incident_Name
    iList = []
    for i in iRows:
        iList.append(i.Incident_Name)
    return(iList)

def clearNulls(myList):
    """ Pass in list parameter, clears out NULL values in list items """
        # Determine item type
    for i in range(len(myList)):
        myType = type(myList[i])
        if myType is str or myType is unicode:
            if 'NULL' in myList[i]:
                myList[i] = ''

        elif myType is int or myType is float or myType is long:
            if not myList[i] > 0:
                myList[i] = None
    return(myList)

def assignmentExport(output, aSelection, aRows):
    for row in aRows:
        # Clean out list and dict for each iteration
        aList = []
        iList = []
        pList = []
        tList = []
        mDict = {}

        # Assignments: aList [0] Assignment_Number, [1] Description, [2] Mileage, [3] Status, [4] Period, [5] Team_Name, [6] Transportation, [7] Personal_Equipment, [8] Team_Equipment
        # [9] Comm_Instructions, [10] DeBrief_Location

        aList = [row.getValue("Assignments.Assignment_Number"), row.getValue("Assignments.Description"), row.getValue("Assignments.Mileage"), \
                row.getValue("Assignments.Status"), row.getValue("Assignments.Period"), row.getValue("Assignments.Team_Name"), \
                row.getValue("Assignments.Transportation"), row.getValue("Assignments.Personal_Equipment"), row.getValue("Assignments.Team_Equipment"), \
                row.getValue("Assignments.Comm_Instructions"), row.getValue("Assignments.DeBrief_Location")]

        iList = readIncident()
        pList = readPeriods(aList[4])
        tList = readTeams(aList[5])
        mDict = readTeamMembers(aList[5])


        # Get current date and time from system
        now = datetime.datetime.now()
        todaydate = now.strftime("%m-%d-%Y")
        todaytime = now.strftime("%H.%M %p")

        # CREATE FDF File, Adobe format that requires an PDF file template.

        # Tuples containing data, iList = Incident, aList = Assignment, tList = Teams, pList = Periods
        # iList =   [0] Incident_Name
        # aList     [0] Assignment_Number, [1] Description, [2] Mileage, [3] Status, [4] Period, [5] Team_Name,
        #           [6] Transportation, [7] Personal_Equipment, [8] Team_Equipment
        #           [9] Comm_Instructions, [10] DeBrief_Location
        # tList =   [0] Team_Type, [1] radio_Call_Sign
        # pList =   [0] Weather, [1] Incident_Commander, [2] Planning_Chief, [3] Operations_Chief, [4] Logistics_Chief,
        #           [5] Air_Ops_Chief, [6] Safety_Message, [7] Primary_Comms, [8] Emergency_Comms, [9] Start_Date

        filename = "{0}\Assignment_Task_{1}_.fdf".format(output, str(aList[0]))
        arcpy.AddMessage("Creating Task Form for Assignment {0} : {1} ".format(str(aList[0]),filename))

        # Open new FDF file
        txt = open (filename, "w")
        txt.write("%FDF-1.2\n")
        txt.write("%????\n")
        txt.write("1 0 obj<</FDF<</F(Task_Assignment_Template.pdf)/Fields 2 0 R>>>>\n")
        txt.write("endobj\n")
        txt.write("2 0 obj[\n")
        txt.write ("\n")

        if iList:
            iList = clearNulls(iList)
            txt.write("<</T(IncidentName)/V({0})>>\n".format(iList[0]))
        if pList:
            pList = clearNulls(pList)
            txt.write("<</T(Weather)/V({0})>>\n".format(pList[0]))
            txt.write("<</T(IC)/V({0})>>\n".format(pList[1]))
            txt.write("<</T(PreparedBy)/V({0})>>\n".format(pList[2]))
            txt.write("<</T(Operations)/V({0})>>\n".format(pList[3]))
            txt.write("<</T(Logistics)/V({0})>>\n".format(pList[4]))
            txt.write("<</T(AirOps)/V({0})>>\n".format(pList[5]))
            txt.write("<</T(SafetyMessage)/V({0})>>\n".format(pList[6]))
            txt.write("<</T(PrimaryComs)/V({0})>>\n".format(pList[7]))
            txt.write("<</T(EmergencyComs)/V({0})>>\n".format(pList[8]))
            txt.write("<</T(StartDate)/V({0})>>\n".format(pList[9]))
        if aList:
            aList = clearNulls(aList)
            txt.write("<</T(AssignmentNum)/V({0})>>\n".format(aList[0]))
            txt.write("<</T(AssignDescription)/V({0})>>\n".format(aList[1]))
            txt.write("<</T(AssignMileage)/V({0})>>\n".format(aList[2]))
            txt.write("<</T(AssignStatus)/V({0})>>\n".format(aList[3]))
            txt.write("<</T(AssignPeriod)/V({0})>>\n".format(aList[4]))
            txt.write("<</T(AssignTeam)/V({0})>>\n".format(aList[5]))
            txt.write("<</T(AssignTransportation)/V({0})>>\n".format(aList[6]))
            txt.write("<</T(AssignPersonalEquipment)/V({0})>>\n".format(aList[7]))
            txt.write("<</T(AssignTeamEquipment)/V({0})>>\n".format(aList[8]))
            txt.write("<</T(AssignComInstructions)/V({0})>>\n".format(aList[9]))
            txt.write("<</T(Assignlocation)/V({0})>>\n".format(aList[10]))
        if tList:
            tList = clearNulls(tList)
            txt.write("<</T(TeamType)/V({0})>>\n".format(tList[0]))
            txt.write("<</T(TeamCallSign)/V({0})>>\n".format(tList[1]))

        # Loop through each team member in mDict and write the the field and value value
        # Fields read: [0] Name, [1] Role, [2] Team_Name, [3] Originating_Team, [4] Skills, [5] Total_Weight
        if mDict:
            for k, v in mDict.iteritems():

                v = clearNulls(v)
                txt.write("<</T({0}.name)/V({1})>>\n".format(k,v[0]))
                if v[1] != None:
                    txt.write("<</T({0}.roll)/V({1})>>\n".format(k,v[1]))

                txt.write("<</T({0}.team)/V({1})>>\n".format(k,v[2]))
                txt.write("<</T({0}.origteam)/V({1})>>\n".format(k,v[3]))
                if v[5] > 0:
                    txt.write("<</T({0}.skillsandweight)/V({1} - weight = {2})>>\n".format(k,v[4],v[5]))
                elif v[5] == None:
                    txt.write("<</T({0}.skillsandweight)/V({1})>>\n".format(k,v[4]))

        txt.write("<</T(PrepDate)/V({0})>>\n".format(todaydate))
        txt.write("<</T(PrepTime)/V({0})>>\n".format(todaytime))

        # Close and write FDF file
        txt.write("]\n")
        txt.write("endobj\n")
        txt.write("trailer\n")
        txt.write("<</Root 1 0 R>>\n")
        txt.write("%%EO\n")
        txt.close ()


if __name__ == '__main__':
    # Parameters
    # 0. Folder to store FDF files - string
    # 1. Select ALL or SELECTION of assignments - string
    # 2. or 1-5 or 10-15 assignment range definition, must use a dash. - string
    PDFlocation = arcpy.GetParameterAsText(0)
    aSelection = arcpy.GetParameterAsText(1)
    Printpages = arcpy.GetParameterAsText(2)
    arcpy.AddMessage(Printpages)
    if Printpages != '':
        PageRange = mapsar.getPrintRange(Printpages)

    fc = "Assignments"

    # Print the Task assignments
    # Check the selection parameter aSelection, process either the SELECTION or ALL assignments
    if aSelection == "SELECTION":
        arcpy.AddMessage("Assignments Selected are  " + str(sorted(PageRange)))
        for p in sorted(PageRange):
            iQuery = 'Assignments.Assignment_Number = {0}'.format(p)
            arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION",iQuery)
            aRows = arcpy.SearchCursor(fc)
            assignmentExport(PDFlocation, aSelection, aRows)

    if aSelection == "ALL":
        arcpy.SelectLayerByAttribute_management (fc, "CLEAR_SELECTION")
        PageRange = [row[0] for row in arcpy.da.SearchCursor(fc, ("Assignments.Assignment_Number"))]
        arcpy.AddMessage("Assignments Selected are  " + str(sorted(PageRange)))
        for p in sorted(PageRange):
            iQuery = 'Assignments.Assignment_Number = {0}'.format(p)
            arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION",iQuery)
            aRows = arcpy.SearchCursor(fc)
            assignmentExport(PDFlocation, aSelection, aRows)

    # Clear the selection and refresh the active view
    arcpy.SelectLayerByAttribute_management("Assignments", "CLEAR_SELECTION")
    arcpy.RefreshActiveView()

