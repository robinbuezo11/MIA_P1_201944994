import ctypes
import struct

const = '16i'

class PointersBlock(ctypes.Structure):
    
        _fields_ = [
            ('b_pointers', ctypes.c_int * 16)
        ]
    
        def __init__(self):
            self.b_pointers = [0]*16
    
        def getConst(self):
            return const
        
        def setInfo(self, pointers):
            self.b_pointers = pointers
    
        def display_info(self):
            print("\nBloque de Punteros")
            print("b_pointers: ", self.b_pointers, "\n")
        
        def doSerialize(self): 
            return struct.pack(
                const,
                *self.b_pointers
            )
    
        def doDeserialize(self, data):
            *self.b_pointers, = struct.unpack(const, data) 