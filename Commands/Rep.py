from Objects.MBR import MBR
from Utils.load import *

def rep(path):
    print('Ejecutando el comando REP')
    mrb = MBR()

    file = open(path, "rb+")

    Fread_displacement(file, 0, mrb)
    print("=====Leyendo MBR======")
    mrb.display_info()
    file.close()
    print("=====Finalizando REP======")