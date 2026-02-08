import socket
import time
import random
from scapy.all import rdpcap, DNSQR
from collections import Counter
import os

# ------------ 用户可自定义设置 ------------
domains = [
     "google.com", "openai.com", "baidu.com", "github.com",
    "stackoverflow.com", "microsoft.com", "apple.com", "amazon.com",
    "wikipedia.org", "python.org", "bing.com", "yahoo.com",
    "tiktok.com", "instagram.com", "linkedin.com", "reddit.com"
]
pcap_file = "dns_capture.pcap"
interval = 2  # DNS 查询间隔 (秒)
duration = 30 * 60  # 总持续时间（秒）30分钟
# -----------------------------------------

def generate_dns_queries():
    print("开始生成 DNS 查询数据，请保持抓包中...")
    repeats = duration // interval
    for i in range(int(repeats)):
        domain = random.choice(domains)
        try:
            socket.gethostbyname(domain)
            print(f"[{i+1}] 查询：{domain}")
        except Exception as e:
            print(f"[{i+1}] 查询失败：{domain} -> {e}")
        time.sleep(interval)
    print("DNS 查询模拟已完成，请关闭抓包并保存为 pcap 文件。")

def analyze_pcap(file_path):
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    print("正在分析 PCAP 文件，请稍候...")
    packets = rdpcap(file_path)
    domain_counter = Counter()

    for pkt in packets:
        if pkt.haslayer(DNSQR):
            domain = pkt[DNSQR].qname.decode().strip('.').lower()
            domain_counter[domain] += 1

    sorted_domains = domain_counter.most_common()

    print("\nDNS 查询域名统计（已忽略大小写）:")
    with open("dns_stats.txt", "w", encoding="utf-8") as f:
        for domain, count in sorted_domains:
            line = f"{domain}: {count} 次"
            print(line)
            f.write(line + "\n")

    print("\n分析完成，结果已保存到 dns_stats.txt")

def main():
    print("="*50)
    print("DNS 模拟抓包 & 分析工具")
    print("="*50)
    print("请选择功能：")
    print("1. 生成 DNS 查询流量（请先启动 Wireshark）")
    print("2. 分析保存好的 PCAP 文件（默认：dns_capture.pcap）")
    choice = input("请输入序号 (1/2): ")

    if choice == "1":
        generate_dns_queries()
    elif choice == "2":
        analyze_pcap(pcap_file)
    else:
        print("输入无效，请重试。")

if __name__ == "__main__":
    main()
