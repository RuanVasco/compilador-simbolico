import ply.lex as lex
import ply.yacc as yacc

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
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN',
    'EQUALS'
] + list(reserved.values())

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
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'), 
    ('right', 'UMINUS'),
)

start = 'programa'


def p_programa(p):
    '''
    programa : atribuir_stmt
             | atribuir_stmt E_KW mostrar_stmt
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('programa', p[1], p[3]) 

def p_atribuir_stmt(p):
    '''
    atribuir_stmt : ATRIBUIR_KW ID EQUALS exp
    '''
    p[0] = ('atribuir', p[2], p[4]) 

def p_mostrar_stmt(p):
    '''
    mostrar_stmt : MOSTRAR_KW ID
    '''
    p[0] = ('mostrar', p[2])

def p_exp_binop(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp POWER exp
    '''
    p[0] = ('binop', p[2], p[1], p[3]) 

def p_exp_group(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = p[2] 

def p_exp_unary_minus(p):
    '''
    exp : MINUS exp %prec UMINUS
    '''
    p[0] = ('unop', '-', p[2]) 

def p_exp_number(p):
    '''
    exp : NUMBER
    '''
    p[0] = ('numero', p[1])

def p_exp_variable(p):
    '''
    exp : ID
    '''
    p[0] = ('variavel', p[1])

def p_exp_derivar(p):
    '''
    exp : DERIVAR_KW exp
    '''
    p[0] = ('derivar', p[2])

def p_exp_integrar(p):
    '''
    exp : INTEGRAR_KW exp
    '''
    p[0] = ('integrar', p[2])

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do arquivo!")

parser = yacc.yacc()

input1 = "atribuir x = 10"
input2 = "atribuir y = (5 + 3) * 2"
input3 = "atribuir f = derivar x^2"
input4 = "atribuir z = 10 e mostrar z"
input5 = "atribuir w = integrar (x + 1)"

print("--- TESTANDO ENTRADAS ---")

print(f"\nEntrada: '{input1}'")
result1 = parser.parse(input1)
print("AST:", result1)

print(f"\nEntrada: '{input2}'")
result2 = parser.parse(input2)
print("AST:", result2)

print(f"\nEntrada: '{input3}'")
result3 = parser.parse(input3)
print("AST:", result3)

print(f"\nEntrada: '{input4}'")
result4 = parser.parse(input4)
print("AST:", result4)

print(f"\nEntrada: '{input5}'")
result5 = parser.parse(input5)
print("AST:", result5)

print("\n--- TESTANDO ERRO ---")
input_error = "atribuir x = 5 +"
parser.parse(input_error)