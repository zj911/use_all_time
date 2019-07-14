import os
for root,dirs,files in os.walk('/mnt/zhaojie'):
    for name in files:
        print(os.path.join(root, name))

#打印出绝对路径
该方法对于每个目录返回一个三元组，(dirpath, dirnames, filenames)。
第一个是路径，第二个是路径下面的目录，第三个是路径下面的非目录（对于windows来说也就是文件）

os.listdir('/mnt/zhaojie')
打印出文件子目录