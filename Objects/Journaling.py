import ctypes
import struct
from Objects.Journal import Journal

class Journaling(ctypes.Structure):

    def __init__(self):
        self.j_journals = [Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),
                          Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),
                          Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),
                          Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),
                          Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),Journal(),]
        
    def get_const_num(self):
        return struct.calcsize(self.j_journals[0].get_const())*50

    def display_info(self):
        print("\nJournaling")
        for i in range(50):
            print("Journal", i)
            self.j_journals[i].display_info()
    
    def doSerialize(self): 
        serialize = b''
        for i in range(50):
            serialize += self.j_journals[i].doSerialize()
        return serialize

    def doDeserialize(self, data):
        sizeJournal = struct.calcsize(Journal().get_const())

        for i in range(50):
            dataJournal = data[i*sizeJournal: (i+1)*sizeJournal]
            self.j_journals[i].doDeserialize(dataJournal)
            

