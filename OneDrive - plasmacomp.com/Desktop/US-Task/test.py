import os
import time

folder_path = r'D:\monitoring\moniter_logs'
log_filename = 'log.log'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

log_file_path = os.path.join(folder_path, log_filename)

if not os.path.exists(log_file_path):
    open(log_file_path, 'w').close()

min_log = 0
max_log = 3
last_checked_line = 0

while min_log < max_log:
    with open(log_file_path, 'r') as log_file:
        all_lines = log_file.readlines()
        new_lines = all_lines[last_checked_line:]
        
        if new_lines:
            for line in new_lines:
                print(f"New log entry: {line.strip()}")
            last_checked_line = len(all_lines)
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"New log entry at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    min_log += 1
    time.sleep(2)

print("Script stopped after 3 log entries.")
