from scapy.all import rdpcap, ICMP, IP

# 读取 pcap 文件
packets = rdpcap("D:\计算机网络与通讯\etrace-2.pcap")

# 筛选 ICMP 数据包
icmp_packets = [pkt for pkt in packets if ICMP in pkt]

# 记录发现的路由器 IP 和 TTL 值
router_ips = set()
ttl_values = []

for pkt in icmp_packets:
    if pkt.haslayer(IP):
        ttl_values.append(pkt[IP].ttl)  # 记录 TTL 值
        router_ips.add(pkt[IP].src)  # 记录路由器 IP

# 按 TTL 递增排序，确定路由顺序
router_ips_sorted = sorted(router_ips, key=lambda ip: ttl_values[icmp_packets.index(pkt)])

# 输出结果
print(f"发现的路由器数量: {len(router_ips_sorted)}")
print("路由器 IP 顺序:", router_ips_sorted)

