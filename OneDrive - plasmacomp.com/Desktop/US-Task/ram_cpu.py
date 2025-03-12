import psutil
import time

while True:
    
    #print("----x----x----x----x----x----x----x----x")
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

    ram = psutil.virtual_memory()
    print(f"RAM Usage: {ram.percent}%")

    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}%")
    
    print("----x----x----x----x----x----x----x----x")
    
    time.sleep(2)

    
