# import ply
import ply.lex as lex

# List of errors
errors = []

# List of global token names.   This is always required
tokens = [
    'CADENA',
    'IGUAL',
    'GUION',
    'EXECUTE',
    'MKDISK',
    'REP',
    'PATH',
]

# Regular expression rules for simple tokens
t_IGUAL = r'\='
t_GUION = r'\-'
t_EXECUTE = r'execute'
t_MKDISK = r'mkdisk'
t_REP = r'rep'
t_PATH = r'path'

# Regular expression rules with some action code
#   All values are returned as strings
def t_CADENA(t):
    r'\"(.|\n)*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    errors.append(t.value[0])
    print(f'Caracter no reconocido: {t.value[0]} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Build the lexer
lexer = lex.lex()