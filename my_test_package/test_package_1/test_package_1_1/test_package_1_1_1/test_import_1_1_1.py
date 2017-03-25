## import test of test_module_1_1_1.py from same directory
#import test_module_1_1_1
#print("-------------------")

## import test of test111 class from test_module_1_1_1.py in same directory
#from test_module_1_1_1 import test111
#test111().testFunc()
#print("-------------------")

## import test of test_module_1_1_2.py from test_package_1_1_2
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from test_package_1_1_2.test_module_1_1_2 import test112
test112().testFunc()



def importSomething(parentDirName, moduleToImport, somethingInsideModule):
    if __name__ == '__main__':
        if __package__ is None:
            import sys
            from os import path
            sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
            from parentDirName.moduleToImport import test111
        else:
            from ..parentDirName.moduleToImport import somethingInsideModule

