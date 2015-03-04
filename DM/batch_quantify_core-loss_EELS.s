String output_file_path = "C:/Documents and Settings/p2admin/My Documents/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150217_10Ca_XRDCrushed_ARM200kV/"
String output_file_name = "t_over_lambda_raw_DM_output"

string menu = "EELS"
string submenu = "Quantification"
string item = "Log-ratio (relative)"


// loop through open images and calculate t/lamba; store file names and results in text file

number images = CountImages() // get the number of open images
number i

OpenResultsWindow()
DocumentWindow results_window = GetDocumentWindowByTitle( "Results" )
EditorWindowSetText( results_window, "" )

for( i = 0; i < images - 1; i++ ) {
	image front_image := GetFrontImage() // store image in variable
	string file_name = GetName( front_image ) // store image file name
    Result( "\n" + file_name + "\n" )
	// attempt to execute menu item function, throw exception if function doesn't exist
	// ChooseMenuItem( menu, submenu, item )
	If ( !ChooseMenuItem( menu, submenu, item ) )
    	Throw( "The menu-command " + menu + " / "+ submenu + " / " + item + "  was not found!" )
    DeleteImage( front_image ) //close front image
    // showalert( file_name + "\t" + t_over_lambda, 2 )
}

EditorWindowSaveToFile( results_window, output_file_path + output_file_name )