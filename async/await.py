import asyncio
import time

async def cook_dish(dish_name, delay):
    print(f"开始烹饪 {dish_name}...")
    await asyncio.sleep(delay)
    print(f"完成烹饪 {dish_name}!")
    return f"{dish_name} 已上桌"

async def kitchen():
    print(f'begin {time.time():.2f}')
    # 方式一：顺序烹饪 (阻塞)
    await cook_dish("宫保鸡丁", 2)
    await cook_dish("麻婆豆腐", 1)
    print(f'begin {time.time():.2f}')
    # 方式二：并发烹饪 (非阻塞)
    # 怎么让它们同时开始做呢？这就需要 Task 了！
    # pass # 这里需要 Task


if __name__ == "__main__":
    asyncio.run(kitchen())