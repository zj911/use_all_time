# 装饰器内容
In [7]: def log(func):
   ...:     def wrapper(*args, **kw):
   ...:         print('call %s():'% func.__name__)
   ...:         return func(*args, **kw)
   ...:     return wrapper

In [10]: @log
    ...: def demo():
    ...:     print('name.js')


In [11]: demo()
call demo():
name.js


@log相当于执行了demo = log(demo),先执行装饰器内容，在调用原始函数。

import time
def time_log(func):
    def wrapper(*args, **kw):
        print(time.ctime())
        return func(*args, **kw)
    return wrapper

while True:
    @time_log
    def name():
        print('name.js')
    time.sleep(2)
    name()

print出现正常结果。
