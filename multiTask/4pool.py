from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print( f'Run task {name} {os.getpid()}...' )
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print( f'Task {name} runs {end-start} seconds.' )


if __name__=='__main__':
    print( f'Parent process {os.getpid()}.' ) # 打印父进程 pid
    p = Pool(4) # 初始化一个 进程池, 具有4个工作进程
    # 通过循环调用 p.apply_async() 方法, 异步提交 5 个任务到进程池中
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    
    print( 'Waiting for all subprocesses done...' )

    # 在所有任务提交完毕后，调用 p.close() 方法关闭进程池，这意味着不再允许向进程池中添加新的任务
    p.close()


    p.join()# 阻塞主进程, 等待直到进程池中的所有子进程结束
    print('All subprocesses done.')