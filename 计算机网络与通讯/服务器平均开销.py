from scapy.all import rdpcap, IP, TCP

packets = rdpcap("C:\\Users\\86189\\Desktop\\lab1-wget-trace.pcap")  

# 服务器 IP 地址
server_ip = "74.125.129.94"

# 以太网头部
ETHERNET_HEADER_SIZE = 14
IP_HEADER_SIZE = 20
TCP_HEADER_SIZE = 20

total_header_size = 0
total_packet_size = 0

for packet in packets:
    if IP in packet and TCP in packet:
        if packet[IP].src == server_ip:  # 服务器发送的数据包
            packet_size = len(packet)  # 数据包总大小
            header_size = ETHERNET_HEADER_SIZE + IP_HEADER_SIZE + TCP_HEADER_SIZE

            total_header_size += header_size
            total_packet_size += packet_size
average_overhead = (total_header_size / total_packet_size) * 100 if total_packet_size > 0 else 0

print(f"服务器到客户端的平均开销：{average_overhead:.2f}%")
