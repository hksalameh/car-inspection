from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v-day2"' in s:
    print('Day 2 already present')
    raise SystemExit(0)

# Admin tabs.
old = '''  <section class="sec"><div class="card"><div class="tabs"><button id="tabg" class="tab on" onclick="adminMode('g')">① عام</button><button id="tabw" class="tab" onclick="adminMode('w')">② مجال العمل</button></div></div></section>'''
new = '''  <section class="sec"><div class="card"><div class="tabs"><button id="tabg" class="tab on" onclick="adminMode('g')">① الجلسة الأولى</button><button id="tabd2" class="tab" onclick="adminMode('d2')">② الجلسة الثانية</button><button id="tabw" class="tab" onclick="adminMode('w')">③ مجال العمل</button></div></div></section>'''
if old not in s:
    raise SystemExit('Admin tabs anchor not found')
s = s.replace(old, new, 1)
s = s.replace('.tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px}', '.tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}', 1)

# Participant view.
anchor = '  <div id="v-roles" class="hide">'
day2_html = '''  <div id="v-day2" class="hide">
    <span class="tag">🚀 الجلسة الثانية</span><span id="d2count" class="count"></span>
    <div class="qhead"><div id="d2title" class="qtitle"></div><div id="d2sub" class="qsub"></div></div>
    <div id="d2body"></div>
  </div>

'''
if anchor not in s:
    raise SystemExit('Participant anchor not found')
s = s.replace(anchor, day2_html + anchor, 1)

# Admin guided section.
anchor2 = '  <section id="aw" class="sec hide"><div class="card">'
day2_admin = '''  <section id="ad2" class="sec hide"><div class="card">
    <div class="qhead"><div class="qtitle">مش بس اسأله… خلّيه يفكّر معك</div><div class="qsub">كل ما تحتاجه لتقديم الجلسة أمامك هنا، والموظفون يرون فقط النشاط الذي تنشره.</div></div>
    <label>الفقرة الحالية</label><select id="d2sel" onchange="previewDay2Admin()"></select>
    <div id="d2guide" class="facGuide"></div>
    <div class="navBtns"><button class="btn outline" onclick="prevDay2()">السابق</button><button class="btn outline" onclick="nextDay2()">التالي</button><button class="btn primary" onclick="showDay2()">عرض هذه الفقرة</button></div>
    <div class="actions"><button class="btn secondary" onclick="hideAll()">إخفاء المحتوى عن الحضور</button></div>
  </div></section>

'''
if anchor2 not in s:
    raise SystemExit('Admin section anchor not found')
s = s.replace(anchor2, day2_admin + anchor2, 1)

# CSS.
css = '''
.day2Hero{padding:18px;border-radius:18px;background:linear-gradient(135deg,#172b58,#315fce);color:#fff;margin:10px 0}.day2Hero h2{margin:0 0 5px;font-size:22px}.day2Hero p{margin:0;opacity:.94;font-size:13px}
.powerGrid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:12px}.powerCard{padding:12px;border:1px solid var(--line);border-radius:14px;background:#fff}.powerCard b{display:block;font-size:14px}.powerCard span{display:block;color:var(--muted);font-size:11px;margin-top:2px}
.d2Prompt{margin-top:11px;padding:14px;border:1px solid #dbe4fb;background:#f8fbff;border-radius:15px}.d2Prompt .label{font-size:11px;font-weight:900;color:var(--brand);margin-bottom:5px}.d2Prompt .txt{font-size:16px;font-weight:800;white-space:pre-wrap}.d2Hint{margin-top:10px;padding:10px 12px;background:#fff8e9;border:1px solid #f0ddb3;border-radius:12px;color:#795400;font-size:12px}
.d2ChoiceGrid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:12px}.d2Choice{border:1px solid var(--line);background:#fff;border-radius:13px;padding:12px;text-align:right;font-weight:900}.d2Choice.on{border-color:var(--brand);background:var(--brand-soft);color:var(--brand)}
.facGuide{margin-top:12px}.facTop{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}.facPill{padding:6px 9px;border-radius:999px;background:var(--brand-soft);color:var(--brand);font-size:11px;font-weight:900}.facBlock{margin-top:8px;padding:12px;border-radius:13px;border:1px solid var(--line);background:#fbfcfe}.facBlock b{display:block;margin-bottom:4px;font-size:13px}.facBlock p{margin:0;color:#475467;font-size:13px;white-space:pre-wrap}.facSay{background:#f4fbf8;border-color:#d9f0e6}.facDiscuss{background:#fff8e9;border-color:#f0ddb3}
@media(max-width:460px){.powerGrid,.d2ChoiceGrid{grid-template-columns:1fr}.tabs{grid-template-columns:1fr}.tabs .tab{padding:9px 6px;font-size:12px}}
'''
if '.privacy{' not in s:
    raise SystemExit('CSS anchor not found')
