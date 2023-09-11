import ctypes
import struct
import random
from Utils.Utilities import coding_str
from Objects.Partition import Partition

const = 'i19sis' 
#i es un entero de 4 bytes, 19s es un string de 19 bytes, i es un entero de 4 bytes, s es un string de 1 byte

class MBR(ctypes.Structure):

    _fields_ = [
        ('mbr_tamano', ctypes.c_int),
        ('mbr_fecha_creacion', ctypes.c_char * 19),
        ('mbr_dsk_signature', ctypes.c_int),
        ('dsk_fit', ctypes.c_char)
    ]

    def __init__(self):
        self.mbr_tamano = -1     # Tamaño del disco en KB
        self.mbr_fecha_creacion = b'\0'*19
        self.mbr_dsk_signature = -1
        self.dsk_fit = b'\0'
        self.partitions = [Partition(), Partition(), Partition(), Partition()]

    def get_const(self):
        return const

    def _set_mbr_tamano(self, mbr_tamano):
        self.mbr_tamano = mbr_tamano

    def _set_mbr_fecha_creacion(self, mbr_fecha_creacion):
        self.mbr_fecha_creacion = coding_str(mbr_fecha_creacion, 19)

    def _set_mbr_dsk_signature(self, mbr_dsk_signature):
        self.mbr_dsk_signature = mbr_dsk_signature

    def _set_dsk_fit(self, dsk_fit):
        self.dsk_fit = coding_str(dsk_fit, 1)
 
    def set_info(self, mbr_fecha_creacion, mbr_tamano, dsk_fit):
        self._set_mbr_tamano(mbr_tamano)
        self._set_mbr_fecha_creacion(mbr_fecha_creacion)
        self._set_mbr_dsk_signature(random.randint(1, 2**31 - 1))
        self._set_dsk_fit(dsk_fit)
    
    def display_info(self):
        print("\n*** MBR ***")
        print(f"Tamaño: {self.mbr_tamano/1024} KB")
        print("Fecha de creacion: ", self.mbr_fecha_creacion.decode())
        print("Identificador: ", self.mbr_dsk_signature)
        print("Ajuste: ", self.dsk_fit.decode().upper())
        print("\n* PARTICIONES *")
        for i in range(4):
            print(f'Particion {i+1}:')
            if self.partitions[i].part_type == b'\0':
                print("No hay particion\n")
            else:
                self.partitions[i].display_info()

    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature,
            self.dsk_fit
        )
        for i in range(4):
            serialize += self.partitions[i].doSerialize()
        return serialize
    
    def doDeserialize(self, data):
        sizeMBR = struct.calcsize(const)
        sizePartition = struct.calcsize(Partition().get_const())

        dataMBR = data[:sizeMBR]
        self.mbr_tamano, self.mbr_fecha_creacion, self.mbr_dsk_signature, self.dsk_fit = struct.unpack(const, dataMBR)

        for i in range(4):
            dataPartition = data[sizeMBR + i*sizePartition: sizeMBR + (i+1)*sizePartition]
            self.partitions[i].doDeserialize(dataPartition)

