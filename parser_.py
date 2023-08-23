import ply.yacc as yacc
# Import all from lexer
from lexer import *
from Commands.Mkdisk import *
from Commands.Rep import *

file_name = ''

# Grammar rules
def p_init(t):
    'init : list_commands'
    t[0] = t[1]

def p_list_commands(t):
    '''list_commands : list_commands commands
                    | commands'''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
def p_commands(t): 
    '''commands : command_execute
                | command_mkdisk
                | command_rep'''
    t[0] = t[1]

def p_command_execute(t):
    '''command_execute : EXECUTE GUION PATH IGUAL CADENA'''
    t[0] = [t[1], t[5]]

def p_command_mkdisk(t):
    'command_mkdisk : MKDISK'
    global file_name
    file_name = mkdisk()
    t[0] = t[1]

def p_command_rep(t):
    'command_rep : REP'
    rep(file_name)
    t[0] = t[1]

parser = yacc.yacc()

def get_parser():
    return parser

'''entrada = '''
#execute -path="C:/Users/Usuario/Desktop/entrada.txt"
''' 
print(parser.parse(entrada))
'''