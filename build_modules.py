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
  .passage-wrap{display:flex;gap:18px;align-items:flex-start}
  .topic-img{flex:0 0 110px;background:var(--c-accent-soft);border:2px solid #00000010;border-radius:16px;padding:18px 10px 14px;text-align:center}
  .topic-emoji{font-size:54px;line-height:1;display:block;margin-bottom:8px}
  .topic-label{font-size:10px;font-weight:800;color:var(--c-deep);text-transform:uppercase;letter-spacing:.06em;line-height:1.3}
  .passage-text{flex:1;min-width:0}
  .passage h3{margin:0 0 10px;font-family:'Fredoka',sans-serif;color:var(--c-deep)}
  .passage p{margin:0 0 14px}
  .passage p:last-child{margin-bottom:0}
  @media(max-width:560px){.passage-wrap{flex-direction:column}.topic-img{display:flex;align-items:center;gap:14px;width:100%;flex:none;padding:12px 16px}.topic-emoji{font-size:42px;margin:0}.topic-label{font-size:11px;text-align:left}}
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
      <div class="passage-wrap">
        <div class="topic-img">
          <span class="topic-emoji">%%HERO_EMOJI%%</span>
          <div class="topic-label">%%PASSAGE_TITLE%%</div>
        </div>
        <div class="passage-text">
          <h3>%%PASSAGE_TITLE%%</h3>
          %%PASSAGE_HTML%%
        </div>
      </div>
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
 "heroEmoji":"🐆","watermark":"🌿","pageTitle":"Animals of the Rainforest",
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
 "heroEmoji":"🧠","watermark":"💭","pageTitle":"Emotional Intelligence",
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
 "heroEmoji":"🍝","watermark":"🍅","pageTitle":"How Spaghetti Is Made",
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
 "heroEmoji":"🎉","watermark":"🎊","pageTitle":"Celebrations Around the World",
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
 "heroEmoji":"🐕","watermark":"🐾","pageTitle":"All About Dogs",
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
 "heroEmoji":"🐍","watermark":"🐍","pageTitle":"Boa Constrictors",
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
 "heroEmoji":"🛞","watermark":"⚙️","pageTitle":"The Importance of the Wheel",
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
 "heroEmoji":"👗","watermark":"🧵","pageTitle":"Fashion History",
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
 "heroEmoji":"🎮","watermark":"🕹️","pageTitle":"Roblox",
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
 "heroEmoji":"🐩","watermark":"🐩","pageTitle":"Types of Poodles",
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
 "heroEmoji":"👗","watermark":"🧥","pageTitle":"Fashion and Clothing",
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

{"activityId":"volcano","projectKey":"volcano","title":"Volcanoes","heroEmoji":"🌋","watermark":"🌋","pageTitle":"Volcanoes",
 "win":"PERFECT, Amara! Red hot! 🌋","cheer":"Your reading is on fire! 🌋",
 "palette":{"primary":"#e8590c","dark":"#b8460a","deep":"#7d2f06","accent":"#f4a06a","accentSoft":"#fde4d4","cream":"#fff7f1","bgTop":"#fdf1e9","bgBottom":"#f8e6d8","glow1":"#e8590c22","glow2":"#7d2f0618"},
 "passageTitle":"Volcanoes",
 "passageHtml":"<p>Deep beneath the Earth's surface, it is so hot that rock melts into a thick, glowing liquid called <span class=\"voc\">magma</span>. A volcano is an opening in the ground where this melted rock can reach the surface. When pressure builds up, a volcano can <span class=\"voc\">erupt</span>, sending magma, gas, and <span class=\"voc\">ash</span> bursting out. Once the magma flows onto the surface it is called <span class=\"voc\">lava</span>. Lava is <span class=\"voc\">molten</span>, which means melted by heat, and it can be hotter than 1,000 degrees. As the lava cools, it hardens into new rock.</p><p>Most volcanoes have a bowl-shaped opening at the top called a <span class=\"voc\">crater</span>, and the channel that magma travels up is called a <span class=\"voc\">vent</span>. Not all volcanoes erupt often. A volcano that has not erupted for a long time but still could is called <span class=\"voc\">dormant</span>, like a sleeping giant. Volcanoes can be dangerous, but they also build new islands and rich soil. Over millions of years, they have helped shape the surface of our planet.</p>",
 "questions":[{"type":"Main idea","q":"What is this passage mostly about?","opts":["How to climb a mountain","How volcanoes work and what they do","Why rocks are grey"],"a":1},{"type":"Detail","q":"Melted rock below the ground is called —","opts":["magma","lava","ash"],"a":0},{"type":"Vocabulary","q":"\"Molten\" means —","opts":["frozen solid","melted by heat","very loud"],"a":1},{"type":"Detail","q":"The bowl-shaped opening at the top is the —","opts":["vent","crater","island"],"a":1},{"type":"Cause & effect","q":"A volcano erupts when —","opts":["it rains","pressure builds up inside","the lava cools"],"a":1},{"type":"Inference","q":"A \"dormant\" volcano is best described as —","opts":["one that can never erupt","a sleeping giant that could erupt again","an underwater cave"],"a":1}],
 "match":[{"word":"magma","def":"melted rock below the ground","hint":"\"…rock melts into a thick, glowing liquid called <b>magma</b>.\""},{"word":"lava","def":"melted rock that has reached the surface","hint":"\"Once the magma flows onto the surface it is called <b>lava</b>.\""},{"word":"crater","def":"the bowl-shaped opening at a volcano's top","hint":"\"…a bowl-shaped opening at the top called a <b>crater</b>.\""},{"word":"molten","def":"melted by great heat","hint":"\"Lava is <b>molten</b>, which means melted by heat…\""},{"word":"vent","def":"the channel magma travels up through","hint":"\"…the channel that magma travels up is called a <b>vent</b>.\""},{"word":"dormant","def":"not erupting now but able to erupt again","hint":"\"…still could is called <b>dormant</b>, like a sleeping giant.\""}],
 "bank":["magma","lava","erupt","crater","molten","vent","dormant","ash"],
 "fills":[{"text":"Hot melted rock under the ground is called ___.","a":"magma"},{"text":"When a volcano ___s, gas and ash burst out.","a":"erupt"},{"text":"Glowing ___ flowed down the mountain and cooled into rock.","a":"lava"},{"text":"The metal was so hot it turned ___.","a":"molten"},{"text":"Smoke poured from the ___ at the top of the volcano.","a":"crater"},{"text":"Magma rises through a ___ to reach the surface.","a":"vent"},{"text":"The ___ volcano had been quiet for hundreds of years.","a":"dormant"},{"text":"After the campfire, grey ___ was left in the pit.","a":"ash","challenge":True}]},

{"activityId":"egypt","projectKey":"egypt","title":"Ancient Egypt","heroEmoji":"🏺","watermark":"🔺","pageTitle":"Ancient Egypt",
 "win":"PERFECT, Amara! Like a pharaoh! 👑","cheer":"A true explorer of the past! 🏺",
 "palette":{"primary":"#c79a2b","dark":"#9c7820","deep":"#6b5012","accent":"#e0c069","accentSoft":"#f7eecf","cream":"#fffbf0","bgTop":"#faf3e0","bgBottom":"#f3ead2","glow1":"#c79a2b22","glow2":"#6b501218"},
 "passageTitle":"Life in Ancient Egypt",
 "passageHtml":"<p>Thousands of years ago, a great civilization grew along the <span class=\"voc\">Nile</span> River in Egypt. The ruler of ancient Egypt was called a <span class=\"voc\">pharaoh</span>, who was treated like a god. The Egyptians built giant stone <span class=\"voc\">pyramid</span>s as resting places for their pharaohs. They wrote using picture symbols called <span class=\"voc\">hieroglyph</span>s, often on a paper made from reeds called <span class=\"voc\">papyrus</span>.</p><p>The Egyptians believed in an <span class=\"voc\">afterlife</span>, a life that continues after death. To prepare a body for it, they preserved it as a <span class=\"voc\">mummy</span>, wrapping it carefully in cloth. A pharaoh was buried in a <span class=\"voc\">tomb</span> filled with treasure and everyday objects to use in the next life. Much of what we know about ancient Egypt comes from these tombs, which have lasted for thousands of years.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to build a boat","the life and beliefs of ancient Egypt","the weather in Africa"],"a":1},{"type":"Detail","q":"The ruler of ancient Egypt was a —","opts":["pharaoh","mummy","farmer"],"a":0},{"type":"Vocabulary","q":"\"Hieroglyphs\" were —","opts":["stone boats","picture symbols used for writing","river fish"],"a":1},{"type":"Detail","q":"The Egyptians wrote on paper made from —","opts":["wood","reeds called papyrus","animal skin"],"a":1},{"type":"Cause & effect","q":"Egyptians made mummies because they believed in —","opts":["an afterlife","flying","rain"],"a":0},{"type":"Inference","q":"We know so much about ancient Egypt mainly because —","opts":["tombs and their objects survived","they used computers","nothing was ever buried"],"a":0}],
 "match":[{"word":"pharaoh","def":"the god-like ruler of ancient Egypt","hint":"\"The ruler of ancient Egypt was called a <b>pharaoh</b>…\""},{"word":"pyramid","def":"a giant stone resting place for a pharaoh","hint":"\"…built giant stone <b>pyramid</b>s as resting places…\""},{"word":"hieroglyph","def":"a picture symbol used for writing","hint":"\"…picture symbols called <b>hieroglyph</b>s…\""},{"word":"mummy","def":"a body preserved and wrapped in cloth","hint":"\"…they preserved it as a <b>mummy</b>, wrapping it in cloth.\""},{"word":"papyrus","def":"paper made from reeds","hint":"\"…a paper made from reeds called <b>papyrus</b>.\""},{"word":"afterlife","def":"a life believed to continue after death","hint":"\"The Egyptians believed in an <b>afterlife</b>…\""}],
 "bank":["pharaoh","pyramid","hieroglyph","mummy","Nile","tomb","papyrus","afterlife"],
 "fills":[{"text":"The ___ ruled Egypt like a living god.","a":"pharaoh"},{"text":"The huge ___ was built from millions of stone blocks.","a":"pyramid"},{"text":"Each tiny ___ stood for a sound or an idea.","a":"hieroglyph"},{"text":"The dry desert helped turn the body into a ___.","a":"mummy"},{"text":"Egypt grew crops along the ___ River.","a":"Nile"},{"text":"The king was buried in a hidden ___.","a":"tomb"},{"text":"They wrote letters on smooth sheets of ___.","a":"papyrus"},{"text":"Many cultures tell stories about an ___ after we die.","a":"afterlife","challenge":True}]},

