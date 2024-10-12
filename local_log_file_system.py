import os
from datetime import datetime
import shutil
import log_proof

LOG_FILE_NAME="audit.log"
AUDIT_LOG_CATEGORY = "AUDIT"

# Write logs to a file based on category
def write_log(category, message):
    log_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{category}-{message}"
    chain_txn_id = None
    if category == AUDIT_LOG_CATEGORY:
        # write audit log hash on blockchain
        chain_txn_id = log_proof.store_log_hash(category, log_data)

    log_file = os.path.join(_get_log_directory(), LOG_FILE_NAME)
    # Prepend the log message with txid from blockchain
    with open(log_file, 'a') as f:
        log_entry = f"{chain_txn_id}-{log_data}"
        f.write(log_entry)
    
    print(f"Log written to {log_file}")

# Read the content of a log file
def read_log_file(log_file_name):
    log_file_abs_path = os.path.join(_get_log_directory(), log_file_name)
    if os.path.exists(log_file_abs_path):
        with open(log_file_abs_path, 'r') as f:
            content = f.readlines()
        print(f"Content of {log_file_name}:\n{content}")
        return content
    else:
        print(f"Log file {log_file} does not exist.")
        return None

# Delete the entire logs directory and its contents
def delete_logs_directory():
    log_dir = _get_log_directory()
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
        print(f"Logs directory {log_dir} and all its contents have been deleted.")
    else:
        print(f"Logs directory {log_dir} does not exist.")

# Create the log directory relative to the Python file's directory
def _get_log_directory():
    # Get the directory where the Python file is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Create a 'logs' directory relative to the script's location
    log_dir = os.path.join(script_dir, "logs")
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return log_dir