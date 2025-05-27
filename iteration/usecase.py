from collections.abc import Iterable, Iterator


# 自定义实现 可迭代对象 和 迭代器


# Python 里为什么要分开定义 可迭代对象 和 迭代器?

# 1. 清晰的职责划分
# 可迭代对象（Iterable）：负责管理和存储数据，提供一种方法来生成迭代器。可迭代对象通常实现了__iter__方法，该方法返回一个迭代器。
# 迭代器（Iterator）：负责遍历数据，提供一种方法来获取下一个元素。迭代器通常实现了__next__方法，该方法返回下一个元素，如果没有更多元素则抛出StopIteration异常。


# 定义一个 可迭代对象 Iterable:
# 1 负责管理和存储数据
# 2 提供 __iter__() 方法. 该方法要返回一个 迭代器 Iterator, 供 iter 函数使用


class Color(object):

    # __init__()方法负责管理和存储数据
    def __init__(self, mode):
        self.index = -1
        self.mode = mode
        self.colors = ['red', 'white', 'black', 'green']

    # __iter__()方法要返回一个迭代器 Iterator
    # 可以有不同的实现__iter__()的办法

    def __iter__(self):
        if self.mode == 'singular':
            return self.__iter_singular__()
        else:
            return self.__iter_nonsingular__()

    # 实现办法1: 直接返回self自己. 因为只要 self 也实现了 __next__() 方法, 那么 self 自己就是一个Iterator 实例. __iter__()方法返回一个Iterator
    # 但是这种实现，用 iter 函数调用, 只会返回同一个 Iterator. 这种属性被归纳为 iter的singularity性质. 故而:
    # 一个 Iterable实例 只能生成 一个独立的 Iterator实例, 意味着同一个可迭代对象 只可以被 遍历一次. 同一个 可迭代对象, 多次调用iter()函数只会有同一个迭代器。
    def __iter_singular__(self):
        return self
    
    # 实现办法2: 返回一个 新的 Iterator 实例. 所以我们需要先定义一个 Iterator 类, 称为 订制迭代器类.
    # 这个 订制迭代器类 可以是 有iter的singularity性质的, 因为 是通过实例化, 来得到不同的 Iterator实例, 而非通过 iter函数
    # 每次实例化 订制迭代器类得到 订制迭代器实例, 它们是独立的 Iterator实例.
    def __iter_nonsingular__(self):
        return ListIterator(self.colors)
    

    # 使用内置函数next对迭代器进行遍历. 在这个过程中，是在调用迭代器的__next__方法,
    # 内置函数的作用是返回迭代器的下一个值，这个功能的实现，我们需要放在__next__方法
    def __next__(self):
        # 每调用一次 __next__()方法, self.index + 1
        self.index += 1
        # 界定遍历结束的边界
        if self.index >= len(self.colors):
            raise StopIteration
        # 返回每次遍历应该返回的元素
        return self.colors[self.index]





# 订制Iterator类 (订制迭代器)
class ListIterator:
    def __init__(self, lst):
        self.lst = lst
        self.index = -1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        if self.index >= len(self.lst):
            raise StopIteration
        return self.lst[self.index]




## 测试 singular 模式


# 实例化一个 Iterable
color_iterable = Color(mode='singular')
# iter 得到 Iterator
color_iter1 = iter(color_iterable)
color_iter2 = iter(color_iterable)
# 遍历, 看是否是同一个 迭代器
print(f'singular mode on color_iter1 {next(color_iter1)}')
print(f'singular mode on color_iter2 {next(color_iter2)}')




## 测试 non-singular 模式


# 实例化一个 Iterable
color_iterable = Color(mode='non-singular')
# iter 得到 Iterator
color_iter1 = iter(color_iterable)
color_iter2 = iter(color_iterable)
# 遍历, 看是否是同一个 迭代器
print(f'non-singular mode on color_iter1 {next(color_iter1)}')
print(f'non-singular mode on color_iter2 {next(color_iter2)}')