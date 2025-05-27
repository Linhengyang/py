# 子进程 可以是外部进程
# subprocess模块可以 非常方便地启动一个子进程，然后控制其输入和输出

import subprocess


print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org']) # 调用子进程, 执行 nslookup www.python.org 命令
print('Exit code:', r)


# 需要输入 参数
print('$ nslookup')
# subprocess.Popen 用于创建子进程并与其进行交互。它提供了非常灵活的方式来启动和控制子进程，包括读取其输出、发送输入以及获取其退出状态。
# Popen 参数 stdin/stdout/stderr

# stdin=None
# 子进程的标准输入将连接到父进程的标准输入。这意味着子进程可以直接从父进程的标准输入中读取数据。
# 用途：适用于不需要与子进程进行交互的场景，或者子进程可以从用户的键盘输入中读取数据。

# p = subprocess.Popen(['ls'])

# stdin=subprocess.PIPE
# 子进程的标准输入将被重定向到一个管道。父进程可以通过这个管道向子进程发送数据。
# 用途：适用于需要从父进程向子进程发送数据的场景。父进程可以通过 Popen 对象的 communicate 方法或 stdin 属性向子进程发送数据。

p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 与子进程通信
input_instr = b'set q=mx\npython.org\nexit\n'
output, err = p.communicate( input=input_instr )

# 打印子进程的输出
print(output.decode('utf-8'))
print(err.decode('utf-8'))


# 获取子进程的退出代码
print('Exit code:', p.returncode)