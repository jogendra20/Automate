import os, urllib.request, urllib.parse, json, mimetypes
from datetime import datetime

token     = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_id   = os.environ.get("TELEGRAM_CHAT_ID", "")
nexus_url = os.environ.get("NEXUS_URL", "")
nexus_key = os.environ.get("NEXUS_API_KEY", "")
task_desc = os.environ.get("TASK_DESCRIPTION", "")
script_path = os.environ.get("SCRIPT_PATH", "")
script_name = os.environ.get("SCRIPT_PATH", "").replace("scripts/","").replace(".py","")
run_id    = os.environ.get("GITHUB_RUN_ID") or os.environ.get("RUN_ID", script_name or datetime.now().strftime("%Y%m%d_%H%M%S"))

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

# Check for image files
image_extensions = [".png", ".jpg", ".jpeg", ".webp"]
image_file = None
for ext in image_extensions:
    for fname in os.listdir("."):
        if fname.endswith(ext):
            image_file = fname
            break
    if image_file:
        break

def nexus_post(endpoint, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{nexus_url}/{endpoint}",
        data=data,
        headers={"Content-Type": "application/json", "X-API-Key": nexus_key}
    )
    try:
        res = urllib.request.urlopen(req, timeout=10)
        return json.loads(res.read())
    except Exception as e:
        print(f"Nexus {endpoint} failed: {e}")
        return {}

# Store output in Nexus so UI can poll it
if nexus_url and nexus_key and run_id:
    image_b64 = None
    if image_file:
        import base64
        with open(image_file, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

    nexus_post("store-output", {
        "run_id": run_id,
        "status": "done" if exit_code == 0 else "failed",
        "output": output,
        "exit_code": exit_code,
        "image_b64": image_b64,
        "task": task_desc,
        "timestamp": datetime.now().isoformat()
    })
    print(f"Output stored for run_id: {run_id}")

# If failed — send to /fix
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
            "code": script_code
        }).encode()

        fix_req = urllib.request.Request(
            f"{nexus_url}/fix",
            data=fix_payload,
            headers={"Content-Type": "application/json", "X-API-Key": nexus_key}
        )
        fix_res = urllib.request.urlopen(fix_req, timeout=60)
        fix_data = json.loads(fix_res.read())
        print("Fix request sent:", fix_data.get("triggered"))
    except Exception as e:
        print(f"Fix request error: {e}")

print("Done.")
