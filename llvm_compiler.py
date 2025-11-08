import sympy as sp
from llvmlite import ir, binding

import sympy as sp
from sympy.core.function import Function
from llvmlite import ir, binding

class CodeGenerator:
    def __init__(self, expr, func_name='compiled_func'):
        self.expr = expr
        self.func_name = func_name
        self.double = ir.DoubleType()
        self.module = ir.Module(name='meu_modulo')

        symbols = list(expr.free_symbols)
        if not symbols:
            self.variable = sp.Symbol('x')
        else:
            self.variable = symbols[0]

        func_type = ir.FunctionType(self.double, [self.double])
        self.func = ir.Function(self.module, func_type, name=self.func_name)

        self.func.args[0].name = str(self.variable)

        block = self.func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(block)

        pow_ty = ir.FunctionType(self.double, [self.double, self.double])
        self.pow_func = ir.Function(self.module, pow_ty, name="llvm.pow.f64")

    def _codegen(self, expr):

        if isinstance(expr, sp.Symbol):
            arg_map = {arg.name: arg for arg in self.func.args}
            return arg_map.get(str(expr), ir.Constant(self.double, 0.0))

        if isinstance(expr, (sp.Integer, sp.Rational)):
            return ir.Constant(self.double, float(expr))

        if isinstance(expr, sp.Add):
            res = self._codegen(expr.args[0])
            for arg in expr.args[1:]:
                res = self.builder.fadd(res, self._codegen(arg), name='add_tmp')
            return res

        if isinstance(expr, sp.Mul):
            res = self._codegen(expr.args[0])
            for arg in expr.args[1:]:
                res = self.builder.fmul(res, self._codegen(arg), name='mul_tmp')
            return res

        if isinstance(expr, sp.Pow):
            base = self._codegen(expr.args[0])
            exp = self._codegen(expr.args[1])

            return self.builder.call(self.pow_func, [base, exp], name='pow_tmp')

        if isinstance(expr, Function):
            pass

        raise TypeError(f"Tipo desconhecido do SymPy: {type(expr)}")

    def generate(self):
        result = self._codegen(self.expr)
        self.builder.ret(result)
        return self.module


def compile_and_run(llvm_module, func_name, *args):
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = binding.parse_assembly(str(llvm_module))
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)

    engine.finalize_object()

    func_ptr = engine.get_function_address(func_name)
    if not func_ptr:
        raise RuntimeError(f"Erro do JIT: Nao foi possivel encontrar a funcao '{func_name}'")

    from ctypes import CFUNCTYPE, c_double
    cfunc = CFUNCTYPE(c_double, c_double)(func_ptr)

    result = cfunc(*args)
    return result
