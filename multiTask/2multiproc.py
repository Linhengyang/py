from multiprocessing import Process
import os
import time
# 子进程要执行的代码: 打印当前 子进程的名字 和 进程pid
def run_proc(name):
    print( f'Run child process {name} {os.getpid()}...' )
    time.sleep(5)
    print( f'Run child process {name} {os.getpid()}...' )



if __name__=='__main__':
    # print( f'Parent process now is {os.getpid()}.' )
    p = Process(target=run_proc, args=('test',)) # 创建 子进程. 子进程处于 就绪状态 
    print( f'Now is {os.getpid()}' )
    p.start() # 子进程开始执行, 但是 .start()方法是异步的, 即它不会阻塞主进程, 直接返回接着执行主进程后续代码, 子进程相当于在背后默默执行

    print( f'Process run. Now is {os.getpid()}' ) # 主进程 没有被.start()阻塞, 继续得到执行. 子进程此时也在执行中
    time.sleep(20) # 主进程和子进程同步执行. 所以 子进程 走完 5s 之后, 主进程继续走 20-5 = 15s.

    p.join() # 用于阻塞当前进程或线程，直到调用 .join() 的子进程或子线程完成. 即阻塞 主进程, 运行 子进程 p. 即
    # 如果上面 主进程是 time.sleep(1), 那么主进程会先于 子进程 结束. 但是 由于 p.join() 的存在, 主进程会被阻塞（而不会跑下面的代码），直到 子进程结束
    # 子进程结束后, join合入当前进程

    print( f'Child process end. Now is {os.getpid()}' ) # 因为子进程已经被 .join()方法合入主进程, 所以此语句只会被主进程执行一遍