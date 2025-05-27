# to compile
'''
compile(source, filename, mode)
主要三个参数: 
    1. source: python代码字符串
    2. filename: 虚拟代表 source 的文件名. 一般用来 traceback in debug
    3. mode:
        'exec': 执行 source 代码. 此时 source 代码应该是完整的
        'eval': 执行 source 代码并返回右值. 此时 source 代码应该是右值
        'single': 交互式执行 REPL 代码(read-eval-print loop)


return: a code project --> 封装过的字节码
    1. exec(code_object) --> for exec/single mode compile
    2. eval(code_object) --> for eval mode compile

'''



if __name__ == "__main__":
    def add_():
        return '''
def add(a, b):
    return a + b
'''

    def fancy_func_():
        return '''
def fancy_func(a, b, c, d):
    e = add(a, b)
    f = add(c, d)
    g = add(e, f)
    return g
'''

    def evoke_():
        return add_() + fancy_func_() + 'print(fancy_func(1, 2, 3, 4))'

    prog = evoke_()

    print(prog)
    # from imperative programming to 
    # symbolic programming
    y = compile(prog, '<exec_input>', 'exec') # a code object, executable prorgam, pre-defined before compile

    exec(y)

    # 1. can skip the Python interpretre in many cases: multiple GPUs paired with a single Python thread on a CPU
    # 2. optimize and rewrite code since it can read code entirely
    # 3. easy to port: run the program in a non-Python environment

