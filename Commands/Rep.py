from Objects.MBR import MBR
from Utils.Fmanager import *
from Utils.Utilities import *
from Utils.Globals import *

def rep(name, path, id, ruta):
    printConsole('Ejecutando el comando REP')
    
    print('\n***** Buscando el disco *****')
    partition = get_mounted_partitionbyId(id)

    if not partition:
        printError(f'No se encontró la partición {id}')
        return False
    
    print('\n***** Abriendo el disco *****')
    try:
        file = open(partition['path'], 'rb+')
    except:
        printError(f'No se pudo abrir el disco {partition["path"]}')
        return False
    
    print('\n***** Leyendo el MBR *****')
    mbr = MBR()
    if not Fread_displacement(file, 0, mbr):
        printError(f'No se pudo leer el MBR del disco {partition["path"]}')
        file.close()
        return False
    
    # We have to check the type of report to generate in base of the name
    print('\n***** Generando el reporte *****')
    if name == 'mbr':
        code = mbr.generate_report_mbr(file)

        if not execute_graphviz(code, path):
            printError(f'No se pudo generar el reporte {name}')
            file.close()
            return False
        printSuccess(f'Se genero el reporte {name} correctamente')
    
    elif name == 'disk':
        code = mbr.generate_report_disk(file, id[3:])

        if not execute_graphviz(code, path):
            printError(f'No se pudo generar el reporte {name}')
            file.close()
            return False
        printSuccess(f'Se genero el reporte {name} correctamente')
        
    try:
        file.close()
    except:
        printError(f'No se pudo cerrar el disco {partition["path"]}')
        return False    
    
    printConsole("Finalizando REP\n")
    return True

def execute_graphviz(code, path):
    if code != '':
        try:
            dir, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)
            if dir != '':
                if not os.path.exists(dir):
                    os.makedirs(dir)
            dot = open(dir + '/' + name + '.dot', 'w+')
            dot.write(code)
            dot.close()
            os.system(f'dot -T{ext[1:]} {dir}/{name}.dot -o {dir}/{name}.{ext[1:]}')
        except Exception as e:
            printError(f'{e}')
            return False
    return True