# ---------------------------------------------------------------------------
# Update_Value_Lists.py
# Description: Updates values in selection lists throughout MapSAR. Run this after exiting an edit session.
# 3/12/13
# Jon Pedder, MapSAR
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
# ---------------------------------------------------------------------------

# Import arcpy module
import MapSARfunctions as mapsar


# Set enviroment
from arcpy import env

mapsar.updateAAvalues()
mapsar.updateValueLists('script')

