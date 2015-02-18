// Function to export the data in the front-most 1D profile as tab-delimited text. This text file can be
// as a script file. This has the extension .s - a DM script
// file, but it is in fact identical to a plain text (.txt) file. To import the tabbed text file (.s) into
// Excel, simply open the saved file in Excel and accept all the default import prompts.
// This first column is x and the second y.

// Version 3 adds a batch export function and the option to export x axis values in calibrated units or pixels

// D. R. G. Mitchell, adminnospam@dmscripting.com (remove the nospam to make this work)
// version:201117, v3.1, Nov. 2013, www.dmscripting.com

// Update in v3.1: Fixed a bug whereby profiles created from the same image
// would end up with the same file name when saved and each would therefore overwrite
// the previous saved file.


// Pass in a 1D profile image to create a tab delimited text file thereof in a script window.
// Then save the script window as a .s (script) file

// Profile is the spectrum passed in for export; calibratedexport is a boolean which dictates whether the
// the x axis values are exported as calibrated units (1) or simply as the pixel values (0)

documentwindow ExportasTabbedData(image profile, number calibratedexport)
	{
		// Get some info on the passed in image
		
		string imgname=getname(profile)
		number scale, origin, xsize, ysize
		string units
		profile.imagegetdimensioncalibration(0, origin,scale,units,1)
		getsize(profile, xsize, ysize)
		
		
		// create a text window to output the data
		
		documentwindow textoutputwindow
		textoutputwindow=NewScriptWindow(imgname+" (tabbed text)", 84,202, 726, 740)
				
				
		// Loop through all the x axis pixels extracting the data and writing it to the text window
		
		number i
		for(i=0; i<xsize; i++)
			{
				number yval=getpixel(profile, i,0)	
				number xval
				if(calibratedexport==1)xval=(i-origin)*scale
				else xval=i
				editorwindowaddtext(textoutputwindow,format(xval,"%8.4f")+"\t"+format(yval, "%8.4f")+"\n")
			}
				
				
		// Return the textoutputwindow
				
		return textoutputwindow				
	}


// A function to show all the hidden images. As the above script works through the open images it hides them
// before moving onto the next. This funciton restores them.

void showallhiddenimages()
	{
		// variables

		number nodocs,shown, hidden, imgdocid, counter
		number i
		imagedocument imgdoc


		// count the number of image documents - this includes both shown and hidden ones
		// and delete any temporary tag information which may have been left over from last time.
		
		shown=Countdocumentwindowsoftype(5) // images currently shown
		nodocs=countimagedocuments() // all image documents, including hidden ones
		hidden=nodocs-shown // the number of hidden images
		
		deletepersistentnote("Show Hidden Temp")


		// Image documents are indexed (0,1,2 . . . ) in the following manner
		// Front-most shown image (0) then the image shown behind that (1) etc.
		// Hidden images appear at the end of the stacking sequence. The last image in the sequence is the last
		// image to be hidden. In the Window menu, hidden images have a 'h' next to them. 
		// Hidden images have indexes which run top to bottom in this menu. If there are only 3 image documents
		// open and all three are hidden, then the top one in the 'Window' menu will have an index of 0
		// next down 1, and the last will have an index of 2. If there are four image documents open, one is shown
		// and three are hidden, the hidden image documents are indexed 1,2 and 3 ie
		
		// Shown images
		// Front most - index = 0
		// behind front - index = 1
		// rear most - index = n = number of shown imagedocuments-1
		
		// Hidden images
		// First to be hidden - index n+1
		// Last to be hidden - index number of imagedocuments-1

		// Get the IDs of the hidden image documents
		
		for(i=shown; i<nodocs; i++)
			{
				imgdoc=getimagedocument(i)
				imgdocid=imgdoc.imagedocumentgetid()
				setpersistentnumbernote("Show Hidden Temp:Image "+counter,imgdocid)
				counter=counter+1
			}

		// loop to display all the hidden image documents in a stacked sequence. 
		
		number j

		for(j=hidden-1; j>-1; j--) // loop through the number of hidden image documents
			{
				getpersistentnumbernote("Show Hidden Temp:Image "+j,imgdocid)
				imgdoc=getimagedocumentbyid(imgdocid)
				imagedocumentshow(imgdoc)
			}


		// Remove the temporary tags

		deletepersistentnote("Show Hidden Temp")
	}
	


// Main program


// Count the number of image documents shown

number nodocs=countdocumentwindowsoftype(5)

if(nodocs<1)
	{
		showalert("Ensure a 1D profile or spectrum is front-most.",2)
		exit(0)
	}


// Export all the open spectra or just the front most
	
number exportnumber=0
if(twobuttondialog("Export all open spectra, or just the front-most spectrum, as tabbed text?","All","Front"))
exportnumber=nodocs
else exportnumber=1
	

// Export in calibrated units or pixels
	
number calibratedexport=0
if(twobuttondialog("Export x values in calibrated units or in pixels?","Units","Pixels"))
calibratedexport=1


// Select the save location

string path
if(!saveasdialog("Select the location to save the exported file(s) . . .","Do not change me", path)) exit(0)
string directory=pathextractdirectory(path, 0)

	
// Loop through the open images only processing those which have a y dimension of 1 (1D profile)

number i, counter
for(i=0; i<exportnumber;i++)
	{
		image front:=getfrontimage()
		number xsize, ysize
		getsize(front,xsize, ysize)

		if(ysize==1) // It is a 1D profile
			{
				string imgname=getname(front)
				imgname=imgname+" profile "+i
				string fullpath=pathconcatenate(directory, imgname)


				// Export the profile as tabbed text and display the result

				documentwindow profiledata=ExportasTabbedData(front, calibratedexport)
				editorwindowsavetofile(profiledata,fullpath)
				windowclose(profiledata,0)
				counter=counter+1
			}
			
		hideimage(front)
	}

showallhiddenimages()
showalert(""+counter+" spectra saved to : "+directory,2)