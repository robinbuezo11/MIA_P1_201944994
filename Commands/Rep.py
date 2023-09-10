from Objects.MBR import MBR
from Utils.Fmanager import *
from Utils.Utilities import *

def rep(path):
    print('Ejecutando el comando REP')
    mrb = MBR()

    try:
        file = open(path, "rb+")
    except:
        printError(f'No se pudo abrir el archivo {path}')
        return

    Fread_displacement(file, 0, mrb)
    print("=====Mostrando Reporte======\n")
    mrb.display_info()
    file.close()
    print("=====Finalizando REP======")