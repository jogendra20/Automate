import os, urllib.request, urllib.parse, json, mimetypes

token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
nexus_url = os.environ.get("NEXUS_URL", "")
nexus_key = os.environ.get("NEXUS_API_KEY", "")
task_desc = os.environ.get("TASK_DESCRIPTION", "")
script_path = os.environ.get("SCRIPT_PATH", "")

# Read exit code
try:
    with open("exit_code.txt") as f:
        exit_code = int(f.read().strip())
except:
    exit_code = 0

# Read output
try:
    with open("output.txt") as f:
        output = f.read(3500).strip()
except:
    output = "No output captured"

if not output:
    output = "Script ran but produced no output"

# Check for image files first
image_extensions = [".png", ".jpg", ".jpeg", ".webp"]
image_file = None
for ext in image_extensions:
    for fname in os.listdir("."):
        if fname.endswith(ext):
            image_file = fname
            break
    if image_file:
        break

def send_message(text):
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)

def send_photo(filepath):
    boundary = "----FormBoundary"
    with open(filepath, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{filepath}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendPhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    urllib.request.urlopen(req)

# If failed and nexus available — send to /fix
if exit_code != 0 and nexus_url and nexus_key and task_desc:
    print("Script failed, sending to Nexus for fix...")
    try:
        script_code = ""
        if script_path and os.path.exists(script_path):
            with open(script_path) as f:
                script_code = f.read()

        fix_payload = json.dumps({
            "prompt": task_desc,
            "error": output,
            "code": script_code,
            "api_key": nexus_key
        }).encode()

        fix_req = urllib.request.Request(
            f"{nexus_url}/fix",
            data=fix_payload,
            headers={"Content-Type": "application/json", "X-API-Key": nexus_key}
        )
        fix_res = urllib.request.urlopen(fix_req, timeout=60)
        fix_data = json.loads(fix_res.read())

        if fix_data.get("triggered"):
            send_message(f"❌ Failed. Nexus analyzing and retrying...\n\nError:\n{output[:500]}")
        else:
            send_message(f"❌ Failed. Fix attempt also failed.\n\nError:\n{output[:500]}")
    except Exception as e:
        send_message(f"❌ Failed + fix request error: {e}\n\nOriginal error:\n{output[:500]}")
    print("Fix request sent")

elif image_file:
    send_photo(image_file)
    print(f"Image {image_file} sent to Telegram")

else:
    text = "📤 Automation Output\n\n" + output
    send_message(text)
    print("Output sent to Telegram")
