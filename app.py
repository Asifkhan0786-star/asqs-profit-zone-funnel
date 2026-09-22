import os
import json
import urllib.request
import urllib.error
from flask import Flask, jsonify, request

app = Flask(__name__)

CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL", "https://t.me/your_channel")
BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "@ASQSProfitZone_bot")
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "gpt-5-mini")

SYSTEM_PROMPT = """You are the ASQS Profit Zone AI Assistant.
Help with trading education, technical-analysis concepts, market terminology,
risk management, trading psychology, and general research.

Rules:
- Educational information only. Never promise profits or guaranteed signals.
- Never claim certainty about future prices or market direction.
- Explain assumptions and risks clearly.
- If a user asks for live/current prices or news, explain that live data must be supplied
  or connected separately; do not invent current prices.
- Keep answers practical and easy to understand.
- Never ask for passwords, private keys, API keys, or account credentials.
"""

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ASQS PROFIT ZONE</title>
<style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#070b14;color:#fff;line-height:1.6}
header{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:16px 6%;background:rgba(7,11,20,.96);border-bottom:1px solid #202638}
.logo{font-size:21px;font-weight:800;letter-spacing:1px}.logo span{color:#9b6cff}
a{text-decoration:none;color:#fff}.btn{display:inline-block;padding:12px 18px;border-radius:11px;font-weight:700;border:1px solid #7650db;background:linear-gradient(135deg,#6937d8,#a052ee)}
.hero{text-align:center;padding:80px 7% 70px;background:radial-gradient(circle at 50% 10%,rgba(124,58,237,.28),transparent 43%)}
.badge{display:inline-block;padding:7px 14px;border:1px solid #51388e;border-radius:999px;color:#cdbdff;background:#15102b;font-size:13px;font-weight:700}
h1{font-size:clamp(40px,9vw,72px);line-height:1.05;margin:22px 0 15px}.grad{color:#a56cff}
.hero p,.sub{max-width:720px;margin:0 auto 24px;color:#aeb6c8}.actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.ghost{display:inline-block;padding:12px 18px;border-radius:11px;border:1px solid #384157;color:#dce2ef}
.section{padding:65px 6%;max-width:1100px;margin:auto}h2{text-align:center;font-size:32px;margin:0 0 8px}.sub{text-align:center}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:28px}.card{background:#0d1320;border:1px solid #202a3d;border-radius:17px;padding:24px}.icon{font-size:30px}.card h3{margin:10px 0 5px}.card p{color:#9fa9bd;margin:0}
.ai-wrap{max-width:900px;margin:28px auto 0;background:linear-gradient(180deg,#10172a,#0b111d);border:1px solid #2a3550;border-radius:20px;padding:20px;box-shadow:0 18px 50px rgba(0,0,0,.25)}
textarea{width:100%;min-height:130px;resize:vertical;background:#070b14;color:#fff;border:1px solid #34405a;border-radius:13px;padding:15px;font:inherit;outline:none}
textarea:focus{border-color:#8c5cf4}.ai-row{display:flex;gap:10px;align-items:center;margin-top:12px;flex-wrap:wrap}.ask{border:0;cursor:pointer;color:#fff;padding:12px 20px;border-radius:11px;font-weight:800;background:linear-gradient(135deg,#6d35e0,#a552ef)}
.status{color:#9ca8bc;font-size:13px}.answer{white-space:pre-wrap;margin-top:18px;padding:18px;border-radius:14px;background:#080d17;border:1px solid #27334a;min-height:60px;color:#e8ecf5;display:none}
.telegram{text-align:center;margin:20px 6% 60px;padding:45px 20px;border:1px solid #28344a;border-radius:22px;background:#0c1320}.telegram p{color:#aab3c4}
footer{text-align:center;padding:28px 20px;color:#7f8aa0;border-top:1px solid #1d2637;font-size:13px}
@media(max-width:600px){header{padding:13px 4%}.logo{font-size:17px}.nav{padding:9px 12px;font-size:13px}.hero{padding:65px 5%}.section{padding:50px 5%}.ai-wrap{padding:14px}}
</style>
</head>
<body>
<header>
  <div class="logo">ASQS <span>PROFIT ZONE</span></div>
  <a class="btn nav" href="{{CHANNEL_URL}}" target="_blank" rel="noopener">📢 Join Telegram</a>
</header>

<main>
<section class="hero">
  <div class="badge">🚀 AI TRADING COMMUNITY</div>
  <h1>Trade Smarter.<br><span class="grad">Learn Better.</span></h1>
  <p>Trading education, research tools and an AI assistant built for responsible learning.</p>
  <div class="actions">
    <a class="btn" href="{{CHANNEL_URL}}" target="_blank" rel="noopener">📢 Join Telegram</a>
    <a class="ghost" href="#ai">🤖 Try AI Assistant</a>
  </div>
</section>

<section class="section">
  <h2>AI Trading Tools</h2>
  <p class="sub">Use the assistant to learn concepts, study setups and understand risk.</p>
  <div class="cards">
    <div class="card"><div class="icon">📊</div><h3>Market Analysis</h3><p>Ask about chart concepts, indicators, support/resistance and setups.</p></div>
    <div class="card"><div class="icon">🤖</div><h3>AI Assistant</h3><p>Ask questions in natural language and get an educational response.</p></div>
    <div class="card"><div class="icon">📈</div><h3>Trading Education</h3><p>Learn terminology, strategies and risk-management concepts.</p></div>
    <div class="card"><div class="icon">🧠</div><h3>Smart Learning</h3><p>Turn difficult trading topics into simple explanations.</p></div>
  </div>
</section>

<section id="ai" class="section">
  <h2>🤖 ASQS AI Assistant</h2>
  <p class="sub">Ask a trading-education question. Do not enter passwords, API keys or account credentials.</p>
  <div class="ai-wrap">
    <textarea id="q" maxlength="4000" placeholder="Example: Explain support and resistance in simple words..."></textarea>
    <div class="ai-row">
      <button class="ask" id="ask">Ask AI</button>
      <span class="status" id="status">Ready</span>
    </div>
    <div class="answer" id="answer"></div>
  </div>
</section>

<section class="telegram">
  <h2>Join ASQS PROFIT ZONE</h2>
  <p>Get updates, educational content and community information on Telegram.</p>
  <a class="btn" href="{{CHANNEL_URL}}" target="_blank" rel="noopener">✈️ Join Our Telegram</a>
</section>
</main>

<footer><strong>ASQS PROFIT ZONE</strong><br>Educational content only. Trading involves risk.<br>© 2026 ASQS Profit Zone</footer>

<script>
const q=document.getElementById("q"), ask=document.getElementById("ask"),
statusEl=document.getElementById("status"), answer=document.getElementById("answer");

async function runAI(){
  const message=q.value.trim();
  if(!message){statusEl.textContent="Please enter a question.";q.focus();return}
  ask.disabled=true;statusEl.textContent="Thinking…";answer.style.display="block";answer.textContent="";
  try{
    const r=await fetch("/api/ai",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message})});
    const data=await r.json();
    if(!r.ok) throw new Error(data.error||"AI request failed");
    answer.textContent=data.answer||"No answer returned.";
    statusEl.textContent="Ready";
  }catch(e){answer.textContent="⚠️ "+e.message;statusEl.textContent="Error"}
  finally{ask.disabled=false}
}
ask.addEventListener("click",runAI);
q.addEventListener("keydown",e=>{if((e.ctrlKey||e.metaKey)&&e.key==="Enter")runAI()});
</script>
</body>
</html>"""

def extract_output_text(data):
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []) if isinstance(item, dict) else []:
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text", "")
                if text:
                    parts.append(text)
    return "\n".join(parts).strip()

@app.get("/")
def home():
    return PAGE.replace("{{CHANNEL_URL}}", CHANNEL_URL)

@app.post("/api/ai")
def ai():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please enter a question."}), 400
    if len(message) > 4000:
        return jsonify({"error": "Question is too long. Keep it under 4000 characters."}), 400
    if not AI_API_KEY:
        return jsonify({"error": "AI is not configured yet. Add AI_API_KEY in Render Environment."}), 503

    payload = json.dumps({
        "model": AI_MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": message
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + AI_API_KEY
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
        answer = extract_output_text(result)
        if not answer:
            return jsonify({"error": "The AI returned an empty response."}), 502
        return jsonify({"answer": answer})
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
            detail = json.loads(body).get("error", {}).get("message", body)
        except Exception:
            detail = str(exc)
        return jsonify({"error": "OpenAI API error: " + str(detail)[:350]}), 502
    except Exception as exc:
        app.logger.exception("AI request failed")
        return jsonify({"error": "AI request failed: " + str(exc)[:250]}), 502

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "asqs-profit-zone-web",
        "ai_configured": bool(AI_API_KEY)
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
