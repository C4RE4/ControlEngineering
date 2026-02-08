from scapy.all import rdpcap, Dot11
packets = rdpcap("C:\\Users\\86189\\Desktop\\wlan-trace-1.pcap")

# 统计总数据帧数量 (wlan.fc.type == 2)
total_data_frames = [pkt for pkt in packets if pkt.haslayer(Dot11) and pkt.type == 2]

# 统计原始数据帧数量 (wlan.fc.type == 2 且 wlan.fc.retry == 0)
original_transmissions = [pkt for pkt in total_data_frames if not pkt.FCfield.retry]

# 计算重传次数
total_transmissions = len(total_data_frames)
original_transmissions_count = len(original_transmissions)
retransmissions = total_transmissions - original_transmissions_count

# 计算重传比值
if original_transmissions_count > 0:
    retransmission_ratio = retransmissions / original_transmissions_count
else:
    retransmission_ratio = 0  # 防止除零错误

# 输出结果
print(f"总传输次数: {total_transmissions}")
print(f"原始传输次数: {original_transmissions_count}")
print(f"重传次数: {retransmissions}")
print(f"重传比值: {retransmission_ratio:.2f}")