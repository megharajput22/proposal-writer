from flask import Flask, request, jsonify
import requests as req
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html>
<head>
<title>Proposal Writer AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
    font-family:'Inter',sans-serif;
    background:#080810;
    color:#e2e8f0;
    min-height:100vh;
    overflow-x:hidden;
    position:relative
}

/* BLOBS */
.blob{
    position:fixed;
    border-radius:50%;
    filter:blur(100px);
    opacity:0.12;
    z-index:0;
    pointer-events:none
}
.blob1{
    width:600px;height:600px;
    background:#7c3aed;
    top:-200px;left:-200px;
    animation:blob1Move 15s ease-in-out infinite alternate
}
.blob2{
    width:500px;height:500px;
    background:#06b6d4;
    bottom:-200px;right:-200px;
    animation:blob2Move 18s ease-in-out infinite alternate
}
.blob3{
    width:300px;height:300px;
    background:#4f46e5;
    top:50%;left:50%;
    animation:blob3Move 12s ease-in-out infinite alternate
}
@keyframes blob1Move{
    0%{transform:translate(0,0) scale(1)}
    100%{transform:translate(80px,60px) scale(1.15)}
}
@keyframes blob2Move{
    0%{transform:translate(0,0) scale(1)}
    100%{transform:translate(-60px,-80px) scale(1.1)}
}
@keyframes blob3Move{
    0%{transform:translate(-50%,-50%) scale(1)}
    100%{transform:translate(-45%,-55%) scale(1.2)}
}