{"activityId":"watercycle","projectKey":"watercycle","title":"The Water Cycle","heroEmoji":"💧","watermark":"🌧️","pageTitle":"The Water Cycle",
 "win":"PERFECT, Amara! You're flowing! 💧","cheer":"Brilliant, rain or shine! 🌧️",
 "palette":{"primary":"#2563eb","dark":"#1d4fc0","deep":"#143285","accent":"#7aa0f0","accentSoft":"#e1e9fc","cream":"#f5f8ff","bgTop":"#eef3fd","bgBottom":"#e3ecf8","glow1":"#2563eb22","glow2":"#14328518"},
 "passageTitle":"The Water Cycle",
 "passageHtml":"<p>Water on Earth is always moving in a never-ending journey called the water <span class=\"voc\">cycle</span>. It begins when the sun heats water in oceans, lakes, and rivers. The warm water <span class=\"voc\">evaporate</span>s, turning into a gas called water <span class=\"voc\">vapor</span> that rises into the sky.</p><p>High in the sky the air is cold, so the vapor begins to <span class=\"voc\">condense</span>, changing back into tiny <span class=\"voc\">droplet</span>s of liquid water. Millions of these droplets gather to form a <span class=\"voc\">cloud</span>. When the droplets grow heavy enough, they fall as <span class=\"voc\">precipitation</span> — rain, snow, or hail. The water lands on the ground, where rivers <span class=\"voc\">collect</span> it and carry it back to the sea, and the whole cycle starts again.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to swim","how water moves around the Earth","why the sky is blue"],"a":1},{"type":"Detail","q":"The sun causes water to —","opts":["freeze","evaporate into vapor","disappear forever"],"a":1},{"type":"Vocabulary","q":"\"Condense\" means —","opts":["turn from gas back into liquid","heat up","fall as rain"],"a":0},{"type":"Detail","q":"Rain, snow, and hail are all kinds of —","opts":["clouds","precipitation","vapor"],"a":1},{"type":"Cause & effect","q":"Droplets fall from a cloud when they —","opts":["get too heavy","turn into gas","freeze the sun"],"a":0},{"type":"Inference","q":"The water cycle is called \"never-ending\" because —","opts":["it repeats again and again","it happens only once","water is destroyed"],"a":0}],
 "match":[{"word":"evaporate","def":"to turn from a liquid into a gas","hint":"\"The warm water <b>evaporate</b>s…\""},{"word":"vapor","def":"water in the form of a gas","hint":"\"…a gas called water <b>vapor</b>…\""},{"word":"condense","def":"to turn from a gas back into a liquid","hint":"\"…the vapor begins to <b>condense</b>…\""},{"word":"precipitation","def":"water falling as rain, snow, or hail","hint":"\"…they fall as <b>precipitation</b> — rain, snow, or hail.\""},{"word":"collect","def":"to gather together","hint":"\"…rivers <b>collect</b> it and carry it back to the sea.\""},{"word":"cycle","def":"something that repeats again and again","hint":"\"…a never-ending journey called the water <b>cycle</b>.\""}],
 "bank":["evaporate","vapor","condense","cloud","precipitation","collect","cycle","droplet"],
 "fills":[{"text":"The sun makes puddles ___ into the air.","a":"evaporate"},{"text":"Warm water turns into invisible water ___.","a":"vapor"},{"text":"In the cold sky, vapor will ___ into drops.","a":"condense"},{"text":"A white fluffy ___ floated across the sky.","a":"cloud"},{"text":"Rain and snow are types of ___.","a":"precipitation"},{"text":"A bucket can ___ rain that falls from the roof.","a":"collect"},{"text":"Tiny ___s of water clung to the cold glass.","a":"droplet"},{"text":"The seasons follow a ___ that repeats every year.","a":"cycle","challenge":True}]},

{"activityId":"solar","projectKey":"solar","title":"The Solar System","heroEmoji":"🪐","watermark":"⭐","pageTitle":"The Solar System",
 "win":"PERFECT, Amara! Out of this world! 🪐","cheer":"You're a star, Amara! ⭐",
 "palette":{"primary":"#312e81","dark":"#26235f","deep":"#161440","accent":"#7c79c8","accentSoft":"#e4e3f4","cream":"#f6f6fc","bgTop":"#eeedf8","bgBottom":"#e3e2f2","glow1":"#312e8122","glow2":"#16144018"},
 "passageTitle":"Our Solar System",
 "passageHtml":"<p>Our solar system is made up of the Sun and everything that travels around it. The Sun is a giant <span class=\"voc\">star</span>, a huge ball of burning gas. Eight <span class=\"voc\">planet</span>s move around the Sun, each following a curved path called an <span class=\"voc\">orbit</span>. What keeps the planets from flying off into space is <span class=\"voc\">gravity</span>, an invisible force that pulls objects toward one another. The Sun's strong gravity holds the whole solar system together.</p><p>Between the planets float chunks of rock called <span class=\"voc\">asteroid</span>s, and far beyond our solar system lie billions of other stars that make up our <span class=\"voc\">galaxy</span>, the Milky Way. As each planet orbits the Sun, it also spins around an imaginary line through its middle called an <span class=\"voc\">axis</span>; this spinning is what gives us day and night. Scientists study all of this using a <span class=\"voc\">telescope</span>, a tool that makes faraway objects look closer.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fly a plane","what the solar system is made of","why the Sun is yellow"],"a":1},{"type":"Detail","q":"The Sun is a —","opts":["planet","star","moon"],"a":1},{"type":"Vocabulary","q":"An \"orbit\" is —","opts":["a kind of rock","the curved path a planet travels","a telescope"],"a":1},{"type":"Detail","q":"What holds the solar system together?","opts":["gravity","wind","ice"],"a":0},{"type":"Cause & effect","q":"A planet spinning on its axis gives us —","opts":["day and night","summer only","asteroids"],"a":0},{"type":"Inference","q":"A telescope is useful because it —","opts":["makes faraway things look closer","heats the Sun","creates gravity"],"a":0}],
 "match":[{"word":"orbit","def":"the curved path an object travels around another","hint":"\"…a curved path called an <b>orbit</b>.\""},{"word":"gravity","def":"a force that pulls objects toward each other","hint":"\"…<b>gravity</b>, an invisible force that pulls objects together.\""},{"word":"asteroid","def":"a chunk of rock in space","hint":"\"…chunks of rock called <b>asteroid</b>s…\""},{"word":"axis","def":"an imaginary line an object spins around","hint":"\"…an imaginary line through its middle called an <b>axis</b>.\""},{"word":"galaxy","def":"a huge group of stars","hint":"\"…make up our <b>galaxy</b>, the Milky Way.\""},{"word":"telescope","def":"a tool that makes faraway objects look closer","hint":"\"…using a <b>telescope</b>, a tool that makes faraway objects look closer.\""}],
 "bank":["orbit","planet","gravity","star","asteroid","axis","galaxy","telescope"],
 "fills":[{"text":"Earth follows its ___ around the Sun.","a":"orbit"},{"text":"Mars is a rocky ___ near Earth.","a":"planet"},{"text":"When you jump up, ___ always pulls you back down.","a":"gravity","challenge":True},{"text":"The Sun is the closest ___ to Earth.","a":"star"},{"text":"A small ___ zoomed past, made of rock and metal.","a":"asteroid"},{"text":"The Earth spins on its ___ once a day.","a":"axis"},{"text":"Our Sun is one of billions of stars in the ___.","a":"galaxy"},{"text":"She looked through the ___ to see Saturn's rings.","a":"telescope"}]},

