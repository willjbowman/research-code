//+++++++++++ OVERVIEW +++++++++++//
// AUTHOR: Will Bowman
// VERSION: 0.1
// DATE CREATED: 2015-02-23
// This script makes it easy to code in your favorite text editor outside of DM. 
// This script executes a script saved at location defined by file_name string.
// Just open this script in DM, specify the location of your script and run 
// (Ctrl+K on Windows). If you're working in a text editor outside of DM, make sure
// you save your changes before executing Execute_Script_File inside of DM.


//+++++++++++ USER-DEFINED +++++++++++//
// String file_name = "C:/path/to/my/script/file.s"
String file_name = "C:/Dropbox/Crozier Group Users - Will Bowman/active_research/codecode/DM/Export_Line_Profile_As_Tabbed_Text/Export_Line_Profile_As_Tabbed_Text.s"


//+++++++++++ FUNCTIONS +++++++++++//


//+++++++++++ MAIN SCRIPT +++++++++++//
InstallScriptLibraryFile( file_name ) // install and run script

//+++++++++++ REFERENCES +++++++++++//
//