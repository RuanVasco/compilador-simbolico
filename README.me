# Compilador Simbólico com Backend LLVM

Este projeto consiste em um compilador *source-to-source* desenvolvido em Python, capaz de interpretar expressões matemáticas complexas (incluindo derivadas e integrais), convertê-las para Código de Três Endereços (TAC) e, finalmente, gerar código de máquina intermediário (LLVM IR) executável.

O sistema utiliza a biblioteca **SymPy** para a análise simbólica e **llvmlite** para a geração de código nativo.

## Funcionalidades

- **Aritmética Básica:** Soma, Subtração, Multiplicação, Divisão, Potência e Módulo.
- **Cálculo Simbólico:**
  - **Derivadas:** `derivar(expressao)`
  - **Integrais:** `integrar(expressao)`
- **Funções Trigonométricas:** `seno(x)`, `cosseno(x)`.
- **Geração de Código Intermediário (TAC):** Linearização da árvore sintática abstrata.
- **Backend LLVM:** Geração de arquivos `.ll` compatíveis com o interpretador `lli`.
- **Execução Automática:** Wrapper em C (`main`) injetado automaticamente para exibir resultados no console via `printf`.

## Arquitetura do Compilador

O fluxo de compilação segue uma arquitetura em camadas:

1.  **Frontend (Lexer & Parser):** Utiliza `ply` para análise léxica e sintática. As expressões são convertidas imediatamente para objetos simbólicos do SymPy.
2.  **Middleware (TAC Generator):** Implementa o padrão **Visitor** para percorrer a Árvore de Sintaxe Abstrata (AST) do SymPy e "linearizar" as operações em instruções sequenciais (ex: `t0 = x + 1`).
3.  **Backend (LLVM Compiler):** Lê as instruções TAC e utiliza `llvmlite` para construir um módulo LLVM IR, definindo tipos, alocando registradores e chamando funções intrínsecas (como `llvm.pow`).

## Exemplo de Sintaxe da Linguagem

A linguagem aceita comandos no formato `atribuir VAR = EXPRESSAO` e `mostrar VAR`.

```text
atribuir x = 10 + 5
atribuir y = derivar(x^2 + 2*x)
atribuir z = integrar(y)
atribuir w = seno(z) + cos(z)
atribuir k = (x + 2) * (x - 2) e mostrar k
```

## Estrutura de Arquivos

* `main.py`: Ponto de entrada. Gerencia os inputs, chama o parser, o gerador TAC e o backend LLVM.
* `lexical_analyzer.py`: Definição dos tokens (Lexer).
* `parser.py`: Regras gramaticais e integração com SymPy.
* `tac_generator.py`: Transforma a AST do SymPy em código de três endereços.
* `llvm_compiler.py`: Traduz TAC para LLVM IR e gera o wrapper de execução.
* `out/`: Pasta onde os arquivos `.ll` compilados são salvos automaticamente.

## Compatibilidade e Versões

Este projeto depende da biblioteca `llvmlite`, que possui requisitos estritos de versão do Python.

- **Python Recomendado:** 3.10 ou 3.11 (Testado na 3.11.9).

**Tabela de Compatibilidade Sugerida:**

| Python | llvmlite | Status |
| :--- | :--- | :--- |
| 3.11.x | >= 0.39.1 | ✅ Estável (Recomendado) |
| 3.10.x | >= 0.38.0 | ✅ Estável |

> **Nota sobre o LLVM:** O `llvmlite` instala sua própria versão minimalista do LLVM para gerar o código intermediário. Para executar os arquivos `.ll` gerados, você pode usar qualquer versão recente do interpretador `lli` (LLVM 14 a 20+), pois o código IR é retrocompatível.

## Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/RuanVasco/compilador-simbolico.git
    cd compilador-simbolico
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

O projeto possui um arquivo principal que executa uma bateria de testes automatizados (definidos na lista `inputs`).

Para rodar o compilador:

```bash
python main.py
```
