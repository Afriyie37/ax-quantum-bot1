from flask import Flask, request
import requests
import os

app = Flask(__name__)

META_TOKEN = os.environ.get("META_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SECRET_PREFIX = "AX-131486-"

def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {META_TOKEN}"}
    data = {"messaging_product": "whatsapp","to": to,"text": {"body": text[:4000]}}
    requests.post(url, headers=headers, json=data)

def ai_quantum_answer(question):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are AX, Afriyie's private quantum physics AI. Brilliant, deep, clear. Explain quantum computing, entanglement, superposition, black holes, AI."},
            {"role": "user", "content": question}
        ]
    }
    res = requests.post(url, headers=headers, json=payload).json()
    return res['choices'][0]['message']['content']

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        sender = msg['from']
        text = msg['text']['body']
        if text.startswith(SECRET_PREFIX) or text.startswith("AX-"):
            clean_q = text.replace(SECRET_PREFIX, "").replace("AX-", "").strip() or "Give me a mind-blowing quantum fact"
            send_whatsapp(sender, "AX detected ✅ Unlocking Quantum Mode...")
            answer = ai_quantum_answer(clean_q)
            send_whatsapp(sender, answer)
        else:
            send_whatsapp(sender, "Hi there! 👋 I'm Afriyie's Bot. For general help, just ask! (Private features locked 🔒)")
    except Exception as e:
        print(e)
    return "ok", 200

@app.route("/webhook", methods=["GET"])
def verify():
    return request.args.get("hub.challenge", "ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
