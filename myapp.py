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
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Poppins',sans-serif;background:#0a0a1a;color:white;min-height:100vh}

/* ANIMATED BACKGROUND */
body::before{
    content:'';position:fixed;top:0;left:0;width:100%;height:100%;
    background:radial-gradient(ellipse at top,#1a0533 0%,#0a0a1a 70%);
    z-index:-1
}

/* POPUP */
.popup-overlay{
    position:fixed;top:0;left:0;width:100%;height:100%;
    background:rgba(0,0,0,0.85);
    display:flex;align-items:center;justify-content:center;
    z-index:999;backdrop-filter:blur(5px)
}
.popup-box{
    background:linear-gradient(135deg,#1a0533,#0d1f4a);
    border:1px solid rgba(139,92,246,0.5);
    border-radius:24px;padding:40px 30px;text-align:center;
    max-width:340px;width:90%;
    animation:popIn 0.6s cubic-bezier(0.175,0.885,0.32,1.275)
}
@keyframes popIn{
    from{transform:scale(0.3) rotate(-10deg);opacity:0}
    to{transform:scale(1) rotate(0deg);opacity:1}
}
.popup-emoji{font-size:60px;margin-bottom:15px;display:block;animation:bounce 2s infinite}
@keyframes bounce{
    0%,100%{transform:translateY(0)}
    50%{transform:translateY(-10px)}
}
.popup-box h1{
    font-size:26px;font-weight:700;margin-bottom:10px;
    background:linear-gradient(135deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.popup-box p{color:#aaa;font-size:14px;margin-bottom:20px;line-height:1.6}
.badge{
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    color:white;padding:8px 20px;border-radius:20px;
    font-weight:600;font-size:13px;display:inline-block;margin-bottom:20px
}
.popup-btn{
    width:100%;padding:15px;
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    color:white;border:none;border-radius:12px;
    font-size:16px;font-weight:600;font-family:'Poppins',sans-serif;
    cursor:pointer;transition:transform 0.2s;margin-top:10px
}
.popup-btn:active{transform:scale(0.97)}

/* HEADER */
.header{
    text-align:center;padding:40px 20px 20px;
    background:linear-gradient(180deg,rgba(124,58,237,0.1) 0%,transparent 100%)
}
.header h1{
    font-size:32px;font-weight:700;
    background:linear-gradient(135deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.header p{color:#888;font-size:14px;margin-top:8px}

/* CARD */
.card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;padding:25px;margin:15px;
    backdrop-filter:blur(10px)
}
label{
    color:#a78bfa;font-weight:600;font-size:13px;
    display:block;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px
}
input,textarea{
    width:100%;padding:14px;border-radius:12px;
    border:1px solid rgba(139,92,246,0.3);
    background:rgba(255,255,255,0.05);
    color:white;font-size:14px;font-family:'Poppins',sans-serif;
    margin-bottom:18px;transition:border 0.3s
}
input:focus,textarea:focus{
    outline:none;border-color:#7c3aed;
    background:rgba(124,58,237,0.1)
}
textarea{height:100px;resize:none}

/* BUTTON */
#genBtn{
    width:100%;padding:18px;
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    color:white;border:none;border-radius:14px;
    font-size:17px;font-weight:700;font-family:'Poppins',sans-serif;
    letter-spacing:0.5px;position:relative;overflow:hidden
}
#genBtn::before{
    content:'';position:absolute;top:-50%;left:-50%;
    width:200%;height:200%;
    background:linear-gradient(transparent,rgba(255,255,255,0.1),transparent);
    transform:rotate(45deg);transition:0.5s
}

/* LOADING */
#loading{
    text-align:center;padding:30px;display:none
}
.spinner{
    width:50px;height:50px;border:3px solid rgba(124,58,237,0.3);
    border-top:3px solid #7c3aed;border-radius:50%;
    animation:spin 1s linear infinite;margin:0 auto 15px
}
@keyframes spin{to{transform:rotate(360deg)}}
#loading p{color:#a78bfa;font-size:14px}

/* OUTPUT */
.output{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(139,92,246,0.3);
    border-radius:20px;padding:25px;margin:15px;display:none;
    animation:fadeIn 0.5s ease
}
@keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.output h3{
    font-size:16px;font-weight:600;margin-bottom:15px;
    background:linear-gradient(135deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.proposal-text{
    background:rgba(0,0,0,0.3);padding:18px;
    border-radius:12px;line-height:1.8;color:#ddd;
    font-size:14px;white-space:pre-wrap;border-left:3px solid #7c3aed
}
#copyBtn{
    margin-top:15px;width:100%;padding:15px;
    background:linear-gradient(135deg,#059669,#0d9488);
    color:white;border:none;border-radius:12px;
    font-size:15px;font-weight:600;font-family:'Poppins',sans-serif
}

/* FOOTER */
.footer{text-align:center;padding:20px;color:#444;font-size:12px}
</style>
</head>
<body>

<!-- WELCOME POPUP -->
<div class="popup-overlay" id="welcomePopup">
    <div class="popup-box">
        <span class="popup-emoji">💼</span>
        <h1>Proposal Writer AI</h1>
        <p>Generate winning freelancer proposals instantly using the power of AI!</p>
        <div class="badge">✨ 100% Free Forever</div>
        <p style="font-size:12px;color:#666">No signup needed. Just enter details and get your proposal!</p>
        <button class="popup-btn" id="startBtn">🚀 Start Writing Proposals!</button>
    </div>
</div>

<div class="header">
    <h1>💼 Proposal Writer AI</h1>
    <p>Generate winning proposals in seconds</p>
</div>

<div class="card">
    <label>📌 Project Title</label>
    <input type="text" id="title" placeholder="e.g. Build a landing page for my bakery"/>
    <label>📝 Project Description</label>
    <textarea id="description" placeholder="Describe what the client needs..."></textarea>
    <label>⚡ Your Skills</label>
    <input type="text" id="skills" placeholder="e.g. Python, Web Design, React"/>
    <button id="genBtn">✨ Generate Winning Proposal</button>
</div>

<div id="loading">
    <div class="spinner"></div>
    <p>AI is crafting your proposal...</p>
</div>

<div class="output" id="output">
    <h3>✅ Your Winning Proposal</h3>
    <div class="proposal-text" id="proposalText"></div>
    <button id="copyBtn">📋 Copy Proposal</button>
</div>

<div class="footer">Made with ❤️ by Proposal Writer AI</div>

<script>
document.getElementById("startBtn").addEventListener("touchend", function(e){
    e.preventDefault();
    document.getElementById("welcomePopup").style.display = "none";
});

document.getElementById("startBtn").addEventListener("click", function(){
    document.getElementById("welcomePopup").style.display = "none";
});

document.getElementById("copyBtn").addEventListener("touchend", function(e){
    e.preventDefault();
    copyProposal();
});

document.getElementById("copyBtn").addEventListener("click", function(){
    copyProposal();
});

function copyProposal(){
    var text = document.getElementById("proposalText").innerText;
    navigator.clipboard.writeText(text).then(function(){
        alert("✅ Proposal Copied!");
    });
}

document.getElementById("genBtn").addEventListener("touchend", function(e){
    e.preventDefault();
    generate();
});

document.getElementById("genBtn").addEventListener("click", function(){
    generate();
});

function generate(){
    var title = document.getElementById("title").value.trim();
    var desc = document.getElementById("description").value.trim();
    var skills = document.getElementById("skills").value.trim();

    if(!title || !desc || !skills){
        alert("Please fill all fields!");
        return;
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("output").style.display = "none";

    fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title:title, description:desc, skills:skills})
    })
    .then(function(res){ return res.json(); })
    .then(function(data){
        document.getElementById("loading").style.display = "none";
        if(data.proposal){
            document.getElementById("proposalText").innerText = data.proposal;
            document.getElementById("output").style.display = "block";
        } else {
            alert("Error: " + JSON.stringify(data));
        }
    })
    .catch(function(err){
        document.getElementById("loading").style.display = "none";
        alert("Error: " + err.message);
    });
}
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
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Proposal Writer AI"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        result = response.json()
        print("API Response:", result)
        if "choices" in result:
            proposal = result["choices"][0]["message"]["content"]
            return jsonify({"proposal": proposal})
        else:
            return jsonify({"proposal": "API Error: " + str(result)})
    except Exception as e:
        return jsonify({"proposal": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
