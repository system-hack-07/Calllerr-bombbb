from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { background: #0a0a0a; font-family: 'VT323', monospace; color: #00ff9f; }
        .matrix { background: linear-gradient(180deg, rgba(0,255,159,0.03) 0%, transparent 100%); }
        .terminal { font-family: 'VT323', monospace; }
        .scanline { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, transparent 50%, rgba(0,255,159,0.05) 50%); background-size: 100% 4px; pointer-events: none; animation: scan 4s linear infinite; z-index: 10; }
        @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
    </style>
</head>
<body class="overflow-x-hidden">
    <div class="scanline"></div>

    <!-- Top Bar -->
    <div class="fixed top-0 w-full bg-black border-b border-green-500/30 py-2 text-xs flex items-center justify-between px-6 z-50">
        <div class="flex items-center gap-4">
            <span class="text-red-500">●</span>
            <span>SAMARTH_BOMBER_v9.1</span>
        </div>
        <div class="flex items-center gap-6 text-green-400">
            <span>ROOT@VOID:\~$</span>
            <button onclick="toggleMute()" id="mute-btn" class="hover:text-white"><i class="fas fa-volume-up"></i></button>
        </div>
    </div>

    <!-- Header -->
    <header class="pt-20 pb-12 border-b border-green-500/20">
        <div class="max-w-5xl mx-auto px-6 text-center">
            <div class="inline-block bg-red-500/10 text-red-400 px-4 py-1 text-sm mb-6 border border-red-500/30">WARNING: HIGH RISK TOOL</div>
            <h1 class="text-7xl font-bold tracking-widest text-green-400">SAMARTH BOMBER</h1>
            <div class="text-2xl text-green-500/70 mt-2">UNLIMITED • UNTRACEABLE</div>
            <p class="mt-8 max-w-md mx-auto text-green-500/60">Professional SMS, Call & WhatsApp bombing platform.</p>
        </div>
    </header>

    <!-- Main Terminal -->
    <div class="max-w-4xl mx-auto px-6 py-12">
        <div class="glass border border-green-500/30 rounded-xl p-8 bg-black/80">
            <div class="flex justify-between mb-6 text-xs">
                <div class="flex gap-8">
                    <span onclick="switchTab(0)" class="cursor-pointer tab-btn active text-green-400">ATTACK CONSOLE</span>
                    <span onclick="switchTab(1)" class="cursor-pointer tab-btn text-green-400/60">API VAULT</span>
                </div>
                <div id="conn-status" class="text-green-400">CONNECTED • 47 NODES</div>
            </div>

            <!-- Attack Panel -->
            <div id="tab-0">
                <div class="mb-8">
                    <label class="block text-green-500/70 text-sm mb-2">TARGET NUMBER</label>
                    <input id="phone" maxlength="10" class="w-full bg-black border border-green-500/50 focus:border-green-400 outline-none p-6 text-5xl font-mono tracking-widest text-center" placeholder="98XXXXXXXX">
                </div>
                <div class="grid grid-cols-2 gap-6">
                    <button onclick="startAttack()" id="startBtn" class="py-8 bg-green-500 hover:bg-green-400 text-black font-bold text-2xl transition">EXECUTE FLOOD</button>
                    <button onclick="stopAttack()" id="stopBtn" class="hidden py-8 bg-red-600 hover:bg-red-500 text-white font-bold text-2xl transition">TERMINATE</button>
                </div>
                <div class="mt-12 grid grid-cols-3 gap-8">
                    <div class="text-center"><div id="calls" class="text-6xl font-bold text-orange-400">0</div><div class="text-xs text-green-500/50">CALLS</div></div>
                    <div class="text-center"><div id="sms" class="text-6xl font-bold text-sky-400">0</div><div class="text-xs text-green-500/50">SMS</div></div>
                    <div class="text-center"><div id="wa" class="text-6xl font-bold text-purple-400">0</div><div class="text-xs text-green-500/50">WA</div></div>
                </div>
                <div class="mt-12">
                    <div class="text-xs text-green-500/60 mb-4">SYSTEM LOG</div>
                    <div id="logs" class="h-64 overflow-auto text-xs font-mono text-green-400/80 bg-black/90 p-6 border border-green-500/20 rounded-xl"></div>
                </div>
            </div>

            <!-- API Vault Tab -->
            <div id="tab-1" class="hidden">
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <div class="p-4 border border-green-500/30 rounded-xl">TATA CAPITAL [CALL]</div>
                    <div class="p-4 border border-green-500/30 rounded-xl">1MG [CALL]</div>
                    <div class="p-4 border border-green-500/30 rounded-xl">SWIGGY [CALL]</div>
                    <div class="p-4 border border-green-500/30 rounded-xl">LENKART [SMS]</div>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center py-8 text-green-500/30 text-xs border-t border-green-500/10">
        SAMARTH BOMBER • MADE BY SAMARTH 2026
    </footer>

    <audio id="hover" src="https://freesound.org/data/previews/66/66930_931655-lq.mp3" preload="auto"></audio>
    <audio id="launch" src="https://freesound.org/data/previews/387/387186_7258993-lq.mp3" preload="auto"></audio>
    <audio id="stop" src="https://freesound.org/data/previews/131/131660_2391587-lq.mp3" preload="auto"></audio>

    <script>
        let isRunning = false;
        let isMuted = false;
        function play(type) {
            if (isMuted) return;
            const audio = document.getElementById(type);
            audio.currentTime = 0;
            audio.play();
        }

        function toggleMute() {
            isMuted = !isMuted;
            document.getElementById('mute-btn').innerHTML = isMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>';
        }

        function switchTab(n) {
            document.querySelectorAll('[id^="tab-"]').forEach(t => t.classList.add('hidden'));
            document.getElementById('tab-'+n).classList.remove('hidden');
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active', 'text-green-400'));
        }

        async function startAttack() {
            const phone = document.getElementById('phone').value.trim();
            if (phone.length !== 10) return alert("INVALID TARGET");
            play('launch');
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
            play('stop');
            document.getElementById("startBtn").classList.remove("hidden");
            document.getElementById("stopBtn").classList.add("hidden");
        }

        function pollStatus() {
            if (!isRunning) return;
            fetch("/status").then(r => r.json()).then(d => {
                document.getElementById("calls").textContent = d.stats.Call || 0;
                document.getElementById("sms").textContent = d.stats.SMS || 0;
                document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                document.getElementById("logs").innerHTML += `<div>> Cycle ${d.cycles} executed</div>`;
                document.getElementById("logs").scrollTop = 9999;
                setTimeout(pollStatus, 900);
            });
        }

        document.querySelectorAll('button').forEach(b => b.addEventListener('mouseenter', () => play('hover')));
    </script>
</body>
</html>
    """
    return html

@app.post("/start")
async def start(phone):
    return {"status": "success"}

@app.post("/stop")
async def stop():
    return {"status": "success"}

@app.get("/status")
async def status():
    return {"stats": {"Call": 23, "SMS": 87, "WhatsApp": 12}, "cycles": 14, "logs": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
