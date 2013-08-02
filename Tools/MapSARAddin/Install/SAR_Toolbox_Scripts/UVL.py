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

def updateValueLists(launched):
    """ UpdateValueLists populates all db domains with data. pass launched = 'script' or 'tool' to change error message delivery """
    try:
        import arcpy, pythonaddins
        # Set enviroment
        from arcpy import env
        workspace = arcpy.env.workspace

        # Define FC's
        Search_Segments = workspace+"\\Search_Segments"
        Teams = workspace+"\\Teams"
        Operation_Period = workspace+"\\Incident\\Operation_Period"
        Incident = workspace+"\\Incident\\Incident"
        PLS = workspace+"\\Incident\\PLS"
        Clues_Point = workspace+"\\Resources_Clues_Routes\\Clues_Point"
        Assignments = workspace+"\\Assignments"
        fc = ''
        errorString = ''

        # Process: Table To Domain
        fc = 'Segments'
        arcpy.TableToDomain_management(Search_Segments, "Area_Name", "Area_Name", workspace, "Areas", "Areas", "REPLACE")

        fc = 'Teams'
        arcpy.TableToDomain_management(Teams, "Team_Name", "Team_Name", workspace, "Teams", "Teams", "REPLACE")

        fc = 'Operational Periods'
        arcpy.TableToDomain_management(Operation_Period, "Period", "PeriodText", workspace, "Period", "PeriodText", "REPLACE")

        fc = 'PLS'
        arcpy.TableToDomain_management(PLS, "Victim_Number", "Name", workspace, "Victim_Number", "Victim_Number", "REPLACE")

        fc = 'Incident Information'
        arcpy.TableToDomain_management(Incident, "Incident_Name", "Incident_Name", workspace, "Incident_Name", "Incident_Name", "REPLACE")

        fc = 'Clues'
        arcpy.TableToDomain_management(Clues_Point, "Clue_Number", "Clue_NumText", workspace, "Clue_Number", "Clue_NumText", "REPLACE")

        fc = 'Assignments'
        arcpy.TableToDomain_management(Assignments, "Assignment_Number", "AssignNumText", workspace, "Assignment_Number", "AssignNumText", "REPLACE")

        if launched == 'script': arcpy.AddMessage('Values Have Been Updated')

    except:
        errors = arcpy.GetMessages(2)
        # Does not have exclusive access to the database
        if 'ERROR 000464' in errors:
            arcpy.AddError('UPDATE ERROR: There is an active editing session, editing MUST be stopped to update values')
        # Duplicate values exist
        elif 'ERROR 999999' in errors:
            a, b = getDomainErr(errors)
            if a == 'unknown':
                errorString = b
            else:
                errorString = "\nThe process failed because the field '{0}' in {1} already has a value of '{2}', all values must be unique! \n\nCorrect the entry and run again.\n".format(a,fc,b)
            if launched == 'script':
                arcpy.AddMessage(errorString)
            if launched == 'tool':
                pythonaddins.MessageBox(errorString,'ERROR in {0}'.format(fc),0)