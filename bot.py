import logging
import boto3
import requests
import os
import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = [623957865]  # your Telegram user ID
REGIONS = ["ap-south-1", "eu-central-1", "us-east-1"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= OLLAMA =================
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=30
        )
        return response.json().get("response", "")
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""

import re

def parse_ai(user_input):
    # First try AI
    prompt = f"""
    You are an AWS DevOps assistant.

    Extract intent from: "{user_input}"

    Return ONLY JSON:
    {{
      "action": "status|start|stop|terminate|brief",
      "target": "all|instance_id|name",
      "value": "optional"
    }}
    """

    try:
        res = ask_ollama(prompt)
        logger.info(f"Ollama raw: {res}")
        return json.loads(res)
    except:
        pass

    # 🔥 Fallback logic (VERY IMPORTANT)
    text = user_input.lower()

    # Detect action
    if "start" in text:
        action = "start"
    elif "stop" in text:
        action = "stop"
    elif "terminate" in text:
        action = "terminate"
    elif "status" in text:
        action = "status"
    elif "brief" in text:
        action = "brief"
    else:
        action = "unknown"

    # Detect instance ID
    match = re.search(r"(i-[a-zA-Z0-9]+)", text)

    if match:
        return {
            "action": action,
            "target": "instance_id",
            "value": match.group(1)
        }

    # Detect "all"
    if "all" in text:
        return {
            "action": action,
            "target": "all",
            "value": None
        }

    return {
        "action": action,
        "target": "all",
        "value": None
    }

# ================= AWS =================
def get_instances(region):
    ec2 = boto3.client("ec2", region_name=region)
    return ec2.describe_instances()

def filter_instances(data, target="all", value=None):
    ids = []
    for r in data['Reservations']:
        for i in r['Instances']:
            if target == "all":
                ids.append(i['InstanceId'])
            elif target == "instance_id" and value == i['InstanceId']:
                ids.append(i['InstanceId'])
            elif target == "name":
                for tag in i.get("Tags", []):
                    if tag["Key"] == "Name" and value and value.lower() in tag["Value"].lower():
                        ids.append(i['InstanceId'])
    return ids

def manage_instances(action, ids, region):
    ec2 = boto3.client("ec2", region_name=region)

    if not ids:
        return None

    if action == "start":
        ec2.start_instances(InstanceIds=ids)
    elif action == "stop":
        ec2.stop_instances(InstanceIds=ids)
    elif action == "terminate":
        return f"[{region}] ⚠️ Termination blocked (add confirmation logic)"

    return f"[{region}] {action.upper()} → {', '.join(ids)}"

# ================= STATUS =================
def get_status():
    output = []

    for region in REGIONS:
        ec2 = boto3.client("ec2", region_name=region)
        data = ec2.describe_instances()

        for r in data['Reservations']:
            for i in r['Instances']:
                output.append(
                    f"[{region}] {i['InstanceId']} | {i['State']['Name']} | Boot: {i['LaunchTime']}"
                )

    return "\n".join(output) if output else "No instances found."

# ================= BRIEF =================
def generate_brief():
    status_text = get_status()

    prompt = f"""
    Summarize AWS EC2 status:

    {status_text}

    Keep it SHORT (max 5 lines).
    """

    result = ask_ollama(prompt)

    if not result.strip():
        return "Showing raw status:\n\n" + status_text

    return result

# ================= TELEGRAM =================
def is_authorized(user_id):
    return user_id in ALLOWED_USERS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized ❌")
        return

    await update.message.reply_text(
        "🤖 Multi-Region AWS AI Agent Ready\n\n"
        "Try:\n"
        "/status\n"
        "/brief\n"
        "Start all instances\n"
        "Stop instance i-xxxx\n"
        "Start server my-app"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_status()
    await update.message.reply_text(result)

async def brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating brief...")
    result = generate_brief()
    await update.message.reply_text(result)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized ❌")
        return

    user_input = update.message.text
    await update.message.reply_text("⏳ Processing...")

    ai = parse_ai(user_input)

    action = ai.get("action")
    target = ai.get("target", "all")
    value = ai.get("value")

    results = []

    if action in ["start", "stop", "terminate"]:
        for region in REGIONS:
            data = get_instances(region)
            ids = filter_instances(data, target, value)

            res = manage_instances(action, ids, region)
            if res:
                results.append(res)

        result = "\n".join(results) if results else "No matching instances."

    elif action == "status":
        result = get_status()

    elif action == "brief":
        result = generate_brief()

    else:
        result = "❓ Could not understand."

    await update.message.reply_text(result)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("brief", brief))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
