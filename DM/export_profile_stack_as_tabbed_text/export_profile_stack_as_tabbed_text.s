//// OVERVIEW ////
//// USER-DEFINED ////
//// FUNCTIONS ////
//// MAIN SCRIPT ////
//// REFERENCES ////

Image profiles := GetFrontImage() //get image containing profiles
String image_name = GetName( profiles ) //extract profile data file name
String file_name = image_name + ".txt" //create file name for output file

If ( !SaveAsDialog( "Save text file as", GetApplicationDirectory( 2, 0 ) + file_name, file_name ) )
	Exit(0)
Number output_file_ID = CreateFileForWriting( file_name ) //create output text file

Number scale, origin, x_size, y_size //get information about axes
String units //get units text string
profiles.ImageGetDimensionCalibration( 0, origin, scale, units, 1 ) //get axes' calibration data
GetSize( profiles, x_size, y_size ) //get image size data
	
Result( "\nExporting profile data to " + file_name + "\n" ) //tell user that output file is being written
//DocumentWindow result_window
//result_window = NewScriptWindow( "Result Window", 84, 202, 726, 740 )
//EditorWindowAddText( result_window, "Starting\n" )

WriteFile( output_file_ID, "Row 1 is the calibrated x-axis of profile data in " + units + "\n" )
// write first line as calibrated scale
number x_i
for( x_i = 0; x_i < x_size; x_i++) {
	WriteFile( output_file_ID, ( origin + ( scale * x_i ) ) + "\t" )
	EditorWindowAddText( result_window, "x_i = " + x_i + "\n" )
}
WriteFile( output_file_ID, "\n" ) //create new row in output file

ImageDisplay profiles_image_display = profiles.ImageGetImageDisplay( 0 )
Number i, slice_count
slice_count = profiles_image_display.ImageDisplayCountSlices()

for( i = 0; i < slice_count; i++ ) {
	Object slice_ID = profiles_image_display.ImageDisplayGetSliceIDByIndex( i )
	profiles_image_display.ImageDisplaySetSliceSelected( slice_ID, 0 ) // boolean flag sets selection
}

for( i = 0; i < slice_count; i++ ) {
	Object slice_ID = profiles_image_display.ImageDisplayGetSliceIDByIndex( 0 )
	//profiles_image_display.ImageDisplaySetSliceSelected( slice_ID, 1 ) // boolean flag sets selection
	//UpdateImage( profiles )
	//LinePlotImageDisplaySetSlice( profiles_image_display, i )
	EditorWindowAddText( result_window, "i = " + i + "\n" )
	
	Image current_profiles := GetFrontImage() //get front image in current state
	Number j //loop counter
	for( j = 0; j < x_size; j++ ) { //loop through slice's pixel values
		Number y = GetPixel( current_profiles, j, 0 ) //store each pixel value
		WriteFile( output_file_ID, y + "\t" ) //write value to output file row
		//EditorWindowAddText( result_window, "j = " + j + "," + y + "\n" )
	}
	WriteFile( output_file_ID, "\n" ) //create new line for next slice's values
	If( i < slice_count - 1 ) //don't delete slice on last iteration (image locks up w/out this, not sure why)
		profiles_image_display.ImageDisplayDeleteSliceWithId( slice_ID )
}

CloseFile( output_file_ID ) //close output file (end cpu process)
Result( "DONE\n" ) //report the end of the script execution to user
//EditorWindowAddText( result_window, "DONE" )