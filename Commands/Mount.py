from Utils.Utilities import *
from Utils.Fmanager import *
from Objects.MBR import *
from Utils.Globals import *

def mount(path, name):
    printConsole('Ejecutando el comando MOUNT')
    print('\n***** Abriendo el disco *****')
    try:
        file = open(path, 'rb+')
    except:
        printError(f'No se pudo abrir el disco {path}')
        return False
    
    print('\n***** Leyendo el MBR *****')
    mbr = MBR()
    if not Fread_displacement(file, 0, mbr):
        printError(f'No se pudo leer el MBR del disco {path}')
        return False    
    mbr.display_info()

    print('\n***** Buscando la particion *****')
    partition = mbr.get_partitionbyName(name)
    if not partition:
        printError(f'No se encontro la particion {name} en el disco {path}')
        return False

    if partition.part_status.decode() == 'y':
        printError(f'La particion {name} ya esta montada')
        return False
    
    partition.display_info()
    # We make the id of the partition
    print('\n***** Creando ID de la particion *****')
    _, disk_name = os.path.split(path)
    disk_name = disk_name[:-4]

    index = 1
    for data in mounted_partitions:
        if data['path'] == path:
            index = int(data['id'][2:3]) + 1

    id = '94' + str(index) + disk_name
    print(f'ID: {id}')

    # We add the partition to the list
    print('\n***** Montando la partición *****')
    mounted_partitions.append({'id': id, 'path': path, 'name': name, 'partition': partition})
    printSuccess(f'Particion {name} montada con exito')
    display_mounted_partitions()
    printConsole('Finalizando MOUNT\n')