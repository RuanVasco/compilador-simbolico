import logging
import ply.yacc as yacc
import sympy as sp

from lexical_analyzer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
)

def get_variable(expr):
    simbolos = list(expr.free_symbols)
    var_x = sp.Symbol('x')

    if var_x in simbolos:
        var = var_x
    elif len(simbolos) > 0:
        var = simbolos[0]
    else:
        var = var_x

    return var

def p_programa(p):
    '''
    programa : atribuir
             | atribuir E_KW mostrar
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
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
        | exp MODULO exp
    '''
    e1 = p[1]
    e2 = p[3]
    op = p[2]

    e1_is_str = isinstance(e1, str)
    e2_is_str = isinstance(e2, str)

    if e1_is_str or e2_is_str:
        if op == '+' and e1_is_str and e2_is_str:
            p[0] = e1 + e2
        else:
            raise TypeError(f"Operação inválida: {type(e1)} {op} {type(e2)}")
        return

    is_e1_num = isinstance(e1, (sp.Integer, sp.Float))
    is_e2_num = isinstance(e2, (sp.Integer, sp.Float))

    if is_e1_num and is_e2_num:
        is_e1_float = isinstance(e1, sp.Float)
        is_e2_float = isinstance(e2, sp.Float)

        if is_e1_float != is_e2_float:
            raise TypeError(f"Operação inválida: {type(e1)} {op} {type(e2)}")

    if op == '%':
        p[0] = e1 % e2
    elif op == '+':
        p[0] = e1 + e2
    elif op == '-':
        p[0] = e1 - e2
    elif op == '*':
        p[0] = e1 * e2
    elif op == '/':
        p[0] = e1 / e2
    elif op == '^':
        p[0] = e1 ** e2

def p_exp_group(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = p[2]

def p_exp_derivada(p):
    '''
    exp : DERIVAR_KW exp
    '''
    expr = p[2]
    p[0] = sp.diff(expr, get_variable(expr))

def p_exp_integral(p):
    '''
    exp : INTEGRAR_KW exp
    '''
    expr = p[2]
    p[0] = sp.integrate(expr, get_variable(expr))

def p_exp_seno(p):
    '''
    exp : SENO_KW exp
    '''
    expr = p[2]
    p[0] = sp.sin(expr)

def p_exp_cosseno(p):
    '''
    exp : COSSENO_KW exp
    '''
    expr = p[2]
    p[0] = sp.cos(expr)

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

def p_exp_string(p):
    '''
    exp : STRING
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        logging.error(f"Erro de sintaxe: Token inesperado {p.type} ('{p.value}') na linha {p.lineno}")
    else:
        logging.error("Erro de sintaxe: Fim inesperado do arquivo (EOF)")

parser = yacc.yacc()
