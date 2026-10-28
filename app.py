import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="水的三態與飽和蒸氣壓互動模擬", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
        .rule-box { background-color: #f8fafc; border-left: 5px solid #2563eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .step-box { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("化學教學互動模擬：水的飽和蒸氣壓與動態平衡")

tab1, tab2, tab3 = st.tabs([
    "📊 專案一：蒸發與凝結動態平衡", 
    "🔥 專案二：P-T / P-V 關係圖", 
    "🧮 專案三：相態判斷與液態水量計算"
])

# ==========================================
# Tab 1: 專案一
# ==========================================
with tab1:
    st.markdown("觀察定溫下密閉容器中，隨時間推進**蒸發與凝結速率**、**蒸氣壓**的變化，以及微觀粒子達動態平衡的實體動畫。")
    html_tab1 = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 4px; background: #ffffff; color: #1f2937; }
        .control-panel { background: #f8fafc; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 10px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
        .btn { background: #2563eb; color: white; border: none; padding: 6px 14px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 13px; }
        .btn-reset { background: #64748b; }
        .speed-select { padding: 5px 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; font-weight: 600; color: #334155; background: #fff; cursor: pointer; }
        .slider-wrap { flex-grow: 1; display: flex; align-items: center; gap: 10px; min-width: 240px; }
        input[type=range] { flex-grow: 1; height: 6px; cursor: pointer; accent-color: #2563eb; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }
        .metric-card { background: #ffffff; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .metric-title { font-size: 11.5px; color: #64748b; margin-bottom: 2px; font-weight: 600; }
        .metric-value { font-size: 17px; font-weight: 700; }
        .status-banner { grid-column: span 4; padding: 10px 14px; border-radius: 8px; font-size: 13px; line-height: 1.4; background: #eff6ff; border-left: 5px solid #2563eb; }
        .canvas-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; }
        .canvas-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; display: flex; flex-direction: column; align-items: center; width: 100%; }
        canvas { width: 100%; max-width: 440px; height: 330px; display: block; }
        .legend-bar { display: flex; gap: 12px; font-size: 11.5px; color: #475569; margin-top: 4px; justify-content: center; flex-wrap: wrap; }
        .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
        .chart-toggles { display: flex; gap: 8px; margin-bottom: 6px; width: 100%; justify-content: center; }
        .c-btn { padding: 4px 14px; font-size: 12px; font-weight: 700; border: 2px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #475569; cursor: pointer; transition: 0.2s; }
        .c-btn.active { background: #eff6ff; border-color: #2563eb; color: #1d4ed8; }
    </style>
    </head>
    <body>
    <div class="control-panel">
        <button id="playBtn1" class="btn">⏸ 暫停時間</button>
        <button id="resetBtn1" class="btn btn-reset">🔄 重置 (t=0)</button>
        <div style="display:flex; align-items:center; gap:4px;">
            <span style="font-size:12.5px; font-weight:600; color:#475569;">時間流速：</span>
            <select id="speedSel1" class="speed-select"><option value="0.0025">0.5x</option><option value="0.005" selected>1.0x</option><option value="0.012">2.0x</option></select>
        </div>
        <div class="slider-wrap">
            <span style="font-weight:600; font-size:13px;">時間軸 (t)：</span>
            <input type="range" id="timeSlider1" min="0" max="10" step="0.02" value="0">
            <span id="timeLabel1" style="font-weight:700; min-width:45px; color:#2563eb;">0.0 s</span>
        </div>
    </div>
    <div class="metrics-grid">
        <div class="metric-card"><div class="metric-title">蒸發速率 (r_蒸發)</div><div class="metric-value" style="color:#16a34a;">10.0</div></div>
        <div class="metric-card"><div class="metric-title">凝結速率 (r_凝結)</div><div class="metric-value" id="rCondVal1" style="color:#ea580c;">0.0</div></div>
        <div class="metric-card"><div class="metric-title">氣相水蒸氣粒子數</div><div class="metric-value" id="pCountVal1" style="color:#d97706;">0 / 45</div></div>
        <div class="metric-card"><div class="metric-title">蒸氣壓狀態</div><div class="metric-value" id="pressureVal1" style="color:#2563eb;">0% 飽和</div></div>
        <div class="status-banner" id="statusBanner1"></div>
    </div>
    <div class="canvas-grid">
        <div class="canvas-box">
            <div class="chart-toggles"><button id="btnRT" class="c-btn active">📈 r-t 圖</button><button id="btnPT" class="c-btn">☁️ P-t 圖</button></div>
            <canvas id="gCanvas1" width="880" height="660"></canvas>
        </div>
        <div class="canvas-box">
            <div style="font-size:13.5px; font-weight:700; margin-bottom:10px;">密閉容器微觀動態 (一進一出動態平衡)</div>
            <canvas id="bCanvas1" width="880" height="660"></canvas>
            <div class="legend-bar">
                <span><span class="dot" style="background:#f59e0b;"></span>水蒸氣</span>
                <span><span class="dot" style="background:#22c55e;"></span>蒸發 (↑)</span>
                <span><span class="dot" style="background:#ea580c;"></span>凝結 (↓)</span>
            </div>
        </div>
    </div>
    <script>
    const gCtx1 = document.getElementById('gCanvas1').getContext('2d');
    const bCtx1 = document.getElementById('bCanvas1').getContext('2d');
    gCtx1.scale(2, 2); bCtx1.scale(2, 2);
    let t1 = 0, isPlay1 = true, dt1 = 0.005, currentView = 'rt';
    const r_evap1 = 10, t_eq1 = 7, k1 = 0.45, norm1 = 1 - Math.exp(-k1 * t_eq1), maxP1 = 45;
    const BL1 = 55, BR1 = 385, BT1 = 52, BB1 = 300, EVAP_INTERVAL = 24;
    let evapTimer = 0, condAccumulator = 0, liqP1 = [], gasP1 = [], condAnimP1 = [], eff1 = [];
    
    function getRC1(time) { return time<=0 ? 0 : (time>=t_eq1 ? r_evap1 : r_evap1 * (1 - Math.exp(-k1 * time)) / norm1); }
    for(let i=0; i<65; i++) liqP1.push({x: BL1+15+Math.random()*(BR1-BL1-30), y: 210+Math.random()*(BB1-220), vx:(Math.random()-0.5)*0.6, vy:(Math.random()-0.5)*0.6});
    
    function spawnGP1(fromSurf=true, waterY=200, customX=null) {
        const x = customX !== null ? customX : (BL1 + 28 + Math.random()*(BR1 - BL1 - 56));
        const y = fromSurf ? waterY - 3 : BT1 + 20 + Math.random()*(waterY - BT1 - 35);
        const angle = -Math.PI/3 - Math.random()*(Math.PI/3);
        const speed = 1.9 + Math.random()*0.9;
        gasP1.push({x, y, vx: fromSurf ? Math.cos(angle)*speed : (Math.random()-0.5)*2.4, vy: fromSurf ? Math.sin(angle)*speed : (Math.random()-0.5)*2.4, hGreen: fromSurf ? 42 : 0});
    }

    document.getElementById('btnRT').onclick = () => { currentView = 'rt'; document.getElementById('btnRT').className = 'c-btn active'; document.getElementById('btnPT').className = 'c-btn'; };
    document.getElementById('btnPT').onclick = () => { currentView = 'pt'; document.getElementById('btnPT').className = 'c-btn active'; document.getElementById('btnRT').className = 'c-btn'; };
    document.getElementById('speedSel1').onchange = e => dt1 = parseFloat(e.target.value);
    document.getElementById('timeSlider1').oninput = e => { t1 = parseFloat(e.target.value); isPlay1 = false; };
    document.getElementById('playBtn1').onclick = () => { if(t1>=10){t1=0; gasP1=[]; condAnimP1=[]; eff1=[];} isPlay1 = !isPlay1; };
    document.getElementById('resetBtn1').onclick = () => { t1=0; isPlay1=false; gasP1=[]; condAnimP1=[]; eff1=[]; };

    function animate1() {
        if(isPlay1 && t1 < 10) { t1 += dt1; if(t1 >= 10) t1 = 10; document.getElementById('timeSlider1').value = t1; }
        const rc = getRC1(t1), ratio = rc / r_evap1, isEq = t1 >= t_eq1;
        document.getElementById('timeLabel1').textContent = t1.toFixed(1) + " s";
        document.getElementById('rCondVal1').innerHTML = isEq ? `10.0 <span style="font-size:12px;color:#16a34a;">(= r_蒸發)</span>` : rc.toFixed(1);
        const targetC = Math.round(maxP1 * ratio);
        document.getElementById('pCountVal1').textContent = `${targetC} / ${maxP1}`;
        document.getElementById('pressureVal1').textContent = `${Math.round(ratio*100)}% 飽和`;

        if(t1 === 0) document.getElementById('statusBanner1').innerHTML = "<b>狀態 ①：初始瞬間 (t = 0)</b> — r_蒸發 = 10.0，r_凝結 = 0。";
        else if(t1 < t_eq1) document.getElementById('statusBanner1').innerHTML = "<b>狀態 ②：未飽和階段 (0 &lt; t &lt; 7s)</b> — 蒸發速率仍大於凝結速率。";
        else document.getElementById('statusBanner1').innerHTML = "<b>狀態 ③：達動態平衡 (t ≥ 7s)</b> — 每蒸發 1 顆，同時凝結 1 顆，氣相總數不變。";

        gCtx1.clearRect(0, 0, 440, 330);
        const ox=45, oy=280, w=375, h=230, eqX = ox + (t_eq1/10)*w, evapY = oy - h, curX = ox + (t1/10)*w;
        gCtx1.strokeStyle="#334155"; gCtx1.lineWidth=2; gCtx1.beginPath(); gCtx1.moveTo(ox, oy-h-10); gCtx1.lineTo(ox, oy); gCtx1.lineTo(ox+w+10, oy); gCtx1.stroke();
        
        if (currentView === 'rt') {
            gCtx1.fillStyle="#334155"; gCtx1.fillText("速率 (r)", 8, 25); gCtx1.fillText("時間 (t)", ox+w-20, oy+22);
            if (t1 >= t_eq1) { gCtx1.fillStyle="rgba(22,163,74,0.08)"; gCtx1.fillRect(eqX, oy-h, (ox+w)-eqX, h); }
            gCtx1.strokeStyle="#16a34a"; gCtx1.lineWidth=3.5; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke();
            gCtx1.strokeStyle="#ea580c"; gCtx1.beginPath();
            const steps = Math.max(2, Math.floor(Math.min(t1,t_eq1)*12));
            for(let i=0; i<=steps; i++) { let ti=(i/steps)*Math.min(t1,t_eq1); let py=oy-(getRC1(ti)/12)*h; if(i===0)gCtx1.moveTo(ox+(ti/10)*w,py); else gCtx1.lineTo(ox+(ti/10)*w,py); }
            gCtx1.stroke();
            if (t1 > t_eq1) { gCtx1.save(); gCtx1.setLineDash([6,6]); gCtx1.beginPath(); gCtx1.moveTo(eqX, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke(); gCtx1.restore(); }
            gCtx1.fillStyle="#ea580c"; gCtx1.beginPath(); gCtx1.arc(curX, oy - (rc/12)*h, 5, 0, Math.PI*2); gCtx1.fill();
        } else {
            gCtx1.fillStyle="#334155"; gCtx1.fillText("蒸氣壓 (P)", 8, 25); gCtx1.fillText("時間 (t)", ox+w-20, oy+22);
            if (t1 >= t_eq1) { gCtx1.fillStyle="rgba(37,99,235,0.05)"; gCtx1.fillRect(eqX, oy-h, (ox+w)-eqX, h); }
            gCtx1.strokeStyle="#2563eb"; gCtx1.lineWidth=3.5; gCtx1.beginPath();
            const steps = Math.max(2, Math.floor(Math.min(t1,t_eq1)*12));
            for(let i=0; i<=steps; i++) { let ti=(i/steps)*Math.min(t1,t_eq1); let py=oy-(getRC1(ti)/12)*h; if(i===0)gCtx1.moveTo(ox+(ti/10)*w,py); else gCtx1.lineTo(ox+(ti/10)*w,py); }
            gCtx1.stroke();
            if (t1 > t_eq1) { gCtx1.beginPath(); gCtx1.moveTo(eqX, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke(); }
            gCtx1.fillStyle="#2563eb"; gCtx1.beginPath(); gCtx1.arc(curX, oy - (rc/12)*h, 5.5, 0, Math.PI*2); gCtx1.fill();
        }

        bCtx1.clearRect(0, 0, 440, 330);
        const waterY = 200 + ratio * 12;
        if ((isPlay1 || t1 >= t_eq1) && t1 > 0) {
            evapTimer++;
            if (evapTimer >= EVAP_INTERVAL) {
                evapTimer = 0; spawnGP1(true, waterY, BL1 + 30 + Math.random()*270);
                condAccumulator += ratio;
                if (condAccumulator >= 0.99) {
                    condAccumulator -= 1.0;
                    if(gasP1.length>0) gasP1.splice(0,1);
                    condAnimP1.push({x: BL1+30+Math.random()*270, y: waterY-20, targetY: waterY+12, vy: 2.8, age:0});
                }
            }
        }
        while(gasP1.length < targetC) spawnGP1(false, waterY);
        while(gasP1.length > targetC) gasP1.pop();

        bCtx1.fillStyle = "rgba(56, 189, 248, 0.35)"; bCtx1.fillRect(BL1, waterY, BR1 - BL1, BB1 - waterY);
        for(let lp of liqP1) { lp.x += lp.vx; lp.y += lp.vy; if(lp.x < BL1+6 || lp.x > BR1-6) lp.vx *= -1; if(lp.y < waterY+6) lp.y = waterY+6; if(lp.y > BB1-6) lp.y = BB1-6; bCtx1.beginPath(); bCtx1.arc(lp.x, lp.y, 3.5, 0, Math.PI*2); bCtx1.fill(); }
        for(let p of gasP1) { p.x += p.vx; p.y += p.vy; if(p.x < BL1+6 || p.x > BR1-6) { p.x = Math.max(BL1+6, Math.min(BR1-6, p.x)); p.vx *= -1; } if(p.y < BT1+6) { p.y = BT1+6; p.vy *= -1; } if(p.y > waterY - 6) { p.y = waterY - 6; p.vy *= -1; } bCtx1.beginPath(); bCtx1.arc(p.x, p.y, 5.5, 0, Math.PI*2); bCtx1.fillStyle="#f59e0b"; bCtx1.fill(); }
        for(let i = condAnimP1.length - 1; i >= 0; i--) { let cp = condAnimP1[i]; cp.y += cp.vy; bCtx1.beginPath(); bCtx1.arc(cp.x, cp.y, 5.5, 0, Math.PI*2); bCtx1.fillStyle = "#ea580c"; bCtx1.fill(); if(cp.y >= cp.targetY) condAnimP1.splice(i, 1); }
        bCtx1.strokeStyle = "#475569"; bCtx1.lineWidth = 3.5; bCtx1.strokeRect(BL1, BT1, BR1 - BL1, BB1 - BT1);
        requestAnimationFrame(animate1);
    }
    animate1();
    </script>
    </body>
    </html>
    """
    components.html(html_tab1, height=740, scrolling=True)

# ==========================================
# Tab 2: 專案二
# ==========================================
with tab2:
    st.markdown("觀察液-氣共存與完全汽化轉折點。")
    html_tab2 = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body { font-family: sans-serif; margin: 0; padding: 4px; }
        .control-bar { background: #f8fafc; padding: 10px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 10px; display: flex; gap: 10px; }
        input[type=range] { flex-grow: 1; }
        .canvas-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        canvas { width: 100%; max-width: 440px; height: 350px; border: 1px solid #e2e8f0; border-radius: 10px; }
    </style>
    </head>
    <body>
    <div class="control-bar">
        <span style="font-weight:700;">調整溫度 (T)：</span>
        <input type="range" id="mainSlider2" min="0" max="140" step="0.5" value="30">
        <span id="sliderValLabel2" style="font-weight:700; color:#2563eb;">30.0 °C</span>
    </div>
    <div class="canvas-grid">
        <canvas id="gCanvas2" width="880" height="700"></canvas>
        <canvas id="sCanvas2" width="880" height="700"></canvas>
    </div>
    <script>
    const gCtx2 = document.getElementById('gCanvas2').getContext('2d');
    const sCtx2 = document.getElementById('sCanvas2').getContext('2d');
    gCtx2.scale(2, 2); sCtx2.scale(2, 2);
    const T_CRIT2 = 80.0, P_CRIT2 = 450.0;
    
    function animate2() {
        const val = parseFloat(document.getElementById('mainSlider2').value);
        document.getElementById('sliderValLabel2').textContent = val.toFixed(1) + " °C";
        
        gCtx2.clearRect(0,0,440,350); sCtx2.clearRect(0,0,440,350);
        
        // P-T 曲線繪製邏輯
        const zX = 42, mX = 415, oy = 290, h = 240, maxP = 600;
        const tX = tc => zX + ((tc + 273) / (140 + 273)) * (mX - zX);
        const pY = p => oy - (p / maxP) * h;
        const ox = tX(0), cX = tX(T_CRIT2), cY = pY(P_CRIT2);
        
        gCtx2.strokeStyle="#334155"; gCtx2.lineWidth=2; gCtx2.beginPath(); gCtx2.moveTo(zX - 12, oy); gCtx2.lineTo(mX + 12, oy); gCtx2.moveTo(ox, oy - h - 15); gCtx2.lineTo(ox, oy); gCtx2.stroke();
        gCtx2.strokeStyle="#16a34a"; gCtx2.lineWidth=3.5; gCtx2.beginPath(); gCtx2.moveTo(ox, pY(70)); gCtx2.lineTo(cX, cY); gCtx2.stroke();
        gCtx2.strokeStyle="#0284c7"; gCtx2.beginPath(); gCtx2.moveTo(cX, cY); gCtx2.lineTo(tX(140), pY(P_CRIT2 * (140+273)/(T_CRIT2+273))); gCtx2.stroke();

        let curP = val <= T_CRIT2 ? 70 * Math.exp(Math.log(P_CRIT2/70) * (val/T_CRIT2)) : P_CRIT2 * ((val + 273)/(T_CRIT2 + 273));
        gCtx2.fillStyle="#dc2626"; gCtx2.beginPath(); gCtx2.arc(tX(val), pY(curP), 6, 0, Math.PI*2); gCtx2.fill();
        
        sCtx2.strokeStyle="#475569"; sCtx2.lineWidth=3.5; sCtx2.strokeRect(85, 45, 230, 245);
        requestAnimationFrame(animate2);
    }
    animate2();
    </script>
    </body>
    </html>
    """
    components.html(html_tab2, height=450, scrolling=True)

# ==========================================
# Tab 3: 專案三
# ==========================================
with tab3:
    st.markdown("### 🧮 專案三：相態判斷與液態水量計算")
    
    st.info("💡 **解題核心原則**[cite: 5]：\n"
            "1. 先將所有液體假設為氣化，由 $PV=nRT$ 求理論壓力 $P$。\n"
            "2. 判斷相態：\n"
            "   * 若 $P > P_v^0$：表示氣液共存，氣體凝結為液體使 $P=P_v^0$。\n"
            "   * 若 $P = P_v^0$：表示氣體恰好蒸乾無液體 $P=P_v^0$。\n"
            "   * 若 $P < P_v^0$：表示僅有氣體 $P=P$。")

    st.markdown("#### ⚙️ 設定參數")
    
    # 預設快速按鈕 (對應先前提到的 4 個情境)
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    if col_btn1.button("情境 1：0.36g 於 24.6L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 0.36, 24.6
    if col_btn2.button("情境 2：1.80g 於 24.6L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 1.80, 24.6
    if col_btn3.button("情境 3：體積壓縮至 4.92L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 0.36, 4.92
    if col_btn4.button("情境 4：體積擴張至 98.4L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 1.80, 98.4

    # 初始化 Session State
    if "w_input" not in st.session_state: st.session_state.w_input = 1.80
    if "v_input" not in st.session_state: st.session_state.v_input = 8.20

    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    W = col_in1.number_input("注入水量 $W$ (g)", value=st.session_state.w_input, step=0.1)
    V = col_in2.number_input("容器體積 $V$ (L)", value=st.session_state.v_input, step=1.0)
    T_c = col_in3.number_input("溫度 $T$ (°C)", value=27.0, step=1.0)
    Pv0 = col_in4.number_input("飽和蒸氣壓 $P_v^0$ (atm)", value=0.050, step=0.01, format="%.3f")

    # 運算邏輯
    R = 0.082
    T_k = T_c + 273
    n_total = W / 18.0
    P_theo = (n_total * R * T_k) / V

    st.markdown("#### 📝 步驟一：假設完全汽化，計算理論壓力 $P$")
    with st.container():
        st.markdown('<div class="step-box">', unsafe_allow_html=True)
        st.latex(rf"n_{{總}} = \frac{{{W}}}{{18.0}} = {n_total:.3f} \text{{ mol}}")
        st.latex(rf"P = \frac{{nRT}}{{V}} = \frac{{{n_total:.3f} \times 0.082 \times {T_k}}}{{{V}}} = {P_theo:.4f} \text{{ atm}}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### ⚖️ 步驟二：與飽和蒸氣壓 $P_v^0$ 比較並判斷相態")
    
    epsilon = 1e-5
    if P_theo - Pv0 > epsilon:
        # P > Pv0
        st.error(f"**判斷結果： 理論壓力 $P ({P_theo:.4f}\text{{ atm}}) > P_v^0 ({Pv0:.3f}\text{{ atm}})$**")
        st.markdown('<div class="rule-box">表示<b>氣液共存</b>，部分氣體將凝結為液態水，最終容器內的實際壓力維持在飽和狀態 $P = P_v^0$[cite: 5]。</div>', unsafe_allow_html=True)
        
        st.markdown("#### 💧 步驟三：計算殘留液態水量")
        with st.container():
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            n_gas = (Pv0 * V) / (R * T_k)
            n_liq = n_total - n_gas
            W_liq = n_liq * 18.0
            
            st.markdown("1. 利用飽和蒸氣壓反推平衡時的「氣態水莫耳數」：")
            st.latex(rf"n_{{氣}} = \frac{{P_v^0 V}}{{RT}} = \frac{{{Pv0:.3f} \times {V}}}{{0.082 \times {T_k}}} = {n_gas:.4f} \text{{ mol}}")
            st.markdown("2. 總莫耳數減去氣態莫耳數，得出「液態水殘留量」：")
            st.latex(rf"n_{{液}} = {n_total:.3f} - {n_gas:.4f} = {n_liq:.4f} \text{{ mol}}")
            st.latex(rf"W_{{液}} = {n_liq:.4f} \times 18.0 = \mathbf{{{W_liq:.3f} \text{{ g}}}}")
            st.markdown('</div>', unsafe_allow_html=True)

    elif abs(P_theo - Pv0) <= epsilon:
        # P == Pv0
        st.warning(f"**判斷結果： 理論壓力 $P ({P_theo:.4f}\text{{ atm}}) = P_v^0 ({Pv0:.3f}\text{{ atm}})$**")
        st.markdown('<div class="rule-box">表示氣體<b>恰好蒸乾無液體</b>，達完全汽化點，實際壓力 $P = P_v^0$[cite: 5]。</div>', unsafe_allow_html=True)
        st.markdown("#### 💧 殘留液態水量： **0 g**")

    else:
        # P < Pv0
        st.success(f"**判斷結果： 理論壓力 $P ({P_theo:.4f}\text{{ atm}}) < P_v^0 ({Pv0:.3f}\text{{ atm}})$**")
        st.markdown(f'<div class="rule-box">表示<b>僅有氣體 (未飽和)</b>，水已完全汽化，實際壓力為計算所得之 $P = {P_theo:.4f}\text{{ atm}}$[cite: 5]。</div>', unsafe_allow_html=True)
        st.markdown("#### 💧 殘留液態水量： **0 g**")
