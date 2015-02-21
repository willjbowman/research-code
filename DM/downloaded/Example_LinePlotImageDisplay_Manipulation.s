// Example script to show the implementation of commands to work
// with line plots.

// D. R. G. Mitchell, adminnospam@dmscripting.com (remove the nospam)
// version:20111123, v1.0, November 2011


// create two intensity profiles (two sine waves with an offset
// between them

okdialog("Displaying an intensity profile")

image sine=realimage("",4,360,1)
sine=sin(icol/(90/pi()))

// display the first image

showimage(sine)
setwindowposition(sine, 142,24)
setname(sine, "A sine wave")
updateimage(sine)


// Now turning on the legend and setting the name

okdialog("Now turning on the ledend display and setting the name to 'Sine'")

// Get the image display of the first profile
// Note lineplotimagedisplay is a subset of imagedisplay
// The imagedisplay object (imgdisp in this script) works with both imagedisplay commands
// and lineplotimagedisplaycommands.

imagedisplay imgdisp=sine.imagegetimagedisplay(0)


// Turn on the legend and name the slice 'Sine'

imgdisp.lineplotimagedisplaysetlegendshown(1)
object sliceid=imgdisp.imagedisplaygetsliceidbyindex(0)
imgdisp.imagedisplaysetslicelabelbyid(sliceid, "Sine")



// Add a cursor and position it at the first minmum

okdialog("Adding a cursor and positioning it")
imgdisp.lineplotimagedisplaysetcursorstate(sliceid, 90, 1) // 30 is the cursor channel position and 1 is on



// now add a second intensity profile
okdialog("Adding a second intensity profile")

// Create the second intensity profile

image sine2=imageclone(sine)
sine2=sin((180/pi())+(icol/(90/pi())))

// Add the second profile to it

imgdisp.imagedisplayaddimage(sine2, "Sine 2")



// Change the colour of the added slice - note the first slice is index 0, the 2nd is index 1 etc

okdialog("Changing the colours.")

imgdisp.lineplotimagedisplaysetslicecomponentcolor(1,0,0,0,1) 
// 1=2nd slice, 0=component number =line, 0,0,1= RGB (blue)


// Change the colour of the fill (component=1) to red
imgdisp.lineplotimagedisplaysetslicecomponentcolor(0,1,1,0,0) 
// 1=2nd slice, 0=component number =line, 1,0,0= RGB (red)


// Change the fill of the first plot from fill to line

okdialog("Changing the first plot from fill to line") // (0=no plot, 1=line, 2=fill)
imgdisp.lineplotimagedisplaysetslicedrawingstyle(sliceid,1)
imgdisp.lineplotimagedisplaysetslicecomponentcolor(1,0,1,0,0) //
// in the above expression (1st number is slice index 0=1st, 1=2nd etc); next number is is component 0=line, 1=fill; next three numbers are RGB (1,0,0=Red)



// Turn off the background

okdialog("Turn off the grid")
imgdisp.lineplotimagedisplaysetgridon(0)


// Delete the second plot

okdialog("Deleting the second plot")
object sliceid2=imgdisp.imagedisplaygetsliceidbyindex(1) // 1 is the index of the 2nd slice (0 is the first)
imgdisp.imagedisplaydeleteslicewithid(sliceid2)


// Calibrate the image in radians
okdialog("Adding scaling and axis labels")
number xsize, ysize
getsize(sine, xsize, ysize)

number xscaling=1/(xsize/(2*pi())) //the scale in radians per pixel
sine.setscale(xscaling,1)
sine.imagesetdimensionunitstring(0,"Angle / radians")
sine.imagesetintensityunitstring("Arbitrary Intensity")


// Add a region of interest

okdialog("Adding a region of interest")
roi temproi=createroi()
temproi.roisetrange(180,270) // these are the channel numbers - left and right
imgdisp.imagedisplayaddroi(temproi)



// Note the examples below show how to move the plot horizontally and scale it vertically. However, this is
// done by deleting the plot, scaling the original plot data to suit and then adding this modified
// data back to the plot. This works, but there are more elegant, albeit much more complex
// ways of achievimg this - see the end of the script.


// Add the second plot back first as itself, then again but this time offset by 90 channels

