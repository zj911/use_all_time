列表分割：
l = [i for i in range(15)]
print(l)
n = 3 #大列表中几个数据组成一个小列表
print([l[i:i + n] for i in range(0, len(l), n)])