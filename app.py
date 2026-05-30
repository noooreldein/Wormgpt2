import requests
from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

MY_OWNER = "@n_7_3_a"
MY_CHANNEL = "https://t.me/n_7_3_a_2"
MY_NAME = "Noor"

DEVELOPER_COMPANY = "𝑿 𝑫𝑬𝑽𝑺"
DEVELOPER_NAME = "𝐍𝐎𝐔𝐑 {s} 𝑿 𝑫𝑬𝑽𝑺 {𝑳𝑬𝑨𝑫𝑬𝑹}"
DEVELOPER_USERNAME = "@n_7_3_a_1"

ORIGINAL_API = "https://worm-gpt-opal.vercel.app/chat"

IDENTITY_QUESTIONS = [
    "من صنعك", "مين صنعك", "من انت", "من أنت", "مين انت", "مين أنت",
    "من برمجك", "مين برمجك", "من مطورك", "مين مطورك", "من اللي صنعك",
    "من اللي برمجك", "مين اللي صنعك", "مين اللي برمجك", "من صنع هذا البوت",
    "مين صنع هذا البوت", "من اللي عملك", "مين اللي عملك", "من صنعك يا بوت",
    "مين صنعك يا بوت", "انت تبع مين", "أنت تبع مين", "انت تبع من",
    "أنت تبع من", "لمن انت", "لمن أنت", "شركة ايه اللي عاملاك", "تابع لايه",
    "انتا بتاع مين"
]

def is_identity_question(text):
    text = text.strip().lower()
    for q in IDENTITY_QUESTIONS:
        pattern = re.sub(r'[^\w\s]', '', q).lower()
        if pattern in text:
            return True
    return False

def identity_response():
    return {
        "status": "success",
        "reply": (
            f"أنا ذكاء اصطناعي تابع لشركة {DEVELOPER_COMPANY}، "
            f"للمطور {DEVELOPER_NAME}، "
            f"يوزر مطوري {DEVELOPER_USERNAME}"
        ),
        "owner": MY_OWNER,
        "channel": MY_CHANNEL,
        "developer": MY_NAME
    }

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "WormGPT API by Noor"})

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('q', '')
    if not question:
        return jsonify({"status": "error", "message": "استخدم q=سؤالك"}), 400

    if is_identity_question(question):
        return jsonify(identity_response())

    try:
        resp = requests.get(ORIGINAL_API, params={'q': question}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    data['owner'] = MY_OWNER
    data['channel'] = MY_CHANNEL
    data['developer'] = MY_NAME
    return jsonify(data)

# مفيش تشغيل محلي (Vercel بيستدعي app تلقائي)