/* POPUP */
.popup-overlay{
    position:fixed;top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.92);
    display:flex;align-items:center;justify-content:center;
    z-index:999;backdrop-filter:blur(12px)
}
.popup-box{
    background:rgba(12,12,20,0.98);
    border:1px solid rgba(124,58,237,0.4);
    border-radius:20px;
    padding:45px 35px;
    text-align:center;
    max-width:360px;width:90%;
    box-shadow:0 0 80px rgba(124,58,237,0.2);
    animation:popIn 0.5s cubic-bezier(0.175,0.885,0.32,1.275)
}
@keyframes popIn{
    from{transform:scale(0.85) translateY(20px);opacity:0}
    to{transform:scale(1) translateY(0);opacity:1}
}
.popup-lottie{
    width:130px;height:130px;
    margin:0 auto 15px
}
.popup-box h1{
    font-family:'Orbitron',sans-serif;
    font-size:20px;font-weight:700;
    color:#ffffff;
    margin-bottom:10px;
    letter-spacing:1px
}
.popup-box p{
    color:#94a3b8;font-size:13px;
    line-height:1.7;margin-bottom:25px
}
.popup-features{
    display:flex;flex-direction:column;gap:10px;
    margin-bottom:25px;text-align:left
}
.popup-feature{
    display:flex;align-items:center;gap:10px;
    color:#cbd5e1;font-size:13px
}
.popup-feature-dot{
    width:6px;height:6px;border-radius:50%;
    background:linear-gradient(135deg,#7c3aed,#06b6d4);
    flex-shrink:0
}
.popup-btn{
    width:100%;padding:15px;
    background:linear-gradient(135deg,#7c3aed,#4f46e5);
    color:white;border:none;border-radius:12px;
    font-size:14px;font-weight:600;
    font-family:'Inter',sans-serif;
    cursor:pointer;
    box-shadow:0 4px 20px rgba(124,58,237,0.4);
    transition:all 0.2s
}

/* MAIN */
.container{
    position:relative;z-index:1;
    max-width:680px;margin:0 auto;padding:20px
}

/* NAVBAR */
.navbar{
    display:flex;align-items:center;
    justify-content:space-between;
    padding:20px 0 30px
}
.nav-logo{
    display:flex;align-items:center;gap:10px
}
.nav-logo-icon{
    width:36px;height:36px;
    background:linear-gradient(135deg,#7c3aed,#06b6d4);
    border-radius:10px;
    display:flex;align-items:center;
    justify-content:center;font-size:18px
}
.nav-logo-text{
    font-family:'Orbitron',sans-serif;
    font-size:14px;font-weight:700;
    color:#ffffff;letter-spacing:1px
}
.nav-badge{
    background:rgba(124,58,237,0.15);
    border:1px solid rgba(124,58,237,0.3);
    color:#a78bfa;
    padding:5px 14px;border-radius:20px;
    font-size:11px;font-weight:600;
    letter-spacing:1px
}

/* HERO */
.hero{
    text-align:center;
    padding:10px 0 30px;
    position:relative
}
.hero-lottie{
    width:110px;height:110px;
    margin:0 auto 15px
}
.hero-title{
    font-family:'Orbitron',sans-serif;
    font-size:28px;font-weight:900;
    line-height:1.2;margin-bottom:12px;
    background:linear-gradient(135deg,#ffffff 0%,#a78bfa 50%,#06b6d4 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    filter:drop-shadow(0 0 25px rgba(124,58,237,0.5))
}
.hero-sub{
    color:#64748b;font-size:13px;
    line-height:1.7;max-width:420px;margin:0 auto
}

/* DIVIDER */
.divider{
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(124,58,237,0.4),rgba(6,182,212,0.4),transparent);
    margin:5px 0 25px
}

/* CARD */
.card{
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:16px;padding:28px;margin-bottom:16px;
    backdrop-filter:blur(20px);
    box-shadow:0 4px 24px rgba(0,0,0,0.5)
}
.card-title{
    font-size:11px;font-weight:600;
    color:#64748b;text-transform:uppercase;
    letter-spacing:2px;margin-bottom:22px;
    display:flex;align-items:center;gap:8px
}
.card-title::before{
    content:'';width:3px;height:12px;
    background:linear-gradient(#7c3aed,#06b6d4);
    border-radius:2px
}

/* LABELS - BRIGHT WHITE */
label{
    color:#ffffff !important;
    font-weight:700 !important;
    font-size:13px !important;
    display:block;
    margin-bottom:8px;
    letter-spacing:0.3px
}

/* INPUTS - HIGH CONTRAST */
input,textarea{
    width:100%;
    padding:13px 16px;
    border-radius:10px;
    border:1px solid rgba(255,255,255,0.1);
    background:rgba(255,255,255,0.06);
    color:#ffffff !important;
    font-size:14px;
    font-family:'Inter',sans-serif;
    margin-bottom:20px;
    transition:all 0.25s ease;
    outline:none;
    caret-color:#a78bfa
}
input::placeholder,textarea::placeholder{
    color:#64748b !important;
    font-size:13px
}
input:focus,textarea:focus{
    border-color:rgba(124,58,237,0.7) !important;
    background:rgba(124,58,237,0.08) !important;
    box-shadow:0 0 0 3px rgba(124,58,237,0.15),
               0 0 20px rgba(124,58,237,0.2) !important;
    color:#ffffff !important
}
textarea{height:105px;resize:none}

/* SKILLS INPUT SPECIAL GLOW */
#skills:focus{
    border-color:rgba(6,182,212,0.7) !important;
    background:rgba(6,182,212,0.06) !important;
    box-shadow:0 0 0 3px rgba(6,182,212,0.15),
               0 0 20px rgba(6,182,212,0.2) !important
}

/* BUTTON */
#genBtn{
    width:100%;padding:16px;
    background:linear-gradient(135deg,#7c3aed,#4f46e5);
    color:#ffffff;border:none;border-radius:12px;
    font-size:14px;font-weight:600;
    font-family:'Inter',sans-serif;
    cursor:pointer;
    position:relative;overflow:hidden;
    box-shadow:0 4px 20px rgba(124,58,237,0.35);
    animation:subtlePulse 3s ease-in-out infinite;
    letter-spacing:0.5px
}
@keyframes subtlePulse{
    0%,100%{box-shadow:0 4px 20px rgba(124,58,237,0.35)}
    50%{box-shadow:0 4px 35px rgba(124,58,237,0.65)}
}
#genBtn::after{
    content:'';position:absolute;
    top:0;left:-100%;width:100%;height:100%;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent);
    animation:shimmer 2.5s linear infinite
}
@keyframes shimmer{
    0%{left:-100%}100%{left:100%}
}

/* LOADING */
#loading{
    text-align:center;padding:35px;display:none
}
.spinner{
    width:42px;height:42px;
    border:2px solid rgba(124,58,237,0.15);
    border-top:2px solid #7c3aed;
    border-right:2px solid #06b6d4;
    border-radius:50%;
    animation:spin 0.7s linear infinite;
    margin:0 auto 15px
}
@keyframes spin{to{transform:rotate(360deg)}}
#loading p{color:#64748b;font-size:13px;font-weight:500}

