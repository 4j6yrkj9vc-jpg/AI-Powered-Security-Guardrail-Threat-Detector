import re

# 1. Read the log file
with open('server_logs.txt', 'r') as file:
    logs = file.readlines()

failed_attempts = {}

# 2. Parse logs for failed logins
for line in logs:
    if "LOGIN FAILED" in line:
        # Extract the IP address using Regex
        ip_match = re.search(r'IP:\s*([\d\.]+)', line)
        if ip_match:
            ip = ip_match.group(1)
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

# 3. Identify suspicious IPs (> 3 failed attempts)
flagged_ips = {ip: count for ip, count in failed_attempts.items() if count >= 3}

print("=== TECHNICAL INCIDENT REPORT ===")
if flagged_ips:
    for ip, count in flagged_ips.items():
        print(f"[ALERT] Suspicious IP Detected: {ip} ({count} failed login attempts)")
else:
    print("[INFO] No immediate threats detected.")
