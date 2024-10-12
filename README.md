# immutable_audit_logs
Ensuring integrity and immutability of audit logs using blockchain

## How to run on UNIX based systems
### Tested on the following system config
- Docker Desktop v4.34.2 (167172)
- Docker Compose: v2.29.2-desktop.2

### Steps
````
git clone https://github.com/akshaynagpal/immutable_audit_logs.git
cd immutable_audit_logs
docker compose up --build
````
should produce the following output
````
....
python-app       | Stream 'stream1' is available.
python-app       | Successfully connected to MultiChain
python-app       | Attempting to store log hash on blockchain
python-app       | Log hash stored on blockchain. txid: b0a80e00b094c23bee7aeea1cba5ee375870a17211464f865b37d46620eef943
python-app       | Log written to /app/logs/audit.log
python-app       | Content of audit.log:
python-app       | ['b0a80e00b094c23bee7aeea1cba5ee375870a17211464f865b37d46620eef943-2024-10-12 07:13:55-AUDIT-User login event at 10:01 AM']
python-app       | Log verified: No tampering detected.
python-app       | Log tampered!
python-app       | Logs directory /app/logs and all its contents have been deleted.
python-app exited with code 0
````
