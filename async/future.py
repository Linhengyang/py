# future就是一个占位符：当你发起一个异步操作时，它不会立即返回结果，而是返回一个 Future 对象。
# 这个 Future 对象承诺在未来的某个时候，会持有这个异步操作的最终结果（成功值或异常）。

# future的一些特点
# 结果占位符： Future 对象本身不包含最终结果，它只是一个表示“某个值将在未来出现”的抽象。

# 状态管理： Future 对象有明确的生命周期和状态，通常包括：

    # Pending (等待中)： 异步操作正在进行，结果尚未可用。

    # Running (运行中)： 任务正在执行。

    # Done (已完成)： 异步操作已经结束，无论是成功还是失败，结果都已确定并可用。

    # Cancelled (已取消)： 异步操作在完成前被取消。

# 非阻塞获取结果状态： 你可以通过 Future 检查操作是否完成，而不需要阻塞主程序。

# 注册回调： 你可以在 Future 对象上注册一个或多个回调函数。当 Future 状态变为“已完成”时，这些回调函数就会被执行。



# concurrent.futures
# 多线程并发里的 future
# 用异步执行单计算核心的方式，实现了多线程并发。
# 然而线程之间仍然是平行独立的，站在使用线程池子的角度，只会觉得多个线程在同时运行，只是返回结果的时间有先后差别。

# 让我们来拆解和强调其中的几个关键点：

# “异步执行单计算核心的方式，实现了多线程并发”：

    # 单计算核心： 意味着在任何一个瞬间，CPU 核心只能真正执行一个线程上的指令。

    # 异步执行的方式： 这里的“异步”指的是非阻塞。当一个线程遇到 I/O 操作（比如等待网络数据、文件读写）时，它会主动或被动地让出 CPU 控制权。
    # 操作系统调度器会趁这个机会切换到另一个正在等待 CPU 的线程去执行。这使得 CPU 不会因为等待 I/O 而空闲。

    # 实现了多线程并发： 虽然不是真正的并行（Parallelism），但由于 CPU 在线程之间快速切换（上下文切换），并且在 I/O 等待期间能去做其他事情，
    # 给人的感觉就是多个线程在“同时”向前推进，即并发 (Concurrency)。

# “然而线程之间仍然是平行独立的”：

    # 每个线程都有自己独立的执行路径和堆栈。它们之间的切换是由操作系统内核的调度器完成的，对程序员来说，这些线程就像是独立运行的程序段。

    # 这种独立性也带来了共享数据时的线程安全问题（如竞态条件和死锁），需要使用锁等同步机制来协调。

# “站在使用线程池子的角度，只会觉得多个线程在同时运行，只是返回结果的时间有先后差别”：

    # 这是用户（开发者）的直观感受。你提交任务给线程池后，不会感觉到阻塞。线程池会立即返回 Future 对象。

    # 这些 Future 对象的 result() 返回顺序和 as_completed() 的产出顺序，会反映出实际的任务完成时间，而不是提交时间，
    # 因为它受到任务本身的耗时（特别是 I/O 耗时）和线程调度情况的影响。

import concurrent.futures
import time





# Python
def long_running_task(name, delay):
    """模拟一个耗时的任务"""
    print(f"任务 {name} 开始执行...")
    time.sleep(delay) # 模拟耗时操作
    print(f"任务 {name} 完成。")
    return f"任务 {name} 的结果"

print("主程序开始执行...")

# 创建一个线程池执行器
begin = time.time()
num_threads = 2
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # 提交任务，并立即获得一个 Future 对象
    future1 = executor.submit(long_running_task, "A", 2)
    future2 = executor.submit(long_running_task, "B", 3)
    future3 = executor.submit(long_running_task, "C", 4)

    print("主程序提交任务后立即继续执行其他代码...")

    # 方式一：检查 Future 状态和阻塞获取结果
    print(f"Future1 是否完成? {future1.done()}") # False
    print(f"Future2 是否完成? {future2.done()}") # False
    print(f"Future2 是否完成? {future3.done()}") # False

    # get() 方法会阻塞，直到 Future 完成并返回结果
    # 如果任务失败，get() 会重新抛出异常
    print(f"获取 Future1 的结果: {future1.result()}") # 会阻塞future1所在的线程，直到任务A完成。其线程占据的计算资源被释放
    print(f"Future1 现在是否完成? {future1.done()}") # True

    # 方式二：注册回调函数 (不常用，通常用 result() 或 as_completed())
    def task_done_callback(future):
        try:
            print(f"回调函数：任务 {future.result()} 已完成！")
        except Exception as e:
            print(f"回调函数：任务失败，错误: {e}")

    future2.add_done_callback(task_done_callback)
    # add_done_callback 不会阻塞，回调会在任务完成后被调用

    # 方式三：as_completed() 接受一个可迭代的 Future 对象集合，然后返回一个迭代器。
    # 当你迭代这个迭代器时，它会阻塞，直到下一个 Future 对象完成，然后立即产出（yield）那个完成的 Future
    for finished_future in concurrent.futures.as_completed([future3]):
        try:
            # result() 方法获取 Future 的结果。
            # 如果 Future 已经完成，result() 不会阻塞。
            # 如果任务执行过程中发生异常，result() 会重新抛出该异常。
            result = finished_future.result()
            print(f"处理结果: {result}")
        except Exception as exc:
            # 捕获任务执行中的异常
            print(f"任务发生异常: {exc}")


print("所有任务提交完毕，主程序可以退出")
# 注意：with 语句块结束后，executor 会等待所有提交的任务完成
print(f'{num_threads} threads time {time.time()-begin}')












