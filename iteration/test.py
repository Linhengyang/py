from collections.abc import Iterable, Iterator


class Color(object):

    def __init__(self):
        self.colors = ['red', 'white', 'black', 'green']

    # 仅仅是实现了__iter__ 方法,在方法内部什么都不做
    def __iter__(self):
        pass

Color_obj_1 = Color()
print(isinstance(Color_obj_1, Iterable)) # 验证是否 可迭代对象


class Color(object):

    def __init__(self):
        self.colors = ['red', 'white', 'black', 'green']

    # 仅仅是实现了__iter__ 方法,在方法内部什么都不做
    def __iter__(self):
        pass

    def __next__(self):
        pass

Color_obj_2 = Color()
print(isinstance(Color_obj_2, Iterator)) # 验证是否 迭代器



# 测试 列表 是不是 可迭代对象
print(isinstance([1,2,3], Iterable))

# 测试 列表 是不是 迭代器
print(isinstance([1,2,3], Iterator))

#### 列表 list 不是迭代器 iterator ####




#### iter 内置函数的作用 : iterable ----> iterator, 给一个 可迭代对象, 调用该 可迭代对象的 __iter__()方法, 返回一个迭代器
lst_iter = iter([1,2,3])
print(isinstance(lst_iter, Iterator))



#### next 内置函数的作用 : iterator ----> element in order/stopIteration, 给一个 迭代器, 返回其中的下一个元素/StopIteration
print(next(lst_iter)) # 1
print(next(lst_iter)) # 2
print(next(lst_iter)) # 3
print(next(lst_iter)) # StopIteration


#### 迭代器不能重复使用. 遍历一遍之后, 就无法从头开始遍历. 需要使用 iter 函数, 从可迭代对象重新得到一个 迭代器 ####

#### for 循环 工作原理 ####
#### for element_obj in Iterable 中, 首先使用 iter on Iterable 得到 Iterator, 然后使用 next on Iterator 不断得到 element,
#### 最后捕捉 stopIteration

