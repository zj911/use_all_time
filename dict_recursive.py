# 获得字典递归处理
import re

global optx
optx = -1
global ff_cmd
cmdline = ""

info = {
    "-preset":'3,1', \
    "-rc-lookahead": '3,1', \
    "-bf": '3,1', \
    "-bitrate": '3,1', \
    "-output": '3,1'
    }

def option_cmdline():
    global optx
    optx += 1 
    global cmdline
    tmp_idx = 0
    tmp_len = 0
    if optx == leng:
        optx -= 1
        return 1
    while [i[tmp_idx] for i in options[optx].values()][0] != 'NULL':
        tmp_len = len([i[tmp_idx] for i in options[optx].values()][0])
        value_data = [i[tmp_idx] for i in options[optx].values()][0]
        key_data = [i for i in options[optx].keys()][0]
        cmdline = cmdline + ' ' + key_data + ' ' + value_data
        jas = option_cmdline()
        if jas == 1:
            cmdline_list.append(cmdline.lstrip(' '))
        cmdline = cmdline[0:len(cmdline)-tmp_len-2-len(key_data)]    
        tmp_idx += 1
    tmp_len = len(options) - 1
    optx -= 1
    return 0

options = []
AL = {}
for option ,value in info.items():
    AL[option] = value
    op_value = value + ',NULL'
    op_value = op_value.split(',')
    if option != 'frames':
        options.append({option:op_value})
options.append({'END':'NULL'})
print(options)

cmdline_list = []
leng = len(options) - 1
option_cmdline()
# print(cmdline_list)

print("**************")
for i in cmdline_list:
    print(i)
print(len(cmdline_list))