from lexical_analyzer import lexer
from parser import parser
from llvm_compiler import CodeGenerator, compile_and_run
import sympy as sp

def run_lexer(data):
    print("--- 1. Análise Léxica (Tokens) ---")
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"    {tok}")

def run_parser(data):
    print("\n--- 2. Análise Sintática (Parser + SymPy) ---")
    result = parser.parse(data, lexer=lexer)

    if result is None:
        print("    Falha na análise sintática (ver erro acima).")
        return None

    print(f"    Resultado simbólico: {result}")
    return result

def run_backend(expression, func_name):
    print("    Gerando LLVM IR...")

    if isinstance(expression, str):
        print("    Expressão é uma string constante.")
        return expression

    variables = list(expression.free_symbols)
    if len(variables) > 1:
        print(f"    AVISO: Expressão com múltiplas variáveis ({variables}).")
        print("    O JIT não pode compilar esta função. Pulando.")
        return None

    if not variables:
        print("    Expressão é uma constante. Não há função para compilar.")
        return float(expression)

    codegen = CodeGenerator(expression, func_name)
    llvm_module = codegen.generate()
    print(str(llvm_module))

    print("\n    --- 4. Execução (JIT) ---")
    test_value = 3.0
    print(f"Usando {test_value} como valor de teste")

    test_variable_name = codegen.variable.name

    jit_result = compile_and_run(llvm_module, func_name, test_value)
    print(f"    Resultado da função: {func_name}({test_variable_name}={test_value}) = {jit_result}")

    return jit_result

def process_input(title, value, symbol_table):
    print(f"\n======================================")
    print(f"Analisando {title}: '{value}'")
    print(f"======================================")

    try:
        run_lexer(value)

        result = run_parser(value)

        if result is None:
            return

        print("\n--- 3. Análise Semântica e Execução ---")

        if isinstance(result, tuple) and len(result) == 3 and result[1] == 'E':
            atribuir_tuple = result[0]
            mostrar_tuple = result[2]

            if isinstance(atribuir_tuple, tuple) and atribuir_tuple[0] == 'atribuir':
                var_name = str(atribuir_tuple[1])
                expression = atribuir_tuple[2]

                valor = run_backend(expression, var_name)

                if valor is not None:
                    print(f"    Armazenando na Tabela de Símbolos: {var_name} = {valor}")
                    symbol_table[var_name] = valor

            if isinstance(mostrar_tuple, tuple) and mostrar_tuple[0] == 'mostrar':
                var_name_mostrar = str(mostrar_tuple[1])

                if var_name_mostrar in symbol_table:
                    print(f"\n    Comando 'mostrar' executado:")
                    print(f"    >>> {symbol_table[var_name_mostrar]}")
                else:
                    print(f"\n    ERRO: Variável '{var_name_mostrar}' não foi definida antes de 'mostrar'.")

        elif isinstance(result, tuple) and result[0] == 'atribuir':
            var_name = str(result[1])
            expression = result[2]

            valor = run_backend(expression, var_name)

            if valor is not None:
                print(f"    Armazenando na Tabela de Símbolos: {var_name} = {valor}")
                symbol_table[var_name] = valor

    except Exception as e:
        print(f"\n--- ERRO INESPERADO ---")
        print(f"    Ocorreu um erro: {e}")

def main():
    inputs = {
        "input1": "atribuir g = x + 'ola'",
        "input2": "atribuir l = 8 % 3 e mostrar l",
        "input3": "atribuir f = derivar x^2",
        "input4": "atribuir y = integrar (seno y^2)",
        "input5": "atribuir w = integrar (x + 1)",
        "input18": "atribuir f_deriv = derivar (derivar x^4)",
        "input19": "atribuir f_integ = integrar (integrar x)",
        "input20": "atribuir m = (derivar t^2) + (integrar y)",
        "input21": "atribuir k = (x+2)*(x-2)",
        "input22": "atribuir l = (x^2 + 1) / x",
        "input23": "atribuir val = (3+2)^2 e mostrar val",
        "input28": "atribuir s = 10 % 3",
        "input29": 'atribuir s = "ola" + " mundo" e mostrar s',
    }

    symbol_table = {}

    for title, value in inputs.items():
        process_input(title, value, symbol_table)

if __name__ == '__main__':
    main()
