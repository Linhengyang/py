import dis

def add_numbers(a, b):
    c = a + b
    return c

dis.dis(add_numbers)


'''
output in WSL ubuntu24.04 python3.12
3           0 RESUME                   0

4           2 LOAD_FAST                0 (a)
            4 LOAD_FAST                1 (b)
            6 BINARY_OP                0 (+)
            10 STORE_FAST               2 (c)

5          12 LOAD_FAST                2 (c)
            14 RETURN_VALUE
'''