import os
from scp import SCPClient
import paramiko
import sys
import time
import json
import multiprocessing
import datetime
import math

def run(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

ssh_list = ['172.16.231.210','172.16.231.211','172.16.231.212']
# ssh_list = ['172.16.231.210']
ssh_port = '22'
ssh_name = 'root'
ssh_pass= 'admin123'

# http info
source_video = "http://172.16.15.31/video/kakao/kakao_sample.mp4"


def dict_get(dict1, objkey, default):
    tmp = dict1
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            if type(v) is dict:
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
            if type(v) is list:
                ret = dict_get(v[0], objkey, default)
                if ret is not default:
                    return ret
    return default


# http link
def http_link(ssh_server):
    client = get_connect(ssh_server)
    print('\n*******init http link...\n')
    # create share http link
    stdin, stdout, stderr = client.exec_command(str('mount -o remount, rw /;ln -s /tmp/seg/ /D0/'))
    client.close()


def get_connect(ssh_server):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ssh_server, port=ssh_port, username=ssh_name, password=ssh_pass)
    return client

def cmd_transcode(ssh_server, cmdline, thread_index, output_url):
    thread_time1  = datetime.datetime.now()
    # init_mount(ssh_server)
    http_link(ssh_server)
    client = get_connect(ssh_server)    
    print('\nThe command to be executed is: \n' + cmdline)
    stdin, stdout, stderr = client.exec_command(cmdline)
    print('\n******* Start Encoding...\n')
    for line in stdout:
        pass
    thread_time2  = datetime.datetime.now()
    print("ssh_server:{} thread {}: running transcode time {}".format(ssh_server ,thread_index, thread_time2-thread_time1))
    # wget this output file 
    wget_cmd = "wget {}".format(output_url)
    print(wget_cmd)
    cc = run(wget_cmd + ' -o /dev/null')
    client.close()


# define time
def time_cal(time_basic, t):
    time_list = time_basic.split(':')
    time_s = int(time_list[2]) + t
    time_m = int(time_list[1])
    time_h = int(time_list[0])
    if time_s >= 60:
        time_m = int(time_list[1]) + 1
        time_s = time_s - 60
    if time_m >= 60:
        time_h = int(time_list[0]) + 1
        time_m = time_m - 60
    time_start = "{}:{}:{}".format('%02d' % time_h, '%02d' % time_m, '%02d' % time_s)
    return time_start


source_video_without_http = source_video.split('/')[-1]
test_file_folder = source_video_without_http.split('.')[0]

if os.path.exists(test_file_folder):
    pass
else:
    os.mkdir(test_file_folder)
os.chdir(test_file_folder)

time1  = datetime.datetime.now()
# get video duration
info_cmdline = 'ffprobe -v quiet -print_format json -show_format -select_streams v:0 -show_streams -i {}'.format(source_video)
video_info_str = run(info_cmdline)
video_info_json = json.loads(video_info_str)
video_duration = round(eval(dict_get(video_info_json, 'duration', None)))

# split duration
duration_split = math.ceil(video_duration / len(ssh_list))
strart_base = '00:00:00'

# get node cmdline
node_cmd = []
out_put_link = []
for index, value in enumerate(ssh_list):
    index_num = index + 1
    time_base = index_num * duration_split
    output_name = source_video_without_http.split('.')[0] + '_' + str(index_num) + '.ts'
    cmdline = "cd /tmp/seg; pwd; ffmpeg2 -y -ss {} -i {} -t {} -c:v v205h264 -b:v 3000k -c:a copy {};sync".format(strart_base, source_video, duration_split, output_name)
    # cmdline = "cd /tmp/seg; pwd; ffmpeg -y -ss {} -i {} -t {} -c copy  {};sync".format(strart_base, source_video, duration_split, output_name)
    node_cmd.append(cmdline)
    out_put_link.append("http://{}:8890/seg/".format(value) + output_name)
    strart_base = time_cal(strart_base, duration_split)
time2  = datetime.datetime.now()
print("before thread run {}".format(time2-time1))


# thread pool ssh_list number to run 
threads = []
p = multiprocessing.Pool(processes=len(ssh_list))
results = []
# every server get a thread
for index, server in enumerate(ssh_list):
    result = p.apply_async(cmd_transcode, (server, node_cmd[index], index, out_put_link[index]))
    results.append(result)
p.close()
p.join()

for i in results:
    # print(i.get())
    pass

time3  = datetime.datetime.now()
print("total thread run {}".format(time3-time2))

# transcode finish then concat
c = run("sync")

video_ts_list = [ i for i in os.listdir(os.getcwd()) if i.endswith('ts')]
video_ts_list.sort()
concat_videos = "concat:" + '|'.join(video_ts_list)
concat_video_name = source_video_without_http.split('.')[0] + '_concat.mp4'
concat_cmdline = 'ffmpeg -y -i "{}"  -threads 0 -f mp4 -codec copy {}'.format(concat_videos, concat_video_name)
print(concat_cmdline)
c = run(concat_cmdline)
time4 = datetime.datetime.now()
print("total concat run {}".format(time4-time3))
time5  = datetime.datetime.now()
print("total transcode run {}".format(time5-time1))