s = s.replace('.privacy{', css + '\n.privacy{', 1)

# Data for the second session.
jsdata = '''
var DAY2_BASE=20;
var DAY2=[
{icon:'🎬',title:'افتتاحية: مش بس اسأله… خلّيه يفكّر معك',minutes:'5 دقائق',kind:'intro',sub:'اليوم سنستخدم الذكاء الاصطناعي بست طرق مختلفة، وليس فقط للحصول على جواب.',say:'أمس جرّبنا كيف الذكاء الاصطناعي يجاوبنا. اليوم بدنا نخليه يسألنا، يعارضنا، يصنع لنا أدوات، يغيّر أسلوب الكلام، ويراجع نفسه.',doit:'خليهم فقط يتابعوا الفكرة، ولا تطلب منهم كتابة أي شيء.',discuss:'اسألهم بسرعة: برأيكم، هل الذكاء الاصطناعي مجرد مكان نسأله أسئلة؟',take:'الفكرة الأساسية: قيمة الذكاء الاصطناعي تزيد عندما نعطيه دورًا وطريقة عمل، وليس سؤالًا فقط.'},
{icon:'🧠',title:'القوة الأولى: خليه يسألك',minutes:'8 دقائق',kind:'single',sub:'بدل أن تطلب الحل مباشرة، خليه يفهمك أولًا.',prompt:'لدي يوم مزدحم ومهام كثيرة. لا تعطيني خطة الآن. اسألني 5 أسئلة فقط تساعدك على فهم وقتي وأولوياتي، وبعد أن أجيبك ساعدني في ترتيب يومي.',say:'اليوم أول مرة ما بدنا الذكاء الاصطناعي يجاوبنا مباشرة. بدنا هو يسألنا.',doit:'الموظف ينسخ السؤال الجاهز ويفتح ChatGPT. يقرأ الأسئلة التي رجعت له فقط.',discuss:'هل سألك عن شيء ما كنت منتبه له؟',take:'أحيانًا أفضل فائدة من الذكاء الاصطناعي هي السؤال الذي يجعلك تفكر.'},
{icon:'🪞',title:'القوة الثانية: خليه يعارضك',minutes:'8 دقائق',kind:'single',sub:'استخدمه ليكشف نقاط الضعف في فكرتك، لا ليوافقك فقط.',prompt:'أفكر بإلغاء الاجتماع الأسبوعي للموظفين واستبداله برسائل واتساب. لا توافقني مباشرة. أعطني 5 مشاكل أو مخاطر قد تنتج عن هذا القرار، ثم اقترح حلًا وسطًا.',say:'لو وافقنا الذكاء الاصطناعي على كل شيء نقوله، فائدته محدودة. الآن بدنا نخليه يعارضنا.',doit:'خلي الجميع ينسخوا نفس السؤال ويقارنوا المخاطر والحل الوسط الذي ظهر لهم.',discuss:'هل ذكر مشكلة ما كانت على بالك؟',take:'قبل قرار مهم، اطلب منه أن يبحث عن الشيء الذي ربما لا تراه.'},
{icon:'🛠️',title:'القوة الثالثة: خليه يصنع لك أداة',minutes:'10 دقائق',kind:'tool',sub:'هذه المرة لا نريد معلومة؛ نريد شيئًا نستخدمه في العمل.',say:'ممنوع نطلب منه معلومة الآن. كل واحد سيأخذ منه أداة بسيطة تناسب شغله.',doit:'كل موظف يرى سؤالًا مناسبًا لمجاله الذي اختاره سابقًا. ينسخه ويشاهد النموذج الذي ينشئه الذكاء الاصطناعي.',discuss:'هل النموذج الناتج يصلح أن تستخدمه فعلًا؟ وما الخانة التي يمكن تعديلها؟',take:'الذكاء الاصطناعي لا يعطي معلومات فقط؛ يمكنه بناء قوالب وقوائم ونماذج عمل خلال دقيقة.'},
{icon:'🎭',title:'القوة الرابعة: نفس المعلومة لثلاثة أشخاص',minutes:'8 دقائق',kind:'single',sub:'المعلومة ثابتة، لكن أسلوب التواصل يتغير حسب الشخص.',prompt:'المعلومة هي: سيتم إيقاف النظام غدًا من الساعة 10 إلى 12 بسبب أعمال الصيانة. اكتبها بثلاث طرق: 1) رسالة رسمية للموظفين، 2) رسالة واتساب قصيرة جدًا، 3) شرح بسيط لشخص كبير في السن لا يعرف شيئًا عن الأنظمة الإلكترونية.',say:'الذكاء الاصطناعي مش بس يكتب؛ يقدر يغيّر طريقة الكلام حسب الشخص اللي قدامك.',doit:'خليهم ينسخوا السؤال ويقارنوا النسخ الثلاث.',discuss:'هل المعلومة تغيّرت؟ أم الذي تغيّر هو طريقة إيصالها؟',take:'حدد دائمًا لمن تكتب، لأن الجمهور يغير الأسلوب والطول والكلمات.'},
{icon:'🔍',title:'القوة الخامسة: صدّق أو لا تصدّق',minutes:'8 دقائق',kind:'verify',sub:'سنجرب كيف نطلب منه مراجعة نفسه بدل أن نصدق أول جواب.',p1:'من هو الشخص الذي اخترع الإنترنت؟ أعطني اسمه والسنة التي اخترعه فيها.',p2:'راجع إجابتك السابقة نقديًا. ما الأجزاء التي قد تكون مبسطة أو غير دقيقة؟ وما الذي يجب أن أتحقق منه من مصدر موثوق؟',say:'الآن رح نحاول نوقع الذكاء الاصطناعي في التبسيط أو الخطأ. لا نريد حفظ الجواب؛ نريد نتعلم كيف نتحقق.',doit:'انسخوا السؤال الأول، اقرأوا الجواب، ثم انسخوا السؤال الثاني في نفس المحادثة.',discuss:'هل تغيرت نبرة الإجابة الثانية؟ وهل اعترف أن الموضوع أعقد؟',take:'معلومة مهمة + صحة + مال + قانون + قرار مهم = تحقق من مصدر آخر.'},
{icon:'🚀',title:'القوة السادسة: حوار من 3 خطوات',minutes:'10 دقائق',kind:'challenge',sub:'اختر حالة جاهزة، ثم استخدم الذكاء الاصطناعي كحوار متدرج بدون كتابة داخل الموقع.',say:'آخر تجربة: مش رح نعطيه أمر واحد. رح نمشي معه بثلاث خطوات: يفهم، يقارن، ثم يحول الحل إلى خطة.',doit:'الموظف يختار حالة جاهزة بكبسة واحدة، ثم ينسخ الخطوات الثلاث بالتتابع إلى نفس محادثة ChatGPT.',discuss:'هل النتيجة النهائية أفضل من لو سألته من البداية: أعطني الحل؟',take:'كلما كان الحوار متدرجًا، صار الذكاء الاصطناعي أقرب إلى مساعد يفهم السياق بدل ماكينة إجابات.'},
{icon:'🏁',title:'الخلاصة: ست قوى جديدة',minutes:'3 دقائق',kind:'recap',sub:'هذه ليست أوامر للحفظ؛ هي ست طرق تفكير في استخدام الذكاء الاصطناعي.',say:'إذا طلعتوا بفكرة واحدة: الذكاء الاصطناعي مش بديل عن عقلك؛ هو أداة توسّع عقلك.',doit:'اعرض الخلاصة، ثم اسأل كل شخص بجملة قصيرة: ما أول شيء ستستخدم فيه واحدة من هذه القوى؟',discuss:'ما القوة التي شعرت أنها مفيدة لك أكثر؟',take:'اسأله — خليه يسألك — خليه يعارضك — خليه يبني — خليه يغيّر الأسلوب — وخليه يراجع نفسه.'}
];
var DAY2_TOOLS={
'مدير':'أنشئ لي نموذج متابعة أسبوعية للموظفين يكون بسيطًا جدًا ويتكون من: المهمة، المسؤول، الموعد، الحالة، والملاحظة.',
'باحث اجتماعي':'أنشئ لي نموذجًا مختصرًا لتسجيل ملاحظات زيارة اجتماعية، بدون أسماء أو بيانات شخصية، يساعدني على ترتيب الاحتياجات والمتابعة.',
'سائق':'أنشئ لي قائمة فحص يومية للمركبة قبل الانطلاق، لا تتجاوز 10 نقاط، ورتبها حسب الأهمية.',
'مراسل':'أنشئ لي نموذج متابعة يومية للمهام يحتوي: المهمة، الجهة، الأولوية، وهل تم التنفيذ.',
'منسق العشوائيات':'أنشئ لي نموذجًا بسيطًا لتصنيف الاحتياجات إلى عاجلة ومتوسطة وغير عاجلة، مع خانة للإجراء المطلوب.'
};
var DAY2_CASES=[
{icon:'📋',name:'ترتيب مهام',p:'لدي عدة مهام اليوم ولا أعرف من أين أبدأ. لا تعطيني الحل مباشرة. اسألني أهم 4 أسئلة تحتاجها حتى تساعدني على ترتيب الأولويات.'},
{icon:'💬',name:'رسالة صعبة',p:'أحتاج أن أكتب رسالة محترمة لشخص في موضوع حساس. لا تكتب الرسالة الآن. اسألني 4 أسئلة فقط حتى تفهم الموقف والنبرة المناسبة.'},
{icon:'⚖️',name:'قرار بين خيارين',p:'لدي خياران وأريد أن أقرر بينهما. لا تقل لي أيهما أفضل الآن. اسألني 4 أسئلة تساعدك على فهم ما يهمني قبل المقارنة.'},
{icon:'📚',name:'تعلّم شيء',p:'أريد أن أتعلم موضوعًا جديدًا لكن وقتي محدود. لا تضع خطة الآن. اسألني 4 أسئلة تساعدك على معرفة مستواي ووقتي وهدفي.'}
];
var d2Case=-1;
var d2Prompts=[];
'''
if 'var ROLE_INFO={' not in s:
    raise SystemExit('JS data anchor not found')
