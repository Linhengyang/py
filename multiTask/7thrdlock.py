# multithread
import time, threading, random

# 假定这是你的银行存款:
balance = 0

def change_it_nolock(n):
    # 先存后取，结果应该为0:
    global balance

    ###### 归根结底 下述操作 不是 原子操作, 即不存在不可分割性. 它可以被分割成 四个操作: 1 x = bal+n, 2 bal = x, 3 y = x-n, 4 bal = y
    ###### 在多线程环境中, 可能引发 竞态条件, 即线程1 里的操作1234可能和线程2 里的操作1234顺序混乱, 但又因为是同一个bal, 导致最后的bal结果出错
    balance = balance + n
    time.sleep(random.random() * 0.0001)  # 引入随机延迟, 增加竞态条件的概率, 增加线程切换的概率
    balance = balance - n


# 执行 change_it_nolock 操作很多次. 计划部署在 线程上. 后续可以部署在 进程上试试
def run_thread_nolock(n):
    for i in range(500):
        change_it_nolock(n)
    print( f'half in {threading.current_thread().name}' )
    for i in range(500):
        change_it_nolock(n)
    print( f'whole in {threading.current_thread().name}' )


t1 = threading.Thread(target=run_thread_nolock, args=(5,), name='t1')
t2 = threading.Thread(target=run_thread_nolock, args=(8,), name='t2')

t1.start()
t2.start()

t1.join() # 触发阻塞 主线程, t1 和 t2 线程并发运行, 所以os可能先执行 t1 线程, 也可能先执行 t2 线程.
# 当t1执行完毕, 阻塞被释放, 但此时 t2还没执行完毕. 这样会出现 主线程 和 t2线程的并发运行.
t2.join() # 所以需要 t2.join() 继续阻塞 主线程. 万一是主线程继续运行, t2.join() 可以及时阻塞 主线程

print(f'balance no lock: {balance}') # 在macos 环境中, 无法复现 balance != 0 的情景. 可能是因为 macos的实现中, 自加操作是原子操作

print('################################################################')

# 假定这是你的银行存款:
balance = 0
lock = threading.Lock()

def change_it_lock(n):
    # 先存后取，结果应该为0:
    global balance

    #### 加锁lock, 使得下面的操作变成原子操作 ####
    #### 但这意味着 每次 change it 操作都要执行一遍 lock.acquire() 和 lock.release()
    with lock:
        balance = balance + n
        time.sleep(random.random() * 0.0001)  # 引入随机延迟, 增加竞态条件的概率, 增加线程切换的概率
        balance = balance - n


# 执行 change_it_lock 操作 很多次. 计划部署在 线程上. 后续可以部署在 进程上试试
def run_thread_lock(n):
    for i in range(1000):
        change_it_lock(n)
    print( f'half in {threading.current_thread().name}' )
    for i in range(1000):
        change_it_lock(n)
    print( f'whole in {threading.current_thread().name}' )


t1 = threading.Thread(target=run_thread_lock, args=(5,), name='t1')
t2 = threading.Thread(target=run_thread_lock, args=(8,), name='t2')

t1.start()
t2.start()

t1.join() # 触发阻塞 主线程, 等t1执行完毕之后, 释放阻塞. 由于线程t1和t2并发运行, 所以os可能先执行t1线程, 也可能先执行t2线程.
t2.join() # 如果不使用 t2.join(), 那么可能会出现一种情况: t1执行完毕, 阻塞被释放, 但此时 t2还没执行完毕. 这样会出现 主线程 和 t2线程的并发运行
# 如果 主线程 和 t2线程 并发运行, 可以导致 t2线程并未执行完毕时, 就输出了 balance, 导致输出错误

print(f'balance lock: {balance}')