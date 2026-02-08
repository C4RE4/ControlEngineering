from scapy.all import rdpcap, IP, ICMP

# 读取 pcap 文件
pcap_file = "D:\计算机网络与通讯\ping-trace-1.pcap"  # 请确保文件路径正确
packets = rdpcap(pcap_file)

# 过滤 ICMP 报文
icmp_packets = [pkt for pkt in packets if pkt.haslayer(ICMP)]

# 提取源 IP 和目标 IP
src_ip = icmp_packets[0][IP].src if icmp_packets else "N/A"
dst_ip = icmp_packets[0][IP].dst if icmp_packets else "N/A"

# 计算平均往返时间 (RTT)
request_times = {}
rtt_list = []

for pkt in icmp_packets:
    if pkt[ICMP].type == 8:  # ICMP Echo Request
        request_times[pkt[ICMP].seq] = pkt.time
    elif pkt[ICMP].type == 0 and pkt[ICMP].seq in request_times:  # ICMP Echo Reply
        rtt = pkt.time - request_times[pkt[ICMP].seq]
        rtt_list.append(rtt)

avg_rtt = sum(rtt_list) / len(rtt_list) if rtt_list else 0

# 检查一个 Ping 请求数据包
ping_request = next((pkt for pkt in icmp_packets if pkt[ICMP].type == 8), None)
if ping_request:
    req_type = ping_request[ICMP].type
    req_code = ping_request[ICMP].code
    req_checksum = ping_request[ICMP].chksum
    req_id = ping_request[ICMP].id
    req_seq = ping_request[ICMP].seq

# 检查对应的 Ping 响应数据包
ping_reply = next((pkt for pkt in icmp_packets if pkt[ICMP].type == 0), None)
if ping_reply:
    rep_type = ping_reply[ICMP].type
    rep_code = ping_reply[ICMP].code
    rep_checksum = ping_reply[ICMP].chksum
    rep_id = ping_reply[ICMP].id
    rep_seq = ping_reply[ICMP].seq

# 输出分析结果
print(f"源 IP 地址: {src_ip}")
print(f"目标 IP 地址: {dst_ip}")
print(f"平均 RTT: {avg_rtt:.6f} 秒")
print(f"请求包 - 类型: {req_type}, 码号: {req_code}, 校验和: {req_checksum}, 标识: {req_id}, 序列号: {req_seq}")
print(f"响应包 - 类型: {rep_type}, 码号: {rep_code}, 校验和: {rep_checksum}, 标识: {rep_id}, 序列号: {rep_seq}")
