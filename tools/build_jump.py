#!/usr/bin/env python3
"""从 campus.html 派生 jump.html（3D 跳转页）。

为什么是生成而不是手抄：跳转页要复用整个 3D 场景（1395 行、几十个程序化贴图函数），
复制一份迟早会跟 campus.html 漂移。这里做**定向注入**——每一处替换都断言必须命中，
命中不了就报错退出，不会静默产出一个半成品。

跑：/usr/local/bin/python3 tools/build_jump.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "campus.html")
DST = os.path.join(ROOT, "jump.html")
OPEN_SRC = os.path.join(ROOT, "index.html")
OPEN_DST = os.path.join(ROOT, "jump-opening.html")

s = open(SRC, encoding="utf-8").read()
edits = []


def sub(old, new, label):
    global s
    if old not in s:
        print("✗ 锚点没命中：「%s」" % label)
        print("  期望片段：%r" % old[:120])
        sys.exit(1)
    if s.count(old) != 1:
        print("✗ 锚点不唯一（%d 处）：「%s」" % (s.count(old), label))
        sys.exit(1)
    s = s.replace(old, new)
    edits.append(label)


# ── 1. head ─────────────────────────────────────────────
sub('<title>中国奶娃大学 · 校门报到日</title>',
    '<title>正在前往 · 南京传媒学院</title>', "标题")

sub('<meta name="description" content="全程序化建模与光照的 3D 校门报到日场景，可自由漫游。">',
    '<meta name="description" content="中国奶娃大学 → 南京传媒学院，3D 校门报到日跳转。">\n'
    '<meta name="robots" content="noindex">', "描述")

sub('<link rel="icon" href="favicon.ico" sizes="any">',
    '<link rel="icon" href="favicon.ico" sizes="any">\n'
    '<noscript><meta http-equiv="refresh" content="6;url=https://www.cucn.edu.cn/"></noscript>',
    "noscript 兜底")

# ── 2. 跳转页自己的样式 ──────────────────────────────────
JUMP_CSS = """  /* ── 跳转页专用 ── */
  html,body{height:100%;min-height:100%;overflow:hidden;background:#F3EFE5}
  body{display:grid;place-items:center;padding:clamp(12px,2.2vw,34px);color:#18304D;
    background:radial-gradient(ellipse at 50% 45%,#fffdf8 0%,#f5f0e5 70%,#ebe4d5 100%)}
  body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.34;
    background-image:radial-gradient(rgba(27,75,141,.12) .7px,transparent .7px);
    background-size:18px 18px;mask-image:linear-gradient(transparent,#000 22%,#000 78%,transparent)}
  .jump-shell{position:relative;isolation:isolate;width:min(1600px,100%);height:min(1600px,calc(100dvh - 28px));
    min-height:520px;display:grid;grid-template-rows:auto minmax(0,1fr) auto;overflow:hidden;
    background:rgba(255,254,250,.96);border:1px solid rgba(27,75,141,.22);border-radius:14px;
    box-shadow:0 28px 90px rgba(50,58,65,.18),0 4px 14px rgba(27,75,141,.08)}
  .jump-shell::before{content:"";position:absolute;inset:9px;z-index:8;pointer-events:none;
    border:1px solid rgba(27,75,141,.13);border-radius:8px}
  #opening{position:fixed;inset:0;z-index:40;background:#FFFDF6;opacity:1;
    transition:opacity .85s cubic-bezier(.22,.75,.25,1)}
  #opening.out{opacity:0;pointer-events:none}
  #opening iframe{display:block;width:100%;height:100%;border:0}
  #stage-wait{position:fixed;inset:0;z-index:35;display:none;place-items:center;
    background:rgba(245,241,232,.88);backdrop-filter:blur(8px);color:#18304D}
  #stage-wait.on{display:grid}
  #stage-wait p{font-size:12px;letter-spacing:.22em;color:rgba(24,48,77,.66)}
  .bar,.jp,#sub{opacity:0;visibility:hidden;transition:opacity .65s ease,visibility .65s}
  body.stage3d-on .bar,body.stage3d-on .jp,
  body.stage3d-on #sub.on{opacity:1;visibility:visible}
  .bar{position:relative;inset:auto;z-index:3;height:clamp(76px,9.4vh,112px);padding:0 clamp(22px,4vw,62px);
    display:flex;align-items:center;gap:18px;justify-content:flex-start;pointer-events:auto;
    background:linear-gradient(180deg,rgba(255,255,255,.94),rgba(255,254,250,.9));
    border-bottom:1px solid rgba(27,75,141,.14)}
  .brand-seal{width:clamp(42px,5vw,62px);height:clamp(42px,5vw,62px);object-fit:contain;flex:none;
    filter:drop-shadow(0 2px 4px rgba(27,75,141,.13))}
  .brand-copy{min-width:0}
  .bar b{display:block;font-size:clamp(16px,1.8vw,23px);font-weight:700;letter-spacing:.16em;color:#1B4B8D;text-shadow:none}
  .brand-copy small{display:block;margin-top:5px;font-size:clamp(9px,1vw,11px);letter-spacing:.32em;color:#8995A5}
  .bar-spacer{flex:1}
  .bar .destination{display:flex;align-items:center;gap:9px;margin-right:clamp(5px,2vw,26px);
    font-size:clamp(10px,1.1vw,13px);letter-spacing:.1em;color:#66768B}
  .bar .destination i{display:block;width:7px;height:7px;border-radius:50%;background:#C9A227;
    box-shadow:0 0 0 4px rgba(201,162,39,.12)}
  .bar .destination b{display:inline;font-size:inherit;letter-spacing:.04em;color:#1B4B8D}
  .bar .ab{pointer-events:auto;font:inherit;font-size:11px;letter-spacing:.1em;color:#58708F;cursor:pointer;
    border:1px solid rgba(27,75,141,.24);border-radius:99px;padding:8px 15px;background:#fff;
    transition:background .2s,border-color .2s,color .2s}
  .bar .ab:hover{background:#1B4B8D;border-color:#1B4B8D;color:#fff}
  .jump-stage{position:relative;min-height:0;overflow:hidden;isolation:isolate;
    background:linear-gradient(180deg,#B7C9CF 0%,#E7E4D7 49%,#B8B8A2 100%)}
  .jump-stage::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
    background:linear-gradient(90deg,rgba(15,31,48,.12),transparent 16%,transparent 84%,rgba(15,31,48,.12)),
      linear-gradient(0deg,rgba(18,35,52,.16),transparent 22%,transparent 82%,rgba(18,35,52,.11))}
  #gl{position:absolute;inset:0;z-index:0;width:100%;height:100%;display:block;touch-action:none;cursor:grab}
  #gl.drag{cursor:grabbing}
  #sub{position:absolute;top:20px;right:clamp(20px,4vw,58px);z-index:2;left:auto;text-align:right;
    pointer-events:none;opacity:0;transition:opacity .9s ease;padding:11px 15px;
    border:1px solid rgba(255,255,255,.32);border-radius:8px;background:rgba(13,31,49,.42);
    color:#fff;backdrop-filter:blur(10px);box-shadow:0 8px 28px rgba(13,31,49,.15)}
  #sub.on{opacity:1}
  #sub b{display:block;font-size:clamp(13px,1.5vw,17px);font-weight:600;letter-spacing:.1em;
    text-shadow:0 1px 5px rgba(0,0,0,.25)}
  #sub span{display:block;margin-top:5px;font-size:10px;letter-spacing:.2em;color:rgba(255,255,255,.78)}
  .jp{position:relative;left:auto;right:auto;bottom:auto;z-index:3;min-height:clamp(148px,19vh,205px);
    padding:22px clamp(24px,4vw,64px);display:grid;grid-template-columns:minmax(180px,1fr) minmax(260px,1.05fr) auto;
    align-items:center;gap:clamp(18px,3vw,48px);pointer-events:auto;background:#FFFEFA;
    border-top:1px solid rgba(27,75,141,.14)}
  .footer-copy .eyebrow{font-size:10px;letter-spacing:.24em;color:#9A8C6D}
  .footer-copy p{margin-top:8px;font-size:clamp(13px,1.4vw,17px);letter-spacing:.08em;color:#8390A0}
  .footer-copy p b{margin-left:4px;color:#1B4B8D;font-size:1.08em;letter-spacing:.07em}
  .jp-progress{min-width:0}
  .progress-label{display:flex;align-items:center;gap:10px;margin-bottom:10px;color:#728198;
    font-size:11px;letter-spacing:.1em}
  .ring{width:34px;height:34px;flex:none;transform:rotate(-90deg)}
  .ring circle{fill:none;stroke-width:3;stroke-linecap:round}
  .ring .bg{stroke:rgba(27,75,141,.12)}
  .ring .fg{stroke:var(--gold);transition:stroke-dashoffset .18s linear}
  .progress-status{flex:1;color:#1B4B8D;font-weight:600;letter-spacing:.12em}
  .progress-time{font-variant-numeric:tabular-nums;color:#97A1AE}
  .progress-track{height:5px;overflow:hidden;border-radius:99px;background:rgba(27,75,141,.1)}
  .progress-track i{display:block;width:0;height:100%;border-radius:inherit;
    background:linear-gradient(90deg,#8AA4C4,#1B4B8D);transition:width .18s linear}
  .jp .hint{margin-top:9px;font-size:10px;letter-spacing:.09em;color:#A1A9B2}
  .go{pointer-events:auto;white-space:nowrap;font:inherit;font-size:13px;letter-spacing:.1em;color:#fff;
    cursor:pointer;padding:13px 26px;border-radius:99px;border:1px solid #1B4B8D;
    background:#1B4B8D;box-shadow:0 8px 18px rgba(27,75,141,.19);transition:background .2s,transform .12s,box-shadow .2s}
  .go:hover{background:#143B72;box-shadow:0 10px 22px rgba(27,75,141,.26)}
  .go:active{transform:translateY(1px) scale(.98)}
  .hold{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;
    text-align:center;pointer-events:none;opacity:0;transition:opacity .25s}
  .hold.on{opacity:1}
  .hold span{font-size:12px;letter-spacing:.2em;color:#fff;
    background:rgba(8,24,40,.72);padding:9px 18px;border-radius:99px;box-shadow:0 4px 18px rgba(0,0,0,.2)}
  @media (max-width:760px){
    body{padding:9px}
    .jump-shell{height:calc(100dvh - 18px);min-height:0;border-radius:11px}
    .jump-shell::before{inset:6px}
    .bar{height:70px;padding:0 17px;gap:10px}
    .brand-seal{width:42px;height:42px}
    .bar b{font-size:15px;letter-spacing:.1em}
    .brand-copy small{margin-top:3px;font-size:8px;letter-spacing:.2em}
    .bar .destination{display:none}
    .bar .ab{padding:7px 11px;font-size:10px}
    .jp{min-height:148px;padding:15px 19px;grid-template-columns:minmax(0,1fr) auto;gap:9px 14px}
    .footer-copy{grid-column:1/-1}
    .footer-copy .eyebrow{font-size:9px}
    .footer-copy p{margin-top:5px;font-size:13px}
    .progress-label{margin-bottom:7px;gap:7px;font-size:10px}
    .ring{width:28px;height:28px}
    .progress-track{height:4px}
    .jp .hint{margin-top:6px;font-size:9px;letter-spacing:.02em;white-space:nowrap}
    .go{grid-column:2;grid-row:2;padding:11px 17px;font-size:11px}
    #sub{top:12px;right:14px;padding:8px 10px}
    #sub b{font-size:12px}
    #sub span{font-size:9px;margin-top:3px}
  }
  @media (max-width:390px){
    .footer-copy p{font-size:12px}
    .jp{padding-left:14px;padding-right:14px;column-gap:8px}
    .jp .hint{font-size:8px}
    .go{padding:10px 12px}
  }
  @media (max-height:620px) and (min-width:761px){
    .jump-shell{height:calc(100dvh - 20px);min-height:0}
    .bar{height:66px}
    .jp{min-height:126px;padding-top:14px;padding-bottom:14px}
  }
  /* 3D 是整页底景；2D 开场与常驻控件作为轻透玻璃层叠在前面。 */
  html,body{width:100%;height:100%;min-height:0;overflow:hidden;background:#0E1A2B}
  body{display:block;padding:0;color:#18304D;background:#0E1A2B}
  body::before,body::after{display:none}
  .jump-shell,.jump-shell::before{display:none}
  .jump-stage{position:fixed;inset:0;z-index:0;width:100vw;height:100dvh;min-height:0;overflow:hidden;
    background:#0E1A2B}
  .jump-stage::after{background:linear-gradient(90deg,rgba(9,22,36,.12),transparent 20%,transparent 80%,rgba(9,22,36,.12)),
      linear-gradient(0deg,rgba(9,22,36,.22),transparent 24%,transparent 78%,rgba(9,22,36,.08))}
  .bar{position:fixed;inset:0 0 auto;height:clamp(78px,10vh,112px);z-index:6;padding:0 clamp(22px,5vw,76px);
    background:linear-gradient(180deg,rgba(255,253,246,.97),rgba(255,253,246,.84) 68%,rgba(255,253,246,0));
    border:0;pointer-events:auto}
  .jp{position:fixed;inset:auto 0 0;z-index:6;min-height:clamp(148px,19vh,205px);
    padding:24px clamp(22px,5vw,76px) 28px;
    background:linear-gradient(0deg,rgba(255,253,246,.98),rgba(255,253,246,.88) 72%,rgba(255,253,246,0));
    border:0}
  #sub{position:absolute;top:clamp(88px,12vh,136px);right:clamp(22px,5vw,76px);left:auto;z-index:3}
  .hold{position:absolute}
  #opening{background:transparent}
  #opening iframe{background:transparent}
  @media(max-width:760px){
    body{padding:0}
    .bar{height:76px;padding:0 18px;gap:10px}
    .brand-seal{width:42px;height:42px}
    .bar b{font-size:15px;letter-spacing:.1em}
    .brand-copy small{font-size:8px;letter-spacing:.2em}
    .bar .destination{display:none}
    .bar .ab{padding:7px 11px;font-size:10px}
    .jp{min-height:154px;padding:15px 19px 18px;grid-template-columns:minmax(0,1fr) auto;gap:9px 14px}
    .footer-copy{grid-column:1/-1}
    .footer-copy p{margin-top:5px;font-size:13px}
    .progress-label{margin-bottom:7px;gap:7px;font-size:10px}
    .ring{width:28px;height:28px}
    .progress-track{height:4px}
    .jp .hint{margin-top:6px;font-size:9px;letter-spacing:.02em;white-space:nowrap}
    .go{grid-column:2;grid-row:2;padding:11px 17px;font-size:11px}
    #sub{top:84px;right:14px;padding:8px 10px}
    #sub b{font-size:12px}
    #sub span{font-size:9px;margin-top:3px}
  }
  @media(max-width:390px){
    .jp{padding-left:14px;padding-right:14px;column-gap:8px}
    .jp .hint{font-size:8px}
    .go{padding:10px 12px}
  }
  @media(max-height:620px){
    .bar{height:70px}
    .jp{min-height:120px;padding-top:13px;padding-bottom:15px}
    #sub{top:76px}
  }
  @media (prefers-reduced-motion:reduce){#opening{transition-duration:.2s}}
</style>"""
sub("</style>", JUMP_CSS, "跳转页样式")

# ── 3. body：换掉顶部条与 HUD ────────────────────────────
sub('''<div id="opening">
  <iframe id="opening-frame" title="中国奶娃大学校徽开场动画" src="jump-opening.html?embedded=1&amp;campus=1"></iframe>
</div>
<script>
(function(){
  var frame=document.getElementById("opening-frame"),opening=document.getElementById("opening"),done=false;
  window.__campusSequence={phase:"intro",elapsed:0,from:null,redirecting:false};
  var cameraReady=false,openingReady=false,openingStarted=false;
  function startOpening(){
    if(done||!cameraReady||!openingReady||openingStarted)return;
    openingStarted=true;
    frame.contentWindow.postMessage({type:"opening-start"},location.protocol==="file:"?"*":location.origin);
    setTimeout(finishOpening,8000);
  }
  window.__campusStartOpening=function(){cameraReady=true;startOpening();};
  function finishOpening(){
    if(done)return;done=true;opening.classList.add("out");
    setTimeout(function(){
      if(opening.parentNode)opening.parentNode.removeChild(opening);
    },480);
  }
  window.addEventListener("message",function(e){
    if(e.source!==frame.contentWindow||!e.data)return;
    if(e.data.type==="opening-ready"){
      openingReady=true;opening.classList.add("ready");startOpening();return;
    }
    if(e.data.type==="jump-stage")finishOpening();
  });
  frame.addEventListener("load",function(){
    if(done)return;
    if(!opening.classList.contains("ready"))opening.classList.add("ready");
    setTimeout(function(){if(!openingStarted)finishOpening();},12000);
  },{once:true});
  setTimeout(function(){if(!openingStarted)finishOpening();},15000);
})();
</script>''',
    '', "移除校园页开场层")

sub('''<header class="bar">
  <img class="brand-seal" src="assets/badge.webp" alt="中国奶娃大学校徽">
  <div class="brand-copy"><b>中国奶娃大学</b><small>新 生 护 送 中 心 · 校 园 报 到 日</small></div>
  <span class="bar-spacer"></span>
  <div class="destination"><i aria-hidden="true"></i><span>目的地 <b>南京传媒学院</b></span></div>
  <button class="bar-action" id="about-btn" type="button">关于本站</button>
</header>''',
    '', "移除旧顶栏")

sub('<canvas id="gl"></canvas>',
    '<div class="jump-stage" id="stage3d"><canvas id="gl"></canvas>'
    '<div id="sub"><b>南京传媒学院 · 新生报到</b><span>奶娃陪你走进校园</span></div>'
    '<div class="hold" id="hold"><span>已暂停</span></div></div>\n'
    '<header class="bar">'
    '<img class="brand-seal" src="assets/badge.webp" alt="">'
    '<div class="brand-copy"><b>中国奶娃大学</b><small>新 生 护 送 中 心</small></div>'
    '<span class="bar-spacer"></span>'
    '<span class="destination"><i></i>正在护送你前往 <b>南京传媒学院</b></span>'
    '<button class="ab" id="about-btn" type="button">关于本站</button></header>', "建立全屏 3D 底景")

sub("""<footer class="hud">
  <div class="arrival-card">
    <div class="footer-copy">
      <span class="eyebrow">FRESHMAN ARRIVAL · 2026</span>
      <p>奶娃正在护送你前往 <b>南京传媒学院</b></p>
      <p class="tip" id="tip">拖动场景自由探索 · 滚轮或双指缩放</p>
    </div>
    <div class="row">
      <button id="reset" type="button" title="恢复默认视角">回到正门</button>
      <button id="qual" type="button">画质</button>
      <button id="go" class="primary" type="button">前往南传官网 ↗</button>
    </div>
  </div>
</footer>""",
    """<footer class="jp">
  <div class="footer-copy">
    <span class="eyebrow">新 生 报 到 · CAMPUS ARRIVAL</span>
    <p>奶娃正在护送你前往 <b>南京传媒学院</b></p>
  </div>
  <div class="jp-progress">
    <div class="progress-label">
  <svg class="ring" viewBox="0 0 52 52" aria-hidden="true">
    <circle class="bg" cx="26" cy="26" r="23"></circle>
    <circle class="fg" id="ring" cx="26" cy="26" r="23"
            stroke-dasharray="144.5" stroke-dashoffset="144.5"></circle>
  </svg>
      <span class="progress-status" id="phase">护送中</span>
      <span class="progress-time" id="jump-seconds">7.0s</span>
    </div>
    <div class="progress-track"><i id="jump-fill"></i></div>
    <p class="hint" id="tip">轻点画面立即前往 · 长按暂停</p>
  </div>
  <button class="go" id="go" type="button">立即前往 ↗</button>
</footer>
<div id="opening"><iframe id="opening-frame" title="中国奶娃大学开场动画" src="jump-opening.html?embedded=1"></iframe></div>
<script>(function(){var f=document.getElementById("opening-frame"),m=new URLSearchParams(location.search).get("motion");
if(m)f.src="jump-opening.html?embedded=1&motion="+encodeURIComponent(m);})();</script>
<div id="stage-wait"><p>校门正在显影</p></div>""", "上下 UI 与 3D 场景框架")

sub('<div id="load"><div><div class="sp"></div><p>正在打光与烘焙材质</p></div></div>',
    '<div id="load"><div><div class="sp"></div><p>正在搭建校门场景</p></div></div>', "载入文案")

sub('<p>本站与南京传媒学院无任何官方关联，「中国奶娃大学」是虚构校名，仅作趣味用途。</p>',
    '<p>本站与南京传媒学院无任何官方关联，「中国奶娃大学」是虚构校名，仅作趣味用途。'
    '本页看完即跳转至 www.cucn.edu.cn。</p>', "免责声明")

# ── 4. 顶部加 JUMP 标志（必须早于所有引用）────────────────
sub("var JUMP=/[?&]jump/.test(Q);", "var JUMP=true;", "跳转页默认进入动画")

# ── 5. WebGL 起不来 → 退回 2D 版（他选的兜底）────────────
sub("""if(!window.THREE||!probe){
  load.innerHTML='<div><p style="letter-spacing:.05em">这台设备没开 WebGL，3D 场景起不来。<br>'+
    '<a href="index.html" style="color:#C9A227">← 回到护送页（2D 版）</a></p></div>';
  return;
}""",
    """if(!window.THREE||!probe){
  /* WebGL 不可用时继续完整播放同一段 2D 动画，结束后由顶层页面跳转。 */
  var fallbackFrame=document.getElementById("opening-frame");
  if(fallbackFrame){
    var fallbackMotion=new URLSearchParams(Q).get("motion");
    window.addEventListener("message",function(e){
      if(e.origin===location.origin&&e.source===fallbackFrame.contentWindow&&
         e.data&&e.data.type==="jump-target")location.replace("https://www.cucn.edu.cn/");
    });
    fallbackFrame.src="jump-opening.html?embedded=1&fallback=1"+
      (fallbackMotion?"&motion="+encodeURIComponent(fallbackMotion):"");
  }
  load.style.display="none";
  return;
}""", "WebGL 兜底")

# ── 6. 场景侧：捕获脚下 AO、关掉自由漫游推镜、交出控制权 ──
sub("scene.add(ao(3.6,.34,2.05,.05,-4.3));",
    "var heroAO=ao(3.6,.34,2.05,.05,-4.3);scene.add(heroAO);", "捕获脚下 AO")

sub("var intro={t:0,dur:JUMP?3.4:3,on:!JUMP};",
    "var intro={t:0,dur:3.4,on:false};", "关掉自由漫游推镜")

sub("  var amp=intro.on?0:1;", "  var amp=JUMP?0:(intro.on?0:1);", "接管手臂空闲动画")

sub("  applyCam(el);",
    "  if(JUMP)jumpTick(dt);\n  applyCam(el);\n  if(JUMP)jumpCam();   /* 跳转模式直接摆相机，压掉上面的轨道控制器 */",
    "相机上轨道")

sub("  hero.userData.eyes.forEach(function(x){x.scale.y=blink;});",
    "  hero.userData.eyes.forEach(function(x){x.scale.y=blink;});\n  if(JUMP)jumpHero();",
    "角色上轨道")

# ── 7. UI 段：跳转页没有画质/回正按钮，原绑定会 Null 崩 ────
sub("""var hi=hiEnd,usePost=!!composer,qualBtn=document.getElementById("qual");
function paintQual(){qualBtn.textContent="画质："+(hi?(usePost?"后期":"高"):"低");}
paintQual();
qualBtn.addEventListener("click",function(){
  hi=!hi;
  /* 关后期不能只把 pass 全 disable（那样没东西渲染到屏幕），要退回直出 */
  usePost=hi&&!!composer;
  if(composer)composer.passes.forEach(function(p){p.enabled=hi;});
  renderer.shadowMap.enabled=hi;sun.castShadow=hi;
  scene.traverse(function(o){if(o.isMesh)o.material.needsUpdate=true;});
  paintQual();
});
if(!hi){renderer.shadowMap.enabled=false;sun.castShadow=hi;}
document.getElementById("reset").addEventListener("click",function(){
  var delta=Math.atan2(Math.sin(HOME.theta-orb.theta),Math.cos(HOME.theta-orb.theta));
  resetTween={t:0,dur:.8,from:{theta:orb.theta,phi:orb.phi,r:orb.r,
    x:orb.target.x,y:orb.target.y,z:orb.target.z},
    to:{theta:orb.theta+delta,phi:HOME.phi,r:HOME.r,
      x:HOME_TARGET.x,y:HOME_TARGET.y,z:HOME_TARGET.z}};
  intro.on=false;orb.vTheta=0;});
document.getElementById("go").addEventListener("click",function(){location.href="https://www.cucn.edu.cn/";});
var dlg=document.getElementById("about");
document.getElementById("about-btn").addEventListener("click",function(){dlg.showModal();});
document.getElementById("close").addEventListener("click",function(){dlg.close();});
dlg.addEventListener("click",function(e){if(e.target===dlg)dlg.close();});""",
    """/* 跳转页没有「画质 / 回到正门」两个按钮，也不该让别人抢走 #go，
   所以这一段整体换掉（原绑定里 getElementById 会拿到 null 直接抛）。
   注意 usePost 要留着：主循环里 `if(usePost)composer.render()` 在用它，
   整段删掉会变成 ReferenceError，把渲染循环当场打死（表现为"永远不跳转"）。 */
var hi=hiEnd,usePost=!!composer;
if(!hi){renderer.shadowMap.enabled=false;sun.castShadow=hi;}
var dlg=document.getElementById("about");
document.getElementById("about-btn").addEventListener("click",function(){
  jt.paused=true;dlg.showModal();});
document.getElementById("close").addEventListener("click",function(){dlg.close();});
dlg.addEventListener("click",function(e){if(e.target===dlg)dlg.close();});""",
    "UI 段换成跳转版")

# ── 8. 注入跳转模块 ─────────────────────────────────────
JUMP_JS = r"""
/* ══ 99. 跳转模式 ═══════════════════════════════════════
   上轨道的入场：推镜 → 奶娃从画外走入 → 招手 → 鞠躬 → 跳南传。
   时间轴是 t 的纯函数（没有积分状态），所以 ?jump&frame=3.2 能定点截图验收。 */
var TARGET="https://www.cucn.edu.cn/";
var jt={t:0,paused:false,fired:false,started:false,dragTheta:0,dragPhi:0,zoom:1};
/* 相机：一段纯推轨，起终点视线只差约 4°，几乎没有摇镜头，像小摇臂下压。
   P0/L0 直接抄自由漫游已验证过的 HOME 构图当远景。
   为什么要明确摆 camera.position 而不走 orb：轨道控制器的阻尼会把精确机位吃掉。 */
var P0=new T.Vector3(8.0,5.25,10.6), L0=new T.Vector3(0.0,3.7,-12.0);
/* 终点机位压到接近平视（俯角 2.9°）。上一版俯角 9.5°、机位偏到 x=4，
   结果校门整个被报到处帐篷挡掉、背景只剩展板和楼。
   奶娃从报到队伍前方 z=2.4 的空道入场，绕开前排后回到门洞轴线 z=0.6，
   这样它背后就是校门中柱 —— 匾额(≈15.1°)和红横幅(≈12.1°)刚好卡在画幅上沿内。 */
var P1=new T.Vector3(0.0,2.05,10.4), L1=new T.Vector3(0.0,1.52,0.20);
var _jp=new T.Vector3(), _jl=new T.Vector3();
/* 角色先沿队列前方 z=2.4 的空道前进，越过固定队列后再回到门洞轴线；移动行人由碰撞约束避让。
   早期版本把奶娃摆在 (2.05,-5.4) —— 那是报到队伍正中间，
   终点机位等于一头扎进人群，奶娃被裁掉一半、画面全是别人的后脑勺。 */
var H0={x:-5.6,z:2.40,ry:1.57};        /* 画外左起点，走在人群前方，避免穿过报到队伍 */
var H1={x: 0.0,z:0.60,ry:.06};         /* 站位：门洞正前方，终点构图保持不变 */
/* 用肩、肘、腕三个关节制作可复现的分段动作；关键帧时间与跳转时间轴共用秒数。 */
var armMixer=new T.AnimationMixer(hero);
function armTrack(name,keys){
  return new T.NumberKeyframeTrack(name,keys.map(function(k){return k[0];}),
    keys.map(function(k){return k[1];}),T.InterpolateSmooth);
}
var armClip=new T.AnimationClip("奶娃_护送与挥手",7.0,[
  armTrack("ArmRShoulder.rotation[x]",[[0,0],[1.72,0],[1.98,.24],[2.38,-.24],[2.78,.24],
    [3.18,-.23],[3.58,.18],[3.88,0],[4,0],[4.25,-.15],[4.60,-.28],[4.9,-.30],[5.55,-.30],[5.8,-.25],
    [6.08,-.12],[6.32,0],[7,0]]),
  armTrack("ArmRShoulder.rotation[z]",[[0,0],[1.72,0],[1.98,-.045],[2.38,.045],[2.78,-.045],
    [3.18,.04],[3.58,-.025],[3.88,0],[4,0],[4.22,-.40],[4.53,-1.58],
    [4.82,-2.38],[5.60,-2.38],
    [5.82,-1.75],[6.04,-1.0],[6.30,0],[7,0]]),
  armTrack("ArmRElbow.rotation[x]",[[0,0],[1.72,0],[1.98,-.14],[2.38,-.19],[2.78,-.13],
    [3.18,-.18],[3.58,-.12],[3.88,-.12],
    [4,-.12],[4.3,.22],[4.6,.66],[4.85,.78],[5.55,.78],[5.8,.66],
    [6.05,.28],[6.32,-.12],[7,-.12]]),
  armTrack("ArmRWrist.rotation[y]",[[0,0],[4.65,0],[4.86,-.48],[5.02,.50],[5.18,-.52],
    [5.34,.50],[5.50,-.42],[5.68,0],[7,0]]),
  armTrack("ArmLShoulder.rotation[x]",[[0,0],[1.72,0],[1.98,-.22],[2.38,.22],[2.78,-.22],
    [3.18,.21],[3.58,-.16],[3.88,0],[4,0],[7,0]]),
  armTrack("ArmLShoulder.rotation[z]",[[0,0],[1.72,0],[1.98,.035],[2.38,-.035],[2.78,.035],
    [3.18,-.03],[3.58,.02],[3.88,0],[4,0],[7,0]]),
  armTrack("ArmLElbow.rotation[x]",[[0,0],[1.72,0],[1.98,-.14],[2.38,-.18],[2.78,-.12],
    [3.18,-.17],[3.58,-.10],[3.88,-.10],
    [4,-.10],[7,-.10]]),
  armTrack("ArmLWrist.rotation[y]",[[0,0],[4.4,0],[4.9,.06],[5.2,-.06],[5.5,.04],[5.8,0],[7,0]]),
  armTrack("UpperBody.rotation[x]",[[0,0],[5.65,0],[5.92,.045],[6.12,.13],[6.28,.13],
    [6.48,.04],[6.7,0],[7,0]])
]);
var armAction=armMixer.clipAction(armClip);
armAction.setLoop(T.LoopOnce,1);armAction.clampWhenFinished=true;armAction.play();
var HY=hero.position.y;
var DUR=reduce?2.6:7.0;
var STAGE_PENDING=false,STAGE_STARTED=false;
var GATE_TIMED_OUT=false;
var openFrame=document.getElementById("opening-frame");
var opening=document.getElementById("opening");
var stageWait=document.getElementById("stage-wait");
setTimeout(function(){
  if(!GATE_READY){
    GATE_TIMED_OUT=true;GATE_READY=true;
    if(STAGE_PENDING)start3D();
  }
},4200);

function requestStageStart(){
  if(STAGE_STARTED)return;
  STAGE_PENDING=true;
  if(!GATE_READY&&stageWait)stageWait.classList.add("on");
  start3D();
}
/* 文件协议下 iframe 的 load 时序偶尔晚于动画时间轴，交接消息之外再留一个恢复入口。 */
if(openFrame)openFrame.addEventListener("load",function(){
  setTimeout(requestStageStart,3600);
},{once:true});
setTimeout(requestStageStart,7200);

function start3D(){
  if(!STAGE_PENDING||STAGE_STARTED||!GATE_READY)return;
  STAGE_STARTED=true;jt.started=true;
  hero.visible=true;if(heroAO)heroAO.visible=true;
  document.body.classList.add("stage3d-on");
  if(stageWait)stageWait.classList.remove("on");
  if(opening){
    opening.classList.add("out");
    setTimeout(function(){if(opening.parentNode)opening.parentNode.removeChild(opening);},900);
  }
  jumpTick(0);
}

window.addEventListener("message",function(e){
  if(!openFrame||e.source!==openFrame.contentWindow||!e.data)return;
  if(e.origin!==location.origin&&!(location.protocol==="file:"&&e.origin==="null"))return;
  if(e.data.type==="jump-target"){
    location.replace(TARGET);return;
  }
  if(e.data.type==="jump-stage"){
    requestStageStart();
  }
});

function sstep(t,a,b){return Math.max(0,Math.min(1,(t-a)/(b-a)));}
function sease(p){return 1-Math.pow(1-p,3);}

function jumpCam(){
  var p=reduce?1:sease(sstep(jt.t,0,2.2));
  _jp.lerpVectors(P0,P1,p);_jl.lerpVectors(L0,L1,p);
  var dx=_jp.x-_jl.x,dy=_jp.y-_jl.y,dz=_jp.z-_jl.z;
  var radius=Math.sqrt(dx*dx+dy*dy+dz*dz)*jt.zoom;
  var theta=Math.atan2(dx,dz)+jt.dragTheta;
  var phi=T.MathUtils.clamp(Math.acos(T.MathUtils.clamp(dy/Math.sqrt(dx*dx+dy*dy+dz*dz),-1,1))+jt.dragPhi,1.02,1.98);
  var sinPhi=Math.sin(phi);
  camera.position.set(_jl.x+radius*sinPhi*Math.sin(theta),
    _jl.y+radius*Math.cos(phi),_jl.z+radius*sinPhi*Math.cos(theta));
  camera.lookAt(_jl);
}
function jumpHero(){
  var legs=hero.userData.legs;
  if(reduce){                            /* 减弱动态：直接落在终态，不动 */
    hero.position.x=H1.x;hero.position.z=H1.z;hero.rotation.y=H1.ry;
    hero.rotation.x=0;armMixer.setTime(6.7);
    legs[0].rotation.x=0;legs[1].rotation.x=0;
    if(heroAO){heroAO.position.x=H1.x;heroAO.position.z=H1.z;}
    return;
  }
  var w=sstep(jt.t,1.8,4.0),we=sease(w);
  hero.position.x=H0.x+(H1.x-H0.x)*we;
  var zPath=sease(sstep(we,.58,.92));  /* 先沿队伍前方通过，再平滑转入门洞轴线 */
  hero.position.z=H0.z+(H1.z-H0.z)*zPath;
  hero.rotation.y=H0.ry+(H1.ry-H0.ry)*we;
  var walking=(w>0&&w<1);
  hero.position.y=HY+(walking?(1-Math.cos(jt.t*7.6))*.018:0);
  hero.rotation.z=walking?Math.sin(jt.t*3.8)*.018:0;
  if(heroAO){heroAO.position.x=hero.position.x;heroAO.position.z=hero.position.z;}

  var sw=walking?Math.sin(jt.t*7.6):0;
  legs[0].rotation.x=sw*.34;legs[1].rotation.x=-sw*.34;
  hero.rotation.x=0;
  armMixer.setTime(Math.min(7,jt.t));
  if(jt.t>5.75){var sb=document.getElementById("sub");if(sb)sb.classList.add("on");}
}

function jumpFire(){
  if(jt.fired)return;jt.fired=true;
  location.replace(TARGET);
  setTimeout(function(){location.href=TARGET;},900);   /* replace 被拦时的二道保险 */
}

/* 看门狗：11 秒内没出第一帧（着色器编译失败 / 显存不够 / 崩了）就回退 2D 版 */
var FIRST=false;
setTimeout(function(){ if(!FIRST)location.replace("index.html"); },
           reduce?7000:11000);

function jumpUI(){
  var progress=Math.max(0,Math.min(1,jt.t/DUR));
  var r=document.getElementById("ring");
  if(r)r.setAttribute("stroke-dashoffset",String(144.5*(1-progress)));
  var fill=document.getElementById("jump-fill");if(fill)fill.style.width=(progress*100)+"%";
  var seconds=document.getElementById("jump-seconds");
  if(seconds)seconds.textContent=Math.max(0,DUR-jt.t).toFixed(1)+"s";
  if(jt.t>=DUR&&!FREEZE)jumpFire();
}

/* 交互：轻点立即前往，长按暂停 */
var FREEZE=(function(){var m=/[?&]frame=([-0-9.]+)/.exec(Q);return m?parseFloat(m[1]):null;})();
if(JUMP){
  canvas.style.cursor="grab";
  document.getElementById("go").addEventListener("click",function(e){
    e.stopPropagation();jumpFire();});
  var jpd=0,jhold=false,jmoved=0,jx=0,jy=0;
  canvas.addEventListener("pointerdown",function(e){
    if(e.button!==undefined&&e.button!==0)return;
    jpd=performance.now();jhold=false;jmoved=0;jx=e.clientX;jy=e.clientY;
    try{canvas.setPointerCapture(e.pointerId);}catch(_){}});
  canvas.addEventListener("pointermove",function(e){
    if(!jpd)return;
    jmoved=Math.max(jmoved,Math.abs(e.clientX-jx)+Math.abs(e.clientY-jy));
    if(performance.now()-jpd>400&&jmoved<14){
      jhold=true;jt.paused=true;
      var h=document.getElementById("hold");if(h)h.classList.add("on");
    }});
  var jup=function(){
    if(!jpd)return;
    var held=performance.now()-jpd,wasHold=jhold;jpd=0;
    if(wasHold){jt.paused=false;
      var h=document.getElementById("hold");if(h)h.classList.remove("on");}
    else if(held<400&&jmoved<14)jumpFire();      /* 轻点 = 立即前往 */
  };
  ["pointerup","pointercancel"].forEach(function(ev){
    canvas.addEventListener(ev,jup);});
  document.addEventListener("visibilitychange",function(){
    if(document.hidden)jt.paused=true; else if(!jpd)jt.paused=false;});
}

/* 他本机 macOS 开着「减弱动态效果」，不加这行提示的话打开只会看到一张静止图 */
if(reduce){
  var _tp=document.getElementById("tip");
  if(_tp)_tp.textContent="系统开着「减弱动态效果」，这里直接跳到终帧 · 加 ?motion=full 看完整动画";
}

function jumpTick(dt){
  if(!jt.started)return;
  if(FREEZE!==null){jt.t=FREEZE;jumpCam();jumpUI();return;}
  if(!jt.paused)jt.t+=dt;
  jumpCam();jumpUI();
}
"""

sub("    if(pinch)orb.tR=T.MathUtils.clamp(orb.tR*(pinch/d),orb.minR,orb.maxR);",
    "    if(JUMP)jt.zoom=T.MathUtils.clamp(jt.zoom*(pinch/d),.72,1.3);\n"
    "    else orb.tR=T.MathUtils.clamp(orb.tR*(pinch/d),orb.minR,orb.maxR);",
    "跳转页双指缩放")
sub("  orb.tTheta-=dx*.0052;\n"
    "  orb.tPhi=T.MathUtils.clamp(orb.tPhi-dy*.0042,orb.minPhi,orb.maxPhi);\n"
    "  orb.vTheta=-dx*.0052;",
    "  if(JUMP){\n"
    "    jt.dragTheta-=dx*.0052;\n"
    "    jt.dragPhi=T.MathUtils.clamp(jt.dragPhi-dy*.0042,-.48,.48);\n"
    "  }else{\n"
    "    orb.tTheta-=dx*.0052;\n"
    "    orb.tPhi=T.MathUtils.clamp(orb.tPhi-dy*.0042,orb.minPhi,orb.maxPhi);\n"
    "    orb.vTheta=-dx*.0052;\n"
    "  }", "跳转页拖拽相机")
sub("  orb.tR=T.MathUtils.clamp(orb.tR*(1+Math.sign(e.deltaY)*.09),orb.minR,orb.maxR);hideTip();",
    "  if(JUMP)jt.zoom=T.MathUtils.clamp(jt.zoom*(1+Math.sign(e.deltaY)*.09),.72,1.3);\n"
    "  else orb.tR=T.MathUtils.clamp(orb.tR*(1+Math.sign(e.deltaY)*.09),orb.minR,orb.maxR);\n"
    "  hideTip();", "跳转页滚轮缩放")
sub('["pointerup","pointercancel","pointerleave"].forEach(function(ev){canvas.addEventListener(ev,endPtr);});',
    '["pointerup","pointercancel"].forEach(function(ev){canvas.addEventListener(ev,endPtr);});\n'
    'canvas.addEventListener("pointerleave",function(e){if(!JUMP)endPtr(e);});',
    "跳转页持续拖拽")

sub("applyCam();updateCrowd(0,0);renderer.render(scene,camera);",
    JUMP_JS + "\nif(JUMP){hero.visible=false;if(heroAO)heroAO.visible=false;}\n"
    "applyCam();if(JUMP)jumpTick(0);updateCrowd(0,0);renderer.render(scene,camera);",
    "注入跳转模块")

# 首帧标记：必须放在 frame() 体内最后一行。
# 放到 frame() 外面的话，渲染循环第一帧就抛错它照样是 true，看门狗形同虚设。
sub("  requestAnimationFrame(frame);",
    "  FIRST=true;\n  requestAnimationFrame(frame);", "首帧标记")

opening_s = open(OPEN_SRC, encoding="utf-8").read()
opening_edits = []


def open_sub(old, new, label):
    global opening_s
    if opening_s.count(old) != 1:
        print("✗ 开场页锚点异常（%d 处）：「%s」" % (opening_s.count(old), label))
        sys.exit(1)
    opening_s = opening_s.replace(old, new)
    opening_edits.append(label)


open_sub('<meta name="description" content="奶娃正在护送你前往南京传媒学院。">',
         '<meta name="description" content="奶娃正在护送你前往南京传媒学院。">\n'
         '<meta name="robots" content="noindex">', "开场页不索引")
open_sub("</style>", '''
  /* 嵌入跳转页时只保留 2D 内容；卡片中央完全透明，3D 校园从人物周围透出。 */
  html.embedded,html.embedded body{width:100%;height:100%;min-height:0;overflow:hidden}
  html.embedded body{display:flex;align-items:center;justify-content:center;padding:12px;
    background:transparent!important}
  html.embedded body::before,html.embedded body::after{display:none}
  html.embedded #scene{width:100%;height:100%;margin:0;justify-content:center}
  html.embedded .sheet{width:min(760px,94vw);max-height:calc(100dvh - 26px);
    padding:clamp(24px,3.2vh,48px) clamp(24px,4vw,62px) clamp(20px,2.6vh,36px);
    overflow:hidden;background:transparent;border:0;border-radius:0;backdrop-filter:none;
    -webkit-backdrop-filter:none;box-shadow:none}
  html.embedded .sheet::before{display:none}
  html.embedded .stage{height:clamp(170px,24vh,286px);margin-top:clamp(6px,1vh,12px)}
  html.embedded .walker,html.embedded .shadow{display:none!important}
  html.embedded .ticker,html.embedded .status,html.embedded .quote,html.embedded .meter,
  html.embedded .actions,html.embedded .foot,html.embedded .stamp,html.embedded .impact,
  html.embedded .confetti{display:none!important}
  html.embedded .crest{width:clamp(80px,11vh,112px);height:clamp(80px,11vh,112px)}
  html.embedded .crest img{width:100%;height:100%}
  html.embedded h1{font-size:clamp(25px,4vh,34px);margin-top:12px;
    text-shadow:0 1px 3px rgba(255,253,246,.95),0 0 18px rgba(255,253,246,.88)}
  html.embedded .dept{margin-top:5px;text-shadow:0 1px 8px rgba(255,253,246,.95)}
  html.embedded .rule{margin-top:11px}
  html.embedded .status{width:fit-content;max-width:100%;margin:0 auto;font-size:clamp(13px,1.8vh,16px);
    padding:7px 16px;border:1px solid rgba(255,255,255,.54);border-radius:10px;
    background:rgba(255,253,246,.76);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
    box-shadow:0 4px 18px rgba(10,28,48,.12)}
  html.embedded .quote{text-shadow:0 1px 8px rgba(255,253,246,.95)}
  html.embedded .meter{margin:clamp(10px,1.8vh,18px) auto 0;padding:10px 16px 8px;
    border:1px solid rgba(255,255,255,.58);border-radius:10px;background:rgba(255,253,246,.82);
    backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);box-shadow:0 4px 18px rgba(10,28,48,.1)}
  html.embedded .actions{margin-top:clamp(10px,1.8vh,18px)}
  html.embedded .foot{display:none}
  html.embedded .confetti{z-index:12}
  @media(max-height:720px){
    html.embedded body{padding:8px}
    html.embedded .sheet{padding:18px 22px 16px}
    html.embedded .crest{width:68px;height:68px}
    html.embedded .crest svg{inset:-9px}
    html.embedded h1{font-size:24px;margin-top:8px}
    html.embedded .stage{height:112px;margin-top:4px}
    html.embedded .walker,html.embedded .shadow{display:none!important}
    html.embedded .status{font-size:13px;line-height:1.45}
    html.embedded .quote{display:none}
    html.embedded .meter{margin-top:8px}
    html.embedded .actions{margin-top:8px}
  }
</style>''', "开场动画叠加到 3D 底景")
open_sub('  const TARGET = "https://www.cucn.edu.cn/";',
         '  const TARGET = "https://www.cucn.edu.cn/";\n'
         '  const OPENING_PARAMS = new URLSearchParams(location.search);\n'
         '  const EMBEDDED = OPENING_PARAMS.get("embedded") === "1";\n'
         '  const CAMPUS_SEQUENCE = OPENING_PARAMS.get("campus") === "1";\n'
         '  const FALLBACK = OPENING_PARAMS.get("fallback") === "1";\n'
         '  if (EMBEDDED) document.documentElement.classList.add("embedded");\n'
         '  let stageSent = false;\n'
         '  function sendStage(type){\n'
         '    if(stageSent && type === "jump-stage") return;\n'
         '    if(type === "jump-stage") stageSent = true;\n'
         '    if(window.parent !== window) window.parent.postMessage({type}, location.protocol === "file:" ? "*" : location.origin);\n'
         '  }', "开场交接消息")
open_sub('''    paper:[0, .80], cam:[0, 1.35], ring:[.42, 1.30], badge:[.86, 1.42],
    title:1.06, titleGap:.052, titleDur:.62, dept:1.52, rule:1.58, sheen:1.72,
    ui:1.90,
    /* 角色三段表演：走入 → 招手 → 待命 */
    walk:[2.02, 2.74], cut1:2.80, wave:[2.86, 3.52], cut2:3.58,
    idle:3.64, stamp:3.86, settle:4.36, countEnd:5.44, bow:5.44, end:5.86''',
         '''    paper:[0, 1.45], cam:[0, 3.10], ring:[.72, 2.55], badge:[1.36, 2.88],
    title:1.85, titleGap:.073, titleDur:.72, dept:2.98, rule:3.14, sheen:3.34,
    ui:3.55,
    /* 角色三段表演：走入 → 招手 → 待命 */
    walk:[6.55, 7.12], cut1:7.18, wave:[7.24, 7.90], cut2:7.96,
    idle:8.02, stamp:8.28, settle:8.78, countEnd:9.88, bow:9.88, end:10.28''', "延长 2D 开场节奏")
open_sub("  render(0);\n  requestAnimationFrame(tick);",
         '''  render(0);
  if (EMBEDDED) sendStage("opening-ready");
  if (CAMPUS_SEQUENCE) {
    let started = false;
    const start = () => {
      if (started) return;
      started = true;
      last = 0;
      raf = requestAnimationFrame(tick);
    };
    window.addEventListener("message", e=>{
      if (e.source === window.parent && e.data && e.data.type === "opening-start") start();
    });
  } else requestAnimationFrame(tick);''',
         "开场层就绪消息")
open_sub('''    setTimeout(()=>{
      location.replace(TARGET);
      setTimeout(()=>{ location.href = TARGET; }, 900);
    }, reduce ? 0 : 340);''',
         '''    if (EMBEDDED) { sendStage(FALLBACK ? "jump-target" : "jump-stage"); return; }
    setTimeout(()=>{
      location.replace(TARGET);
      setTimeout(()=>{ location.href = TARGET; }, 900);
    }, reduce ? 0 : 340);''', "开场嵌入模式")
open_sub('''    const t = el/1000;
    render(t);''',
         '''    const t = el/1000;
    render(t);
    if (EMBEDDED && !FALLBACK && t >= K.walk[0]) { sendStage("jump-stage"); return; }''',
         "2D 开场转入 3D")
open_sub('''  q("go").addEventListener("click", ()=>{ cancelAnimationFrame(raf); });''',
         '''  q("go").addEventListener("click", e=>{
    cancelAnimationFrame(raf);
    if (EMBEDDED) { e.preventDefault(); sendStage("jump-target"); }
  });''', "开场立即前往")

open(DST, "w", encoding="utf-8").write(s)
open(OPEN_DST, "w", encoding="utf-8").write(opening_s)
print("✓ 生成 %s（%d 处注入）" % (os.path.relpath(DST, ROOT), len(edits)))
for i, e in enumerate(edits, 1):
    print("   %2d. %s" % (i, e))
print("✓ 生成 %s（%d 处注入）" % (os.path.relpath(OPEN_DST, ROOT), len(opening_edits)))
