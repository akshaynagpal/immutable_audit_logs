import requests
import os
import local_log_file_system as logger
import log_proof

LOG_FILE_NAME="audit.log"

# Example usage
if __name__ == "__main__":
    # initialize multichain
    if log_proof.connect_to_multichain():
        print("Successfully connected to MultiChain")
    else:
        print("Could not establish connection to MultiChain")
    log_data = "User login event at 10:01 AM"


    logger.write_log("AUDIT", log_data)
    log_file_content = logger.read_log_file(LOG_FILE_NAME)
    for log_entry in log_file_content:
        # verify log entry
        log_proof.verify_log_hash(log_entry)
        # tamper log entry
        tampered_log_entry = log_entry+"tampered"
        # verify tampered log entry
        log_proof.verify_log_hash(tampered_log_entry)
    # cleanup
    logger.delete_logs_directory()
