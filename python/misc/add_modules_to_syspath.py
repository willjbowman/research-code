'''
Acknowledgements:
Thanks to dg99 on Stack Overflow for this solution [1].


Purpose:
Appends wills_modules directory path onto the module search path [2] variable.


Usage:

!*!*!*!*!*!*!*!*!

THIS MUST BE DONE!

Save this file in a directory that is perminently in the module search path 
(e.g. 'C:\\pyzo2013c\\lib').
Keep a copy of this file for versioning only.

!*!*!*!*!*!*!*!*!


Then by adding the below line to the top of a script, all modules in the 
wills_modules directory become accessible.

import add_modules_to_syspath

Then, for a module pytry.py in wills_modules, use this:

import pytry as pt


References:
1. http://stackoverflow.com/questions/20843088/where-to-save-my-custom-scripts-
so-that-my-python-scripts-can-access-the-module
2. https://docs.python.org/2/tutorial/modules.html#the-module-search-path
'''

import sys
# sys.path.append( "C:/Users/willb/Dropbox/WillB/Crozier_Lab/
# research_PhD/code/github/python/wills_modules" )
sys.path.append( "C:\\Users\\willb\\Dropbox\\WillB\\Crozier_Lab\\"
	"research_PhD\\code\\github\\python\\wills_modules" )