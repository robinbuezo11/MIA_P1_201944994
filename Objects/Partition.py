import ctypes
import struct
from Utils.Utilities import coding_str
from Objects.EBR import EBR
from Utils.Fmanager import *

const = 'sssii16s' 

class Partition(ctypes.Structure):

    _fields_ = [
        ('part_status', ctypes.c_char),
        ('part_type', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('part_start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('part_name', ctypes.c_char * 16)
    ]

    def __init__(self):
        self.part_status = b'\0'
        self.part_type = b'\0'
        self.part_fit = b'\0'
        self.part_start = -1
        self.part_s = -1
        self.part_name = b'\0'*16

    def get_const(self):
        return const

    def _set_part_status(self, part_status):
        self.part_status = coding_str(part_status, 1)

    def _set_part_type(self, part_type):
        self.part_type = coding_str(part_type, 1)

    def _set_part_fit(self, part_fit):
        self.part_fit = coding_str(part_fit, 1)

    def _set_part_start(self, part_start):
        self.part_start = part_start

    def _set_part_s(self, part_s):
        self.part_s = part_s

    def _set_part_name(self, part_name):
        self.part_name = coding_str(part_name, 16)
 
    def set_info(self, part_status, part_type, part_fit, part_start, part_s, part_name):
        self._set_part_status(part_status)
        self._set_part_type(part_type)
        self._set_part_fit(part_fit)
        self._set_part_start(part_start)
        self._set_part_s(part_s)
        self._set_part_name(part_name)
    
    def display_info(self):
        print("Estado: ", self.part_status.decode().upper())
        print("Tipo: ", self.part_type.decode().upper())
        print("Ajuste: ", self.part_fit.decode().upper())
        print("Inicio: ", self.part_start)
        print(f"Tamaño: {self.part_s/1024} KB")
        print("Nombre: ", self.part_name.decode().upper(), "\n")

    def doSerialize(self):
        return struct.pack(
            const,
            self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_name
        )
    
    def doDeserialize(self, data):
        self.part_status, self.part_type, self.part_fit, self.part_start, self.part_s, self.part_name = struct.unpack(const, data)

    def generate_report_mbr(self, file):
        code = '''
            <tr>
                <td bgcolor="#3371ff"<b>MBR</b></td>
            <tr>
                <td><b>part_status</b> ''' + self.part_status.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_type</b> ''' + self.part_type.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_fit</b> ''' + self.part_fit.decode().upper() + '''</td>
            </tr>
            <tr>
                <td><b>part_start</b> ''' + str(self.part_start) + '''</td>
            </tr>
            <tr>
                <td><b>part_size</b> ''' + str(self.part_s) + '''</td>
            </tr>
            <tr>
                <td><b>part_name</b> ''' + self.part_name.decode().upper() + '''</td>
            </tr>
            '''
        if self.part_type.decode() == 'e':
            ebr = EBR()
            if not Fread_displacement(file, self.part_start, ebr):
                printError(f'No se pudo leer el EBR del disco {file.name}')
                return code
            if ebr.part_s != -1:
                code += ebr.generate_report_mbr()
            while ebr.part_next != -1:
                if not Fread_displacement(file, ebr.part_next, ebr):
                    printError(f'No se pudo leer el EBR del disco {file.name}')
                    return code
                if ebr.part_s != -1:
                    code += ebr.generate_report_mbr()
        return code
    
    def generate_report_disk(self, file, size_disk):
        if self.part_type.decode() == 'e':
            ebr = EBR()
            if not Fread_displacement(file, self.part_start, ebr):
                printError(f'No se pudo leer el EBR del disco {file.name}')
                return ''
            end_used = 0
            code = '''|{Extendida|{'''
            while ebr.part_next != -1:
                if end_used != ebr.part_start-struct.calcsize(ebr.get_const()):
                    code += f'|Libre\\n{(((ebr.part_start-struct.calcsize(ebr.get_const())) - end_used)/size_disk)*100}% del disco'
                code += f'|EBR|Lógica\\n{((ebr.part_s)/size_disk)*100}% del disco'
                end_used = ebr.part_start + ebr.part_s

                if not Fread_displacement(file, ebr.part_next, ebr):
                    printError(f'No se pudo leer el EBR del disco {file.name}')
                    return ''
                
            if end_used != self.part_s:
                code += f'|Libre\\n{((self.part_s - end_used)/size_disk)*100}% del disco'
            code += '''}}'''
            return code
        else:
            code = f'|Primaria\\n{((self.part_s)/size_disk)*100}% del disco'
            return code