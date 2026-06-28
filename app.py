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
    <meta name="description" content="Premium Digital Experience">
    <title>NEXUS • Elite Digital Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root { --primary: 34 211 238; }
        body { font-family: 'Inter', system-ui, sans-serif; }
        .title-font { font-family: 'Space Grotesk', sans-serif; }
        .glass { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); }
        .neon { text-shadow: 0 0 20px rgb(var(--primary)), 0 0 40px rgb(var(--primary)); }
        .cursor-dot { position: fixed; width: 20px; height: 20px; border: 2px solid rgb(var(--primary)); border-radius: 50%; pointer-events: none; z-index: 9999; mix-blend-mode: difference; transition: transform 0.1s; }
        .scroll-progress { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(to right, rgb(var(--primary)), #67e8f9); z-index: 50; }
    </style>
</head>
<body class="bg-zinc-950 text-white overflow-x-hidden">
    <!-- Custom Cursor -->
    <div id="cursor" class="cursor-dot hidden md:block"></div>

    <!-- Scroll Progress -->
    <div id="progress" class="scroll-progress w-0"></div>

    <!-- Navbar -->
    <nav class="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10">
        <div class="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-cyan-400 rounded-2xl flex items-center justify-center text-black font-bold">N</div>
                <span class="title-font text-2xl font-semibold tracking-tighter">NEXUS</span>
            </div>
            <div class="hidden md:flex items-center gap-8 text-sm">
                <a href="#home" class="hover:text-cyan-400 transition">Home</a>
                <a href="#features" class="hover:text-cyan-400 transition">Features</a>
                <a href="#services" class="hover:text-cyan-400 transition">Services</a>
                <a href="#pricing" class="hover:text-cyan-400 transition">Pricing</a>
                <a href="#contact" class="hover:text-cyan-400 transition">Contact</a>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="toggleTheme()" class="w-9 h-9 flex items-center justify-center rounded-xl hover:bg-white/10 transition">
                    <i id="theme-icon" class="fas fa-moon"></i>
                </button>
                <button onclick="showToast('Demo request sent!')" class="px-6 py-3 bg-white text-black rounded-2xl font-medium text-sm hover:bg-cyan-400 hover:text-black transition">GET STARTED</button>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section id="home" class="min-h-screen flex items-center pt-20 relative">
        <div class="max-w-5xl mx-auto px-6 text-center">
            <div class="inline-flex items-center gap-2 bg-white/5 px-5 py-2 rounded-3xl text-sm mb-8">
                <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                NOW ACCEPTING NEW CLIENTS 2026
            </div>
            <h1 class="title-font text-7xl md:text-8xl font-bold leading-none tracking-tighter neon mb-6">WE CRAFT<br>DIGITAL<br>EXCELLENCE</h1>
            <p class="max-w-md mx-auto text-xl text-slate-400">Premium web experiences for visionary brands.</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center mt-12">
                <button onclick="document.getElementById('contact').scrollIntoView({behavior:'smooth'})" class="px-10 py-6 bg-white text-black rounded-3xl text-lg font-semibold hover:scale-105 transition">START PROJECT</button>
                <button onclick="showToast('Portfolio opening in new tab...')" class="px-10 py-6 border border-white/30 rounded-3xl text-lg font-semibold hover:bg-white/5 transition">VIEW WORK</button>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section id="features" class="py-24">
        <div class="max-w-7xl mx-auto px-6">
            <div class="text-center mb-16">
                <span class="text-cyan-400 text-sm tracking-widest">CAPABILITIES</span>
                <h2 class="title-font text-5xl font-bold mt-3">Built for the extraordinary</h2>
            </div>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="glass p-8 rounded-3xl group hover:-translate-y-2 transition">
                    <i class="fas fa-bolt text-4xl text-cyan-400 mb-6"></i>
                    <h3 class="text-2xl font-semibold mb-3">Lightning Performance</h3>
                    <p class="text-slate-400">Sub-100ms load times with cutting-edge optimization.</p>
                </div>
                <div class="glass p-8 rounded-3xl group hover:-translate-y-2 transition">
                    <i class="fas fa-palette text-4xl text-cyan-400 mb-6"></i>
                    <h3 class="text-2xl font-semibold mb-3">Bespoke Design</h3>
                    <p class="text-slate-400">Pixel-perfect interfaces tailored to your brand DNA.</p>
                </div>
                <div class="glass p-8 rounded-3xl group hover:-translate-y-2 transition">
                    <i class="fas fa-shield-alt text-4xl text-cyan-400 mb-6"></i>
                    <h3 class="text-2xl font-semibold mb-3">Enterprise Security</h3>
                    <p class="text-slate-400">Bank-grade protection and privacy by default.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats -->
    <section class="py-20 bg-black/40">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div><div class="text-6xl font-bold text-cyan-400" data-count="240">0</div><div class="text-slate-400">Projects Delivered</div></div>
            <div><div class="text-6xl font-bold text-cyan-400" data-count="98">0</div><div class="text-slate-400">% Client Retention</div></div>
            <div><div class="text-6xl font-bold text-cyan-400" data-count="45">0</div><div class="text-slate-400">Countries Reached</div></div>
            <div><div class="text-6xl font-bold text-cyan-400" data-count="12">0</div><div class="text-slate-400">Awards Won</div></div>
        </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="py-24">
        <div class="max-w-7xl mx-auto px-6">
            <div class="text-center mb-16">
                <h2 class="title-font text-5xl font-bold">Simple, Transparent Pricing</h2>
            </div>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="glass p-8 rounded-3xl">
                    <div class="text-cyan-400">STARTER</div>
                    <div class="text-6xl font-bold my-6">$4,900</div>
                    <ul class="space-y-4 mb-10 text-slate-400">
                        <li>✓ Custom Landing Page</li>
                        <li>✓ Basic SEO</li>
                        <li>✓ 3 Revisions</li>
                    </ul>
                    <button onclick="showToast('Quote request sent')" class="w-full py-6 border border-white/30 rounded-2xl">GET STARTED</button>
                </div>
                <div class="glass p-8 rounded-3xl ring-2 ring-cyan-400 scale-105">
                    <div class="bg-cyan-400 text-black text-center text-sm py-1 rounded-full -mt-4">MOST POPULAR</div>
                    <div class="text-cyan-400 mt-8">PRO</div>
                    <div class="text-6xl font-bold my-6">$12,500</div>
                    <ul class="space-y-4 mb-10 text-slate-400">
                        <li>✓ Full Website</li>
                        <li>✓ Advanced Animations</li>
                        <li>✓ Dashboard + CMS</li>
                        <li>✓ Priority Support</li>
                    </ul>
                    <button onclick="showToast('Pro package selected')" class="w-full py-6 bg-cyan-400 text-black rounded-2xl font-semibold">CHOOSE PRO</button>
                </div>
                <div class="glass p-8 rounded-3xl">
                    <div class="text-cyan-400">ENTERPRISE</div>
                    <div class="text-6xl font-bold my-6">Custom</div>
                    <ul class="space-y-4 mb-10 text-slate-400">
                        <li>✓ Everything Unlimited</li>
                        <li>✓ Dedicated Team</li>
                        <li>✓ White Label</li>
                    </ul>
                    <button onclick="showToast('Enterprise inquiry sent')" class="w-full py-6 border border-white/30 rounded-2xl">CONTACT US</button>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="py-24">
        <div class="max-w-2xl mx-auto px-6">
            <h2 class="text-5xl font-bold text-center title-font mb-12">Let's Build Something Legendary</h2>
            <form onsubmit="handleSubmit(event)" class="space-y-8">
                <input type="text" id="name" placeholder="Your Name" required class="w-full bg-white/5 border border-white/20 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400">
                <input type="email" id="email" placeholder="Business Email" required class="w-full bg-white/5 border border-white/20 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400">
                <textarea id="message" rows="6" placeholder="Tell us about your project..." required class="w-full bg-white/5 border border-white/20 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400"></textarea>
                <button type="submit" class="w-full py-7 bg-gradient-to-r from-cyan-400 to-blue-500 text-black font-semibold rounded-3xl text-lg">SEND MESSAGE</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-white/10 py-16">
        <div class="max-w-7xl mx-auto px-6 text-center text-slate-400">
            <div class="flex justify-center gap-8 text-2xl mb-8">
                <i onclick="showToast('Twitter opened')" class="fab fa-twitter cursor-pointer hover:text-cyan-400"></i>
                <i onclick="showToast('Instagram opened')" class="fab fa-instagram cursor-pointer hover:text-cyan-400"></i>
                <i onclick="showToast('LinkedIn opened')" class="fab fa-linkedin cursor-pointer hover:text-cyan-400"></i>
            </div>
            <p>© 2026 NEXUS Studio. All Rights Reserved.</p>
        </div>
    </footer>

    <!-- Toast -->
    <div id="toast" class="hidden fixed bottom-6 right-6 bg-zinc-900 border border-cyan-400 text-cyan-400 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3">
        <span id="toast-text"></span>
    </div>

    <script>
        // Tailwind script already loaded
        function toggleTheme() {
            if (document.documentElement.classList.contains('light')) {
                document.documentElement.classList.remove('light');
                document.getElementById('theme-icon').classList.replace('fa-sun', 'fa-moon');
            } else {
                document.documentElement.classList.add('light');
                document.getElementById('theme-icon').classList.replace('fa-moon', 'fa-sun');
            }
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-text').textContent = msg;
            toast.classList.remove('hidden');
            setTimeout(() => toast.classList.add('hidden'), 2800);
        }

        function handleSubmit(e) {
            e.preventDefault();
            showToast("Message received. We'll reply within 24 hours.");
            e.target.reset();
        }

        // Custom cursor
        const cursor = document.getElementById('cursor');
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        // Scroll progress
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("progress").style.width = scrolled + "%";
        });

        // Counter animation
        function animateCounters() {
            document.querySelectorAll('[data-count]').forEach(el => {
                const target = parseInt(el.getAttribute('data-count'));
                let count = 0;
                const increment = target / 60;
                const timer = setInterval(() => {
                    count += increment;
                    if (count >= target) {
                        el.textContent = target;
                        clearInterval(timer);
                    } else {
                        el.textContent = Math.floor(count);
                    }
                }, 30);
            });
        }
        window.onload = () => {
            animateCounters();
            console.log("%cNEXUS Loaded Successfully", "color:#22d3ee;font-family:monospace");
        };
    </script>
</body>
</html>
    """
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