s = s.replace('var ROLE_INFO={', jsdata + '\nvar ROLE_INFO={', 1)

# JS functions.
jsfunc = '''
function copyRawText(t){if(!t)return;try{if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(function(){toast('تم النسخ ✓')})}else{throw new Error('fallback')}}catch(e){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.focus();a.select();document.execCommand('copy');a.remove();toast('تم النسخ ✓')}}
function copyD2Prompt(i){copyRawText(d2Prompts[i]||'')}
function day2PromptCard(label,text,btn){var i=d2Prompts.push(text)-1;return '<div class="d2Prompt"><div class="label">'+label+'</div><div class="txt">'+text+'</div><div class="actions"><button class="btn primary" onclick="copyD2Prompt('+i+')">📋 '+btn+'</button><button class="btn outline" onclick="openAI()">فتح ChatGPT ↗</button></div></div>'}
function chooseD2Case(i){d2Case=i;renderDay2(DAY2.length-2)}
function renderDay2(i){
  var x=DAY2[i]||DAY2[0],body='',n=i+1;d2Prompts=[];
  $('d2title').textContent=x.icon+' '+x.title;$('d2sub').textContent=x.sub||'';$('d2count').textContent=n+' من '+DAY2.length;
  if(x.kind==='intro'){
    body='<div class="day2Hero"><h2>مش بس اسأله… خلّيه يفكّر معك</h2><p>اليوم ستكتشف أن الذكاء الاصطناعي يمكن أن يكون مدرّبًا، ناقدًا، صانع أدوات، محررًا، ومدققًا.</p></div><div class="powerGrid"><div class="powerCard"><b>🧠 يسألك</b><span>يساعدك على التفكير</span></div><div class="powerCard"><b>🪞 يعارضك</b><span>يكشف نقاط الضعف</span></div><div class="powerCard"><b>🛠️ يبني</b><span>يصنع أداة للعمل</span></div><div class="powerCard"><b>🎭 يغيّر الأسلوب</b><span>حسب الشخص</span></div><div class="powerCard"><b>🔍 يراجع نفسه</b><span>لا تصدق أول جواب</span></div><div class="powerCard"><b>🚀 يتحاور معك</b><span>خطوة بعد خطوة</span></div></div>';
  }else if(x.kind==='single'){
    body=day2PromptCard('السؤال الجاهز للنسخ',x.prompt,'نسخ السؤال')+'<div class="d2Hint">بعد التجربة، ارجع إلى هذه الصفحة وانتظر النقاش مع المجموعة.</div>';
  }else if(x.kind==='tool'){
    if(!role||!DAY2_TOOLS[role]){body='<div class="wait"><div class="waitIco">👤</div><h2>اختر مجال عملك أولًا</h2><p>سنجهز لك سؤالًا يناسب طبيعة عملك.</p><button class="btn primary" onclick="openRoleSwitch()">اختيار مجال العمل</button></div>'}
    else{body='<div class="chosen"><div><b>مجالك الحالي: '+role+'</b><div class="small">يمكنك تغييره متى أردت.</div></div><button class="btn outline" onclick="openRoleSwitch()">تغيير</button></div>'+day2PromptCard('أداة تناسب عملك',DAY2_TOOLS[role],'نسخ الطلب')}
  }else if(x.kind==='verify'){
    body=day2PromptCard('الخطوة 1 — اسأل',x.p1,'نسخ السؤال الأول')+day2PromptCard('الخطوة 2 — خليه يراجع نفسه',x.p2,'نسخ سؤال المراجعة')+'<div class="d2Hint"><b>القاعدة:</b> معلومة مهمة، صحة، مال، قانون، أو قرار مهم = تحقق من مصدر موثوق.</div>';
  }else if(x.kind==='challenge'){
    body='<div class="d2Hint">اختر حالة واحدة فقط. لا تحتاج أن تكتب شيئًا داخل الموقع.</div><div class="d2ChoiceGrid">'+DAY2_CASES.map(function(c,j){return '<button class="d2Choice '+(d2Case===j?'on':'')+'" onclick="chooseD2Case('+j+')">'+c.icon+' '+c.name+'</button>'}).join('')+'</div>';
    if(d2Case>=0){var c=DAY2_CASES[d2Case];body+=day2PromptCard('الخطوة 1 — افهمني أولًا',c.p,'نسخ الخطوة الأولى')+day2PromptCard('الخطوة 2 — أعطني خيارات','بناءً على إجاباتي السابقة، أعطني 3 حلول مختلفة، واشرح ميزة وعيب كل حل.','نسخ الخطوة الثانية')+day2PromptCard('الخطوة 3 — حوله إلى خطة','اختر الحل الأبسط والأكثر واقعية، وحوّله إلى 3 خطوات أستطيع البدء بها اليوم.','نسخ الخطوة الثالثة')}
  }else if(x.kind==='recap'){
    body='<div class="powerGrid"><div class="powerCard"><b>🧠 قوة السؤال</b><span>خليه يسألك</span></div><div class="powerCard"><b>🪞 قوة النقد</b><span>خليه يعارضك</span></div><div class="powerCard"><b>🛠️ قوة البناء</b><span>خليه يصنع لك أداة</span></div><div class="powerCard"><b>🎭 قوة الأسلوب</b><span>غيّر الرسالة حسب الشخص</span></div><div class="powerCard"><b>🔍 قوة التحقق</b><span>خليه يراجع نفسه</span></div><div class="powerCard"><b>🚀 قوة الحوار</b><span>تدرج معه خطوة بخطوة</span></div></div><div class="goal"><b>الفكرة الأخيرة:</b> الذكاء الاصطناعي مش بديل عن عقلك؛ هو أداة توسّع عقلك.</div>';
  }
  $('d2body').innerHTML=body;
}
function fillDay2(){$('d2sel').innerHTML=DAY2.map(function(x,i){return '<option value="'+i+'">'+(i+1)+'. '+x.title+'</option>'}).join('');previewDay2Admin()}
function previewDay2Admin(){var i=+$('d2sel').value,x=DAY2[i]||DAY2[0];$('d2guide').innerHTML='<div class="facTop"><span class="facPill">'+x.icon+' الفقرة '+(i+1)+'</span><span class="facPill">⏱ '+x.minutes+'</span></div><div class="facBlock facSay"><b>🗣️ قل لهم</b><p>'+x.say+'</p></div><div class="facBlock"><b>👥 ماذا يفعل الموظفون؟</b><p>'+x.doit+'</p></div><div class="facBlock facDiscuss"><b>💬 سؤال النقاش بعد التجربة</b><p>'+x.discuss+'</p></div><div class="facBlock"><b>🎯 الفكرة التي تريد تثبيتها</b><p>'+x.take+'</p></div>'}
function prevDay2(){var z=$('d2sel');z.value=Math.max(0,+z.value-1);previewDay2Admin()}
function nextDay2(){var z=$('d2sel');z.value=Math.min(DAY2.length-1,+z.value+1);previewDay2Admin()}
function showDay2(){update({screen:'general',generalIndex:DAY2_BASE+(+$('d2sel').value),specialIndex:state.specialIndex})}
'''
if 'function hideViews(){' not in s:
    raise SystemExit('JS function anchor not found')
