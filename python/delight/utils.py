import sys

from maya.OpenMaya import *
from maya.OpenMayaMPx import *

class ArrayDataHandleIterator(object):
    def __init__(self, arrayDataHandle, output):
        self.arrayDataHandle = arrayDataHandle
        self.output = output
        self.status = MStatus.kSuccess
            
    def next(self):
        lastStatus = self.status
        try:
            self.status = self.arrayDataHandle.next()
        except:
            self.status = MStatus.kFailure

        if lastStatus == MStatus.kSuccess:
            if self.output:
                return self.arrayDataHandle.outputValue()
            else:
                return self.arrayDataHandle.inputValue()
        else:
            raise StopIteration
 
    def __iter__(self):
        return self


def getSortingIndices(unsorted):
    idxlist = [[unsorted[i], i] for i in range(0, len(unsorted))]
    idxlist.sort()
    sorted = [item[1] for item in idxlist]
    return sorted



