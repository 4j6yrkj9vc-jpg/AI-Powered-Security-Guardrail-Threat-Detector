import time
import json

# Simulated firewall / local blocklist database
blocked_ips = set()

def simulate_firewall_block(ip_address, reason):
    """Simulates updating local firewall rules to eliminate a threat."""
    blocked_ips.add(ip_address)
    print(f"\n[🛡️ ACTIVE DEFENSE TRIGGERED]")
    print(f" -> ACTION: IP {ip_address} added to Firewall Drop Rules.")
    print(f" -> REASON: {reason}")
    print(f" -> STATUS: Threat Neutralized.\n")

# Simulated stream of incoming activity
incoming_traffic = [
    {"ip": "192.168.1.50", "action": "LOGIN_SUCCESS", "user": "alex"},
    {"ip": "45.33.32.156", "action": "LOGIN_FAILED", "user": "admin"},
    {"ip": "45.33.32.156", "action": "LOGIN_FAILED", "user": "admin"},
    {"ip": "45.33.32.156", "action": "PATH_TRAVERSAL_ATTEMPT", "user": "root"},  # Malicious payload
    {"ip": "10.0.0.12", "action": "LOGIN_SUCCESS", "user": "maria"},
]

print("=== STARTING REAL-TIME THREAT HUNTING ENGINE ===")

for event in incoming_traffic:
    ip = event["ip"]
    action = event["action"]
    
    # Check if IP is already eliminated
    if ip in blocked_ips:
        print(f"[BLOCKED TRAFFIC Dropped] Connection attempt from {ip} dropped at firewall.")
        continue

    print(f"[MONITORING] Inspecting packet from {ip} | Action: {action}")
    
    # Threat Detection Logic
    if action == "PATH_TRAVERSAL_ATTEMPT":
        simulate_firewall_block(ip, "Detected malicious web exploit attempt.")
    
    time.sleep(1)

print("=== HUNT COMPLETE ===")
print("Current Firewall Blocklist:", list(blocked_ips))
