import concurrent.futures
import time
import os
import threading

# --- 模拟 I/O 密集型任务 ---
def perform_io_task(task_id, delay_seconds):
    """
    一个模拟 I/O 密集型操作的函数。
    它会打印开始信息，然后模拟 I/O 等待，最后打印结束信息并返回结果。
    """
    thread_name = threading.current_thread().name
    print(f"[{time.time():.2f}] IO 任务 {task_id} (线程: {thread_name})：开始模拟 I/O 等待 {delay_seconds} 秒...")
    
    # 模拟 I/O 操作：Python 线程在执行这种阻塞式 I/O 时会释放 GIL
    time.sleep(delay_seconds) 
    
    print(f"[{time.time():.2f}] IO 任务 {task_id} (线程: {thread_name})：I/O 等待结束。")
    return f"IO 任务 {task_id} 完成 (耗时 {delay_seconds} 秒)"

# --- 模拟 CPU 密集型任务 ---
def perform_cpu_task(task_id, iterations):
    """
    一个模拟 CPU 密集型操作的函数。
    它会进行大量计算，消耗 CPU 时间。
    """
    thread_name = threading.current_thread().name
    print(f"[{time.time():.2f}] CPU 任务 {task_id} (线程: {thread_name})：开始计算 {iterations} 次...")
    
    # 模拟 CPU 计算
    result = 0
    for i in range(iterations):
        result += i * 2 / 3.1415926 # 简单计算
    
    print(f"[{time.time():.2f}] CPU 任务 {task_id} (线程: {thread_name})：计算结束。")
    return f"CPU 任务 {task_id} 完成 (计算 {iterations} 次)"

# --- 主程序 ---
def main():
    print(f"[{time.time():.2f}] 主线程 (线程: {threading.current_thread().name})：程序开始。")

    # 使用 ThreadPoolExecutor 创建一个线程池
    # max_workers 可以根据你的 CPU 核心数和任务类型来调整
    # 这里设置 3 个工作线程，以便观察并行性
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # --- 提交 I/O 密集型任务 ---
        # 任务1：需要等待 5 秒 (最长的 I/O 任务)
        future_io_1 = executor.submit(perform_io_task, 1, 5)
        # 任务2：需要等待 2 秒
        future_io_2 = executor.submit(perform_io_task, 2, 4)

        # --- 提交 CPU 密集型任务 (用于观察调度) ---
        # 任务3：进行大量计算
        future_cpu_3 = executor.submit(perform_cpu_task, 3, 100_000_000) 
        # 任务4：进行少量计算
        future_cpu_4 = executor.submit(perform_cpu_task, 4, 2_000_000)

        print(f"[{time.time():.2f}] 主线程：所有任务已提交到线程池。")

        # --- 获取 I/O 任务的结果 ---
        # 对 future_io_1 调用 .result() 会阻塞主线程
        print(f"[{time.time():.2f}] 主线程：正在等待任务 1 的 I/O 结果 (最长的 I/O 任务)。")
        result_io_1 = future_io_1.result() # 主线程在此处阻塞，等待任务1完成
        print(f"[{time.time():.2f}] 主线程：收到结果：{result_io_1}")

        # 主线程继续等待其他 I/O 任务的结果
        print(f"[{time.time():.2f}] 主线程：正在等待任务 2 的 I/O 结果。")
        result_io_2 = future_io_2.result()
        print(f"[{time.time():.2f}] 主线程：收到结果：{result_io_2}")

        # --- 获取 CPU 任务的结果 ---
        # 虽然主线程之前在等待 I/O，但 CPU 任务可能已经完成或正在进行
        print(f"[{time.time():.2f}] 主线程：正在等待 CPU 任务 3 的结果。")
        result_cpu_3 = future_cpu_3.result()
        print(f"[{time.time():.2f}] 主线程：收到结果：{result_cpu_3}")

        print(f"[{time.time():.2f}] 主线程：正在等待 CPU 任务 4 的结果。")
        result_cpu_4 = future_cpu_4.result()
        print(f"[{time.time():.2f}] 主线程：收到结果：{result_cpu_4}")

    print(f"[{time.time():.2f}] 主线程：所有任务完成，程序结束。")



if __name__ == "__main__":
    main()