s = s.replace('function hideViews(){', jsfunc + '\nfunction hideViews(){', 1)
s = s.replace("['v-wait','v-general','v-roles','v-special']", "['v-wait','v-general','v-day2','v-roles','v-special']", 1)

oldrender = "  if(state.screen==='general'){var q=GENERAL[state.generalIndex]||GENERAL[0];$('v-general').classList.remove('hide');$('gt').textContent=q[0];$('gq').textContent=q[1];$('gg').innerHTML=q[2];$('gcount').textContent='سؤال '+(state.generalIndex+1)+' من '+GENERAL.length;$('status').textContent='عام — سؤال '+(state.generalIndex+1);$('lifeDemo').classList.toggle('hide',state.generalIndex!==1);if(state.generalIndex===1)resetLifePrompt()}"
newrender = "  if(state.screen==='general'){if(state.generalIndex>=DAY2_BASE&&state.generalIndex<DAY2_BASE+DAY2.length){var di=state.generalIndex-DAY2_BASE;$('v-day2').classList.remove('hide');$('status').textContent='الجلسة الثانية — الفقرة '+(di+1);renderDay2(di)}else{var q=GENERAL[state.generalIndex]||GENERAL[0];$('v-general').classList.remove('hide');$('gt').textContent=q[0];$('gq').textContent=q[1];$('gg').innerHTML=q[2];$('gcount').textContent='سؤال '+(state.generalIndex+1)+' من '+GENERAL.length;$('status').textContent='الجلسة الأولى — سؤال '+(state.generalIndex+1);$('lifeDemo').classList.toggle('hide',state.generalIndex!==1);if(state.generalIndex===1)resetLifePrompt()}}"
if oldrender not in s:
    raise SystemExit('Render anchor not found')
