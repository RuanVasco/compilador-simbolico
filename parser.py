import ply.yacc as yacc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
)

def p_programa(p):
    '''
    programa : atribuir
             | atribuir E_KW mostrar
    '''
    if len(p) == 2:
        print(f"Programa Válido (Atribuição Simples): {p[1]}")
        p[0] = p[1]
    else:
        print(f"Programa Válido (Atribuição e Mostrar): {p[1]} e {p[3]}")
        p[0] = (p[1], 'E', p[3])

def p_atribuir(p):
    '''
    atribuir : ATRIBUIR_KW ID EQUALS exp
    '''
    p[0] = ('atribuir', p[2], p[4])

def p_mostrar(p):
    '''
    mostrar : MOSTRAR_KW ID
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
    p[0] = (p[1], p[2], p[3])

def p_exp_group(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = p[2]

def p_exp_derivada(p):
    '''
    exp : DERIVAR_KW exp
    '''
    p[0] = ('derivar', p[2])

def p_exp_integral(p):
    '''
    exp : INTEGRAR_KW exp
    '''
    p[0] = ('integrar', p[2])

def p_exp_number(p):
    '''
    exp : NUMBER
    '''
    p[0] = p[1]

def p_exp_variable(p):
    '''
    exp : ID
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe: Token inesperado {p.type} ('{p.value}') na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo (EOF)")

parser = yacc.yacc()
