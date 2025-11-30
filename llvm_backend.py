from llvmlite import ir, binding

class LLVMBackend:
    def __init__(self, func_name='main_func'):
        try:
            binding.initialize_native_target()
            binding.initialize_native_asmprinter()
        except RuntimeError:
            pass

        self.func_name = func_name
        self.module = ir.Module(name='modulo_compilador')

        triple = binding.get_default_triple()

        self.module.triple = triple

        self.double = ir.DoubleType()
        self.var_map = {}
        self.builder = None
        self.func = None

    def _init_function(self, variables):
        arg_types = [self.double] * len(variables)
        func_type = ir.FunctionType(self.double, arg_types)

        self.func = ir.Function(self.module, func_type, name=self.func_name)

        for i, var_name in enumerate(variables):
            arg = self.func.args[i]
            arg.name = str(var_name)
            self.var_map[str(var_name)] = arg

        block = self.func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(block)

    def _get_llvm_value(self, operand_str):
        operand_str = operand_str.strip()

        if operand_str in self.var_map:
            return self.var_map[operand_str]

        try:
            val = float(operand_str)
            return ir.Constant(self.double, val)
        except ValueError:
            raise ValueError(f"Operando desconhecido: {operand_str}")

    def _declare_pow(self):
        try:
            return self.module.get_global("llvm.pow.f64")
        except KeyError:
            pow_func_ty = ir.FunctionType(self.double, [self.double, self.double])
            return ir.Function(self.module, pow_func_ty, name="llvm.pow.f64")

    def _declare_sin(self):
        try:
            return self.module.get_global("sin")
        except KeyError:
            sin_func_ty = ir.FunctionType(self.double, [self.double])
            return ir.Function(self.module, sin_func_ty, name="sin")

    def _declare_cos(self):
        try:
            return self.module.get_global("cos")
        except KeyError:
            cos_func_ty = ir.FunctionType(self.double, [self.double])
            return ir.Function(self.module, cos_func_ty, name="cos")

    def _declare_printf(self):
        try:
            return self.module.get_global("printf")
        except KeyError:
            voidptr_ty = ir.IntType(8).as_pointer()
            printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            return ir.Function(self.module, printf_ty, name="printf")

    def _create_main_wrapper(self, num_args):
        main_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, main_type, name="main")
        block = main_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        test_value = 3.0
        test_args = [ir.Constant(self.double, test_value)] * num_args

        result = builder.call(self.func, test_args)

        printf_func = self._declare_printf()

        fmt_str = "Resultado do LLVM: %f \n\0"
        c_fmt_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt_str)), bytearray(fmt_str.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt_str.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt_str

        fmt_arg = builder.bitcast(global_fmt, ir.IntType(8).as_pointer())

        builder.call(printf_func, [fmt_arg, result])

        builder.ret(ir.Constant(ir.IntType(32), 0))

    def generate_from_tac(self, tac_instructions, variables):
        self.var_map = {}
        self._init_function(variables)

        for line in tac_instructions:
            parts = line.split()

            if parts[0] == 'return':
                ret_val = self._get_llvm_value(parts[1])
                self.builder.ret(ret_val)
                continue

            target = parts[0]

            if (len(parts) == 5):
                op1_str = parts[2]
                operator = parts[3]
                op2_str = parts[4]

                val1 = self._get_llvm_value(op1_str)
                val2 = self._get_llvm_value(op2_str)

                result = None

                if operator == '+':
                    result = self.builder.fadd(val1, val2, name=target)
                elif operator == '*':
                    result = self.builder.fmul(val1, val2, name=target)
                elif operator == '-':
                    result = self.builder.fsub(val1, val2, name=target)
                elif operator == '/':
                    result = self.builder.fdiv(val1, val2, name=target)
                elif operator == '^':
                    pow_func = self._declare_pow()
                    result = self.builder.call(pow_func, [val1, val2], name=target)

                if result:
                    self.var_map[target] = result

            elif len(parts) == 4:
                operator = parts[2]
                op1_str = parts[3]

                val1 = self._get_llvm_value(op1_str)
                result = None

                if operator == 'sin':
                    func = self._declare_sin()
                    result = self.builder.call(func, [val1], name=target)
                elif operator == 'cos':
                    func = self._declare_cos()
                    result = self.builder.call(func, [val1], name=target)

                if result: self.var_map[target] = result

        self._create_main_wrapper(len(variables))

        return str(self.module)

    def save_to_file(self, filename="programa.ll"):
        with open(filename, "w") as f:
            f.write(str(self.module))
        return filename