s = s.replace(oldrender, newrender, 1)

oldmode = "function adminMode(m){$('ag').classList.toggle('hide',m!=='g');$('aw').classList.toggle('hide',m!=='w');$('tabg').classList.toggle('on',m==='g');$('tabw').classList.toggle('on',m==='w')}"
newmode = "function adminMode(m){$('ag').classList.toggle('hide',m!=='g');$('ad2').classList.toggle('hide',m!=='d2');$('aw').classList.toggle('hide',m!=='w');$('tabg').classList.toggle('on',m==='g');$('tabd2').classList.toggle('on',m==='d2');$('tabw').classList.toggle('on',m==='w')}"
if oldmode not in s:
    raise SystemExit('Admin mode anchor not found')
s = s.replace(oldmode, newmode, 1)

oldlive = "function syncLive(){var t='لا يوجد شيء ظاهر الآن',on=false;if(state.screen==='general'){t='الحضور يرون الآن: عام — سؤال '+(state.generalIndex+1);on=true}if(state.screen==='roles'){t='الحضور يرون الآن: اختيار مجال العمل';on=true}if(state.screen==='special'){t='الحضور يرون الآن: مثال تخصصي رقم '+(state.specialIndex+1);on=true}$('live').textContent=t;$('dot').classList.toggle('on',on)}"
newlive = "function syncLive(){var t='لا يوجد شيء ظاهر الآن',on=false;if(state.screen==='general'){if(state.generalIndex>=DAY2_BASE&&state.generalIndex<DAY2_BASE+DAY2.length){t='الحضور يرون الآن: الجلسة الثانية — '+DAY2[state.generalIndex-DAY2_BASE].title}else{t='الحضور يرون الآن: الجلسة الأولى — سؤال '+(state.generalIndex+1)}on=true}if(state.screen==='roles'){t='الحضور يرون الآن: اختيار مجال العمل';on=true}if(state.screen==='special'){t='الحضور يرون الآن: مثال تخصصي رقم '+(state.specialIndex+1);on=true}$('live').textContent=t;$('dot').classList.toggle('on',on)}"
if oldlive not in s:
    raise SystemExit('Live state anchor not found')
