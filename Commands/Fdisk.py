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
        file.close()
        return False
    
    # Here we have to check wich operation we are going to do
    
    # If we are going to delete a partition
    if delete:
        if printWarning(f"¿Seguro que desea eliminar la partición {name.upper()}? (s/n)"):
            print("\n***** Eliminando PARTICIÓN *****")
            try:
                found = False
                for i, partition in enumerate(mbr.partitions):
                    if partition.part_name.decode() == name:
                        partition.display_info()
                        # Here we have to delete the partition from the disk
                        if Fwrite_displacement_data(file, partition.part_start, b'\0'*partition.part_s):
                            printSuccess("Se elimino la partición del disco correctamente")
                        else:
                            printError("No se pudo eliminar la partición del disco")
                            file.close()
                            return False
                        # Here we delete the partition from the MBR
                        mbr.partitions[i] = Partition()
                        printSuccess("Se elimino la partición del MBR correctamente")
                        found = True
                        break
                if not found:
                    printError(f"No se encontro la partición {name}")
                    file.close()
                    return False
                
                print("\n***** Escribiendo MBR *****")
                if Fwrite_displacement(file, 0, mbr):
                    printSuccess("Se escribio el MBR correctamente")
                else:
                    printError("No se pudo escribir el MBR")
                    file.close()
                    return False
            except Exception as e:
                printError(f"{e}")
                file.close()
                return False
            printSuccess("Se elimino la partición correctamente\n")
        else:
            printConsole("Cancelando FDISK\n")
            return False
        
    # If we are going to add space to a partition
    elif add:
        size_bytes = get_sizeB(add, unit)
        # Comprobate if the partition exists and if this have space at the end
        print("\n***** Buscando PARTICION *****")
        found = False
        setted = False
        for i in range(4):
            try:
                if mbr.partitions[i].part_name.decode() == name:
                    found = True
                    # In case that the partition is the last one and the size is positive
                    if i == 3 and size_bytes > 0:
                        if (mbr.partitions[i].part_start + mbr.partitions[i].part_s) + size_bytes > mbr.mbr_tamano:
                            printError("No hay espacio suficiente en el disco")
                            file.close()
                            return False
                        else:
                            mbr.partitions[i].part_s += size_bytes
                            printSuccess(f"Se agregaron {size_bytes}B a la partición {name.upper()}")
                            mbr.partitions[i].display_info()
                            setted = True
                            break
                            
                    # In case that the partition is not the last one and the size is positive
                    elif i < 3 and size_bytes > 0:
                        index = i + 1
                        nextStart = mbr.mbr_tamano
                        while index < 4:
                            if mbr.partitions[index].part_s != -1:
                                nextStart = mbr.partitions[index].part_start
                                break
                            index += 1
                        if (mbr.partitions[i].part_start + mbr.partitions[i].part_s) + size_bytes > nextStart:
                            printError("No hay espacio suficiente en el disco")
                            file.close()
                            return False
                        else:
                            mbr.partitions[i].part_s += size_bytes
                            printSuccess(f"Se agregaron {size_bytes}B a la partición {name.upper()}")
                            mbr.partitions[i].display_info()
                            setted = True
                            break

                    # In case that the partition's size is negative
                    elif size_bytes < 0:
                        if mbr.partitions[i].part_s + size_bytes <= 0:
                            printError("La partición no puede tener un tamaño negativo o cero")
                            file.close()
                            return False
                        else:
                            new_size = mbr.partitions[i].part_s + size_bytes
                            if Fwrite_displacement_data(file, mbr.partitions[i].part_start + new_size, b'\0'*abs(size_bytes)):
                                mbr.partitions[i].part_s += size_bytes
                                printSuccess(f"Se redujeron {abs(size_bytes)}B a la partición {name.upper()}")
                                mbr.partitions[i].display_info()
                                setted = True
                                break
                            else:
                                printError("No se pudo eliminar espacio a la partición")
                                file.close()
                                return False
            except Exception as e:
                printError(f"{e}")
                file.close()
                return False
        if not found:
            printError(f"No se encontro la partición {name}")
            file.close()
            return False
        if setted:
            print("\n***** Escribiendo MBR *****")
            if Fwrite_displacement(file, 0, mbr):
                printSuccess("Se escribio el MBR correctamente")
                printSuccess("Se modifico la partición correctamente\n")
            else:
                printError("No se pudo escribir el MBR")
                file.close()
                return False
                
    # If we are going to create a new partition
    else:
        size_bytes = get_sizeB(size, unit)
        
        # Here we create a new partition
        start = len(mbr.doSerialize())
        foundSpace = False
        index = 0
        print("\n***** Buscando Espacio *****")
        for i, partition in enumerate(mbr.partitions):
            print(f"Particion {i+1}:")
            if partition.part_s != -1:
                start = partition.part_start + partition.part_s
                print("Ocupada")
            else:
                # Here we have to check if the space is enough
                indx = i + 1
                nextStart = mbr.mbr_tamano
                while indx < 4:
                    if mbr.partitions[indx].part_s != -1:
                        nextStart = mbr.partitions[indx].part_start
                        break
                    indx += 1
                if start + size_bytes <= nextStart:
                    foundSpace = True
                    index = i
                    break
                else:
                    print("No hay espacio")

        if not foundSpace:
            printError("No hay espacio disponible")
            file.close()
            return False

        print("\n***** Creando PARTICIÓN *****")
        part = Partition()
        part.set_info('n',type,fit,start,size_bytes,name)
        part.display_info()

        print("\n***** Escribiendo PARTICIÓN *****")
        mbr.partitions[index] = part
        if Fwrite_displacement(file, 0, mbr):
            printSuccess("Se creo la partición correctamente")
        else:
            printError("No se pudo escribir el MBR")
            file.close()
            return False

        try:
            file.close()
        except Exception as e:
            printError(f"{e}")
            return False

    printConsole("Finalizando FDISK\n")
    return True