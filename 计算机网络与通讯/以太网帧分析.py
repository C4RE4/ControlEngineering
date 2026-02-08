from scapy.all import rdpcap, Ether

packets = rdpcap("C:\\Users\\86189\\Desktop\\ethernet-trace-1.pcap")

http_get_packet = None
http_response_packet = None

for packet in packets:
    if Ether in packet:
        if http_get_packet is None and packet.haslayer("Raw") and b"GET" in bytes(packet["Raw"]):
            http_get_packet = packet

        if http_response_packet is None and packet.haslayer("Raw") and b"HTTP/1.1 200 OK" in bytes(packet["Raw"]):
            http_response_packet = packet

        if http_get_packet and http_response_packet:
            break

if http_get_packet:
    dest_mac_get = http_get_packet[Ether].dst
    src_mac_get = http_get_packet[Ether].src
    ethertype_get = hex(http_get_packet[Ether].type)
else:
    dest_mac_get, src_mac_get, ethertype_get = None, None, None

if http_response_packet:
    dest_mac_response = http_response_packet[Ether].dst
    ethertype_response = hex(http_response_packet[Ether].type)
else:
    dest_mac_response, ethertype_response = None, None

print(f"1. 目的 MAC 地址: {dest_mac_get}")
print(f"2. 帧类型字段: {ethertype_get}")
print(f"3. 源 MAC 地址: {src_mac_get}")
print(f"4. 响应的目的 MAC 地址: {dest_mac_response}")
print(f"5. 响应的帧类型字段: {ethertype_response}")
