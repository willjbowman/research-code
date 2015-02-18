// This script requires a spatially calibrated SADP which has had the centre located using the DIFFPack Auto Find Centre
// routine (or manually located by the user). It uses this centre to rotationally average the SADP, greatly improving the 
// S/N ratio on weakly exposed patterns. If it is run without the centre appropriately 
// located, the physical centre of the image will be the rotation point and smearing of the pattern
// will occur. This is a heavily modified version of script designed for averaging diffractograms released by GATAN
// D. Mitchell, drm@ansto.gov.au, Feb 2003

// By holding down the SHIFT key at launch, some instructions will be displayed in the Instructions window.

If (SHIFTdown())
{
documentwindow reswin
reswin =getresultswindow(1)
if(reswin.windowisvalid()) windowclose(reswin,0)
reswin =getresultswindow(1)
WindowSetFramePosition( reswin, 140, 480 ) 
WindowSetFrameSize( reswin, 820, 220 ) 
WindowSetTitle( reswin, "Instructions") 

result("This script takes a SADP, and rotationally averages it to yield intensity vs 1/A."+"\n")
result("It allows an estimation of intensity on otherwise spotty rings. It also allows accurate measurement of spacings."+"\n\n")
result("1 Spatially calibrate your SADP in 1/A, using the Analysis/Calibrate tool."+"\n")
result("2 Use DIFFPACK to locate the centre of the pattern. If you don't have DIFPACK or DIFPACK does not"+"\n")
result(" locate the centre correctly - estimate where the centre is - by eye - inaccurate, or by drawing a circle."+"\n")
result(" which just touches equivalent spots, then shrink the circle to its smallest to define the centre."+"\n")
result(" Position the cursor at this point and read off the position in the Image Status window."+"\n")
result(" You don't have to work with calibrated images, but you should where possible."+"\n")
result("3. Run the script. You will be asked to provide the location of the centre - if it has not already been located."+"\n")
result("4. The rotationally averaged image and the radial intensity profile are shown."+"\n\n")
result("D. Mitchell, drm@ansto.gov.au, Feb 2003.")
exit(0)
}


//***********************
// Setting up variables//
//***********************

number samples =512, k = 2 * pi() / samples
number xsize, ysize, minor, centery, centerx, xval, yval, scalex, scaley
image temp, dst, lineProj, rotAvg, originalimage
image img
string units
centerx = 0; centery = 0; xval=0; yval=0


//****************************************************************
//Acquiring the foremost image and obtaining the centre location//
//****************************************************************

img:= GetFrontImage()
GetNumberNote(img,"Diffraction Package:Center:X", centerx )
GetNumberNote(img,"Diffraction Package:Center:Y", centery)


//**************************************************************
//Checking to see if the image is calibrated and warning if not//
//*************************************************************

getscale(img,xval,yval)
units=getunitstring(img)

	if(val(units)!=1)
		{
			beep()
			if (!ContinueCancelDialog("Your image should be calibrated in 1/A."+ "\n" + "You should calibrate it first (Analyse/Calibrate)."))
		{
        Exit(0)
}
}


//********************************************************************
//Checking to see if the image centre has been located with DIFFPACK//
//********************************************************************

if (centerx < 1)
{
   if(!twobuttondialog("There is no centre defined. Do you want to:","Use DifPack","User Define"))
		{
			if (units=="") units="pixels"

			while(centerx==0)
				{
					if(!getnumber("Enter the x coordinate (in "+units+") of the pattern centre",0,centerx)) exit(0)
				}
				
			while(centery==0)
				{
					if(!getnumber("Enter the y coordinate (in "+units+") of the pattern centre",0,centery)) exit(0)
				}

		
			getscale(img,scalex, scaley)
			centerx=centerx/scalex
			centery=centery/scaley

			SetNumberNote(img,"Diffraction Package:Center:X", centerx )
			setNumberNote(img,"Diffraction Package:Center:Y", centery)
		}
	else
		{
			okdialog("Run DIFPACK to find the centre of the pattern, then rerun this script")
			exit(0)
		}
}



//*****************************************************************
//Warping the image to obtaining the linear projection of the data //
//*****************************************************************

hideimage(img)

ConvertToComplex( img )

temp := modulus( img )

GetSize( img, xsize, ysize )
minor = min( xsize, ysize )
dst := RealImage( "dst", 4, minor/2, samples )
dst = warp( temp,	icol * sin(irow * k) + centerx, \
						icol * cos(irow * k) + centery )
lineProj := RealImage( "Radial Intensity", 4, minor/2, 1 )
lineProj = 0
lineProj[icol,0] += dst; lineProj /= samples
setscale(lineproj,xval,yval)
setunitstring(lineproj,units)


//*****************************************
//Converting the SADP image back to its original form and displaying it
//****************************************

converttofloat(img)
showimage(img)
setwindowposition(img,140,24)


//*********************************************
//Displaying the radial intensity distribution //
//*********************************************

showimage(lineproj)
setwindowsize (lineproj, xsize/2, ysize/2)
setwindowposition(lineproj,660,306)
number smallx=0, smally=0
getsize(lineproj,smallx, smally)


//*****************************************************************
//Warping the image to obtaining the rotational average of the data //
//*****************************************************************

rotAvg := RealImage( "Rotational Average", 4, minor, minor )
rotavg = 0

number rotx, roty
rotAvg = warp( lineProj, iradius, 0 )
getsize(rotavg,rotx,roty)
setorigin(rotavg,rotx/2,roty/2)
setscale(rotavg,xval,yval)
setunitstring(rotavg,units)


//*****************************************
//Displaying the rotational average image //
//****************************************

showImage( rotAvg )
setwindowsize (rotavg, xsize/2, ysize/2)
setwindowposition(rotavg,660,24)








