import os
import gzip

log_folder = "/root/Python-scripts/monitoring_logs/syslog_monitoring.log"

# Check if the log file exists
if os.path.isfile(log_folder):
    compressed_file = log_folder + '.gz'

    try:
        # Open the original log file and the compressed file
        with gzip.open(compressed_file, 'wb') as compressed:
            with open(log_folder, 'rb') as original_file:
                # Write the contents of the log file to the compressed file
                compressed.write(original_file.read())

        print(f"Compressed: {log_folder} to {compressed_file}")

    except Exception as e:
        print(f"Error during compression: {e}")
else:
    print(f"Log file {log_folder} does not exist.")