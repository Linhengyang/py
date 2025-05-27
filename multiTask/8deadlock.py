import threading, time

# 创建两个锁
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    with lock1:
        print("Thread 1 acquired lock1")
        time.sleep(0.1)  # 模拟一些操作
        with lock2:
            print("Thread 1 acquired lock2")

def thread2():
    with lock2:
        print("Thread 2 acquired lock2")
        time.sleep(0.1)  # 模拟一些操作
        with lock1:
            print("Thread 2 acquired lock1")

# 创建两个线程
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

# 启动线程
t1.start()
t2.start()

# 等待线程结束
t1.join()
t2.join()