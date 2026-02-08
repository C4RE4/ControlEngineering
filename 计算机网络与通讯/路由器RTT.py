from scapy.all import *
import statistics

# 读取 pcap 文件
packets = rdpcap("D:\计算机网络与通讯\etrace-2.pcap")

# 存储每个 TTL 的 RTT  
rtt_data = {}

# 遍历所有数据包
for pkt in packets:
    if ICMP in pkt and pkt[ICMP].type == 11:  # ICMP Time Exceeded
        ttl = pkt[IP].ttl
        src_ip = pkt[IP].src
        timestamp = pkt.time
        
        if ttl not in rtt_data:
            rtt_data[ttl] = []
        rtt_data[ttl].append((src_ip, timestamp))

# 计算 RTT
rtt_results = {}
for ttl, values in rtt_data.items():
    timestamps = [t[1] for t in values]
    avg_rtt = statistics.mean(timestamps) if timestamps else None
    rtt_results[ttl] = avg_rtt

# 打印每个路由器的平均 RTT
print("TTL\tRouter IP\tAverage RTT (ms)")
for ttl, values in sorted(rtt_data.items()):
    router_ip = values[0][0]  # 取第一个 IP 作为路由器 IP
    avg_rtt = (rtt_results[ttl] - packets[0].time) * 1000  # 转换为 ms
    print(f"{ttl}\t{router_ip}\t{avg_rtt:.2f}")

