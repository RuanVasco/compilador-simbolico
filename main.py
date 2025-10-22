from lexical_analyzer import lexer
from parser import parser

def main():
    inputs = {
        "input1": "atribuir x = 10",
        "input2": "atribuir y = (5 + 3) * 2",
        "input3": "atribuir f = derivar x^2",
        "input4": "atribuir z = 10 e mostrar z",
        "input5": "atribuir w = integrar (x + 1)",
        "input6": "atribuir g = somar 4 e 3"
    }

    for title, value in inputs.items():
        print(f"\n--- Analisando {title}: '{value}' ---")
        try:
            result = parser.parse(value, lexer=lexer)
            if result is not None:
                print(f"Resultado final do parse: {result}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    main()
