# import time, threading

# # 新线程执行的代码:
# def loop():
#     print( f'thread {threading.current_thread().name} is running...' )
#     n = 0
#     while n < 5:
#         n = n + 1
#         print( f'thread {threading.current_thread().name} >>> {n}' )
#         time.sleep(1)
#     print( f'thread {threading.current_thread().name} ended.' )

# print( f'thread {threading.current_thread().name} is running...' )
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()

# print( f'thread {threading.current_thread().name} ended.' )


import threading, time

def thread_function(name):
    time.sleep(1) # 线程的调度由操作系统完成
    print(f"Thread {name}: {threading.current_thread().name}")

if __name__ == "__main__":
    # 创建两个线程
    threads = []
    for index in range(2):
        thread = threading.Thread(target=thread_function, args=(index,)) # 分别创建线程
        threads.append(thread)
        thread.start() # 线程就绪

    # 主线程也调用 current_thread()
    print(f"Main thread: {threading.current_thread().name}")

    # 等待所有线程完成
    # 实际的输出顺序仍然取决于操作系统的线程调度策略
    for thread in threads:
        thread.join() # 阻塞当前线程（主线程），开始执行 指定线程
