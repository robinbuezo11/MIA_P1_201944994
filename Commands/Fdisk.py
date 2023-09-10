import struct
from Utils.Fmanager import *
from Objects.Partition import Partition
from Objects.MBR import MBR

def fdisk(path, size, unit, name, type, fit, delete, add):
    printConsole('Ejecutando el comando FDISK')
    print("***** Abriendo Disco *****")

    try:
        file = open(path, "rb+")
    except Exception as e:
        printError(f"Error al abrir el disco: {e}")
        return False
    
    mbr = MBR()

    print("\n***** Leyendo MBR *****")
    mbr = Fread_displacement(file, 0, mbr)
    
    if mbr:
        mbr.display_info()
    else:
        printError("No se pudo leer el MBR")
        return False
    
    # Here we have to check wich operation we are going to do
    # if delete, add or create
    if delete:
        if printWarning(f"¿Seguro que desea eliminar la partición {name}? (s/n)"):
            print("\n***** Eliminando PARTICIÓN *****")
            try:
                found = False
                for partition in mbr.partitions:
                    if partition.part_name == name:
                        partition.display_info()
                        partition = Partition()
                        found = True
                        break
                if not found:
                    printError(f"No se encontro la partición {name}")
                    return False
                
                print("\n***** Escribiendo MBR *****")
                if Fwrite_displacement(file, 0, mbr):
                    printSuccess("Se escribio el MBR correctamente")
                else:
                    printError("No se pudo escribir el MBR")
                    return False
                
                file.close()
            except Exception as e:
                printError(f"{e}")
                return False
            
            printSuccess("Se elimino la partición correctamente\n")
            printConsole("Finalizando FDISK\n")
            return True
        else:
            printConsole("Cancelando FDISK\n")
            return False
    elif add:
        # Here we add the code to add or delete space from a partition
        pass
    else:
        # Here we create a new partition
        cursor = struct.calcsize(mbr.get_const())

        print("\n***** Buscando Espacio *****")
        for i in range(4):
            part = Fread_displacement(file, cursor, Partition())
            if part.part_type != b'\0':
                cursor += struct.calcsize(part.get_const())
            else:
                break

        if unit == 'm':
            size = size * 1024
        elif unit == 'b':
            size = size / 1024

        print("\n***** Creando PARTICIÓN *****")

        part = Partition()
        part.set_info('y','p','w', cursor, size, name)
        part.display_info()

        print("\n***** Escribiendo PARTICIÓN *****")
        if Fwrite_displacement(file, cursor, part):
            printSuccess("Se escribio la partición correctamente\n")
        else:
            printError("No se pudo escribir la partición")

        try:
            file.close()
        except Exception as e:
            printError(f"{e}")
            return False

        printConsole("Finalizando FDISK\n")