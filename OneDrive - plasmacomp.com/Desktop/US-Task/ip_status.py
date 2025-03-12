import ipaddress
import os

ip_with_subnet = ['192.168.29.1/28']
ping_output = []

for ip in ip_with_subnet:
    ip_net = ipaddress.ip_network(ip, strict=False)
    all_hosts = list(ip_net.hosts())
    
    print(f"{ip}\n")
    
    for host in all_hosts:
        ping = os.system(f"ping -n 1 {host}")
        if ping == 0:   
            ping_output.append(f"{host} is active")
        else:
            ping_output.append(f"{host} is not active")
                
with open("ip_status.txt", "w") as ip_status:
    for result in ping_output:
        ip_status.write(f"{result}\n")

print("Ping results saved to ip_status.txt.")
