# AWS-Telegram-agent
# 🚀 AI DevOps Telegram Bot (AWS + Ollama)

> Control your AWS infrastructure using natural language from Telegram 🤖☁️

---

## 🔥 Overview

This project is an **AI-powered DevOps agent** that allows you to manage AWS EC2 instances directly from Telegram using natural language commands.

It combines:

* 📲 Telegram Bot (UI)
* ☁️ AWS (EC2 control via boto3)
* 🧠 Ollama (Local LLM for AI understanding)

---

## 🧠 Features

### ⚙️ Instance Management

* Start all instances
* Stop all instances
* Start/Stop specific instance (by ID)
* Filter by instance name tag

### 🌍 Multi-Region Support

* ap-south-1 (Mumbai)
* eu-central-1 (Frankfurt)
* us-east-1 (N. Virginia)

### 🤖 AI Capabilities

* Understand natural language commands
* AI-powered infrastructure summary (`/brief`)
* Fallback parsing (works even if AI fails)

---

## 🏗️ Architecture

```
Telegram → Python Bot → Ollama (AI)
                     → AWS (boto3)
```

---

## ⚡ Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-devops-telegram-bot.git
cd ai-devops-telegram-bot
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install python-telegram-bot boto3 requests
```

---

### 4️⃣ Install Ollama

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama run llama3
```

---

### 5️⃣ Configure AWS

```bash
aws configure
```

---

### 6️⃣ Set Telegram Token

```bash
export BOT_TOKEN="your-telegram-bot-token"
```

---

### 7️⃣ Run the Bot

```bash
python bot.py
```

---

## 📲 Usage

### 🔹 Start Bot

```
/start
```

---

### 🔹 Get Instance Status

```
/status
```

**Example Output:**

```
[ap-south-1] i-123 | running | Boot: 2026-04-16
[eu-central-1] i-456 | stopped | Boot: 2026-04-16
```

---

### 🔹 AI Summary

```
/brief
```

**Example Output:**

```
✅ All regions operational

- ap-south-1: running
- eu-central-1: stopped

⚠️ Recommendation:
Review stopped instances
```

---

### 🔹 Natural Language Commands

```
Start all instances
Stop instance i-123456
Start server prod-web
```

---

## 🎯 Use Cases

* 🔧 DevOps Automation (control AWS from mobile)
* 🤖 AI Agent Demonstration
* 📊 Quick Infrastructure Monitoring
* 💰 Cost Optimization (identify unused resources)
* 🎓 Portfolio / Interview Project

---

## 🧠 How It Works

### 1. User Input

User sends command via Telegram

### 2. AI Processing

Ollama interprets the command

### 3. Fallback Logic

Regex ensures reliability if AI fails

### 4. AWS Execution

boto3 performs EC2 operations

### 5. Response

Bot sends result back to Telegram

---

## 🔐 Security Best Practices

* Restrict allowed Telegram user IDs
* Use IAM Roles instead of access keys
* Add confirmation before terminate actions

---

## 🚀 Future Enhancements

* 📈 CloudWatch metrics (CPU, RAM, Disk)
* 🔔 Alerts & notifications
* 🌐 Web dashboard (Flask)
* ☁️ Serverless deployment (AWS Lambda)
* ⚡ Caching for faster responses

---

## 🎥 YouTube Demo Idea

**Title:**

> Build Your Own AI DevOps Agent (Telegram + AWS + Ollama)

**Demo Flow:**

* Show problem (manual AWS ops)
* Introduce bot
* Live demo (/status, /brief, start/stop)
* Explain architecture
* Show code walkthrough

---

## ⭐ Contribute

Feel free to fork, improve, and contribute!

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

* AWS boto3
* Telegram Bot API
* Ollama (Local LLM)

---

## 💡 Final Thought

> This project is a powerful example of combining **AI + Cloud + Automation** into a real-world DevOps solution.

---

🔥 *If you like this project, don’t forget to star the repo!*
