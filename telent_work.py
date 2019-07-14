# 匹配字符进行输入指令
import telnetlib
import time

def telnetip(tn, flag ,str_word):
    data = tn.read_until(flag.encode())
    print(data.decode(errors='ignore'))
    tn.write(str_word.encode() + b"\n")
    return data

if __name__ == '__main__':
    # 配置选项
    ips = ['172.16.233.1','172.16.233.3']  # Telnet IP
    username = 'root'  # 登录用户名
    password = 'admin123'  # 登录密码
    cmd = 'ifconfig'

    for ip in ips:
        tn = telnetlib.Telnet(ip, port=23, timeout=50)
        telnetip(tn, "Aupv205 login:", username)
        telnetip(tn, "Password:", password)
        telnetip(tn, "#", cmd)
        telnetip(tn, "#", "exit")
        time.sleep(0.5)
        tn.close()
        time.sleep(0.5)