{"activityId":"heart","projectKey":"heart","title":"The Human Heart","heroEmoji":"❤️","watermark":"🫀","pageTitle":"The Human Heart",
 "win":"PERFECT, Amara! You've got heart! ❤️","cheer":"That answer was a heartbeat away from perfect! ❤️",
 "palette":{"primary":"#d6336c","dark":"#ab2856","deep":"#741a3a","accent":"#ec8ab0","accentSoft":"#fbe2ec","cream":"#fff6f9","bgTop":"#fceef3","bgBottom":"#f7e2ea","glow1":"#d6336c22","glow2":"#741a3a18"},
 "passageTitle":"Your Amazing Heart",
 "passageHtml":"<p>Your heart is one of the hardest-working <span class=\"voc\">muscle</span>s in your body. About the size of your fist, it sits in the middle of your chest and never stops working. The heart's job is to <span class=\"voc\">pump</span> <span class=\"voc\">blood</span> to every part of your body. Blood carries <span class=\"voc\">oxygen</span>, the gas your body needs to stay alive, from your lungs to your muscles and organs.</p><p>Blood travels through a network of tubes called <span class=\"voc\">vessel</span>s, which reach every corner of your body. The heart pushes blood out, the body uses the oxygen, and the blood returns to be filled again — this loop is how blood <span class=\"voc\">circulate</span>s. Tiny doors inside the heart called <span class=\"voc\">valve</span>s open and close to keep the blood flowing the right way. You can feel each beat as a <span class=\"voc\">pulse</span> in your wrist or neck.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to run fast","what the heart does","why blood is red"],"a":1},{"type":"Detail","q":"The heart is about the size of your —","opts":["fist","foot","head"],"a":0},{"type":"Vocabulary","q":"\"Vessels\" are —","opts":["bones","tubes that carry blood","lungs"],"a":1},{"type":"Detail","q":"Blood carries ___ to the body.","opts":["oxygen","sugar only","air bubbles"],"a":0},{"type":"Cause & effect","q":"Valves open and close to —","opts":["keep blood flowing the right way","make a pulse stop","cool the body"],"a":0},{"type":"Inference","q":"You can feel your pulse because —","opts":["the heart beats and pushes blood","your bones move","you are breathing out"],"a":0}],
 "match":[{"word":"pump","def":"to push a liquid along","hint":"\"The heart's job is to <b>pump</b> blood…\""},{"word":"vessel","def":"a tube that carries blood","hint":"\"…a network of tubes called <b>vessel</b>s…\""},{"word":"oxygen","def":"the gas the body needs to live","hint":"\"Blood carries <b>oxygen</b>, the gas your body needs…\""},{"word":"circulate","def":"to move around in a loop","hint":"\"…this loop is how blood <b>circulate</b>s.\""},{"word":"muscle","def":"a body part that moves by squeezing","hint":"\"…one of the hardest-working <b>muscle</b>s in your body.\""},{"word":"valve","def":"a small door that controls flow","hint":"\"Tiny doors inside the heart called <b>valve</b>s…\""}],
 "bank":["pump","blood","vessel","oxygen","pulse","circulate","muscle","valve"],
 "fills":[{"text":"The heart works to ___ blood all day.","a":"pump"},{"text":"Red ___ flows through your whole body.","a":"blood"},{"text":"Blood moves through tubes called ___s.","a":"vessel"},{"text":"We breathe in ___ from the air.","a":"oxygen"},{"text":"Warm air and water ___ around the Earth, too.","a":"circulate","challenge":True},{"text":"You use a ___ to bend your arm.","a":"muscle"},{"text":"A ___ keeps the blood from flowing backward.","a":"valve"},{"text":"I felt my ___ speed up after running.","a":"pulse"}]},

{"activityId":"sharks","projectKey":"sharks","title":"Sharks","heroEmoji":"🦈","watermark":"🦈","pageTitle":"Sharks",
 "win":"PERFECT, Amara! Jaw-some! 🦈","cheer":"You swam through that, Amara! 🌊",
 "palette":{"primary":"#51688a","dark":"#3e5170","deep":"#28354b","accent":"#8fa1bd","accentSoft":"#e4e9f0","cream":"#f5f8fb","bgTop":"#eef3f8","bgBottom":"#e3ebf2","glow1":"#51688a22","glow2":"#28354b18"},
 "passageTitle":"All About Sharks",
 "passageHtml":"<p>Sharks are powerful fish that have lived in the oceans for millions of years. Unlike most fish, a shark's skeleton is not made of bone but of <span class=\"voc\">cartilage</span>, the same bendy material in your ears and nose. This makes sharks light and fast. They breathe through slits called <span class=\"voc\">gill</span>s that take in oxygen from the water, and they steer using their <span class=\"voc\">fin</span>s.</p><p>Most sharks are <span class=\"voc\">predator</span>s, animals that hunt other animals for food. A shark has an amazing <span class=\"voc\">sense</span> of smell and can detect a tiny amount of blood from far away. There are more than 500 kinds, or <span class=\"voc\">species</span>, of shark, from the tiny dwarf shark to the giant whale shark. Even though sharks have rows of sharp teeth in their strong <span class=\"voc\">jaw</span>s, very few species are dangerous to people.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fish","what sharks are like and how they live","why the sea is salty"],"a":1},{"type":"Detail","q":"A shark's skeleton is made of —","opts":["bone","cartilage","metal"],"a":1},{"type":"Vocabulary","q":"A \"predator\" is —","opts":["an animal that hunts others","a kind of plant","a baby fish"],"a":0},{"type":"Detail","q":"Sharks breathe using their —","opts":["fins","gills","tails"],"a":1},{"type":"Cause & effect","q":"A shark can find faraway prey because of its —","opts":["strong sense of smell","loud voice","bright color"],"a":0},{"type":"Inference","q":"The passage suggests most sharks are —","opts":["not dangerous to people","friendly pets","unable to swim"],"a":0}],
 "match":[{"word":"predator","def":"an animal that hunts others for food","hint":"\"Most sharks are <b>predator</b>s…\""},{"word":"gill","def":"a slit a fish breathes through","hint":"\"They breathe through slits called <b>gill</b>s…\""},{"word":"cartilage","def":"a bendy material that is not bone","hint":"\"…made of <b>cartilage</b>, the same bendy material in your ears…\""},{"word":"fin","def":"a body part a fish uses to steer","hint":"\"…they steer using their <b>fin</b>s.\""},{"word":"sense","def":"a way of feeling the world, like smell","hint":"\"A shark has an amazing <b>sense</b> of smell…\""},{"word":"species","def":"a particular kind of animal","hint":"\"…more than 500 kinds, or <b>species</b>, of shark…\""}],
 "bank":["predator","gill","cartilage","fin","prey","sense","species","jaw"],
 "fills":[{"text":"A lion is a ___ that hunts other animals.","a":"predator"},{"text":"Fish breathe through their ___s.","a":"gill"},{"text":"Your nose is made of bendy ___.","a":"cartilage"},{"text":"A shark steers with its ___s.","a":"fin"},{"text":"The deer was the ___ that the wolf chased.","a":"prey"},{"text":"A sharp ___ of hearing helps an owl hunt at night.","a":"sense"},{"text":"There are many ___ of dog, like poodles and pugs.","a":"species","challenge":True},{"text":"The shark opened its huge ___.","a":"jaw"}]},

