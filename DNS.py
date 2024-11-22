import ctypes
import subprocess
import sys
import re


def is_admin():
    """检查当前是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def request_admin():
    """直接申请管理员权限"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()


def get_adapter_name():
    """检索网卡名称"""
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            text=True,
        )
        interfaces = re.findall(r"^\s*.*?\s+.*?\s+.*?\s+(以太网|本地连接.*)$", result.stdout, re.I | re.M)
        if interfaces:
            return interfaces[0]
        else:
            print("未找到符合条件的网卡名称，请检查您的网络适配器！")
            sys.exit(1)
    except Exception as e:
        print("获取网卡名称时出错:", e)
        sys.exit(1)


def check_in():
    try:
        result = subprocess.run(
            "ipconfig /all",
            shell=True,
            capture_output=True,
            text=True,
        )
        output_str = result.stdout
        re_str_ip = re.findall(r"172.\d+.\d+.\d+", output_str)
        if len(re_str_ip):
            return "你现在处于财务网"
        else:
            return "你现在处于外网"
    except Exception as e:
        print("获取网络信息出错:", e)
        return "未知网络状态"


def set_dns(adapter_name, primary_dns, secondary_dns):
    """设置 DNS 地址"""
    try:
        subprocess.run(
            ["netsh", "interface", "ip", "set", "dns", adapter_name, "static", primary_dns],
            check=True,
        )
        subprocess.run(
            ["netsh", "interface", "ip", "add", "dns", adapter_name, secondary_dns, "index=2"],
            check=True,
        )
        print(f"DNS 已切换为：主 {primary_dns}，备用 {secondary_dns}")
    except subprocess.CalledProcessError as e:
        print("设置 DNS 时出错:", e)


def main():
    while True:
        adapter_name = get_adapter_name()
        print(f"已检索到网卡名称: {adapter_name}")
        print("请选择 DNS 配置:")
        print("1.---互联网")
        print("2.---财务专网")
        choice = input("请输入选项 (1 或 2): ")

        if choice == "1":
            set_dns(adapter_name, "222.222.222.222", "114.114.114.144")
        elif choice == "2":
            set_dns(adapter_name, "172.168.192.222", "172.168.254.31")
        else:
            print("无效选项，请重新运行程序。")


if __name__ == "__main__":
    request_admin()
    print("当前程序已以管理员权限运行。")
    main()
