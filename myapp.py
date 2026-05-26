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
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
    font-family:'Poppins',sans-serif;
    background:#0a0a0a;
    color:white;
    min-height:100vh;
    overflow-x:hidden;
    position:relative
}

/* BLURRY BLOBS */
.blob{
    position:fixed;
    border-radius:50%;
    filter:blur(80px);
    opacity:0.25;
    z-index:0;
    animation:blobMove 8s ease-in-out infinite alternate
}
.blob1{
    width:500px;height:500px;
    background:radial-gradient(circle,#7c3aed,#4c1d95);
    top:-100px;left:-100px;
    animation-duration:10s
}
.blob2{
    width:400px;height:400px;
    background:radial-gradient(circle,#06b6d4,#0e7490);
    bottom:-100px;right:-100px;
    animation-duration:12s;
    animation-delay:2s
}
@keyframes blobMove{
    0%{transform:translate(0,0) scale(1)}
    33%{transform:translate(60px,-40px) scale(1.1)}
    66%{transform:translate(-40px,60px) scale(0.95)}
    100%{transform:translate(30px,30px) scale(1.05)}
}

/* POPUP */
.popup-overlay{
    position:fixed;top:0;left:0;width:100%;height:100%;
    background:rgba(0,0,0,0.9);
    display:flex;align-items:center;justify-content:center;
    z-index:999;backdrop-filter:blur(10px)
}
.popup-box{
    background:rgba(15,15,25,0.95);
    border:1px solid rgba(124,58,237,0.6);
    border-radius:24px;padding:40px 30px;text-align:center;
    max-width:340px;width:90%;
    box-shadow:0 0 60px rgba(124,58,237,0.4),inset 0 0 60px rgba(124,58,237,0.05);
    animation:popIn 0.7s cubic-bezier(0.175,0.885,0.32,1.275)
}
@keyframes popIn{
    from{transform:scale(0.3) rotate(-15deg);opacity:0}
    to{transform:scale(1) rotate(0deg);opacity:1}
}
.popup-lottie{width:120px;height:120px;margin:0 auto 15px}
.popup-box h1{
    font-family:'Orbitron',sans-serif;
    font-size:22px;font-weight:900;margin-bottom:10px;
    text-shadow:0 0 20px #7c3aed,0 0 40px #7c3aed;
    background:linear-gradient(135deg,#a78bfa,#06b6d4);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.popup-box p{color:#888;font-size:13px;margin-bottom:20px;line-height:1.6}
.badge{
    background:linear-gradient(135deg,#7c3aed,#06b6d4);
    color:white;padding:8px 20px;border-radius:20px;
    font-weight:600;font-size:12px;display:inline-block;
    margin-bottom:20px;
    box-shadow:0 0 20px rgba(124,58,237,0.5)
}
.popup-btn{
    width:100%;padding:16px;
    background:linear-gradient(135deg,#7c3aed,#06b6d4);
    color:white;border:none;border-radius:14px;
    font-size:16px;font-weight:700;
    font-family:'Orbitron',sans-serif;
    letter-spacing:1px;
    box-shadow:0 0 30px rgba(124,58,237,0.6);
    transition:transform 0.2s,box-shadow 0.2s
}
.popup-btn:active{transform:scale(0.97)}

/* MAIN CONTAINER */
.container{
    position:relative;z-index:1;
    max-width:700px;margin:0 auto;padding:20px
}

/* HEADER */
.header{text-align:center;padding:40px 0 20px;position:relative}
.header-lottie{width:100px;height:100px;margin:0 auto 10px}
.header h1{
    font-family:'Orbitron',sans-serif;
    font-size:32px;font-weight:900;
    background:linear-gradient(135deg,#a78bfa,#06b6d4,#f472b6);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    text-shadow:none;
    filter:drop-shadow(0 0 20px rgba(124,58,237,0.8));
    animation:neonPulse 2s ease-in-out infinite alternate;
    letter-spacing:2px
}
@keyframes neonPulse{
    from{filter:drop-shadow(0 0 10px rgba(124,58,237,0.6))}
    to{filter:drop-shadow(0 0 30px rgba(6,182,212,0.9))}
}
.header p{color:#555;font-size:13px;margin-top:8px;letter-spacing:1px}

/* GLASS CARD */
.card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(124,58,237,0.3);
    border-radius:24px;padding:30px;margin:15px 0;
    backdrop-filter:blur(15px);
    box-shadow:0 8px 32px rgba(0,0,0,0.5),
               0 0 0 1px rgba(124,58,237,0.1),
               inset 0 1px 0 rgba(255,255,255,0.05)
}

label{
    color:#a78bfa;font-weight:600;font-size:11px;
    display:block;margin-bottom:8px;
    text-transform:uppercase;letter-spacing:2px
}

input,textarea{
    width:100%;padding:14px 16px;border-radius:12px;
    border:1px solid rgba(124,58,237,0.2);
    background:rgba(0,0,0,0.4);
    color:white;font-size:14px;font-family:'Poppins',sans-serif;
    margin-bottom:20px;
    transition:all 0.3s ease;
    outline:none
}
input:focus,textarea:focus{
    border-color:#06b6d4;
    background:rgba(6,182,212,0.05);
    box-shadow:0 0 0 3px rgba(6,182,212,0.15),
               0 0 20px rgba(6,182,212,0.2)
}
textarea{height:110px;resize:none}
input::placeholder,textarea::placeholder{color:#333}

/* GENERATE BUTTON */
#genBtn{
    width:100%;padding:18px;
    background:linear-gradient(135deg,#7c3aed,#06b6d4);
    color:white;border:none;border-radius:14px;
    font-size:16px;font-weight:700;
    font-family:'Orbitron',sans-serif;
    letter-spacing:1px;cursor:pointer;
    position:relative;overflow:hidden;
    box-shadow:0 0 30px rgba(124,58,237,0.5);
    animation:btnPulse 2s ease-in-out infinite
}
@keyframes btnPulse{
    0%,100%{box-shadow:0 0 20px rgba(124,58,237,0.5),0 0 40px rgba(124,58,237,0.2)}
    50%{box-shadow:0 0 40px rgba(6,182,212,0.7),0 0 80px rgba(6,182,212,0.3)}
}
#genBtn::after{
    content:'';position:absolute;
    top:-50%;left:-60%;
    width:200%;height:200%;
    background:linear-gradient(transparent,rgba(255,255,255,0.08),transparent);
    transform:rotate(30deg);
    animation:shimmer 3s linear infinite
}
@keyframes shimmer{
    0%{left:-60%}100%{left:100%}
}

/* LOADING */
#loading{text-align:center;padding:30px;display:none}
.spinner{
    width:60px;height:60px;
    border:2px solid rgba(124,58,237,0.2);
    border-top:2px solid #a78bfa;
    border-right:2px solid #06b6d4;
    border-radius:50%;
    animation:spin 0.8s linear infinite;
    margin:0 auto 15px;
    box-shadow:0 0 30px rgba(124,58,237,0.4)
}
@keyframes spin{to{transform:rotate(360deg)}}
#loading p{
    color:#a78bfa;font-size:13px;
    font-family:'Orbitron',sans-serif;
    letter-spacing:1px;
    animation:loadingPulse 1.5s ease infinite
}
@keyframes loadingPulse{0%,100%{opacity:1}50%{opacity:0.3}}

/* OUTPUT */
.output{
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(6,182,212,0.3);
    border-radius:24px;padding:25px;
    margin:15px 0;display:none;
    backdrop-filter:blur(15px);
    box-shadow:0 0 40px rgba(6,182,212,0.1),
               inset 0 1px 0 rgba(255,255,255,0.05);
    animation:slideUp 0.6s ease
}
@keyframes slideUp{
    from{opacity:0;transform:translateY(40px)}
    to{opacity:1;transform:translateY(0)}
}
.output-header{
    display:flex;align-items:center;gap:10px;margin-bottom:15px
}
.result-lottie{width:50px;height:50px}
.output h3{
    font-family:'Orbitron',sans-serif;
    font-size:14px;font-weight:700;
    background:linear-gradient(135deg,#a78bfa,#06b6d4);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    letter-spacing:1px
}
.proposal-text{
    background:rgba(0,0,0,0.4);padding:20px;
    border-radius:14px;line-height:1.9;color:#ccc;
    font-size:14px;
    border-left:2px solid #7c3aed;
    border-bottom:1px solid rgba(124,58,237,0.2);
    min-height:50px
}
#copyBtn{
    margin-top:15px;width:100%;padding:15px;
    background:rgba(5,150,105,0.2);
    border:1px solid rgba(5,150,105,0.4);
    color:#34d399;border-radius:12px;
    font-size:14px;font-weight:600;
    font-family:'Poppins',sans-serif;
    transition:all 0.3s
}
#copyBtn:active{background:rgba(5,150,105,0.4)}

/* CONFETTI */
.confetti-piece{
    position:fixed;width:8px;height:8px;
    border-radius:2px;z-index:9999;
    pointer-events:none;
    animation:confettiFall 2.5s ease-in forwards
}
@keyframes confettiFall{
    0%{transform:translateY(-20px) rotate(0deg);opacity:1}
    100%{transform:translateY(100vh) rotate(720deg);opacity:0}
}

/* STICKERS */
.stickers{
    text-align:center;padding:10px 0 30px
}
.sticker{
    font-size:30px;display:inline-block;
    margin:6px;animation:stickerFloat 3s ease-in-out infinite
}
.sticker:nth-child(1){animation-delay:0s}
.sticker:nth-child(2){animation-delay:0.4s}
.sticker:nth-child(3){animation-delay:0.8s}
.sticker:nth-child(4){animation-delay:1.2s}
.sticker:nth-child(5){animation-delay:1.6s}
@keyframes stickerFloat{
    0%,100%{transform:translateY(0) rotate(-5deg)}
    50%{transform:translateY(-15px) rotate(5deg)}
}
</style>
</head>
<body>

<!-- BLOBS -->
<div class="blob blob1"></div>
<div class="blob blob2"></div>

<!-- POPUP -->
<div class="popup-overlay" id="welcomePopup">
    <div class="popup-box">
        <div class="popup-lottie" id="popupLottie"></div>
        <h1>PROPOSAL AI</h1>
        <p>Next-gen AI powered proposal generator. Win more clients instantly!</p>
        <div class="badge">⚡ FREE • UNLIMITED • INSTANT</div>
        <button class="popup-btn" id="startBtn">🚀 LAUNCH APP</button>
    </div>
</div>

<div class="container">
    <!-- HEADER -->
    <div class="header">
        <div class="header-lottie" id="headerLottie"></div>
        <h1>PROPOSAL WRITER</h1>
        <p>[ AI POWERED • CYBERPUNK EDITION ]</p>
    </div>

    <!-- FORM CARD -->
    <div class="card">
        <label>⬡ Project Title</label>
        <input type="text" id="title" placeholder="e.g. Build a landing page for my bakery"/>
        <label>⬡ Project Description</label>
        <textarea id="description" placeholder="Describe what the client needs..."></textarea>
        <label>⬡ Your Skills</label>
        <input type="text" id="skills" placeholder="e.g. Python, Web Design, React"/>
        <button id="genBtn">⚡ GENERATE WINNING PROPOSAL</button>
    </div>

    <!-- LOADING -->
    <div id="loading">
        <div class="spinner"></div>
        <p>[ AI PROCESSING... ]</p>
    </div>

    <!-- OUTPUT -->
    <div class="output" id="output">
        <div class="output-header">
            <div class="result-lottie" id="resultLottie"></div>
            <h3>◈ YOUR WINNING PROPOSAL</h3>
        </div>
        <div class="proposal-text" id="proposalText"></div>
        <button id="copyBtn">📋 Copy to Clipboard</button>
    </div>

    <!-- STICKERS -->
    <div class="stickers">
        <span class="sticker">🚀</span>
        <span class="sticker">💡</span>
        <span class="sticker">🎯</span>
        <span class="sticker">⚡</span>
        <span class="sticker">🏆</span>
    </div>
</div>

<script>
// LOTTIE ANIMATIONS
lottie.loadAnimation({
    container:document.getElementById('popupLottie'),
    renderer:'svg',path:'https://assets9.lottiefiles.com/packages/lf20_myejiggj.json',
    loop:true,autoplay:true
});
lottie.loadAnimation({
    container:document.getElementById('headerLottie'),
    renderer:'svg',path:'https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json',
    loop:true,autoplay:true
});
lottie.loadAnimation({
    container:document.getElementById('resultLottie'),
    renderer:'svg',path:'https://assets10.lottiefiles.com/packages/lf20_touohxv0.json',
    loop:true,autoplay:true
});

// POPUP
document.getElementById("startBtn").addEventListener("touchend",function(e){
    e.preventDefault();
    document.getElementById("welcomePopup").style.display="none";
});
document.getElementById("startBtn").addEventListener("click",function(){
    document.getElementById("welcomePopup").style.display="none";
});

// CONFETTI
function launchConfetti(){
    var colors=["#a78bfa","#06b6d4","#f472b6","#fbbf24","#34d399"];
    for(var i=0;i<60;i++){
        var piece=document.createElement("div");
        piece.className="confetti-piece";
        piece.style.left=Math.random()*100+"vw";
        piece.style.background=colors[Math.floor(Math.random()*colors.length)];
        piece.style.animationDelay=Math.random()*1.5+"s";
        piece.style.animationDuration=(2+Math.random()*2)+"s";
        piece.style.width=(5+Math.random()*8)+"px";
        piece.style.height=(5+Math.random()*8)+"px";
        piece.style.borderRadius=Math.random()>0.5?"50%":"2px";
        document.body.appendChild(piece);
        setTimeout(function(p){return function(){p.remove()}}(piece),4000);
    }
}

// TYPEWRITER
function typeWriter(text,element,speed){
    element.innerText="";
    var i=0;
    function type(){
        if(i<text.length){
            element.innerText+=text.charAt(i);
            i++;setTimeout(type,speed);
        }
    }
    type();
}

// COPY
function copyProposal(){
    var text=document.getElementById("proposalText").innerText;
    navigator.clipboard.writeText(text).then(function(){alert("✅ Copied!");});
}
document.getElementById("copyBtn").addEventListener("touchend",function(e){e.preventDefault();copyProposal();});
document.getElementById("copyBtn").addEventListener("click",function(){copyProposal();});

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
            typeWriter(data.proposal,document.getElementById("proposalText"),18);
            launchConfetti();
        }else{alert("Error: "+JSON.stringify(data));}
    })
    .catch(function(err){
        document.getElementById("loading").style.display="none";
        alert("Error: "+err.message);
    });
}
document.getElementById("genBtn").addEventListener("touchend",function(e){e.preventDefault();generate();});
document.getElementById("genBtn").addEventListener("click",function(){generate();});
</script>
</body>
</html>"""

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = "Write a professional freelancer proposal for:\nProject: " + str(data.get("title")) + "\nDescription: " + str(data.get("description")) + "\nSkills: " + str(data.get("skills")) + "\nMax 200 words. Be professional, confident and persuasive."
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
            return jsonify({"proposal": proposal})
        else:
            return jsonify({"proposal": "API Error: " + str(result)})
    except Exception as e:
        return jsonify({"proposal": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
