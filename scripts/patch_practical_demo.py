from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css='''
.lifeDemo{margin-top:16px;padding:15px;border:1px solid #d8e4ff;border-radius:17px;background:linear-gradient(180deg,#f9fbff,#fff)}
.lifeHead{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:10px}
.lifeTitle{font-weight:900;font-size:17px}.lifeBadge{font-size:11px;font-weight:900;color:var(--brand);background:var(--brand-soft);padding:5px 8px;border-radius:999px;white-space:nowrap}
.lifeModes{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:9px 0 10px}
.lifeMode{border:1px solid var(--line);background:#fff;border-radius:11px;padding:9px 7px;font-size:12px;font-weight:800;color:#475467}
.lifeMode.on{background:var(--brand-soft);border-color:#bfd0ff;color:var(--brand)}
.lifeDemo textarea{width:100%;min-height:96px;resize:vertical;border:1px solid #cfd8e6;border-radius:12px;padding:11px 12px;background:#fff;font:inherit;line-height:1.6}
.lifeDemo textarea:focus{outline:2px solid #d6e3ff;border-color:#9eb9ff}
.lifeResult{margin-top:10px;padding:12px;border:1px dashed #b9c8e4;border-radius:12px;background:#fff;white-space:pre-wrap;font-size:14px}
.lifeWhy{margin-top:10px;display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.lifeWhy div{padding:8px;border-radius:10px;background:#f8fafc;border:1px solid var(--line);text-align:center;font-size:11px;color:#475467}
@media(max-width:560px){.lifeModes{grid-template-columns:repeat(2,1fr)}.lifeWhy{grid-template-columns:1fr}}
'''
if '.lifeDemo{' not in s:
    s=s.replace('.privacy{',css+'\n.privacy{',1)

html='''

    <div id="lifeDemo" class="lifeDemo hide">
      <div class="lifeHead"><div><div class="lifeTitle">⚡ جرّب كيف يساعدك في حياتك خلال دقيقة</div><div class="small">استخدم المثال كما هو أو غيّر التفاصيل إلى شيء من يومك.</div></div><span class="lifeBadge">تجربة عملية</span></div>
      <div class="lifeModes">
        <button class="lifeMode on" data-life="day" onclick="setLifeMode('day',this)">📅 تنظيم يومي</button>
        <button class="lifeMode" data-life="message" onclick="setLifeMode('message',this)">💬 كتابة رسالة</button>
        <button class="lifeMode" data-life="decision" onclick="setLifeMode('decision',this)">⚖️ قرار ومقارنة</button>
        <button class="lifeMode" data-life="learn" onclick="setLifeMode('learn',this)">📚 تعلّم شيء</button>
      </div>
      <textarea id="lifeInput">غدًا عندي دوام من 8 إلى 3، موعد الساعة 4:30، شراء أغراض للبيت، دفع فاتورة، وأريد 30 دقيقة مشي.</textarea>
      <div class="actions"><button class="btn primary" onclick="buildLifePrompt()">✨ حوّله إلى سؤال ذكي</button></div>
      <div id="lifeResult" class="lifeResult"></div>
      <div class="actions"><button class="btn primary wide" onclick="copyLifePrompt()">📋 نسخ السؤال الناتج</button><button class="btn outline" onclick="openAI()">فتح ChatGPT ↗</button></div>
      <div class="lifeWhy"><div>⏱️ يوفر وقتك</div><div>🧠 يرتب أفكارك</div><div>🔁 يعطيك بدائل بسرعة</div></div>
    </div>'''
anchor='    <div class="how"><div class="howItem"><span>①</span>انسخ السؤال</div><div class="howItem"><span>②</span>الصقه في ChatGPT</div><div class="howItem"><span>③</span>اقرأ النتيجة وناقشها</div></div>'
if 'id="lifeDemo"' not in s:
    s=s.replace(anchor,anchor+html,1)

demo_item="['تجربة 60 ثانية: مساعدك اليومي','لدي غدًا: دوام من 8 إلى 3، موعد الساعة 4:30، شراء أغراض للبيت، دفع فاتورة، وأريد 30 دقيقة مشي. ساعدني في ترتيب يومي بشكل واقعي، وضع وقتًا احتياطيًا، ثم أخبرني ما الذي يمكن تأجيله إذا ضاق الوقت.','<b>الهدف:</b> أن ترى عمليًا أن الذكاء الاصطناعي ليس للعمل فقط؛ يمكنه تنظيم يومك، ترتيب أولوياتك، ومساعدتك على التفكير بسرعة.'],\n"
first_item="['ما هو الذكاء الاصطناعي؟','اشرح لي ببساطة شديدة، وكأنك تشرح لموظف لا يعرف شيئًا عن الذكاء الاصطناعي: ما هو الذكاء الاصطناعي؟ وما 5 أمثلة عملية يمكن أن يفيد بها موظفًا في عمله اليومي؟','<b>الهدف:</b> التعرف على الفكرة من خلال أمثلة قريبة من الحياة والعمل.'],\n"
if 'تجربة 60 ثانية: مساعدك اليومي' not in s:
    s=s.replace(first_item,first_item+demo_item,1)