okdialog("Adding a second copy with a 90 pixel offset")

imgdisp.imagedisplayaddimage(sine2, "Sine2")
imgdisp.lineplotimagedisplaysetslicecomponentcolor(1,0,0,0,1) // make the line blue
sliceid2=imgdisp.imagedisplaygetsliceidbyindex(1)
// Note this variable was defined earlier. however, the slice was subsequently deleted. When it was
// added again to the image, the sliceid will change, hence the need to re-source it.

// Add a second copy of the second profile with a 90 pixel offset
image sineoffset=exprsize(xsize, ysize)// set this to the dimension of the second plot
sineoffset=offset(sine2,-90,0) // create a copy of the sine2 image offset by 90 channels

sineoffset[0,0,1,90]=0 // makes the leading edge of the offset spectrum 0
imgdisp.imagedisplayaddimage(sineoffset, "Offset")
imgdisp.lineplotimagedisplaysetslicecomponentcolor(2,1,0,1,1) // make the line blur


// Set the displayed range to match the range of available data

okdialog("Changing the range of displayed data")
imgdisp.lineplotimagedisplaysetdisplayedchannels(90,360) // left origin set to 90 pixels, right axis limit set to 360

// Change the vertical scaling. Note if the autosurvey option in on (right click on the image and
// select imagedisplay to check this option) it will override and vertical scaling you make. So always
// turn autosurvey off before setting the vertical limits

imgdisp.lineplotimagedisplaysetdoautosurvey(0,0)// turns off autosurvey for both low and high limits
imgdisp.lineplotimagedisplaysetcontrastlimits(-2, 1.2)



// Change the vertical scaling of the second plot

okdialog("Change the vertical position of the sine2 plot")
// Delete the image
imgdisp.imagedisplaydeleteslicewithid(sliceid2)

// Scale downward by 0.5
sine2=sine2-0.5
// having 0.5 added to them

// add it back to the image

imgdisp.imagedisplayaddimage(sine2, "Sine2") // note it is now the third slice
// DM will automatically assign the above slice a colour to it must be set back to blue
sliceid2=imgdisp.imagedisplaygetsliceidbyindex(2)
imgdisp.lineplotimagedisplaysetslicecomponentcolor(2,0,0,0,1)


// Hide a plot temporarily

okdialog("Going to hide the Sine2 plot temporarily")
imgdisp.imagedisplaysetslicevisible(sliceid2,0)
updateimage(sine)
delay(90) // 1.5s delay
imgdisp.imagedisplaysetslicevisible(sliceid2,1)



// Select each of the spectra in turn
okdialog("Select each plot in turn - see the legend bar")

number i, noslices
noslices=imgdisp.imagedisplaycountslices()
for(i=0; i<noslices; i++)
	{
		object sliceid=imgdisp.imagedisplaygetsliceidbyindex(i)
		imgdisp.imagedisplaysetsliceselected(sliceid,1)
		updateimage(sine)
		delay(90)
		imgdisp.imagedisplaysetsliceselected(sliceid,0)
	}



// Add all three plots together and display the result

okdialog("Adding the three plots together")

image sumimg=sine+sine2+sineoffset
imgdisp.imagedisplayaddimage(sumimg, "Sum Image")
object sliceid3=imgdisp.imagedisplaygetsliceidbyindex(3) // fourth image we have added to the display
imgdisp.lineplotimagedisplaysetslicedrawingstyle(sliceid3, 3) //(3=fill)
imgdisp.lineplotimagedisplaysetslicecomponentcolor(3,0,0.5,.7,0)


// For an excellent demonstration on how to scale lineplot horizontally and vertically
// see Bernhard Schaffer's tutorial on the front page of the DM Script Database at:

//http://www.felmi-zfe.tugraz.at/dm_scripts/welcome.html

//scroll down to tutorials / Slices in Lineplot Display (by Bernhard Schaffer)

okdialog("For an excellent demonstration on how to scale lineplots horizontally and vertically\n"\
+"see Bernhard Schaffer's tutorial on the front page of the DM Script Database at:\n"\
+"http://www.felmi-zfe.tugraz.at/dm_scripts/welcome.html\n"\
+"scroll down to tutorials / Slices in Lineplot Display (by Bernhard Schaffer)")