s = s.replace(oldlive, newlive, 1)

oldprev = "if(state.screen==='general'){var q=GENERAL[state.generalIndex]||GENERAL[0];h='<span class=\"tag\">عام</span><div class=\"miniTitle\">'+q[0]+'</div><div class=\"miniText\">'+q[1]+'</div>'}"
newprev = "if(state.screen==='general'){if(state.generalIndex>=DAY2_BASE&&state.generalIndex<DAY2_BASE+DAY2.length){var dx=DAY2[state.generalIndex-DAY2_BASE];h='<span class=\"tag\">الجلسة الثانية</span><div class=\"miniTitle\">'+dx.icon+' '+dx.title+'</div><div class=\"miniText\">'+dx.sub+'</div>'}else{var q=GENERAL[state.generalIndex]||GENERAL[0];h='<span class=\"tag\">الجلسة الأولى</span><div class=\"miniTitle\">'+q[0]+'</div><div class=\"miniText\">'+q[1]+'</div>'}}"
if oldprev not in s:
    raise SystemExit('Preview anchor not found')
s = s.replace(oldprev, newprev, 1)

oldadmin = "function showAdmin(){$('participant').classList.add('hide');$('admin').classList.remove('hide');$('gsel').value=Math.min(state.generalIndex,GENERAL.length-1);$('ssel').value=Math.min(state.specialIndex,2);previewG();previewSpecialAdmin();syncLive();preview()}"
newadmin = "function showAdmin(){$('participant').classList.add('hide');$('admin').classList.remove('hide');$('gsel').value=Math.min(state.generalIndex,GENERAL.length-1);$('d2sel').value=(state.generalIndex>=DAY2_BASE&&state.generalIndex<DAY2_BASE+DAY2.length)?state.generalIndex-DAY2_BASE:0;$('ssel').value=Math.min(state.specialIndex,2);previewG();previewDay2Admin();previewSpecialAdmin();syncLive();preview()}"
if oldadmin not in s:
    raise SystemExit('Show admin anchor not found')
s = s.replace(oldadmin, newadmin, 1)

init_old = 'fillGeneral();previewSpecialAdmin();renderRoles();render();poll();setInterval(poll,1000);'
init_new = 'fillGeneral();fillDay2();previewSpecialAdmin();renderRoles();render();poll();setInterval(poll,1000);'
if init_old not in s:
    raise SystemExit('Init anchor not found')
s = s.replace(init_old, init_new, 1)

p.write_text(s, encoding='utf-8')
print('Day 2 session added')