{"activityId":"olympics","projectKey":"olympics","title":"The Olympic Games","heroEmoji":"🏅","watermark":"🔥","pageTitle":"The Olympic Games",
 "win":"PERFECT, Amara! Gold medal! 🥇","cheer":"A champion reader! 🏅",
 "palette":{"primary":"#c92a2a","dark":"#a01f1f","deep":"#6e1414","accent":"#e87f7f","accentSoft":"#fbe1e1","cream":"#fff6f6","bgTop":"#fceeee","bgBottom":"#f7e2e2","glow1":"#c92a2a22","glow2":"#6e141418"},
 "passageTitle":"The Olympic Games",
 "passageHtml":"<p>The Olympic Games are one of the world's biggest sporting events, where <span class=\"voc\">athlete</span>s from many countries <span class=\"voc\">compete</span> against one another. The Games began in <span class=\"voc\">ancient</span> Greece almost 3,000 years ago, held in honor of the Greek gods. Back then, winners were given a crown of olive leaves. The ancient Games ended long ago, but in 1896 they were brought back to life as the modern Olympics.</p><p>Today the Games are held every four years, and a different city gets to <span class=\"voc\">host</span> them each time. Winning athletes receive a gold, silver, or bronze <span class=\"voc\">medal</span>, and a <span class=\"voc\">champion</span> is celebrated around the world. The Games open with a grand <span class=\"voc\">ceremony</span> and the lighting of the Olympic <span class=\"voc\">torch</span>, a flame carried all the way from Greece. The Olympics bring people from different nations together in friendship and sport.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to ride a bike","the history and meaning of the Olympic Games","Greek food"],"a":1},{"type":"Detail","q":"The Olympic Games began in —","opts":["ancient Greece","modern America","ancient Egypt"],"a":0},{"type":"Vocabulary","q":"To \"compete\" means —","opts":["to give up","to try to win against others","to watch"],"a":1},{"type":"Detail","q":"How often are the modern Games held?","opts":["every year","every four years","every month"],"a":1},{"type":"Detail","q":"A winning athlete receives a —","opts":["medal","car","crown of gold"],"a":0},{"type":"Inference","q":"The passage suggests the Olympics help to —","opts":["bring nations together","start wars","end all sports"],"a":0}],
 "match":[{"word":"athlete","def":"a person trained in a sport","hint":"\"…<b>athlete</b>s from many countries compete…\""},{"word":"compete","def":"to try to win against others","hint":"\"…<b>compete</b> against one another.\""},{"word":"ancient","def":"very old, from long ago","hint":"\"The Games began in <b>ancient</b> Greece…\""},{"word":"ceremony","def":"a special event with traditions","hint":"\"The Games open with a grand <b>ceremony</b>…\""},{"word":"host","def":"to hold an event for others","hint":"\"…a different city gets to <b>host</b> them…\""},{"word":"champion","def":"a winner who is the best","hint":"\"…a <b>champion</b> is celebrated around the world.\""}],
 "bank":["athlete","compete","ancient","medal","ceremony","host","torch","champion"],
 "fills":[{"text":"The fast runner was a famous ___.","a":"athlete"},{"text":"Teams ___ to see who is fastest.","a":"compete"},{"text":"The pyramids are part of ___ history.","a":"ancient"},{"text":"The winner proudly wore a gold ___.","a":"medal"},{"text":"Our town will ___ a big music festival next year.","a":"host","challenge":True},{"text":"The runner carried the flaming ___.","a":"torch"},{"text":"The opening ___ had music and flags.","a":"ceremony"},{"text":"She became the world ___ in swimming.","a":"champion"}]},

{"activityId":"money","projectKey":"money","title":"How Money Works","heroEmoji":"💰","watermark":"🪙","pageTitle":"How Money Works",
 "win":"PERFECT, Amara! Money smart! 💰","cheer":"You earned every point! 🪙",
 "palette":{"primary":"#2f9e44","dark":"#247a35","deep":"#175223","accent":"#74c686","accentSoft":"#dcf2e1","cream":"#f4fbf6","bgTop":"#ebf7ee","bgBottom":"#e0f0e4","glow1":"#2f9e4422","glow2":"#17522318"},
 "passageTitle":"How Money Works",
 "passageHtml":"<p>Long ago, before money existed, people got what they needed by <span class=\"voc\">barter</span>, which means trading one thing directly for another. A farmer might <span class=\"voc\">trade</span> a basket of eggs for a pair of shoes. But bartering was tricky — what if the shoemaker did not want eggs? To make trading easier, people invented money, a special kind of <span class=\"voc\">currency</span> that everyone agrees has <span class=\"voc\">value</span>.</p><p>Today, people <span class=\"voc\">earn</span> money by working, and they spend it to buy <span class=\"voc\">goods</span> and services they need. Because money is limited, it is smart to make a <span class=\"voc\">budget</span>, a plan for how much to spend and how much to <span class=\"voc\">save</span>. Saving money now means you can buy something bigger later, or be ready if an emergency comes. Understanding money helps people make good choices.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to bake bread","what money is and why people use it","how shoes are made"],"a":1},{"type":"Detail","q":"Before money, people traded by —","opts":["bartering","using cards","printing bills"],"a":0},{"type":"Vocabulary","q":"\"Currency\" means —","opts":["a kind of food","money that people use","a job"],"a":1},{"type":"Detail","q":"People earn money by —","opts":["sleeping","working","bartering only"],"a":1},{"type":"Cause & effect","q":"A budget helps because money is —","opts":["free","limited","heavy"],"a":1},{"type":"Inference","q":"Saving money is smart because it —","opts":["lets you buy bigger things later or handle emergencies","makes money disappear","is against the rules"],"a":0}],
 "match":[{"word":"trade","def":"to give one thing to get another","hint":"\"A farmer might <b>trade</b> a basket of eggs for shoes.\""},{"word":"currency","def":"money that people use","hint":"\"…a special kind of <b>currency</b>…\""},{"word":"barter","def":"trading goods directly without money","hint":"\"…by <b>barter</b>, which means trading one thing for another.\""},{"word":"value","def":"how much something is worth","hint":"\"…everyone agrees has <b>value</b>.\""},{"word":"earn","def":"to get money by working","hint":"\"…people <b>earn</b> money by working…\""},{"word":"budget","def":"a plan for spending and saving","hint":"\"…it is smart to make a <b>budget</b>…\""}],
 "bank":["trade","currency","barter","value","earn","budget","save","goods"],
 "fills":[{"text":"The dollar is the ___ used in the United States.","a":"currency"},{"text":"People with no money would ___ chickens for corn.","a":"barter"},{"text":"You ___ money by doing a job.","a":"earn"},{"text":"A wise family makes a ___ each month.","a":"budget"},{"text":"I will ___ my coins to buy a new bike.","a":"save"},{"text":"Stores sell ___ like food and clothes.","a":"goods"},{"text":"Two kids might ___ stickers at school.","a":"trade"},{"text":"A rare card can have a high ___ to collectors.","a":"value","challenge":True}]},

