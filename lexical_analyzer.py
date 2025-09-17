import ply.lex as lex

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

inputs = {
    "input1": "atribuir x = 10",
    "input2": "atribuir y = (5 + 3) * 2",
    "input3": "atribuir f = derivar x^2",
    "input4": "atribuir z = 10 e mostrar z",
    "input5": "atribuir w = integrar (x + 1)",
    "input6": "atribuir g = somar 4 e 3"
}

lexer = lex.lex()

for title, value in inputs.items():
    print(f"Tokens para {title}")
    lexer.input(value)

    for tok in lexer :
        print(tok)