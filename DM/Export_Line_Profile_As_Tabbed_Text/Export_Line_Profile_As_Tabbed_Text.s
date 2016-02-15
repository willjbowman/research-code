//+++++++++++ OVERVIEW +++++++++++//
// AUTHOR: Will Bowman
// VERSION: 0.1
// DATE CREATED: 2015-02-23
// This script takes an image with multiple profiles and stores the data from 
// each in a tab delimited text file. The first row of values are calibrated 
// x-axis values and each subsequent row is a profile's values. The first entry 
// in each row is the legend label of that profile. The label of the first row
// of profile values is the image's file name (this is not ideal, but also not
// worth fixing for my use case).

// USAGE: Have 1D line profile open as front-most image. Make sure to specify
// '.txt' extension during save dialog!

// KNOWN ISSUES:
// 1. profile data are not labeled properly because they take the
//    image display's name rather than the slice's name in the legend. ( Should use String ImageDisplayGetSliceLabelById( ImageDisplay img_disp, ScriptObject slice_id ) .)
// 2. the initial profiles should be saved before conversion to .txt
// 3. the script ends with an error - press ok.
// 4. the editor window doesn't show up in the free version, so there's code here
//    to accommodate that - which is clunky and useless.

//+++++++++++ USER-DEFINED +++++++++++//
String export_start_text = "\nExporting profile data to "
String export_end_text = "Done, yay!\n"

//+++++++++++ FUNCTIONS +++++++++++//


//+++++++++++ MAIN SCRIPT +++++++++++//

Image profiles := GetFrontImage() //get image containing profiles
String image_name = GetName( profiles ) //extract profile data file name
String file_name = image_name + ".txt" //create file name for output file

If( !SaveAsDialog( "Save text file as", GetApplicationDirectory( 2, 0 ) + file_name, file_name ) )
	Exit(0)
Number output_file_ID = CreateFileForWriting( file_name ) //create output text file

Number scale, origin, x_size, y_size //get information about axes
String units //get units text string
profiles.ImageGetDimensionCalibration( 0, origin, scale, units, 1 ) //get axes' calibration data
GetSize( profiles, x_size, y_size ) //get image size data

//tell user that output file is being written
Result( export_start_text + file_name + "\n" )

// create new script window with progress messages for user (comment this out if
// you have Result window)
// DocumentWindow result_window
// result_window = NewScriptWindow( "Result Window", 84, 202, 726, 740 )
// EditorWindowAddText( result_window, export_start_text + file_name + "\n" )

// write first row as calibrated x-axis
WriteFile( output_file_ID, units + "\t" ) //write units text string in first column
Number x_i //define counter
for( x_i = 0; x_i < x_size; x_i++) {
	WriteFile( output_file_ID, ( origin + ( scale * x_i ) ) + "\t" )
	// EditorWindowAddText( result_window, "x_i = " + x_i + "\n" ) // for debugging
}

WriteFile( output_file_ID, "\n" ) //create new row in output file

// get ImageDisplay of profiles Image
ImageDisplay profiles_image_display = profiles.ImageGetImageDisplay( 0 )
Number i, slice_count // define counters
slice_count = profiles_image_display.ImageDisplayCountSlices() // count slice

for( i = 0; i < slice_count; i++ ) {
	Object slice_ID = profiles_image_display.ImageDisplayGetSliceIDByIndex( 0 )
	// EditorWindowAddText( result_window, "i = " + i + "\n" ) //for debugging
	
	Image current_profiles := GetFrontImage() //get front image (in current state)
	String current_profile_name = current_profiles.ImageGetName() //get current image name
	WriteFile( output_file_ID, current_profile_name + "\t" ) //write name in first column

	Number j // define loop counter [1]
	for( j = 0; j < x_size; j++ ) { //loop through slice's pixel values
		Number y = GetPixel( current_profiles, j, 0 ) //store each pixel value
		WriteFile( output_file_ID, y + "\t" ) //write value to output file row
		//EditorWindowAddText( result_window, "j = " + j + "," + y + "\n" ) //debug
	}
	WriteFile( output_file_ID, "\n" ) //create new line for next slice's values
	If( i < slice_count - 1 ) //don't delete slice on last iteration (image locks 
														// up w/out this, not sure why)
		// delete current slice from image so the next slice's data is available.
		profiles_image_display.ImageDisplayDeleteSliceWithId( slice_ID )
}

CloseFile( output_file_ID ) //close output file (end cpu process)
Result( export_end_text ) //report the end of the script execution to user
// EditorWindowAddText( result_window, export_end_text ) //comment out if you have results window


//+++++++++++ REFERENCES +++++++++++//
//[1] DGR Mitchell. Batch Export Spectra as Tabbed Text. http://www.dmscripting.com/batch_export_spectra_as_tabbed_text.html