{"activityId":"storms","projectKey":"storms","title":"Thunderstorms","heroEmoji":"⛈️","watermark":"⚡","pageTitle":"Thunderstorms",
 "win":"PERFECT, Amara! Electric! ⚡","cheer":"You brightened the sky! ⛈️",
 "palette":{"primary":"#364fc7","dark":"#2a3e9c","deep":"#1a2766","accent":"#7c8de0","accentSoft":"#e2e6f8","cream":"#f5f6fd","bgTop":"#eef0fb","bgBottom":"#e3e7f6","glow1":"#364fc722","glow2":"#1a276618"},
 "passageTitle":"Thunderstorms",
 "passageHtml":"<p>A thunderstorm is a powerful weather event filled with <span class=\"voc\">lightning</span>, <span class=\"voc\">thunder</span>, heavy rain, and strong wind. Storms often form on warm, <span class=\"voc\">humid</span> days, when the air is full of moisture. Warm air rises quickly and builds tall storm clouds. Inside these clouds, ice and water bump together and create a build-up of <span class=\"voc\">electricity</span>.</p><p>When that electricity jumps through the <span class=\"voc\">atmosphere</span> — the layer of air around the Earth — we see a flash of lightning. Lightning heats the air so fast that it makes a loud bang we call thunder. Storms can bring sudden <span class=\"voc\">gust</span>s of wind that bend the trees. Weather scientists watch the sky and give a <span class=\"voc\">forecast</span> so people know a storm is coming and can take <span class=\"voc\">shelter</span> somewhere safe.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to fly a kite","what thunderstorms are and how they form","why grass is green"],"a":1},{"type":"Detail","q":"Thunderstorms often form on days that are —","opts":["cold and dry","warm and humid","snowy"],"a":1},{"type":"Vocabulary","q":"The \"atmosphere\" is —","opts":["a storm cloud","the layer of air around Earth","a flash of light"],"a":1},{"type":"Cause & effect","q":"Thunder happens because lightning —","opts":["heats the air very fast","cools the rain","blocks the Sun"],"a":0},{"type":"Detail","q":"A forecast tells people —","opts":["a storm is coming","how to swim","the time of day only"],"a":0},{"type":"Inference","q":"People take shelter during a storm to —","opts":["stay safe","see more lightning","make thunder"],"a":0}],
 "match":[{"word":"lightning","def":"a flash of electricity in the sky","hint":"\"…filled with <b>lightning</b>, thunder, heavy rain…\""},{"word":"atmosphere","def":"the layer of air around the Earth","hint":"\"…the <b>atmosphere</b> — the layer of air around the Earth…\""},{"word":"electricity","def":"a form of energy that can flow or flash","hint":"\"…create a build-up of <b>electricity</b>.\""},{"word":"humid","def":"having a lot of moisture in the air","hint":"\"Storms often form on warm, <b>humid</b> days…\""},{"word":"gust","def":"a sudden rush of wind","hint":"\"Storms can bring sudden <b>gust</b>s of wind…\""},{"word":"forecast","def":"a guess about what the weather will do","hint":"\"…scientists…give a <b>forecast</b>…\""}],
 "bank":["thunder","lightning","atmosphere","electricity","humid","gust","forecast","shelter"],
 "fills":[{"text":"A bright bolt of ___ lit up the sky.","a":"lightning"},{"text":"We heard a loud crack of ___.","a":"thunder"},{"text":"The air felt sticky and ___ before the rain.","a":"humid"},{"text":"A strong ___ of wind blew my hat away.","a":"gust"},{"text":"The weather ___ said it would rain at noon.","a":"forecast"},{"text":"We ran inside to take ___ from the storm.","a":"shelter"},{"text":"A lamp and a TV both run on ___.","a":"electricity","challenge":True},{"text":"Birds fly high up in the ___.","a":"atmosphere"}]},

{"activityId":"castles","projectKey":"castles","title":"Castles and Knights","heroEmoji":"🏰","watermark":"⚔️","pageTitle":"Castles and Knights",
 "win":"PERFECT, Amara! A noble win! 🏰","cheer":"You defended every answer! ⚔️",
 "palette":{"primary":"#6c757d","dark":"#545b61","deep":"#373b40","accent":"#a3abb2","accentSoft":"#e6e9eb","cream":"#f7f8f9","bgTop":"#eff1f2","bgBottom":"#e5e8ea","glow1":"#6c757d22","glow2":"#373b4018"},
 "passageTitle":"Castles and Knights",
 "passageHtml":"<p>In the Middle Ages, powerful lords built castles to protect their land and people. A castle was a strong stone <span class=\"voc\">fortress</span> designed to be hard to attack. Many castles were surrounded by a <span class=\"voc\">moat</span>, a deep ditch filled with water. To cross it, visitors used a <span class=\"voc\">drawbridge</span> that could be raised to lock enemies out. Thick walls and tall towers helped the people inside <span class=\"voc\">defend</span> themselves.</p><p>Castles were home to <span class=\"voc\">noble</span>s — important, wealthy families — and the soldiers who served them. The most famous of these soldiers were <span class=\"voc\">knight</span>s, warriors who fought on horseback wearing metal <span class=\"voc\">armor</span> to protect their bodies. Sometimes an enemy army would surround a castle and try to break in, an attack called a <span class=\"voc\">siege</span>. A castle's clever design could keep its people safe for months.</p>",
 "questions":[{"type":"Main idea","q":"This passage is mostly about —","opts":["how to ride a horse","how castles protected people in the Middle Ages","what knights ate"],"a":1},{"type":"Detail","q":"A moat is a —","opts":["tall tower","deep ditch filled with water","metal suit"],"a":1},{"type":"Vocabulary","q":"A \"fortress\" is —","opts":["a strong building made for defense","a horse","a king's crown"],"a":0},{"type":"Detail","q":"Knights protected their bodies with —","opts":["armor","blankets","paper"],"a":0},{"type":"Cause & effect","q":"A drawbridge could be raised in order to —","opts":["lock enemies out","let in more water","feed the horses"],"a":0},{"type":"Inference","q":"A \"siege\" suggests the castle was —","opts":["under attack","having a party","being built"],"a":0}],
 "match":[{"word":"fortress","def":"a strong building made for defense","hint":"\"…a strong stone <b>fortress</b> designed to be hard to attack.\""},{"word":"moat","def":"a deep, water-filled ditch around a castle","hint":"\"…a <b>moat</b>, a deep ditch filled with water.\""},{"word":"drawbridge","def":"a bridge that can be raised and lowered","hint":"\"…a <b>drawbridge</b> that could be raised…\""},{"word":"armor","def":"a metal suit that protects the body","hint":"\"…wearing metal <b>armor</b> to protect their bodies.\""},{"word":"siege","def":"an attack that surrounds a place","hint":"\"…an attack called a <b>siege</b>.\""},{"word":"noble","def":"an important, wealthy person","hint":"\"Castles were home to <b>noble</b>s…\""}],
 "bank":["fortress","moat","drawbridge","knight","armor","siege","noble","defend"],
 "fills":[{"text":"The castle was a stone ___ on a hill.","a":"fortress"},{"text":"Water filled the ___ around the walls.","a":"moat"},{"text":"They lowered the ___ to let the cart cross.","a":"drawbridge"},{"text":"The brave ___ rode a horse into battle.","a":"knight"},{"text":"His shiny ___ protected him from swords.","a":"armor"},{"text":"The army began a ___ around the city.","a":"siege"},{"text":"A wealthy ___ owned the land and the farms.","a":"noble"},{"text":"Our soccer team must ___ its goal in the game.","a":"defend","challenge":True}]},

{"activityId":"cats","projectKey":"cats","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"All About Cats","heroEmoji":"🐱","watermark":"🐾","pageTitle":"Cats",
 "win":"PERFECT, Dani! Purr-fect! 🐱","cheer":"The kittens love you, Dani! 🐾",
 "palette":{"primary":"#9b6cd6","dark":"#7a52ad","deep":"#523372","accent":"#c2a0e6","accentSoft":"#efe6f8","cream":"#fbf8fe","bgTop":"#f4ecfb","bgBottom":"#ece0f5","glow1":"#9b6cd622","glow2":"#52337218"},
 "passageTitle":"All About Cats",
 "passageHtml":"<p>A cat is a soft, furry pet. Cats have long <span class=\"voc\">whiskers</span> on their face. They walk on four soft <span class=\"voc\">paws</span>. When a cat is happy, it will <span class=\"voc\">purr</span>.</p><p>A baby cat is called a <span class=\"voc\">kitten</span>. Cats have sharp <span class=\"voc\">claws</span> to climb and play. They like to <span class=\"voc\">pounce</span> on toys. Cats are fun and cuddly pets.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["dogs","cats","birds"],"a":1},{"type":"Detail","q":"A baby cat is a —","opts":["kitten","puppy","chick"],"a":0},{"type":"Detail","q":"A happy cat will —","opts":["bark","purr","swim"],"a":1},{"type":"Detail","q":"Cats walk on —","opts":["two feet","four paws","wheels"],"a":1},{"type":"Vocabulary","q":"\"Pounce\" means —","opts":["to jump on something","to sleep","to eat"],"a":0}],
 "match":[{"word":"whiskers","def":"long hairs on a cat's face","hint":"\"Cats have long <b>whiskers</b> on their face.\""},{"word":"purr","def":"a soft happy sound a cat makes","hint":"\"…it will <b>purr</b>.\""},{"word":"claws","def":"sharp nails on a cat's paw","hint":"\"Cats have sharp <b>claws</b> to climb…\""},{"word":"kitten","def":"a baby cat","hint":"\"A baby cat is called a <b>kitten</b>.\""},{"word":"pounce","def":"to jump on something quickly","hint":"\"They like to <b>pounce</b> on toys.\""}],
 "bank":["whiskers","purr","paws","claws","kitten","pounce"],
 "fills":[{"text":"A cat has long ___ on its face.","a":"whiskers"},{"text":"My cat will ___ when it is happy.","a":"purr"},{"text":"The cat walks on soft ___.","a":"paws"},{"text":"Sharp ___ help a cat climb.","a":"claws"},{"text":"A baby cat is a ___.","a":"kitten"},{"text":"The cat likes to ___ on its toy.","a":"pounce"}]},

