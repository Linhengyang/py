from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q: Queue):
    print( f'write write write write: {os.getpid()}' )
    print( f'write write write S to queue...' )
    q.put( 'S' )
    for value in ['A', 'B', 'C']:
        print( f'write write write {value} to queue...' )
        q.put(value) # 压入 队列 q. 当压入不成功的时候(比如 q 在压入 value 之前已经达到最大容量了, 那么触发 阻塞 当前进程). 当前这种写法不会被阻塞
        time.sleep( 10 ) # 模拟延迟. 该线程阻塞 设定 时间



# 读数据进程执行的代码:
def read(q: Queue):
    print( f'read read read read: {os.getpid()}' )
    i = 0
    while True: # 一次性读完所有队列中存在的element
        print(i)
        value = q.get( block=True ) # block=True: 当队列读取不成功(在get之前 q 就为空）时, 触发 阻塞 当前进程
        print( f'read read read {value} from queue at index {i}' )
        i += 1






if __name__=='__main__':
    # 父进程创建Queue，并共享给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动 子进程pw 写入: 当前 父进程、pw子进程并发运行
    pw.start()
    # 由于父进程没有被阻塞, 所以pr.start()启动 子进程pr。当前 父进程、pw子进程、pr子进程 并发运行.
    pr.start()

    # 执行 pw 进程. 执行过程中, 写入'A'后 sleep 触发阻塞进程pw.
    # 执行 pr 进程. 执行过程中, 打印 0 之后，可能因为 read 空队列 触发阻塞pr，也可能read S 或 SA 之后，read 空队列 触发阻塞 pr

    # pr 读取'A'后, 在第二次读取时从空 q 读取出发阻塞. os 寻找 就绪 状态的进程, 找不到
    # 直到 pw进程 sleep结束, 进入就绪状态, 马上被 os 调度执行, 执行写入'B'之后（此时 pr 判定自己转为 就绪）, sleep 触发阻塞进程pw
    # os 寻找就绪状态的进程, 此时 pr 已经在 q 被写入 'B' 之后判定自己转为 就绪, 所以被 os 调度执行.
    # 执行 pr 进程. 执行过程中, 发现 q 是空的, 触发阻塞进程pr, pw进程开始执行. 然后发生的事情如上行所叙述

    pw.join() # 阻塞父进程. 当前 pw、pr两个子进程并行运行. 由于 pw 和 pr 进程是并发的, 所以os可能先执行 pr 进程, 也可能先执行 pw 进程. 
    # pw 进程执行完毕之后, 释放阻塞, 然后父进程和pr进程可能并发运行
    
    pr.terminate() # 父进程执行到此, 即结束 pr子进程