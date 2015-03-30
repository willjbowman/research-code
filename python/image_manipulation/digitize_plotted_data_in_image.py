''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-03-29 by Will Bowman. This script is used to digitize data plotted
 in images, like those printed in papers
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger


##

''' ########################### USER-DEFINED ########################### '''
# _data_path = '' # path to data file


''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# _data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

if __name__ == "__main__":

    root = tk.Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = tk.filedialog.askopenfilename( parent = root, initialdir = "C:/", title = 'Choose an image.' )
    img = PhotoImage( file = File )
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    global calibration_string, calibration_list
    calibration_string = ''
    calibration_list = []
        
    def print_coordinates( event ):
        #outputting x and y coords to console
        print ( event.x, event.y )
        # return ( event.x, event.y )
        
    def return_plot_data_coordinates( event ):
        global curve_coordinates
        curve_coordinates[ event.x, 1 ] = event.y
        print ( event.x, event.y, 'plot' )
    
    def quit():
        global root
        root.quit()
    
    global curve_coordinates
    curve_coordinates = [ '', '' ]   
         
    global plot_image_curves
    plot_image_curves = []
    
    def new_curve():
        curve_name = tk.simpledialog.askstring( 'New curve', 'Name:' )
        global curve_coordinates, plot_image_curves
        curve_coordinates[ 1 ] = curve_name
        for i in np.arange( calibration_list[ 6 ] ):
            curve_coordinates = np.vstack(( curve_coordinates, [ i+1, 0 ] ))
        
        if plot_image_curves:
            pass
        else:
            plot_image_curves = curve_coordinates[ :, 0 ]
            
        canvas.bind( "<Button 1>", return_plot_data_coordinates )
        print( 'Click points along the curve to store the pixel coordinates.\n' )
    
    def save_data():
        global plot_image_curves, curve_coordinates
        if plot_image_curves:
            plot_image_curves = np.hstack(( plot_image_curves, curve_coordinates[ :, 1 ] ))
            curve_coordinates = [ '', '' ]
        else:
            print( 'No curve exists' )
            pass
        
        
    def calibrate():
        plot_bounds_units_string = tk.simpledialog.askstring( 'Calibrate plot', 'Comma-separated plot area bounds: x-min, x-max, y-min, y-max' )
        print( plot_bounds_units_string )
        
        plot_northwest_coordinates = tk.simpledialog.askstring( 'Calibrate plot', 'Comma-separated northwest plot area coordinates: NW_x, NW_y' )
        print( plot_northwest_coordinates )
        
        plot_southest_coordinates = tk.simpledialog.askstring( 'Calibrate plot', 'Comma-separated southeast plot area coordinates: SE_x, SE_y' )
        print( plot_southest_coordinates )
        
        global calibration_string, calibration_list
        calibration_string = plot_bounds_units_string + ',' + plot_northwest_coordinates + ',' + plot_southest_coordinates
        calibration_list = [ float( x ) for x in calibration_string.split( ',' ) ]
        
    #mouseclick event
    canvas.bind( "<Button 1>", print_coordinates )
    
    # button to close the tk window 
    tk.Button( root, text = "Calibrate", command = calibrate ).pack() 
    tk.Button( root, text = "Save data", command = save_data ).pack()      
    tk.Button( root, text = "New curve", command = new_curve ).pack()
    tk.Button( root, text = "Quit", command = root.destroy ).pack()  

    root.mainloop()

    
''' ########################### REFERENCES ########################### '''