{"activityId":"rainbows","projectKey":"rainbows","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Rainbows","heroEmoji":"🌈","watermark":"🌈","pageTitle":"Rainbows",
 "win":"PERFECT, Dani! Bright and colorful! 🌈","cheer":"You made the sky smile, Dani! 🌈",
 "palette":{"primary":"#14b8a6","dark":"#0f9384","deep":"#0a6358","accent":"#6dd5c8","accentSoft":"#d6f4ef","cream":"#f2fcfa","bgTop":"#e8f8f5","bgBottom":"#ddf1ed","glow1":"#14b8a622","glow2":"#0a635818"},
 "passageTitle":"Rainbows",
 "passageHtml":"<p>A <span class=\"voc\">rainbow</span> is a band of pretty <span class=\"voc\">color</span>s in the <span class=\"voc\">sky</span>. It looks like a big <span class=\"voc\">arch</span>. You can see a rainbow after it rains.</p><p>A rainbow is made when <span class=\"voc\">sunlight</span> shines through a <span class=\"voc\">raindrop</span>. The light bends and splits into many colors. Red, blue, and green are some of them. Rainbows make people smile!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["bugs","rainbows","cars"],"a":1},{"type":"Detail","q":"A rainbow is shaped like an —","opts":["arch","box","star"],"a":0},{"type":"Detail","q":"You see a rainbow after it —","opts":["rains","snows","sleeps"],"a":0},{"type":"Detail","q":"A rainbow is made from —","opts":["sunlight and raindrops","mud","rocks"],"a":0},{"type":"Vocabulary","q":"The \"sky\" is —","opts":["the ground","the air high above us","a pond"],"a":1}],
 "match":[{"word":"rainbow","def":"a band of colors in the sky","hint":"\"A <b>rainbow</b> is a band of pretty colors…\""},{"word":"arch","def":"a curved shape like a bridge","hint":"\"It looks like a big <b>arch</b>.\""},{"word":"sky","def":"the air high above us","hint":"\"…colors in the <b>sky</b>.\""},{"word":"sunlight","def":"light from the sun","hint":"\"…when <b>sunlight</b> shines through a raindrop.\""},{"word":"raindrop","def":"a small drop of rain","hint":"\"…shines through a <b>raindrop</b>.\""}],
 "bank":["rainbow","color","arch","sky","sunlight","raindrop"],
 "fills":[{"text":"A ___ has many colors.","a":"rainbow"},{"text":"Red is my favorite ___.","a":"color"},{"text":"The rainbow makes a big ___.","a":"arch"},{"text":"Clouds float in the ___.","a":"sky"},{"text":"Plants need ___ to grow.","a":"sunlight"},{"text":"One ___ landed on my nose.","a":"raindrop"}]},

{"activityId":"dinos","projectKey":"dinos","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Dinosaurs","heroEmoji":"🦕","watermark":"🦖","pageTitle":"Dinosaurs",
 "win":"PERFECT, Dani! Dino-mite! 🦕","cheer":"Roar! Great job, Dani! 🦖",
 "palette":{"primary":"#43a047","dark":"#347a37","deep":"#225224","accent":"#85c888","accentSoft":"#dcf1dd","cream":"#f4fbf4","bgTop":"#ebf7ec","bgBottom":"#e0f0e1","glow1":"#43a04722","glow2":"#22522418"},
 "passageTitle":"Dinosaurs",
 "passageHtml":"<p><span class=\"voc\">Dinosaur</span>s were animals that lived long, long ago. Some were very <span class=\"voc\">huge</span>. Their skin was covered in tough <span class=\"voc\">scales</span>. Some dinosaurs could <span class=\"voc\">roar</span> very loudly.</p><p>Dinosaurs are now <span class=\"voc\">extinct</span>. That means there are none left alive today. We learn about them from a <span class=\"voc\">fossil</span>, which is a bone or print saved in rock. Dinosaurs are amazing to study!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["fish","dinosaurs","trucks"],"a":1},{"type":"Detail","q":"Dinosaur skin had —","opts":["fur","scales","feathers only"],"a":1},{"type":"Vocabulary","q":"\"Extinct\" means —","opts":["none are left alive","very small","very fast"],"a":0},{"type":"Detail","q":"We learn about dinosaurs from a —","opts":["fossil","photo","video"],"a":0},{"type":"Detail","q":"Some dinosaurs were very —","opts":["tiny","huge","purple"],"a":1}],
 "match":[{"word":"dinosaur","def":"an animal that lived long ago","hint":"\"<b>Dinosaur</b>s were animals that lived long ago.\""},{"word":"fossil","def":"a bone or print saved in rock","hint":"\"…a <b>fossil</b>, which is a bone or print saved in rock.\""},{"word":"extinct","def":"when none are left alive","hint":"\"Dinosaurs are now <b>extinct</b>.\""},{"word":"scales","def":"tough skin like a lizard's","hint":"\"Their skin was covered in tough <b>scales</b>.\""},{"word":"roar","def":"a loud, deep sound","hint":"\"Some dinosaurs could <b>roar</b> very loudly.\""}],
 "bank":["dinosaur","fossil","extinct","scales","huge","roar"],
 "fills":[{"text":"A ___ lived millions of years ago.","a":"dinosaur"},{"text":"We found a ___ in the rock.","a":"fossil"},{"text":"Dinosaurs are ___ now.","a":"extinct"},{"text":"Its skin had bumpy ___.","a":"scales"},{"text":"The dinosaur was very ___ and tall.","a":"huge"},{"text":"The big dinosaur let out a ___.","a":"roar"}]},

{"activityId":"beach","projectKey":"beach","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"A Day at the Beach","heroEmoji":"🏖️","watermark":"🐚","pageTitle":"The Beach",
 "win":"PERFECT, Dani! Beach star! 🏖️","cheer":"You made waves, Dani! 🌊",
 "palette":{"primary":"#2bb3d4","dark":"#208ca7","deep":"#155e70","accent":"#7ad3e6","accentSoft":"#d6f1f8","cream":"#f2fbfd","bgTop":"#e8f6fa","bgBottom":"#ddeff4","glow1":"#2bb3d422","glow2":"#155e7018"},
 "passageTitle":"A Day at the Beach",
 "passageHtml":"<p>The <span class=\"voc\">beach</span> is a fun place by the <span class=\"voc\">ocean</span>. The ground is covered in soft <span class=\"voc\">sand</span>. You can build castles in the sand. The blue <span class=\"voc\">wave</span>s splash on the shore.</p><p>You can find a pretty <span class=\"voc\">shell</span> in the sand. The water moves in and out with the <span class=\"voc\">tide</span>. Bring a hat and sunscreen to stay safe. A day at the beach is lots of fun!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["a farm","the beach","a city"],"a":1},{"type":"Detail","q":"The beach is next to the —","opts":["ocean","forest","mountains"],"a":0},{"type":"Detail","q":"The ground at the beach is —","opts":["sand","grass","snow"],"a":0},{"type":"Detail","q":"Waves splash on the —","opts":["shore","roof","road"],"a":0},{"type":"Vocabulary","q":"The \"tide\" is —","opts":["the water moving in and out","a sandcastle","a hat"],"a":0}],
 "match":[{"word":"beach","def":"a sandy place by the sea","hint":"\"The <b>beach</b> is a fun place by the ocean.\""},{"word":"wave","def":"water that rolls onto the shore","hint":"\"The blue <b>wave</b>s splash on the shore.\""},{"word":"shell","def":"a hard cover from a sea animal","hint":"\"You can find a pretty <b>shell</b> in the sand.\""},{"word":"ocean","def":"a very large body of salt water","hint":"\"…a fun place by the <b>ocean</b>.\""},{"word":"tide","def":"the rising and falling of the sea","hint":"\"The water moves in and out with the <b>tide</b>.\""}],
 "bank":["beach","sand","wave","shell","ocean","tide"],
 "fills":[{"text":"We played all day at the ___.","a":"beach"},{"text":"I built a castle in the ___.","a":"sand"},{"text":"A big ___ splashed my feet.","a":"wave"},{"text":"I found a pink ___ on the shore.","a":"shell"},{"text":"Fish live in the ___.","a":"ocean"},{"text":"The ___ went out and left wet sand.","a":"tide"}]},

