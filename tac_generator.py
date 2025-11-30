import sympy as sp

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.instructions = []

    def new_temp(self):
        name = f"t{self.temp_count}"
        self.temp_count += 1
        return name

    def generate(self, expr):
        self.temp_count = 0
        self.instructions = []
        last_temp = self.visit(expr)

        self.instructions.append(f"return {last_temp}")
        return self.instructions, last_temp

    def visit(self, node):
        if isinstance(node, (sp.Symbol, sp.Integer, sp.Float)):
            return str(node)

        if isinstance(node, sp.Rational):
            return str(float(node))

        if isinstance(node, (sp.Add, sp.Mul)):
            op = "+" if isinstance(node, sp.Add) else "*"

            left_operand = self.visit(node.args[0])

            for i in range(1, len(node.args)):
                right_operand = self.visit(node.args[i])
                result_temp = self.new_temp()

                self.instructions.append(f"{result_temp} = {left_operand} {op} {right_operand}")

                left_operand = result_temp

            return left_operand

        if isinstance(node, sp.Pow):
            base = self.visit(node.args[0])
            exp = self.visit(node.args[1])
            result_temp = self.new_temp()

            self.instructions.append(f"{result_temp} = {base} ^ {exp}")
            return result_temp

        if isinstance(node, (sp.sin, sp.cos)):
            func_name = "sin" if isinstance(node, sp.sin) else "cos"

            arg = self.visit(node.args[0])

            result_temp = self.new_temp()

            self.instructions.append(f"{result_temp} = {func_name} {arg}")

            return result_temp

        return str(node)
