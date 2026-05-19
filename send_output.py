import os, urllib.request, urllib.parse, json, mimetypes

token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

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

if image_file:
    # Send as photo
    boundary = "----FormBoundary"
    with open(image_file, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{image_file}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendPhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    urllib.request.urlopen(req)
    print(f"Image {image_file} sent to Telegram")
else:
    # Send text output
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