{"activityId":"farm","projectKey":"farm","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"On the Farm","heroEmoji":"🐄","watermark":"🚜","pageTitle":"Farm Animals",
 "win":"PERFECT, Dani! Farm star! 🐄","cheer":"The animals are cheering, Dani! 🐔",
 "palette":{"primary":"#a1662f","dark":"#7e4f24","deep":"#523114","accent":"#cc9a6c","accentSoft":"#f0e3d4","cream":"#fdf9f3","bgTop":"#f7f0e7","bgBottom":"#efe5d7","glow1":"#a1662f22","glow2":"#52311418"},
 "passageTitle":"On the Farm",
 "passageHtml":"<p>A <span class=\"voc\">farm</span> is home to many animals. The <span class=\"voc\">cow</span> gives us milk. A <span class=\"voc\">hen</span> lays eggs for us to eat. Sheep give us soft <span class=\"voc\">wool</span> for warm clothes.</p><p>At night the animals sleep in the <span class=\"voc\">barn</span>. The farmer feeds them dry <span class=\"voc\">hay</span>. The animals help the farmer every day. Farms are busy, happy places.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["the city","farm animals","the ocean"],"a":1},{"type":"Detail","q":"A cow gives us —","opts":["milk","eggs","wool"],"a":0},{"type":"Detail","q":"A hen lays —","opts":["eggs","hay","wool"],"a":0},{"type":"Detail","q":"Animals sleep in the —","opts":["barn","pool","car"],"a":0},{"type":"Vocabulary","q":"\"Wool\" comes from —","opts":["sheep","cows","hens"],"a":0}],
 "match":[{"word":"farm","def":"a place where animals and crops are raised","hint":"\"A <b>farm</b> is home to many animals.\""},{"word":"barn","def":"a building where farm animals sleep","hint":"\"…the animals sleep in the <b>barn</b>.\""},{"word":"hen","def":"a female chicken that lays eggs","hint":"\"A <b>hen</b> lays eggs for us to eat.\""},{"word":"wool","def":"soft hair from a sheep","hint":"\"Sheep give us soft <b>wool</b>…\""},{"word":"hay","def":"dried grass that animals eat","hint":"\"The farmer feeds them dry <b>hay</b>.\""}],
 "bank":["farm","barn","cow","hen","wool","hay"],
 "fills":[{"text":"We saw many animals at the ___.","a":"farm"},{"text":"The ___ gave us fresh milk.","a":"cow"},{"text":"A ___ laid three eggs.","a":"hen"},{"text":"My sweater is made of warm ___.","a":"wool"},{"text":"The horses sleep in the ___.","a":"barn"},{"text":"The cows eat dry ___.","a":"hay"}]},

{"activityId":"pizza","projectKey":"pizza","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"How We Make Pizza","heroEmoji":"🍕","watermark":"🍕","pageTitle":"Pizza",
 "win":"PERFECT, Dani! Tasty work! 🍕","cheer":"Yum! Great reading, Dani! 🍕",
 "palette":{"primary":"#e2452f","dark":"#b53624","deep":"#7c2314","accent":"#ef8675","accentSoft":"#fbe1dc","cream":"#fff6f4","bgTop":"#fceee9","bgBottom":"#f7e2dc","glow1":"#e2452f22","glow2":"#7c231418"},
 "passageTitle":"How We Make Pizza",
 "passageHtml":"<p><span class=\"voc\">Pizza</span> is a yummy food that many people love. First you flatten the <span class=\"voc\">dough</span> into a round shape. Then you spread red <span class=\"voc\">sauce</span> on top. Next you add lots of <span class=\"voc\">cheese</span>.</p><p>You can put a <span class=\"voc\">topping</span> on your pizza, like mushrooms or ham. Then it bakes in a hot <span class=\"voc\">oven</span>. The cheese melts and bubbles. Hot pizza is so tasty!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["how to swim","how pizza is made","a pet"],"a":1},{"type":"Detail","q":"The first step is to flatten the —","opts":["dough","cheese","oven"],"a":0},{"type":"Detail","q":"Pizza bakes in a hot —","opts":["oven","pool","box"],"a":0},{"type":"Detail","q":"You spread red ___ on the dough.","opts":["sauce","paint","milk"],"a":0},{"type":"Vocabulary","q":"A \"topping\" is —","opts":["something you add on top","the floor","a drink"],"a":0}],
 "match":[{"word":"dough","def":"soft mix used to make pizza crust","hint":"\"…flatten the <b>dough</b> into a round shape.\""},{"word":"sauce","def":"a soft red topping made from tomatoes","hint":"\"…spread red <b>sauce</b> on top.\""},{"word":"cheese","def":"a melty food made from milk","hint":"\"…add lots of <b>cheese</b>.\""},{"word":"topping","def":"something added on top of pizza","hint":"\"You can put a <b>topping</b> on your pizza…\""},{"word":"oven","def":"a hot box used for baking","hint":"\"…it bakes in a hot <b>oven</b>.\""}],
 "bank":["pizza","dough","sauce","cheese","topping","oven"],
 "fills":[{"text":"We ordered a big ___ for dinner.","a":"pizza"},{"text":"Roll the ___ into a circle.","a":"dough"},{"text":"Spread red ___ on top.","a":"sauce"},{"text":"Add lots of melty ___.","a":"cheese"},{"text":"My favorite ___ is mushrooms.","a":"topping"},{"text":"Bake the pizza in the ___.","a":"oven"}]},

{"activityId":"bugs","projectKey":"bugs","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Bugs and Insects","heroEmoji":"🐞","watermark":"🐛","pageTitle":"Bugs",
 "win":"PERFECT, Dani! Bug expert! 🐞","cheer":"The ladybugs are proud, Dani! 🐞",
 "palette":{"primary":"#84a516","dark":"#677f11","deep":"#445409","accent":"#b8cf6a","accentSoft":"#eaf2d4","cream":"#f9fbf0","bgTop":"#f1f6e2","bgBottom":"#e7efd2","glow1":"#84a51622","glow2":"#44540918"},
 "passageTitle":"Bugs and Insects",
 "passageHtml":"<p>A bug is a small <span class=\"voc\">insect</span>. Most insects are very <span class=\"voc\">tiny</span>. Many have six legs and two <span class=\"voc\">antenna</span>s on their head. Some bugs have <span class=\"voc\">wing</span>s and can fly.</p><p>A ladybug and a <span class=\"voc\">beetle</span> are kinds of insects. Some bugs <span class=\"voc\">crawl</span> on the ground. Bees and butterflies fly from flower to flower. Bugs are small but very important!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["fish","bugs and insects","cars"],"a":1},{"type":"Detail","q":"Many insects have how many legs?","opts":["two","six","ten"],"a":1},{"type":"Detail","q":"Antennas are on a bug's —","opts":["head","foot","wing"],"a":0},{"type":"Detail","q":"A ladybug is a kind of —","opts":["insect","fish","bird"],"a":0},{"type":"Vocabulary","q":"\"Crawl\" means —","opts":["to move slowly on the ground","to fly fast","to sleep"],"a":0}],
 "match":[{"word":"insect","def":"a small animal with six legs","hint":"\"A bug is a small <b>insect</b>.\""},{"word":"antenna","def":"a feeler on a bug's head","hint":"\"…two <b>antenna</b>s on their head.\""},{"word":"wing","def":"a body part used to fly","hint":"\"Some bugs have <b>wing</b>s and can fly.\""},{"word":"crawl","def":"to move slowly on the ground","hint":"\"Some bugs <b>crawl</b> on the ground.\""},{"word":"beetle","def":"a kind of insect with hard wings","hint":"\"A ladybug and a <b>beetle</b> are kinds of insects.\""}],
 "bank":["insect","antenna","wing","crawl","beetle","tiny"],
 "fills":[{"text":"An ant is a small ___.","a":"insect"},{"text":"A bug feels with its ___s.","a":"antenna"},{"text":"A bee uses its ___s to fly.","a":"wing"},{"text":"The caterpillar will ___ on the leaf.","a":"crawl"},{"text":"A red ___ walked up the stem.","a":"beetle"},{"text":"Ants are very ___.","a":"tiny"}]},

