// $BACKGROUND$
/********************************/
/*	Spectrum Images to Text		*/
/********************************/
/*							*/
/*	Takes a Spectrum Image and dumps it to a	*/
/*	tab-separated, similarly named text file.	*/
/*	Runs in background by default.			*/
/*								*/
/********************************/
/* Author: 	Mike Sarahan    	*/
/* Email: 	msarahan@superstem.org    	*/
/* Date:	19.07.2010			*/
/* Version:	1.0					*/
/********************************/
/* 					
version 1.0 (19.07.2010): first version released
*/

/********************************/
/* Main Program					*/
/********************************/
image 	current
number 	width, height, depth, fileID, origin, scale
number ctX, ctY, ctZ, tstart, tend
string	filename, units

// Exit if no images open
If (!GetFrontImage(current)) Exit(0)

// Get frontmost image
current   := getfrontimage()

tstart = GetHighResTickCount()


// Get image dimensions and energy calibration data
width  = ImageGetDimensionSize(current,0)
height = ImageGetDimensionSize(current,1)
depth  = ImageGetDimensionSize(current,2)
ImageGetDimensionCalibration(current,1, origin, scale, units, 0)

// Read voxel values to tab-separated text file
// 2D image gets flattened - each row gets stacked onto
// the end of the previous row.

filename = GetName(current)+".txt"
If (!SaveAsDialog("Save text file as", GetApplicationDirectory(2,0) + filename, filename)) Exit(0)
fileID = CreateFileForWriting(filename)

Result("\nStarting text dump of file: "+GetName(current)+"\n")
WriteFile(fileID, "Original spectrum dimensions:\n")
WriteFile(fileID, width+","+height+"\n")
WriteFile(fileID, "Spectral data (calibrated energy in first column, spectra in order thereafter):")
for (ctZ=0;ctZ<depth;ctZ++)
{
	WriteFile(fileID, "\n"+(origin+(scale*ctZ))+"\t")
	for (ctY=0;ctY<height;ctY++)
	{
		for (ctX=0;ctX<width;ctX++)
		{
		WriteFile(fileID, Sum(current[ctX,ctY,ctZ])+"\t")
		}
	}
}
CloseFile(fileID)
Result("\n\nSaved file: "+filename+"\n")
tend = GetHighResTickCount()
Result("\n Time taken: \n")
Number tres, tps
tps = GetHighResTicksPerSecond()
tres = GetHighResTickResolution()
Result(Format(CalcHighResSecondsBetween(tstart,tend)," %12.1f"))
Result(" +/- "+Format((tres/tps),"%12.1f")+" sec\n")
