import ctypes
import struct
from Objects.Content import Content

class FolderBlock(ctypes.Structure):

    def __init__(self):
        self.b_content = [Content(),Content(),Content(),Content()]

    def display_info(self):
        print("\nBloque de Carpeta")
        for i in range(4):
            print("Content", i)
            self.b_content[i].display_info()
    
    def doSerialize(self): 
        serialize = b''
        for i in range(4):
            serialize += self.b_content[i].doSerialize()
        return serialize

    def doDeserialize(self, data):
        sizeContent = struct.calcsize(Content().getConst())

        for i in range(4):
            dataContent = data[i*sizeContent: (i+1)*sizeContent]
            self.b_content[i].doDeserialize(dataContent)
            

