from scapy.all import rdpcap, Ether, ARP

# 加载您的 pcap 文件
pcap_file = "D:\计算机网络与通讯\ethernet-trace-1.pcap"  # 确保文件路径正确
packets = rdpcap(pcap_file)

# 查找第一个 ARP 请求报文
arp_request_packet = None
for packet in packets:
    if Ether in packet and packet[Ether].type == 0x0806 and ARP in packet and packet[ARP].op == 1:
        arp_request_packet = packet
        break

if arp_request_packet:
    # 1. 源地址和目的地址
    src_mac = arp_request_packet[Ether].src
    dst_mac = arp_request_packet[Ether].dst

    # 2. 以太网类型字段
    ether_type = arp_request_packet[Ether].type
    
    # 3. ARP 操作码字段的位置
    opcode_offset = 14 + 4  # 以太网头 + 硬件类型 + 协议类型 + 硬件地址长度 + 协议地址长度
    
    # 4. ARP 操作码字段的值
    arp_opcode = arp_request_packet[ARP].op
    
 # 输出结果
    print(f"1. 源 MAC 地址 (十六进制): {src_mac}")
    print(f"   目的 MAC 地址 (十六进制): {dst_mac}")
    print(f"2. 以太网类型字段 (十六进制): {hex(ether_type)}")
    print(f"3. ARP 操作码字段的第一个字节与以太网帧的第一个字节之间的字节数: {opcode_offset}")
    print(f"4. ARP 操作码字段的值 (十进制): {arp_opcode}")
    print(f"   ARP 操作码字段的值 (十六进制): {hex(arp_opcode)}")
    # 5. ARP 报文是否包含发送方的 IP 地址
    if ARP in arp_request_packet and hasattr(arp_request_packet[ARP], 'psrc'):
        print("5. ARP 报文包含发送方的 IP 地址。")
        sender_ip = arp_request_packet[ARP].psrc
        print(f"   发送方的 IP 地址: {sender_ip}")
    else:
        print("5. ARP 报文不包含发送方的 IP 地址 (异常情况).")

else:
    print("未在文件中找到 ARP 请求报文。")