from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ----------------------------
# 🔑 WhatsApp Cloud API Config
# ----------------------------
ACCESS_TOKEN = "EAAV77U9o0ksBPa9aJX4B2MNEUwI8k3V9FJI8CCkxXsf20F5drW2tLXbM0bfr4mANRIOxINQS0QWRBKSNUj7t0kckFvVeHG8odgBSwWJOECQqdc7QutZBIepQQlweTZB1T1J0ghEfp6ligqT1kgZCCiyKZCGiJdifGifZAaqRGkKEjTVww6vYRIWP8eDU6APJytp5PgM2JZBsd7FgKKREZCDNdKptds3ifLgpM1DHCsftTVmeDYZD"
PHONE_NUMBER_ID = "771929146005620"
VERIFY_TOKEN = "Zain123"

WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

# ----------------------------
# ✅ Webhook Verification
# ----------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verified successfully!")
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Invalid request", 400

# ----------------------------
# 📩 Handle Incoming Messages
# ----------------------------
@app.route("/webhook", methods=["POST"])
def incoming_messages():
    data = request.get_json()
    print("Incoming:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]

        # Send welcome message automatically
        send_welcome_message(sender)

    except Exception as e:
        print("Error processing message:", e)

    return "OK", 200

# ----------------------------
# 📤 Send Template Message
# ----------------------------
def send_template(to, template_name, components=None):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
        }
    }

    if components:
        payload["template"]["components"] = components

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    print("Reply:", response.json())
    return response.json()

# ----------------------------
# 📤 Send Welcome Message
# ----------------------------
def send_welcome_message(to):
    components = [
        {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": "Welcome and congratulations!! This message demonstrates your ability to send a WhatsApp message notification from the Cloud API, hosted by Meta. Thank you for taking the time to test with us."
                }
            ]
        }
    ]
    return send_template(to, "welcome_message", components)

# ----------------------------
# 🚀 Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
