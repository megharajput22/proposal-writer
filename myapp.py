from flask import Flask, request, jsonify
import requests as req

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html>
<head>
<title>Proposal Writer</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial;background:#0f0f1a;color:white;padding:20px}
h1{color:#6c63ff;text-align:center;padding:20px 0}
.sub{color:#aaa;text-align:center;margin-bottom:20px}
.card{background:#1a1a2e;border-radius:15px;padding:20px;margin-bottom:20px}
label{color:#6c63ff;font-weight:bold;display:block;margin-bottom:8px}
input,textarea{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0f0f1a;color:white;font-size:14px;margin-bottom:15px}
textarea{height:100px;resize:none}
#genBtn{width:100%;padding:18px;background:#6c63ff;color:white;border:none;border-radius:10px;font-size:18px;font-weight:bold}
.output{background:#1a1a2e;border-radius:15px;padding:20px;margin-top:20px;display:none}
.output h3{color:#6c63ff;margin-bottom:15px}
.proposal-text{background:#0f0f1a;padding:15px;border-radius:10px;line-height:1.6;color:#ddd;white-space:pre-wrap}
#copyBtn{margin-top:15px;width:100%;padding:15px;background:#28a745;color:white;border:none;border-radius:10px;font-size:16px;font-weight:bold}
#loading{text-align:center;color:#6c63ff;padding:20px;display:none;font-size:18px}
</style>
</head>
<body>

<h1>💼 Proposal Writer</h1>
<p class="sub">AI powered winning proposals</p>

<div class="card">
<label>Project Title</label>
<input type="text" id="title" placeholder="e.g. Build a website"/>
<label>Project Description</label>
<textarea id="description" placeholder="What does client need..."></textarea>
<label>Your Skills</label>
<input type="text" id="skills" placeholder="e.g. Python, Web Design"/>
<button id="genBtn">⚡ Generate Proposal</button>
</div>

<div id="loading">⏳ Generating...</div>

<div class="output" id="output">
<h3>✅ Your Proposal</h3>
<div class="proposal-text" id="proposalText"></div>
<button id="copyBtn">📋 Copy Proposal</button>
</div>

<script>
document.getElementById("copyBtn").addEventListener("touchend", function(e){
    e.preventDefault();
    var text = document.getElementById("proposalText").innerText;
    navigator.clipboard.writeText(text).then(function(){ alert("Copied!"); });
});

document.getElementById("genBtn").addEventListener("touchend", function(e){
    e.preventDefault();

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
});
</script>
</body>
</html>"""

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = "Write a professional freelancer proposal for:\nProject: " + str(data.get("title")) + "\nDescription: " + str(data.get("description")) + "\nSkills: " + str(data.get("skills")) + "\nMax 200 words. Be professional and confident."

    try:
        response = req.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + API_KEY,
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Proposal Writer"
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
    app.run(debug=True, host="127.0.0.1", port=5000)