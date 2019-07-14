map() #批量将迭代对象中的元素进行操作,map('函数','可迭代对象(可以for循环的东西)')；

#通过整个函数实现对列表中数据全部加100操作
li = [11,22,33,44,55]
def f1(args):
    resault = []
    for i in args:
        resault.append(100+i)
    return resault
r = f1(li)
print(r)
#函数方式map使用形式
li = [11,22,33,44,55]
def f2(a):
    return  a+100
resault = map(f2,li)
print(list(resault))
#lambda方式map使用形式
li = [11,22,33,44,55]
resault = map(lambda a:a+100,li)
print(list(resault))

#filter 函数返回True，将元素添加到结果中
#map 将函数返回值添加到结果中