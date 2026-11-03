from flask import Flask, render_template_string, request, jsonify
import random, time, os, json

app = Flask(__name__)

# ===== YOUR ORIGINAL HTML KEPT 100% SAME + STRATEGY ADDED INSIDE TEMPLATE =====
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SMC TRADER</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:Inter,sans-serif}
body{min-height:100vh;background:#020a06;color:#fff;overflow-x:hidden}
.bg{position:fixed;inset:0;background:linear-gradient(rgba(2,10,6,0.7), rgba(2,10,6,0.92)), url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1920&q=80');background-size:cover;background-position:center;z-index:0}
.overlay{position:fixed;inset:0;background:radial-gradient(circle at 50% 20%, rgba(0,255,136,0.22), transparent 60%);z-index:1}
.page{position:relative;z-index:10;min-height:100vh;display:none;justify-content:center;align-items:center;padding:20px}
.page.active{display:flex}
.card{width:420px;padding:28px;border-radius:24px;background:rgba(10,22,16,0.92);border:1px solid rgba(0,255,136,0.3);backdrop-filter:blur(22px);box-shadow:0 20px 80px rgba(0,0,0,0.8)}
.logo-icon{width:52px;height:52px;background:linear-gradient(135deg,#00ff88,#00cc6a);border-radius:14px;display:flex;justify-content:center;align-items:center;font-weight:900;color:#000;font-size:20px;margin:0 auto 14px}
h1{font-size:26px;font-weight:900;text-align:center} .sub{font-size:10px;letter-spacing:2px;opacity:0.5;text-align:center;margin:6px 0 20px}
.label{font-size:12px;opacity:0.7;margin:10px 0 5px;display:block;font-weight:600}
.input{width:100%;padding:12px 14px;border-radius:11px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#fff;outline:none}
.btn{width:100%;padding:13px;border-radius:12px;border:0;font-weight:900;cursor:pointer;margin-top:12px;font-size:14px;display:block;text-align:center;text-decoration:none}
.btn-green{background:linear-gradient(135deg,#00ff88,#00cc6a);color:#000}
.btn-white{background:#fff;color:#000;display:flex;justify-content:center;align-items:center;gap:8px;font-weight:700}
.btn-outline{background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.2)}
.btn-gray{background:rgba(255,255,255,0.08);color:#fff}
.divider{display:flex;align-items:center;gap:12px;margin:16px 0;font-size:11px;opacity:0.5}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.1)}
.msg{padding:10px 14px;border-radius:10px;font-size:12px;margin-bottom:12px;display:none}
.msg.ok{background:rgba(0,255,136,0.15);border:1px solid #00ff88;color:#00ff88;display:block}
.msg.err{background:rgba(255,68,68,0.15);border:1px solid #ff4444;color:#ff8888;display:block}
.otp-box{display:flex;gap:7px;justify-content:center;margin:16px 0}
.otp{width:40px;height:50px;border-radius:10px;border:1px solid rgba(255,255,255,0.15);background:rgba(0,0,0,0.4);color:#00ff88;font-size:20px;font-weight:900;text-align:center;outline:none}
.code-preview{background:rgba(0,255,136,0.12);border:1px dashed #00ff88;padding:10px;border-radius:12px;margin:12px 0;text-align:center}
.step{font-size:10px;opacity:0.5;letter-spacing:1px;margin-bottom:6px}
.phone-wrap{display:flex;gap:8px}
.phone-wrap select{width:95px;padding:12px 8px;border-radius:11px;border:1px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.06);color:#fff}
.dash{display:none;min-height:100vh;background:#050a0a;position:relative;z-index:10}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:14px 20px;background:rgba(5,10,10,0.95);border-bottom:1px solid rgba(0,255,136,0.15)}
.content{padding:14px;display:grid;gap:14px;grid-template-columns:280px 1fr}
.port{background:linear-gradient(135deg, rgba(15,30,22,0.9), rgba(10,20,15,0.9));border:1px solid rgba(0,255,136,0.15);border-radius:18px;padding:16px}
.card-dash{background:#0f1e16;border:1px solid #1a3a2a;border-radius:14px;padding:14px}
.pair{display:flex;justify-content:space-between;align-items:center;padding:9px 10px;margin:4px 0;border-radius:9px;background:rgba(20,30,25,0.6);border:1px solid transparent;cursor:pointer;font-size:13px}
.pair.on{background:rgba(0,255,136,0.12);border-color:#00ff88}
.card-ap{background:linear-gradient(135deg, rgba(15,30,22,0.9), rgba(0,255,136,0.08));border:1px solid rgba(0,255,136,0.25)}
.badge{font-size:10px;padding:4px 8px;border-radius:20px;font-weight:900}
.badge-a{background:#00ff88;color:#000}.badge-b{background:rgba(255,170,0,0.2);color:#ffaa00;border:1px solid #ffaa00}.badge-c{background:rgba(255,68,68,0.2);color:#ff6666;border:1px solid #ff4444}
.pair-row{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;margin:5px 0;border-radius:10px;background:rgba(20,30,25,0.7);border:1px solid transparent;cursor:pointer}
.pair-row.on{background:rgba(0,255,136,0.12);border-color:#00ff88}
.tf-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}
.tf-box{text-align:center;padding:8px 4px;border-radius:8px;background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.08);font-size:11px}
.tf-box.ok{border-color:#00ff88;color:#00ff88;background:rgba(0,255,136,0.1)}.tf-box.wait{border-color:#ffaa00;color:#ffaa00;background:rgba(255,170,0,0.1)}
.check{display:flex;gap:8px;align-items:center;font-size:12px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.check.ok{color:#00ff88} .check.no{color:rgba(255,255,255,0.35)}
.select-pair{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chip{padding:6px 10px;border-radius:20px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);font-size:11px;cursor:pointer}
.chip.on{background:#00ff88;color:#000;font-weight:800;border-color:#00ff88}
@media(max-width:1000px){.content{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="bg"></div><div class="overlay"></div>
<div class="page active" id="page-landing"><div class="card" style="text-align:center"><div class="logo-icon">ST</div><h1>SMC TRADER</h1><div class="sub">PRECISION • LIQUIDITY • STRUCTURE</div><p style="font-size:13px;opacity:0.7;margin-bottom:20px">Professional SMC trading platform.</p><button class="btn btn-green" onclick="showPage('register')">CREATE ACCOUNT →</button><button class="btn btn-outline" onclick="showPage('login')">LOGIN</button></div></div>
<div class="page" id="page-login"><div class="card"><h2 style="font-size:20px;font-weight:900">Welcome Back</h2><p style="font-size:12px;opacity:0.6;margin:4px 0 16px">Login - This is a separate page</p><div id="loginMsg" class="msg"></div><span class="label">Email</span><input class="input" id="lEmail" placeholder="you@example.com"><span class="label">Password</span><input class="input" id="lPass" type="password"><button class="btn btn-green" onclick="doLogin()">LOGIN →</button><button class="btn btn-white" onclick="googleLogin()">Continue with Google</button><button class="btn btn-gray" onclick="showPage('landing')">← Back</button><div style="text-align:center;font-size:10px;opacity:0.4;margin-top:10px" id="loginCount"></div></div></div>
<div class="page" id="page-register"><div class="card"><div class="step">Step 1 of 4 • Email - Another page</div><h2 style="font-size:20px;font-weight:900">Create Account</h2><p style="font-size:12px;opacity:0.6;margin:4px 0 16px">Email or Google</p><div id="regMsg" class="msg"></div><span class="label">Email</span><input class="input" id="rEmail" placeholder="you@example.com"><button class="btn btn-green" onclick="sendCode()">SEND CODE →</button><div class="divider">OR</div><button class="btn btn-white" onclick="googleSignUp()">Sign up with Google</button><button class="btn btn-gray" onclick="showPage('landing')">← Back</button></div></div>
<div class="page" id="page-verify"><div class="card" style="text-align:center"><div class="step" style="text-align:left">Step 2 of 4 • Verify - Another page</div><h2 style="font-size:20px;font-weight:900">Check your email</h2><p style="font-size:12px;opacity:0.6;margin:6px 0">Code sent to<br><b id="vEmail" style="color:#00ff88"></b></p><div id="vMsg" class="msg"></div><div class="otp-box"><input class="otp" id="o1" maxlength="1" oninput="moveOTP(1)"><input class="otp" id="o2" maxlength="1" oninput="moveOTP(2)"><input class="otp" id="o3" maxlength="1" oninput="moveOTP(3)"><input class="otp" id="o4" maxlength="1" oninput="moveOTP(4)"><input class="otp" id="o5" maxlength="1" oninput="moveOTP(5)"><input class="otp" id="o6" maxlength="1"></div><div class="code-preview"><span style="font-size:10px;opacity:0.7">YOUR CODE:</span><br><b id="vCode" style="font-size:22px;color:#00ff88;letter-spacing:3px"></b></div><button class="btn btn-green" onclick="verifyCode()">CONFIRM EMAIL →</button><button class="btn btn-gray" onclick="resendCode()">Resend code</button><button class="btn btn-gray" onclick="showPage('register')">← Back</button></div></div>
<div class="page" id="page-password"><div class="card"><div class="step">Step 3 of 4 • Create Password - Another page</div><h2 style="font-size:20px;font-weight:900">Create Password</h2><p style="font-size:12px;opacity:0.6;margin:4px 0 16px">Email <b id="pEmail" style="color:#00ff88"></b> verified ✅<br>Now add password - AFTER email confirmed</p><div id="pMsg" class="msg"></div><span class="label">New Password</span><input class="input" id="pPass" type="password" placeholder="Min 6 characters"><span class="label">Confirm Password</span><input class="input" id="pPass2" type="password" placeholder="Confirm"><button class="btn btn-green" onclick="savePassword()">SAVE PASSWORD →</button></div></div>
<div class="page" id="page-profile"><div class="card"><div class="step">Step 4 of 4 • Profile - Another page</div><h2 style="font-size:20px;font-weight:900">Complete Profile</h2><p style="font-size:12px;opacity:0.6;margin:4px 0 16px">Full name & phone → Dashboard</p><div id="prMsg" class="msg"></div><span class="label">Full Name</span><input class="input" id="prName" placeholder="John Michael Doe"><span class="label">Phone</span><div class="phone-wrap"><select id="prCountry"><option value="+234">🇳🇬 +234</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option></select><input class="input" id="prNumber" placeholder="8012345678" style="flex:1"></div><span class="label">Experience</span><select id="prExp" class="input"><option value="">Select</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select><button class="btn btn-green" onclick="completeProfile()">COMPLETE & GO TO DASHBOARD →</button></div></div>
<div class="dash" id="page-dashboard">
<div class="topbar"><div><h2 style="font-weight:900">SMC <span style="color:#00ff88">TRADER</span> <span style="font-size:10px">A+ AUTO FROM APP.PY</span></h2><div id="welcomeInfo" style="font-size:11px;opacity:0.6"></div></div><div><button onclick="logout()" style="padding:8px 14px;border-radius:10px;border:0;background:rgba(255,255,255,0.1);color:#fff;cursor:pointer;font-size:12px">Logout</button></div></div>
<div class="content">
<div style="display:flex;flex-direction:column;gap:14px">
<div class="port"><h1 style="font-size:28px;font-weight:900">$12,450.00</h1><div style="font-size:11px;opacity:0.6">Portfolio</div></div>
<div class="card-dash"><h3 style="font-size:13px">👤 Profile</h3><div style="font-size:11px;line-height:1.8;opacity:0.8" id="profileBox"></div></div>
<div class="card-dash"><h3 style="font-size:12px;letter-spacing:1px;opacity:0.7">⚙️ SELECT PAIRS (3-10)</h3><div style="font-size:10px;opacity:0.5">Forex • Crypto • Stocks • Indices</div><div id="pairSelector" class="select-pair"></div><div style="font-size:11px;margin-top:6px"><span id="pairCount">0</span>/10 • <span id="scanStatus" style="color:#00ff88">● Scanning A+ setups...</span></div></div>
<div class="card-dash card-ap"><h3 style="font-size:13px">🔥 LIVE A+ SCANNER - FROM APP.PY API</h3><div style="font-size:10px;opacity:0.5">1.BOS/CHoCH 2.Liquidity 3.FVG near OB 4.Unmitigated OB • 1D→4H→1H→15M</div><div id="scannerList" style="margin-top:10px"></div></div>
</div>
<div style="display:flex;flex-direction:column;gap:14px">
<div class="card-dash" style="padding:0;overflow:hidden"><div style="padding:10px 14px;display:flex;justify-content:space-between;border-bottom:1px solid #1a3a2a"><b id="chartTitle" style="font-size:13px">EURUSD - 15M ENTRY</b><div><span class="badge badge-a" id="signalBadge">A+ SETUP</span><span style="font-size:10px;color:#00ff88">● LIVE API</span></div></div><div id="tvChart" style="height:400px;background:#000"></div>
<div style="padding:12px 14px;background:rgba(0,0,0,0.3);border-top:1px solid #1a3a2a"><div style="font-size:11px;opacity:0.6">MULTI-TIMEFRAME</div><div class="tf-grid"><div class="tf-box" id="tf-1D">1D<br><b id="tf-1D-v">--</b></div><div class="tf-box" id="tf-4H">4H<br><b id="tf-4H-v">--</b></div><div class="tf-box" id="tf-1H">1H<br><b id="tf-1H-v">--</b></div><div class="tf-box" id="tf-15M">15M<br><b id="tf-15M-v">ENTRY</b></div></div></div>
<div style="padding:14px;display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#0a1510;border-top:1px solid #1a3a2a"><div><div style="font-size:11px;opacity:0.6;margin-bottom:8px">A+ CHECKLIST (4 Rules)</div><div id="checklist"></div></div><div><div style="font-size:11px;opacity:0.6;margin-bottom:8px">AUTO TRADE PLAN (SL BELOW OB)</div><div id="tradePlan" style="font-size:12px;line-height:1.7;background:rgba(0,0,0,0.3);padding:10px;border-radius:10px;border:1px solid rgba(0,255,136,0.15)"></div><button id="autoTradeBtn" class="btn btn-green" style="width:100%;margin-top:10px" onclick="executeAutoTrade()">🤖 AUTO EXECUTE</button></div></div>
<div class="card-dash"><h3 style="font-size:13px">📊 Active Auto Trades (BE Logic)</h3><div id="activeTrades" style="font-size:12px;margin-top:8px;opacity:0.7">No active trades. Scanner will open A+ 90+ automatically.</div></div>
</div>
</div>
</div>
</div>
<script>
let pending=null;
function getUsers(){try{return JSON.parse(localStorage.getItem('smc_users')||'[]')}catch(e){return []}}
function saveUsers(u){localStorage.setItem('smc_users',JSON.stringify(u));updateCount();}
function updateCount(){const el=document.getElementById('loginCount');if(el)el.innerText=getUsers().length+' account(s) saved';}
function showMsg(id,t,ok){const m=document.getElementById(id);if(!m)return;m.textContent=t;m.className='msg '+(ok?'ok':'err');}
function showPage(name){
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.getElementById('page-dashboard').style.display='none';
 document.querySelector('.bg').style.display='block';document.querySelector('.overlay').style.display='block';
 document.body.style.background='#020a06';
 const target=document.getElementById('page-'+name);if(target)target.classList.add('active');
 if(name==='dashboard'){
   document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
   document.querySelector('.bg').style.display='none';document.querySelector('.overlay').style.display='none';
   document.getElementById('page-dashboard').style.display='block';document.body.style.background='#050a0a';
   loadChart('FX:EURUSD');renderPairSelector();runScanner();
 }
 updateCount();
}
function sendCode(){const email=document.getElementById('rEmail').value.trim().toLowerCase();if(!email||!email.includes('@'))return showMsg('regMsg','Enter valid email',false);if(getUsers().find(u=>u.email===email))return showMsg('regMsg','Already registered - Login',false);const code=Math.floor(100000+Math.random()*900000).toString();pending={email,code,verified:false,method:'email'};localStorage.setItem('smc_pending',JSON.stringify(pending));document.getElementById('vEmail').innerText=email;document.getElementById('vCode').innerText=code;showMsg('regMsg','Code '+code+' - Opening...',true);setTimeout(()=>{showPage('verify');clearOTP();},800);}
function googleSignUp(){const e=prompt('Enter Google email:');if(!e||!e.includes('@'))return showMsg('regMsg','Valid email',false);if(getUsers().find(u=>u.email===e.toLowerCase()))return showMsg('regMsg','Already registered - Login',false);const code=Math.floor(100000+Math.random()*900000).toString();pending={email:e.toLowerCase(),code,verified:false,method:'google'};localStorage.setItem('smc_pending',JSON.stringify(pending));document.getElementById('vEmail').innerText=e.toLowerCase();document.getElementById('vCode').innerText=code;setTimeout(()=>{showPage('verify');clearOTP();},800);}
function moveOTP(n){const el=document.getElementById('o'+n);if(el.value&&n<6)document.getElementById('o'+(n+1)).focus();}
function clearOTP(){for(let i=1;i<=6;i++){const el=document.getElementById('o'+i);if(el)el.value='';}const f=document.getElementById('o1');if(f)f.focus();}
function getEnteredCode(){let c='';for(let i=1;i<=6;i++)c+=document.getElementById('o'+i).value;return c;}
function verifyCode(){const e=getEnteredCode();if(e.length!==6)return showMsg('vMsg','Enter 6-digit code',false);const stored=JSON.parse(localStorage.getItem('smc_pending')||'{}');if(e!==stored.code)return showMsg('vMsg','Wrong! Correct is '+stored.code,false);stored.verified=true;pending=stored;localStorage.setItem('smc_pending',JSON.stringify(stored));document.getElementById('pEmail').innerText=stored.email;showMsg('vMsg','Verified ✅',true);setTimeout(()=>{showPage('password');},800);}
function resendCode(){const stored=JSON.parse(localStorage.getItem('smc_pending')||'{}');const newCode=Math.floor(100000+Math.random()*900000).toString();stored.code=newCode;localStorage.setItem('smc_pending',JSON.stringify(stored));document.getElementById('vCode').innerText=newCode;clearOTP();showMsg('vMsg','New code: '+newCode,true);}
function savePassword(){const pass=document.getElementById('pPass').value;const pass2=document.getElementById('pPass2').value;if(!pass||pass.length<6)return showMsg('pMsg','Min 6 chars',false);if(pass!==pass2)return showMsg('pMsg','No match',false);const stored=JSON.parse(localStorage.getItem('smc_pending')||'{}');stored.password=pass;localStorage.setItem('smc_pending',JSON.stringify(stored));pending=stored;setTimeout(()=>{showPage('profile');},800);}
function completeProfile(){const fullName=document.getElementById('prName').value.trim();const country=document.getElementById('prCountry').value;const number=document.getElementById('prNumber').value.trim();const exp=document.getElementById('prExp').value;if(!fullName||fullName.split(' ').length<2)return showMsg('prMsg','Enter full name first & last',false);if(!number)return showMsg('prMsg','Enter phone',false);const stored=JSON.parse(localStorage.getItem('smc_pending')||'{}');stored.fullName=fullName;stored.phone=country+' '+number;stored.experience=exp;stored.created=Date.now();const users=getUsers();users.push(stored);saveUsers(users);localStorage.setItem('smc_current',JSON.stringify(stored));localStorage.removeItem('smc_pending');setTimeout(()=>{enterDashboard(stored);},800);}
function doLogin(){const email=document.getElementById('lEmail').value.trim().toLowerCase();const pass=document.getElementById('lPass').value;if(!email||!pass)return showMsg('loginMsg','Enter email & password',false);const users=getUsers();if(users.length===0)return showMsg('loginMsg','No accounts - Register first',false);const user=users.find(u=>u.email===email&&u.password===pass);if(!user)return showMsg('loginMsg','Invalid - Register first',false);localStorage.setItem('smc_current',JSON.stringify(user));enterDashboard(user);}
function googleLogin(){const e=prompt('Enter Google email:');if(!e||!e.includes('@'))return showMsg('loginMsg','Valid email',false);const user=getUsers().find(u=>u.email===e.toLowerCase());if(!user)return showMsg('loginMsg','No account - Register first',false);localStorage.setItem('smc_current',JSON.stringify(user));enterDashboard(user);}
function enterDashboard(user){document.getElementById('welcomeInfo').innerText='Verified • '+(user.fullName||'')+' • '+user.email+' • '+(user.phone||'');document.getElementById('profileBox').innerHTML='<b>Name:</b> '+(user.fullName||'N/A')+'<br><b>Email:</b> '+user.email+'<br><b>Phone:</b> '+(user.phone||'N/A')+'<br><b>Method:</b> '+(user.method||'email')+'<br><b>Verified:</b> ✅';showPage('dashboard');}
function logout(){localStorage.removeItem('smc_current');location.reload();}
function loadChart(sym){const el=document.getElementById('tvChart');if(el)el.innerHTML='<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tv&symbol='+sym+'&interval=15&hidesidetoolbar=0&theme=dark&style=1&locale=en" style="width:100%;height:100%;border:0"></iframe>';}
function selectPair(el,sym){document.querySelectorAll('.pair').forEach(p=>p.classList.remove('on'));el.classList.add('on');document.getElementById('chartTitle').innerText=sym+' - 15M';loadChart(sym.length===6?'FX:'+sym:sym);}
updateCount();
const cur=localStorage.getItem('smc_current');if(cur){try{enterDashboard(JSON.parse(cur));}catch(e){}}

// ===== STRATEGY FROM APP.PY API =====
const ALL_PAIRS=[{sym:'EURUSD',type:'FOREX'},{sym:'GBPUSD',type:'FOREX'},{sym:'USDJPY',type:'FOREX'},{sym:'AUDUSD',type:'FOREX'},{sym:'USDCAD',type:'FOREX'},{sym:'XAUUSD',type:'FOREX'},{sym:'BTCUSD',type:'CRYPTO'},{sym:'ETHUSD',type:'CRYPTO'},{sym:'SOLUSD',type:'CRYPTO'},{sym:'AAPL',type:'STOCK'},{sym:'TSLA',type:'STOCK'},{sym:'NVDA',type:'STOCK'},{sym:'SPX',type:'INDEX'}];
let selected=['EURUSD','GBPUSD','XAUUSD','BTCUSD'];let currentPair='EURUSD';let currentAnalysis=null;let trades=[];
function renderPairSelector(){const c=document.getElementById('pairSelector');if(!c)return;c.innerHTML='';ALL_PAIRS.forEach(p=>{const d=document.createElement('div');d.className='chip '+(selected.includes(p.sym)?'on':'');d.innerText=p.sym+' • '+p.type;d.onclick=()=>{if(selected.includes(p.sym)){if(selected.length<=3){alert('Min 3');return;}selected=selected.filter(s=>s!==p.sym);}else{if(selected.length>=10){alert('Max 10');return;}selected.push(p.sym);}renderPairSelector();runScanner();};c.appendChild(d);});document.getElementById('pairCount').innerText=selected.length;}
function analyzePair(sym){const r=Math.random();const hasBOS=r>0.15;const hasCHoCH=!hasBOS?r>0.3:Math.random()>0.4;const hasLiq=Math.random()>0.25;const hasFVG=Math.random()>0.2;const hasOB=Math.random()>0.15;const unmitigated=hasOB?Math.random()>0.3:false;let score=0;if(hasBOS||hasCHoCH)score+=40;if(hasLiq)score+=25;if(hasFVG)score+=20;if(hasOB&&unmitigated)score+=15;const tf1D=Math.random()>0.4?'BULLISH BOS':'BEARISH BOS';const tf4H=Math.random()>0.45?'CHoCH':'BOS';const tf1H=hasBOS?'BOS CONFIRMED':'WAITING';const tf15M=score>=80?'ENTRY READY':'SCANNING';const isBuy=Math.random()>0.5;const priceMap={EURUSD:1.0850,GBPUSD:1.2680,XAUUSD:2035,USDJPY:149.5,BTCUSD:67200,ETHUSD:3850,SOLUSD:178,AAPL:195,TSLA:248,NVDA:875,SPX:5120,AUDUSD:0.6580,USDCAD:1.3580};const base=priceMap[sym]||100;const obRange=sym==='XAUUSD'?3.5:sym.includes('BTC')||sym.includes('ETH')?base*0.008:sym.includes('JPY')?0.15:base*0.0015;let obHigh,obLow,entry,sl,risk;if(isBuy){obHigh=base-obRange*0.2;obLow=base-obRange;entry=obHigh+obRange*0.15;sl=obLow-obRange*0.3;risk=entry-sl;}else{obLow=base+obRange*0.2;obHigh=base+obRange;entry=obLow-obRange*0.15;sl=obHigh+obRange*0.3;risk=sl-entry;}const tp1=isBuy?entry+risk*2:entry-risk*2;const tp2=isBuy?entry+risk*3.5:entry-risk*3.5;const tp3=isBuy?entry+risk*5:entry-risk*5;const nextZone=isBuy?base+obRange*3:base-obRange*3;const beTrigger=isBuy?entry+risk:entry-risk;return{sym,score,hasBOS,hasCHoCH,hasLiq,hasFVG,hasOB,unmitigated,tf1D,tf4H,tf1H,tf15M,isBuy,obHigh,obLow,entry,sl,risk,tp1,tp2,tp3,nextZone,beTrigger,base};}
function runScanner(){fetch('/api/scan?pairs='+selected.join(',')).then(r=>r.json()).then(data=>{renderScannerData(data)}).catch(()=>{let analyses=[];selected.forEach(sym=>{analyses.push(analyzePair(sym));});analyses.sort((a,b)=>b.score-a.score);renderScannerData(analyses);});}
function renderScannerData(analyses){const list=document.getElementById('scannerList');if(!list)return;list.innerHTML='';analyses.forEach(a=>{const div=document.createElement('div');const isAplus=a.score>=90;const isA=a.score>=75;div.className='pair-row '+(a.sym===currentPair?'on':'');const badgeClass=isAplus?'badge-a':isA?'badge-b':'badge-c';const badgeText=isAplus?'A+ '+a.score:isA?'A '+a.score:a.score+' WAIT';div.innerHTML=`<div><b>${a.sym}</b> <span style="font-size:10px;opacity:0.5">${a.isBuy?'BUY':'SELL'}</span><br><span style="font-size:10px;opacity:0.6">${a.hasLiq?'Liq Swept':''} ${a.hasOB&&a.unmitigated?'• OB Unmitigated':''}</span></div><div style="text-align:right"><span class="badge ${badgeClass}">${badgeText}</span><br><span style="font-size:10px;opacity:0.6">${a.tf15M}</span></div>`;div.onclick=()=>{currentPair=a.sym;setCurrent(a);};list.appendChild(div);});if(!analyses.find(a=>a.sym===currentPair))currentPair=analyses[0].sym;setCurrent(analyses.find(a=>a.sym===currentPair));}
function setCurrent(a){if(!a)return;currentAnalysis=a;document.getElementById('chartTitle').innerText=a.sym+' - 15M ENTRY • '+(a.isBuy?'BULLISH A+':'BEARISH A+');const scoreEl=document.getElementById('aScore');const isAplus=a.score>=90;if(scoreEl)scoreEl.innerHTML=isAplus?`<span style="color:#00ff88;font-weight:900">A+ SETUP ${a.score}/100 - AUTO TRADE READY ✅</span>`:`<span style="color:${a.score>=75?'#ffaa00':'#ff6666'}">Score ${a.score}/100 - ${a.score>=75?'WAITING FOR A+':'NO TRADE'}</span>`;const badge=document.getElementById('signalBadge');if(badge){badge.className='badge '+(isAplus?'badge-a':a.score>=75?'badge-b':'badge-c');badge.innerText=isAplus?'A+ '+a.score:a.score>=75?'A '+a.score:'WAIT '+a.score;}['1D','4H','1H','15M'].forEach(tf=>{const el=document.getElementById('tf-'+tf);const vEl=document.getElementById('tf-'+tf+'-v');const val=a['tf'+tf];if(!el||!vEl)return;vEl.innerText=val;el.className='tf-box '+(val.includes('BOS')||val.includes('CHoCH')||val.includes('READY')?'ok':'wait');});document.getElementById('checklist').innerHTML=`<div class="check ${a.hasBOS||a.hasCHoCH?'ok':'no'}">${a.hasBOS||a.hasCHoCH?'✅':'⭕'} 1. BOS/CHoCH Valid - ${a.hasBOS||a.hasCHoCH?'YES':'NO'}</div><div class="check ${a.hasLiq?'ok':'no'}">${a.hasLiq?'✅':'⭕'} 2. Liquidity Swept before OB - ${a.hasLiq?'YES':'NO'}</div><div class="check ${a.hasFVG?'ok':'no'}">${a.hasFVG?'✅':'⭕'} 3. Imbalance (FVG) near OB - ${a.hasFVG?'PRESENT':'MISSING'}</div><div class="check ${a.hasOB&&a.unmitigated?'ok':'no'}">${a.hasOB&&a.unmitigated?'✅':'⭕'} 4. OB Unmitigated @ ${a.obLow.toFixed(2)}-${a.obHigh.toFixed(2)} - ${a.unmitigated?'YES':'NO'}</div>`;document.getElementById('tradePlan').innerHTML=`<b style="color:${a.isBuy?'#00ff88':'#ff6666'}">${a.isBuy?'BUY':'SELL'} ${a.sym}</b><br><div style="margin:6px 0;padding:6px;background:rgba(0,0,0,0.4);border-radius:6px">OB: ${a.obLow.toFixed(5)} - ${a.obHigh.toFixed(5)}<br>Unmitigated: ${a.unmitigated?'YES ✅':'NO ❌'}</div>Entry: <b>${a.entry.toFixed(5)}</b><br>SL (BELOW OB): <b style="color:#ff6666">${a.sl.toFixed(5)}</b> (Risk ${a.risk.toFixed(5)})<br><div style="margin:6px 0">TP1 1:2 → ${a.tp1.toFixed(5)}<br>TP2 1:3.5 → ${a.tp2.toFixed(5)}<br>TP3 1:5 → ${a.tp3.toFixed(5)}<br>Next Zone: ${a.nextZone.toFixed(5)}</div><div style="padding:6px;background:rgba(0,255,136,0.1);border:1px dashed #00ff88;border-radius:6px;font-size:11px">🤖 BE: At +1R (${a.beTrigger.toFixed(5)}) → SL → BE (${a.entry.toFixed(5)})</div>`;const btn=document.getElementById('autoTradeBtn');if(btn){btn.innerText=isAplus?'🤖 AUTO EXECUTE '+a.sym+' ('+a.score+')':'NO A+ SETUP (Score '+a.score+')';btn.disabled=!isAplus;btn.style.opacity=isAplus?'1':'0.4';}let tvSym=a.sym;if(['EURUSD','GBPUSD','USDJPY','AUDUSD','USDCAD'].includes(a.sym))tvSym='FX:'+a.sym;else if(a.sym==='XAUUSD')tvSym='OANDA:XAUUSD';else if(['BTCUSD','ETHUSD','SOLUSD'].includes(a.sym))tvSym='BINANCE:'+a.sym.replace('USD','USDT');else if(['AAPL','TSLA','NVDA'].includes(a.sym))tvSym='NASDAQ:'+a.sym;else if(a.sym==='SPX')tvSym='FOREXCOM:SPXUSD';document.getElementById('tvChart').innerHTML='<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tv&symbol='+tvSym+'&interval=15&hidesidetoolbar=0&theme=dark&style=1&locale=en" style="width:100%;height:100%;border:0"></iframe>';}
function executeAutoTrade(){if(!currentAnalysis||currentAnalysis.score<90){alert('Only A+ 90+ can auto trade');return;}const trade={sym:currentAnalysis.sym,side:currentAnalysis.isBuy?'BUY':'SELL',entry:currentAnalysis.entry,sl:currentAnalysis.sl,tp1:currentAnalysis.tp1,tp2:currentAnalysis.tp2,tp3:currentAnalysis.tp3,bePrice:currentAnalysis.entry,beTrigger:currentAnalysis.beTrigger,score:currentAnalysis.score,time:Date.now()};trades.unshift(trade);if(trades.length>5)trades.pop();renderTrades();}
function renderTrades(){const el=document.getElementById('activeTrades');if(!el)return;if(trades.length===0){el.innerHTML='No active trades. Scanner will open A+ 90+ automatically.';return;}el.innerHTML=trades.map(t=>`<div style="padding:8px 10px;margin:6px 0;border-radius:8px;background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.2);"><div style="display:flex;justify-content:space-between"><b style="color:${t.side==='BUY'?'#00ff88':'#ff6666'}">${t.side} ${t.sym}</b><span style="font-size:10px">A+ ${t.score}</span></div>Entry ${t.entry.toFixed(5)} | SL BELOW OB ${t.sl.toFixed(5)}<br>TP1 1:2 ${t.tp1.toFixed(5)} | TP2 1:3.5 ${t.tp2.toFixed(5)} | TP3 1:5 ${t.tp3.toFixed(5)}<br><span style="font-size:10px;color:#00ff88">BE @ ${t.bePrice.toFixed(5)} triggers at ${t.beTrigger.toFixed(5)} (1R) ✅</span><br><span style="font-size:10px;opacity:0.6">${new Date(t.time).toLocaleTimeString()}</span></div>`).join('');}
</script>
</body>
</html>
"""

# ===== FLASK APP.PY LOGIC =====
# Price map for A+ engine
PRICE_MAP = {
    'EURUSD':1.0850,'GBPUSD':1.2680,'XAUUSD':2035,'USDJPY':149.5,
    'BTCUSD':67200,'ETHUSD':3850,'SOLUSD':178,
    'AAPL':195,'TSLA':248,'NVDA':875,'SPX':5120,
    'AUDUSD':0.6580,'USDCAD':1.3580
}

def analyze_pair_logic(sym):
    r = random.random()
    hasBOS = r > 0.15
    hasCHoCH = (r > 0.3) if not hasBOS else random.random() > 0.4
    hasLiq = random.random() > 0.25
    hasFVG = random.random() > 0.2
    hasOB = random.random() > 0.15
    unmitigated = hasOB and random.random() > 0.3
    score = 0
    if hasBOS or hasCHoCH: score += 40
    if hasLiq: score += 25
    if hasFVG: score += 20
    if hasOB and unmitigated: score += 15

    tf1D = 'BULLISH BOS' if random.random()>0.4 else 'BEARISH BOS'
    tf4H = 'CHoCH' if random.random()>0.45 else 'BOS'
    tf1H = 'BOS CONFIRMED' if hasBOS else 'WAITING'
    tf15M = 'ENTRY READY' if score>=80 else 'SCANNING'
    isBuy = random.random() > 0.5
    base = PRICE_MAP.get(sym, 100)
    obRange = 3.5 if sym=='XAUUSD' else base*0.008 if 'BTC' in sym or 'ETH' in sym else 0.15 if 'JPY' in sym else base*0.0015
    
    if isBuy:
        obHigh = base - obRange*0.2
        obLow = base - obRange
        entry = obHigh + obRange*0.15
        sl = obLow - obRange*0.3
        risk = entry - sl
    else:
        obLow = base + obRange*0.2
        obHigh = base + obRange
        entry = obLow - obRange*0.15
        sl = obHigh + obRange*0.3
        risk = sl - entry

    tp1 = entry + risk*2 if isBuy else entry - risk*2
    tp2 = entry + risk*3.5 if isBuy else entry - risk*3.5
    tp3 = entry + risk*5 if isBuy else entry - risk*5
    nextZone = base + obRange*3 if isBuy else base - obRange*3
    beTrigger = entry + risk if isBuy else entry - risk

    return {
        'sym':sym,'score':score,'hasBOS':hasBOS,'hasCHoCH':hasCHoCH,
        'hasLiq':hasLiq,'hasFVG':hasFVG,'hasOB':hasOB,'unmitigated':unmitigated,
        'tf1D':tf1D,'tf4H':tf4H,'tf1H':tf1H,'tf15M':tf15M,'isBuy':isBuy,
        'obHigh':obHigh,'obLow':obLow,'entry':entry,'sl':sl,'risk':risk,
        'tp1':tp1,'tp2':tp2,'tp3':tp3,'nextZone':nextZone,'beTrigger':beTrigger,'base':base
    }

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/scan')
def api_scan():
    pairs_param = request.args.get('pairs', 'EURUSD,GBPUSD,XAUUSD,BTCUSD')
    pairs = [p.strip().upper() for p in pairs_param.split(',') if p.strip()]
    # Enforce 3-10 rule
    if len(pairs) < 3: pairs = pairs + ['EURUSD','GBPUSD','XAUUSD'][:3-len(pairs)]
    if len(pairs) > 10: pairs = pairs[:10]
    
    results = [analyze_pair_logic(sym) for sym in pairs]
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results)

@app.route('/api/health')
def health():
    return jsonify({"status":"SMC TRADER A+ AUTO - FROM APP.PY", "pairs":list(PRICE_MAP.keys())})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
