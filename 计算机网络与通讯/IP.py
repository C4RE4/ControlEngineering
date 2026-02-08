from scapy.all import *
import matplotlib.pyplot as plt

# 读取 pcap 文件
packets = rdpcap("D:\计算机网络与通讯\ethernet-trace-1.pcap")

# 选取第10个数据包（索引从0开始）
pkt = packets[9] if len(packets) > 9 else None

if pkt and pkt.haslayer(IP):
    ip_layer = pkt[IP]
    
    # IP 首部字段信息
    ip_fields = {
        "Version & IHL": (0, 1),
        "DSCP & ECN": (1, 1),
        "Total Length": (2, 2),
        "Identification": (4, 2),
        "Flags & Fragment Offset": (6, 2),
        "TTL": (8, 1),
        "Protocol": (9, 1),
        "Header Checksum": (10, 2),
        "Source IP": (12, 4),
        "Destination IP": (16, 4)
    }

    # 获取 IP 头部二进制数据
    ip_raw = bytes(ip_layer)

    # 绘制 IP 头部字段
    fig, ax = plt.subplots(figsize=(10, 2))
    x_pos = 0
    for field, (start, size) in ip_fields.items():
        value_hex = ip_raw[start:start + size].hex().upper()
        ax.barh(0, size, left=x_pos, label=f"{field}: {value_hex}")
        x_pos += size

    ax.set_yticks([])
    ax.set_xticks(range(0, 21))
    ax.set_xticklabels(range(0, 21))
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("字节位置")
    plt.title("IP 头部字段可视化")
    plt.show()

    # 获取源 IP & 目标 IP & 源 MAC & 目标 MAC
    print(f"源 IP: {ip_layer.src}, 目的 IP: {ip_layer.dst}")
    print(f"源 MAC: {pkt.src}, 目的 MAC: {pkt.dst}")

# 分析所有数据包的 Identification 变化情况
id_values = [p[IP].id for p in packets if p.haslayer(IP)]
print(f"IP Identification 字段前 10 个数据包的值: {id_values[:10]}")

# 检测分片
def check_fragmented(pkt):
    """ 判断 IP 数据包是否被分片 """
    if pkt.haslayer(IP):
        flags = pkt[IP].flags
        fragment_offset = pkt[IP].frag
        return flags.MF == 1 or fragment_offset > 0
    return False

fragmented_packets = [p for p in packets if check_fragmented(p)]
print(f"检测到 {len(fragmented_packets)} 个分片的数据包")