/* OUTPUT */
.output{
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(6,182,212,0.2);
    border-radius:16px;padding:28px;
    margin-bottom:16px;display:none;
    backdrop-filter:blur(20px);
    animation:fadeUp 0.4s ease
}
@keyframes fadeUp{
    from{opacity:0;transform:translateY(20px)}
    to{opacity:1;transform:translateY(0)}
}
.output-header{
    display:flex;align-items:center;
    justify-content:space-between;margin-bottom:18px
}
.output-title{
    font-size:11px;font-weight:600;
    color:#64748b;text-transform:uppercase;
    letter-spacing:2px;
    display:flex;align-items:center;gap:8px
}
.output-title::before{
    content:'';width:3px;height:12px;
    background:linear-gradient(#06b6d4,#7c3aed);
    border-radius:2px
}
.output-lottie{
    width:45px;height:45px
}
.output-status{
    display:flex;align-items:center;gap:6px;
    font-size:11px;color:#22c55e;font-weight:500
}
.status-dot{
    width:6px;height:6px;border-radius:50%;
    background:#22c55e;
    animation:statusPulse 2s ease infinite
}
@keyframes statusPulse{
    0%,100%{opacity:1}50%{opacity:0.4}
}

/* PROPOSAL TEXT - SPACING FIXED */
.proposal-text{
    background:rgba(0,0,0,0.3);
    padding:20px;border-radius:12px;
    line-height:1.9;
    color:#e2e8f0;
    font-size:14px;
    white-space:pre-wrap;
    word-spacing:normal;
    word-break:normal;
    letter-spacing:normal;
    border-left:2px solid rgba(124,58,237,0.5);
    min-height:60px;
    font-family:'Inter',sans-serif;
    font-weight:400
}

#copyBtn{
    margin-top:16px;width:100%;padding:13px;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    color:#94a3b8;border-radius:10px;
    font-size:13px;font-weight:500;
    font-family:'Inter',sans-serif;
    cursor:pointer;transition:all 0.2s
}
#copyBtn:active{
    background:rgba(255,255,255,0.07);
    color:#ffffff
}

/* CONFETTI */
.confetti-piece{
    position:fixed;border-radius:2px;
    z-index:9999;pointer-events:none;
    animation:confettiFall 3s ease-in forwards
}
@keyframes confettiFall{
    0%{transform:translateY(-10px) rotate(0deg);opacity:1}
    100%{transform:translateY(105vh) rotate(540deg);opacity:0}
}

