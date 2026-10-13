from flask import Flask, render_template_string, request, jsonify
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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ஸ்ரீ அஷ்டபுஜ மகா காளிகம்பாள்</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Poppins',sans-serif}
body{min-height:100vh;background: linear-gradient(-45deg,#1a0000,#4c0519,#000000,#7f1d1d);background-size:400% 400%;animation:bgMove 12s ease infinite;display:flex;flex-direction:column;align-items:center}
@keyframes bgMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.header{width:100%;padding:25px;text-align:center;color:white;background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,0.1)}
.header h1{font-size:26px;font-weight:700;text-shadow:0 0 10px #ff0040,0 0 20px #ff0040;animation:rgbGlow 3s infinite alternate;line-height:1.3}
@keyframes rgbGlow{0%{text-shadow:0 0 10px #ff0040,0 0 20px #ff0040}50%{text-shadow:0 0 10px #00f2ff,0 0 20px #00f2ff,0 0 40px #00f2ff}100%{text-shadow:0 0 10px #ffea00,0 0 20px #ffea00}}
.card{width:92%;max-width:440px;margin:20px 0;padding:25px;background:rgba(255,255,255,0.08);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-radius:22px;border:1px solid rgba(255,255,255,0.18);box-shadow:0 8px 32px rgba(0,0,0,0.4);animation:float 5s ease-in-out infinite;color:white}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
label{font-size:13px;opacity:0.9;margin-left:5px;display:block;margin-top:5px}
input,select{width:100%;padding:14px;margin:6px 0 14px 0;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:12px;color:white;outline:none;transition:0.3s;font-size:15px}
input:focus,select:focus{border-color:#00f2ff;box-shadow:0 0 15px #00f2ff;background:rgba(255,255,255,0.15)}
input::placeholder{color:rgba(255,255,255,0.5)}
select option{color:black}
.glass-btn{width:100%;padding:15px;border:none;border-radius:14px;background:linear-gradient(135deg,rgba(255,255,255,0.25),rgba(255,255,255,0.05));backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.3);color:white;font-size:18px;font-weight:700;cursor:pointer;box-shadow:0 0 20px rgba(255,0,64,0.4),inset 0 0 10px rgba(255,255,255,0.2);transition:0.4s;position:relative;overflow:hidden}
.glass-btn::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.4),transparent);transition:0.5s}
.glass-btn:hover::before{left:100%}
.glass-btn:hover{transform:scale(1.03);box-shadow:0 0 30px #00f2ff,0 0 50px #00f2ff}
.token-card{margin-top:20px;padding:25px;background:rgba(0,0,0,0.4);border:1px solid #00f2ff;border-radius:18px;box-shadow:0 0 30px rgba(0,242,255,0.5);text-align:center;animation:pop 0.6s ease}
@keyframes pop{from{transform:scale(0.8);opacity:0}to{transform:scale(1);opacity:1}}
.big-token{font-size:32px;font-weight:800;color:#00f2ff;text-shadow:0 0 15px #00f2ff,0 0 30px #00f2ff;margin:10px 0;word-break:break-all}
</style>
</head>
<body>
<div class="header">
  <h1>ஸ்ரீ அஷ்டபுஜ<br>மகா காளிகம்பாள் துணை</h1>
  <p style="margin-top:5px;opacity:0.8">சூலகிரி - செவ்வாய் & வெள்ளி மட்டும்</p>
</div>
<div class="card">
  <form id="bookForm">
    <label>பெயர்</label>
    <input type="text" id="name" placeholder="உங்கள் பெயர்" required>
    <label>ஊர்</label>
    <input type="text" id="place" placeholder="உங்கள் ஊர்" required>
    <label>போன் நம்பர்</label>
    <input type="tel" id="phone" placeholder="10 இலக்க எண்" pattern="[0-9]{10}" required>
    <label>தரிசன தேதி (செவ்வாய் / வெள்ளி மட்டும்)</label>
    <select id="date" required></select>
    <button class="glass-btn" type="submit">✨ டோக்கன் பெறுக ✨</button>
  </form>
  <div id="result"></div>
</div>
<script>
const dateSelect = document.getElementById('date');
let today = new Date();
for(let i=0;i<60;i++){
  let d = new Date();
  d.setDate(today.getDate()+i);
  let day = d.getDay();
  if(day===2 || day===5){
    let dateStr = d.toISOString().split('T')[0];
    let tamilDay = day===2? 'செவ்வாய்' : 'வெள்ளி';
    let display = d.toLocaleDateString('ta-IN',{day:'numeric',month:'long',year:'numeric'}) + ' - ' + tamilDay;
    let opt = document.createElement('option');
    opt.value = dateStr;
    opt.textContent = display;
    dateSelect.appendChild(opt);
  }
}
document.getElementById('bookForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const data = {
    name: document.getElementById('name').value,
    place: document.getElementById('place').value,
    phone: document.getElementById('phone').value,
    date: document.getElementById('date').value
  };
  document.getElementById('result').innerHTML = "<p style='text-align:center;margin-top:15px'>⏳ பதிவு செய்கிறது...</p>";
  const res = await fetch('/api/book', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)});
  const result = await res.json();
  if(result.status==='exists'){
    document.getElementById('result').innerHTML = `<div class="token-card" style="border-color:#ff0040;box-shadow:0 0 20px #ff0040"><h3 style="color:#ff6b6b">⚠️ ஏற்கனவே பதிவு உள்ளது</h3><p>டோக்கன்: <b>${result.token}</b></p><p>${result.date}</p></div>`;
  } else if(result.status==='success'){
    document.getElementById('result').innerHTML = `<div class="token-card"><p>🙏 ஸ்ரீ காளிகம்பாள் துணை</p><div class="big-token">${result.token}</div><p><b>${result.name}</b> | ${result.place}</p><p>📅 ${result.date} (${result.day})</p><p>📱 ${result.phone}</p><hr style="margin:12px 0;opacity:0.2"><p style="font-size:11px;opacity:0.8">Screenshot எடுத்து கோயிலில் காட்டவும்</p></div>`;
    document.getElementById('bookForm').reset();
  }
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/book', methods=['POST'])
def api_book():
    data = request.json
    bookings = load_data()
    name = data.get('name','').strip()
    place = data.get('place','').strip()
    phone = data.get('phone','').strip()
    date_str = data.get('date','').strip()

    if not name or not place or not phone or not date_str:
        return jsonify({"status":"error"}), 400

    for b in bookings:
        if b['phone'] == phone and b['date'] == date_str:
            return jsonify({"status":"exists", "token": b['token'], "date": b['date']})

    max_num = 0
    for b in bookings:
        if b['date'] == date_str:
            try:
                num = int(b['token'].split('_')[-1])
                if num > max_num:
                    max_num = num
            except:
                continue

    next_number = max_num + 1
    token_no = f"Token_No_{next_number:03d}"

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    tamil_day = "செவ்வாய்" if dt.weekday() == 1 else "வெள்ளி"

    new_booking = {"token":token_no,"name":name,"place":place,"phone":phone,"date":date_str,"day":tamil_day,"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    bookings.append(new_booking)
    save_data(bookings)
    return jsonify({"status":"success", **new_booking})

@app.route('/admin')
def admin():
    bookings = load_data()
    html = f"<meta name='viewport' content='width=device-width, initial-scale=1'><h2>Admin - Total Bookings: {len(bookings)}</h2><table border=1 cellpadding=8 style='border-collapse:collapse;width:100%;font-family:Arial'><tr><th>Token</th><th>Date</th><th>Day</th><th>Name</th><th>Place</th><th>Phone</th></tr>"
    for b in sorted(bookings, key=lambda x: (x['date'], x['token'])):
        html+=f"<tr><td>{b['token']}</td><td>{b['date']}</td><td>{b['day']}</td><td>{b['name']}</td><td>{b['place']}</td><td>{b['phone']}</td></tr>"
    html+="</table><p><a href='/'>Back to Home</a></p>"
    return html

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    return "Running", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
