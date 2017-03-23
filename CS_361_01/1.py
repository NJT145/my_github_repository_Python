import sys

print sys.path
print "-------------------------------------------------------------------------"
sys.path.append("./my_package")
print sys.path
"""
print "-------------------"
import my_package
print type(my_package.my_file) ## AttributeError: 'module' object has no attribute 'my_file'
print "-------------------"
"""
import my_package.my_file
#print type(my_package._init_)  ## AttributeError: 'module' object has no attribute '_init_'
print type(my_package.my_file)
#print type(my_package.my_module)  ## AttributeError: 'module' object has no attribute 'my_module'
#print "-------------------"
import my_package.my_module
print type(my_package.my_module)
