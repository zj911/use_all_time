压缩：
import os
import tarfile
f = os.getcwd()

with tarfile.open('/home/farmer/PycharmProjects/hpt/my2.tar', "w:gz") as tar:
    tar.add('my1.log', arcname=os.path.basename('my1.log'))
    tar.add('my2.log', arcname=os.path.basename('my2.log'))
tar.close()

解压：
tar = tarfile.open('/home/farmer/PycharmProjects/hpt/my.tar','w')
for i in tar:
    tar.extract(i)
tar.close()