import os
import time

syslog_file_path = '/var/log/syslog'
log_directory = "/root/Python-scripts/monitoring_logs"
log_file_name = 'syslog_monitoring.log'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

monitoring_log_file_path = os.path.join(log_directory, log_file_name)

if os.path.exists(syslog_file_path):
    try:
        with open(syslog_file_path, 'r') as syslog_file:
            all_log_lines = syslog_file.readlines()

        last_20_log_lines = all_log_lines[-20:]

        with open(monitoring_log_file_path, 'w') as monitoring_log_file:
            monitoring_log_file.writelines(last_20_log_lines)

        print("Last 20 lines from syslog:")
        for line in last_20_log_lines:
            print(line.strip())

        print("\nExiting the script after copying and printing the last 20 lines.")
        exit()

    except Exception as error:
        print(f"Error occurred while copying logs: {error}")