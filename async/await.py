import asyncio
import time


# async 和 await
# async: 定义一个 协程函数。被定义的协程函数 在调用时，不会立即执行里面的代码，而是返回一个协程对象。
# await 是执行这个 协程对象的方法之一： 
# await

# await 保证当前协程的顺序执行
    # 这个是针对一个特定的协程（比如 main 协程）而言的：
    # 当 main 协程内部遇到 await some_async_operation() 时，它会暂停自身的执行。
    # 它不会跳过这一行，也不会在 some_async_operation() 还没完成的时候就执行 await 后面紧跟着的代码。
    # main 协程会忠实地“等待” some_async_operation() 的结果，然后才继续执行它自己的下一行代码。
    # 所以，从 main 协程自身的视角来看，它内部的 await 表达式是顺序执行的：一个 await 完成，才会进行下一个 await 或后续的代码。

# await 允许事件循环调度其他已准备好的协程
    # 这个是针对整个事件循环而言的，它描述的是宏观上的并发性。
    # 当 main 协程因为 await 而暂停时，它把 CPU 的控制权还给了事件循环。
    # 事件循环并不会闲着。它会立即去检查是否有其他已经处于就绪状态（Ready）的协程（例如，你用 asyncio.create_task() 启动的另一个协程，
    # 或者某个网络请求刚刚收到了数据，其对应的协程可以继续执行了）。
    # 如果有，事件循环就会去执行那些其他的协程。

# 总结 await：
# 只能在协程函数内部使用。
# 用于等待一个异步操作（例如另一个协程、一个 Future 或一个 Task）的完成。
# 当协程遇到 await 时，它会暂停自身的执行，将控制权交还给 asyncio 事件循环。
# 事件循环会趁机去执行其他的协程或处理 I/O 事件。
# 当 await 等待的异步操作完成后，事件循环会把控制权交还给暂停的协程，让它从 await 的地方恢复执行。


# await 保证了你当前编写的协程（例如 main）的内部逻辑是按顺序执行的，依赖关系明确。
# 但与此同时，当这个协程暂停等待 I/O 时，它并没有阻塞整个程序或线程，而是给了事件循环机会去调度和执行其他独立的、正在等待 CPU 的协程，从而实现了并发。

async def cook_dish(dish_name, delay):
    print(f"开始烹饪 {dish_name}...")
    await asyncio.sleep(delay)
    print(f"完成烹饪 {dish_name}!")
    return f"{dish_name} 已上桌"

async def kitchen_order():
    begin = time.time()
    print(f'begin {begin:.2f}')
    
    # 方式一：顺序烹饪 (阻塞)
    await cook_dish("宫保鸡丁", 2)
    await cook_dish("麻婆豆腐", 3)
    print(f'end at {time.time():.2f} with sec {time.time()-begin:.0f}')





# asyncio 库 / Task 类 ----> 构建抽象的 event-loop, 单线程并发执行其内所有ready的协程 when 线程资源空出
# asyncio.create_task( coroutine object ) ---> 立即返回 task object 并注册协程到 event-loop
# 一旦 await 阻塞当前（前台）主协程，event-loop中注册的协程立即获得线程资源，以运行

# asyncio.gather(*coros_or_futures)
# 用于并发地运行多个协程或 Future，并等待它们全部完成。
# 它会按照传入的顺序, 返回每个协程的结果（即使它们完成的顺序不同）。
# 如果其中任何一个协程失败，gather 会立即抛出该异常，其他协程可能继续运行或被取消（取决于 return_exceptions 参数）。
# 用法举例
# async def main_concurrent():
#     print("主协程开始 (并发下载)")

#     # 使用 create_task 启动多个协程，它们会并发运行
#     task1 = asyncio.create_task(download_data("http://example.com/data1", 3)) # 3秒
#     task2 = asyncio.create_task(download_data("http://example.com/data2", 1)) # 1秒
#     task3 = asyncio.create_task(download_data("http://example.com/data3", 2)) # 2秒

#     print("所有下载任务已启动，主协程等待它们完成...\n")

#     # await 可以等待单个 Task，也可以用 asyncio.gather() 等待多个 Task
#     results = await asyncio.gather(task1, task2, task3) # 等待所有任务完成

#     print("\n所有下载任务已完成，结果如下:")
#     for res in results:
#         print(res)


# asyncio.as_completed(coros_or_futures)
# 类似 concurrent.futures.as_completed()，它返回一个迭代器，用于按完成顺序产出已完成的 Task 或 Future。
# 当你需要实时处理完成的任务，而不必等待所有任务时非常有用。
# 用法举例
# async def main_as_completed():
#     print("使用 as_completed 异步获取数据...")
#     tasks = [asyncio.create_task(fetch_item(i)) for i in range(5)]

#     # as_completed 会按完成顺序产出已完成的任务
#     for finished_task in asyncio.as_completed(tasks):
#         result = await finished_task # await 这个已完成的任务，立即获取结果
#         print(f"Received result: {result}")

#     print("所有项目获取完毕。")


async def kitchen_async():
    begin = time.time()
    print(f'begin {begin:.2f}')

    # 方式二：异步烹饪 (阻塞当前协程，让出线程给event-loop中的协程)
    dish2 = asyncio.create_task(  )



if __name__ == "__main__":
    print('await execute: stall main coro, waiting for 空保鸡丁 to cook, since there is no ready coro in event-loop')
    asyncio.run(kitchen_order())

