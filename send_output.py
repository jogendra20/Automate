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



# Auto-skill proposal on success
if exit_code == 0 and token and chat_id and script_path:
    try:
        import re
        import urllib.request as _ur

        domain_match = re.search(r"([\w.-]+\.(com|in|org|net|io|edu|gov)[\w/.-]*)", task_desc or "")
        domain = domain_match.group(0).rstrip("/") if domain_match else None

        if domain:
            gh_raw = "https://raw.githubusercontent.com/jogendra20/Automate/main/skills/playwright.md"
            try:
                skill_res = _ur.urlopen(gh_raw, timeout=8)
                skill_content = skill_res.read().decode()
            except:
                skill_content = ""

            already_exists = domain in skill_content

            if not already_exists and output and output != "Script ran but produced no output":
                script_code = ""
                if script_path and os.path.exists(script_path):
                    with open(script_path) as f:
                        script_code = f.read()

                if nexus_url and nexus_key:
                    nexus_post("store-skill-proposal", {
                        "domain": domain,
                        "task": task_desc,
                        "code": script_code,
                        "output_sample": output[:500],
                        "run_id": run_id
                    })

                msg = (
                    f"New verified recipe ready\n\n"
                    f"Domain: {domain}\n"
                    f"Task: {task_desc[:100]}\n\n"
                    f"Output sample:\n{output[:300]}\n\n"
                    f"Reply:\n"
                    f"approve skill {domain}\n"
                    f"reject skill {domain}"
                )
                tg_payload = json.dumps({
                    "chat_id": chat_id,
                    "text": msg
                }).encode()
                tg_req = _ur.Request(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    data=tg_payload,
                    headers={"Content-Type": "application/json"}
                )
                _ur.urlopen(tg_req, timeout=10)
                print(f"Skill proposal sent for: {domain}")
    except Exception as e:
        print(f"Skill proposal error: {e}")


# Send output to Telegram on success
if exit_code == 0 and token and chat_id and output and output != "Script ran but produced no output":
    try:
        import urllib.request as _ur
        summary = output[:800]
        msg = (
            f"AUTOMATION DONE\n"
            f"Task: {task_desc[:60]}\n"
            f"\n{summary}"
        )
        tg_payload = json.dumps({
            "chat_id": chat_id,
            "text": msg
        }).encode()
        tg_req = _ur.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=tg_payload,
            headers={"Content-Type": "application/json"}
        )
        _ur.urlopen(tg_req, timeout=10)
        print("Output sent to Telegram")
    except Exception as e:
        print(f"Telegram delivery error: {e}")

print("Done.")
