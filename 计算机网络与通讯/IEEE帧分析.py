from scapy.all import rdpcap, Dot11
from collections import Counter

# 读取 PCAP 文件
pcap_file = "C:\\Users\\86189\\Desktop\\wlan-trace-1.pcap"  # 确保文件路径正确
packets = rdpcap(pcap_file)

# 统计 AP 发送的信标帧（Beacon）
ap_beacon_count = Counter()

# 统计数据帧、控制帧、管理帧的数量和子类型
data_frames = []
control_frames = []
management_frames = []

# 统计重传次数
total_transmissions = 0
original_transmissions = 0

# 关联请求/响应帧 和 探测请求/响应帧 的类型和子类型
assoc_req_type, assoc_req_subtype = None, None
assoc_resp_type, assoc_resp_subtype = None, None
probe_req_type, probe_req_subtype = None, None
probe_resp_type, probe_resp_subtype = None, None

# 遍历数据包
for packet in packets:
    if packet.haslayer(Dot11):
        dot11 = packet[Dot11]
        
        # 统计 Beacon 帧（管理帧，子类型 8）
        if dot11.type == 0 and dot11.subtype == 8:
            ap_beacon_count[dot11.addr2] += 1

        # 统计数据帧
        elif dot11.type == 2:
            data_frames.append(dot11.subtype)
            total_transmissions += 1
            if not dot11.FCfield.retry:
                original_transmissions += 1

        # 统计控制帧
        elif dot11.type == 1:
            control_frames.append(dot11.subtype)

        # 统计管理帧
        elif dot11.type == 0:
            management_frames.append(dot11.subtype)

            # 记录关联请求/响应帧和探测请求/响应帧
            if dot11.subtype == 0:  # 关联请求
                assoc_req_type, assoc_req_subtype = dot11.type, dot11.subtype
            elif dot11.subtype == 1:  # 关联响应
                assoc_resp_type, assoc_resp_subtype = dot11.type, dot11.subtype
            elif dot11.subtype == 4:  # 探测请求
                probe_req_type, probe_req_subtype = dot11.type, dot11.subtype
            elif dot11.subtype == 5:  # 探测响应
                probe_resp_type, probe_resp_subtype = dot11.type, dot11.subtype

# 计算最活跃的 AP
most_active_ap, most_active_ap_count = ap_beacon_count.most_common(1)[0] if ap_beacon_count else (None, 0)

# 统计子类型
data_subtype_count = Counter(data_frames)
control_subtype_count = Counter(control_frames)
management_subtype_count = Counter(management_frames)

# 计算重传比率
retry_ratio = (total_transmissions - original_transmissions) / original_transmissions if original_transmissions else None

# 输出结果
print(f"最活跃的 AP: {most_active_ap}, BSS ID: {most_active_ap}")
print(f"数据帧总数: {len(data_frames)}")
print(f"数据帧子类型统计: {data_subtype_count}")
print(f"最常见的数据帧子类型: {data_subtype_count.most_common(1)}")
print(f"控制帧总数: {len(control_frames)}")
print(f"控制帧子类型统计: {control_subtype_count}")
print(f"最常见的控制帧子类型: {control_subtype_count.most_common(1)}")
print(f"管理帧总数: {len(management_frames)}")
print(f"管理帧子类型统计: {management_subtype_count}")
print(f"最常见的管理帧子类型: {management_subtype_count.most_common(1)}")
print(f"重传比率: {retry_ratio:.2%}")
print(f"关联请求类型/子类型: {assoc_req_type}/{assoc_req_subtype}")
print(f"关联响应类型/子类型: {assoc_resp_type}/{assoc_resp_subtype}")
print(f"探测请求类型/子类型: {probe_req_type}/{probe_req_subtype}")
print(f"探测响应类型/子类型: {probe_resp_type}/{probe_resp_subtype}")
