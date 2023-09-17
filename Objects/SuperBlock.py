import ctypes
import struct
from Utils.Utilities import coding_str
from Utils.Fmanager import *
from Objects.Inode import Inode

const = 'iiiii19s19siHiiiiiiii'

class SuperBlock(ctypes.Structure):

    _fields_ = [
        ('s_filesystem_type', ctypes.c_int),
        ('s_inodes_count', ctypes.c_int),
        ('s_blocks_count', ctypes.c_int),
        ('s_free_blocks_count', ctypes.c_int),
        ('s_free_inodes_count', ctypes.c_int),
        ('s_mtime', ctypes.c_char * 19),
        ('s_umtime', ctypes.c_char * 19),
        ('s_mnt_count', ctypes.c_int),
        ('s_magic', ctypes.c_uint16),
        ('s_inode_s', ctypes.c_int),
        ('s_block_s', ctypes.c_int),
        ('s_first_ino', ctypes.c_int),
        ('s_first_blo', ctypes.c_int),
        ('s_bm_inode_start', ctypes.c_int),
        ('s_bm_block_start', ctypes.c_int),
        ('s_inode_start', ctypes.c_int),
        ('s_block_start', ctypes.c_int)
    ]

    def __init__(self):
        self.s_magic = 0xEF53

    def get_const(self):
        return const

    def _set_s_filesystem_type(self, s_filesystem_type):
        self.s_filesystem_type = s_filesystem_type

    def _set_s_inodes_count(self, s_inodes_count):
        self.s_inodes_count = s_inodes_count

    def _set_s_blocks_count(self, s_blocks_count):
        self.s_blocks_count = s_blocks_count

    def _set_s_free_blocks_count(self, s_free_blocks_count):
        self.s_free_blocks_count = s_free_blocks_count

    def _set_s_free_inodes_count(self, s_free_inodes_count):
        self.s_free_inodes_count = s_free_inodes_count

    def _set_s_mtime(self, s_mtime):
        self.s_mtime = coding_str(s_mtime, 19)

    def _set_s_umtime(self, s_umtime):
        self.s_umtime = coding_str(s_umtime, 19)

    def _set_s_mnt_count(self, s_mnt_count):
        self.s_mnt_count = s_mnt_count

    def _set_s_magic(self, s_magic):
        self.s_magic = s_magic

    def _set_s_inode_s(self, s_inode_s):
        self.s_inode_s = s_inode_s

    def _set_s_block_s(self, s_block_s):
        self.s_block_s = s_block_s

    def _set_s_first_ino(self, s_first_ino):
        self.s_first_ino = s_first_ino

    def _set_s_first_blo(self, s_first_blo):
        self.s_first_blo = s_first_blo

    def _set_s_bm_inode_start(self, s_bm_inode_start):
        self.s_bm_inode_start = s_bm_inode_start

    def _set_s_bm_block_start(self, s_bm_block_start):
        self.s_bm_block_start = s_bm_block_start

    def _set_s_inode_start(self, s_inode_start):
        self.s_inode_start = s_inode_start

    def _set_s_block_start(self, s_block_start):
        self.s_block_start = s_block_start
 
    def set_info(self, s_filesystem_type, s_inodes_count, s_blocks_count, s_free_blocks_count, s_free_inodes_count, s_mtime, s_umtime, 
                 s_mnt_count, s_magic, s_inode_s, s_block_s, s_first_ino, s_first_blo, s_bm_inode_start, s_bm_block_start, s_inode_start, s_block_start):
        self._set_s_filesystem_type(s_filesystem_type)
        self._set_s_inodes_count(s_inodes_count)
        self._set_s_blocks_count(s_blocks_count)
        self._set_s_free_blocks_count(s_free_blocks_count)
        self._set_s_free_inodes_count(s_free_inodes_count)
        self._set_s_mtime(s_mtime)
        self._set_s_umtime(s_umtime)
        self._set_s_mnt_count(s_mnt_count)
        self._set_s_magic(s_magic)
        self._set_s_inode_s(s_inode_s)
        self._set_s_block_s(s_block_s)
        self._set_s_first_ino(s_first_ino)
        self._set_s_first_blo(s_first_blo)
        self._set_s_bm_inode_start(s_bm_inode_start)
        self._set_s_bm_block_start(s_bm_block_start)
        self._set_s_inode_start(s_inode_start)
        self._set_s_block_start(s_block_start)
    
    def display_info(self):
        print("\n*** Super Bloque ***")
        print("Tipo de Sistema de Archivos: ", self.s_filesystem_type)
        print("Cantidad de Inodos: ", self.s_inodes_count)
        print("Cantidad de Bloques: ", self.s_blocks_count)
        print("Bloques Libres: ", self.s_free_blocks_count)
        print("Inodos Libres: ", self.s_free_inodes_count)
        print("Fecha de Montaje: ", self.s_mtime.decode())
        print("Ultima Fecha de Desmontaje: ", self.s_umtime.decode())
        print("Numero de Montajes: ", self.s_mnt_count)
        print("Magic Number: ", self.s_magic)
        print("Tamaño del Inodo: ", self.s_inode_s)
        print("Tamaño del Bloque: ", self.s_block_s)
        print("Primer Inodo Libre: ", self.s_first_ino)
        print("Primer Bloque Libre: ", self.s_first_blo)
        print("Inicio del Bitmap de Inodos: ", self.s_bm_inode_start)
        print("Inicio del Bitmap de Bloques: ", self.s_bm_block_start)
        print("Inicio de la Tabla de Inodos: ", self.s_inode_start)
        print("Inicio de la Tabla de Bloques: ", self.s_block_start, "\n")

    def doSerialize(self):
        return struct.pack(
            const,
            self.s_filesystem_type,
            self.s_inodes_count,
            self.s_blocks_count,
            self.s_free_blocks_count,
            self.s_free_inodes_count,
            self.s_mtime,
            self.s_umtime,
            self.s_mnt_count,
            self.s_magic,
            self.s_inode_s,
            self.s_block_s,
            self.s_first_ino,
            self.s_first_blo,
            self.s_bm_inode_start,
            self.s_bm_block_start,
            self.s_inode_start,
            self.s_block_start
        )
    
    def doDeserialize(self, data):
        (self.s_filesystem_type,
        self.s_inodes_count,
        self.s_blocks_count,
        self.s_free_blocks_count,
        self.s_free_inodes_count,
        self.s_mtime,
        self.s_umtime,
        self.s_mnt_count,
        self.s_magic,
        self.s_inode_s,
        self.s_block_s,
        self.s_first_ino,
        self.s_first_blo,
        self.s_bm_inode_start,
        self.s_bm_block_start,
        self.s_inode_start,
        self.s_block_start) = struct.unpack(const, data)

    def generate_report_inode(self, file):
        try:
            inode = Inode()
            code = ''
            connections = ''
            for i in range(self.s_inodes_count):
                Fread_displacement(file, self.s_inode_start + i * struct.calcsize(inode.get_const()), inode)
                if inode.i_s == -1:
                    continue

                code += f'node{i} [label = <<table cellspacing="0" cellpadding="2">\n'
                code += inode.generate_report_inode(i)
                code += '</table>>];\n'

                if i == 0:
                    connections += f'node{i}'
                else:
                    connections += f'->node{i}'
            code += connections + ';\n'
            return code
        except:
            return ''