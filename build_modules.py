#!/usr/bin/env python3
import json, os

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%PAGE_TITLE%% — Reading for Amara</title>

<!--
  AMARA READING PROJECT module. Format: Read -> Comprehend -> Match -> Use.
  INTEGRATION: ACTIVITY_ID/STORE_KEY below must match your index.html hub
  for the tile + score to show on the dashboard. Send index.html and I'll
  set them exactly. Runs offline; optional window.amaraSyncScore() hook.
-->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">

<style>
  :root{
%%CSSVARS%%
    --right:#1f8a4c; --right-soft:#dff3e2;
    --wrong:#e06b5a; --wrong-soft:#fbe6e2;
    --amber:#f6b21b;
    --ink:#26303a; --ink-soft:#566370;
    --shadow:0 8px 26px rgba(40,40,60,.16);
    --radius:20px;
  }
  *{box-sizing:border-box}
  body{
    margin:0;font-family:'Nunito','Trebuchet MS','Segoe UI',system-ui,sans-serif;
    color:var(--ink);min-height:100vh;line-height:1.55;padding:18px;
    background:
      radial-gradient(900px 500px at 12% -8%, var(--glow1), transparent 60%),
      radial-gradient(800px 600px at 100% 0%, var(--glow2), transparent 55%),
      linear-gradient(180deg,var(--bg-top) 0%, var(--bg-bottom) 100%);
  }
  .wrap{max-width:760px;margin:0 auto}
  header.hero{
    background:linear-gradient(135deg,var(--c-dark),var(--c-deep));
    color:#fff;border-radius:24px;padding:22px 24px;box-shadow:var(--shadow);
    position:relative;overflow:hidden;
  }
  header.hero::after{content:"%%WATERMARK%%";position:absolute;right:-6px;bottom:-14px;font-size:120px;opacity:.16;transform:rotate(-12deg)}
  .backlink{display:inline-flex;align-items:center;gap:6px;color:#fff;text-decoration:none;font-weight:700;font-size:.92rem;background:rgba(255,255,255,.16);padding:6px 12px;border-radius:999px;margin-bottom:12px}
  .backlink:hover{background:rgba(255,255,255,.28)}
  header.hero h1{font-family:'Fredoka',system-ui,sans-serif;font-weight:700;margin:0;font-size:clamp(1.5rem,5vw,2.1rem);letter-spacing:.3px}
  header.hero p{margin:4px 0 0;color:#ffffffcc;font-weight:600}
  .steps{display:flex;gap:8px;margin:16px 0 6px;flex-wrap:wrap}
  .step-tab{flex:1 1 120px;border:none;cursor:pointer;border-radius:14px;padding:12px 10px;font-family:'Fredoka',sans-serif;font-weight:600;font-size:.95rem;background:var(--c-paper);color:var(--ink-soft);box-shadow:var(--shadow);display:flex;align-items:center;gap:8px;justify-content:center;transition:transform .12s, background .2s, color .2s}
  .step-tab .num{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--c-accent-soft);color:var(--c-dark);font-weight:800;font-size:.85rem;flex:none}
  .step-tab.active{background:var(--c-primary);color:#fff}
  .step-tab.active .num{background:#fff;color:var(--c-dark)}
  .step-tab.done .num{background:var(--amber);color:#fff}
  .step-tab:hover{transform:translateY(-1px)}
  .panel{background:var(--c-paper);border-radius:var(--radius);padding:22px;box-shadow:var(--shadow);margin-top:14px;animation:rise .3s ease}
  @keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
  .panel.hidden{display:none}
  .panel h2{font-family:'Fredoka',sans-serif;color:var(--c-dark);margin:0 0 4px;font-size:1.3rem;display:flex;align-items:center;gap:10px}
  .panel .lead{color:var(--ink-soft);margin:0 0 16px;font-weight:600}
  .passage{background:var(--c-cream);border:2px solid #00000012;border-radius:16px;padding:18px 20px;font-size:1.06rem;line-height:1.7}
  .topic-diagram{margin:0 0 16px;text-align:center}
  .topic-diagram img{max-width:100%;height:auto;border-radius:12px;border:2px solid #00000012;display:block;margin:0 auto}
  .passage h3{margin:0 0 10px;font-family:'Fredoka',sans-serif;color:var(--c-deep)}
  .passage p{margin:0 0 14px}
  .passage p:last-child{margin-bottom:0}
  .voc{background:var(--c-accent-soft);border-bottom:2px solid var(--c-accent);border-radius:5px;padding:0 3px;font-weight:700;color:var(--c-deep)}
  .q{margin-bottom:18px}
  .q .qtext{font-weight:800;margin-bottom:10px}
  .q .qtext .badge{font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.5px;background:var(--c-accent-soft);color:var(--c-dark);padding:2px 8px;border-radius:999px;margin-right:8px;vertical-align:middle}
  .opt{display:block;width:100%;text-align:left;border:2px solid #0000001a;background:#fff;border-radius:12px;padding:11px 14px;margin:7px 0;cursor:pointer;font-size:1rem;font-weight:600;color:var(--ink);transition:border-color .15s, background .15s}
  .opt:hover{border-color:var(--c-accent)}
  .opt.selected{border-color:var(--c-primary);background:var(--c-accent-soft)}
  .opt.correct{border-color:var(--right);background:var(--right-soft)}
  .opt.incorrect{border-color:var(--wrong);background:var(--wrong-soft)}
  .opt .mark{float:right;font-weight:800}
  .match-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:#fff;border:2px solid #0000001a;border-radius:12px;padding:10px 12px;margin:8px 0}
  .match-word{font-weight:800;color:var(--c-dark);min-width:120px}
  .match-row select{flex:1;min-width:150px;font-family:inherit;font-size:.98rem;font-weight:600;padding:9px 10px;border-radius:10px;border:2px solid #0000001f;background:#fbfbfd;color:var(--ink)}
  .hint-btn{border:none;background:var(--c-accent-soft);color:var(--c-dark);font-weight:800;font-size:.82rem;padding:7px 12px;border-radius:999px;cursor:pointer;white-space:nowrap}
  .hint-btn:hover{filter:brightness(.96)}
  .hint-text{flex-basis:100%;font-size:.92rem;color:var(--ink-soft);background:var(--c-cream);border-left:3px solid var(--c-accent);border-radius:6px;padding:7px 11px;margin-top:4px;display:none}
  .hint-text.show{display:block}
  .match-row.correct{border-color:var(--right);background:var(--right-soft)}
  .match-row.incorrect{border-color:var(--wrong);background:var(--wrong-soft)}
  .wordbank{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
  .chip{background:var(--c-accent-soft);color:var(--c-deep);border:2px solid var(--c-accent);border-radius:999px;padding:6px 14px;font-weight:800;cursor:pointer;font-size:.95rem;user-select:none}
  .chip:hover{background:var(--c-accent);color:#fff}
  .chip.used{opacity:.35;text-decoration:line-through}
  .fill{margin:11px 0;font-size:1.04rem;font-weight:600;line-height:1.9}
  .fill input{border:none;border-bottom:3px dotted var(--c-primary);background:var(--c-cream);font-family:inherit;font-size:1rem;font-weight:800;color:var(--c-dark);width:150px;text-align:center;padding:3px 6px;border-radius:6px 6px 0 0}
  .fill input:focus{outline:none;background:var(--c-accent-soft)}
  .fill input.correct{border-bottom-color:var(--right);background:var(--right-soft);color:var(--c-deep)}
  .fill input.incorrect{border-bottom-color:var(--wrong);background:var(--wrong-soft);color:var(--wrong)}
  .fill .tag{font-size:.72rem;color:var(--amber);font-weight:800;margin-left:4px}
  .actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
  .btn{border:none;cursor:pointer;font-family:'Fredoka',sans-serif;font-weight:600;font-size:1rem;padding:12px 22px;border-radius:14px;transition:transform .1s, filter .15s}
  .btn:hover{transform:translateY(-1px);filter:brightness(1.04)}
  .btn-primary{background:var(--c-primary);color:#fff;box-shadow:var(--shadow)}
  .btn-ghost{background:#fff;color:var(--c-dark);border:2px solid #0000001f}
  .feedback{margin-top:14px;border-radius:12px;padding:12px 16px;font-weight:800;display:none}
  .feedback.show{display:block}
  .feedback.good{background:var(--right-soft);color:var(--right)}
  .feedback.try{background:var(--wrong-soft);color:#a83a2c}
  #results .score-big{font-family:'Fredoka',sans-serif;font-size:3.4rem;color:var(--c-dark);text-align:center;margin:6px 0 0}
  #results .score-sub{text-align:center;color:var(--ink-soft);font-weight:700;margin:0 0 8px}
  #results .trophy{font-size:3rem;text-align:center}
  #results .msg{text-align:center;font-weight:800;font-size:1.1rem;color:var(--c-deep);margin:8px 0 0}
  .breakdown{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:16px 0}
  .bd{background:var(--c-cream);border-radius:12px;padding:10px 16px;text-align:center;min-width:96px}
  .bd b{font-family:'Fredoka',sans-serif;color:var(--c-dark);font-size:1.3rem;display:block}
  .bd span{font-size:.8rem;color:var(--ink-soft);font-weight:700}
  .saved-note{text-align:center;font-size:.85rem;color:var(--ink-soft);font-weight:700;margin-top:6px}
  .kwl-box{background:var(--c-accent-soft);border:2px solid var(--c-accent);border-radius:16px;padding:16px 18px;margin-bottom:16px}
  .kwl-title{font-family:'Fredoka',sans-serif;font-weight:700;color:var(--c-dark);font-size:1rem;margin:0 0 12px}
  .kwl-row{display:flex;gap:10px;margin-bottom:10px;align-items:flex-start}
  .kwl-row:last-child{margin-bottom:0}
  .kwl-letter{flex:0 0 30px;height:30px;border-radius:8px;background:var(--c-primary);color:#fff;font-family:'Fredoka',sans-serif;font-weight:700;font-size:1rem;display:flex;align-items:center;justify-content:center}
  .kwl-letter.l-letter{background:var(--right)}
  .kwl-col{flex:1;min-width:0}
  .kwl-label{font-size:.82rem;font-weight:800;color:var(--c-deep);margin-bottom:4px}
  .kwl-input{width:100%;font-family:inherit;font-size:.95rem;font-weight:600;padding:7px 11px;border:2px solid #0000001a;border-radius:10px;background:#fff;color:var(--ink)}
  .kwl-input:focus{outline:none;border-color:var(--c-primary)}
  .kwl-recap{font-size:.9rem;color:var(--ink-soft);background:rgba(0,0,0,.05);border-radius:8px;padding:6px 10px;font-weight:600;font-style:italic}
  @media (max-width:520px){body{padding:12px}.step-tab{flex:1 1 calc(50% - 8px)}.match-word{min-width:100%}}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <a class="backlink" href="%%HUB_FILE%%">← All activities</a>
    <h1>%%HERO_EMOJI%% %%HERO_TITLE%%</h1>
    <p>A reading adventure for %%SUBJECT_NAME%%</p>
  </header>

  <div class="steps" id="steps">
    <button class="step-tab active" data-step="0"><span class="num">1</span> Read</button>
    <button class="step-tab" data-step="1"><span class="num">2</span> Comprehend</button>
    <button class="step-tab" data-step="2"><span class="num">3</span> Match</button>
    <button class="step-tab" data-step="3"><span class="num">4</span> Use</button>
  </div>

  <section class="panel" data-panel="0">
    <h2>📖 Read the passage</h2>
    <p class="lead">Read it once for the meaning. Then read it again and look for the <span class="voc">coloured words</span>.</p>
    <div class="kwl-box">
      <div class="kwl-title">📋 Before you read — KWL</div>
      <div class="kwl-row">
        <div class="kwl-letter">K</div>
        <div class="kwl-col">
          <div class="kwl-label">What do you already KNOW about this topic?</div>
          <input class="kwl-input" id="kwl-k" type="text" placeholder="One word or sentence is enough…" maxlength="200" autocomplete="off">
        </div>
      </div>
      <div class="kwl-row">
        <div class="kwl-letter">W</div>
        <div class="kwl-col">
          <div class="kwl-label">What do you WANT to find out?</div>
          <input class="kwl-input" id="kwl-w" type="text" placeholder="One word or sentence is enough…" maxlength="200" autocomplete="off">
        </div>
      </div>
    </div>
    <div class="passage">
      <div class="topic-diagram">
        <img src="%%DIAGRAM_FILE%%" alt="%%PASSAGE_TITLE%% diagram">
      </div>
      <h3>%%PASSAGE_TITLE%%</h3>
      %%PASSAGE_HTML%%
    </div>
    <div class="actions"><button class="btn btn-primary" onclick="go(1)">I'm ready — Comprehend →</button></div>
  </section>

  <section class="panel hidden" data-panel="1">
    <h2>🤔 Comprehend</h2>
    <p class="lead">Pick the best answer for each question, then press <b>Check answers</b>.</p>
    <div id="quiz"></div>
    <div class="actions">
      <button class="btn btn-primary" onclick="checkQuiz()">Check answers</button>
      <button class="btn btn-ghost" onclick="go(2)">Next: Match →</button>
    </div>
    <div class="feedback" id="quizFb"></div>
  </section>

  <section class="panel hidden" data-panel="2">
    <h2>🔗 Match the word to its meaning</h2>
    <p class="lead">Choose the meaning for each word. Stuck? Tap <b>Hint</b> to see the word in the passage.</p>
    <div id="match"></div>
    <div class="actions">
      <button class="btn btn-primary" onclick="checkMatch()">Check matches</button>
      <button class="btn btn-ghost" onclick="go(3)">Next: Use →</button>
    </div>
    <div class="feedback" id="matchFb"></div>
  </section>

  <section class="panel hidden" data-panel="3">
    <h2>✏️ Use the words</h2>
    <p class="lead">%%USE_LEAD%%</p>
    <div class="wordbank" id="bank"></div>
    <div id="fills"></div>
    <div class="actions"><button class="btn btn-primary" onclick="checkFills()">Check &amp; finish 🎉</button></div>
    <div class="feedback" id="fillFb"></div>
  </section>

  <section class="panel hidden" id="results">
    <div class="trophy" id="trophy">🌟</div>
    <div class="score-big" id="scoreBig">0%</div>
    <p class="score-sub" id="scoreSub">0 out of 20</p>
    <div class="breakdown" id="breakdown"></div>
    <p class="msg" id="resultMsg"></p>
    <p class="saved-note" id="savedNote"></p>
    <div class="kwl-box" id="kwl-results" style="text-align:left;margin:20px 0 6px">
      <div class="kwl-title">📋 Your KWL chart</div>
      <div class="kwl-row">
        <div class="kwl-letter">K</div>
        <div class="kwl-col">
          <div class="kwl-label">What you KNEW</div>
          <div class="kwl-recap" id="kwl-k-show">—</div>
        </div>
      </div>
      <div class="kwl-row">
        <div class="kwl-letter">W</div>
        <div class="kwl-col">
          <div class="kwl-label">What you WANTED to find out</div>
          <div class="kwl-recap" id="kwl-w-show">—</div>
        </div>
      </div>
      <div class="kwl-row">
        <div class="kwl-letter l-letter">L</div>
        <div class="kwl-col">
          <div class="kwl-label">What did you LEARN?</div>
          <input class="kwl-input" id="kwl-l" type="text" placeholder="One word or sentence is enough…" maxlength="200" autocomplete="off">
        </div>
      </div>
    </div>
    <div class="actions" style="justify-content:center">
      <button class="btn btn-primary" onclick="restart()">Try again 🔁</button>
      <button class="btn btn-ghost" onclick="location.href='%%HUB_FILE%%'">Back to all activities</button>
    </div>
  </section>
</div>

<script>
const MODULE = %%MODULE_JSON%%;
const PROJECT = MODULE.projectKey;
const HUB_KEY = MODULE.hubKey || 'amaraReading';
const NAME    = MODULE.name || 'Amara';
const TITLE   = MODULE.title;
const QUESTIONS = MODULE.questions, MATCH = MODULE.match, BANK = MODULE.bank, FILLS = MODULE.fills;
const TOTAL = QUESTIONS.length + MATCH.length + FILLS.length;

let selected = Array(QUESTIONS.length).fill(null);
let quizScore=null, matchScore=null, fillScore=null, focusedFill=null;

function go(step){
  document.querySelectorAll('.panel[data-panel]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('results').classList.add('hidden');
  document.querySelector('.panel[data-panel="'+step+'"]').classList.remove('hidden');
  document.querySelectorAll('.step-tab').forEach(t=>t.classList.toggle('active', +t.dataset.step===step));
  window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.step-tab').forEach(t=>t.addEventListener('click',()=>go(+t.dataset.step)));
function markDone(step){const tab=document.querySelector('.step-tab[data-step="'+step+'"]');if(tab)tab.classList.add('done');}

const quizEl=document.getElementById('quiz');
QUESTIONS.forEach((item,qi)=>{
  const div=document.createElement('div');div.className='q';
  div.innerHTML='<div class="qtext"><span class="badge">'+item.type+'</span>'+(qi+1)+'. '+item.q+'</div>';
  item.opts.forEach((opt,oi)=>{
    const b=document.createElement('button');b.className='opt';b.textContent=opt;
    b.onclick=()=>{selected[qi]=oi;div.querySelectorAll('.opt').forEach(o=>o.classList.remove('selected'));b.classList.add('selected');};
    div.appendChild(b);
  });
  quizEl.appendChild(div);
});
function checkQuiz(){
  if(selected.includes(null)){flash('quizFb','try','Try answering every question first 🙂');return;}
  let s=0;
  document.querySelectorAll('#quiz .q').forEach((qd,qi)=>{
    const opts=qd.querySelectorAll('.opt');
    opts.forEach(o=>{o.classList.remove('correct','incorrect');const m=o.querySelector('.mark');if(m)m.remove();});
    const correct=QUESTIONS[qi].a;
    if(selected[qi]===correct){s++;opts[correct].classList.add('correct');opts[correct].innerHTML+=' <span class="mark">✓</span>';}
    else{opts[selected[qi]].classList.add('incorrect');opts[selected[qi]].innerHTML+=' <span class="mark">✗</span>';opts[correct].classList.add('correct');opts[correct].innerHTML+=' <span class="mark">✓</span>';}
  });
  quizScore=s;markDone(1);recordSub('comprehend',s,QUESTIONS.length);
  flash('quizFb', s===QUESTIONS.length?'good':'try','You got '+s+' of '+QUESTIONS.length+'. '+(s===QUESTIONS.length?('Perfect reading, '+NAME+'! 🌟'):'Look back at the passage, then tap Next.'));
}

const matchEl=document.getElementById('match');
const shuffledDefs = MATCH.map((m,i)=>({def:m.def,i})).sort(()=>Math.random()-0.5);
MATCH.forEach((m,mi)=>{
  const row=document.createElement('div');row.className='match-row';row.dataset.idx=mi;
  let opts='<option value="">— choose a meaning —</option>';
  shuffledDefs.forEach(d=>opts+='<option value="'+d.i+'">'+d.def+'</option>');
  row.innerHTML='<span class="match-word">'+m.word+'</span><select>'+opts+'</select><button class="hint-btn" type="button">💡 Hint</button><div class="hint-text">'+m.hint+'</div>';
  row.querySelector('.hint-btn').onclick=()=>row.querySelector('.hint-text').classList.toggle('show');
  matchEl.appendChild(row);
});
function checkMatch(){
  const rows=document.querySelectorAll('#match .match-row');
  let unanswered=false;rows.forEach(r=>{if(!r.querySelector('select').value)unanswered=true;});
  if(unanswered){flash('matchFb','try','Match every word first 🧩');return;}
  let s=0;
  rows.forEach(r=>{const mi=+r.dataset.idx;const chosen=+r.querySelector('select').value;r.classList.remove('correct','incorrect');if(chosen===mi){s++;r.classList.add('correct');}else{r.classList.add('incorrect');}});
  matchScore=s;markDone(2);recordSub('match',s,MATCH.length);
  flash('matchFb', s===MATCH.length?'good':'try','You matched '+s+' of '+MATCH.length+'. '+(s===MATCH.length?'Word wizard! ⭐':'Use the hints and try the red ones again.'));
}

const bankEl=document.getElementById('bank');
BANK.forEach(w=>{const c=document.createElement('span');c.className='chip';c.textContent=w;c.dataset.word=w;c.onclick=()=>{if(focusedFill){focusedFill.value=w;updateBank();focusedFill.classList.remove('correct','incorrect');}};bankEl.appendChild(c);});
const fillsEl=document.getElementById('fills');
FILLS.forEach((f,fi)=>{
  const div=document.createElement('div');div.className='fill';
  const parts=f.text.split('___');
  div.innerHTML=(fi+1)+'. '+parts[0]+'<input type="text" data-i="'+fi+'" autocomplete="off" spellcheck="false">'+(parts[1]||'')+(f.challenge?'<span class="tag">★ challenge</span>':'');
  fillsEl.appendChild(div);
});
fillsEl.querySelectorAll('input').forEach(inp=>{inp.addEventListener('focus',()=>focusedFill=inp);inp.addEventListener('input',()=>{updateBank();inp.classList.remove('correct','incorrect');});});
function updateBank(){const used=[...fillsEl.querySelectorAll('input')].map(i=>i.value.trim().toLowerCase());bankEl.querySelectorAll('.chip').forEach(c=>{c.classList.toggle('used', used.includes(c.dataset.word.toLowerCase()));});}
function norm(s){return s.trim().toLowerCase().replace(/[^a-z]/g,'');}
function checkFills(){
  const inputs=fillsEl.querySelectorAll('input');
  let blank=false;inputs.forEach(i=>{if(!i.value.trim())blank=true;});
  if(blank){flash('fillFb','try','Fill in every blank first ✏️');return;}
  let s=0;
  inputs.forEach((inp,i)=>{inp.classList.remove('correct','incorrect');if(norm(inp.value)===norm(FILLS[i].a)){s++;inp.classList.add('correct');}else{inp.classList.add('incorrect');}});
  fillScore=s;markDone(3);recordSub('use',s,FILLS.length);
  flash('fillFb', s===FILLS.length?'good':'try', s===FILLS.length?('All '+FILLS.length+' correct! 🎉'):(s+' of '+FILLS.length+' correct. Fix the red words, then check again.'));
  setTimeout(showResults,700);
}

function showResults(){
  const q=quizScore||0,m=matchScore||0,f=fillScore||0,total=q+m+f,pct=Math.round(total/TOTAL*100);
  document.querySelectorAll('.panel[data-panel]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('results').classList.remove('hidden');
  document.getElementById('scoreBig').textContent=pct+'%';
  document.getElementById('scoreSub').textContent=total+' out of '+TOTAL;
  document.getElementById('breakdown').innerHTML='<div class="bd"><b>'+q+'/'+QUESTIONS.length+'</b><span>Comprehend</span></div><div class="bd"><b>'+m+'/'+MATCH.length+'</b><span>Match</span></div><div class="bd"><b>'+f+'/'+FILLS.length+'</b><span>Use</span></div>';
  let trophy,msg;
  if(pct===100){trophy='🏆';msg=MODULE.win;}
  else if(pct>=80){trophy='🌟';msg='Brilliant work, '+NAME+'! '+MODULE.cheer;}
  else if(pct>=60){trophy='💪';msg='Great effort, '+NAME+' — read once more and beat your score!';}
  else{trophy='🌈';msg='Good try, '+NAME+'! Tap Try again and explore the passage.';}
  document.getElementById('trophy').textContent=trophy;
  document.getElementById('resultMsg').textContent=msg;
  document.getElementById('savedNote').textContent='Scores saved on this device ✓';
  kwlShowResults();
  window.scrollTo({top:0,behavior:'smooth'});
}

function recordSub(sub, best, total){
  var data={};
  try{data=JSON.parse(localStorage.getItem(HUB_KEY)||'{}');}catch(e){data={};}
  var k=PROJECT+':'+sub;
  var rec=data[k]||{best:0,attempts:0};
  rec.best=Math.max(rec.best||0,best);
  rec.attempts=(rec.attempts||0)+1;
  data[k]=rec;
  try{localStorage.setItem(HUB_KEY,JSON.stringify(data));}catch(e){}
  try{window.dispatchEvent(new Event('amara-scores-updated'));}catch(e){}
  if(window.amaraCloud){try{
    if(typeof window.amaraCloud.save==='function')window.amaraCloud.save(data);
    else if(typeof window.amaraCloud.set==='function')window.amaraCloud.set(k,rec);
    else if(typeof window.amaraCloud.sync==='function')window.amaraCloud.sync(data);
  }catch(e){}}
}
const KWL_KEY='kwl-'+PROJECT;
function kwlGet(){try{return JSON.parse(localStorage.getItem(KWL_KEY)||'{}');}catch(e){return{};}}
function kwlSet(key,val){var d=kwlGet();d[key]=val;try{localStorage.setItem(KWL_KEY,JSON.stringify(d));}catch(e){}}
(function(){
  var k=document.getElementById('kwl-k'),w=document.getElementById('kwl-w');
  var d=kwlGet();
  if(k){k.value=d.k||'';k.addEventListener('input',function(){kwlSet('k',k.value);});}
  if(w){w.value=d.w||'';w.addEventListener('input',function(){kwlSet('w',w.value);});}
})();
function kwlShowResults(){
  var d=kwlGet();
  var ks=document.getElementById('kwl-k-show'),ws=document.getElementById('kwl-w-show'),l=document.getElementById('kwl-l');
  if(ks)ks.textContent=d.k||'(nothing written)';
  if(ws)ws.textContent=d.w||'(nothing written)';
  if(l){l.value=d.l||'';l.addEventListener('input',function(){kwlSet('l',l.value);});}
}
function flash(id,kind,text){const el=document.getElementById(id);el.className='feedback show '+kind;el.textContent=text;}
function restart(){location.reload();}
</script>
</body>
</html>
"""

def cssvars(p):
    return ("    --c-primary:%s; --c-dark:%s; --c-deep:%s;\n"
            "    --c-accent:%s; --c-accent-soft:%s;\n"
            "    --c-cream:%s; --c-paper:#ffffff;\n"
            "    --bg-top:%s; --bg-bottom:%s;\n"
            "    --glow1:%s; --glow2:%s;") % (
        p['primary'],p['dark'],p['deep'],p['accent'],p['accentSoft'],
        p['cream'],p['bgTop'],p['bgBottom'],p['glow1'],p['glow2'])

MODULES = [
{
 "activityId":"rainforest",
 "projectKey":"rainforest",
 "title":"Animals of the Rainforest",
 "heroEmoji":"🐆","watermark":"🌿","pageTitle":"Animals of the Rainforest","diagramFile":"diagrams/rainforest.svg",
 "win":"PERFECT, Amara! Queen of the rainforest! 🌴",
 "cheer":"The toucans are cheering for you! 🦜",
 "palette":{"primary":"#1f8a4c","dark":"#176b3d","deep":"#0a3d27","accent":"#7cc242","accentSoft":"#e7f6d8","cream":"#fdfbf4","bgTop":"#f1faf1","bgBottom":"#e7f4ea","glow1":"#2fa55f22","glow2":"#176b3d18"},
 "passageTitle":"Animals of the Rainforest",
 "passageHtml":
"<p>The rainforest is one of the busiest places on Earth. It is split into layers, and different animals live in each one. High above, the leafy <span class=\"voc\">canopy</span> forms a green roof where monkeys swing and colorful birds like toucans search for fruit. Below that, the shady <span class=\"voc\">understory</span> is home to frogs, snakes, and insects that climb the trunks and vines. Down on the dark forest floor, larger animals such as jaguars move quietly between the trees. Because the rainforest is warm and wet all year, an enormous number of plants and animals can live there. Scientists call this huge variety of living things <span class=\"voc\">biodiversity</span>, and no other habitat on land has more of it.</p>"
"<p>Living in such a crowded place is not easy, so rainforest animals have special ways to survive. Many use <span class=\"voc\">camouflage</span>, blending into leaves or bark so that <span class=\"voc\">predator</span>s cannot spot them. The sloth even grows tiny green algae on its fur to help it hide. Camouflage works for hunters too: a jaguar's spotted coat lets it creep up on its <span class=\"voc\">prey</span> without being seen. Some animals are <span class=\"voc\">nocturnal</span>, meaning they sleep during the day and come out at night, when it is cooler and safer. Others protect themselves with bright warning colors instead of hiding — the skin of a poison dart frog tells a hungry predator that it would make a dangerous meal. Over millions of years, each animal has slowly <span class=\"voc\">adapt</span>ed to fit its part of the forest, and that is one reason the rainforest holds so much life.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mostly about?","opts":["How tall rainforest trees grow","How rainforest animals live and survive in different layers","Why jaguars are the strongest animals"],"a":1},
   {"type":"Detail","q":"Where do toucans search for fruit?","opts":["On the dark forest floor","In the shady understory","High in the canopy"],"a":2},
   {"type":"Vocabulary","q":"In the passage, the word \"biodiversity\" means —","opts":["the weather staying warm and wet","the huge variety of living things in a place","the layers of the rainforest"],"a":1},
   {"type":"Inference","q":"Why does the sloth grow green algae on its fur?","opts":["To keep itself warm at night","To blend in and hide from predators","To make its fur grow faster"],"a":1},
   {"type":"Cause & effect","q":"Because the rainforest is warm and wet all year, —","opts":["very few animals can survive there","an enormous number of plants and animals can live there","all the animals must be nocturnal"],"a":1},
   {"type":"Inference","q":"The bright skin of a poison dart frog most likely helps it by —","opts":["warning predators to stay away","helping it swim faster","blending into the green leaves"],"a":0}
 ],
 "match":[
   {"word":"canopy","def":"the leafy top layer of the forest, like a green roof","hint":"\"High above, the leafy <b>canopy</b> forms a green roof…\""},
   {"word":"understory","def":"the shady layer below the treetops","hint":"\"Below that, the shady <b>understory</b> is home to frogs, snakes, and insects…\""},
   {"word":"biodiversity","def":"the huge variety of living things in a place","hint":"\"…this huge variety of living things, <b>biodiversity</b>…\""},
   {"word":"camouflage","def":"colors or patterns that help an animal blend in and hide","hint":"\"Many use <b>camouflage</b>, blending into leaves or bark…\""},
   {"word":"nocturnal","def":"active at night and asleep during the day","hint":"\"Some animals are <b>nocturnal</b> — they sleep during the day and come out at night.\""},
   {"word":"adapt","def":"to slowly change over time to fit where you live","hint":"\"…each animal has slowly <b>adapted</b> to fit its part of the forest.\""}
 ],
 "bank":["canopy","understory","biodiversity","camouflage","nocturnal","predator","prey","adapt"],
 "fills":[
   {"text":"The thick green ___ at the top of the trees blocks most of the sunlight.","a":"canopy"},
   {"text":"Ferns and small bushes grow in the dim ___ beneath the tall trees.","a":"understory"},
   {"text":"A coral reef has high ___ because so many kinds of fish and creatures live there.","a":"biodiversity","challenge":True},
   {"text":"The stick insect uses ___ to look exactly like a twig.","a":"camouflage"},
   {"text":"Owls are ___ animals that hunt mostly after dark.","a":"nocturnal"},
   {"text":"A hawk is a ___ that hunts smaller animals for food.","a":"predator"},
   {"text":"A rabbit is the ___ that the fox tries to catch.","a":"prey"},
   {"text":"Animals that move to a colder place must ___ to survive the winter.","a":"adapt"}
 ]
},
{
 "activityId":"emotional-intelligence",
 "projectKey":"ei",
 "title":"What Is Emotional Intelligence?",
 "heroEmoji":"🧠","watermark":"💭","pageTitle":"Emotional Intelligence","diagramFile":"diagrams/emotional-intelligence.svg",
 "win":"PERFECT, Amara! You really understand feelings! 💛",
 "cheer":"You read with real understanding! 💛",
 "palette":{"primary":"#4f5bd5","dark":"#343fb0","deep":"#262d86","accent":"#7c86ee","accentSoft":"#e8eafe","cream":"#f8f8ff","bgTop":"#f1f1fb","bgBottom":"#e8e9f7","glow1":"#4f5bd522","glow2":"#262d8618"},
 "passageTitle":"What Is Emotional Intelligence?",
 "passageHtml":
"<p>Everyone feels emotions — happiness, anger, worry, and excitement come and go all day long. <span class=\"voc\">Emotion</span>al intelligence is the skill of understanding those feelings and handling them in a helpful way. It starts with being <span class=\"voc\">self-aware</span>, which means noticing what you are feeling and why. For example, you might realise that you snapped at your friend not because of them, but because you were tired and hungry. People who are self-aware can spot a feeling early, before it grows too big. That gives them a chance to choose how they want to <span class=\"voc\">react</span> instead of letting the feeling decide for them.</p>"
"<p>Emotional intelligence is also about other people. <span class=\"voc\">Empathy</span> means imagining how someone else feels and seeing a situation from their <span class=\"voc\">perspective</span>. A friend who notices you are sad and sits with you is using empathy. The second big skill is learning to <span class=\"voc\">regulate</span> your emotions — to manage strong feelings instead of being swept away by them. When <span class=\"voc\">frustration</span> builds, an emotionally intelligent person might take a deep breath, count to ten, or walk away to <span class=\"voc\">calm</span> down before speaking. None of this means hiding your feelings. It means understanding them well enough that they help you, instead of running the show.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mostly about?","opts":["Why people get angry","The skill of understanding and handling emotions","How to make new friends"],"a":1},
   {"type":"Detail","q":"According to the passage, emotional intelligence starts with —","opts":["being self-aware","counting to ten","making other people happy"],"a":0},
   {"type":"Vocabulary","q":"In the passage, \"empathy\" means —","opts":["hiding what you feel","imagining how someone else feels","winning an argument"],"a":1},
   {"type":"Cause & effect","q":"Why might someone take a deep breath when frustration builds?","opts":["to calm down before speaking","to ignore the problem forever","to make others feel bad"],"a":0},
   {"type":"Inference","q":"The person who \"snapped at a friend\" was really upset because —","opts":["the friend was mean to them","they were tired and hungry","they wanted to be alone"],"a":1},
   {"type":"Inference","q":"The passage suggests emotional intelligence means you should —","opts":["hide your feelings from everyone","understand your feelings so they help you","only think about yourself"],"a":1}
 ],
 "match":[
   {"word":"empathy","def":"imagining how another person feels and seeing their side","hint":"\"<b>Empathy</b> means imagining how someone else feels…\""},
   {"word":"self-aware","def":"noticing what you are feeling and why","hint":"\"being <b>self-aware</b>, which means noticing what you are feeling and why.\""},
   {"word":"regulate","def":"to manage strong feelings instead of being swept away","hint":"\"learning to <b>regulate</b> your emotions — to manage strong feelings…\""},
   {"word":"frustration","def":"the annoyed feeling when something is hard or blocked","hint":"\"When <b>frustration</b> builds, an emotionally intelligent person might take a deep breath…\""},
   {"word":"react","def":"to act or respond when something happens","hint":"\"…choose how they want to <b>react</b> instead of letting the feeling decide.\""},
   {"word":"perspective","def":"the way a person sees or understands a situation","hint":"\"…seeing a situation from their <b>perspective</b>.\""}
 ],
 "bank":["emotion","empathy","self-aware","regulate","frustration","react","calm","perspective"],
 "fills":[
   {"text":"A sudden feeling like joy or anger is called an ___.","a":"emotion"},
   {"text":"Being ___ means you can name what you feel and why.","a":"self-aware"},
   {"text":"She showed ___ by comforting her friend who lost the game.","a":"empathy"},
   {"text":"When you ___ your feelings, you manage them instead of exploding.","a":"regulate"},
   {"text":"He felt ___ when the puzzle would not fit together.","a":"frustration"},
   {"text":"Try to ___ down by breathing slowly before you answer.","a":"calm"},
   {"text":"In a drawing, ___ makes faraway objects look smaller than close ones.","a":"perspective","challenge":True},
   {"text":"A wise person thinks before they ___ to bad news.","a":"react"}
 ]
},
{
 "activityId":"spaghetti",
 "projectKey":"spaghetti",
 "title":"How Spaghetti Is Made",
 "heroEmoji":"🍝","watermark":"🍅","pageTitle":"How Spaghetti Is Made","diagramFile":"diagrams/spaghetti.svg",
 "win":"PERFECT, Amara! Master of the pasta process! 🍝",
 "cheer":"The chefs are clapping for you! 🍅",
 "palette":{"primary":"#d6402c","dark":"#a82a1a","deep":"#7e1d10","accent":"#ef7a52","accentSoft":"#fde3da","cream":"#fff7f1","bgTop":"#fdf1ec","bgBottom":"#fae7df","glow1":"#d6402c22","glow2":"#7e1d1018"},
 "passageTitle":"How Spaghetti Is Made",
 "passageHtml":
"<p>Have you ever wondered how a hard, dry strand of spaghetti begins? It starts in a wheat field. Spaghetti is made from a special kind of wheat called <span class=\"voc\">durum</span>, which is harder than the wheat used for bread. At the mill, the durum grains are ground into a coarse, golden flour called <span class=\"voc\">semolina</span>. To turn semolina into pasta, workers mix it with water to form a stiff <span class=\"voc\">dough</span>. Machines then <span class=\"voc\">knead</span> the dough, pressing and folding it over and over until it becomes smooth and even. Unlike bread dough, pasta dough has very few <span class=\"voc\">ingredient</span>s — usually just semolina and water — so the wheat's flavour really stands out.</p>"
"<p>Next comes the part that gives spaghetti its shape. The dough is pushed through a metal disc full of tiny round holes, a step called <span class=\"voc\">extrud</span>ing. As the dough is forced through the holes, it comes out as long, thin strings. The strings are cut to length and laid out to <span class=\"voc\">dry</span>. Drying is the slowest step; the pasta must lose its moisture slowly, sometimes over many hours, or it will crack. Once it is fully dry and firm, the spaghetti is weighed and sent to a machine that will <span class=\"voc\">package</span> it into boxes or bags. From a field of golden wheat to the box on a shelf, every strand follows the same careful process.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mostly about?","opts":["How bread is baked","The steps that turn wheat into spaghetti","Why wheat fields are golden"],"a":1},
   {"type":"Detail","q":"Spaghetti is made from a special wheat called —","opts":["semolina","durum","dough"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"extruding\" means —","opts":["cutting pasta into squares","pushing dough through holes to shape it","drying the pasta slowly"],"a":1},
   {"type":"Cause & effect","q":"Why must the pasta be dried slowly?","opts":["so it does not crack","so it tastes sweeter","so it cooks faster"],"a":0},
   {"type":"Detail","q":"Pasta dough is different from bread dough because it —","opts":["has very few ingredients","is baked in an oven","is made from rice"],"a":0},
   {"type":"Inference","q":"You can tell from the passage that making spaghetti is —","opts":["a careful, step-by-step process","done entirely by hand","finished in a few minutes"],"a":0}
 ],
 "match":[
   {"word":"durum","def":"a hard kind of wheat used to make pasta","hint":"\"a special kind of wheat called <b>durum</b>, which is harder than… bread.\""},
   {"word":"semolina","def":"the coarse, golden flour made from durum wheat","hint":"\"ground into a coarse, golden flour called <b>semolina</b>.\""},
   {"word":"dough","def":"a stiff mixture of flour and water","hint":"\"mix it with water to form a stiff <b>dough</b>.\""},
   {"word":"knead","def":"to press and fold dough until it is smooth","hint":"\"Machines then <b>knead</b> the dough, pressing and folding it…\""},
   {"word":"extrude","def":"to push dough through holes to give it a shape","hint":"\"pushed through a metal disc… a step called <b>extruding</b>.\""},
   {"word":"ingredient","def":"one of the things used to make a food","hint":"\"pasta dough has very few <b>ingredients</b> — usually just semolina and water.\""}
 ],
 "bank":["durum","semolina","dough","knead","extrude","dry","ingredient","package"],
 "fills":[
   {"text":"Pasta begins as a hard wheat called ___.","a":"durum"},
   {"text":"The durum is ground into a golden flour called ___.","a":"semolina"},
   {"text":"Flour and water are mixed to make a stiff ___.","a":"dough"},
   {"text":"Machines ___ the dough by pressing and folding it.","a":"knead"},
   {"text":"To give spaghetti its shape, machines ___ the dough through tiny holes.","a":"extrude"},
   {"text":"After shaping, the strands must ___ slowly so they do not crack.","a":"dry"},
   {"text":"Sugar is the main ___ in most candy.","a":"ingredient","challenge":True},
   {"text":"Finally, a machine will ___ the spaghetti into boxes.","a":"package"}
 ]
},
{
 "activityId":"celebrations",
 "projectKey":"celebrations",
 "title":"Celebrations Around the World",
 "heroEmoji":"🎉","watermark":"🎊","pageTitle":"Celebrations Around the World","diagramFile":"diagrams/celebrations.svg",
 "win":"PERFECT, Amara! A true world explorer! 🎉",
 "cheer":"The whole world is cheering for you! 🎊",
 "palette":{"primary":"#c026a3","dark":"#9a127f","deep":"#6e0c5c","accent":"#f4b400","accentSoft":"#fbe5f5","cream":"#fff7fc","bgTop":"#fbeef8","bgBottom":"#f6e3f3","glow1":"#c026a322","glow2":"#f4b40022"},
 "passageTitle":"Celebrations Around the World",
 "passageHtml":
"<p>All around the world, people <span class=\"voc\">celebrate</span> special days that are important to them. The beliefs, foods, music, and customs that a group of people share are called their <span class=\"voc\">culture</span>. Many celebrations are part of a <span class=\"voc\">tradition</span> — something passed down from parents and grandparents over many years. A <span class=\"voc\">custom</span> is one particular way of doing something, like lighting candles, wearing special clothes, or sharing a certain meal. These traditions are part of a family's <span class=\"voc\">heritage</span>, the history and ways of life handed down from their <span class=\"voc\">ancestor</span>s. Even when people move to new countries, they often keep their celebrations alive so their children can learn where they came from.</p>"
"<p>Festivals look different from place to place, but they share a common purpose. In India, families light rows of small lamps during Diwali, the festival of lights. In Mexico, people honour relatives who have died during the Day of the Dead, decorating with flowers and favourite foods. In China, the Lunar New Year fills streets with red decorations and dragon dances. Each <span class=\"voc\">festival</span> brings a <span class=\"voc\">community</span> together to remember what matters to them. By learning about other people's celebrations, we discover how much we have in common: nearly everyone, everywhere, loves to gather, share food, and honour the people and stories that shaped them.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mostly about —","opts":["how to cook festival food","how cultures celebrate and why it matters","which country has the best holiday"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"culture\" means —","opts":["a kind of festival food","the shared beliefs, foods, music, and customs of a group","a country's weather"],"a":1},
   {"type":"Detail","q":"During Diwali in India, families —","opts":["light rows of small lamps","wear red dragon costumes","decorate graves with flowers"],"a":0},
   {"type":"Detail","q":"The Day of the Dead in Mexico honours —","opts":["famous kings and queens","relatives who have died","the start of summer"],"a":1},
   {"type":"Cause & effect","q":"Why do people keep their celebrations alive after moving to new countries?","opts":["so their children can learn where they came from","so they can win prizes","so they never learn a new language"],"a":0},
   {"type":"Inference","q":"The passage suggests that celebrations around the world —","opts":["have nothing in common","show how much people everywhere are alike","are only about food"],"a":1}
 ],
 "match":[
   {"word":"culture","def":"the shared beliefs, foods, music, and customs of a group","hint":"\"…that a group of people share are called their <b>culture</b>.\""},
   {"word":"tradition","def":"something passed down from parents and grandparents over years","hint":"\"part of a <b>tradition</b> — something passed down from parents and grandparents…\""},
   {"word":"custom","def":"one particular way of doing something","hint":"\"A <b>custom</b> is one particular way of doing something, like lighting candles…\""},
   {"word":"heritage","def":"the history and ways of life handed down in a family","hint":"\"part of a family's <b>heritage</b>, the history and ways of life handed down…\""},
   {"word":"community","def":"a group of people who share a place or way of life","hint":"\"Each festival brings a <b>community</b> together…\""},
   {"word":"ancestor","def":"a family member who lived long before you","hint":"\"…handed down from their <b>ancestors</b>.\""}
 ],
 "bank":["culture","tradition","custom","heritage","celebrate","community","ancestor","festival"],
 "fills":[
   {"text":"The food, music, and beliefs a group shares make up their ___.","a":"culture"},
   {"text":"Lighting candles every year can become a family ___.","a":"tradition"},
   {"text":"Shaking hands when you meet someone is a common ___.","a":"custom"},
   {"text":"My grandparents taught me dances that are part of my ___.","a":"heritage"},
   {"text":"People all over town came to the street ___ with music and dancing.","a":"festival"},
   {"text":"Our whole ___ helped clean up the park on Saturday.","a":"community"},
   {"text":"A great-great-grandmother is an example of an ___.","a":"ancestor"},
   {"text":"The scientists ___ when their long experiment finally worked.","a":"celebrate","challenge":True}
 ]
},
{
 "activityId":"dogs",
 "projectKey":"dogs",
 "title":"All About Dogs",
 "heroEmoji":"🐕","watermark":"🐾","pageTitle":"All About Dogs","diagramFile":"diagrams/dogs.svg",
 "win":"PERFECT, Amara! Top dog! 🐶",
 "cheer":"The puppies are wagging their tails for you! 🐾",
 "palette":{"primary":"#92591f","dark":"#6f4416","deep":"#432a0d","accent":"#cf9a55","accentSoft":"#f3e6d4","cream":"#fdfaf4","bgTop":"#f7f1e8","bgBottom":"#efe6d8","glow1":"#92591f22","glow2":"#6f441618"},
 "passageTitle":"All About Dogs",
 "passageHtml":
"<p>Dogs are often called our best friends, and they have lived alongside people for a very long time. Scientists believe all dogs <span class=\"voc\">descend</span> from wolves that began living near humans thousands of years ago. Over many generations, people kept the friendliest wolves, and slowly these animals became tame, or <span class=\"voc\">domesticate</span>d. A domesticated animal is one that has been changed over time to live safely with humans. Today there are hundreds of different kinds, or <span class=\"voc\">breed</span>s, of dog, from tiny Chihuahuas to giant Great Danes. Even though they look so different, every breed shares the same wolf ancestors.</p>"
"<p>Although dogs are gentle <span class=\"voc\">companion</span>s, many of their behaviours come from <span class=\"voc\">instinct</span> — a way of acting an animal is born knowing, without being taught. A puppy that circles before lying down or buries a toy is following an instinct from its wild past. Dogs also have powerful <span class=\"voc\">sense</span>s: their hearing and especially their sense of smell are far sharper than ours. Because they are <span class=\"voc\">loyal</span> and eager to please, dogs can be <span class=\"voc\">train</span>ed to do important jobs — guiding people who cannot see, sniffing out danger, or herding sheep. It is this mix of friendship and ability that has kept dogs and humans together for so long.</p>",
 "questions":[
   {"type":"Main idea","q":"What is the passage mostly about?","opts":["How to train a Great Dane","Where dogs came from and what makes them special","Why wolves are dangerous"],"a":1},
   {"type":"Detail","q":"Scientists believe dogs descend from —","opts":["foxes","wolves","wild cats"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"instinct\" means —","opts":["a trick a dog is taught at school","a way of acting an animal is born knowing","a kind of dog breed"],"a":1},
   {"type":"Cause & effect","q":"Dogs can be trained to do important jobs because they are —","opts":["loyal and eager to please","bigger than wolves","unable to smell"],"a":0},
   {"type":"Detail","q":"Which sense is described as especially sharp in dogs?","opts":["taste","smell","sight"],"a":1},
   {"type":"Inference","q":"A puppy that buries a toy is —","opts":["following an instinct from its wild past","trying to plant a tree","copying a cat"],"a":0}
 ],
 "match":[
   {"word":"domesticate","def":"to change an animal over time so it can live with humans","hint":"\"…became tame, or <b>domesticate</b>d.\""},
   {"word":"breed","def":"one particular kind of dog","hint":"\"…hundreds of different kinds, or <b>breed</b>s, of dog…\""},
   {"word":"instinct","def":"a way of acting an animal is born knowing","hint":"\"…<b>instinct</b> — a way of acting an animal is born knowing…\""},
   {"word":"descend","def":"to come from an earlier kind of animal","hint":"\"…all dogs <b>descend</b> from wolves…\""},
   {"word":"companion","def":"a friend who keeps you company","hint":"\"…dogs are gentle <b>companion</b>s…\""},
   {"word":"loyal","def":"faithful and sticking by someone","hint":"\"…they are <b>loyal</b> and eager to please…\""}
 ],
 "bank":["domesticate","breed","loyal","instinct","descend","companion","sense","train"],
 "fills":[
   {"text":"Cows and chickens are animals that humans ___d long ago to live with them.","a":"domesticate"},
   {"text":"A poodle is one ___ of dog, and a bulldog is another.","a":"breed"},
   {"text":"A good dog is ___ and stays by your side.","a":"loyal"},
   {"text":"Birds build nests by ___, without ever being taught.","a":"instinct"},
   {"text":"All dogs ___ from ancient wolves.","a":"descend"},
   {"text":"My dog is my favourite ___ on long walks.","a":"companion"},
   {"text":"A dog's ___ of smell is much stronger than a human's.","a":"sense"},
   {"text":"With patience, you can ___ a parrot to say words.","a":"train","challenge":True}
 ]
},
{
 "activityId":"boa-constrictors",
 "projectKey":"boa",
 "title":"The Boa Constrictor",
 "heroEmoji":"🐍","watermark":"🐍","pageTitle":"Boa Constrictors","diagramFile":"diagrams/boa-constrictors.svg",
 "win":"PERFECT, Amara! A powerful effort! 🐍",
 "cheer":"You squeezed every answer right! 🐍",
 "palette":{"primary":"#7c8a1e","dark":"#5e6916","deep":"#353c0a","accent":"#b3bf57","accentSoft":"#eef2d6","cream":"#fbfbf2","bgTop":"#f4f6e6","bgBottom":"#ebeed7","glow1":"#7c8a1e22","glow2":"#5e691618"},
 "passageTitle":"The Boa Constrictor",
 "passageHtml":
"<p>The boa constrictor is a large snake found in the warm forests of Central and South America. Unlike some snakes, a boa is not venomous — it has no poison. Instead, it gets its name from the way it catches food. A boa will <span class=\"voc\">ambush</span> its <span class=\"voc\">prey</span>, waiting quietly and hidden before striking suddenly. Once it grabs an animal, the boa wraps its strong body around it and begins to <span class=\"voc\">constrict</span>, or squeeze. Each time the animal breathes out, the snake tightens its coils a little more, until the prey can no longer breathe and <span class=\"voc\">suffocate</span>s. The whole hunt can be over in minutes.</p>"
"<p>A boa's body is built for this life. Its skin is covered in smooth, overlapping <span class=\"voc\">scale</span>s, patterned in browns and tans that act as <span class=\"voc\">camouflage</span> against the forest floor. Like all reptiles, the boa is <span class=\"voc\">cold-blooded</span>, which means its body temperature changes with the air around it, so it suns itself to warm up and rests in the shade to cool down. After a big meal, a boa can go for weeks without eating again, because it takes a long time for its body to <span class=\"voc\">digest</span>, or break down, such a large amount of food. A boa constrictor is a patient and powerful hunter.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mostly about —","opts":["how boas build nests","how a boa constrictor hunts and lives","why boas are venomous"],"a":1},
   {"type":"Detail","q":"A boa constrictor catches food by —","opts":["injecting venom","squeezing its prey","chasing prey for hours"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"camouflage\" means —","opts":["colours and patterns that help it hide","the snake's sharp teeth","a warm, sunny spot"],"a":0},
   {"type":"Cause & effect","q":"A boa suns itself because it is —","opts":["cold-blooded and needs warmth","hungry for plants","trying to scare predators"],"a":0},
   {"type":"Detail","q":"After a big meal, a boa can —","opts":["go for weeks without eating","eat again right away","stop breathing"],"a":0},
   {"type":"Inference","q":"Because a boa ambushes its prey, it must be good at —","opts":["running very fast","staying still and hidden","climbing the tallest trees"],"a":1}
 ],
 "match":[
   {"word":"constrict","def":"to squeeze tightly","hint":"\"…wraps its strong body around it and begins to <b>constrict</b>, or squeeze.\""},
   {"word":"suffocate","def":"to be unable to breathe","hint":"\"…the prey can no longer breathe and <b>suffocate</b>s.\""},
   {"word":"cold-blooded","def":"having a body temperature that changes with the surroundings","hint":"\"…the boa is <b>cold-blooded</b>, which means its body temperature changes with the air…\""},
   {"word":"camouflage","def":"colours or patterns that help an animal hide","hint":"\"…patterned in browns and tans that act as <b>camouflage</b>…\""},
   {"word":"ambush","def":"to hide and attack by surprise","hint":"\"A boa will <b>ambush</b> its prey, waiting quietly and hidden…\""},
   {"word":"digest","def":"to break down food inside the body","hint":"\"…it takes a long time for its body to <b>digest</b>, or break down… food.\""}
 ],
 "bank":["constrict","prey","suffocate","camouflage","cold-blooded","scales","digest","ambush"],
 "fills":[
   {"text":"The snake began to ___ the mouse by squeezing it.","a":"constrict"},
   {"text":"A lion hunts a zebra, so the zebra is its ___.","a":"prey"},
   {"text":"Without any air, a creature will ___.","a":"suffocate"},
   {"text":"The moth's grey wings are perfect ___ against tree bark.","a":"camouflage"},
   {"text":"Snakes and lizards are ___ animals that warm up in the sun.","a":"cold-blooded"},
   {"text":"A snake's body is covered in smooth ___.","a":"scales"},
   {"text":"It takes hours for your stomach to ___ a big lunch.","a":"digest","challenge":True},
   {"text":"The cat liked to ___ its toy from behind the couch.","a":"ambush"}
 ]
},
{
 "activityId":"the-wheel",
 "projectKey":"wheel",
 "title":"Why the Wheel Changed the World",
 "heroEmoji":"🛞","watermark":"⚙️","pageTitle":"The Importance of the Wheel","diagramFile":"diagrams/the-wheel.svg",
 "win":"PERFECT, Amara! You're really rolling! 🛞",
 "cheer":"Your thinking is in full motion! ⚙️",
 "palette":{"primary":"#3f6f9c","dark":"#2f567a","deep":"#1e3850","accent":"#7aa3c6","accentSoft":"#e2edf6","cream":"#f6f9fc","bgTop":"#eef4fa","bgBottom":"#e3edf5","glow1":"#3f6f9c22","glow2":"#1e385018"},
 "passageTitle":"Why the Wheel Changed the World",
 "passageHtml":
"<p>Some <span class=\"voc\">invention</span>s are so useful that it is hard to imagine life without them, and the wheel is one of the greatest of all. People made the first wheels more than 5,000 years ago, but a wheel by itself does not do much. The real breakthrough came when someone joined a wheel to a rod called an <span class=\"voc\">axle</span>, which lets the wheel <span class=\"voc\">rotate</span>, or spin, freely while holding it in place. Interestingly, early wheels were not used for travel at all — they were laid flat and used to shape clay pots. Only later did people stand them up and use them to move things.</p>"
"<p>Once wheels and axles were placed under carts, everything changed. Suddenly people could <span class=\"voc\">transport</span> heavy loads and <span class=\"voc\">goods</span> over long distances far more <span class=\"voc\">efficient</span>ly than carrying them by hand. Farmers could bring crops to market, traders could travel between towns, and builders could haul stone for huge structures. The wheel became part of almost every <span class=\"voc\">machine</span> humans built, from water mills to clocks to cars. Many historians believe the wheel helped early <span class=\"voc\">civilization</span>s — large, organized groups of people living together — to grow, trade, and share ideas. A simple round shape truly helped build the modern world.</p>",
 "questions":[
   {"type":"Main idea","q":"The passage is mostly about —","opts":["how to make a clay pot","why the wheel was such an important invention","who invented the first car"],"a":1},
   {"type":"Detail","q":"A wheel can spin freely when it is joined to a —","opts":["clay pot","rod called an axle","market stall"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"transport\" means —","opts":["to shape clay","to move things from place to place","to spin in a circle"],"a":1},
   {"type":"Detail","q":"The first wheels were used to —","opts":["shape clay pots","race chariots","power clocks"],"a":0},
   {"type":"Cause & effect","q":"After wheels were put under carts, people could —","opts":["carry less than before","move heavy goods more efficiently","stop trading with other towns"],"a":1},
   {"type":"Inference","q":"The passage suggests the wheel helped civilizations by —","opts":["making it easier to trade and share ideas","keeping people from travelling","replacing all farmers"],"a":0}
 ],
 "match":[
   {"word":"invention","def":"something new that someone creates for the first time","hint":"\"Some <b>invention</b>s are so useful…\""},
   {"word":"axle","def":"a rod that a wheel turns on","hint":"\"…a rod called an <b>axle</b>, which lets the wheel rotate…\""},
   {"word":"transport","def":"to move things from one place to another","hint":"\"…people could <b>transport</b> heavy loads…\""},
   {"word":"civilization","def":"a large, organized group of people living together","hint":"\"…<b>civilization</b>s — large, organized groups of people living together…\""},
   {"word":"efficient","def":"done quickly and without wasted effort","hint":"\"…far more <b>efficient</b>ly than carrying them by hand.\""},
   {"word":"rotate","def":"to turn or spin around","hint":"\"…lets the wheel <b>rotate</b>, or spin, freely…\""}
 ],
 "bank":["invention","axle","transport","goods","civilization","efficient","rotate","machine"],
 "fills":[
   {"text":"The telephone was a famous ___ that changed how people talk.","a":"invention"},
   {"text":"The wheel spins around a metal ___.","a":"axle"},
   {"text":"Trucks and trains ___ food across the country.","a":"transport"},
   {"text":"Shops sell all kinds of ___, like clothes and toys.","a":"goods"},
   {"text":"Ancient Egypt was an early ___ along the Nile River.","a":"civilization"},
   {"text":"Using a wheelbarrow is a more ___ way to move bricks.","a":"efficient"},
   {"text":"The Earth ___s once every day, giving us day and night.","a":"rotate","challenge":True},
   {"text":"A bicycle is a simple ___ that uses two wheels.","a":"machine"}
 ]
},
{
 "activityId":"fashion-history",
 "projectKey":"fashion",
 "title":"A Short History of Fashion",
 "heroEmoji":"👗","watermark":"🧵","pageTitle":"Fashion History","diagramFile":"diagrams/fashion-history.svg",
 "win":"PERFECT, Amara! Effortlessly stylish! 👗",
 "cheer":"You're a fashion historian now! 🧵",
 "palette":{"primary":"#7a3b9c","dark":"#5e2c7a","deep":"#3c1a52","accent":"#b985d6","accentSoft":"#f0e4f8","cream":"#fcf8fe","bgTop":"#f4ecf9","bgBottom":"#ece0f3","glow1":"#7a3b9c22","glow2":"#3c1a5218"},
 "passageTitle":"A Short History of Fashion",
 "passageHtml":
"<p><span class=\"voc\">Fashion</span> — the styles of clothing people choose to wear — has changed in every <span class=\"voc\">era</span> of history. Long ago, people made <span class=\"voc\">garment</span>s by hand from whatever materials they could find, such as animal skins, wool, and plant fibres. They learned to <span class=\"voc\">weave</span> threads together to create <span class=\"voc\">fabric</span>, and over time these woven <span class=\"voc\">textile</span>s became softer, stronger, and more colourful. In ancient Egypt, light linen kept people cool, while heavy furs warmed people in colder lands. What someone wore often showed where they lived, what work they did, and even how rich they were.</p>"
"<p>For most of history, clothes were sewn one at a time by a <span class=\"voc\">tailor</span>, a person skilled at cutting and stitching fabric to fit a body. Because each garment took so long to make, styles changed slowly. That changed when machines began making cloth and clothing quickly in factories. Suddenly new styles, or <span class=\"voc\">trend</span>s, could spread to many people at once. Today a popular trend can travel around the world in days through pictures and the internet. Yet fashion still does what it always has: it lets people show who they are, and it connects us to the time and place we live in.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mostly about —","opts":["how to sew a dress","how fashion and clothing have changed through history","why linen is the best fabric"],"a":1},
   {"type":"Vocabulary","q":"In the passage, \"garment\" means —","opts":["a piece of clothing","a sewing machine","a kind of factory"],"a":0},
   {"type":"Detail","q":"People made early fabric by —","opts":["printing it on paper","weaving threads together","buying it in stores"],"a":1},
   {"type":"Detail","q":"In ancient Egypt, people wore light linen because it —","opts":["kept them cool","was very heavy","showed they were poor"],"a":0},
   {"type":"Cause & effect","q":"Styles used to change slowly because each garment was —","opts":["made quickly in factories","sewn one at a time by a tailor","worn only by the rich"],"a":1},
   {"type":"Inference","q":"The passage suggests that today trends spread quickly because of —","opts":["pictures and the internet","slower hand-sewing","fewer kinds of clothing"],"a":0}
 ],
 "match":[
   {"word":"textile","def":"a woven cloth or fabric","hint":"\"…these woven <b>textile</b>s became softer, stronger…\""},
   {"word":"trend","def":"a style that becomes popular for a while","hint":"\"…new styles, or <b>trend</b>s, could spread to many people…\""},
   {"word":"garment","def":"a piece of clothing","hint":"\"…people made <b>garment</b>s by hand…\""},
   {"word":"weave","def":"to cross threads over and under to make cloth","hint":"\"They learned to <b>weave</b> threads together to create fabric.\""},
   {"word":"tailor","def":"a person who makes clothes to fit a body","hint":"\"…sewn one at a time by a <b>tailor</b>…\""},
   {"word":"era","def":"a period of time in history","hint":"\"…has changed in every <b>era</b> of history.\""}
 ],
 "bank":["fashion","fabric","textile","trend","garment","weave","tailor","era"],
 "fills":[
   {"text":"The clothes and styles people like to wear are called ___.","a":"fashion"},
   {"text":"This shirt is made from a soft cotton ___.","a":"fabric"},
   {"text":"A spider can ___ a web out of silky threads.","a":"weave","challenge":True},
   {"text":"Bright colours are a popular ___ this year.","a":"trend"},
   {"text":"A coat is a warm ___ for winter.","a":"garment"},
   {"text":"Factories turn cotton into ___ used for clothes and sheets.","a":"textile"},
   {"text":"The ___ measured him carefully before making the suit.","a":"tailor"},
   {"text":"The Stone Age was an ___ long before cities were built.","a":"era"}
 ]
},
{
 "activityId":"roblox",
 "projectKey":"roblox",
 "name":"Dani","hubKey":"daniReading","hubFile":"dani.html",
 "useLead":"Tap a word to fill the blank, or type it. You can do it!",
 "title":"What Is Roblox?",
 "heroEmoji":"🎮","watermark":"🕹️","pageTitle":"Roblox","diagramFile":"diagrams/roblox.svg",
 "win":"PERFECT, Dani! You're a star! 🌟",
 "cheer":"Great reading, Dani! 🎮",
 "palette":{"primary":"#2f7de1","dark":"#235fab","deep":"#173f73","accent":"#7fb0ee","accentSoft":"#e1edfb","cream":"#f5f9fe","bgTop":"#eef4fc","bgBottom":"#e3edf8","glow1":"#2f7de122","glow2":"#173f7318"},
 "passageTitle":"Playing on Roblox",
 "passageHtml":
"<p>Roblox is a place to play <span class=\"voc\">online</span>. It has lots of fun games. You can run, jump, and <span class=\"voc\">explore</span> in them. In Roblox you make a <span class=\"voc\">character</span> called an <span class=\"voc\">avatar</span>. Your avatar can wear fun clothes and hats. You can play with your friends at the same time.</p>"
"<p>Some people even <span class=\"voc\">build</span> their own games for others to play. Roblox is all about playing and making things together. It is a fun way to play and use your ideas.</p>",
 "questions":[
   {"type":"Main idea","q":"What is Roblox?","opts":["A kind of food","A place to play games online","A pet"],"a":1},
   {"type":"Detail","q":"What do you make in Roblox?","opts":["a sandwich","an avatar","a car"],"a":1},
   {"type":"Detail","q":"Your avatar can wear —","opts":["nothing","shoes only","fun clothes and hats"],"a":2},
   {"type":"Detail","q":"You can play with —","opts":["your friends","no one","only grown-ups"],"a":0},
   {"type":"Vocabulary","q":"\"Explore\" means —","opts":["to go to sleep","to look around a new place","to eat"],"a":1}
 ],
 "match":[
   {"word":"online","def":"on the internet","hint":"\"Roblox is a place to play <b>online</b>.\""},
   {"word":"avatar","def":"a character that stands for you in a game","hint":"\"you make a character called an <b>avatar</b>.\""},
   {"word":"character","def":"a person or creature in a game or story","hint":"\"you make a <b>character</b> called an avatar.\""},
   {"word":"explore","def":"to look around a new place","hint":"\"You can run, jump, and <b>explore</b> in them.\""},
   {"word":"build","def":"to make something by putting parts together","hint":"\"Some people even <b>build</b> their own games…\""}
 ],
 "bank":["online","avatar","character","explore","build","game"],
 "fills":[
   {"text":"Roblox is a game you play ___.","a":"online"},
   {"text":"Your ___ wears fun clothes.","a":"avatar"},
   {"text":"A dragon in a story is a ___.","a":"character"},
   {"text":"We like to ___ the new park.","a":"explore"},
   {"text":"I will ___ a tall tower with blocks.","a":"build"},
   {"text":"We played a fun ___ together.","a":"game"}
 ]
},
{
 "activityId":"poodles",
 "projectKey":"poodles",
 "name":"Dani","hubKey":"daniReading","hubFile":"dani.html",
 "useLead":"Tap a word to fill the blank, or type it. You can do it!",
 "title":"Types of Poodles",
 "heroEmoji":"🐩","watermark":"🐩","pageTitle":"Types of Poodles","diagramFile":"diagrams/poodles.svg",
 "win":"PERFECT, Dani! Top dog! 🐩",
 "cheer":"The poodles are proud of you, Dani! 🐩",
 "palette":{"primary":"#e0577f","dark":"#b53e62","deep":"#7e2742","accent":"#f0a0ba","accentSoft":"#fbe4ec","cream":"#fef6f9","bgTop":"#fceef3","bgBottom":"#f7e2ea","glow1":"#e0577f22","glow2":"#7e274218"},
 "passageTitle":"Types of Poodles",
 "passageHtml":
"<p>A <span class=\"voc\">poodle</span> is a dog with soft, <span class=\"voc\">curly</span> fur. There are three sizes of poodle. The biggest is the <span class=\"voc\">standard</span> poodle. The middle size is the <span class=\"voc\">miniature</span> poodle. The smallest is the <span class=\"voc\">toy</span> poodle.</p>"
"<p>Poodles are very smart and learn tricks fast. Their fur can be black, white, or brown. People love poodles because they are kind and <span class=\"voc\">clever</span>.</p>",
 "questions":[
   {"type":"Main idea","q":"This is mostly about —","opts":["cats","types of poodles","fish"],"a":1},
   {"type":"Detail","q":"How many sizes of poodle are there?","opts":["ten","one","three"],"a":2},
   {"type":"Detail","q":"The biggest poodle is the —","opts":["toy poodle","standard poodle","baby poodle"],"a":1},
   {"type":"Detail","q":"A poodle's fur is —","opts":["flat","green","curly"],"a":2},
   {"type":"Vocabulary","q":"\"Clever\" means —","opts":["smart","slow","tired"],"a":0}
 ],
 "match":[
   {"word":"curly","def":"having curls, not straight","hint":"\"a dog with soft, <b>curly</b> fur.\""},
   {"word":"standard","def":"the biggest size of poodle","hint":"\"The biggest is the <b>standard</b> poodle.\""},
   {"word":"miniature","def":"a small or middle size","hint":"\"The middle size is the <b>miniature</b> poodle.\""},
   {"word":"toy","def":"the smallest size","hint":"\"The smallest is the <b>toy</b> poodle.\""},
   {"word":"clever","def":"smart and quick to learn","hint":"\"they are kind and <b>clever</b>.\""}
 ],
 "bank":["poodle","curly","standard","miniature","toy","clever"],
 "fills":[
   {"text":"A ___ is a dog with curly fur.","a":"poodle"},
   {"text":"The poodle has soft, ___ hair.","a":"curly"},
   {"text":"The big dog is a ___ poodle.","a":"standard"},
   {"text":"The middle-size dog is a ___ poodle.","a":"miniature"},
   {"text":"The tiny dog is a ___ poodle.","a":"toy"},
   {"text":"My dog is so ___ it can do tricks.","a":"clever"}
 ]
},
{
 "activityId":"fashion-and-clothing",
 "projectKey":"fashionk",
 "name":"Dani","hubKey":"daniReading","hubFile":"dani.html",
 "useLead":"Tap a word to fill the blank, or type it. You can do it!",
 "title":"Clothes We Wear",
 "heroEmoji":"👗","watermark":"🧥","pageTitle":"Fashion and Clothing","diagramFile":"diagrams/fashion-and-clothing.svg",
 "win":"PERFECT, Dani! So stylish! 👗",
 "cheer":"You dressed up every answer, Dani! 👗",
 "palette":{"primary":"#f08a24","dark":"#c66c11","deep":"#8a4806","accent":"#f7b777","accentSoft":"#fdecd8","cream":"#fff9f2","bgTop":"#fdf2e6","bgBottom":"#f8e8d6","glow1":"#f08a2422","glow2":"#8a480618"},
 "passageTitle":"Clothes We Wear",
 "passageHtml":
"<p>We wear <span class=\"voc\">clothes</span> every day. Clothes keep us warm or cool. In winter we wear a <span class=\"voc\">coat</span> and a hat. In summer we wear shorts and a <span class=\"voc\">shirt</span>. Some clothes are for special days, like a party <span class=\"voc\">dress</span>.</p>"
"<p>People pick clothes in colors they like. The clothes you choose are part of your <span class=\"voc\">style</span>. Getting dressed can be fun!</p>",
 "questions":[
   {"type":"Main idea","q":"This is mostly about —","opts":["how to cook","clothes we wear","cars"],"a":1},
   {"type":"Detail","q":"In winter we wear a —","opts":["coat","swimsuit","nothing"],"a":0},
   {"type":"Detail","q":"In summer we wear —","opts":["a heavy coat","shorts and a shirt","boots and mittens"],"a":1},
   {"type":"Detail","q":"A party dress is for —","opts":["sleeping","swimming","special days"],"a":2},
   {"type":"Vocabulary","q":"Your \"style\" is —","opts":["the way you like to dress","your favorite food","your pet"],"a":0}
 ],
 "match":[
   {"word":"clothes","def":"things you wear, like shirts and pants","hint":"\"We wear <b>clothes</b> every day.\""},
   {"word":"coat","def":"a warm thing you wear outside","hint":"\"In winter we wear a <b>coat</b> and a hat.\""},
   {"word":"shirt","def":"a top you wear on your body","hint":"\"In summer we wear shorts and a <b>shirt</b>.\""},
   {"word":"dress","def":"a one-piece piece of clothing","hint":"\"like a party <b>dress</b>.\""},
   {"word":"style","def":"the way you like to dress","hint":"\"part of your <b>style</b>.\""}
 ],
 "bank":["clothes","coat","shirt","dress","style","hat"],
 "fills":[
   {"text":"We wear ___ to stay warm or cool.","a":"clothes"},
   {"text":"In winter I put on a warm ___.","a":"coat"},
   {"text":"I wear a ___ on the top of my body.","a":"shirt"},
   {"text":"She wore a pretty ___ to the party.","a":"dress"},
   {"text":"The way you like to dress is your ___.","a":"style"},
   {"text":"I put a ___ on my head to keep off the sun.","a":"hat"}
 ]
},

{"activityId":"volcano","projectKey":"volcano","title":"Volcanoes","heroEmoji":"🌋","watermark":"🌋","pageTitle":"Volcanoes","diagramFile":"diagrams/volcano.svg",
 "win":"PERFECT, Amara! Red hot! 🌋","cheer":"Your reading is on fire! 🌋",
 "palette":{"primary":"#e8590c","dark":"#b8460a","deep":"#7d2f06","accent":"#f4a06a","accentSoft":"#fde4d4","cream":"#fff7f1","bgTop":"#fdf1e9","bgBottom":"#f8e6d8","glow1":"#e8590c22","glow2":"#7d2f0618"},
 "passageTitle":"Volcanoes",
 "passageHtml":"<p>Deep beneath the Earth's surface, it is so hot that rock melts into a thick, glowing liquid called <span class=\"voc\">magma</span>. A volcano is an opening in the ground where this melted rock can reach the surface. When pressure builds up, a volcano can <span class=\"voc\">erupt</span>, sending magma, gas, and <span class=\"voc\">ash</span> bursting out. Once the magma flows onto the surface it is called <span class=\"voc\">lava</span>. Lava is <span class=\"voc\">molten</span>, which means melted by heat, and it can be hotter than 1,000 degrees. As the lava cools, it hardens into new rock.</p><p>Most volcanoes have a bowl-shaped opening at the top called a <span class=\"voc\">crater</span>, and the channel that magma travels up is called a <span class=\"voc\">vent</span>. Not all volcanoes erupt often. A volcano that has not erupted for a long time but still could is called <span class=\"voc\">dormant</span>, like a sleeping giant. Volcanoes can be dangerous, but they also build new islands and rich soil. Over millions of years, they have helped shape the surface of our planet.</p>",
 "questions":[{"type":"Main idea","q":"What is this passage mostly about?","opts":["How to climb a mountain","How volcanoes work and what they do","Why rocks are grey"],"a":1},{"type":"Detail","q":"Melted rock below the ground is called —","opts":["magma","lava","ash"],"a":0},{"type":"Vocabulary","q":"\"Molten\" means —","opts":["frozen solid","melted by heat","very loud"],"a":1},{"type":"Detail","q":"The bowl-shaped opening at the top is the —","opts":["vent","crater","island"],"a":1},{"type":"Cause & effect","q":"A volcano erupts when —","opts":["it rains","pressure builds up inside","the lava cools"],"a":1},{"type":"Inference","q":"A \"dormant\" volcano is best described as —","opts":["one that can never erupt","a sleeping giant that could erupt again","an underwater cave"],"a":1}],
 "match":[{"word":"magma","def":"melted rock below the ground","hint":"\"…rock melts into a thick, glowing liquid called <b>magma</b>.\""},{"word":"lava","def":"melted rock that has reached the surface","hint":"\"Once the magma flows onto the surface it is called <b>lava</b>.\""},{"word":"crater","def":"the bowl-shaped opening at a volcano's top","hint":"\"…a bowl-shaped opening at the top called a <b>crater</b>.\""},{"word":"molten","def":"melted by great heat","hint":"\"Lava is <b>molten</b>, which means melted by heat…\""},{"word":"vent","def":"the channel magma travels up through","hint":"\"…the channel that magma travels up is called a <b>vent</b>.\""},{"word":"dormant","def":"not erupting now but able to erupt again","hint":"\"…still could is called <b>dormant</b>, like a sleeping giant.\""}],
 "bank":["magma","lava","erupt","crater","molten","vent","dormant","ash"],
 "fills":[{"text":"Hot melted rock under the ground is called ___.","a":"magma"},{"text":"When a volcano ___s, gas and ash burst out.","a":"erupt"},{"text":"Glowing ___ flowed down the mountain and cooled into rock.","a":"lava"},{"text":"The metal was so hot it turned ___.","a":"molten"},{"text":"Smoke poured from the ___ at the top of the volcano.","a":"crater"},{"text":"Magma rises through a ___ to reach the surface.","a":"vent"},{"text":"The ___ volcano had been quiet for hundreds of years.","a":"dormant"},{"text":"After the campfire, grey ___ was left in the pit.","a":"ash","challenge":True}]},

{"activityId":"egypt","projectKey":"egypt","title":"Ancient Egypt","heroEmoji":"🏺","watermark":"🔺","pageTitle":"Ancient Egypt","diagramFile":"diagrams/egypt.svg",
 "win":"PERFECT, Amara! Like a pharaoh! 👑","cheer":"A true explorer of the past! 🏺",
 "palette":{"primary":"#c79a2b","dark":"#9c7820","deep":"#6b5012","accent":"#e0c069","accentSoft":"#f7eecf","cream":"#fffbf0","bgTop":"#faf3e0","bgBottom":"#f3ead2","glow1":"#c79a2b22","glow2":"#6b501218"},
 "passageTitle":"Life in Ancient Egypt",
 "passageHtml":"<p>Thousands of years ago, a great civilization grew along the <span class=\"voc\">Nile</span> River in Egypt. The ruler of ancient Egypt was called a <span class=\"voc\">pharaoh</span>, who was treated like a god. The Egyptians built giant stone <span class=\"voc\">pyramid</span>s as resting places for their pharaohs. They wrote using picture symbols called <span class=\"voc\">hieroglyph</span>s, often on a paper made from reeds called <span class=\"voc\">papyrus</span>.</p><p>The Egyptians believed in an <span class=\"voc\">afterlife</span>, a life that continues after death. To prepare a body for it, they preserved it as a <span class=\"voc\">mummy</span>, wrapping it carefully in cloth. A pharaoh was buried in a <span class=\"voc\">tomb</span> filled with treasure and everyday objects to use in the next life. Much of what we know about ancient Egypt comes from these tombs, which have lasted for thousands of years.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to build a boat","the life and beliefs of ancient Egypt","the weather in Africa"],"a":1},{"type":"Detail","q":"The ruler of ancient Egypt was a —","opts":["pharaoh","mummy","farmer"],"a":0},{"type":"Vocabulary","q":"\"Hieroglyphs\" were —","opts":["stone boats","picture symbols used for writing","river fish"],"a":1},{"type":"Detail","q":"The Egyptians wrote on paper made from —","opts":["wood","reeds called papyrus","animal skin"],"a":1},{"type":"Cause & effect","q":"Egyptians made mummies because they believed in —","opts":["an afterlife","flying","rain"],"a":0},{"type":"Inference","q":"We know so much about ancient Egypt mainly because —","opts":["tombs and their objects survived","they used computers","nothing was ever buried"],"a":0}],
 "match":[{"word":"pharaoh","def":"the god-like ruler of ancient Egypt","hint":"\"The ruler of ancient Egypt was called a <b>pharaoh</b>…\""},{"word":"pyramid","def":"a giant stone resting place for a pharaoh","hint":"\"…built giant stone <b>pyramid</b>s as resting places…\""},{"word":"hieroglyph","def":"a picture symbol used for writing","hint":"\"…picture symbols called <b>hieroglyph</b>s…\""},{"word":"mummy","def":"a body preserved and wrapped in cloth","hint":"\"…they preserved it as a <b>mummy</b>, wrapping it in cloth.\""},{"word":"papyrus","def":"paper made from reeds","hint":"\"…a paper made from reeds called <b>papyrus</b>.\""},{"word":"afterlife","def":"a life believed to continue after death","hint":"\"The Egyptians believed in an <b>afterlife</b>…\""}],
 "bank":["pharaoh","pyramid","hieroglyph","mummy","Nile","tomb","papyrus","afterlife"],
 "fills":[{"text":"The ___ ruled Egypt like a living god.","a":"pharaoh"},{"text":"The huge ___ was built from millions of stone blocks.","a":"pyramid"},{"text":"Each tiny ___ stood for a sound or an idea.","a":"hieroglyph"},{"text":"The dry desert helped turn the body into a ___.","a":"mummy"},{"text":"Egypt grew crops along the ___ River.","a":"Nile"},{"text":"The king was buried in a hidden ___.","a":"tomb"},{"text":"They wrote letters on smooth sheets of ___.","a":"papyrus"},{"text":"Many cultures tell stories about an ___ after we die.","a":"afterlife","challenge":True}]},

{"activityId":"watercycle","projectKey":"watercycle","title":"The Water Cycle","heroEmoji":"💧","watermark":"🌧️","pageTitle":"The Water Cycle","diagramFile":"diagrams/watercycle.svg",
 "win":"PERFECT, Amara! You're flowing! 💧","cheer":"Brilliant, rain or shine! 🌧️",
 "palette":{"primary":"#2563eb","dark":"#1d4fc0","deep":"#143285","accent":"#7aa0f0","accentSoft":"#e1e9fc","cream":"#f5f8ff","bgTop":"#eef3fd","bgBottom":"#e3ecf8","glow1":"#2563eb22","glow2":"#14328518"},
 "passageTitle":"The Water Cycle",
 "passageHtml":"<p>Water on Earth is always moving in a never-ending journey called the water <span class=\"voc\">cycle</span>. It begins when the sun heats water in oceans, lakes, and rivers. The warm water <span class=\"voc\">evaporate</span>s, turning into a gas called water <span class=\"voc\">vapor</span> that rises into the sky.</p><p>High in the sky the air is cold, so the vapor begins to <span class=\"voc\">condense</span>, changing back into tiny <span class=\"voc\">droplet</span>s of liquid water. Millions of these droplets gather to form a <span class=\"voc\">cloud</span>. When the droplets grow heavy enough, they fall as <span class=\"voc\">precipitation</span> — rain, snow, or hail. The water lands on the ground, where rivers <span class=\"voc\">collect</span> it and carry it back to the sea, and the whole cycle starts again.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to swim","how water moves around the Earth","why the sky is blue"],"a":1},{"type":"Detail","q":"The sun causes water to —","opts":["freeze","evaporate into vapor","disappear forever"],"a":1},{"type":"Vocabulary","q":"\"Condense\" means —","opts":["turn from gas back into liquid","heat up","fall as rain"],"a":0},{"type":"Detail","q":"Rain, snow, and hail are all kinds of —","opts":["clouds","precipitation","vapor"],"a":1},{"type":"Cause & effect","q":"Droplets fall from a cloud when they —","opts":["get too heavy","turn into gas","freeze the sun"],"a":0},{"type":"Inference","q":"The water cycle is called \"never-ending\" because —","opts":["it repeats again and again","it happens only once","water is destroyed"],"a":0}],
 "match":[{"word":"evaporate","def":"to turn from a liquid into a gas","hint":"\"The warm water <b>evaporate</b>s…\""},{"word":"vapor","def":"water in the form of a gas","hint":"\"…a gas called water <b>vapor</b>…\""},{"word":"condense","def":"to turn from a gas back into a liquid","hint":"\"…the vapor begins to <b>condense</b>…\""},{"word":"precipitation","def":"water falling as rain, snow, or hail","hint":"\"…they fall as <b>precipitation</b> — rain, snow, or hail.\""},{"word":"collect","def":"to gather together","hint":"\"…rivers <b>collect</b> it and carry it back to the sea.\""},{"word":"cycle","def":"something that repeats again and again","hint":"\"…a never-ending journey called the water <b>cycle</b>.\""}],
 "bank":["evaporate","vapor","condense","cloud","precipitation","collect","cycle","droplet"],
 "fills":[{"text":"The sun makes puddles ___ into the air.","a":"evaporate"},{"text":"Warm water turns into invisible water ___.","a":"vapor"},{"text":"In the cold sky, vapor will ___ into drops.","a":"condense"},{"text":"A white fluffy ___ floated across the sky.","a":"cloud"},{"text":"Rain and snow are types of ___.","a":"precipitation"},{"text":"A bucket can ___ rain that falls from the roof.","a":"collect"},{"text":"Tiny ___s of water clung to the cold glass.","a":"droplet"},{"text":"The seasons follow a ___ that repeats every year.","a":"cycle","challenge":True}]},

{"activityId":"solar","projectKey":"solar","title":"The Solar System","heroEmoji":"🪐","watermark":"⭐","pageTitle":"The Solar System","diagramFile":"diagrams/solar.svg",
 "win":"PERFECT, Amara! Out of this world! 🪐","cheer":"You're a star, Amara! ⭐",
 "palette":{"primary":"#312e81","dark":"#26235f","deep":"#161440","accent":"#7c79c8","accentSoft":"#e4e3f4","cream":"#f6f6fc","bgTop":"#eeedf8","bgBottom":"#e3e2f2","glow1":"#312e8122","glow2":"#16144018"},
 "passageTitle":"Our Solar System",
 "passageHtml":"<p>Our solar system is made up of the Sun and everything that travels around it. The Sun is a giant <span class=\"voc\">star</span>, a huge ball of burning gas. Eight <span class=\"voc\">planet</span>s move around the Sun, each following a curved path called an <span class=\"voc\">orbit</span>. What keeps the planets from flying off into space is <span class=\"voc\">gravity</span>, an invisible force that pulls objects toward one another. The Sun's strong gravity holds the whole solar system together.</p><p>Between the planets float chunks of rock called <span class=\"voc\">asteroid</span>s, and far beyond our solar system lie billions of other stars that make up our <span class=\"voc\">galaxy</span>, the Milky Way. As each planet orbits the Sun, it also spins around an imaginary line through its middle called an <span class=\"voc\">axis</span>; this spinning is what gives us day and night. Scientists study all of this using a <span class=\"voc\">telescope</span>, a tool that makes faraway objects look closer.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fly a plane","what the solar system is made of","why the Sun is yellow"],"a":1},{"type":"Detail","q":"The Sun is a —","opts":["planet","star","moon"],"a":1},{"type":"Vocabulary","q":"An \"orbit\" is —","opts":["a kind of rock","the curved path a planet travels","a telescope"],"a":1},{"type":"Detail","q":"What holds the solar system together?","opts":["gravity","wind","ice"],"a":0},{"type":"Cause & effect","q":"A planet spinning on its axis gives us —","opts":["day and night","summer only","asteroids"],"a":0},{"type":"Inference","q":"A telescope is useful because it —","opts":["makes faraway things look closer","heats the Sun","creates gravity"],"a":0}],
 "match":[{"word":"orbit","def":"the curved path an object travels around another","hint":"\"…a curved path called an <b>orbit</b>.\""},{"word":"gravity","def":"a force that pulls objects toward each other","hint":"\"…<b>gravity</b>, an invisible force that pulls objects together.\""},{"word":"asteroid","def":"a chunk of rock in space","hint":"\"…chunks of rock called <b>asteroid</b>s…\""},{"word":"axis","def":"an imaginary line an object spins around","hint":"\"…an imaginary line through its middle called an <b>axis</b>.\""},{"word":"galaxy","def":"a huge group of stars","hint":"\"…make up our <b>galaxy</b>, the Milky Way.\""},{"word":"telescope","def":"a tool that makes faraway objects look closer","hint":"\"…using a <b>telescope</b>, a tool that makes faraway objects look closer.\""}],
 "bank":["orbit","planet","gravity","star","asteroid","axis","galaxy","telescope"],
 "fills":[{"text":"Earth follows its ___ around the Sun.","a":"orbit"},{"text":"Mars is a rocky ___ near Earth.","a":"planet"},{"text":"When you jump up, ___ always pulls you back down.","a":"gravity","challenge":True},{"text":"The Sun is the closest ___ to Earth.","a":"star"},{"text":"A small ___ zoomed past, made of rock and metal.","a":"asteroid"},{"text":"The Earth spins on its ___ once a day.","a":"axis"},{"text":"Our Sun is one of billions of stars in the ___.","a":"galaxy"},{"text":"She looked through the ___ to see Saturn's rings.","a":"telescope"}]},

{"activityId":"heart","projectKey":"heart","title":"The Human Heart","heroEmoji":"❤️","watermark":"🫀","pageTitle":"The Human Heart","diagramFile":"diagrams/heart.svg",
 "win":"PERFECT, Amara! You've got heart! ❤️","cheer":"That answer was a heartbeat away from perfect! ❤️",
 "palette":{"primary":"#d6336c","dark":"#ab2856","deep":"#741a3a","accent":"#ec8ab0","accentSoft":"#fbe2ec","cream":"#fff6f9","bgTop":"#fceef3","bgBottom":"#f7e2ea","glow1":"#d6336c22","glow2":"#741a3a18"},
 "passageTitle":"Your Amazing Heart",
 "passageHtml":"<p>Your heart is one of the hardest-working <span class=\"voc\">muscle</span>s in your body. About the size of your fist, it sits in the middle of your chest and never stops working. The heart's job is to <span class=\"voc\">pump</span> <span class=\"voc\">blood</span> to every part of your body. Blood carries <span class=\"voc\">oxygen</span>, the gas your body needs to stay alive, from your lungs to your muscles and organs.</p><p>Blood travels through a network of tubes called <span class=\"voc\">vessel</span>s, which reach every corner of your body. The heart pushes blood out, the body uses the oxygen, and the blood returns to be filled again — this loop is how blood <span class=\"voc\">circulate</span>s. Tiny doors inside the heart called <span class=\"voc\">valve</span>s open and close to keep the blood flowing the right way. You can feel each beat as a <span class=\"voc\">pulse</span> in your wrist or neck.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to run fast","what the heart does","why blood is red"],"a":1},{"type":"Detail","q":"The heart is about the size of your —","opts":["fist","foot","head"],"a":0},{"type":"Vocabulary","q":"\"Vessels\" are —","opts":["bones","tubes that carry blood","lungs"],"a":1},{"type":"Detail","q":"Blood carries ___ to the body.","opts":["oxygen","sugar only","air bubbles"],"a":0},{"type":"Cause & effect","q":"Valves open and close to —","opts":["keep blood flowing the right way","make a pulse stop","cool the body"],"a":0},{"type":"Inference","q":"You can feel your pulse because —","opts":["the heart beats and pushes blood","your bones move","you are breathing out"],"a":0}],
 "match":[{"word":"pump","def":"to push a liquid along","hint":"\"The heart's job is to <b>pump</b> blood…\""},{"word":"vessel","def":"a tube that carries blood","hint":"\"…a network of tubes called <b>vessel</b>s…\""},{"word":"oxygen","def":"the gas the body needs to live","hint":"\"Blood carries <b>oxygen</b>, the gas your body needs…\""},{"word":"circulate","def":"to move around in a loop","hint":"\"…this loop is how blood <b>circulate</b>s.\""},{"word":"muscle","def":"a body part that moves by squeezing","hint":"\"…one of the hardest-working <b>muscle</b>s in your body.\""},{"word":"valve","def":"a small door that controls flow","hint":"\"Tiny doors inside the heart called <b>valve</b>s…\""}],
 "bank":["pump","blood","vessel","oxygen","pulse","circulate","muscle","valve"],
 "fills":[{"text":"The heart works to ___ blood all day.","a":"pump"},{"text":"Red ___ flows through your whole body.","a":"blood"},{"text":"Blood moves through tubes called ___s.","a":"vessel"},{"text":"We breathe in ___ from the air.","a":"oxygen"},{"text":"Warm air and water ___ around the Earth, too.","a":"circulate","challenge":True},{"text":"You use a ___ to bend your arm.","a":"muscle"},{"text":"A ___ keeps the blood from flowing backward.","a":"valve"},{"text":"I felt my ___ speed up after running.","a":"pulse"}]},

{"activityId":"sharks","projectKey":"sharks","title":"Sharks","heroEmoji":"🦈","watermark":"🦈","pageTitle":"Sharks","diagramFile":"diagrams/sharks.svg",
 "win":"PERFECT, Amara! Jaw-some! 🦈","cheer":"You swam through that, Amara! 🌊",
 "palette":{"primary":"#51688a","dark":"#3e5170","deep":"#28354b","accent":"#8fa1bd","accentSoft":"#e4e9f0","cream":"#f5f8fb","bgTop":"#eef3f8","bgBottom":"#e3ebf2","glow1":"#51688a22","glow2":"#28354b18"},
 "passageTitle":"All About Sharks",
 "passageHtml":"<p>Sharks are powerful fish that have lived in the oceans for millions of years. Unlike most fish, a shark's skeleton is not made of bone but of <span class=\"voc\">cartilage</span>, the same bendy material in your ears and nose. This makes sharks light and fast. They breathe through slits called <span class=\"voc\">gill</span>s that take in oxygen from the water, and they steer using their <span class=\"voc\">fin</span>s.</p><p>Most sharks are <span class=\"voc\">predator</span>s, animals that hunt other animals for food. A shark has an amazing <span class=\"voc\">sense</span> of smell and can detect a tiny amount of blood from far away. There are more than 500 kinds, or <span class=\"voc\">species</span>, of shark, from the tiny dwarf shark to the giant whale shark. Even though sharks have rows of sharp teeth in their strong <span class=\"voc\">jaw</span>s, very few species are dangerous to people.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fish","what sharks are like and how they live","why the sea is salty"],"a":1},{"type":"Detail","q":"A shark's skeleton is made of —","opts":["bone","cartilage","metal"],"a":1},{"type":"Vocabulary","q":"A \"predator\" is —","opts":["an animal that hunts others","a kind of plant","a baby fish"],"a":0},{"type":"Detail","q":"Sharks breathe using their —","opts":["fins","gills","tails"],"a":1},{"type":"Cause & effect","q":"A shark can find faraway prey because of its —","opts":["strong sense of smell","loud voice","bright color"],"a":0},{"type":"Inference","q":"The passage suggests most sharks are —","opts":["not dangerous to people","friendly pets","unable to swim"],"a":0}],
 "match":[{"word":"predator","def":"an animal that hunts others for food","hint":"\"Most sharks are <b>predator</b>s…\""},{"word":"gill","def":"a slit a fish breathes through","hint":"\"They breathe through slits called <b>gill</b>s…\""},{"word":"cartilage","def":"a bendy material that is not bone","hint":"\"…made of <b>cartilage</b>, the same bendy material in your ears…\""},{"word":"fin","def":"a body part a fish uses to steer","hint":"\"…they steer using their <b>fin</b>s.\""},{"word":"sense","def":"a way of feeling the world, like smell","hint":"\"A shark has an amazing <b>sense</b> of smell…\""},{"word":"species","def":"a particular kind of animal","hint":"\"…more than 500 kinds, or <b>species</b>, of shark…\""}],
 "bank":["predator","gill","cartilage","fin","prey","sense","species","jaw"],
 "fills":[{"text":"A lion is a ___ that hunts other animals.","a":"predator"},{"text":"Fish breathe through their ___s.","a":"gill"},{"text":"Your nose is made of bendy ___.","a":"cartilage"},{"text":"A shark steers with its ___s.","a":"fin"},{"text":"The deer was the ___ that the wolf chased.","a":"prey"},{"text":"A sharp ___ of hearing helps an owl hunt at night.","a":"sense"},{"text":"There are many ___ of dog, like poodles and pugs.","a":"species","challenge":True},{"text":"The shark opened its huge ___.","a":"jaw"}]},

{"activityId":"olympics","projectKey":"olympics","title":"The Olympic Games","heroEmoji":"🏅","watermark":"🔥","pageTitle":"The Olympic Games","diagramFile":"diagrams/olympics.svg",
 "win":"PERFECT, Amara! Gold medal! 🥇","cheer":"A champion reader! 🏅",
 "palette":{"primary":"#c92a2a","dark":"#a01f1f","deep":"#6e1414","accent":"#e87f7f","accentSoft":"#fbe1e1","cream":"#fff6f6","bgTop":"#fceeee","bgBottom":"#f7e2e2","glow1":"#c92a2a22","glow2":"#6e141418"},
 "passageTitle":"The Olympic Games",
 "passageHtml":"<p>The Olympic Games are one of the world's biggest sporting events, where <span class=\"voc\">athlete</span>s from many countries <span class=\"voc\">compete</span> against one another. The Games began in <span class=\"voc\">ancient</span> Greece almost 3,000 years ago, held in honor of the Greek gods. Back then, winners were given a crown of olive leaves. The ancient Games ended long ago, but in 1896 they were brought back to life as the modern Olympics.</p><p>Today the Games are held every four years, and a different city gets to <span class=\"voc\">host</span> them each time. Winning athletes receive a gold, silver, or bronze <span class=\"voc\">medal</span>, and a <span class=\"voc\">champion</span> is celebrated around the world. The Games open with a grand <span class=\"voc\">ceremony</span> and the lighting of the Olympic <span class=\"voc\">torch</span>, a flame carried all the way from Greece. The Olympics bring people from different nations together in friendship and sport.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to ride a bike","the history and meaning of the Olympic Games","Greek food"],"a":1},{"type":"Detail","q":"The Olympic Games began in —","opts":["ancient Greece","modern America","ancient Egypt"],"a":0},{"type":"Vocabulary","q":"To \"compete\" means —","opts":["to give up","to try to win against others","to watch"],"a":1},{"type":"Detail","q":"How often are the modern Games held?","opts":["every year","every four years","every month"],"a":1},{"type":"Detail","q":"A winning athlete receives a —","opts":["medal","car","crown of gold"],"a":0},{"type":"Inference","q":"The passage suggests the Olympics help to —","opts":["bring nations together","start wars","end all sports"],"a":0}],
 "match":[{"word":"athlete","def":"a person trained in a sport","hint":"\"…<b>athlete</b>s from many countries compete…\""},{"word":"compete","def":"to try to win against others","hint":"\"…<b>compete</b> against one another.\""},{"word":"ancient","def":"very old, from long ago","hint":"\"The Games began in <b>ancient</b> Greece…\""},{"word":"ceremony","def":"a special event with traditions","hint":"\"The Games open with a grand <b>ceremony</b>…\""},{"word":"host","def":"to hold an event for others","hint":"\"…a different city gets to <b>host</b> them…\""},{"word":"champion","def":"a winner who is the best","hint":"\"…a <b>champion</b> is celebrated around the world.\""}],
 "bank":["athlete","compete","ancient","medal","ceremony","host","torch","champion"],
 "fills":[{"text":"The fast runner was a famous ___.","a":"athlete"},{"text":"Teams ___ to see who is fastest.","a":"compete"},{"text":"The pyramids are part of ___ history.","a":"ancient"},{"text":"The winner proudly wore a gold ___.","a":"medal"},{"text":"Our town will ___ a big music festival next year.","a":"host","challenge":True},{"text":"The runner carried the flaming ___.","a":"torch"},{"text":"The opening ___ had music and flags.","a":"ceremony"},{"text":"She became the world ___ in swimming.","a":"champion"}]},

{"activityId":"money","projectKey":"money","title":"How Money Works","heroEmoji":"💰","watermark":"🪙","pageTitle":"How Money Works","diagramFile":"diagrams/money.svg",
 "win":"PERFECT, Amara! Money smart! 💰","cheer":"You earned every point! 🪙",
 "palette":{"primary":"#2f9e44","dark":"#247a35","deep":"#175223","accent":"#74c686","accentSoft":"#dcf2e1","cream":"#f4fbf6","bgTop":"#ebf7ee","bgBottom":"#e0f0e4","glow1":"#2f9e4422","glow2":"#17522318"},
 "passageTitle":"How Money Works",
 "passageHtml":"<p>Long ago, before money existed, people got what they needed by <span class=\"voc\">barter</span>, which means trading one thing directly for another. A farmer might <span class=\"voc\">trade</span> a basket of eggs for a pair of shoes. But bartering was tricky — what if the shoemaker did not want eggs? To make trading easier, people invented money, a special kind of <span class=\"voc\">currency</span> that everyone agrees has <span class=\"voc\">value</span>.</p><p>Today, people <span class=\"voc\">earn</span> money by working, and they spend it to buy <span class=\"voc\">goods</span> and services they need. Because money is limited, it is smart to make a <span class=\"voc\">budget</span>, a plan for how much to spend and how much to <span class=\"voc\">save</span>. Saving money now means you can buy something bigger later, or be ready if an emergency comes. Understanding money helps people make good choices.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to bake bread","what money is and why people use it","how shoes are made"],"a":1},{"type":"Detail","q":"Before money, people traded by —","opts":["bartering","using cards","printing bills"],"a":0},{"type":"Vocabulary","q":"\"Currency\" means —","opts":["a kind of food","money that people use","a job"],"a":1},{"type":"Detail","q":"People earn money by —","opts":["sleeping","working","bartering only"],"a":1},{"type":"Cause & effect","q":"A budget helps because money is —","opts":["free","limited","heavy"],"a":1},{"type":"Inference","q":"Saving money is smart because it —","opts":["lets you buy bigger things later or handle emergencies","makes money disappear","is against the rules"],"a":0}],
 "match":[{"word":"trade","def":"to give one thing to get another","hint":"\"A farmer might <b>trade</b> a basket of eggs for shoes.\""},{"word":"currency","def":"money that people use","hint":"\"…a special kind of <b>currency</b>…\""},{"word":"barter","def":"trading goods directly without money","hint":"\"…by <b>barter</b>, which means trading one thing for another.\""},{"word":"value","def":"how much something is worth","hint":"\"…everyone agrees has <b>value</b>.\""},{"word":"earn","def":"to get money by working","hint":"\"…people <b>earn</b> money by working…\""},{"word":"budget","def":"a plan for spending and saving","hint":"\"…it is smart to make a <b>budget</b>…\""}],
 "bank":["trade","currency","barter","value","earn","budget","save","goods"],
 "fills":[{"text":"The dollar is the ___ used in the United States.","a":"currency"},{"text":"People with no money would ___ chickens for corn.","a":"barter"},{"text":"You ___ money by doing a job.","a":"earn"},{"text":"A wise family makes a ___ each month.","a":"budget"},{"text":"I will ___ my coins to buy a new bike.","a":"save"},{"text":"Stores sell ___ like food and clothes.","a":"goods"},{"text":"Two kids might ___ stickers at school.","a":"trade"},{"text":"A rare card can have a high ___ to collectors.","a":"value","challenge":True}]},

{"activityId":"storms","projectKey":"storms","title":"Thunderstorms","heroEmoji":"⛈️","watermark":"⚡","pageTitle":"Thunderstorms","diagramFile":"diagrams/storms.svg",
 "win":"PERFECT, Amara! Electric! ⚡","cheer":"You brightened the sky! ⛈️",
 "palette":{"primary":"#364fc7","dark":"#2a3e9c","deep":"#1a2766","accent":"#7c8de0","accentSoft":"#e2e6f8","cream":"#f5f6fd","bgTop":"#eef0fb","bgBottom":"#e3e7f6","glow1":"#364fc722","glow2":"#1a276618"},
 "passageTitle":"Thunderstorms",
 "passageHtml":"<p>A thunderstorm is a powerful weather event filled with <span class=\"voc\">lightning</span>, <span class=\"voc\">thunder</span>, heavy rain, and strong wind. Storms often form on warm, <span class=\"voc\">humid</span> days, when the air is full of moisture. Warm air rises quickly and builds tall storm clouds. Inside these clouds, ice and water bump together and create a build-up of <span class=\"voc\">electricity</span>.</p><p>When that electricity jumps through the <span class=\"voc\">atmosphere</span> — the layer of air around the Earth — we see a flash of lightning. Lightning heats the air so fast that it makes a loud bang we call thunder. Storms can bring sudden <span class=\"voc\">gust</span>s of wind that bend the trees. Weather scientists watch the sky and give a <span class=\"voc\">forecast</span> so people know a storm is coming and can take <span class=\"voc\">shelter</span> somewhere safe.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fly a kite","what thunderstorms are and how they form","why grass is green"],"a":1},{"type":"Detail","q":"Thunderstorms often form on days that are —","opts":["cold and dry","warm and humid","snowy"],"a":1},{"type":"Vocabulary","q":"The \"atmosphere\" is —","opts":["a storm cloud","the layer of air around Earth","a flash of light"],"a":1},{"type":"Cause & effect","q":"Thunder happens because lightning —","opts":["heats the air very fast","cools the rain","blocks the Sun"],"a":0},{"type":"Detail","q":"A forecast tells people —","opts":["a storm is coming","how to swim","the time of day only"],"a":0},{"type":"Inference","q":"People take shelter during a storm to —","opts":["stay safe","see more lightning","make thunder"],"a":0}],
 "match":[{"word":"lightning","def":"a flash of electricity in the sky","hint":"\"…filled with <b>lightning</b>, thunder, heavy rain…\""},{"word":"atmosphere","def":"the layer of air around the Earth","hint":"\"…the <b>atmosphere</b> — the layer of air around the Earth…\""},{"word":"electricity","def":"a form of energy that can flow or flash","hint":"\"…create a build-up of <b>electricity</b>.\""},{"word":"humid","def":"having a lot of moisture in the air","hint":"\"Storms often form on warm, <b>humid</b> days…\""},{"word":"gust","def":"a sudden rush of wind","hint":"\"Storms can bring sudden <b>gust</b>s of wind…\""},{"word":"forecast","def":"a guess about what the weather will do","hint":"\"…scientists…give a <b>forecast</b>…\""}],
 "bank":["thunder","lightning","atmosphere","electricity","humid","gust","forecast","shelter"],
 "fills":[{"text":"A bright bolt of ___ lit up the sky.","a":"lightning"},{"text":"We heard a loud crack of ___.","a":"thunder"},{"text":"The air felt sticky and ___ before the rain.","a":"humid"},{"text":"A strong ___ of wind blew my hat away.","a":"gust"},{"text":"The weather ___ said it would rain at noon.","a":"forecast"},{"text":"We ran inside to take ___ from the storm.","a":"shelter"},{"text":"A lamp and a TV both run on ___.","a":"electricity","challenge":True},{"text":"Birds fly high up in the ___.","a":"atmosphere"}]},

{"activityId":"castles","projectKey":"castles","title":"Castles and Knights","heroEmoji":"🏰","watermark":"⚔️","pageTitle":"Castles and Knights","diagramFile":"diagrams/castles.svg",
 "win":"PERFECT, Amara! A noble win! 🏰","cheer":"You defended every answer! ⚔️",
 "palette":{"primary":"#6c757d","dark":"#545b61","deep":"#373b40","accent":"#a3abb2","accentSoft":"#e6e9eb","cream":"#f7f8f9","bgTop":"#eff1f2","bgBottom":"#e5e8ea","glow1":"#6c757d22","glow2":"#373b4018"},
 "passageTitle":"Castles and Knights",
 "passageHtml":"<p>In the Middle Ages, powerful lords built castles to protect their land and people. A castle was a strong stone <span class=\"voc\">fortress</span> designed to be hard to attack. Many castles were surrounded by a <span class=\"voc\">moat</span>, a deep ditch filled with water. To cross it, visitors used a <span class=\"voc\">drawbridge</span> that could be raised to lock enemies out. Thick walls and tall towers helped the people inside <span class=\"voc\">defend</span> themselves.</p><p>Castles were home to <span class=\"voc\">noble</span>s — important, wealthy families — and the soldiers who served them. The most famous of these soldiers were <span class=\"voc\">knight</span>s, warriors who fought on horseback wearing metal <span class=\"voc\">armor</span> to protect their bodies. Sometimes an enemy army would surround a castle and try to break in, an attack called a <span class=\"voc\">siege</span>. A castle's clever design could keep its people safe for months.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to ride a horse","how castles protected people in the Middle Ages","what knights ate"],"a":1},{"type":"Detail","q":"A moat is a —","opts":["tall tower","deep ditch filled with water","metal suit"],"a":1},{"type":"Vocabulary","q":"A \"fortress\" is —","opts":["a strong building made for defense","a horse","a king's crown"],"a":0},{"type":"Detail","q":"Knights protected their bodies with —","opts":["armor","blankets","paper"],"a":0},{"type":"Cause & effect","q":"A drawbridge could be raised in order to —","opts":["lock enemies out","let in more water","feed the horses"],"a":0},{"type":"Inference","q":"A \"siege\" suggests the castle was —","opts":["under attack","having a party","being built"],"a":0}],
 "match":[{"word":"fortress","def":"a strong building made for defense","hint":"\"…a strong stone <b>fortress</b> designed to be hard to attack.\""},{"word":"moat","def":"a deep, water-filled ditch around a castle","hint":"\"…a <b>moat</b>, a deep ditch filled with water.\""},{"word":"drawbridge","def":"a bridge that can be raised and lowered","hint":"\"…a <b>drawbridge</b> that could be raised…\""},{"word":"armor","def":"a metal suit that protects the body","hint":"\"…wearing metal <b>armor</b> to protect their bodies.\""},{"word":"siege","def":"an attack that surrounds a place","hint":"\"…an attack called a <b>siege</b>.\""},{"word":"noble","def":"an important, wealthy person","hint":"\"Castles were home to <b>noble</b>s…\""}],
 "bank":["fortress","moat","drawbridge","knight","armor","siege","noble","defend"],
 "fills":[{"text":"The castle was a stone ___ on a hill.","a":"fortress"},{"text":"Water filled the ___ around the walls.","a":"moat"},{"text":"They lowered the ___ to let the cart cross.","a":"drawbridge"},{"text":"The brave ___ rode a horse into battle.","a":"knight"},{"text":"His shiny ___ protected him from swords.","a":"armor"},{"text":"The army began a ___ around the city.","a":"siege"},{"text":"A wealthy ___ owned the land and the farms.","a":"noble"},{"text":"Our soccer team must ___ its goal in the game.","a":"defend","challenge":True}]},

{"activityId":"cats","projectKey":"cats","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"All About Cats","heroEmoji":"🐱","watermark":"🐾","pageTitle":"Cats","diagramFile":"diagrams/cats.svg",
 "win":"PERFECT, Dani! Purr-fect! 🐱","cheer":"The kittens love you, Dani! 🐾",
 "palette":{"primary":"#9b6cd6","dark":"#7a52ad","deep":"#523372","accent":"#c2a0e6","accentSoft":"#efe6f8","cream":"#fbf8fe","bgTop":"#f4ecfb","bgBottom":"#ece0f5","glow1":"#9b6cd622","glow2":"#52337218"},
 "passageTitle":"All About Cats",
 "passageHtml":"<p>A cat is a soft, furry pet. Cats have long <span class=\"voc\">whiskers</span> on their face. They walk on four soft <span class=\"voc\">paws</span>. When a cat is happy, it will <span class=\"voc\">purr</span>.</p><p>A baby cat is called a <span class=\"voc\">kitten</span>. Cats have sharp <span class=\"voc\">claws</span> to climb and play. They like to <span class=\"voc\">pounce</span> on toys. Cats are fun and cuddly pets.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["dogs","cats","birds"],"a":1},{"type":"Detail","q":"A baby cat is a —","opts":["kitten","puppy","chick"],"a":0},{"type":"Detail","q":"A happy cat will —","opts":["bark","purr","swim"],"a":1},{"type":"Detail","q":"Cats walk on —","opts":["two feet","four paws","wheels"],"a":1},{"type":"Vocabulary","q":"\"Pounce\" means —","opts":["to jump on something","to sleep","to eat"],"a":0}],
 "match":[{"word":"whiskers","def":"long hairs on a cat's face","hint":"\"Cats have long <b>whiskers</b> on their face.\""},{"word":"purr","def":"a soft happy sound a cat makes","hint":"\"…it will <b>purr</b>.\""},{"word":"claws","def":"sharp nails on a cat's paw","hint":"\"Cats have sharp <b>claws</b> to climb…\""},{"word":"kitten","def":"a baby cat","hint":"\"A baby cat is called a <b>kitten</b>.\""},{"word":"pounce","def":"to jump on something quickly","hint":"\"They like to <b>pounce</b> on toys.\""}],
 "bank":["whiskers","purr","paws","claws","kitten","pounce"],
 "fills":[{"text":"A cat has long ___ on its face.","a":"whiskers"},{"text":"My cat will ___ when it is happy.","a":"purr"},{"text":"The cat walks on soft ___.","a":"paws"},{"text":"Sharp ___ help a cat climb.","a":"claws"},{"text":"A baby cat is a ___.","a":"kitten"},{"text":"The cat likes to ___ on its toy.","a":"pounce"}]},

{"activityId":"rainbows","projectKey":"rainbows","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Rainbows","heroEmoji":"🌈","watermark":"🌈","pageTitle":"Rainbows","diagramFile":"diagrams/rainbows.svg",
 "win":"PERFECT, Dani! Bright and colorful! 🌈","cheer":"You made the sky smile, Dani! 🌈",
 "palette":{"primary":"#14b8a6","dark":"#0f9384","deep":"#0a6358","accent":"#6dd5c8","accentSoft":"#d6f4ef","cream":"#f2fcfa","bgTop":"#e8f8f5","bgBottom":"#ddf1ed","glow1":"#14b8a622","glow2":"#0a635818"},
 "passageTitle":"Rainbows",
 "passageHtml":"<p>A <span class=\"voc\">rainbow</span> is a band of pretty <span class=\"voc\">color</span>s in the <span class=\"voc\">sky</span>. It looks like a big <span class=\"voc\">arch</span>. You can see a rainbow after it rains.</p><p>A rainbow is made when <span class=\"voc\">sunlight</span> shines through a <span class=\"voc\">raindrop</span>. The light bends and splits into many colors. Red, blue, and green are some of them. Rainbows make people smile!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["bugs","rainbows","cars"],"a":1},{"type":"Detail","q":"A rainbow is shaped like an —","opts":["arch","box","star"],"a":0},{"type":"Detail","q":"You see a rainbow after it —","opts":["rains","snows","sleeps"],"a":0},{"type":"Detail","q":"A rainbow is made from —","opts":["sunlight and raindrops","mud","rocks"],"a":0},{"type":"Vocabulary","q":"The \"sky\" is —","opts":["the ground","the air high above us","a pond"],"a":1}],
 "match":[{"word":"rainbow","def":"a band of colors in the sky","hint":"\"A <b>rainbow</b> is a band of pretty colors…\""},{"word":"arch","def":"a curved shape like a bridge","hint":"\"It looks like a big <b>arch</b>.\""},{"word":"sky","def":"the air high above us","hint":"\"…colors in the <b>sky</b>.\""},{"word":"sunlight","def":"light from the sun","hint":"\"…when <b>sunlight</b> shines through a raindrop.\""},{"word":"raindrop","def":"a small drop of rain","hint":"\"…shines through a <b>raindrop</b>.\""}],
 "bank":["rainbow","color","arch","sky","sunlight","raindrop"],
 "fills":[{"text":"A ___ has many colors.","a":"rainbow"},{"text":"Red is my favorite ___.","a":"color"},{"text":"The rainbow makes a big ___.","a":"arch"},{"text":"Clouds float in the ___.","a":"sky"},{"text":"Plants need ___ to grow.","a":"sunlight"},{"text":"One ___ landed on my nose.","a":"raindrop"}]},

{"activityId":"dinos","projectKey":"dinos","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Dinosaurs","heroEmoji":"🦕","watermark":"🦖","pageTitle":"Dinosaurs","diagramFile":"diagrams/dinos.svg",
 "win":"PERFECT, Dani! Dino-mite! 🦕","cheer":"Roar! Great job, Dani! 🦖",
 "palette":{"primary":"#43a047","dark":"#347a37","deep":"#225224","accent":"#85c888","accentSoft":"#dcf1dd","cream":"#f4fbf4","bgTop":"#ebf7ec","bgBottom":"#e0f0e1","glow1":"#43a04722","glow2":"#22522418"},
 "passageTitle":"Dinosaurs",
 "passageHtml":"<p><span class=\"voc\">Dinosaur</span>s were animals that lived long, long ago. Some were very <span class=\"voc\">huge</span>. Their skin was covered in tough <span class=\"voc\">scales</span>. Some dinosaurs could <span class=\"voc\">roar</span> very loudly.</p><p>Dinosaurs are now <span class=\"voc\">extinct</span>. That means there are none left alive today. We learn about them from a <span class=\"voc\">fossil</span>, which is a bone or print saved in rock. Dinosaurs are amazing to study!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["fish","dinosaurs","trucks"],"a":1},{"type":"Detail","q":"Dinosaur skin had —","opts":["fur","scales","feathers only"],"a":1},{"type":"Vocabulary","q":"\"Extinct\" means —","opts":["none are left alive","very small","very fast"],"a":0},{"type":"Detail","q":"We learn about dinosaurs from a —","opts":["fossil","photo","video"],"a":0},{"type":"Detail","q":"Some dinosaurs were very —","opts":["tiny","huge","purple"],"a":1}],
 "match":[{"word":"dinosaur","def":"an animal that lived long ago","hint":"\"<b>Dinosaur</b>s were animals that lived long ago.\""},{"word":"fossil","def":"a bone or print saved in rock","hint":"\"…a <b>fossil</b>, which is a bone or print saved in rock.\""},{"word":"extinct","def":"when none are left alive","hint":"\"Dinosaurs are now <b>extinct</b>.\""},{"word":"scales","def":"tough skin like a lizard's","hint":"\"Their skin was covered in tough <b>scales</b>.\""},{"word":"roar","def":"a loud, deep sound","hint":"\"Some dinosaurs could <b>roar</b> very loudly.\""}],
 "bank":["dinosaur","fossil","extinct","scales","huge","roar"],
 "fills":[{"text":"A ___ lived millions of years ago.","a":"dinosaur"},{"text":"We found a ___ in the rock.","a":"fossil"},{"text":"Dinosaurs are ___ now.","a":"extinct"},{"text":"Its skin had bumpy ___.","a":"scales"},{"text":"The dinosaur was very ___ and tall.","a":"huge"},{"text":"The big dinosaur let out a ___.","a":"roar"}]},

{"activityId":"beach","projectKey":"beach","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"A Day at the Beach","heroEmoji":"🏖️","watermark":"🐚","pageTitle":"The Beach","diagramFile":"diagrams/beach.svg",
 "win":"PERFECT, Dani! Beach star! 🏖️","cheer":"You made waves, Dani! 🌊",
 "palette":{"primary":"#2bb3d4","dark":"#208ca7","deep":"#155e70","accent":"#7ad3e6","accentSoft":"#d6f1f8","cream":"#f2fbfd","bgTop":"#e8f6fa","bgBottom":"#ddeff4","glow1":"#2bb3d422","glow2":"#155e7018"},
 "passageTitle":"A Day at the Beach",
 "passageHtml":"<p>The <span class=\"voc\">beach</span> is a fun place by the <span class=\"voc\">ocean</span>. The ground is covered in soft <span class=\"voc\">sand</span>. You can build castles in the sand. The blue <span class=\"voc\">wave</span>s splash on the shore.</p><p>You can find a pretty <span class=\"voc\">shell</span> in the sand. The water moves in and out with the <span class=\"voc\">tide</span>. Bring a hat and sunscreen to stay safe. A day at the beach is lots of fun!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["a farm","the beach","a city"],"a":1},{"type":"Detail","q":"The beach is next to the —","opts":["ocean","forest","mountains"],"a":0},{"type":"Detail","q":"The ground at the beach is —","opts":["sand","grass","snow"],"a":0},{"type":"Detail","q":"Waves splash on the —","opts":["shore","roof","road"],"a":0},{"type":"Vocabulary","q":"The \"tide\" is —","opts":["the water moving in and out","a sandcastle","a hat"],"a":0}],
 "match":[{"word":"beach","def":"a sandy place by the sea","hint":"\"The <b>beach</b> is a fun place by the ocean.\""},{"word":"wave","def":"water that rolls onto the shore","hint":"\"The blue <b>wave</b>s splash on the shore.\""},{"word":"shell","def":"a hard cover from a sea animal","hint":"\"You can find a pretty <b>shell</b> in the sand.\""},{"word":"ocean","def":"a very large body of salt water","hint":"\"…a fun place by the <b>ocean</b>.\""},{"word":"tide","def":"the rising and falling of the sea","hint":"\"The water moves in and out with the <b>tide</b>.\""}],
 "bank":["beach","sand","wave","shell","ocean","tide"],
 "fills":[{"text":"We played all day at the ___.","a":"beach"},{"text":"I built a castle in the ___.","a":"sand"},{"text":"A big ___ splashed my feet.","a":"wave"},{"text":"I found a pink ___ on the shore.","a":"shell"},{"text":"Fish live in the ___.","a":"ocean"},{"text":"The ___ went out and left wet sand.","a":"tide"}]},

{"activityId":"farm","projectKey":"farm","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"On the Farm","heroEmoji":"🐄","watermark":"🚜","pageTitle":"Farm Animals","diagramFile":"diagrams/farm.svg",
 "win":"PERFECT, Dani! Farm star! 🐄","cheer":"The animals are cheering, Dani! 🐔",
 "palette":{"primary":"#a1662f","dark":"#7e4f24","deep":"#523114","accent":"#cc9a6c","accentSoft":"#f0e3d4","cream":"#fdf9f3","bgTop":"#f7f0e7","bgBottom":"#efe5d7","glow1":"#a1662f22","glow2":"#52311418"},
 "passageTitle":"On the Farm",
 "passageHtml":"<p>A <span class=\"voc\">farm</span> is home to many animals. The <span class=\"voc\">cow</span> gives us milk. A <span class=\"voc\">hen</span> lays eggs for us to eat. Sheep give us soft <span class=\"voc\">wool</span> for warm clothes.</p><p>At night the animals sleep in the <span class=\"voc\">barn</span>. The farmer feeds them dry <span class=\"voc\">hay</span>. The animals help the farmer every day. Farms are busy, happy places.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["the city","farm animals","the ocean"],"a":1},{"type":"Detail","q":"A cow gives us —","opts":["milk","eggs","wool"],"a":0},{"type":"Detail","q":"A hen lays —","opts":["eggs","hay","wool"],"a":0},{"type":"Detail","q":"Animals sleep in the —","opts":["barn","pool","car"],"a":0},{"type":"Vocabulary","q":"\"Wool\" comes from —","opts":["sheep","cows","hens"],"a":0}],
 "match":[{"word":"farm","def":"a place where animals and crops are raised","hint":"\"A <b>farm</b> is home to many animals.\""},{"word":"barn","def":"a building where farm animals sleep","hint":"\"…the animals sleep in the <b>barn</b>.\""},{"word":"hen","def":"a female chicken that lays eggs","hint":"\"A <b>hen</b> lays eggs for us to eat.\""},{"word":"wool","def":"soft hair from a sheep","hint":"\"Sheep give us soft <b>wool</b>…\""},{"word":"hay","def":"dried grass that animals eat","hint":"\"The farmer feeds them dry <b>hay</b>.\""}],
 "bank":["farm","barn","cow","hen","wool","hay"],
 "fills":[{"text":"We saw many animals at the ___.","a":"farm"},{"text":"The ___ gave us fresh milk.","a":"cow"},{"text":"A ___ laid three eggs.","a":"hen"},{"text":"My sweater is made of warm ___.","a":"wool"},{"text":"The horses sleep in the ___.","a":"barn"},{"text":"The cows eat dry ___.","a":"hay"}]},

{"activityId":"pizza","projectKey":"pizza","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"How We Make Pizza","heroEmoji":"🍕","watermark":"🍕","pageTitle":"Pizza","diagramFile":"diagrams/pizza.svg",
 "win":"PERFECT, Dani! Tasty work! 🍕","cheer":"Yum! Great reading, Dani! 🍕",
 "palette":{"primary":"#e2452f","dark":"#b53624","deep":"#7c2314","accent":"#ef8675","accentSoft":"#fbe1dc","cream":"#fff6f4","bgTop":"#fceee9","bgBottom":"#f7e2dc","glow1":"#e2452f22","glow2":"#7c231418"},
 "passageTitle":"How We Make Pizza",
 "passageHtml":"<p><span class=\"voc\">Pizza</span> is a yummy food that many people love. First you flatten the <span class=\"voc\">dough</span> into a round shape. Then you spread red <span class=\"voc\">sauce</span> on top. Next you add lots of <span class=\"voc\">cheese</span>.</p><p>You can put a <span class=\"voc\">topping</span> on your pizza, like mushrooms or ham. Then it bakes in a hot <span class=\"voc\">oven</span>. The cheese melts and bubbles. Hot pizza is so tasty!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["how to swim","how pizza is made","a pet"],"a":1},{"type":"Detail","q":"The first step is to flatten the —","opts":["dough","cheese","oven"],"a":0},{"type":"Detail","q":"Pizza bakes in a hot —","opts":["oven","pool","box"],"a":0},{"type":"Detail","q":"You spread red ___ on the dough.","opts":["sauce","paint","milk"],"a":0},{"type":"Vocabulary","q":"A \"topping\" is —","opts":["something you add on top","the floor","a drink"],"a":0}],
 "match":[{"word":"dough","def":"soft mix used to make pizza crust","hint":"\"…flatten the <b>dough</b> into a round shape.\""},{"word":"sauce","def":"a soft red topping made from tomatoes","hint":"\"…spread red <b>sauce</b> on top.\""},{"word":"cheese","def":"a melty food made from milk","hint":"\"…add lots of <b>cheese</b>.\""},{"word":"topping","def":"something added on top of pizza","hint":"\"You can put a <b>topping</b> on your pizza…\""},{"word":"oven","def":"a hot box used for baking","hint":"\"…it bakes in a hot <b>oven</b>.\""}],
 "bank":["pizza","dough","sauce","cheese","topping","oven"],
 "fills":[{"text":"We ordered a big ___ for dinner.","a":"pizza"},{"text":"Roll the ___ into a circle.","a":"dough"},{"text":"Spread red ___ on top.","a":"sauce"},{"text":"Add lots of melty ___.","a":"cheese"},{"text":"My favorite ___ is mushrooms.","a":"topping"},{"text":"Bake the pizza in the ___.","a":"oven"}]},

{"activityId":"bugs","projectKey":"bugs","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Bugs and Insects","heroEmoji":"🐞","watermark":"🐛","pageTitle":"Bugs","diagramFile":"diagrams/bugs.svg",
 "win":"PERFECT, Dani! Bug expert! 🐞","cheer":"The ladybugs are proud, Dani! 🐞",
 "palette":{"primary":"#84a516","dark":"#677f11","deep":"#445409","accent":"#b8cf6a","accentSoft":"#eaf2d4","cream":"#f9fbf0","bgTop":"#f1f6e2","bgBottom":"#e7efd2","glow1":"#84a51622","glow2":"#44540918"},
 "passageTitle":"Bugs and Insects",
 "passageHtml":"<p>A bug is a small <span class=\"voc\">insect</span>. Most insects are very <span class=\"voc\">tiny</span>. Many have six legs and two <span class=\"voc\">antenna</span>s on their head. Some bugs have <span class=\"voc\">wing</span>s and can fly.</p><p>A ladybug and a <span class=\"voc\">beetle</span> are kinds of insects. Some bugs <span class=\"voc\">crawl</span> on the ground. Bees and butterflies fly from flower to flower. Bugs are small but very important!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["fish","bugs and insects","cars"],"a":1},{"type":"Detail","q":"Many insects have how many legs?","opts":["two","six","ten"],"a":1},{"type":"Detail","q":"Antennas are on a bug's —","opts":["head","foot","wing"],"a":0},{"type":"Detail","q":"A ladybug is a kind of —","opts":["insect","fish","bird"],"a":0},{"type":"Vocabulary","q":"\"Crawl\" means —","opts":["to move slowly on the ground","to fly fast","to sleep"],"a":0}],
 "match":[{"word":"insect","def":"a small animal with six legs","hint":"\"A bug is a small <b>insect</b>.\""},{"word":"antenna","def":"a feeler on a bug's head","hint":"\"…two <b>antenna</b>s on their head.\""},{"word":"wing","def":"a body part used to fly","hint":"\"Some bugs have <b>wing</b>s and can fly.\""},{"word":"crawl","def":"to move slowly on the ground","hint":"\"Some bugs <b>crawl</b> on the ground.\""},{"word":"beetle","def":"a kind of insect with hard wings","hint":"\"A ladybug and a <b>beetle</b> are kinds of insects.\""}],
 "bank":["insect","antenna","wing","crawl","beetle","tiny"],
 "fills":[{"text":"An ant is a small ___.","a":"insect"},{"text":"A bug feels with its ___s.","a":"antenna"},{"text":"A bee uses its ___s to fly.","a":"wing"},{"text":"The caterpillar will ___ on the leaf.","a":"crawl"},{"text":"A red ___ walked up the stem.","a":"beetle"},{"text":"Ants are very ___.","a":"tiny"}]},

{"activityId":"trucks","projectKey":"trucks","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Big Trucks","heroEmoji":"🚚","watermark":"🚛","pageTitle":"Trucks","diagramFile":"diagrams/trucks.svg",
 "win":"PERFECT, Dani! Full speed! 🚚","cheer":"You delivered every answer, Dani! 🚛",
 "palette":{"primary":"#5872a8","dark":"#445882","deep":"#2c3a56","accent":"#92a5cb","accentSoft":"#e4e9f2","cream":"#f6f8fb","bgTop":"#eef2f8","bgBottom":"#e4eaf3","glow1":"#5872a822","glow2":"#2c3a5618"},
 "passageTitle":"Big Trucks",
 "passageHtml":"<p>A <span class=\"voc\">truck</span> is a big machine that carries heavy things. It has a strong <span class=\"voc\">engine</span> to make it go. A truck rolls on big rubber <span class=\"voc\">wheel</span>s. The <span class=\"voc\">driver</span> sits up high in the front.</p><p>Trucks carry <span class=\"voc\">cargo</span>, like food and toys. They <span class=\"voc\">deliver</span> things to stores and homes. Some trucks are huge and very long. Trucks help bring us the things we need.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["boats","trucks","cats"],"a":1},{"type":"Detail","q":"A truck is made to carry —","opts":["heavy things","people only","nothing"],"a":0},{"type":"Detail","q":"A truck rolls on —","opts":["wheels","wings","skis"],"a":0},{"type":"Detail","q":"The person who drives is the —","opts":["driver","baker","teacher"],"a":0},{"type":"Vocabulary","q":"\"Deliver\" means —","opts":["to bring something to a place","to eat","to sleep"],"a":0}],
 "match":[{"word":"truck","def":"a big machine for carrying heavy loads","hint":"\"A <b>truck</b> is a big machine that carries heavy things.\""},{"word":"engine","def":"the part that makes a vehicle go","hint":"\"It has a strong <b>engine</b> to make it go.\""},{"word":"cargo","def":"the things a truck carries","hint":"\"Trucks carry <b>cargo</b>, like food and toys.\""},{"word":"driver","def":"the person who drives","hint":"\"The <b>driver</b> sits up high in the front.\""},{"word":"deliver","def":"to bring something to a place","hint":"\"They <b>deliver</b> things to stores and homes.\""}],
 "bank":["truck","engine","wheel","cargo","driver","deliver"],
 "fills":[{"text":"The big ___ carried bricks.","a":"truck"},{"text":"The ___ roared as the truck started.","a":"engine"},{"text":"Each ___ is made of rubber.","a":"wheel"},{"text":"The truck was full of ___.","a":"cargo"},{"text":"The ___ honked the horn.","a":"driver"},{"text":"Trucks ___ food to the store.","a":"deliver"}]},

{"activityId":"teeth","projectKey":"teeth","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Brushing Your Teeth","heroEmoji":"🦷","watermark":"🪥","pageTitle":"Brushing Your Teeth","diagramFile":"diagrams/teeth.svg",
 "win":"PERFECT, Dani! Bright smile! 🦷","cheer":"Sparkling work, Dani! ✨",
 "palette":{"primary":"#1697b5","dark":"#11778f","deep":"#0a4f60","accent":"#69c4d8","accentSoft":"#d4f0f6","cream":"#f2fbfc","bgTop":"#e8f6f9","bgBottom":"#ddeff3","glow1":"#1697b522","glow2":"#0a4f6018"},
 "passageTitle":"Brushing Your Teeth",
 "passageHtml":"<p>It is important to take care of your <span class=\"voc\">teeth</span>. You should <span class=\"voc\">brush</span> them two times a day. Put a little <span class=\"voc\">toothpaste</span> on your brush. Brushing keeps your teeth clean and white.</p><p>Clean teeth are <span class=\"voc\">healthy</span> teeth. If you do not brush, you can get a <span class=\"voc\">cavity</span>, which is a hole in a tooth. A <span class=\"voc\">dentist</span> checks your teeth to keep them strong. A bright smile feels great!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["washing dishes","taking care of your teeth","baking bread"],"a":1},{"type":"Detail","q":"You should brush —","opts":["two times a day","once a week","never"],"a":0},{"type":"Detail","q":"You put ___ on your brush.","opts":["toothpaste","juice","soap"],"a":0},{"type":"Vocabulary","q":"A \"cavity\" is —","opts":["a hole in a tooth","a clean tooth","a brush"],"a":0},{"type":"Detail","q":"A ___ checks your teeth.","opts":["dentist","chef","pilot"],"a":0}],
 "match":[{"word":"brush","def":"to clean with a small tool with bristles","hint":"\"You should <b>brush</b> them two times a day.\""},{"word":"toothpaste","def":"a paste used to clean teeth","hint":"\"Put a little <b>toothpaste</b> on your brush.\""},{"word":"healthy","def":"strong and well, not sick","hint":"\"Clean teeth are <b>healthy</b> teeth.\""},{"word":"cavity","def":"a hole in a tooth","hint":"\"…you can get a <b>cavity</b>, which is a hole in a tooth.\""},{"word":"dentist","def":"a doctor for your teeth","hint":"\"A <b>dentist</b> checks your teeth…\""}],
 "bank":["teeth","brush","toothpaste","healthy","cavity","dentist"],
 "fills":[{"text":"I clean my ___ every morning.","a":"teeth"},{"text":"I ___ my teeth before bed.","a":"brush"},{"text":"Put mint ___ on the brush.","a":"toothpaste"},{"text":"Brushing keeps me ___.","a":"healthy"},{"text":"Too much candy can cause a ___.","a":"cavity"},{"text":"The ___ counted all my teeth.","a":"dentist"}]},

{"activityId":"seasons","projectKey":"seasons","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"The Four Seasons","heroEmoji":"🍂","watermark":"❄️","pageTitle":"The Seasons","diagramFile":"diagrams/seasons.svg",
 "win":"PERFECT, Dani! All four seasons! 🍂","cheer":"You bloomed, Dani! 🌸",
 "palette":{"primary":"#8e57b8","dark":"#6f4392","deep":"#492c60","accent":"#bb93d8","accentSoft":"#ece1f4","cream":"#fbf8fd","bgTop":"#f3ecf9","bgBottom":"#eae0f2","glow1":"#8e57b822","glow2":"#492c6018"},
 "passageTitle":"The Four Seasons",
 "passageHtml":"<p>There are four <span class=\"voc\">season</span>s in a year. In <span class=\"voc\">spring</span>, flowers begin to grow. In <span class=\"voc\">summer</span>, the days are hot and sunny. We swim and play outside.</p><p>In <span class=\"voc\">autumn</span>, the leaves turn orange and fall down. In <span class=\"voc\">winter</span>, it is cold and it may snow. Each season has its own <span class=\"voc\">weather</span>. The seasons change all year long.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["the ocean","the four seasons","trucks"],"a":1},{"type":"Detail","q":"How many seasons are there?","opts":["four","two","ten"],"a":0},{"type":"Detail","q":"In summer the days are —","opts":["hot and sunny","snowy","dark all day"],"a":0},{"type":"Detail","q":"In autumn the leaves —","opts":["fall down","grow blue","disappear"],"a":0},{"type":"Vocabulary","q":"\"Weather\" is —","opts":["what the sky and air are doing","a kind of leaf","a season name"],"a":0}],
 "match":[{"word":"spring","def":"the season when flowers grow","hint":"\"In <b>spring</b>, flowers begin to grow.\""},{"word":"summer","def":"the hot, sunny season","hint":"\"In <b>summer</b>, the days are hot and sunny.\""},{"word":"autumn","def":"the season when leaves fall","hint":"\"In <b>autumn</b>, the leaves turn orange and fall.\""},{"word":"winter","def":"the cold, snowy season","hint":"\"In <b>winter</b>, it is cold and it may snow.\""},{"word":"weather","def":"what the sky and air are doing","hint":"\"Each season has its own <b>weather</b>.\""}],
 "bank":["season","spring","summer","autumn","winter","weather"],
 "fills":[{"text":"There are four ___s in a year.","a":"season"},{"text":"Flowers bloom in the ___.","a":"spring"},{"text":"We swim in the hot ___.","a":"summer"},{"text":"Leaves fall in the ___.","a":"autumn"},{"text":"It snows in the ___.","a":"winter"},{"text":"The ___ today is sunny.","a":"weather"}]},

{"activityId":"butterflies","projectKey":"butterflies","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Butterflies","heroEmoji":"🦋","watermark":"🌸","pageTitle":"Butterflies","diagramFile":"diagrams/butterflies.svg",
 "win":"PERFECT, Dani! You are a butterfly star! 🦋","cheer":"You flew through every question! 🦋",
 "palette":{"primary":"#c94fbf","dark":"#9c3497","deep":"#6b1f6b","accent":"#e89de3","accentSoft":"#fae5f8","cream":"#fef8fe","bgTop":"#faf0fb","bgBottom":"#f5e6f7","glow1":"#c94fbf22","glow2":"#6b1f6b18"},
 "passageTitle":"Butterflies",
 "passageHtml":"<p>A butterfly starts as a tiny <span class=\"voc\">egg</span>. The egg hatches into a <span class=\"voc\">caterpillar</span>. The caterpillar eats and eats. Then it wraps itself in a soft <span class=\"voc\">chrysalis</span>.</p><p>Inside the chrysalis, something amazing happens. The caterpillar changes into a <span class=\"voc\">butterfly</span>. This change is called <span class=\"voc\">metamorphosis</span>. The butterfly opens its <span class=\"voc\">wing</span>s and flies away!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["frogs","butterflies","trucks"],"a":1},{"type":"Detail","q":"A butterfly starts life as a —","opts":["egg","feather","flower"],"a":0},{"type":"Detail","q":"The caterpillar wraps itself in a —","opts":["chrysalis","shell","cave"],"a":0},{"type":"Vocabulary","q":"\"Metamorphosis\" means —","opts":["a big change in form","flying away","eating leaves"],"a":0},{"type":"Detail","q":"What does the butterfly do at the end?","opts":["opens its wings and flies","goes to sleep","lays an egg first"],"a":0}],
 "match":[{"word":"egg","def":"the tiny start of a butterfly's life","hint":"\"A butterfly starts as a tiny <b>egg</b>.\""},{"word":"caterpillar","def":"the worm-like stage after the egg","hint":"\"The egg hatches into a <b>caterpillar</b>.\""},{"word":"chrysalis","def":"the covering a caterpillar makes around itself","hint":"\"…wraps itself in a soft <b>chrysalis</b>.\""},{"word":"metamorphosis","def":"a big change in form","hint":"\"This change is called <b>metamorphosis</b>.\""},{"word":"wing","def":"a body part used for flying","hint":"\"The butterfly opens its <b>wing</b>s and flies away!\""}],
 "bank":["egg","caterpillar","chrysalis","butterfly","metamorphosis","wing"],
 "fills":[{"text":"A butterfly starts as an ___.","a":"egg"},{"text":"The ___ munched on green leaves.","a":"caterpillar"},{"text":"The caterpillar rested in its ___.","a":"chrysalis"},{"text":"A ___ has four beautiful wings.","a":"butterfly"},{"text":"The big change is called ___.","a":"metamorphosis"},{"text":"Each ___ has a pretty pattern.","a":"wing"}]},

{"activityId":"birds","projectKey":"birds","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Birds","heroEmoji":"🐦","watermark":"🪶","pageTitle":"Birds","diagramFile":"diagrams/birds.svg",
 "win":"PERFECT, Dani! You soared through it! 🐦","cheer":"You're a reading bird! 🪶",
 "palette":{"primary":"#2e86de","dark":"#1a6ab8","deep":"#0d4a88","accent":"#74b9ff","accentSoft":"#dff0ff","cream":"#f5faff","bgTop":"#edf5ff","bgBottom":"#e0ecff","glow1":"#2e86de22","glow2":"#0d4a8818"},
 "passageTitle":"Birds",
 "passageHtml":"<p>Birds are animals with <span class=\"voc\">feather</span>s. Feathers keep birds warm and help them fly. A bird has a sharp <span class=\"voc\">beak</span> to pick up food. Birds build a <span class=\"voc\">nest</span> to keep their eggs safe.</p><p>When eggs <span class=\"voc\">hatch</span>, baby birds come out. Some birds fly south when it gets cold. We say they <span class=\"voc\">migrate</span>. Birds that travel together are called a <span class=\"voc\">flock</span>. Birds are amazing!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["fish","dogs","birds"],"a":2},{"type":"Detail","q":"Feathers help birds —","opts":["stay warm and fly","swim","build roads"],"a":0},{"type":"Detail","q":"A bird builds a nest to keep —","opts":["eggs safe","food cold","water clean"],"a":0},{"type":"Vocabulary","q":"\"Migrate\" means —","opts":["to travel to a warmer place","to build a nest","to hatch"],"a":0},{"type":"Detail","q":"A group of birds traveling together is called a —","opts":["flock","herd","pack"],"a":0}],
 "match":[{"word":"feather","def":"a light covering on a bird's body","hint":"\"Birds are animals with <b>feather</b>s.\""},{"word":"beak","def":"the hard, pointed mouth of a bird","hint":"\"A bird has a sharp <b>beak</b> to pick up food.\""},{"word":"nest","def":"a cozy home built by birds for their eggs","hint":"\"Birds build a <b>nest</b> to keep their eggs safe.\""},{"word":"migrate","def":"to travel to a warmer place when it gets cold","hint":"\"…they <b>migrate</b>.\""},{"word":"hatch","def":"to break out of an egg","hint":"\"When eggs <b>hatch</b>, baby birds come out.\""}],
 "bank":["feather","beak","nest","migrate","hatch","flock"],
 "fills":[{"text":"A bird is covered in ___s.","a":"feather"},{"text":"The robin used its ___ to crack the seed.","a":"beak"},{"text":"The bird made a cozy ___ in the tree.","a":"nest"},{"text":"Birds ___ south in autumn.","a":"migrate"},{"text":"The chick began to ___ from the egg.","a":"hatch"},{"text":"A ___ of geese flew overhead.","a":"flock"}]},

{"activityId":"weather","projectKey":"weather","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Weather","heroEmoji":"⛅","watermark":"🌧️","pageTitle":"Weather","diagramFile":"diagrams/weather.svg",
 "win":"PERFECT, Dani! Weather expert! ⛅","cheer":"You shone like the sun! ☀️",
 "palette":{"primary":"#f39c12","dark":"#c77b0a","deep":"#8a5607","accent":"#f8c471","accentSoft":"#fef6e0","cream":"#fffdf5","bgTop":"#fefbec","bgBottom":"#fdf5da","glow1":"#f39c1222","glow2":"#8a560718"},
 "passageTitle":"Weather",
 "passageHtml":"<p><span class=\"voc\">Weather</span> tells us what the air outside is like. On a <span class=\"voc\">sunny</span> day, the sun is bright and warm. On a <span class=\"voc\">cloudy</span> day, clouds cover the sky. When clouds hold lots of water, they make it <span class=\"voc\">rainy</span>.</p><p>On a <span class=\"voc\">windy</span> day, the air blows fast. Sometimes big clouds and strong wind make a <span class=\"voc\">storm</span>. A storm can bring thunder and lightning. We look at the sky to know what to wear each day!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["food","weather","animals"],"a":1},{"type":"Detail","q":"On a sunny day the sun is —","opts":["bright and warm","cold and dark","hiding"],"a":0},{"type":"Detail","q":"Clouds hold water and make it —","opts":["rainy","sunny","windy"],"a":0},{"type":"Vocabulary","q":"A \"storm\" is —","opts":["big clouds and strong wind together","a small cloud","a sunny day"],"a":0},{"type":"Detail","q":"We look at the sky to know what to —","opts":["wear","cook","draw"],"a":0}],
 "match":[{"word":"weather","def":"what the air outside is like","hint":"\"<b>Weather</b> tells us what the air outside is like.\""},{"word":"sunny","def":"bright and warm with lots of sunshine","hint":"\"On a <b>sunny</b> day, the sun is bright and warm.\""},{"word":"cloudy","def":"when clouds cover the sky","hint":"\"On a <b>cloudy</b> day, clouds cover the sky.\""},{"word":"rainy","def":"when water falls from clouds","hint":"\"…they make it <b>rainy</b>.\""},{"word":"storm","def":"big clouds and strong wind together","hint":"\"…big clouds and strong wind make a <b>storm</b>.\""}],
 "bank":["weather","sunny","cloudy","rainy","windy","storm"],
 "fills":[{"text":"Today's ___ is warm and bright.","a":"weather"},{"text":"It is a ___ day — perfect for the park!","a":"sunny"},{"text":"The sky is grey and ___.","a":"cloudy"},{"text":"Bring an umbrella — it will be ___.","a":"rainy"},{"text":"It is so ___ that my hat blew off!","a":"windy"},{"text":"The big ___ knocked down a branch.","a":"storm"}]},

{"activityId":"plants","projectKey":"plants","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"How Plants Grow","heroEmoji":"🌱","watermark":"🌿","pageTitle":"How Plants Grow","diagramFile":"diagrams/plants.svg",
 "win":"PERFECT, Dani! You made it bloom! 🌸","cheer":"You're growing as a reader! 🌱",
 "palette":{"primary":"#27ae60","dark":"#1e8449","deep":"#145a32","accent":"#82e0aa","accentSoft":"#d5f5e3","cream":"#f4fff7","bgTop":"#ebfaf0","bgBottom":"#e0f5e8","glow1":"#27ae6022","glow2":"#145a3218"},
 "passageTitle":"How Plants Grow",
 "passageHtml":"<p>Plants begin as a tiny <span class=\"voc\">seed</span>. A seed needs water and <span class=\"voc\">sunlight</span> to grow. It is planted in <span class=\"voc\">soil</span>. The roots push down and the <span class=\"voc\">stem</span> pushes up.</p><p>A green <span class=\"voc\">leaf</span> grows on the stem. The leaf catches sunlight to make food for the plant. At the top, a beautiful <span class=\"voc\">root</span> drinks water from the soil. Plants give us food, clean air, and beauty!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["trucks","how plants grow","weather"],"a":1},{"type":"Detail","q":"A seed needs water and —","opts":["sunlight","snow","sand"],"a":0},{"type":"Detail","q":"The roots push —","opts":["down into the soil","up into the sky","sideways"],"a":0},{"type":"Vocabulary","q":"\"Soil\" is —","opts":["the dirt where plants grow","a type of leaf","the sun's light"],"a":0},{"type":"Detail","q":"Leaves help the plant by catching —","opts":["sunlight","rain only","insects"],"a":0}],
 "match":[{"word":"seed","def":"the tiny start of a plant","hint":"\"Plants begin as a tiny <b>seed</b>.\""},{"word":"sunlight","def":"the light that comes from the sun","hint":"\"A seed needs water and <b>sunlight</b> to grow.\""},{"word":"soil","def":"the dirt where plants grow","hint":"\"It is planted in <b>soil</b>.\""},{"word":"stem","def":"the tall part of a plant that holds it up","hint":"\"…the <b>stem</b> pushes up.\""},{"word":"leaf","def":"the flat green part of a plant","hint":"\"A green <b>leaf</b> grows on the stem.\""}],
 "bank":["seed","root","stem","leaf","sunlight","soil"],
 "fills":[{"text":"We planted a ___ in the pot.","a":"seed"},{"text":"The ___ drank water deep underground.","a":"root"},{"text":"The tall ___ holds the flower up.","a":"stem"},{"text":"Each ___ is flat and green.","a":"leaf"},{"text":"The plant turned toward the ___.","a":"sunlight"},{"text":"Good ___ helps plants grow strong.","a":"soil"}]},

{"activityId":"penguins","projectKey":"penguins","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Penguins","heroEmoji":"🐧","watermark":"❄️","pageTitle":"Penguins","diagramFile":"diagrams/penguins.svg",
 "win":"PERFECT, Dani! You're an Antarctic champion! 🐧","cheer":"You waddled right through it! 🐧",
 "palette":{"primary":"#1a73c2","dark":"#115ea3","deep":"#0a3f72","accent":"#7ab7f0","accentSoft":"#d9edff","cream":"#f2f8ff","bgTop":"#e8f3ff","bgBottom":"#daeaff","glow1":"#1a73c222","glow2":"#0a3f7218"},
 "passageTitle":"Penguins",
 "passageHtml":"<p>Penguins are birds that cannot fly. They live in cold <span class=\"voc\">Antarctica</span>. Instead of flying, they use their <span class=\"voc\">flipper</span>s to <span class=\"voc\">swim</span> very fast. They eat fish from the ocean.</p><p>Penguins <span class=\"voc\">waddle</span> when they walk on land. When it is very cold, they stand together in a big group called a <span class=\"voc\">huddle</span>. The <span class=\"voc\">penguin</span> in the middle stays the warmest. Penguins are amazing birds!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["butterflies","penguins","baking"],"a":1},{"type":"Detail","q":"Penguins live in cold —","opts":["Antarctica","Africa","the rainforest"],"a":0},{"type":"Detail","q":"Penguins use their flippers to —","opts":["swim","fly","dig"],"a":0},{"type":"Vocabulary","q":"\"Huddle\" means —","opts":["to crowd together for warmth","to swim away","to eat fish"],"a":0},{"type":"Detail","q":"How do penguins walk on land?","opts":["They waddle","They hop","They slide only"],"a":0}],
 "match":[{"word":"Antarctica","def":"the very cold land at the bottom of the Earth","hint":"\"They live in cold <b>Antarctica</b>.\""},{"word":"flipper","def":"the flat limb a penguin uses to swim","hint":"\"…their <b>flipper</b>s to swim very fast.\""},{"word":"swim","def":"to move through water","hint":"\"…use their flippers to <b>swim</b> very fast.\""},{"word":"waddle","def":"to walk by rocking from side to side","hint":"\"Penguins <b>waddle</b> when they walk on land.\""},{"word":"huddle","def":"to crowd together for warmth","hint":"\"…in a big group called a <b>huddle</b>.\""}],
 "bank":["penguin","Antarctica","swim","huddle","flipper","waddle"],
 "fills":[{"text":"A ___ is a bird that cannot fly.","a":"penguin"},{"text":"Penguins live on the ice of ___.","a":"Antarctica"},{"text":"Penguins use their flippers to ___.","a":"swim"},{"text":"They ___ like they are rocking side to side.","a":"waddle"},{"text":"In the cold, penguins ___ together.","a":"huddle"},{"text":"Each ___ acts like a paddle in the water.","a":"flipper"}]},

{"activityId":"frogs","projectKey":"frogs","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Frogs","heroEmoji":"🐸","watermark":"🌿","pageTitle":"Frogs","diagramFile":"diagrams/frogs.svg",
 "win":"PERFECT, Dani! Ribbit ribbit! 🐸","cheer":"You leaped through every question! 🐸",
 "palette":{"primary":"#2ecc71","dark":"#1da85c","deep":"#117a40","accent":"#82e0aa","accentSoft":"#d5f5e3","cream":"#f0fdf5","bgTop":"#e8faf0","bgBottom":"#daf5e8","glow1":"#2ecc7122","glow2":"#117a4018"},
 "passageTitle":"Frogs",
 "passageHtml":"<p>A frog starts life as eggs in a <span class=\"voc\">pond</span>. The eggs <span class=\"voc\">hatch</span> into a <span class=\"voc\">tadpole</span>. A tadpole looks like a tiny fish with a tail. Slowly, the tadpole grows legs.</p><p>When it has four legs and no tail, it is a frog. Frogs can <span class=\"voc\">leap</span> very far with their strong back legs. They catch insects with their long sticky <span class=\"voc\">tongue</span>. A frog is an <span class=\"voc\">amphibian</span> — it can live in water and on land!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["birds","frogs","plants"],"a":1},{"type":"Detail","q":"A frog starts life as eggs in a —","opts":["pond","tree","cloud"],"a":0},{"type":"Detail","q":"A tadpole grows legs and becomes a —","opts":["frog","fish","bird"],"a":0},{"type":"Vocabulary","q":"An \"amphibian\" is an animal that —","opts":["lives in water and on land","only swims","only hops"],"a":0},{"type":"Detail","q":"Frogs catch insects with their —","opts":["tongue","feet","wings"],"a":0}],
 "match":[{"word":"tadpole","def":"a baby frog that swims and has a tail","hint":"\"The eggs hatch into a <b>tadpole</b>.\""},{"word":"pond","def":"a small body of water","hint":"\"…eggs in a <b>pond</b>.\""},{"word":"leap","def":"to jump a long way","hint":"\"Frogs can <b>leap</b> very far.\""},{"word":"tongue","def":"the long sticky part a frog uses to catch insects","hint":"\"…long sticky <b>tongue</b>.\""},{"word":"amphibian","def":"an animal that lives in water and on land","hint":"\"A frog is an <b>amphibian</b>…\""}],
 "bank":["tadpole","pond","leap","tongue","amphibian","hatch"],
 "fills":[{"text":"The frog eggs floated in the ___.","a":"pond"},{"text":"The eggs ___ into tadpoles.","a":"hatch"},{"text":"A ___ has a tail and no legs yet.","a":"tadpole"},{"text":"Frogs ___ from lily pad to lily pad.","a":"leap"},{"text":"The frog flicked its ___ to catch a fly.","a":"tongue"},{"text":"A frog is an ___ that lives in water and on land.","a":"amphibian"}]},

{"activityId":"elephants","projectKey":"elephants","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Elephants","heroEmoji":"🐘","watermark":"🌍","pageTitle":"Elephants","diagramFile":"diagrams/elephants.svg",
 "win":"PERFECT, Dani! You're as strong as an elephant! 🐘","cheer":"Never forget how well you did! 🐘",
 "palette":{"primary":"#7f8c8d","dark":"#606c6d","deep":"#3d4c4d","accent":"#aab7b8","accentSoft":"#e8ecec","cream":"#f7f8f8","bgTop":"#f0f3f3","bgBottom":"#e8ecec","glow1":"#7f8c8d22","glow2":"#3d4c4d18"},
 "passageTitle":"Elephants",
 "passageHtml":"<p>The elephant is the biggest animal that lives on land. It has a long <span class=\"voc\">trunk</span> that it uses to drink water and pick up food. An elephant also has big <span class=\"voc\">tusk</span>s made of ivory. Its large ears help it stay cool.</p><p>Elephants live in <span class=\"voc\">Africa</span> and Asia. They travel in family groups called a <span class=\"voc\">herd</span>. An elephant can <span class=\"voc\">spray</span> water with its trunk to cool down. Elephants are <span class=\"voc\">enormous</span> and very smart!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["penguins","elephants","frogs"],"a":1},{"type":"Detail","q":"An elephant uses its trunk to —","opts":["drink water and pick up food","fly","sing"],"a":0},{"type":"Vocabulary","q":"\"Enormous\" means —","opts":["very very big","very tiny","very loud"],"a":0},{"type":"Detail","q":"Elephants travel in family groups called a —","opts":["herd","flock","pack"],"a":0},{"type":"Detail","q":"Elephants live in Africa and —","opts":["Asia","Europe","Antarctica"],"a":0}],
 "match":[{"word":"trunk","def":"the long nose an elephant uses to drink and pick things up","hint":"\"…a long <b>trunk</b> that it uses to drink water.\""},{"word":"herd","def":"a group of animals that travel together","hint":"\"…family groups called a <b>herd</b>.\""},{"word":"tusk","def":"a long pointed tooth made of ivory","hint":"\"…big <b>tusk</b>s made of ivory.\""},{"word":"spray","def":"to shoot water out","hint":"\"…can <b>spray</b> water with its trunk.\""},{"word":"enormous","def":"very very big","hint":"\"Elephants are <b>enormous</b>…\""}],
 "bank":["trunk","herd","tusk","spray","Africa","enormous"],
 "fills":[{"text":"The elephant lifted hay with its ___.","a":"trunk"},{"text":"A ___ of elephants walked to the river.","a":"herd"},{"text":"Each ___ is made of white ivory.","a":"tusk"},{"text":"The elephant used its trunk to ___ itself with water.","a":"spray"},{"text":"Elephants in ___ live on the hot plains.","a":"Africa"},{"text":"The ___ elephant was taller than the trees.","a":"enormous"}]},

{"activityId":"moon","projectKey":"moon","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"The Moon","heroEmoji":"🌕","watermark":"⭐","pageTitle":"The Moon","diagramFile":"diagrams/moon.svg",
 "win":"PERFECT, Dani! Moonshot! 🌕","cheer":"You're a star reader! ⭐",
 "palette":{"primary":"#5c6bc0","dark":"#3949ab","deep":"#1a237e","accent":"#9fa8da","accentSoft":"#e8eaf6","cream":"#f5f5fd","bgTop":"#eef0fa","bgBottom":"#e5e8f5","glow1":"#5c6bc022","glow2":"#1a237e18"},
 "passageTitle":"The Moon",
 "passageHtml":"<p>The <span class=\"voc\">moon</span> is a big rock that circles the Earth. It does not make its own light. It shines because it reflects light from the sun. The moon has bumps and holes called <span class=\"voc\">crater</span>s on its <span class=\"voc\">surface</span>.</p><p>The moon travels around Earth in an <span class=\"voc\">orbit</span>. As it moves, we see different shapes — these are called <span class=\"voc\">phase</span>s. Sometimes it looks like a thin crescent. Sometimes it is a big full circle! <span class=\"voc\">Astronaut</span>s have walked on the moon.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["the sun","the moon","the stars"],"a":1},{"type":"Detail","q":"The moon does not make its own light — it reflects light from —","opts":["the sun","the earth","the stars"],"a":0},{"type":"Vocabulary","q":"A \"crater\" is —","opts":["a bumpy hole on the moon's surface","a moon phase","an astronaut's suit"],"a":0},{"type":"Detail","q":"The moon travels in an —","opts":["orbit","island","ocean"],"a":0},{"type":"Detail","q":"People who have walked on the moon are called —","opts":["astronauts","teachers","pilots"],"a":0}],
 "match":[{"word":"crater","def":"a hole or bump on the moon's surface","hint":"\"…holes called <b>crater</b>s on its surface.\""},{"word":"orbit","def":"the path the moon takes around the Earth","hint":"\"The moon travels around Earth in an <b>orbit</b>.\""},{"word":"phase","def":"a shape of the moon we see as it moves","hint":"\"…we see different shapes — these are called <b>phase</b>s.\""},{"word":"astronaut","def":"a person who travels to space","hint":"\"<b>Astronaut</b>s have walked on the moon.\""},{"word":"surface","def":"the outside or top layer of something","hint":"\"…on its <b>surface</b>.\""}],
 "bank":["moon","crater","orbit","phase","astronaut","surface"],
 "fills":[{"text":"The ___ glows in the night sky.","a":"moon"},{"text":"Astronauts found a big ___ on the moon.","a":"crater"},{"text":"The moon follows its ___ around the Earth.","a":"orbit"},{"text":"Each ___ of the moon looks a little different.","a":"phase"},{"text":"An ___ floated in space.","a":"astronaut"},{"text":"The moon's ___ is dry and rocky.","a":"surface"}]},

{"activityId":"bread","projectKey":"bread","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Baking Bread","heroEmoji":"🍞","watermark":"🧁","pageTitle":"Baking Bread","diagramFile":"diagrams/bread.svg",
 "win":"PERFECT, Dani! You're a star baker! 🍞","cheer":"That was a piece of cake! 🍞",
 "palette":{"primary":"#e67e22","dark":"#c0640e","deep":"#884707","accent":"#f0a060","accentSoft":"#fdebd0","cream":"#fff8f0","bgTop":"#fdf3e5","bgBottom":"#f9e8d5","glow1":"#e67e2222","glow2":"#88470718"},
 "passageTitle":"Baking Bread",
 "passageHtml":"<p>To make bread, you mix <span class=\"voc\">flour</span>, water, and <span class=\"voc\">yeast</span>. You also add a little salt. When you mix them all together, you get a soft <span class=\"voc\">dough</span>. You knead the dough with your hands.</p><p>Then you wait for the dough to <span class=\"voc\">rise</span> and get bigger. Yeast makes the dough puff up! Next, you put the dough in the <span class=\"voc\">oven</span>. You <span class=\"voc\">bake</span> it until it is golden and warm. Fresh bread smells wonderful!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["baking bread","growing plants","the moon"],"a":0},{"type":"Detail","q":"To make bread you mix flour, water, salt, and —","opts":["yeast","sugar","eggs"],"a":0},{"type":"Vocabulary","q":"\"Dough\" is —","opts":["the soft mixture before it is baked","a baked loaf","the oven heat"],"a":0},{"type":"Detail","q":"Yeast makes the dough —","opts":["rise and puff up","taste salty","turn blue"],"a":0},{"type":"Detail","q":"Where do you bake the bread?","opts":["in the oven","in the fridge","in water"],"a":0}],
 "match":[{"word":"flour","def":"the white powder used to make bread","hint":"\"…you mix <b>flour</b>, water, and yeast.\""},{"word":"yeast","def":"the ingredient that makes dough puff up","hint":"\"…and <b>yeast</b>.\""},{"word":"dough","def":"the soft mixture of flour, water, and yeast","hint":"\"…you get a soft <b>dough</b>.\""},{"word":"rise","def":"to grow bigger and puff up","hint":"\"…for the dough to <b>rise</b>…\""},{"word":"oven","def":"the hot machine used to bake food","hint":"\"…put the dough in the <b>oven</b>.\""}],
 "bank":["flour","yeast","dough","rise","oven","bake"],
 "fills":[{"text":"Stir the ___ into the bowl.","a":"flour"},{"text":"Add the ___ so the bread will puff up.","a":"yeast"},{"text":"Knead the ___ until it is smooth.","a":"dough"},{"text":"Let the dough ___ for one hour.","a":"rise"},{"text":"Put the pan into the hot ___.","a":"oven"},{"text":"We will ___ it at 200 degrees.","a":"bake"}]},

{"activityId":"fish","projectKey":"fish","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Fish","heroEmoji":"🐟","watermark":"🌊","pageTitle":"Fish","diagramFile":"diagrams/fish.svg",
 "win":"PERFECT, Dani! You're swimming in success! 🐟","cheer":"You really went for it, Dani! 🐟",
 "palette":{"primary":"#00897b","dark":"#00695c","deep":"#004d40","accent":"#4db6ac","accentSoft":"#ccf0eb","cream":"#f0fdfb","bgTop":"#e5faf7","bgBottom":"#d8f5f0","glow1":"#00897b22","glow2":"#004d4018"},
 "passageTitle":"Fish",
 "passageHtml":"<p>Fish live <span class=\"voc\">underwater</span>. They breathe through parts called <span class=\"voc\">gill</span>s on the sides of their body. Fish have <span class=\"voc\">fin</span>s to help them steer and balance in the water. Their body is covered in tiny <span class=\"voc\">scale</span>s.</p><p>Fish <span class=\"voc\">swim</span> by moving their tail from side to side. Some fish live in the <span class=\"voc\">ocean</span>. Others live in rivers, lakes, and ponds. Fish come in many sizes and beautiful colours. There are over 30,000 kinds of fish in the world!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["birds","fish","elephants"],"a":1},{"type":"Detail","q":"Fish breathe through —","opts":["gills","lungs","fins"],"a":0},{"type":"Detail","q":"Fish steer and balance using their —","opts":["fins","scales","gills"],"a":0},{"type":"Vocabulary","q":"\"Scale\" is —","opts":["a tiny flat covering on a fish's body","a type of fin","the inside of a gill"],"a":0},{"type":"Detail","q":"Fish swim by moving their —","opts":["tail","fins on top","head"],"a":0}],
 "match":[{"word":"gill","def":"the part a fish uses to breathe underwater","hint":"\"…breathe through parts called <b>gill</b>s.\""},{"word":"fin","def":"a flat part that helps a fish steer in water","hint":"\"Fish have <b>fin</b>s to help them steer.\""},{"word":"scale","def":"a tiny flat piece that covers a fish's body","hint":"\"…covered in tiny <b>scale</b>s.\""},{"word":"underwater","def":"below the surface of the water","hint":"\"Fish live <b>underwater</b>.\""},{"word":"ocean","def":"a huge body of salty water","hint":"\"Some fish live in the <b>ocean</b>.\""}],
 "bank":["gill","fin","scale","underwater","ocean","swim"],
 "fills":[{"text":"Fish breathe through their ___s.","a":"gill"},{"text":"The ___ helps the fish turn left and right.","a":"fin"},{"text":"Each tiny ___ protects the fish's body.","a":"scale"},{"text":"Crabs live ___ on the sea floor.","a":"underwater"},{"text":"Sharks live in the deep ___.","a":"ocean"},{"text":"Fish ___ by moving their tails.","a":"swim"}]}
,
{
 "activityId":"earthquakes",
 "projectKey":"earthquakes",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Earthquakes",
 "heroEmoji":"\U0001f30d","watermark":"\U0001f4a5","pageTitle":"Earthquakes","diagramFile":"diagrams/earthquakes.svg",
 "win":"PERFECT, Amara! You shook it! \U0001f30d",
 "cheer":"Rock-solid reading, Amara! \U0001faa8",
 "palette":{"primary":"#8b4513","dark":"#6a340e","deep":"#3e1f08","accent":"#c8935a","accentSoft":"#f5e0cc","cream":"#fdf6ee","bgTop":"#faf0e4","bgBottom":"#f5e4d4","glow1":"#8b451322","glow2":"#3e1f0818"},
 "passageTitle":"Earthquakes",
 "passageHtml":
"<p>Deep inside the Earth, enormous slabs of rock called <span class=\"voc\">tectonic</span> plates are constantly moving. Where two plates meet, a crack in the crust forms, known as a <span class=\"voc\">fault</span>. Pressure builds up along the fault over hundreds of years. When the pressure finally releases all at once, the ground begins to <span class=\"voc\">vibrate</span>, sending energy racing outward in all directions.</p>"
"<p>The energy travels as <span class=\"voc\">seismic</span> waves, which shake everything in their path. The point on the ground directly above where the earthquake starts underground is called the <span class=\"voc\">epicenter</span>. Scientists measure how powerful an earthquake is using the Richter scale. The number given to describe the earthquake's power is its <span class=\"voc\">magnitude</span>. Larger numbers mean stronger, more destructive shaking.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mostly about —","opts":["how buildings are made to survive earthquakes","what causes earthquakes and how they are measured","why tectonic plates were discovered"],"a":1},
   {"type":"Detail","q":"What builds up along a fault before an earthquake?","opts":["Seismic waves","Heat from the mantle","Pressure"],"a":2},
   {"type":"Vocabulary","q":"\"Seismic\" relates to —","opts":["the movement of tectonic plates","the energy waves produced by an earthquake","the measure of an earthquake's strength"],"a":1},
   {"type":"Detail","q":"What is the epicenter?","opts":["The underground point where the earthquake begins","The point on the surface directly above where the earthquake starts","The scale used to measure earthquake strength"],"a":1},
   {"type":"Vocabulary","q":"\"Magnitude\" describes —","opts":["how deep underground an earthquake starts","how long an earthquake lasts","how powerful an earthquake is"],"a":2},
   {"type":"Cause & effect","q":"When pressure along a fault finally releases, —","opts":["the tectonic plates stop moving","the ground vibrates and sends out seismic waves","a new fault is created underground"],"a":1}
 ],
 "match":[
   {"word":"tectonic","def":"relating to the large moving slabs of rock that make up Earth's crust","hint":"\"enormous slabs of rock called <b>tectonic</b> plates are constantly moving.\""},
   {"word":"fault","def":"a crack in Earth's crust where two plates meet","hint":"\"a crack in the crust forms, known as a <b>fault</b>.\""},
   {"word":"vibrate","def":"to shake rapidly back and forth","hint":"\"the ground begins to <b>vibrate</b>, sending energy racing outward.\""},
   {"word":"seismic","def":"relating to the energy waves produced by an earthquake","hint":"\"The energy travels as <b>seismic</b> waves.\""},
   {"word":"epicenter","def":"the point on the surface directly above where an earthquake begins","hint":"\"directly above where the earthquake starts underground is called the <b>epicenter</b>.\""},
   {"word":"magnitude","def":"the number that describes how powerful an earthquake is","hint":"\"The number given to describe the earthquake's power is its <b>magnitude</b>.\""}
 ],
 "bank":["tectonic","fault","vibrate","seismic","epicenter","magnitude","tremor","rupture"],
 "fills":[
   {"text":"The ___ plates that make up the crust are always moving.","a":"tectonic"},
   {"text":"A ___ is a crack in the Earth's crust where two plates meet.","a":"fault"},
   {"text":"Earthquakes cause the ground to ___ and shake.","a":"vibrate"},
   {"text":"___ waves carry earthquake energy through the ground.","a":"seismic"},
   {"text":"The ___ is the point on the surface above the earthquake's source.","a":"epicenter"},
   {"text":"A 7.0 ___ earthquake is much more powerful than a 4.0.","a":"magnitude"},
   {"text":"A small earthquake is sometimes called a ___.","a":"tremor"},
   {"text":"When a fault ___, stored energy is released all at once as an earthquake.","a":"rupture","challenge":True}
 ]
},
{
 "activityId":"rocks",
 "projectKey":"rocks",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"The Rock Cycle",
 "heroEmoji":"\U0001faa8","watermark":"\U0001f30b","pageTitle":"The Rock Cycle","diagramFile":"diagrams/rocks.svg",
 "win":"PERFECT, Amara! Solid as a rock! \U0001faa8",
 "cheer":"Rock on, Amara! \U0001f30b",
 "palette":{"primary":"#6d4c41","dark":"#4e342e","deep":"#3e2723","accent":"#a1887f","accentSoft":"#efebe9","cream":"#fdf6f2","bgTop":"#f8f0ed","bgBottom":"#f2e8e4","glow1":"#6d4c4122","glow2":"#3e272318"},
 "passageTitle":"The Rock Cycle",
 "passageHtml":
"<p>Rocks are not permanent — they are constantly changing. Deep underground, heat melts rock into a liquid called <span class=\"voc\">magma</span>. When magma rises and cools — either underground or after erupting as lava — it hardens into <span class=\"voc\">igneous</span> rock. This is how granite and basalt are formed. <span class=\"voc\">Erosion</span> then slowly breaks igneous rock into tiny pieces called sediment.</p>"
"<p>Over millions of years, layers of sediment pile up and are squeezed together to form <span class=\"voc\">sedimentary</span> rock, such as sandstone or limestone. If any rock is buried deep enough, the intense heat and pressure transforms it into <span class=\"voc\">metamorphic</span> rock. Marble and slate are examples. Eventually, metamorphic rock can melt back into magma, completing the cycle. Every rock contains tiny crystals called <span class=\"voc\">minerals</span>.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mainly about —","opts":["how to identify different rocks","the continuous cycle of rock formation and change","why volcanoes produce different kinds of lava"],"a":1},
   {"type":"Detail","q":"What is magma?","opts":["Liquid rock found deep underground","Rock formed when sediment is compressed","Rock changed by heat and pressure"],"a":0},
   {"type":"Vocabulary","q":"\"Igneous\" rock is rock that —","opts":["forms from compressed layers of sediment","forms when magma cools and hardens","forms when buried rock is squeezed by pressure"],"a":1},
   {"type":"Detail","q":"How does sedimentary rock form?","opts":["When magma cools on the Earth's surface","When layers of sediment are squeezed together over millions of years","When igneous rock is heated and squeezed"],"a":1},
   {"type":"Vocabulary","q":"\"Metamorphic\" rock has been changed by —","opts":["cooling from liquid magma","layers of sediment building up","intense heat and pressure deep underground"],"a":2},
   {"type":"Sequence","q":"Which is the correct order in the rock cycle?","opts":["Magma → igneous → sediment → sedimentary → metamorphic → magma","Sedimentary → igneous → metamorphic → magma","Metamorphic → sedimentary → igneous → magma"],"a":0}
 ],
 "match":[
   {"word":"magma","def":"molten liquid rock found deep beneath the Earth's surface","hint":"\"heat melts rock into a liquid called <b>magma</b>.\""},
   {"word":"igneous","def":"rock formed when magma or lava cools and hardens","hint":"\"it hardens into <b>igneous</b> rock.\""},
   {"word":"erosion","def":"the process of wearing away rock into smaller pieces","hint":"\"<b>Erosion</b> then slowly breaks igneous rock into tiny pieces.\""},
   {"word":"sedimentary","def":"rock formed when layers of sediment are compressed together","hint":"\"layers of sediment pile up and are squeezed together to form <b>sedimentary</b> rock.\""},
   {"word":"metamorphic","def":"rock that has been changed by intense heat and pressure","hint":"\"heat and pressure transforms it into <b>metamorphic</b> rock.\""},
   {"word":"minerals","def":"natural crystals that make up all rocks","hint":"\"Every rock contains tiny crystals called <b>minerals</b>.\""}
 ],
 "bank":["magma","igneous","erosion","sedimentary","metamorphic","minerals","lava","compaction"],
 "fills":[
   {"text":"Hot liquid rock underground is called ___.","a":"magma"},
   {"text":"Granite is an ___ rock formed from cooled magma.","a":"igneous"},
   {"text":"Wind and rain cause ___ that slowly wears rock away.","a":"erosion"},
   {"text":"Sandstone is a ___ rock made from pressed-together sand.","a":"sedimentary"},
   {"text":"Marble is a ___ rock created by heat and pressure.","a":"metamorphic"},
   {"text":"Rocks are made up of natural crystals called ___.","a":"minerals"},
   {"text":"When magma reaches the surface and flows out of a volcano, it is called ___.","a":"lava"},
   {"text":"The slow squeezing of sediment layers into solid rock is called ___.","a":"compaction","challenge":True}
 ]
},
{
 "activityId":"glaciers",
 "projectKey":"glaciers",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Glaciers",
 "heroEmoji":"\U0001f9ca","watermark":"❄️","pageTitle":"Glaciers","diagramFile":"diagrams/glaciers.svg",
 "win":"PERFECT, Amara! Cool as a glacier! \U0001f9ca",
 "cheer":"Ice-cold brilliance, Amara! ❄️",
 "palette":{"primary":"#0277bd","dark":"#01579b","deep":"#003c6b","accent":"#4fc3f7","accentSoft":"#e1f5fe","cream":"#f2faff","bgTop":"#e8f5fe","bgBottom":"#daeefe","glow1":"#0277bd22","glow2":"#003c6b18"},
 "passageTitle":"Glaciers",
 "passageHtml":
"<p>A <span class=\"voc\">glacier</span> is a massive river of ice that moves very slowly across the land. Glaciers form in cold mountain regions or near the poles, where more snow falls each year than melts. Over time, the snow compresses into thick ice. Snow and ice continue to <span class=\"voc\">accumulate</span> in the upper zone of the glacier, making it heavier and causing it to inch forward under its own enormous weight.</p>"
"<p>As a glacier moves, it carves the landscape beneath it. The slow grinding action <span class=\"voc\">erodes</span> valleys into a distinctive U-shape. Rocks and soil picked up by the glacier are deposited at its edges as ridges called <span class=\"voc\">moraines</span>. Where the glacier melts fastest, in the lower <span class=\"voc\">ablation</span> zone, meltwater streams flow away. Deep cracks that form in the surface of the moving ice are called <span class=\"voc\">crevasses</span>.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mainly about?","opts":["how glaciers form and shape the land","why snow turns into ice in cold places","how to measure the speed of a glacier"],"a":0},
   {"type":"Detail","q":"Where do glaciers form?","opts":["In warm tropical rainforests","In cold regions where snow builds up faster than it melts","Along flat river banks near the ocean"],"a":1},
   {"type":"Vocabulary","q":"To \"accumulate\" means to —","opts":["melt and flow away","build up gradually over time","carve a valley into the rock"],"a":1},
   {"type":"Detail","q":"What shape does a glacier carve into a valley?","opts":["V-shaped","Flat","U-shaped"],"a":2},
   {"type":"Vocabulary","q":"A \"moraine\" is —","opts":["a deep crack in the ice","a ridge of rocks and soil deposited by a glacier","the lower melting zone of a glacier"],"a":1},
   {"type":"Cause & effect","q":"As the glacier moves and grinds along, it —","opts":["smooths the rock into a flat plain","erodes the land into a U-shaped valley","creates warm springs below the ice"],"a":1}
 ],
 "match":[
   {"word":"glacier","def":"a massive slow-moving river of ice","hint":"\"A <b>glacier</b> is a massive river of ice that moves very slowly across the land.\""},
   {"word":"accumulate","def":"to build up gradually over time","hint":"\"Snow and ice continue to <b>accumulate</b> in the upper zone.\""},
   {"word":"erodes","def":"wears away rock and soil by grinding","hint":"\"The slow grinding action <b>erodes</b> valleys into a distinctive U-shape.\""},
   {"word":"moraines","def":"ridges of rocks and soil deposited along the edges of a glacier","hint":"\"Rocks and soil picked up by the glacier are deposited at its edges as ridges called <b>moraines</b>.\""},
   {"word":"ablation","def":"the zone of a glacier where ice melts and is lost","hint":"\"in the lower <b>ablation</b> zone, meltwater streams flow away.\""},
   {"word":"crevasses","def":"deep cracks in the surface of a glacier","hint":"\"Deep cracks that form in the surface of the moving ice are called <b>crevasses</b>.\""}
 ],
 "bank":["glacier","accumulate","erodes","moraines","ablation","crevasses","fjord","iceberg"],
 "fills":[
   {"text":"A ___ is a huge slow-moving mass of ice.","a":"glacier"},
   {"text":"Snow and ice ___ in the upper part of the glacier.","a":"accumulate"},
   {"text":"The moving glacier ___ the valley below it into a U-shape.","a":"erodes"},
   {"text":"A ridge of rocks left at the edge of a glacier is called a ___.","a":"moraines"},
   {"text":"The lower melting zone of a glacier is called the ___ zone.","a":"ablation"},
   {"text":"Deep cracks in the glacier's surface are called ___.","a":"crevasses"},
   {"text":"When a glacier reaches the sea, large chunks break off as ___.","a":"iceberg"},
   {"text":"A long narrow sea inlet carved by a glacier is called a ___.","a":"fjord","challenge":True}
 ]
},
{
 "activityId":"erosion",
 "projectKey":"erosion",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Weathering and Erosion",
 "heroEmoji":"\U0001f3d4️","watermark":"\U0001f30a","pageTitle":"Weathering and Erosion","diagramFile":"diagrams/erosion.svg",
 "win":"PERFECT, Amara! Solid geology! \U0001f3d4️",
 "cheer":"You wore that quiz away, Amara! \U0001f30a",
 "palette":{"primary":"#8d6e63","dark":"#6d4c41","deep":"#4e342e","accent":"#bcaaa4","accentSoft":"#efebe9","cream":"#fdf8f6","bgTop":"#f8f0ed","bgBottom":"#f2e8e4","glow1":"#8d6e6322","glow2":"#4e342e18"},
 "passageTitle":"Weathering and Erosion",
 "passageHtml":
"<p><span class=\"voc\">Weathering</span> is the process that breaks rocks into smaller pieces over time. Rain, frost, heat, and plant roots all act as agents that crack and crumble rock. The tiny broken pieces are called <span class=\"voc\">sediment</span>. Once the rock is broken down, <span class=\"voc\">erosion</span> takes over — it is the process of carrying that sediment away. Water, wind, and ice are the main agents of erosion, and they move sediment from one place to another.</p>"
"<p>Over millions of years, erosion can create dramatic landforms. The Colorado River carved the Grand <span class=\"voc\">Canyon</span> by slowly cutting through layers of rock. When moving water slows down, it can no longer carry its load and the sediment <span class=\"voc\">deposits</span> on the riverbed or shoreline. This creates landforms such as beaches and river deltas. The scratch marks left on rock surfaces by moving particles are evidence of a process called <span class=\"voc\">abrasion</span>.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mainly about —","opts":["how the Grand Canyon was formed","how rocks break down and are carried away","why rivers always flow toward the sea"],"a":1},
   {"type":"Vocabulary","q":"\"Weathering\" is —","opts":["the movement of broken rock from one place to another","the process that breaks rock into smaller pieces","the layer of rock found just below the soil"],"a":1},
   {"type":"Vocabulary","q":"\"Erosion\" is —","opts":["breaking rock into small pieces","the carried-away deposit of sediment","the process of moving broken rock from place to place"],"a":2},
   {"type":"Detail","q":"What are the three main agents of erosion?","opts":["Rain, frost, and plant roots","Water, wind, and ice","Heat, cold, and acid rain"],"a":1},
   {"type":"Cause & effect","q":"When moving water slows down, it —","opts":["picks up more sediment from the riverbed","deposits the sediment it was carrying","cuts deeper into the rock below it"],"a":1},
   {"type":"Vocabulary","q":"\"Abrasion\" refers to —","opts":["the building up of sediment layers","the depositing of sand on a beach","the scratching of rock surfaces by moving particles"],"a":2}
 ],
 "match":[
   {"word":"weathering","def":"the breaking down of rock into smaller pieces by natural forces","hint":"\"<b>Weathering</b> is the process that breaks rocks into smaller pieces over time.\""},
   {"word":"sediment","def":"tiny pieces of broken-down rock","hint":"\"The tiny broken pieces are called <b>sediment</b>.\""},
   {"word":"erosion","def":"the process of carrying sediment away from where it formed","hint":"\"<b>erosion</b> takes over — it is the process of carrying that sediment away.\""},
   {"word":"canyon","def":"a deep valley with steep sides carved by a river","hint":"\"The Colorado River carved the Grand <b>Canyon</b>.\""},
   {"word":"deposits","def":"drops and leaves behind sediment in a new place","hint":"\"the sediment <b>deposits</b> on the riverbed or shoreline.\""},
   {"word":"abrasion","def":"the scratching and wearing of rock by moving particles","hint":"\"scratch marks left on rock surfaces by moving particles are evidence of a process called <b>abrasion</b>.\""}
 ],
 "bank":["weathering","sediment","erosion","canyon","deposits","abrasion","delta","agent"],
 "fills":[
   {"text":"Rain and frost cause ___ that slowly breaks rock apart.","a":"weathering"},
   {"text":"Broken pieces of rock are called ___.","a":"sediment"},
   {"text":"Water and wind carry sediment away in a process called ___.","a":"erosion"},
   {"text":"The Grand ___ was carved by the Colorado River over millions of years.","a":"canyon"},
   {"text":"When a river slows, it ___ its sediment on the riverbed.","a":"deposits"},
   {"text":"Wind, water, and ice are the main ___ of erosion.","a":"agent"},
   {"text":"A fan-shaped landform at the mouth of a river is called a ___.","a":"delta"},
   {"text":"The scratching of rock surfaces by moving sand is called ___.","a":"abrasion","challenge":True}
 ]
},
{
 "activityId":"atmosphere",
 "projectKey":"atmosphere",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Layers of the Atmosphere",
 "heroEmoji":"\U0001f30f","watermark":"☁️","pageTitle":"Layers of the Atmosphere","diagramFile":"diagrams/atmosphere.svg",
 "win":"PERFECT, Amara! Sky-high score! \U0001f30f",
 "cheer":"You rose above every question! ☁️",
 "palette":{"primary":"#1e88e5","dark":"#1565c0","deep":"#0d47a1","accent":"#64b5f6","accentSoft":"#e3f2fd","cream":"#f0f8ff","bgTop":"#e8f4ff","bgBottom":"#daeaff","glow1":"#1e88e522","glow2":"#0d47a118"},
 "passageTitle":"Layers of the Atmosphere",
 "passageHtml":
"<p>Earth is surrounded by a blanket of air called the <span class=\"voc\">atmosphere</span>. It is divided into distinct layers. The lowest layer, the <span class=\"voc\">troposphere</span>, extends from the ground to about 12 kilometres high. This is where all weather — rain, wind, snow, and clouds — takes place, and where we breathe. Above it is the <span class=\"voc\">stratosphere</span>, which contains the all-important <span class=\"voc\">ozone</span> layer. Ozone absorbs most of the Sun's harmful ultraviolet rays, protecting all life on Earth.</p>"
"<p>Higher still is the mesosphere, where most <span class=\"voc\">meteors</span> from space burn up before reaching the ground. Above that is the thermosphere, an extremely hot but very thin layer. Beautiful light shows called <span class=\"voc\">auroras</span> — shimmering green and pink curtains of light — occur in the thermosphere near the poles. The outermost layer, the exosphere, blends gradually into the emptiness of outer space. Without the atmosphere, life on Earth would be impossible.</p>",
 "questions":[
   {"type":"Main idea","q":"What is the passage mostly about?","opts":["why the sky looks blue from the ground","the different layers of Earth's atmosphere and what happens in each","how scientists measure the height of the atmosphere"],"a":1},
   {"type":"Detail","q":"In which layer does all weather take place?","opts":["Stratosphere","Troposphere","Mesosphere"],"a":1},
   {"type":"Vocabulary","q":"The \"ozone\" layer is important because it —","opts":["is where weather forms","absorbs the Sun's harmful ultraviolet rays","is where meteors burn up"],"a":1},
   {"type":"Detail","q":"What happens to most meteors in the mesosphere?","opts":["They orbit the Earth","They burn up before reaching the ground","They cool down and float back into space"],"a":1},
   {"type":"Vocabulary","q":"\"Auroras\" are —","opts":["dangerous ultraviolet rays that reach Earth","beautiful coloured light shows in the thermosphere near the poles","clouds of ice crystals high in the stratosphere"],"a":1},
   {"type":"Inference","q":"Why would life on Earth be impossible without the atmosphere?","opts":["There would be no gravity to keep us on the ground","There would be no rain, no breathable air, and no protection from UV rays","The oceans would not have any water in them"],"a":1}
 ],
 "match":[
   {"word":"atmosphere","def":"the blanket of air surrounding the Earth","hint":"\"Earth is surrounded by a blanket of air called the <b>atmosphere</b>.\""},
   {"word":"troposphere","def":"the lowest layer of the atmosphere, where weather happens","hint":"\"The lowest layer, the <b>troposphere</b>, extends from the ground to about 12 kilometres high.\""},
   {"word":"stratosphere","def":"the layer above the troposphere that contains the ozone layer","hint":"\"Above it is the <b>stratosphere</b>, which contains the all-important ozone layer.\""},
   {"word":"ozone","def":"a gas in the stratosphere that absorbs harmful UV rays","hint":"\"the all-important <b>ozone</b> layer. Ozone absorbs most of the Sun's harmful ultraviolet rays.\""},
   {"word":"meteors","def":"pieces of rock from space that burn up as they enter the atmosphere","hint":"\"where most <b>meteors</b> from space burn up before reaching the ground.\""},
   {"word":"auroras","def":"colourful light displays in the thermosphere near the poles","hint":"\"Beautiful light shows called <b>auroras</b> — shimmering green and pink curtains of light.\""}
 ],
 "bank":["atmosphere","troposphere","stratosphere","ozone","meteors","auroras","exosphere","mesosphere"],
 "fills":[
   {"text":"The blanket of air around our planet is called the ___.","a":"atmosphere"},
   {"text":"Rain, clouds, and wind all occur in the ___.","a":"troposphere"},
   {"text":"The ___ sits above the troposphere and protects us from UV rays.","a":"stratosphere"},
   {"text":"The ___ layer absorbs most of the Sun's harmful radiation.","a":"ozone"},
   {"text":"Most ___ burn up in the mesosphere before hitting the ground.","a":"meteors"},
   {"text":"Beautiful coloured lights called ___ can be seen near the poles.","a":"auroras"},
   {"text":"Most ___ burn up before reaching Earth because of atmospheric friction.","a":"meteors"},
   {"text":"The outermost layer of the atmosphere is the ___.","a":"exosphere","challenge":True}
 ]
},
{
 "activityId":"whales",
 "projectKey":"whales",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Whales",
 "heroEmoji":"\U0001f40b","watermark":"\U0001f30a","pageTitle":"Whales","diagramFile":"diagrams/whales.svg",
 "win":"PERFECT, Amara! Whale of a score! \U0001f40b",
 "cheer":"Deep-dive brilliance, Amara! \U0001f30a",
 "palette":{"primary":"#1565c0","dark":"#0d47a1","deep":"#072f7a","accent":"#64b5f6","accentSoft":"#e3f2fd","cream":"#f0f8ff","bgTop":"#e3f2fd","bgBottom":"#d0e8fc","glow1":"#1565c022","glow2":"#072f7a18"},
 "passageTitle":"Whales",
 "passageHtml":
"<p>Whales are the largest animals on Earth, yet they are not fish — they are <span class=\"voc\">mammals</span>. Like all mammals, whales are warm-blooded and breathe air. They breathe through a <span class=\"voc\">blowhole</span>, a nostril on top of their head, and must surface regularly. There are two main groups of whales. Toothed whales, such as the sperm whale, have teeth. Baleen whales, such as the blue whale, have rows of <span class=\"voc\">baleen</span> plates instead — these act like giant sieves, filtering tiny shrimp-like creatures called krill from the water.</p>"
"<p>Many toothed whales use a remarkable navigation skill called <span class=\"voc\">echolocation</span>. They send out clicks of sound that bounce off objects, telling the whale exactly where prey is hidden. Each year many whale species make enormous journeys between warm breeding waters and cold feeding waters — a seasonal movement called <span class=\"voc\">migration</span>. Whales often travel and hunt together in family groups called <span class=\"voc\">pods</span>. They communicate with each other using complex songs that can travel hundreds of kilometres through the ocean.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mostly about?","opts":["how whales are different from all other sea creatures","the biology and behaviour of whales","why blue whales are the largest animals on Earth"],"a":1},
   {"type":"Detail","q":"What makes whales mammals rather than fish?","opts":["They are very large and live in the ocean","They are warm-blooded, breathe air, and nurse their young","They have a blowhole instead of gills"],"a":1},
   {"type":"Vocabulary","q":"\"Baleen\" plates help a whale —","opts":["find prey using sound echoes","filter krill and small creatures out of the water","breathe air when it surfaces"],"a":1},
   {"type":"Vocabulary","q":"\"Echolocation\" is —","opts":["a type of underwater navigation using sound bouncing off objects","the seasonal journey whales make between warm and cold waters","the way whales breathe through their blowhole"],"a":0},
   {"type":"Detail","q":"What is a \"pod\"?","opts":["A whale's annual migration route","A family group of whales that travel together","The sound clicks a whale uses to find prey"],"a":1},
   {"type":"Cause & effect","q":"Baleen whales have baleen plates instead of teeth because —","opts":["their mouths are too small to catch fish","baleen plates allow them to filter huge amounts of tiny krill from the water","they lost their teeth through evolution and grew baleen instead"],"a":1}
 ],
 "match":[
   {"word":"mammals","def":"warm-blooded animals that breathe air and nurse their young with milk","hint":"\"they are not fish — they are <b>mammals</b>.\""},
   {"word":"blowhole","def":"the nostril on top of a whale's head used for breathing","hint":"\"They breathe through a <b>blowhole</b>, a nostril on top of their head.\""},
   {"word":"baleen","def":"comb-like plates in a whale's mouth used to filter food","hint":"\"have rows of <b>baleen</b> plates instead — these act like giant sieves.\""},
   {"word":"echolocation","def":"a navigation method using sound clicks that bounce off objects","hint":"\"a remarkable navigation skill called <b>echolocation</b>.\""},
   {"word":"migration","def":"the seasonal long-distance journey between feeding and breeding waters","hint":"\"a seasonal movement called <b>migration</b>.\""},
   {"word":"pods","def":"family groups of whales that travel and hunt together","hint":"\"Whales often travel and hunt together in family groups called <b>pods</b>.\""}
 ],
 "bank":["mammals","blowhole","baleen","echolocation","migration","pods","flukes","cetaceans"],
 "fills":[
   {"text":"Whales are ___, not fish — they breathe air and nurse their young.","a":"mammals"},
   {"text":"A whale surfaces to breathe through its ___.","a":"blowhole"},
   {"text":"Blue whales use ___ plates to filter krill from the ocean.","a":"baleen"},
   {"text":"Dolphins use ___ to find fish by sending out click sounds.","a":"echolocation"},
   {"text":"Whales make a long seasonal ___ between warm and cold waters.","a":"migration"},
   {"text":"Whales live and travel in family groups called ___.","a":"pods"},
   {"text":"A whale drives itself through water using its powerful tail ___.","a":"flukes"},
   {"text":"Whales, dolphins, and porpoises all belong to a group of mammals called ___.","a":"cetaceans","challenge":True}
 ]
},
{
 "activityId":"octopus",
 "projectKey":"octopus",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Octopuses",
 "heroEmoji":"\U0001f419","watermark":"\U0001f30a","pageTitle":"Octopuses","diagramFile":"diagrams/octopus.svg",
 "win":"PERFECT, Amara! Eight out of eight! \U0001f419",
 "cheer":"Ink-redible reading, Amara! \U0001f419",
 "palette":{"primary":"#7b1fa2","dark":"#6a1b9a","deep":"#4a148c","accent":"#ce93d8","accentSoft":"#f3e5f5","cream":"#fcf4ff","bgTop":"#f8eeff","bgBottom":"#f0e0ff","glow1":"#7b1fa222","glow2":"#4a148c18"},
 "passageTitle":"Octopuses",
 "passageHtml":
"<p>The octopus is one of the most intelligent invertebrates on Earth. Its round bag-like body is called the <span class=\"voc\">mantle</span>, and from it extend eight flexible arms covered in <span class=\"voc\">suckers</span>. These suckers can grip, taste, and smell at the same time. Octopuses are masters of <span class=\"voc\">camouflage</span> — they can change both the colour and texture of their skin in less than a second to blend perfectly with rocks, coral, or sandy seabeds.</p>"
"<p>Octopuses have three hearts and blue blood. When threatened, they can squirt a cloud of dark <span class=\"voc\">ink</span> to confuse a <span class=\"voc\">predator</span> and escape. Some species also produce mild <span class=\"voc\">venom</span> in their saliva to subdue prey. Despite having no bones, octopuses can squeeze through incredibly small gaps. They are highly intelligent animals that can solve puzzles, open jars, and even recognise individual human faces.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mostly about —","opts":["how to find an octopus on a coral reef","the body, abilities, and behaviour of octopuses","why octopuses have eight arms instead of six"],"a":1},
   {"type":"Detail","q":"What are the suckers on an octopus arm used for?","opts":["Only gripping prey","Gripping, tasting, and smelling simultaneously","Producing the ink cloud that escapes predators"],"a":1},
   {"type":"Vocabulary","q":"\"Camouflage\" means —","opts":["the ability to change colour and texture to blend into surroundings","the dark ink squirted to confuse predators","the bag-like body that holds the octopus's organs"],"a":0},
   {"type":"Detail","q":"How does an octopus escape from a predator?","opts":["By biting with sharp teeth","By squirting a cloud of dark ink","By changing colour so the predator cannot see it"],"a":1},
   {"type":"Vocabulary","q":"\"Venom\" is —","opts":["the ink an octopus squirts","a poisonous substance in the octopus's saliva","the rubbery skin that helps the octopus grip"],"a":1},
   {"type":"Inference","q":"Octopuses can \"squeeze through incredibly small gaps\" because —","opts":["their soft rubbery skin stretches out very thinly","they have no bones and their bodies are very flexible","they have suckers that help them pull themselves through openings"],"a":1}
 ],
 "match":[
   {"word":"mantle","def":"the round bag-like body of an octopus that holds its organs","hint":"\"Its round bag-like body is called the <b>mantle</b>.\""},
   {"word":"suckers","def":"the cup-shaped grips on an octopus arm used to grip, taste, and smell","hint":"\"eight flexible arms covered in <b>suckers</b>.\""},
   {"word":"camouflage","def":"the ability to change colour and texture to blend into surroundings","hint":"\"Octopuses are masters of <b>camouflage</b> — they can change both the colour and texture of their skin.\""},
   {"word":"ink","def":"the dark fluid an octopus squirts to confuse predators","hint":"\"they can squirt a cloud of dark <b>ink</b> to confuse a predator.\""},
   {"word":"predator","def":"an animal that hunts and eats other animals","hint":"\"squirt a cloud of dark ink to confuse a <b>predator</b> and escape.\""},
   {"word":"venom","def":"a mild poisonous substance some octopuses produce in their saliva","hint":"\"Some species also produce mild <b>venom</b> in their saliva.\""}
 ],
 "bank":["mantle","suckers","camouflage","ink","predator","venom","chromatophores","invertebrate"],
 "fills":[
   {"text":"The bag-like body of an octopus is called its ___.","a":"mantle"},
   {"text":"Each arm is covered in ___ that grip, taste, and smell.","a":"suckers"},
   {"text":"An octopus uses ___ to blend into the rocks and coral.","a":"camouflage"},
   {"text":"The octopus squirted a cloud of ___ to confuse the shark.","a":"ink"},
   {"text":"A shark is a ___ that might hunt an octopus.","a":"predator"},
   {"text":"Some octopuses have mild ___ in their saliva to subdue prey.","a":"venom"},
   {"text":"An octopus is an ___, meaning it has no backbone.","a":"invertebrate"},
   {"text":"The colour-changing skin cells of an octopus are called ___.","a":"chromatophores","challenge":True}
 ]
},
{
 "activityId":"coral",
 "projectKey":"coral",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Coral Reefs",
 "heroEmoji":"\U0001fab8","watermark":"\U0001f41f","pageTitle":"Coral Reefs","diagramFile":"diagrams/coral.svg",
 "win":"PERFECT, Amara! Reef champion! \U0001fab8",
 "cheer":"You dove deep and aced it! \U0001f41f",
 "palette":{"primary":"#e64a19","dark":"#bf360c","deep":"#870000","accent":"#ff8a65","accentSoft":"#fbe9e7","cream":"#fff9f8","bgTop":"#fff3f0","bgBottom":"#ffe8e2","glow1":"#e64a1922","glow2":"#87000018"},
 "passageTitle":"Coral Reefs",
 "passageHtml":
"<p>Coral reefs are sometimes called the rainforests of the sea because they are home to an enormous variety of life. A reef is built by tiny animals called <span class=\"voc\">polyps</span>. Each polyp creates a hard cup of calcium carbonate around itself. When polyps die, their hard skeletons remain, and new polyps grow on top. Over thousands of years, these skeletons build up into a massive <span class=\"voc\">reef</span> structure. Coral polyps have a special relationship with microscopic algae called zooxanthellae that live inside them — this is an example of <span class=\"voc\">symbiosis</span>, where two organisms live together and both benefit.</p>"
"<p>Coral reefs are one of the richest <span class=\"voc\">ecosystems</span> on Earth, providing food and shelter for a quarter of all ocean species. Sadly, rising ocean temperatures cause coral to expel the algae living inside them, turning the coral white in a process called <span class=\"voc\">bleaching</span>. Without the algae, the coral loses its food supply and can die. Pollution and overfishing put additional pressure on reefs. Scientists are working urgently to protect these fragile and vital <span class=\"voc\">habitats</span>.</p>",
 "questions":[
   {"type":"Main idea","q":"What is this passage mostly about?","opts":["how coral polyps produce their skeletons","what coral reefs are, how they form, and why they are under threat","why coral reefs are found only in warm tropical seas"],"a":1},
   {"type":"Detail","q":"What builds a coral reef?","opts":["Microscopic algae called zooxanthellae","Tiny animals called polyps that produce hard skeletons","Layers of sand and sediment on the ocean floor"],"a":1},
   {"type":"Vocabulary","q":"\"Symbiosis\" describes —","opts":["a relationship where two organisms live together and both benefit","the process of coral turning white due to rising temperatures","the hard calcium carbonate skeleton of a coral polyp"],"a":0},
   {"type":"Detail","q":"What fraction of all ocean species do coral reefs support?","opts":["Almost none — only coral lives there","About one half","About a quarter"],"a":2},
   {"type":"Vocabulary","q":"\"Bleaching\" happens when —","opts":["coral expels its algae due to warm water, turning white","a reef is damaged by fishing boats and turns pale","polyps produce extra calcium carbonate in cold water"],"a":0},
   {"type":"Inference","q":"Why is the loss of zooxanthellae algae fatal for coral?","opts":["The algae produce the hard skeleton the coral needs","The algae are the coral's food source, so losing them starves the coral","The algae keep the water temperature cool enough for coral"],"a":1}
 ],
 "match":[
   {"word":"polyps","def":"tiny animals whose skeletons build up to form a coral reef","hint":"\"A reef is built by tiny animals called <b>polyps</b>.\""},
   {"word":"reef","def":"the massive underwater structure built by generations of coral polyps","hint":"\"these skeletons build up into a massive <b>reef</b> structure.\""},
   {"word":"symbiosis","def":"a relationship where two different organisms live together and both benefit","hint":"\"this is an example of <b>symbiosis</b>, where two organisms live together and both benefit.\""},
   {"word":"ecosystems","def":"communities of living things interacting with their environment","hint":"\"Coral reefs are one of the richest <b>ecosystems</b> on Earth.\""},
   {"word":"bleaching","def":"the process where coral turns white after expelling its algae due to warm water","hint":"\"turning the coral white in a process called <b>bleaching</b>.\""},
   {"word":"habitats","def":"the natural environments where living things make their home","hint":"\"to protect these fragile and vital <b>habitats</b>.\""}
 ],
 "bank":["polyps","reef","symbiosis","ecosystems","bleaching","habitats","zooxanthellae","calcium"],
 "fills":[
   {"text":"Tiny animals called ___ build coral reefs from their hard skeletons.","a":"polyps"},
   {"text":"A coral ___ can take thousands of years to grow.","a":"reef"},
   {"text":"Coral and algae living together and both benefiting is an example of ___.","a":"symbiosis"},
   {"text":"Coral reefs are among the richest ___ on Earth.","a":"ecosystems"},
   {"text":"Coral ___ occurs when warm water makes the coral expel its algae.","a":"bleaching"},
   {"text":"Reefs are important ___ for about a quarter of all ocean species.","a":"habitats"},
   {"text":"The microscopic algae living inside coral are called ___.","a":"zooxanthellae"},
   {"text":"Coral polyps build their hard cups from a mineral called ___ carbonate.","a":"calcium","challenge":True}
 ]
},
{
 "activityId":"seaturtles",
 "projectKey":"seaturtles",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"Sea Turtles",
 "heroEmoji":"\U0001f422","watermark":"\U0001f30a","pageTitle":"Sea Turtles","diagramFile":"diagrams/seaturtles.svg",
 "win":"PERFECT, Amara! Shell yeah! \U0001f422",
 "cheer":"You swam through it perfectly! \U0001f30a",
 "palette":{"primary":"#2e7d32","dark":"#1b5e20","deep":"#0a3d0e","accent":"#81c784","accentSoft":"#e8f5e9","cream":"#f2fef3","bgTop":"#e8faf0","bgBottom":"#d8f5e6","glow1":"#2e7d3222","glow2":"#0a3d0e18"},
 "passageTitle":"Sea Turtles",
 "passageHtml":
"<p>Sea turtles have swum in Earth's oceans for over 100 million years, making them older than many dinosaurs. Their most recognisable feature is their hard protective shell, called a <span class=\"voc\">carapace</span>. Unlike land tortoises, sea turtles cannot pull their head or <span class=\"voc\">flippers</span> inside their shell. Their flippers are perfectly shaped for swimming — powerful enough to propel them thousands of kilometres across open ocean as they <span class=\"voc\">migrate</span> between feeding and nesting grounds.</p>"
"<p>Female sea turtles make a remarkable journey every few years, returning to the exact beach where they were born to lay their eggs. After digging a hole in the sand, the female lays up to 100 eggs. When the eggs hatch, tiny <span class=\"voc\">hatchlings</span> scramble toward the sea. Many are eaten by birds and crabs on the short journey. Sadly, all species of sea turtles are now either <span class=\"voc\">endangered</span> or threatened due to pollution, hunting, and loss of nesting beaches. Researchers use satellite tags to track their migrations and help with <span class=\"voc\">conservation</span> efforts.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mainly about —","opts":["why sea turtles live longer than most other reptiles","the biology, behaviour, and conservation of sea turtles","how sea turtle hatchlings survive the journey to the ocean"],"a":1},
   {"type":"Detail","q":"How long have sea turtles been on Earth?","opts":["About 10 million years","Over 100 million years","About 65 million years — since the time of the last dinosaurs"],"a":1},
   {"type":"Vocabulary","q":"The \"carapace\" is —","opts":["the flat shape of a sea turtle's flipper","the hard protective shell on a sea turtle's back","the beach where a female sea turtle lays her eggs"],"a":1},
   {"type":"Detail","q":"Why do female sea turtles return to the beach where they were born?","opts":["To find food in the shallow water","To lay their eggs in the same place they hatched","To meet other turtles for migration"],"a":1},
   {"type":"Vocabulary","q":"\"Endangered\" species are —","opts":["species that are very fast swimmers","species at risk of dying out completely","species that are protected by law"],"a":1},
   {"type":"Cause & effect","q":"Sea turtle numbers are falling because of —","opts":["competition with sharks and other large predators","natural changes to ocean currents and water temperature","pollution, hunting, and the destruction of nesting beaches"],"a":2}
 ],
 "match":[
   {"word":"carapace","def":"the hard protective shell on the back of a sea turtle","hint":"\"Their most recognisable feature is their hard protective shell, called a <b>carapace</b>.\""},
   {"word":"flippers","def":"the wide, paddle-shaped limbs sea turtles use to swim","hint":"\"sea turtles cannot pull their head or <b>flippers</b> inside their shell.\""},
   {"word":"migrate","def":"to travel long distances between feeding and nesting grounds","hint":"\"they <b>migrate</b> between feeding and nesting grounds.\""},
   {"word":"hatchlings","def":"baby turtles that have just emerged from their eggs","hint":"\"tiny <b>hatchlings</b> scramble toward the sea.\""},
   {"word":"endangered","def":"at serious risk of dying out if not protected","hint":"\"all species of sea turtles are now either <b>endangered</b> or threatened.\""},
   {"word":"conservation","def":"the effort to protect and preserve wildlife and habitats","hint":"\"Researchers use satellite tags to help with <b>conservation</b> efforts.\""}
 ],
 "bank":["carapace","flippers","migrate","hatchlings","endangered","conservation","nesting","reptiles"],
 "fills":[
   {"text":"The hard shell on a sea turtle's back is called its ___.","a":"carapace"},
   {"text":"Sea turtles use their broad ___ to swim powerfully through the ocean.","a":"flippers"},
   {"text":"Every few years, sea turtles ___ back to the beach where they were born.","a":"migrate"},
   {"text":"Tiny ___ scramble from the sand to the sea as soon as they hatch.","a":"hatchlings"},
   {"text":"All species of sea turtle are either ___ or threatened.","a":"endangered"},
   {"text":"Scientists use satellite tags to support sea turtle ___.","a":"conservation"},
   {"text":"Female sea turtles come ashore to find a ___ site on the beach.","a":"nesting"},
   {"text":"Sea turtles belong to the group of scaly air-breathing animals called ___.","a":"reptiles","challenge":True}
 ]
},
{
 "activityId":"deepsea",
 "projectKey":"deepsea",
 "name":"Amara","hubKey":"amaraReading","hubFile":"index.html",
 "useLead":"Choose the right word for each blank. Challenge question marked ★.",
 "title":"The Deep Sea",
 "heroEmoji":"\U0001f991","watermark":"🌊","pageTitle":"The Deep Sea","diagramFile":"diagrams/deepsea.svg",
 "win":"PERFECT, Amara! Fathoms deep! \U0001f991",
 "cheer":"You plunged to the bottom and came back! 🌊",
 "palette":{"primary":"#1a237e","dark":"#0d1b6e","deep":"#050d4a","accent":"#7986cb","accentSoft":"#e8eaf6","cream":"#f3f4fd","bgTop":"#eceeff","bgBottom":"#e0e4f8","glow1":"#1a237e22","glow2":"#050d4a18"},
 "passageTitle":"The Deep Sea",
 "passageHtml":
"<p>Below 200 metres, sunlight fades and the ocean grows completely dark. This is the deep sea, and it covers more than half of Earth's surface. The water <span class=\"voc\">pressure</span> at great depths is crushing — at the bottom of the Mariana Trench, the deepest known point on Earth, pressure is over 1,000 times greater than at the surface. Yet life still finds a way. Deep sea creatures have <span class=\"voc\">adapted</span> to survive in the cold, dark, and high-pressure environment in remarkable ways.</p>"
"<p>One extraordinary adaptation is <span class=\"voc\">bioluminescence</span> — the ability to produce light using chemical reactions in the body. The anglerfish dangles a glowing lure above its mouth to attract prey in the darkness. Other creatures use light to communicate or to confuse <span class=\"voc\">predators</span>. Near the ocean floor, hot water vents called hydrothermal vents release scorching minerals. Bacteria around these vents perform a process called <span class=\"voc\">chemosynthesis</span>, making food from chemicals instead of sunlight. These vents support entire food chains in the <span class=\"voc\">abyss</span>, completely independent of the sun.</p>",
 "questions":[
   {"type":"Main idea","q":"This passage is mainly about —","opts":["why the Mariana Trench is the deepest place on Earth","how life survives in the extreme conditions of the deep sea","how scientists build submarines to reach the ocean floor"],"a":1},
   {"type":"Detail","q":"At what depth does the deep sea begin?","opts":["Below 20 metres","Below 200 metres","Below 2,000 metres"],"a":1},
   {"type":"Vocabulary","q":"\"Bioluminescence\" is —","opts":["the ability of deep sea creatures to produce their own light","the crushing water pressure at the ocean floor","the process of making food from chemicals instead of sunlight"],"a":0},
   {"type":"Vocabulary","q":"\"Adapted\" means —","opts":["moved to a new part of the ocean","changed over time to suit the environment","hunted prey in complete darkness"],"a":1},
   {"type":"Detail","q":"What is \"chemosynthesis\"?","opts":["A way of producing light using chemicals","Making food from chemicals rather than from sunlight","A type of hunting used by anglerfish"],"a":1},
   {"type":"Inference","q":"The fact that life thrives around hydrothermal vents shows that —","opts":["all life on Earth ultimately depends on sunlight","some ecosystems can survive without any sunlight at all","the deep ocean is actually warmer than the surface"],"a":1}
 ],
 "match":[
   {"word":"pressure","def":"the crushing force exerted by deep water pressing down from above","hint":"\"The water <b>pressure</b> at great depths is crushing.\""},
   {"word":"adapted","def":"changed over time to be well-suited to a particular environment","hint":"\"Deep sea creatures have <b>adapted</b> to survive in the cold, dark, high-pressure environment.\""},
   {"word":"bioluminescence","def":"the ability of living things to produce their own light","hint":"\"One extraordinary adaptation is <b>bioluminescence</b> — the ability to produce light.\""},
   {"word":"predators","def":"animals that hunt and eat other animals","hint":"\"Other creatures use light to communicate or to confuse <b>predators</b>.\""},
   {"word":"chemosynthesis","def":"the process of making food using chemicals instead of sunlight","hint":"\"Bacteria around these vents perform a process called <b>chemosynthesis</b>.\""},
   {"word":"abyss","def":"the very deepest, darkest zone of the ocean","hint":"\"These vents support entire food chains in the <b>abyss</b>.\""}
 ],
 "bank":["pressure","adapted","bioluminescence","predators","chemosynthesis","abyss","hydrothermal","trench"],
 "fills":[
   {"text":"The crushing force of deep water is called ___.","a":"pressure"},
   {"text":"Deep sea creatures have ___ to survive extreme cold and darkness.","a":"adapted"},
   {"text":"Many deep sea animals use ___ to make their own glow in the dark.","a":"bioluminescence"},
   {"text":"The anglerfish uses its glowing lure to attract prey and confuse ___.","a":"predators"},
   {"text":"Bacteria near hot vents use ___ to make food from chemicals.","a":"chemosynthesis"},
   {"text":"The deepest, darkest zone of the ocean is called the ___.","a":"abyss"},
   {"text":"Hot water vents on the ocean floor are called ___ vents.","a":"hydrothermal"},
   {"text":"The deepest known point on Earth is in the Mariana ___.","a":"trench","challenge":True}
 ]
},

{"activityId":"anne-of-green-gables","projectKey":"anne","title":"Anne of Green Gables","heroEmoji":"🏡","watermark":"🌸","pageTitle":"Anne of Green Gables","diagramFile":"diagrams/anne-of-green-gables.svg",
 "win":"PERFECT, Amara! Anne would be proud! 🌸","cheer":"A truly kindred spirit of reading! 🌸",
 "palette":{"primary":"#b5451b","dark":"#8f3514","deep":"#5e220c","accent":"#e08a5f","accentSoft":"#f7e3d6","cream":"#fff8f3","bgTop":"#fbeee6","bgBottom":"#f5e2d5","glow1":"#b5451b22","glow2":"#5e220c18"},
 "passageTitle":"Anne of Green Gables",
 "passageHtml":"<p>Long ago, on the red dirt roads of Prince Edward Island, a shy old farmer named Matthew Cuthbert drove his buggy to the train station. He and his strict sister Marilla lived at a tidy farmhouse called Green Gables, named for the pointed <span class=\"voc\">gable</span>s at the top of its walls. Matthew and Marilla had decided to <span class=\"voc\">adopt</span> a boy from an orphanage to help with the heavy farm work. But when Matthew reached the station, no boy was anywhere in sight. Instead, a skinny eleven-year-old <span class=\"voc\">orphan</span> girl sat waiting on a pile of luggage, swinging her feet.</p><p>The girl's name was Anne Shirley, and she insisted that it be spelled with an \"e.\" She had two long braids of bright red hair and a small face covered in <span class=\"voc\">freckles</span>. From the very first minute, Anne never stopped talking — she was so <span class=\"voc\">talkative</span> that Matthew could barely fit in a word. She was also wonderfully <span class=\"voc\">imaginative</span>, giving pretty names to every pond and tree she passed, and so <span class=\"voc\">dramatic</span> that a single disappointment could feel like the end of the world. Marilla had planned to send the <span class=\"voc\">spirited</span> girl straight back, but Anne's warm heart and big dreams slowly won the Cuthberts over, and Green Gables became the loving home she had always longed for.</p>",
 "questions":[{"type":"Main idea","q":"What is this passage mostly about?","opts":["a farmer learning to drive a buggy","an orphan girl who comes to live at Green Gables","how to name the ponds and trees on a farm"],"a":1},{"type":"Setting","q":"Where does this story take place?","opts":["a busy city far across the sea","a farmhouse called Green Gables on Prince Edward Island","a school high in the mountains"],"a":1},{"type":"Character trait","q":"Which detail tells you how Anne LOOKS?","opts":["she has red braids and a freckled face","she is calm, quiet, and shy","she loves the heavy farm work"],"a":0},{"type":"Character trait","q":"Which words BEST describe Anne's personality?","opts":["lazy and silent","imaginative and talkative","cold and unkind"],"a":1},{"type":"Cause & effect","q":"Why were Matthew and Marilla surprised when Anne arrived?","opts":["they had asked for a boy, but a girl was sent instead","they did not want any children at all","the train had arrived far too early"],"a":0},{"type":"Inference","q":"What does Anne want most of all?","opts":["a place to belong and a family to love her","to leave Avonlea and never come back","a shiny new buggy of her own"],"a":0}],
 "match":[{"word":"orphan","def":"a child whose parents have died","hint":"\"…a skinny eleven-year-old <b>orphan</b> girl sat waiting on a pile of luggage.\""},{"word":"gable","def":"the triangle-shaped part of a wall beneath a sloping roof","hint":"\"…named for the pointed <b>gable</b>s at the top of its walls.\""},{"word":"freckles","def":"small light-brown spots on the skin","hint":"\"…a small face covered in <b>freckles</b>.\""},{"word":"imaginative","def":"good at inventing pictures and ideas in the mind","hint":"\"She was also wonderfully <b>imaginative</b>, giving pretty names to every pond and tree…\""},{"word":"dramatic","def":"showing feelings in a big, theatrical way","hint":"\"…so <b>dramatic</b> that a single disappointment could feel like the end of the world.\""},{"word":"spirited","def":"full of lively energy and strong feeling","hint":"\"Marilla had planned to send the <b>spirited</b> girl straight back…\""}],
 "bank":["orphan","gable","freckles","imaginative","dramatic","spirited","talkative","adopt"],
 "fills":[{"text":"A child whose parents have died is called an ___.","a":"orphan"},{"text":"The house was named for the pointed ___ at the top of its walls.","a":"gable"},{"text":"The summer sun sprinkled light-brown ___ across her nose.","a":"freckles"},{"text":"Anne was so ___ that she gave a name to every tree and pond.","a":"imaginative"},{"text":"He was so ___ that he threw up his arms and wailed at the news.","a":"dramatic"},{"text":"The ___ pony kicked and galloped with wild energy.","a":"spirited"},{"text":"The Cuthberts decided to ___ a child and raise her as their own.","a":"adopt"},{"text":"The parrot was so ___ that it repeated every single word we said.","a":"talkative","challenge":True}]},

{"activityId":"anne-diana","projectKey":"diana","title":"Anne &amp; Diana: Bosom Friends","heroEmoji":"👭","watermark":"🍒","pageTitle":"Anne and Diana","diagramFile":"diagrams/anne-diana.svg",
 "win":"PERFECT, Amara! A true bosom friend! 🍒","cheer":"Kindred spirits think alike — brilliant! 🍒",
 "palette":{"primary":"#b12a54","dark":"#8c1f41","deep":"#5e142b","accent":"#e07a9c","accentSoft":"#f8dde6","cream":"#fff6f9","bgTop":"#fbe9ef","bgBottom":"#f5dbe4","glow1":"#b12a5422","glow2":"#5e142b18"},
 "passageTitle":"Anne and Diana: Bosom Friends",
 "passageHtml":"<p>From the moment they met, Anne Shirley and Diana Barry became what Anne called <span class=\"voc\">kindred</span> spirits — two people whose hearts understand each other without needing to explain. Anne had spent her whole life longing for a \"bosom friend,\" and in Diana she found one at last. They wandered the woods together, invented secret clubs, and <span class=\"voc\">vowed</span> eternal loyalty beneath the blossoming trees.</p><p>One afternoon, Marilla gave Anne permission to invite Diana to tea. Feeling wonderfully grown-up, Anne poured her friend glass after glass of what she believed was raspberry <span class=\"voc\">cordial</span>. In truth, she had mistaken Marilla's homemade currant wine for the sweet drink, and poor Diana went home dizzy and ill. Diana's mother was furious. Believing Anne had behaved disgracefully, Mrs. Barry <span class=\"voc\">forbade</span> the two girls from ever playing together again. Anne was utterly <span class=\"voc\">mortified</span>, and she wept with genuine <span class=\"voc\">remorse</span>, for she had never meant to cause any harm.</p><p>Weeks later, on a bitter winter night, Diana came pounding at the door of Green Gables in a panic: her baby sister, Minnie May, was choking with croup while the grown-ups were far away. Anne, who had once helped nurse sick children, worked without rest until dawn to save the little girl's life. Her steady <span class=\"voc\">devotion</span> impressed even the doctor. When Mrs. Barry heard how Anne had saved her daughter, her anger melted, and she allowed the friends to <span class=\"voc\">reconcile</span> at last. Their friendship, tested and proven, grew stronger than ever.</p>",
 "questions":[{"type":"Figurative language","q":"When Anne calls Diana a \"kindred spirit,\" she means that they —","opts":["look almost exactly alike","understand each other deeply, as if their hearts match","are cousins in the same family"],"a":1},{"type":"Character motivation","q":"Why did Anne serve Diana the currant wine?","opts":["she wanted to make Diana ill","she mistook it for sweet raspberry cordial","Marilla had ordered her to"],"a":1},{"type":"Cause &amp; effect","q":"Why did Mrs. Barry forbid the friendship?","opts":["she believed Anne had disgracefully made Diana drunk","the girls had been too noisy at tea","Anne had broken one of her windows"],"a":0},{"type":"Plot structure","q":"Which event is the turning point that finally repairs the friendship?","opts":["the quiet tea party","Anne saving Minnie May from croup","the secret club in the woods"],"a":1},{"type":"Inference","q":"The fact that the doctor was impressed by Anne suggests that she —","opts":["was only pretending to be helpful","acted with real skill and courage","was far too young to be of any use"],"a":1},{"type":"Theme","q":"What lesson about friendship does this story most clearly show?","opts":["true friendship can survive mistakes and grow stronger","real friends must never once disagree","it is wiser to have many friends than one close friend"],"a":0}],
 "match":[{"word":"kindred","def":"so alike in spirit that you understand each other deeply","hint":"\"…what Anne called <b>kindred</b> spirits — two people whose hearts understand each other.\""},{"word":"cordial","def":"a sweet fruit-flavoured drink","hint":"\"…what she believed was raspberry <b>cordial</b>.\""},{"word":"mortified","def":"filled with deep shame or embarrassment","hint":"\"Anne was utterly <b>mortified</b>…\""},{"word":"remorse","def":"a strong feeling of regret for having done wrong","hint":"\"…she wept with genuine <b>remorse</b>…\""},{"word":"devotion","def":"great loyalty, love, and dedication","hint":"\"Her steady <b>devotion</b> impressed even the doctor.\""},{"word":"reconcile","def":"to become friendly again after a quarrel","hint":"\"…allowed the friends to <b>reconcile</b> at last.\""}],
 "bank":["kindred","cordial","mortified","remorse","devotion","reconcile","forbade","vowed"],
 "fills":[{"text":"Two friends who understand each other deeply are called ___ spirits.","a":"kindred"},{"text":"Anne poured a tall glass of sweet raspberry ___.","a":"cordial"},{"text":"She was ___ when she realised her mistake in front of everyone.","a":"mortified"},{"text":"He felt deep ___ after breaking his sister's toy on purpose.","a":"remorse"},{"text":"The nurse cared for her patients with tireless ___.","a":"devotion"},{"text":"After their quarrel, the two brothers finally agreed to ___.","a":"reconcile"},{"text":"Her father ___ her from staying out after dark.","a":"forbade"},{"text":"The knight ___ to protect the kingdom with his very life.","a":"vowed","challenge":True}]},

{"activityId":"anne-gilbert","projectKey":"gilbert","title":"Anne &amp; Gilbert: Rivals to Friends","heroEmoji":"🎓","watermark":"📖","pageTitle":"Anne and Gilbert","diagramFile":"diagrams/anne-gilbert.svg",
 "win":"PERFECT, Amara! Top of the class! 🎓","cheer":"A rival in reading? Never — you win! 🎓",
 "palette":{"primary":"#0f766e","dark":"#0b574f","deep":"#063a34","accent":"#5eb8ac","accentSoft":"#d5efeb","cream":"#f2fbf9","bgTop":"#e7f5f2","bgBottom":"#dbeeea","glow1":"#0f766e22","glow2":"#063a3418"},
 "passageTitle":"Anne and Gilbert: Rivals to Friends",
 "passageHtml":"<p>On Anne's first day at the Avonlea school, a clever, good-looking boy named Gilbert Blythe tried to get her attention by tugging her red braid and whispering, \"Carrots!\" Anne, deeply sensitive about her hair, was <span class=\"voc\">indignant</span>. In a flash of temper she brought her writing slate down on his head, cracking it in two. Gilbert apologised at once, but Anne, proud and <span class=\"voc\">obstinate</span>, refused to forgive him. She nursed her <span class=\"voc\">grudge</span> for years, treating Gilbert as a sworn <span class=\"voc\">rival</span> rather than a friend.</p><p>That rivalry, however, had an unexpected result. Determined never to let Gilbert beat her, Anne studied harder than anyone in Avonlea. The two became the top students in the school, forever trading first place in spelling, mathematics, and composition. Anne's fierce <span class=\"voc\">ambition</span> carried her all the way to Queen's Academy, where she won a prized scholarship for university. Yet even as she succeeded, she was slowly <span class=\"voc\">humbled</span> by loss and hardship, and her old pride began to soften.</p><p>When Matthew died and Marilla's eyesight began to fail, Anne gave up her university scholarship to stay and care for the woman who had raised her. Gilbert, who had been offered the teaching post at the Avonlea school, quietly made a <span class=\"voc\">sacrifice</span> of his own: he stepped aside so that Anne could teach close to home. Touched by this <span class=\"voc\">gracious</span> act, Anne finally let go of her grudge. The two old rivals became friends at last — the beginning of one of literature's most beloved friendships.</p>",
 "questions":[{"type":"Character motivation","q":"Why did Gilbert call Anne \"Carrots\"?","opts":["to insult her whole family","to get the attention of a girl he found interesting","because he truly disliked her"],"a":1},{"type":"Cause &amp; effect","q":"What did Anne's grudge against Gilbert unexpectedly cause?","opts":["her to leave the school for good","her to study harder and become a top student","Gilbert to move far away"],"a":1},{"type":"Character trait","q":"Anne refusing for years to forgive Gilbert shows that she can be —","opts":["lazy and careless","proud and obstinate","shy and silent"],"a":1},{"type":"Inference","q":"Anne giving up her scholarship to care for Marilla shows that she —","opts":["no longer cared about learning at all","valued love and loyalty above her own ambition","was forced to stay against her will"],"a":1},{"type":"Character change","q":"How does Anne change by the end of the story?","opts":["she grows prouder and angrier than before","her pride softens and she learns to forgive","she forgets everything she studied"],"a":1},{"type":"Theme","q":"Which theme does the story of Anne and Gilbert best express?","opts":["pride can keep us apart, but people can grow and forgive","it is important to always win at any cost","a rival can never be trusted"],"a":0}],
 "match":[{"word":"indignant","def":"angry because something feels unfair","hint":"\"Anne, deeply sensitive about her hair, was <b>indignant</b>.\""},{"word":"obstinate","def":"stubbornly refusing to change your mind","hint":"\"…but Anne, proud and <b>obstinate</b>, refused to forgive him.\""},{"word":"grudge","def":"a lasting feeling of anger over an old wrong","hint":"\"She nursed her <b>grudge</b> for years…\""},{"word":"rival","def":"a person you compete against","hint":"\"…treating Gilbert as a sworn <b>rival</b> rather than a friend.\""},{"word":"ambition","def":"a strong desire to achieve something great","hint":"\"Anne's fierce <b>ambition</b> carried her all the way to Queen's Academy.\""},{"word":"gracious","def":"kind, generous, and thoughtful toward others","hint":"\"Touched by this <b>gracious</b> act, Anne finally let go of her grudge.\""}],
 "bank":["indignant","obstinate","grudge","rival","ambition","gracious","humbled","sacrifice"],
 "fills":[{"text":"She was ___ when the referee made an unfair call against her team.","a":"indignant"},{"text":"The ___ child refused to wear his coat no matter what anyone said.","a":"obstinate"},{"text":"Even years later, he still held a ___ against his old teammate.","a":"grudge"},{"text":"The two chess players were each other's greatest ___.","a":"rival"},{"text":"Her ___ was to become the first doctor in her family.","a":"ambition"},{"text":"It was ___ of the winner to praise everyone she had defeated.","a":"gracious"},{"text":"The proud champion was ___ by his surprising defeat.","a":"humbled"},{"text":"The firefighter's brave ___ saved the whole family's lives.","a":"sacrifice","challenge":True}]}

]

DEFAULT_USE_LEAD = ("Tap a word to drop it in the blank you've selected, or just type it. "
                    "One sentence is a tricky <span style=\"color:var(--amber);font-weight:800\">\u2605 challenge</span> in a different context!")

OUT=os.environ.get("OUT_DIR") or os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT,exist_ok=True)
paths=[]
for m in MODULES:
    data={"activityId":m["activityId"],"projectKey":m["projectKey"],"title":m["title"],
          "questions":m["questions"],"match":m["match"],"bank":m["bank"],"fills":m["fills"],
          "win":m["win"],"cheer":m["cheer"],
          "name":m.get("name","Amara"),"hubKey":m.get("hubKey","amaraReading")}
    html=(TEMPLATE
      .replace("%%PAGE_TITLE%%",m["pageTitle"])
      .replace("%%CSSVARS%%",cssvars(m["palette"]))
      .replace("%%WATERMARK%%",m["watermark"])
      .replace("%%HERO_EMOJI%%",m["heroEmoji"])
      .replace("%%DIAGRAM_FILE%%",m.get("diagramFile","diagrams/watercycle.svg"))
      .replace("%%HERO_TITLE%%",m["title"])
      .replace("%%SUBJECT_NAME%%",m.get("name","Amara"))
      .replace("%%HUB_FILE%%",m.get("hubFile","index.html"))
      .replace("%%USE_LEAD%%",m.get("useLead",DEFAULT_USE_LEAD))
      .replace("%%PASSAGE_TITLE%%",m["passageTitle"])
      .replace("%%PASSAGE_HTML%%",m["passageHtml"])
      .replace("%%MODULE_JSON%%",json.dumps(data,ensure_ascii=False)))
    fn=OUT+"/amara-"+m["activityId"]+"-reading.html" if m.get("name","Amara")=="Amara" else OUT+"/dani-"+m["activityId"]+"-reading.html"
    with open(fn,"w",encoding="utf-8") as f: f.write(html)
    paths.append(fn)
    print("wrote",fn,len(html),"bytes")
print("DONE")
