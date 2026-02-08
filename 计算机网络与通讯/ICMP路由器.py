from scapy.all import *

# 读取 pcap 文件
packets = rdpcap("D:\计算机网络与通讯\etrace-2.pcap")

# 过滤 ICMP 差错报告数据包（类型 3: 目标不可达, 类型 11: TTL 超时）
icmp_errors = [pkt for pkt in packets if ICMP in pkt and pkt[ICMP].type in [3, 11]]

# 分析 ICMP 差错报告数据包
for pkt in icmp_errors:
    print("=" * 50)
    print(f"Packet: {pkt.summary()}")
    
    # ICMP 类型和代码
    icmp_type = pkt[ICMP].type
    icmp_code = pkt[ICMP].code
    print(f"ICMP Type: {icmp_type}, Code: {icmp_code}")
    
    # TTL 字段
    if IP in pkt:
        ttl = pkt[IP].ttl
        print(f"TTL: {ttl} (Time to Live, 表示数据包最多可经过的路由器数量)")
    
    # 原始IP头信息（ICMP 差错数据包中包含导致错误的原始 IP 头）
    if Raw in pkt:
        raw_data = pkt[Raw].load
        print(f"Raw Data (first 20 bytes of original IP header): {raw_data[:20].hex()}")

print(f"Total ICMP error packets found: {len(icmp_errors)}")
