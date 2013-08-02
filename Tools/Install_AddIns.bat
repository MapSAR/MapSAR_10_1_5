cscript msgbox.vbs "Message for 10.1" "This script will install all nesesssary MapSAR add-ins for ArcMap 10.1, click OK to continue"{cr}""{cr}" Please assure ArcMap is closed !" "1"

Set currdir=%CD%
Set workingdir=%CD%\add_ins\
Set "xlwtdir=%CD%\XL_Tools\xlwt-0.7.5"
Set "xlrddir=%CD%\XL_Tools\xlrd-0.9.2"

if exist "C:\Program Files\Common Files\ArcGIS\bin\ESRIRegAddIn.exe" set esridir="C:\Program Files\Common Files\ArcGIS\bin\ESRIRegAddIn.exe"

If exist "C:\Program Files (x86)\Common Files\ArcGIS\bin\ESRIRegAddin.exe" set esridir="C:\Program Files (x86)\Common Files\ArcGIS\bin\ESRIRegAddIn.exe"

IF %ERRORLEVEL% == 1 (

	%esridir% %workingdir%GPX.esriAddIn /s
	%esridir% %workingdir%%ConstructwithBuffer.esriAddIn /s
	%esridir% %workingdir%AttributeAssistant.esriAddIn /s
	%esridir% %workingdir%MapSARAddin.esriaddin /s
	cd %xlwtdir%
	call setup.py install
	cd %xlrddir%
	call setup.py install
	cd %currdir%
	cscript msgbox.vbs "Success" "Addins have been installed" "1"
)