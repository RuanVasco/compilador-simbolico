import ply.lex as lex
import sympy as sp

reserved = {
    'atribuir': 'ATRIBUIR_KW',
    'mostrar': 'MOSTRAR_KW',
    'e': 'E_KW',
    'derivar': 'DERIVAR_KW',
    'integrar': 'INTEGRAR_KW',
}

tokens = [
    'NUMBER',
    'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MODULO',
    'LPAREN', 'RPAREN',
    'EQUALS',
    'STRING'
] + list(reserved.values())

t_MODULO = r'\%'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = sp.S(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, None)
    if t.type:
        return t

    t.type = 'ID'
    t.value = sp.Symbol(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_STRING(t):
    r'"[^"]*"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
