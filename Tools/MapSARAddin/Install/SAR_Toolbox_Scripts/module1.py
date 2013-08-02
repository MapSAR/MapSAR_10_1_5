#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      SMSR
#
# Created:     14/07/2013
# Copyright:   (c) SMSR 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy
import MapSARfunctions as mapsar


def main():
    mapsar.updateAAvalues()

if __name__ == '__main__':
    main()
