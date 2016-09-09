''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-03-29 by Will Bowman. This script is used to digitize data plotted
 in images, like those printed in papers
 
close all windows from the taskbar (right click, close windows) after saving
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
    frame.pack( fill = BOTH, expand = 1 )

    #adding the image
    File = tk.filedialog.askopenfilename( parent = root, initialdir = "C:/", title = 'Choose an image.' )
    img = PhotoImage( file = File )
    canvas.create_image( 0, 0, image = img )
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    global calibration_list
    try:
        calibration_list
    except:
        calibration_list = {
            'xmin-unit': 0, 'xmax-unit': 0, 'ymin-unit': 0, 'ymax-unit': 0,
            'xmin-coord': 0, 'ymax-coord': 0, 'xmax-coord': 0, 'ymin-coord': 0
        }
        
    def calibrated( x = None, y = None ):
        global calibration_list
        del_unit_x = calibration_list[ 'xmax-unit' ] - calibration_list[ 'xmin-unit' ]
        del_pix_x = calibration_list[ 'xmax-coord' ] - calibration_list[ 'xmin-coord' ]
        del_unit_y = calibration_list[ 'ymax-unit' ] - calibration_list[ 'ymin-unit' ]
        del_pix_y = calibration_list[ 'ymax-coord' ] - calibration_list[ 'ymin-coord' ]
        unit_per_pix_x = del_unit_x / del_pix_x
        unit_per_pix_y = del_unit_y / del_pix_y
        
        if x == None and y == None:
            pass
            
        elif x == None and not y == None:
            pix_from_min_pix_y = y - calibration_list[ 'ymin-coord' ]
            calibrated_unit_y = "{0:.2f}".format( calibration_list[ 'ymin-unit' ] + pix_from_min_pix_y * unit_per_pix_y )
            # print( y, calibrated_unit_y )
            return calibrated_unit_y
            
        elif y == None and not x == None:
            pix_from_min_pix_x = x - calibration_list[ 'xmin-coord' ]
            calibrated_unit_x = "{0:.2f}".format( calibration_list[ 'xmin-unit' ] + pix_from_min_pix_x * unit_per_pix_x )
            return calibrated_unit_x
            
        else:
            pix_from_min_pix_y = y - calibration_list[ 'ymin-coord' ]
            calibrated_unit_y = "{0:.2f}".format( calibration_list[ 'ymin-unit' ] + pix_from_min_pix_y * unit_per_pix_y )
            pix_from_min_pix_x = x - calibration_list[ 'xmin-coord' ]
            calibrated_unit_x = "{0:.2f}".format( calibration_list[ 'xmin-unit' ] + pix_from_min_pix_x * unit_per_pix_x )
            return calibrated_unit_x, calibrated_unit_y
            
            
        
    def print_coordinates( event ):
        #output x and y coordinate integers to console
        print( event.x, event.y )
        
    def return_plot_data_coordinates( event ):
        global curve_coordinates
        curve_coordinates[ event.x, 1 ] = event.y
        print ( event.x, event.y, 'plot' )
        print ( calibrated( event.x, event.y ), 'calibrated plot' )
    
    def quit():
        global root
        root.quit()
    
    global curve_coordinates
    curve_coordinates = [ 0, 0 ]   
         
    global plot_image_curves
    def clear_stored_data():
        global plot_image_curves
        plot_image_curves = []
    
    clear_stored_data()
    
    def new_curve():
        curve_name = tk.simpledialog.askstring( 'New curve', 'Name:' )
        global curve_coordinates, plot_image_curves
        curve_coordinates[ 1 ] = curve_name
            
        for i in np.arange( calibration_list[ 'xmax-coord' ] ):
            curve_coordinates = np.vstack(( curve_coordinates, [ i+1, np.nan ] ))
        
        if np.size( plot_image_curves ) > 0: # check if this is not first curve
            pass
        else:
            plot_image_curves = curve_coordinates[ :, 0 ]
            plot_image_curves[ 0 ] = 'x (units)'
            
        canvas.bind( "<Button 1>", return_plot_data_coordinates )
        print( 'Click points along the curve to store the pixel coordinates.\n' )
    
    def store_curve_data():
        global plot_image_curves, curve_coordinates
        if np.size( plot_image_curves ) > 0:
            plot_image_curves = np.vstack(( plot_image_curves.T, curve_coordinates[ :, 1 ].T )).T
            print( 'Stored ' + str( curve_coordinates[ 0, 1 ] ) + ' curve data.\n' )
            curve_coordinates = [ '', '' ]
        else:
            print( 'No curve exists' )
            pass
    
    def save_all_as_txt():
        global plot_image_curves
        # apply calibration
        headers = plot_image_curves[ 0, : ]
        raw_coordinates = np.delete( plot_image_curves, (0), axis = 0 )
        raw_coordinates_floats = raw_coordinates.astype( np.float )
        curves_calibrated_units = raw_coordinates.astype( np.float )
        for row in np.arange( np.size( raw_coordinates_floats, 0 ) ): # rows
            for col in np.arange( np.size( raw_coordinates_floats, 1 ) ): # columns
                if col == 0: # first column: x-axis values
                    curves_calibrated_units[ row, col ] = calibrated( x = raw_coordinates_floats[ row, col ] )
                else: # other columns: y-axis values
                    curves_calibrated_units[ row, col ] = calibrated( y = raw_coordinates_floats[ row, col ] )
        # curves_calibrated_units[ np.isnan( curves_calibrated_units ) ] = 0

        save_name = tk.filedialog.asksaveasfile( mode = 'w', defaultextension = '.txt' )
        if save_name is None:
            return
        np.savetxt( save_name.name, curves_calibrated_units, header = '\t'.join( headers ), newline = '\n', delimiter = '\t', fmt = '%10.3e' )
        print( save_name.name )
        
        
    def calibrate(): # DRY this
        calibrate_root = tk.Tk()
        calibrate_root.title( "Calibrate plot" )
        global blank_calibration_list
        
        Label( calibrate_root, text = "x-min (units) - " + str( calibration_list[ 'xmin-unit' ] ) ).grid( row = 0 )
        Label( calibrate_root, text = "x-max (units) - " + str( calibration_list[ 'xmax-unit' ] ) ).grid( row = 1 )
        Label( calibrate_root, text = "y-min (units) - " + str( calibration_list[ 'ymin-unit' ] ) ).grid( row = 2 )
        Label( calibrate_root, text = "y-max (units) - " + str( calibration_list[ 'ymax-unit' ] ) ).grid( row = 3 )
        Label( calibrate_root, text = "x-min (coords) - " + str( calibration_list[ 'xmin-coord' ] ) ).grid( row = 4 )
        Label( calibrate_root, text = "y-max (coords) - " + str( calibration_list[ 'ymax-coord' ] ) ).grid( row = 5 )
        Label( calibrate_root, text = "x-max (coords) - " + str( calibration_list[ 'xmax-coord' ] ) ).grid( row = 6 )
        Label( calibrate_root, text = "y-min (coords) - " + str( calibration_list[ 'ymin-coord' ] ) ).grid( row = 7 )
        
        e0 = Entry( calibrate_root )
        e0.grid( row = 0, column = 1 )
        e1 = Entry( calibrate_root )
        e1.grid( row = 1, column = 1 )
        e2 = Entry( calibrate_root )
        e2.grid( row = 2, column = 1 )
        e3 = Entry( calibrate_root )
        e3.grid( row = 3, column = 1 )
        e4 = Entry( calibrate_root )
        e4.grid( row = 4, column = 1 )
        e5 = Entry( calibrate_root )
        e5.grid( row = 5, column = 1 )
        e6 = Entry( calibrate_root )
        e6.grid( row = 6, column = 1 )
        e7 = Entry( calibrate_root )
        e7.grid( row = 7, column = 1 )
        
        def save_calibration():
            global calibration_list
            try:
                calibration_list[ 'xmin-unit' ] = float( e0.get() )
                calibration_list[ 'xmax-unit' ] = float( e1.get() )
                calibration_list[ 'ymin-unit' ] = float( e2.get() )
                calibration_list[ 'ymax-unit' ] = float( e3.get() )
                calibration_list[ 'xmin-coord' ] = float( e4.get() )
                calibration_list[ 'ymax-coord' ] = float( e5.get() )
                calibration_list[ 'xmax-coord' ] = float( e6.get() )
                calibration_list[ 'ymin-coord' ] = float( e7.get() )
                print( "Stored calibrations:\n" )
                print( calibration_list )
            except ValueError:
                print( "ValueError: could not convert string to float." )
        
        b1 = Button( calibrate_root, text = 'Save calibration', command = save_calibration )
        b1.grid( row = 8, column = 0 )
        b2 = Button( calibrate_root, text = 'Cancel', command = calibrate_root.destroy )
        b2.grid( row = 8, column = 1 )
        b2 = Button( calibrate_root, text = 'Quit', command = calibrate_root.destroy )
        b2.grid( row = 8, column = 2 )
        
        calibrate_root.mainloop()
        
    #mouseclick event
    canvas.bind( "<Button 1>", print_coordinates )
    
    # button to close the tk window     
    tk.Button( root, text = "New curve", command = new_curve ).pack( side = LEFT )
    tk.Button( root, text = "Store curve data", command = store_curve_data ).pack( side = LEFT )
    tk.Button( root, text = "Save all as .txt", command = save_all_as_txt ).pack( side = LEFT )
    tk.Button( root, text = "Calibrate", command = calibrate ).pack( side = LEFT ) 
    tk.Button( root, text = "Clear stored data", command = clear_stored_data ).pack( side = RIGHT ) 
    tk.Button( root, text = "Quit", command = root.destroy ).pack( side = RIGHT )  

    root.mainloop()

    
''' ########################### REFERENCES ########################### '''