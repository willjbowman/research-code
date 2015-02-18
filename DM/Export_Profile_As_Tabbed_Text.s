
// Function to export the data in the front-most 1D profile as tab-delimited text. This text file can be
// as a script file. This has the extension .s - a DM script
// file, but it is in fact identical to a plain text (.txt) file. To import the tabbed text file (.s) into
// Excel, simply open the saved file in Excel and accept all the default import prompts.
// This first column is x and the second y.

// D. R. G. Mitchell, adminnospam@dmscripting.com (remove the nospam to make this work)
// version:20130413, v2.0, April 2013, www.dmscripting.com


// Pass in a 1D profile image to create a tab delimited text file thereof in a script window.
// Then save the script window as a .s (script) file

documentwindow ExportasTabbedData(image profile)
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
				number xval=(i-origin)*scale
				editorwindowaddtext(textoutputwindow,format(xval,"%8.4f")+"\t"+format(yval, "%8.4f")+"\n")
			}
				
				
		// Return the textoutputwindow
				
		return textoutputwindow				
	}



// Main program

number nodocs=countdocumentwindowsoftype(5)
if(nodocs<1)
	{
		showalert("Ensure a 1D profile or spectrum is front-most.",2)
		exit(0)
	}
	
	
// Source the front-most image and check it is a 1D profile

image front:=getfrontimage()
number xsize, ysize
getsize(front,xsize, ysize)

if(ysize!=1)
	{
		showalert("This only works with 1D images (spectra, profiles etc).",2)
		exit(0)
	}


// Export the profile as tabbed text and display the result

documentwindow profiledata=ExportasTabbedData(front)
windowshow(profiledata)
profiledata.windowsetframeposition(138,0)
windowselect(profiledata)
string imgname=windowgettitle(profiledata)



// Save the text file

if(!saveasdialog("Save Tabbed Text Data as . . .",imgname, imgname)) exit(0)
editorwindowsavetofile(profiledata,imgname)


