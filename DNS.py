# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import ctypes
def network():
    os.popen("netsh interface ip set dns 以太网 source=static addr=222.222.222.222")
    os.popen("netsh interface ip add dns 以太网 addr=222.222.202.202 index=2")
    os.popen("netsh interface ip set dns 本地连接 source=static addr=119.29.29.29")
    os.popen("netsh interface ip add dns 本地连接 addr=8.8.8.8 index=2")
def caiwu_network():
    os.popen("netsh interface ip set dns 以太网 source=static addr=172.168.192.222")
    os.popen("netsh interface ip add dns 以太网 addr=172.168.254.31 index=2")
    os.popen("netsh interface ip set dns 本地连接 source=static addr=172.168.192.222")
    os.popen("netsh interface ip add dns 本地连接 addr=172.168.254.31 index=2")



def DNS():
    cmd = 'ipconfig/all'
    res = os.popen(cmd)
    output_str = res.read()  # 获得输出字符串


    re_str_ip = re.findall(r'172.\d+.\d+.\d+', output_str)#匹配ip
    if len(re_str_ip):
        print("你现在处于财政网")
    else:
        print("你现在处于外网")

    use_in = input("输入 1 切外网 ||  输入 2 切财政专网：") #use是字符串
    if use_in != '1' and use_in != '2':
        print(use_in)
        print("亲爱的你在输入什么？？？")
        time.sleep(5)
        sys.exit()

    if use_in == '1':
        network()
    elif use_in == '2':
        caiwu_network()
    os.popen("ipconfig/flushdns")
    time.sleep(3)

def is_admin():
    """
    检查当前是否具有管理员权限。
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """
    如果不是管理员权限，重新以管理员身份运行当前脚本。
    """
    if not is_admin():
        try:
            # 以管理员身份重新运行当前脚本
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            print(f"无法以管理员权限运行: {e}")
        sys.exit(0)



while True:
    run_as_admin()
    DNS()
