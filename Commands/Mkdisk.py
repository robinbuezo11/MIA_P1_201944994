from Objects.MBR import MBR
from datetime import datetime
from Utils.load import *

def mkdisk():
    print('Ejecutando el comando MKDISK')
    print("=====Creando MBR======")
    mbr = MBR()
    mbr.set_info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mbr.display_info()

    file_name = f'941Disco{mbr.mbr_dsk_signature}.adsj'
    print("=====Creando Disco======")
    if Fcreate_file(file_name): exit()

    file = open(file_name, "rb+")

    print("=====Aplicando Tamaño======")
    Winit_size(file, mbr.mbr_tamano)


    print("=====Writing MBR======")
    Fwrite_displacement(file, 0, mbr)
    file.close()
    print("=====Finalizando MKDISK======")

    return file_name