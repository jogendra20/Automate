import os, urllib.request, json

token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

try:
    with open("output.txt") as f:
        output = f.read(3500).strip()
except:
    output = "No output captured"

if not output:
    output = "Script ran but produced no output"

text = "📤 Automation Output\n\n" + output
data = json.dumps({"chat_id": chat_id, "text": text}).encode()
req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=data,
    headers={"Content-Type": "application/json"}
)
urllib.request.urlopen(req)
print("Output sent to Telegram")