funcs=r'''var lifeMode='day';
function setLifeMode(mode,btn){
  lifeMode=mode;
  Array.from(document.querySelectorAll('.lifeMode')).forEach(function(b){b.classList.remove('on')});
  if(btn)btn.classList.add('on');
  var input=$('lifeInput');
  if(mode==='day')input.value='غدًا عندي دوام من 8 إلى 3، موعد الساعة 4:30، شراء أغراض للبيت، دفع فاتورة، وأريد 30 دقيقة مشي.';
  if(mode==='message')input.value='أريد أن أعتذر لصديق عن عدم قدرتي على حضور مناسبة اليوم بدون أن يكون الكلام رسميًا أو باردًا.';
  if(mode==='decision')input.value='أفكر هل أشتري هاتفًا جديدًا الآن أم أنتظر 3 أشهر. يهمني السعر والبطارية والكاميرا.';
  if(mode==='learn')input.value='أريد أن أفهم أساسيات الذكاء الاصطناعي بطريقة بسيطة خلال أسبوع، ووقتي المتاح 20 دقيقة يوميًا.';
  buildLifePrompt();
}
function lifePromptText(){
  var x=($('lifeInput').value||'').trim();
  if(!x)return '';
  if(lifeMode==='day')return 'ساعدني كمساعد شخصي في تنظيم هذا اليوم: '+x+' رتّب المهام حسب الأولوية والوقت، اقترح جدولًا واقعيًا مع وقت احتياطي، واذكر ما الذي يمكن تأجيله إذا ضاق الوقت.';
  if(lifeMode==='message')return 'اكتب لي رسالة طبيعية ومهذبة اعتمادًا على هذه الفكرة: '+x+' اجعلها قصيرة وواضحة وغير رسمية أكثر من اللازم، وأعطني نسختين أختار بينهما.';
  if(lifeMode==='decision')return 'ساعدني على التفكير في هذا القرار بدون أن تقرر بدلًا مني: '+x+' اعمل مقارنة بسيطة بين الخيارات، اذكر الإيجابيات والسلبيات، ثم اسألني 3 أسئلة مهمة تساعدني على اتخاذ القرار.';
  return 'أريد أن أتعلم هذا الموضوع: '+x+' اشرحه لي ببساطة، ثم ضع لي خطة قصيرة خطوة بخطوة، مع مثال عملي وتمرين صغير أتأكد به أنني فهمت.';
}
function buildLifePrompt(){var t=lifePromptText();$('lifeResult').textContent=t||'اكتب موقفًا بسيطًا من حياتك أولًا.'}
async function copyLifePrompt(){
  var t=lifePromptText();
  if(!t){toast('اكتب مثالًا أولًا');return}
  try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(t)}else{throw new Error('fallback')}}catch(e){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.focus();a.select();a.setSelectionRange(0,a.value.length);document.execCommand('copy');a.remove()}
  toast('تم نسخ السؤال العملي');
}
'''
openai="function openAI(){window.open('https://chatgpt.com/','_blank','noopener')}\n"
if "var lifeMode='day';" not in s:
    s=s.replace(openai,openai+funcs,1)

old="if(state.screen==='general'){var q=GENERAL[state.generalIndex]||GENERAL[0];$('v-general').classList.remove('hide');$('gt').textContent=q[0];$('gq').textContent=q[1];$('gg').innerHTML=q[2];$('gcount').textContent='سؤال '+(state.generalIndex+1)+' من '+GENERAL.length;$('status').textContent='عام — سؤال '+(state.generalIndex+1)}"
new="if(state.screen==='general'){var q=GENERAL[state.generalIndex]||GENERAL[0];$('v-general').classList.remove('hide');$('gt').textContent=q[0];$('gq').textContent=q[1];$('gg').innerHTML=q[2];$('gcount').textContent='سؤال '+(state.generalIndex+1)+' من '+GENERAL.length;$('status').textContent='عام — سؤال '+(state.generalIndex+1);$('lifeDemo').classList.toggle('hide',state.generalIndex!==1);if(state.generalIndex===1)buildLifePrompt()}"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