/* FOOTER */
.footer{
    text-align:center;padding:20px 0 35px
}
.footer p{color:#1e293b;font-size:11px;letter-spacing:1px}
</style>
</head>
<body>

<div class="blob blob1"></div>
<div class="blob blob2"></div>
<div class="blob blob3"></div>

<!-- POPUP -->
<div class="popup-overlay" id="welcomePopup">
    <div class="popup-box">
        <div class="popup-lottie" id="popupLottie"></div>
        <h1>PROPOSAL WRITER AI</h1>
        <p>AI-powered proposal generator for freelancers. Win more clients instantly.</p>
        <div class="popup-features">
            <div class="popup-feature">
                <div class="popup-feature-dot"></div>
                <span>Generate proposals in seconds</span>
            </div>
            <div class="popup-feature">
                <div class="popup-feature-dot"></div>
                <span>Professional quality output</span>
            </div>
            <div class="popup-feature">
                <div class="popup-feature-dot"></div>
                <span>100% free, no signup needed</span>
            </div>
        </div>
        <button class="popup-btn" id="startBtn">Get Started Free</button>
    </div>
</div>

<div class="container">

    <div class="navbar">
        <div class="nav-logo">
            <div class="nav-logo-icon">⚡</div>
            <span class="nav-logo-text">PROPOSAL AI</span>
        </div>
        <div class="nav-badge">FREE</div>
    </div>

    <!-- HERO WITH LOTTIE -->
    <div class="hero">
        <div class="hero-lottie" id="heroLottie"></div>
        <h1 class="hero-title">Write Winning<br>Proposals Instantly</h1>
        <p class="hero-sub">AI-powered tool that generates professional freelancer proposals in seconds.</p>
    </div>

    <div class="divider"></div>

    <!-- FORM -->
    <div class="card">
        <div class="card-title">Project Details</div>

        <label>Project Title</label>
        <input type="text" id="title" placeholder="e.g. Build a landing page for my bakery"/>

        <label>Project Description</label>
        <textarea id="description" placeholder="Describe what the client needs..."></textarea>

        <label>Your Skills</label>
        <input type="text" id="skills" placeholder="e.g. Python, Web Design, React"/>

        <button id="genBtn">Generate Proposal</button>
    </div>

    <div id="loading">
        <div class="spinner"></div>
        <p>Generating your proposal...</p>
    </div>

    <!-- OUTPUT -->
    <div class="output" id="output">
        <div class="output-header">
            <div class="output-title">Generated Proposal</div>
            <div style="display:flex;align-items:center;gap:12px">
                <div class="output-lottie" id="outputLottie"></div>
                <div class="output-status">
                    <div class="status-dot"></div>
                    Ready
                </div>
            </div>
        </div>
        <div class="proposal-text" id="proposalText"></div>
        <button id="copyBtn">Copy to Clipboard</button>
    </div>

    <div class="footer">
        <p>PROPOSAL WRITER AI</p>
    </div>

</div>

<script>
// LOTTIE - AI Robot in popup
lottie.loadAnimation({
    container:document.getElementById('popupLottie'),
    renderer:'svg',
    loop:true,autoplay:true,
    path:'https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json'
});

// LOTTIE - Magic wand in hero
lottie.loadAnimation({
    container:document.getElementById('heroLottie'),
    renderer:'svg',
    loop:true,autoplay:true,
    path:'https://assets9.lottiefiles.com/packages/lf20_myejiggj.json'
});

// LOTTIE - Rocket in output
lottie.loadAnimation({
    container:document.getElementById('outputLottie'),
    renderer:'svg',
    loop:true,autoplay:true,
    path:'https://assets10.lottiefiles.com/packages/lf20_touohxv0.json'
});

// POPUP
document.getElementById("startBtn").addEventListener("click",function(){
    document.getElementById("welcomePopup").style.display="none";
});
document.getElementById("startBtn").addEventListener("touchend",function(e){
    e.preventDefault();
    document.getElementById("welcomePopup").style.display="none";
});

// CONFETTI
function launchConfetti(){
    var colors=["#a78bfa","#06b6d4","#818cf8","#e879f9","#38bdf8","#34d399"];
    for(var i=0;i<55;i++){
        var p=document.createElement("div");
        p.className="confetti-piece";
        p.style.left=Math.random()*100+"vw";
        p.style.background=colors[Math.floor(Math.random()*colors.length)];
        p.style.width=(4+Math.random()*6)+"px";
        p.style.height=(4+Math.random()*6)+"px";
        p.style.animationDelay=Math.random()*2+"s";
        p.style.animationDuration=(2.5+Math.random()*2)+"s";
        p.style.borderRadius=Math.random()>0.5?"50%":"2px";
        document.body.appendChild(p);
        setTimeout(function(el){return function(){el.remove()}}(p),5000);
    }
}

// TYPEWRITER - spaces fixed
function typeWriter(text,element){
    element.innerText="";
    var i=0;
    function type(){
        if(i<text.length){
            element.innerText+=text[i];
            i++;
            setTimeout(type,16);
        }
    }
    type();
}

// COPY
function copyProposal(){
    var text=document.getElementById("proposalText").innerText;
    navigator.clipboard.writeText(text).then(function(){
        var btn=document.getElementById("copyBtn");
        btn.innerText="Copied!";
        setTimeout(function(){btn.innerText="Copy to Clipboard";},2000);
    });
}
document.getElementById("copyBtn").addEventListener("click",copyProposal);
document.getElementById("copyBtn").addEventListener("touchend",function(e){
    e.preventDefault();copyProposal();
});

// GENERATE
function generate(){
    var title=document.getElementById("title").value.trim();
    var desc=document.getElementById("description").value.trim();
    var skills=document.getElementById("skills").value.trim();
    if(!title||!desc||!skills){alert("Please fill all fields!");return;}
    document.getElementById("loading").style.display="block";
    document.getElementById("output").style.display="none";
    fetch("/generate",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({title:title,description:desc,skills:skills})
    })
    .then(function(res){return res.json();})
    .then(function(data){
        document.getElementById("loading").style.display="none";
        if(data.proposal){
            document.getElementById("output").style.display="block";
            typeWriter(data.proposal.trim(),document.getElementById("proposalText"));
            launchConfetti();
        }else{
            alert("Error: "+JSON.stringify(data));
        }
    })
    .catch(function(err){
        document.getElementById("loading").style.display="none";
        alert("Error: "+err.message);
    });
}
document.getElementById("genBtn").addEventListener("click",generate);
document.getElementById("genBtn").addEventListener("touchend",function(e){
    e.preventDefault();generate();
});
</script>
</body>
</html>"""

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = "Write a professional freelancer proposal for:\nProject: " + str(data.get("title")) + "\nDescription: " + str(data.get("description")) + "\nSkills: " + str(data.get("skills")) + "\nMax 200 words. Be professional, confident and persuasive. Use proper spacing between all words."
    try:
        response = req.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + str(API_KEY),
                "Content-Type": "application/json",
                "HTTP-Referer": "https://proposal-writer.up.railway.app",
                "X-Title": "Proposal Writer AI"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        result = response.json()
        if "choices" in result:
            proposal = result["choices"][0]["message"]["content"]
            proposal = " ".join(proposal.split())
            return jsonify({"proposal": proposal})
        else:
            return jsonify({"proposal": "API Error: " + str(result)})
    except Exception as e:
        return jsonify({"proposal": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
