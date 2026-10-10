import os
import time
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def evaluate_payload_with_ai(payload_text):
    system_instruction = (
        "You are an automated web application firewall and cybersecurity guardrail. "
        "Analyze the provided incoming request payload. "
        "You must respond ONLY with a valid JSON object containing two keys: "
        "'threat_score' (a float between 0.0 and 1.0) and "
        "'reason' (a brief explanation of why)."
    )
    try:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=150,
            system=system_instruction,
            messages=[{"role": "user", "content": f"Analyze this payload: {payload_text}"}]
        )
        return json.loads(response.content[0].text)
    except Exception as e:
        return {"threat_score": 0.0, "reason": "API error."}

LOG_FILE = "live_server.log"

print(f"🛡️ Automated Guardian running... Watching '{LOG_FILE}'")
print("Tip: Open 'live_server.log' in Notepad, type an attack, save it, and watch the terminal!\n")

# Ensure the log file exists to start
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        pass

# Track how many lines we've already processed
with open(LOG_FILE, 'r') as f:
    processed_lines = len(f.readlines())

while True:
    try:
        # Read the file fresh every iteration (avoids Windows file locks)
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            
        # If new lines have been added
        if len(lines) > processed_lines:
            new_lines = lines[processed_lines:]
            
            for line in new_lines:
                payload = line.strip()
                if payload:
                    print(f"[NEW EVENT DETECTED]: {payload}")
                    
                    # Run AI analysis
                    result = evaluate_payload_with_ai(payload)
                    score = result.get("threat_score", 0.0)
                    
                    print(f" -> AI Threat Score: {score}")
                    print(f" -> AI Reasoning: {result.get('reason')}")
                    
                    if score >= 0.8:
                        print(" -> 🚨 AUTOMATED ACTION: Threat neutralized! IP blocked.\n")
                    else:
                        print(" -> ✅ AUTOMATED ACTION: Traffic safe.\n")
            
            # Update our tracker so we don't re-process old lines
            processed_lines = len(lines)
            
    except Exception as e:
        print(f"[ERROR]: {e}")
        
    # Wait 1 second before checking again
    time.sleep(1)
