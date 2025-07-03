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


# await 保证了你当前编写的协程（例如 main）的内部逻辑是按顺序执行的，依赖关系明确。
# 但与此同时，当这个协程暂停等待 I/O 时，它并没有阻塞整个程序或线程，而是给了事件循环机会去调度和执行其他独立的、正在等待 CPU 的协程，从而实现了并发。

async def cook_dish(dish_name, delay):
    print(f"开始烹饪 {dish_name}...")
    await asyncio.sleep(delay)
    print(f"完成烹饪 {dish_name}!")
    return f"{dish_name} 已上桌"

async def kitchen():
    begin = time.time()
    print(f'begin {begin:.2f}')
    
    # 方式一：顺序烹饪 (阻塞)
    await cook_dish("宫保鸡丁", 2)
    await cook_dish("麻婆豆腐", 3)
    print(f'end at {time.time():.2f} with sec {time.time()-begin:.0f}')


if __name__ == "__main__":
    asyncio.run(kitchen())