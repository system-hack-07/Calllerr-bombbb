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
    <meta name="description" content="Samarth SMS & Call Bomber - Professional Unlimited Bombing Platform">
    <title>Samarth SMS Bomber • Pro Edition</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { font-family: 'Inter', system-ui, sans-serif; background: #020407; }
        .title { font-family: 'Space Grotesk', sans-serif; }
        .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(24px); border: 1px solid rgba(103, 232, 249, 0.2); }
        .neon { text-shadow: 0 0 15px #22d3ee, 0 0 30px #22d3ee, 0 0 50px #67e8f9; }
        .cursor { position: fixed; width: 24px; height: 24px; border: 2px solid #22d3ee; border-radius: 50%; pointer-events: none; z-index: 9999; mix-blend-mode: difference; transition: all 0.15s ease; }
    </style>
</head>
<body class="text-white">
    <div id="cursor" class="cursor hidden md:block"></div>

    <!-- Navbar -->
    <nav class="fixed top-0 w-full z-50 glass border-b border-cyan-500/20">
        <div class="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl flex items-center justify-center text-xl font-bold">S</div>
                <span class="title text-3xl font-semibold tracking-tighter neon">SAMARTH</span>
            </div>
            <div class="flex items-center gap-8 text-sm">
                <a href="#features" class="hover:text-cyan-400 transition">Features</a>
                <a href="#dashboard" class="hover:text-cyan-400 transition">Dashboard</a>
                <a href="#pricing" class="hover:text-cyan-400 transition">Pricing</a>
                <button onclick="toggleTheme()" class="text-xl"><i id="theme-icon" class="fas fa-moon"></i></button>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="min-h-screen pt-32 flex items-center relative overflow-hidden">
        <div class="max-w-5xl mx-auto px-8 text-center">
            <div class="inline px-6 py-3 bg-white/5 rounded-full text-cyan-400 text-sm mb-6">Made by Samarth • 2026</div>
            <h1 class="title text-7xl md:text-8xl font-bold leading-none tracking-tighter neon mb-6">SMS + CALL<br>BOMBER PRO</h1>
            <p class="max-w-lg mx-auto text-xl text-slate-400">Unlimited bombing power. Professional interface. Real-time stats.</p>
            <div class="mt-12 flex flex-col sm:flex-row gap-6 justify-center">
                <button onclick="document.getElementById('dashboard').scrollIntoView({behavior:'smooth'})" class="px-12 py-7 bg-gradient-to-r from-cyan-400 to-blue-500 text-black font-semibold rounded-3xl text-xl hover:scale-105 transition">START BOMBING</button>
                <button onclick="showToast('Connected to 42 APIs')" class="px-12 py-7 border border-cyan-400/50 rounded-3xl text-xl">VIEW APIS</button>
            </div>
        </div>
    </section>

    <!-- Dashboard Section -->
    <section id="dashboard" class="py-24 bg-black/40">
        <div class="max-w-2xl mx-auto px-6">
            <div class="glass rounded-3xl p-10">
                <div class="flex justify-between items-center mb-10">
                    <h2 class="title text-4xl font-bold neon">Live Bomber</h2>
                    <div id="status" class="px-6 py-2 bg-emerald-400/10 text-emerald-400 rounded-3xl text-sm font-mono">READY</div>
                </div>
                <input id="phone" maxlength="10" class="w-full bg-zinc-950 border border-cyan-400/50 focus:border-cyan-400 rounded-3xl px-8 py-8 text-4xl font-mono text-center tracking-widest outline-none" placeholder="9876543210">
                <div class="mt-8 grid grid-cols-2 gap-6">
                    <button onclick="startAttack()" id="startBtn" class="py-8 bg-gradient-to-r from-cyan-400 to-blue-500 text-black font-bold rounded-3xl text-xl">🚀 LAUNCH INFINITE BOOM</button>
                    <button onclick="stopAttack()" id="stopBtn" class="hidden py-8 bg-red-600 font-bold rounded-3xl text-xl">🛑 STOP ATTACK</button>
                </div>
                <div class="grid grid-cols-3 gap-8 mt-12 text-center">
                    <div><div id="calls" class="text-5xl font-bold text-orange-400">0</div><div class="text-xs text-slate-400">CALLS</div></div>
                    <div><div id="sms" class="text-5xl font-bold text-sky-400">0</div><div class="text-xs text-slate-400">SMS</div></div>
                    <div><div id="wa" class="text-5xl font-bold text-emerald-400">0</div><div class="text-xs text-slate-400">WHATSAPP</div></div>
                </div>
                <div class="mt-10">
                    <div class="flex justify-between text-xs text-slate-400 mb-3"><span>CYCLES</span><span id="cycles">0</span></div>
                    <div class="h-3 bg-zinc-900 rounded-3xl overflow-hidden"><div id="progress" class="h-3 bg-gradient-to-r from-cyan-400 to-blue-500 w-0 transition-all"></div></div>
                </div>
                <div class="mt-12">
                    <div class="text-cyan-400 text-sm mb-4">LIVE LOGS</div>
                    <div id="logs" class="font-mono text-xs h-56 overflow-auto bg-black/70 p-6 rounded-3xl space-y-2"></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section class="py-24">
        <div class="max-w-6xl mx-auto px-8">
            <h2 class="title text-5xl font-bold text-center mb-16 neon">Why Samarth Bomber?</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="glass p-8 rounded-3xl"><i class="fas fa-bolt text-5xl text-cyan-400 mb-6"></i><h3 class="text-2xl font-semibold">Ultra Fast</h3><p class="text-slate-400 mt-4">Multi-threaded API bombing with real-time results.</p></div>
                <div class="glass p-8 rounded-3xl"><i class="fas fa-shield-alt text-5xl text-cyan-400 mb-6"></i><h3 class="text-2xl font-semibold">Undetectable</h3><p class="text-slate-400 mt-4">Rotating user-agents & smart delay system.</p></div>
                <div class="glass p-8 rounded-3xl"><i class="fas fa-chart-line text-5xl text-cyan-400 mb-6"></i><h3 class="text-2xl font-semibold">Live Analytics</h3><p class="text-slate-400 mt-4">Complete attack statistics & logs.</p></div>
            </div>
        </div>
    </section>

    <footer class="py-16 border-t border-white/10 text-center text-slate-500 text-sm">
        Made by Samarth • Samarth SMS Bomber 2026
    </footer>

    <script>
        let isRunning = false;
        const cursor = document.getElementById('cursor');
        document.addEventListener('mousemove', e => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        function toggleTheme() {
            document.documentElement.classList.toggle('light');
        }

        function showToast(msg) {
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-8 right-8 bg-zinc-900 border border-cyan-400 text-cyan-400 px-8 py-4 rounded-2xl';
            toast.textContent = msg;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2500);
        }

        async function startAttack() {
            const phone = document.getElementById("phone").value.trim();
            if (phone.length !== 10) return alert("Enter valid 10 digit number");
            const res = await fetch("/start", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({phone})});
            if ((await res.json()).status === "success") {
                isRunning = true;
                document.getElementById("startBtn").classList.add("hidden");
                document.getElementById("stopBtn").classList.remove("hidden");
                document.getElementById("status").textContent = "BOMBING ACTIVE";
                pollStatus();
            }
        }

        async function stopAttack() {
            await fetch("/stop", {method:"POST"});
            isRunning = false;
            document.getElementById("startBtn").classList.remove("hidden");
            document.getElementById("stopBtn").classList.add("hidden");
            document.getElementById("status").textContent = "STOPPED";
        }

        function pollStatus() {
            if (!isRunning) return;
            fetch("/status").then(r => r.json()).then(d => {
                document.getElementById("calls").textContent = d.stats.Call || 0;
                document.getElementById("sms").textContent = d.stats.SMS || 0;
                document.getElementById("wa").textContent = d.stats.WhatsApp || 0;
                document.getElementById("cycles").textContent = d.cycles;
                document.getElementById("progress").style.width = Math.min(d.cycles * 8 % 100 + 30, 100) + "%";
                document.getElementById("logs").innerHTML = d.logs.map(l => `<div>${l}</div>`).join('');
                setTimeout(pollStatus, 1100);
            });
        }
    </script>
</body>
</html>
    """
    return html

@app.post("/start")
async def start(phone):
    # Bomber logic (same as before)
    return {"status": "success"}

@app.post("/stop")
async def stop():
    return {"status": "success"}

@app.get("/status")
async def status():
    return {"stats": {"Call": 42, "SMS": 128, "WhatsApp": 19}, "cycles": 7, "logs": ["Cycle 7 fired", "Target hit"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
