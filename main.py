import logging
from input import Input
from lexical_analyzer import lexer
from parser import parser
from llvm_compiler import CodeGenerator, compile_and_run
from tac_generator import TACGenerator
import sympy as sp
from sympy import srepr

def setup_logger():
    logging.basicConfig(
        filename='compilador.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8'
    )

def run_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break

def run_parser(data):
    result = parser.parse(data, lexer=lexer)

    if result is None:
        logging.error("Falha na análise sintática (ver erro acima).")
        return None

    return result

def run_backend(expression, var_name):
    if isinstance(expression, str):
        logging.info(f"[TAC] Ignorado: Expressão é uma string constante.")
        return expression

    tac_gen = TACGenerator()

    try:
        tac_code, tac_result = tac_gen.generate(expression)

        logging.info(f"[Bloco TAC para '{var_name}']")
        for line in tac_code:
            logging.info(f"        {line}")
        logging.info(f"[Fim do Bloco TAC]")

        return expression

    except Exception as e:
        logging.error(f"ERRO ao gerar TAC: {e}")
        return None

def process_input(input, symbol_table):
    value = input.expr
    logging.info(f"---==== Processando a entrada {input.name} ====---")
    logging.info(f"'{value}'")

    try:
        run_lexer(value)
        result = run_parser(value)

        if result is None:
            logging.error("Falhou ao rodar o parser")
            return

        atribuir_tuple = None
        mostrar_tuple = None

        if isinstance(result, tuple) and len(result) == 3 and result[1] == 'E':
            atribuir_tuple = result[0]
            mostrar_tuple = result[2]

            if isinstance(atribuir_tuple, tuple) and atribuir_tuple[0] == 'atribuir':
                var_name = str(atribuir_tuple[1])
                expression = atribuir_tuple[2]

        elif isinstance(result, tuple) and result[0] == 'atribuir':
            atribuir_tuple = result
            var_name = str(result[1])
            expression = result[2]

        if atribuir_tuple:
            var_name = str(atribuir_tuple[1])
            expression = atribuir_tuple[2]

            logging.info(f"[SymPy Visual] {expression}")
            logging.info(f"[SymPy Interno] {srepr(expression)}")

            value = run_backend(expression, var_name)

            if value is not None:
                symbol_table[var_name] = value

                real_result_str = str(value).replace(" ", "")
                expect_result_str = str(input.expct).replace(" ", "")

                if real_result_str == expect_result_str:
                    logging.info(f"--- [TESTE APROVADO] Sucesso! O resultado '{real_result_str}' é igual ao esperado. ---")
                elif input.expct != "error":
                    logging.warning(f"--- [TESTE DIVERGENTE] Esperado: '{expect_result_str}' | Obtido: '{real_result_str}' ---")

        if mostrar_tuple:
            var_name_mostrar = str(mostrar_tuple[1])

            if var_name_mostrar in symbol_table:
                value_final = symbol_table[var_name_mostrar]
                logging.info(f"[OUTPUT MOSTRAR] O value de '{var_name_mostrar}' é: {value_final}")
            else:
                logging.error(f"Erro Semântico: Variável '{var_name_mostrar}' não foi definida antes de mostrar.")

    except Exception as e:
        if input.expct == "error":
            logging.error(f"\n--- ERRO ESPERADO: {e} ---")
        else:
            logging.error(f"\n--- ERRO INESPERADO: {e} ---")

def main():
    setup_logger()
    inputs: list[Input] = []

    inputs.append(Input("atribuir erro = x + 'texto'", "error", "teste_erro_semantico"))
    inputs.append(Input("atribuir const = (10 + 2) * 3 e mostrar const", "36", "teste_constantes"))
    inputs.append(Input("atribuir poli = (x + 2) * (x - 2)", "(x - 2)*(x + 2)", "teste_algebra_simples"))
    inputs.append(Input("atribuir d = derivar(x^3 + 2*x)", "3*x**2 + 2", "teste_derivada"))
    inputs.append(Input("atribuir i = integrar(y + t)", "t*y + y**2/2", "teste_integral_multivar"))
    inputs.append(Input("atribuir complexo = derivar(integrar(x^2))", "x**2", "teste_cadeia_calculo"))
    inputs.append(Input("atribuir d_const = derivar 50", "0", "teste_derivada_constante"))
    inputs.append(Input("atribuir res_seno = derivar(seno x)", "cos(x)", "teste_derivada_seno"))
    inputs.append(Input("atribuir res_cos = derivar(cosseno x)", "-sin(x)", "teste_derivada_cosseno"))

    symbol_table = {}

    for item in inputs:
        process_input(item, symbol_table)

if __name__ == '__main__':
    main()