# 线程被阻塞，一般是由于外界耗时操作使它进入等待状态，其实际计算资源被os调度给其他线程。
# 但是，线程上跑多个协程，反而是为了避免该线程进入等待状态，因为当某个协程遇到高耗时io时，由于协程调用是非阻塞的，故马上另一个协程会拉起运行在线程上。
# 这样的设计下，只有所有协程都遇到高耗时io，才会阻塞线程。

# “所以线程被阻塞，一般是由于外界耗时操作使它进入等待状态，其实际计算资源被 OS 调度给其他线程。”
    # 正确。这是操作系统级别的行为。当一个线程发起一个同步的（阻塞的）I/O 操作（比如网络请求、文件读写），它会被操作系统标记为“等待中”，并从 CPU 上移走。
    # CPU 的时间片就会被操作系统调度给其他处于“就绪”状态的线程（无论是同一个进程内的其他线程，还是不同进程的线程）。这种调度是抢占式的，由 OS 全权负责。

# “但是，线程上跑多个协程，反而是为了避免该线程进入等待状态，因为当某个协程遇到高耗时 IO 时，由于协程调用是非阻塞的，故马上另一个协程会拉起运行在线程上。”
    # 完全正确。 这正是异步编程（协程模型）的核心设计目的。
    # 在异步模型中，当一个协程遇到 await 一个耗时的 I/O 操作时，它会「主动让出（yield）控制权」。它并没有“阻塞”线程，
    # 而是告诉事件循环：“我正在等待 I/O，你可以去执行其他任务了。”
    # 事件循环接收到这个信号后，就会立即从其内部的任务队列中选择另一个已准备好执行的协程，并将该协程的执行权交给当前唯一的线程。
    # 这种切换是协作式的（由协程主动让出），并且发生在用户空间，因此非常轻量级和高效。

# “这样的设计下，只有所有协程都遇到高耗时 IO，才会阻塞线程。”
    # 最终理解正确。 更精确地说，是只有当当前线程中没有其他可执行（非等待 I/O）的协程时，这个线程才会进入等待（或空闲）状态。
    # 如果所有正在运行的协程都遇到了 await I/O，那么事件循环就没有其他任务可调度了，此时线程就会被操作系统置于等待状态，直到某个 I/O 操作完成，
    # 唤醒相应的协程，事件循环才能继续。
    # 所以，异步编程的目标就是尽可能地填充线程的空闲时间，避免线程因等待 I/O 而“闲置”，从而最大化单个线程的效率。




# 总结
# 多进程是「独立调度」：每个进程有自己的计算资源、存储资源。
# （宏观上互不干涉）

# 多线程是「抢占调度」：依靠OS调度，当一个线程因 I/O 阻塞时，该线程被动让出计算资源，OS将CPU调度给其他线程。
# （宏观上避免了 CPU 浪费，但每个阻塞的线程本身是暂停的）（调度负担重，因为被调度线程要保存当前状态，以随时抢回来）

# 异步协程是「协作调度」：依靠事件循环和协程的协作，当一个协程因 I/O 挂起时，主动让出控制权给同线程内的其他协程。
# （微观上避免了单个线程的阻塞，最大化了该线程的利用率）（调度负担轻，主动让出控制权，只要响应通知到了，就马上拿回控制权）



# 线程：带状态的复杂任务。带状态意味着可暂停。
# 协程：线程（带状态的复杂任务）里的一个个分解小任务，有些小任务是IO，有些是计算。可主动暂停，直到响应来临
# 将这些分解小任务尽量异步协作，（比如让IO小任务在等待IO时，把能做的计算小任务先做了），保持线程运转不被OS抢占调度
# 协程的异步执行，是依靠
#   1. await(阻塞await所在的主协程），等待await后跟的IO操作，等出了结果再继续执行主协程。）
#            等待期间虽然主协程被阻塞，但会腾出线程，给其他已经提交到事件循环的协程运行。
#            总结就是： await 阻塞 前台协程，腾出线程给后台协程（事件循环等其他已经准备好的协程）
#   2. Task(提交事件循环), 能够并发地开始执行，并且主协程不等待第一个完成就去启动第二个（或处理其他事情），那么
#            需要使用 asyncio.create_task() 来“后台”运行这些协程。asyncio.create_task() 的作用就是把一个协程包装成一个 Task
#           （这也是一个 Future 对象），然后把它提交给事件循环，让它立即开始调度运行，而不会阻塞当前协程。



# asyncio.Future

import asyncio


async def async_long_running_task(name):
    """模拟一个异步耗时的任务"""
    print(f"异步任务 {name} 开始执行...")
    await asyncio.sleep(2) # 异步等待，不阻塞事件循环
    print(f"异步任务 {name} 完成。")
    return f"异步任务 {name} 的结果"

async def main():
    print("主异步程序开始执行...")

    # 创建一个 Future 对象（实际上是由 asyncio.create_task 返回的，Task是Future的子类）
    # asyncio.create_task 启动一个协程并在后台运行，并返回一个 Future
    future1 = asyncio.create_task(async_long_running_task("X"))
    future2 = asyncio.create_task(async_long_running_task("Y"))

    print("主异步程序提交任务后立即继续执行其他代码...")

    # await 会暂停当前协程的执行，直到 Future 完成
    # 但它不阻塞整个事件循环，允许其他协程运行
    result1 = await future1
    print(f"获取 Future X 的结果: {result1}")

    result2 = await future2
    print(f"获取 Future Y 的结果: {result2}")

    print("所有异步任务完成。")


# 运行 asyncio 事件循环
asyncio.run(main())