{"activityId":"trucks","projectKey":"trucks","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Big Trucks","heroEmoji":"🚚","watermark":"🚛","pageTitle":"Trucks",
 "win":"PERFECT, Dani! Full speed! 🚚","cheer":"You delivered every answer, Dani! 🚛",
 "palette":{"primary":"#5872a8","dark":"#445882","deep":"#2c3a56","accent":"#92a5cb","accentSoft":"#e4e9f2","cream":"#f6f8fb","bgTop":"#eef2f8","bgBottom":"#e4eaf3","glow1":"#5872a822","glow2":"#2c3a5618"},
 "passageTitle":"Big Trucks",
 "passageHtml":"<p>A <span class=\"voc\">truck</span> is a big machine that carries heavy things. It has a strong <span class=\"voc\">engine</span> to make it go. A truck rolls on big rubber <span class=\"voc\">wheel</span>s. The <span class=\"voc\">driver</span> sits up high in the front.</p><p>Trucks carry <span class=\"voc\">cargo</span>, like food and toys. They <span class=\"voc\">deliver</span> things to stores and homes. Some trucks are huge and very long. Trucks help bring us the things we need.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["boats","trucks","cats"],"a":1},{"type":"Detail","q":"A truck is made to carry —","opts":["heavy things","people only","nothing"],"a":0},{"type":"Detail","q":"A truck rolls on —","opts":["wheels","wings","skis"],"a":0},{"type":"Detail","q":"The person who drives is the —","opts":["driver","baker","teacher"],"a":0},{"type":"Vocabulary","q":"\"Deliver\" means —","opts":["to bring something to a place","to eat","to sleep"],"a":0}],
 "match":[{"word":"truck","def":"a big machine for carrying heavy loads","hint":"\"A <b>truck</b> is a big machine that carries heavy things.\""},{"word":"engine","def":"the part that makes a vehicle go","hint":"\"It has a strong <b>engine</b> to make it go.\""},{"word":"cargo","def":"the things a truck carries","hint":"\"Trucks carry <b>cargo</b>, like food and toys.\""},{"word":"driver","def":"the person who drives","hint":"\"The <b>driver</b> sits up high in the front.\""},{"word":"deliver","def":"to bring something to a place","hint":"\"They <b>deliver</b> things to stores and homes.\""}],
 "bank":["truck","engine","wheel","cargo","driver","deliver"],
 "fills":[{"text":"The big ___ carried bricks.","a":"truck"},{"text":"The ___ roared as the truck started.","a":"engine"},{"text":"Each ___ is made of rubber.","a":"wheel"},{"text":"The truck was full of ___.","a":"cargo"},{"text":"The ___ honked the horn.","a":"driver"},{"text":"Trucks ___ food to the store.","a":"deliver"}]},

{"activityId":"teeth","projectKey":"teeth","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"Brushing Your Teeth","heroEmoji":"🦷","watermark":"🪥","pageTitle":"Brushing Your Teeth",
 "win":"PERFECT, Dani! Bright smile! 🦷","cheer":"Sparkling work, Dani! ✨",
 "palette":{"primary":"#1697b5","dark":"#11778f","deep":"#0a4f60","accent":"#69c4d8","accentSoft":"#d4f0f6","cream":"#f2fbfc","bgTop":"#e8f6f9","bgBottom":"#ddeff3","glow1":"#1697b522","glow2":"#0a4f6018"},
 "passageTitle":"Brushing Your Teeth",
 "passageHtml":"<p>It is important to take care of your <span class=\"voc\">teeth</span>. You should <span class=\"voc\">brush</span> them two times a day. Put a little <span class=\"voc\">toothpaste</span> on your brush. Brushing keeps your teeth clean and white.</p><p>Clean teeth are <span class=\"voc\">healthy</span> teeth. If you do not brush, you can get a <span class=\"voc\">cavity</span>, which is a hole in a tooth. A <span class=\"voc\">dentist</span> checks your teeth to keep them strong. A bright smile feels great!</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["washing dishes","taking care of your teeth","baking bread"],"a":1},{"type":"Detail","q":"You should brush —","opts":["two times a day","once a week","never"],"a":0},{"type":"Detail","q":"You put ___ on your brush.","opts":["toothpaste","juice","soap"],"a":0},{"type":"Vocabulary","q":"A \"cavity\" is —","opts":["a hole in a tooth","a clean tooth","a brush"],"a":0},{"type":"Detail","q":"A ___ checks your teeth.","opts":["dentist","chef","pilot"],"a":0}],
 "match":[{"word":"brush","def":"to clean with a small tool with bristles","hint":"\"You should <b>brush</b> them two times a day.\""},{"word":"toothpaste","def":"a paste used to clean teeth","hint":"\"Put a little <b>toothpaste</b> on your brush.\""},{"word":"healthy","def":"strong and well, not sick","hint":"\"Clean teeth are <b>healthy</b> teeth.\""},{"word":"cavity","def":"a hole in a tooth","hint":"\"…you can get a <b>cavity</b>, which is a hole in a tooth.\""},{"word":"dentist","def":"a doctor for your teeth","hint":"\"A <b>dentist</b> checks your teeth…\""}],
 "bank":["teeth","brush","toothpaste","healthy","cavity","dentist"],
 "fills":[{"text":"I clean my ___ every morning.","a":"teeth"},{"text":"I ___ my teeth before bed.","a":"brush"},{"text":"Put mint ___ on the brush.","a":"toothpaste"},{"text":"Brushing keeps me ___.","a":"healthy"},{"text":"Too much candy can cause a ___.","a":"cavity"},{"text":"The ___ counted all my teeth.","a":"dentist"}]},

{"activityId":"seasons","projectKey":"seasons","name":"Dani","hubKey":"daniReading","hubFile":"dani.html","useLead":"Tap a word to fill the blank, or type it. You can do it!","title":"The Four Seasons","heroEmoji":"🍂","watermark":"❄️","pageTitle":"The Seasons",
 "win":"PERFECT, Dani! All four seasons! 🍂","cheer":"You bloomed, Dani! 🌸",
 "palette":{"primary":"#8e57b8","dark":"#6f4392","deep":"#492c60","accent":"#bb93d8","accentSoft":"#ece1f4","cream":"#fbf8fd","bgTop":"#f3ecf9","bgBottom":"#eae0f2","glow1":"#8e57b822","glow2":"#492c6018"},
 "passageTitle":"The Four Seasons",
 "passageHtml":"<p>There are four <span class=\"voc\">season</span>s in a year. In <span class=\"voc\">spring</span>, flowers begin to grow. In <span class=\"voc\">summer</span>, the days are hot and sunny. We swim and play outside.</p><p>In <span class=\"voc\">autumn</span>, the leaves turn orange and fall down. In <span class=\"voc\">winter</span>, it is cold and it may snow. Each season has its own <span class=\"voc\">weather</span>. The seasons change all year long.</p>",
 "questions":[{"type":"Main idea","q":"This is mostly about —","opts":["the ocean","the four seasons","trucks"],"a":1},{"type":"Detail","q":"How many seasons are there?","opts":["four","two","ten"],"a":0},{"type":"Detail","q":"In summer the days are —","opts":["hot and sunny","snowy","dark all day"],"a":0},{"type":"Detail","q":"In autumn the leaves —","opts":["fall down","grow blue","disappear"],"a":0},{"type":"Vocabulary","q":"\"Weather\" is —","opts":["what the sky and air are doing","a kind of leaf","a season name"],"a":0}],
 "match":[{"word":"spring","def":"the season when flowers grow","hint":"\"In <b>spring</b>, flowers begin to grow.\""},{"word":"summer","def":"the hot, sunny season","hint":"\"In <b>summer</b>, the days are hot and sunny.\""},{"word":"autumn","def":"the season when leaves fall","hint":"\"In <b>autumn</b>, the leaves turn orange and fall.\""},{"word":"winter","def":"the cold, snowy season","hint":"\"In <b>winter</b>, it is cold and it may snow.\""},{"word":"weather","def":"what the sky and air are doing","hint":"\"Each season has its own <b>weather</b>.\""}],
 "bank":["season","spring","summer","autumn","winter","weather"],
 "fills":[{"text":"There are four ___s in a year.","a":"season"},{"text":"Flowers bloom in the ___.","a":"spring"},{"text":"We swim in the hot ___.","a":"summer"},{"text":"Leaves fall in the ___.","a":"autumn"},{"text":"It snows in the ___.","a":"winter"},{"text":"The ___ today is sunny.","a":"weather"}]}
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
