from scapy.all import rdpcap, Ether, ARP

# 加载您的 pcap 文件
packets = rdpcap('D:\计算机网络与通讯\ethernet-trace-1.pcap')

arp_request_packet = None
arp_response_packet = None

# 查找第一个 ARP 请求报文和其后的第一个 ARP 响应报文
for i in range(len(packets)):
    if Ether in packets[i] and packets[i][Ether].type == 0x0806 and ARP in packets[i] and packets[i][ARP].op == 1 and arp_request_packet is None:
        arp_request_packet = packets[i]
    elif Ether in packets[i] and packets[i][Ether].type == 0x0806 and ARP in packets[i] and packets[i][ARP].op == 2 and arp_request_packet is not None:
        arp_response_packet = packets[i]
        break  # 找到第一个响应后停止

if arp_response_packet:
    # 6. ARP 操作码字段的位置
    opcode_offset = 14 + 4  # 以太网头 + 硬件类型 + 协议类型 + 硬件地址长度 + 协议地址长度
    print(f"6. ARP 操作码字段的第一个字节与 ARP 报文的第一个字节之间的字节数: 4")
    print(f"   ARP 操作码字段的第一个字节与以太网帧的第一个字节之间的字节数: {opcode_offset}")

    # 7. ARP 操作码字段的值
    arp_opcode_response = arp_response_packet[ARP].op
    print(f"7. ARP 响应报文中的操作码字段的值 (十进制): {arp_opcode_response}")
    print(f"   ARP 响应报文中的操作码字段的值 (十六进制): {hex(arp_opcode_response)}")

    # 8. 对先前 ARP 查询的应答 MAC 地址
    responder_mac = arp_response_packet[ARP].hwsrc
    print(f"8. 对先前 ARP 查询的应答 MAC 地址: {responder_mac}")

    # 9. 包含 ARP 响应报文的以太网帧中的源地址和目标地址
    src_mac_response = arp_response_packet[Ether].src
    dst_mac_response = arp_response_packet[Ether].dst
    print(f"9. 包含 ARP 响应报文的以太网帧中的源 MAC 地址 (十六进制): {src_mac_response}")
    print(f"   包含 ARP 响应报文的以太网帧中的目标 MAC 地址 (十六进制): {dst_mac_response}")

else:
    print("未在文件中找到 ARP 响应报文。")

# 关于第 10 个问题，由于没有实际的数据包 No. 6，我们只能给出一般性解释。
print("\n10. 关于第二个 ARP 查询（数据包 No. 6）没有 ARP 响应的可能原因：")
print("- 目标设备不在线或未响应。")
print("- ARP 请求未到达目标设备。")
print("- 防火墙阻止了 ARP 响应。")
print("- ARP 请求的目标 IP 地址不在本地网络。")
print("- 数据包捕获不完整。")

