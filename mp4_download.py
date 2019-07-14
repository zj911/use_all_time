import requests
import os

def download_video(url, file_path):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:# 若文件已经存在，则断点续传，设置接收来需接收数据的位置        
            if os.path.exists(file_path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(file_path)
            res = requests.get(url, stream=True, headers=headers)
            print(res.headers)
            content_length = int(res.headers['Content-Length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (os.path.exists(file_path) and os.path.getsize(file_path) >= content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(file_path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(file_path), content_length))
    except Exception as e:
        dic = {'url':url, 'file_path':file_path}
        print(dic)

url = 'http://172.16.15.31/v/Tencent_RD/006-dump_1080p_v300_12_30fps.264'
file_path = '/home/zhaojie/001.mp4'
download_video(url, file_path)