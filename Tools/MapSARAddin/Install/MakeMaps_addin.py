#-------------------------------------------------------------------------------
# Name:        MapSARAddin
# Purpose:     Script to control actions fo buttons and menus
#
# Author:      Jon Pedder
#
# Created:     3/13/2013
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
import pythonaddins
import arcpy, os, sys
# assure modules are in the python path
currentfolder = os.path.dirname(__file__)
sys.path.append(currentfolder)
sys.path.append(currentfolder+'\SAR_Toolbox_Scripts')
sys.path.append(currentfolder+'\SAR_Maintenance_Scripts')
sys.path.append(currentfolder+'\SAR_Analysis_Scripts')

import MapSARfunctions as mapsar

SAR_toolbox = "SAR_Toolbox"
SAR_Maintenance = "SAR_Maintenance"
SAR_Analysis = "SAR_Analysis"

SAR_toolboxPath = os.path.join(os.path.dirname(__file__), SAR_toolbox + ".tbx")
SAR_MaintenancePath = os.path.join(os.path.dirname(__file__), SAR_Maintenance + ".tbx")
SAR_AnalysisPath = os.path.join(os.path.dirname(__file__), SAR_Analysis + ".tbx")

class Assignment_Auto_Text_button(object):
    """Implementation for MakeMaps_addin.button_Assignment_Auto_Text_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mapsar.toggleAssignment()

class Assignment_Auto_Text_menu(object):
    """Implementation for MakeMaps_addin.menu_Assignment_Auto_Text (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mapsar.toggleAssignment()

class Clear_Database_Data(object):
    """Implementation for MakeMaps_addin.button_Clear_Database_Data (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_MaintenancePath, 'ClearData')

class Combine_Raster_Files_Button(object):
    """Implementation for MakeMaps_addin.Combine_Raster_Files_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_AnalysisPath, 'Mosaic')

class Create_MapSAR_New_button(object):
    """Implementation for Maintenance_addin.button_Create_MapSAR_New_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_MaintenancePath, 'CreateMapSARfiles')

class Enter_UTM_Button(object):
    """Implementation for MakeMaps_addin.button_Enter_UTM_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'CreatePoint')

class Exporter_button(object):
    """Implementation for MakeMaps_addin.button_Exporter_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'ExcelExport')

class Exporter_menu(object):
    """Implementation for MakeMaps_addin.menu_Exporter (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'ExcelExport')

class Importer_button(object):
    """Implementation for MakeMaps_addin.button_Importer_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'ExcelImport')

class Importer_menu(object):
    """Implementation for MakeMaps_addin.menu_Importer (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'ExcelImport')

class Incident_Information_Button(object):
    """Implementation for MakeMaps_addin.button_Incident_Information_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'IncidentInformation')

class Make_Assignment_Maps_button(object):
    """Implementation for MakeMaps_addin.button_Make_Assignment_Maps_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeAssignmentMaps')

class Make_Assignment_Maps_menu(object):
    """Implementation for MakeMaps_addin.menu_Make_Assignment_Maps (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeAssignmentMaps')

class Make_Map_button(object):
    """Implementation for MakeMaps_addin.button_Make_Map_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeMap')

class Make_Map_menu(object):
    """Implementation for MakeMaps_addin.menu_Make_Map (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeMap')

class Make_Multiscale_Map_Button(object):
    """Implementation for MakeMaps_addin.button_Make_Multiscale_Map_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeMultiScaleMap')

class Make_Task_Forms_buton(object):
    """Implementation for MakeMaps_addin.button_Make_Task_Forms_buton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeAssignmentTaskForms')

class Make_Task_Forms_menu(object):
    """Implementation for MakeMaps_addin.menu_Make_Task_Forms (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'MakeAssignmentTaskForms')

class Multi_Ring_Buffer_button(object):
    """Implementation for MakeMaps_addin.button_Multi_Ring_Buffer_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_AnalysisPath, 'MultipleRingBuffer')

class Period_auto_calc_Button(object):
    """Implementation for MakeMaps_addin.button_Period_auto_calc_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mapsar.togglePeriods()

class Period_auto_calc_menu(object):
    """Implementation for MakeMaps_addin.button_Period_auto_calc_menu (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mapsar.togglePeriods()

class Populate_Base_Data_button(object):
    """Implementation for MakeMaps_addin.button_Populate_Base_Data_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'PopulateBaseData')

class Populate_Base_Data_menu(object):
    """Implementation for MakeMaps_addin.menu_Populate_Base_Data (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'PopulateBaseData')

class Process_Cell_Phone_Pings_Button(object):
    """Implementation for MakeMaps_addin.Process_Cell_Phone_Pings_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_AnalysisPath, 'CellPingAnalysis')

class Project_Raster_File_Button(object):
    """Implementation for MakeMaps_addin.MakeMaps_addin_Project_Raster_File_Button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_AnalysisPath, 'ProjectRaster')

class Set_Spatial_Reference_button(object):
    """Implementation for Maintenance_addin.button_Set_Spatial_Reference_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_MaintenancePath, 'SetSpatialReference')

class UpdateValueLists(object):
    """Implementation for MakeMaps_addin.Extension_UVL (Extension)"""
    def __init__(self):
        self.enabled = True
    def onStopEditing(self, save_changes):
        mapsar.updateValueLists('tool')

class Update_Value_Lists_button(object):
    """Implementation for MakeMaps_addin.button_Update_Value_Lists_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'UpdateValueLists')

class Update_Value_Lists_menu(object):
    """Implementation for MakeMaps_addin.menu_Update_Value_Lists (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(SAR_toolboxPath, 'UpdateValueLists')
