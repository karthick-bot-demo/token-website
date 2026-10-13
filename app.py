import flask
from flask import Flask, render_template_string
from datetime import datetime
import json, os

app = Flask(__name__)
DATA_FILE = "bookings.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ஸ்ரீ அஷ்டபுஜ மகா காளிகாம்பாள்</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Noto Sans Tamil',sans-serif}
body{min-height:100vh;background:linear-gradient(135deg,#1a0a2e,#4a1942,#8b2252);color:white;padding:15px}
.header{margin:25px 0;text-align:center}
.header h1{font-size:26px;font-weight:700;line-height:1.3}
.header p{margin-top:5px;opacity:0.8}
.card{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:20px;max-width:440px;margin:20px auto;border:1px solid rgba(255,255,255,0.2)}
.input{width:100%;padding:14px;margin:8px 0;border-radius:12px;border:none;font-size:16px}
.btn{width:100%;padding:14px;background:linear-gradient(90deg,#ff512f,#dd2476);border:none;border-radius:12px;color:white;font-size:18px;font-weight:700;margin-top:10px}
.token-card{margin-top:20px;padding:20px;background:rgba(0,0,0,0.3);border-radius:15px;border:2px dashed #ffcc00;text-align:center}
.big-token{font-size:32px;font-weight:800;color:#ffcc00}
</style>
</head>
<body>
<div class="header">
<h1>🔱 ஸ்ரீ அஷ்டபுஜ மகா காளிகாம்பாள் 🔱</h1>
<p style="margin-top:5px;opacity:0.9;font-size:18px">பு.ஆதனூர்</p>
<p style="font-size:13px;opacity:0.7;margin-top:3px">செவ்வாய் & வெள்ளி மட்டும்</p>
</div>
<div class="card">
<form id="bookForm">
<label>பெயர்</label>
<input class="input" type="text" id="name" placeholder="உங்கள் பெயர்" required>
<label>ஊர்</label>
<input class="input" type="text" id="place" placeholder="ஊர்" required>
<label>செல்</label>
<input class="input" type="tel" id="phone" placeholder="Mobile Number" required>
<label>தேதி</label>
<input class="input" type="date" id="date" required>
<select class="input" id="slot" required><option value="">நேரம் தேர்வு செய்க</option><option>காலை 6-8</option><option>காலை 8-10</option></select>
<button class="btn" type="submit">டோக்கன் பெறுக</button>
</form>
<div id="result"></div>
</div>
<script>
let today = new Date();
document.getElementById('date').min = today.toISOString().split('T')[0];
for(let i=0;i<60;i++){
 let d = new Date(); d.setDate(today.getDate()+i);
 if(d.getDay()==2 || d.getDay()==5){
   let opt = document.createElement('option');
   opt.value = d.toISOString().split('T')[0];
   opt.text = d.toLocaleDateString('ta-IN',{weekday:'long',day:'numeric',month:'long'});
   document.getElementById('date').appendChild(opt);
 }
}
document.getElementById('bookForm').addEventListener('submit', async (e)=>{
 e.preventDefault();
 let res = await fetch('/book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('name').value,place:document.getElementById('place').value,phone:document.getElementById('phone').value,date:document.getElementById('date').value,slot:document.getElementById('slot').value})});
 let data = await res.json();
 document.getElementById('result').innerHTML = `<div class='token-card'><p>டோக்கன் பெறப்பட்டது!</p><div class='big-token'>${data.token}</div><p>${data.name} | ${data.place}</p><p>${data.date} - ${data.slot}</p></div>`;
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/book', methods=['POST'])
def book():
    d = flask.request.json
    all_data = load_data()
    token_no = f"Token_No_{len(all_data)+1:03d}"
    entry = {**d, "token": token_no, "time": datetime.now().strftime("%d-%m-%Y %H:%M")}
    all_data.append(entry)
    save_data(all_data)
    return flask.jsonify(entry)

@app.route('/admin')
def admin():
    data = load_data()
    html = "<h2>Bookings</h2><table border=1><tr><th>Token</th><th>Name</th><th>Place</th><th>Phone</th><th>Date</th></tr>"
    for b in data:
        html += f"<tr><td>{b.get('token')}</td><td>{b.get('name')}</td><td>{b.get('place')}</td><td>{b.get('phone')}</td><td>{b.get('date')}</td></tr>"
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run()
