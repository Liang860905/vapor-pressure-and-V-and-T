import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="水的三態與飽和蒸氣壓互動模擬", layout="wide")

# 移除 Streamlit 預設過多的上下留白，爭取最大顯示空間
st.markdown("""
    <style>
        .block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("化學教學互動模擬：水的飽和蒸氣壓與動態平衡")

# 使用 Streamlit 內建的分頁切換兩個專案
tab1, tab2 = st.tabs(["📊 專案一：蒸發與凝結速率動態平衡 (r - t 圖)", "🔥 專案二：蒸氣壓與溫度、容器體積關係 (P-T / P-V 圖)"])

with tab1:
    st.markdown("觀察定溫下密閉容器中，隨時間推進**蒸發速率**與**凝結速率**的變化，以及微觀粒子達動態平衡的實體動畫[cite: 1]。")
    
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
        .btn:hover { background: #1d4ed8; }
        .btn-reset { background: #64748b; }
        .slider-wrap { flex-grow: 1; display: flex; align-items: center; gap: 10px; min-width: 240px; }
        input[type=range] { flex-grow: 1; height: 6px; cursor: pointer; accent-color: #2563eb; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }
        .metric-card { background: #ffffff; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .metric-title { font-size: 11.5px; color: #64748b; margin-bottom: 2px; font-weight: 600; }
        .metric-value { font-size: 17px; font-weight: 700; }
        .status-banner { grid-column: span 4; padding: 10px 14px; border-radius: 8px; font-size: 13px; line-height: 1.4; background: #eff6ff; border-left: 5px solid #2563eb; }
        .canvas-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; }
        @media (max-width: 768px) { .canvas-grid { grid-template-columns: 1fr; } .metrics-grid { grid-template-columns: repeat(2, 1fr); } .status-banner { grid-column: span 2; } }
        .canvas-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; display: flex; flex-direction: column; align-items: center; width: 100%; }
        /* 嚴格鎖定畫布比例與高畫質 CSS 顯示大小，解決模糊與壓扁問題 */
        canvas { width: 100%; max-width: 440px; height: 350px; display: block; }
        .box-title { font-size: 13.5px; font-weight: 700; color: #334155; margin-bottom: 4px; }
        .legend-bar { display: flex; gap: 12px; font-size: 11.5px; color: #475569; margin-top: 4px; justify-content: center; flex-wrap: wrap; }
        .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
    </style>
    </head>
    <body>
    <div class="control-panel">
        <button id="playBtn1" class="btn">⏸ 暫停時間</button>
        <button id="resetBtn1" class="btn btn-reset">🔄 重置 (t=0)</button>
        <div class="slider-wrap">
            <span style="font-weight:600; font-size:13px;">時間軸 (t)：</span>
            <input type="range" id="timeSlider1" min="0" max="10" step="0.05" value="0">
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
            <div class="box-title">速率對時間關係圖 (r - t 圖)</div>
            <canvas id="gCanvas1" width="880" height="700"></canvas>
        </div>
        <div class="canvas-box">
            <div class="box-title">密閉容器微觀動態 (60 FPS 實體碰撞)</div>
            <canvas id="bCanvas1" width="880" height="700"></canvas>
            <div class="legend-bar">
                <span><span class="dot" style="background:#f59e0b;"></span>水蒸氣 H₂O(g)</span>
                <span><span class="dot" style="background:#16a34a;"></span>蒸發 (↑)</span>
                <span><span class="dot" style="background:#ea580c;"></span>凝結 (↓)</span>
            </div>
        </div>
    </div>
    <script>
    const gC1 = document.getElementById('gCanvas1'), gCtx1 = gC1.getContext('2d');
    const bC1 = document.getElementById('bCanvas1'), bCtx1 = bC1.getContext('2d');
    gCtx1.scale(2, 2); bCtx1.scale(2, 2); // 2x 高畫質 Retina 縮放，畫面極致清晰不模糊

    let t1 = 0.0, isPlay1 = true;
    const r_evap1 = 10.0, t_eq1 = 7.0, k1 = 0.45, norm1 = 1 - Math.exp(-k1 * t_eq1), maxP1 = 45;
    const BL1 = 55, BR1 = 385, BT1 = 35, BB1 = 310;

    function getRC1(time) {
        if (time <= 0) return 0;
        if (time >= t_eq1) return r_evap1;
        return r_evap1 * (1 - Math.exp(-k1 * time)) / norm1;
    }

    let liqP1 = [];
    for(let i=0; i<60; i++) liqP1.push({x: BL1+15+Math.random()*(BR1-BL1-30), y: 220+Math.random()*(BB1-230), vx:(Math.random()-0.5)*0.6, vy:(Math.random()-0.5)*0.6});
    let gasP1 = [], eff1 = [];

    function spawnGP1(fromSurf=true, waterY=210) {
        const x = BL1 + 25 + Math.random()*(BR1 - BL1 - 50);
        const y = fromSurf ? waterY - 4 : BT1 + 20 + Math.random()*(waterY - BT1 - 35);
        const angle = -Math.PI/4 - Math.random()*(Math.PI/2);
        const speed = 2.2 + Math.random()*1.2;
        gasP1.push({ x, y, vx: fromSurf ? Math.cos(angle)*speed : (Math.random()-0.5)*3, vy: fromSurf ? Math.sin(angle)*speed : (Math.random()-0.5)*3, hGreen: fromSurf ? 25 : 0 });
        if(fromSurf) eff1.push({x, y: waterY, type:'evap', age:0, maxAge:25});
    }

    document.getElementById('timeSlider1').addEventListener('input', e => { t1 = parseFloat(e.target.value); isPlay1 = false; document.getElementById('playBtn1').textContent = "▶ 繼續"; });
    document.getElementById('playBtn1').addEventListener('click', () => { isPlay1 = !isPlay1; if(isPlay1 && t1>=10) t1=0; document.getElementById('playBtn1').textContent = isPlay1 ? "⏸ 暫停時間" : "▶ 繼續"; });
    document.getElementById('resetBtn1').addEventListener('click', () => { t1=0; document.getElementById('timeSlider1').value=0; gasP1=[]; eff1=[]; isPlay1=false; document.getElementById('playBtn1').textContent="▶ 開始"; });

    function animate1() {
        if(isPlay1) { t1 += 0.015; if(t1>10) { t1=10; isPlay1=false; document.getElementById('playBtn1').textContent="▶ 重新播放"; } document.getElementById('timeSlider1').value = t1; }
        const rc = getRC1(t1), ratio = rc / r_evap1;

        // 更新數據面板
        document.getElementById('timeLabel1').textContent = t1.toFixed(1) + " s";
        document.getElementById('rCondVal1').textContent = rc.toFixed(1);
        const targetC = Math.round(maxP1 * ratio);
        document.getElementById('pCountVal1').textContent = `${targetC} / ${maxP1}`;
        document.getElementById('pressureVal1').textContent = `${Math.round(ratio*100)}% 飽和`;

        if(t1 === 0) document.getElementById('statusBanner1').innerHTML = "<b>狀態 ①：初始 (t = 0)</b> — 上方尚無水蒸氣，僅有水分子從液面蒸發（<b>r_蒸發 > 0，r_凝結 = 0</b>）[cite: 1]。";
        else if(t1 < t_eq1) document.getElementById('statusBanner1').innerHTML = "<b>狀態 ②：未飽和階段</b> — 蒸氣壓上升，凝結速率隨之加快，但蒸發仍大於凝結[cite: 1]。";
        else document.getElementById('statusBanner1').innerHTML = "<b>狀態 ③：達動態平衡 (r_蒸發 = r_凝結 ≠ 0)</b> — 蒸發與凝結速率相等，粒子數維持固定，此即<b>飽和蒸氣壓</b>[cite: 1]！";

        // 1. 繪製左側曲線圖 (440x350 邏輯坐標)
        gCtx1.clearRect(0, 0, 440, 350);
        const ox=45, oy=290, w=375, h=230;
        gCtx1.strokeStyle="#334155"; gCtx1.lineWidth=2; gCtx1.beginPath();
        gCtx1.moveTo(ox, oy-h-10); gCtx1.lineTo(ox, oy); gCtx1.lineTo(ox+w+10, oy); gCtx1.stroke();
        gCtx1.fillStyle="#334155"; gCtx1.font="bold 12px sans-serif"; gCtx1.fillText("速率 (r)", 8, 25); gCtx1.fillText("時間 (t)", ox+w-20, oy+22);

        const eqX = ox + (t_eq1/10)*w;
        gCtx1.setLineDash([3,3]); gCtx1.strokeStyle="#cbd5e1"; gCtx1.beginPath(); gCtx1.moveTo(eqX, oy-h); gCtx1.lineTo(eqX, oy); gCtx1.stroke(); gCtx1.setLineDash([]);
        
        // 趨勢淡線
        const evapY = oy - (r_evap1/12)*h;
        gCtx1.strokeStyle="rgba(22,163,74,0.25)"; gCtx1.lineWidth=3; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(ox+w, evapY); gCtx1.stroke();
        gCtx1.strokeStyle="rgba(234,88,12,0.25)"; gCtx1.beginPath();
        for(let i=0; i<=80; i++) { let ti=(i/80)*10, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
        gCtx1.stroke();

        // 實線
        const curX = ox + (t1/10)*w;
        gCtx1.strokeStyle="#16a34a"; gCtx1.lineWidth=3; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke();
        gCtx1.strokeStyle="#ea580c"; gCtx1.lineWidth=3; gCtx1.beginPath();
        const steps = Math.max(2, Math.floor(t1*12));
        for(let i=0; i<=steps; i++) { let ti=(i/steps)*t1, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
        gCtx1.stroke();

        gCtx1.fillStyle="#16a34a"; gCtx1.beginPath(); gCtx1.arc(curX, evapY, 5, 0, Math.PI*2); gCtx1.fill();
        gCtx1.fillStyle="#ea580c"; gCtx1.beginPath(); gCtx1.arc(curX, oy - (rc/12)*h, 5, 0, Math.PI*2); gCtx1.fill();

        // 2. 繪製右側微觀容器 (440x350 邏輯坐標)
        bCtx1.clearRect(0, 0, 440, 350);
        const waterY = 210 + ratio * 12;
        while(gasP1.length < Math.round(maxP1 * ratio)) spawnGP1(true, waterY);
        while(gasP1.length > Math.round(maxP1 * ratio)) gasP1.pop();

        if(Math.random() < 0.08) {
            if(Math.random() < ratio && gasP1.length > 0) {
                let m = gasP1.reduce((max, p) => p.y > max.y ? p : max, gasP1[0]);
                eff1.push({x: m.x, y: waterY, type:'cond', age:0, maxAge:25});
                gasP1.splice(gasP1.indexOf(m), 1);
                spawnGP1(true, waterY);
            } else if(t1 > 0) {
                eff1.push({x: BL1+30+Math.random()*(BR1-BL1-60), y: waterY, type:'evap', age:0, maxAge:25});
            }
        }

        bCtx1.fillStyle = "rgba(56, 189, 248, 0.35)"; bCtx1.fillRect(BL1, waterY, BR1 - BL1, BB1 - waterY);
        bCtx1.strokeStyle = "#0284c7"; bCtx1.lineWidth = 2; bCtx1.beginPath(); bCtx1.moveTo(BL1, waterY); bCtx1.lineTo(BR1, waterY); bCtx1.stroke();

        // 水中粒子
        bCtx1.fillStyle = "rgba(2, 132, 199, 0.45)";
        for(let lp of liqP1) {
            lp.x += lp.vx; lp.y += lp.vy;
            if(lp.x < BL1+6 || lp.x > BR1-6) lp.vx *= -1;
            if(lp.y < waterY+6) lp.y = waterY+6; if(lp.y > BB1-6) lp.y = BB1-6;
            bCtx1.beginPath(); bCtx1.arc(lp.x, lp.y, 3.5, 0, Math.PI*2); bCtx1.fill();
        }

        // 氣體粒子
        for(let p of gasP1) {
            p.x += p.vx; p.y += p.vy;
            if(p.x < BL1+6 || p.x > BR1-6) { p.x = Math.max(BL1+6, Math.min(BR1-6, p.x)); p.vx *= -1; }
            if(p.y < BT1+6) { p.y = BT1+6; p.vy *= -1; }
            if(p.y > waterY - 6) { p.y = waterY - 6; p.vy *= -1; }

            bCtx1.beginPath(); bCtx1.arc(p.x, p.y, 5.5, 0, Math.PI*2);
            bCtx1.fillStyle = p.hGreen > 0 ? "#22c55e" : "#f59e0b";
            bCtx1.strokeStyle = p.hGreen > 0 ? "#15803d" : "#b45309";
            if(p.hGreen > 0) p.hGreen--;
            bCtx1.lineWidth = 1.2; bCtx1.fill(); bCtx1.stroke();
        }

        // 特效
        for(let i = eff1.length-1; i>=0; i--) {
            let ef = eff1[i]; ef.age++;
            let a = 1 - ef.age/ef.maxAge;
            bCtx1.font = "bold 11px sans-serif";
            if(ef.type === 'evap') {
                bCtx1.fillStyle = `rgba(22, 163, 74, ${a})`; bCtx1.fillText("↑蒸發", ef.x-14, ef.y - ef.age*0.7);
            } else {
                bCtx1.fillStyle = `rgba(234, 88, 12, ${a})`; bCtx1.fillText("↓凝結", ef.x-14, ef.y + ef.age*0.6+10);
            }
            if(ef.age >= ef.maxAge) eff1.splice(i, 1);
        }

        // 容器框
        bCtx1.strokeStyle = "#475569"; bCtx1.lineWidth = 3.5; bCtx1.strokeRect(BL1, BT1, BR1 - BL1, BB1 - BT1);
        bCtx1.fillStyle = "#64748b"; bCtx1.fillRect(BL1 - 10, BT1 - 8, (BR1 - BL1) + 20, 8);

        requestAnimationFrame(animate1);
    }
    animate1();
    </script>
    </body>
    </html>
    """
    components.html(html_tab1, height=730, scrolling=True)

with tab2:
    st.markdown("自由切換**「(1) 定容，改變溫度」**與**「(2) 定溫，改變容器體積」**，觀察液-氣共存與完全汽化轉折點[cite: 2]。")
    
    html_tab2 = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 4px; background: #ffffff; color: #1f2937; }
        .tabs-inner { display: flex; gap: 8px; margin-bottom: 8px; }
        .tab-btn-in { flex: 1; padding: 8px 12px; font-size: 13.5px; font-weight: 700; border: 2px solid #cbd5e1; border-radius: 8px; background: #f8fafc; color: #475569; cursor: pointer; }
        .tab-btn-in.active { background: #eff6ff; border-color: #2563eb; color: #1d4ed8; }
        .control-bar { background: #f8fafc; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 10px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
        .quick-btns { display: flex; gap: 6px; flex-wrap: wrap; }
        .q-btn { background: #e2e8f0; color: #334155; border: none; padding: 5px 9px; border-radius: 6px; font-weight: 600; font-size: 11.5px; cursor: pointer; }
        .q-btn:hover { background: #cbd5e1; }
        .slider-wrap { flex-grow: 1; display: flex; align-items: center; gap: 10px; min-width: 240px; }
        input[type=range] { flex-grow: 1; height: 6px; cursor: pointer; accent-color: #2563eb; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }
        .metric-card { background: #ffffff; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .metric-title { font-size: 11.5px; color: #64748b; margin-bottom: 2px; font-weight: 600; }
        .metric-value { font-size: 17px; font-weight: 700; }
        .status-banner { grid-column: span 4; padding: 10px 14px; border-radius: 8px; font-size: 13px; line-height: 1.4; background: #f0fdf4; border-left: 5px solid #16a34a; }
        .canvas-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; }
        @media (max-width: 768px) { .canvas-grid { grid-template-columns: 1fr; } .metrics-grid { grid-template-columns: repeat(2, 1fr); } .status-banner { grid-column: span 2; } }
        .canvas-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; display: flex; flex-direction: column; align-items: center; width: 100%; }
        canvas { width: 100%; max-width: 440px; height: 350px; display: block; }
        .box-title { font-size: 13.5px; font-weight: 700; color: #334155; margin-bottom: 4px; }
        .legend-bar { display: flex; gap: 12px; font-size: 11.5px; color: #475569; margin-top: 4px; justify-content: center; flex-wrap: wrap; }
        .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
    </style>
    </head>
    <body>
    <div class="tabs-inner">
        <button id="tabTemp" class="tab-btn-in active" onclick="switchMode('temp')">🔥 (1) 定容，改變溫度 (P-T 圖)</button>
        <button id="tabVol" class="tab-btn-in" onclick="switchMode('vol')">🧪 (2) 定溫，改變體積 (P-V 圖)</button>
    </div>
    <div class="control-bar">
        <div class="slider-wrap">
            <span id="sliderTitle2" style="font-weight:700; font-size:13px;">調整溫度 (T)：</span>
            <input type="range" id="mainSlider2" min="0" max="140" step="0.5" value="30">
            <span id="sliderValLabel2" style="font-weight:700; min-width:65px; color:#2563eb;">30.0 °C</span>
        </div>
        <div id="quickBtns2" class="quick-btns">
            <button class="q-btn" onclick="setSVal(30)">線段① 液氣共存</button>
            <button class="q-btn" onclick="setSVal(80)">★ 完全汽化點</button>
            <button class="q-btn" onclick="setSVal(120)">線段② 氣體獨存</button>
        </div>
    </div>
    <div class="metrics-grid">
        <div class="metric-card"><div class="metric-title" id="mTitle1">當前溫度 (T)</div><div class="metric-value" id="mVal1" style="color:#dc2626;">30.0 °C</div></div>
        <div class="metric-card"><div class="metric-title">蒸氣壓力 (P)</div><div class="metric-value" id="mVal2" style="color:#2563eb;">120 mmHg</div></div>
        <div class="metric-card"><div class="metric-title">氣相粒子數</div><div class="metric-value" id="mVal3" style="color:#d97706;">12 / 45 顆</div></div>
        <div class="metric-card"><div class="metric-title">殘留液態水</div><div class="metric-value" id="mVal4" style="color:#0284c7;">73%</div></div>
        <div class="status-banner" id="statusBanner2"></div>
    </div>
    <div class="canvas-grid">
        <div class="canvas-box">
            <div class="box-title" id="graphTitle2">壓力對溫度關係圖 (P - T 圖)</div>
            <canvas id="gCanvas2" width="880" height="700"></canvas>
        </div>
        <div class="canvas-box">
            <div class="box-title" id="simTitle2">定容加熱裝置與粒子動態</div>
            <canvas id="sCanvas2" width="880" height="700"></canvas>
            <div class="legend-bar">
                <span><span class="dot" style="background:#f59e0b;"></span>氣相水蒸氣</span>
                <span><span class="dot" style="background:#0284c7;"></span>液態水</span>
                <span><span class="dot" style="background:#16a34a;"></span>動態交換</span>
            </div>
        </div>
    </div>
    <script>
    const gC2 = document.getElementById('gCanvas2'), gCtx2 = gC2.getContext('2d');
    const sC2 = document.getElementById('sCanvas2'), sCtx2 = sC2.getContext('2d');
    gCtx2.scale(2, 2); sCtx2.scale(2, 2); // Retina 2x 高畫質晶片級渲染

    let mode2 = 'temp';
    const T_CRIT2 = 80.0, P_CRIT2 = 450.0, V_CRIT2 = 6.0, P_SAT2 = 380.0, TOT_P2 = 45;
    let liqP2 = [];
    for(let i=0; i<60; i++) liqP2.push({rx:Math.random(), ry:Math.random(), vx:(Math.random()-0.5)*0.01, vy:(Math.random()-0.5)*0.01});
    let gasP2 = [], eff2 = [];

    function switchMode(m) {
        mode2 = m;
        document.getElementById('tabTemp').className = mode2==='temp'?'tab-btn-in active':'tab-btn-in';
        document.getElementById('tabVol').className = mode2==='vol'?'tab-btn-in active':'tab-btn-in';
        eff2 = [];
        const sl = document.getElementById('mainSlider2');
        if(mode2==='temp') {
            document.getElementById('sliderTitle2').textContent = "調整溫度 (T)：";
            sl.min=0; sl.max=140; sl.step=0.5; sl.value=30;
            document.getElementById('mTitle1').textContent = "當前溫度 (T)";
            document.getElementById('graphTitle2').textContent = "壓力對溫度關係圖 (P - T 圖)";
            document.getElementById('simTitle2').textContent = "定容加熱裝置與粒子動態";
            document.getElementById('quickBtns2').innerHTML = `<button class="q-btn" onclick="setSVal(30)">線段① 共存</button><button class="q-btn" onclick="setSVal(80)">★ 完全汽化</button><button class="q-btn" onclick="setSVal(120)">線段② 獨存</button>`;
        } else {
            document.getElementById('sliderTitle2').textContent = "容器體積 (V)：";
            sl.min=1.5; sl.max=10.0; sl.step=0.05; sl.value=2.0;
            document.getElementById('mTitle1').textContent = "容器體積 (V)";
            document.getElementById('graphTitle2').textContent = "壓力對體積關係圖 (P - V 圖)";
            document.getElementById('simTitle2').textContent = "定溫附活塞汽缸動態模擬";
            document.getElementById('quickBtns2').innerHTML = `<button class="q-btn" onclick="setSVal(2.0)">狀態 A</button><button class="q-btn" onclick="setSVal(4.0)">狀態 B 共存</button><button class="q-btn" onclick="setSVal(6.0)">★ 狀態 C 完全汽化</button><button class="q-btn" onclick="setSVal(9.0)">狀態 D 獨存</button>`;
        }
    }
    function setSVal(v) { document.getElementById('mainSlider2').value = v; }

    function getP_T(tc) {
        if(tc <= T_CRIT2) return 70 * Math.exp(Math.log(P_CRIT2/70) * (tc/T_CRIT2));
        return P_CRIT2 * ((tc + 273)/(T_CRIT2 + 273));
    }
    function getP_V(v) { return v <= V_CRIT2 ? P_SAT2 : P_SAT2 * (V_CRIT2 / v); }

    function getState2() {
        const val = parseFloat(document.getElementById('mainSlider2').value);
        if(mode2==='temp') {
            const T_c=val, T_k=T_c+273, P=getP_T(T_c);
            const n_r = Math.min(1.0, (P/T_k) / (P_CRIT2/(T_CRIT2+273)));
            return {val:T_c, T_k, P, gasCount:Math.round(TOT_P2*n_r), liqFrac:Math.max(0, 1.0-n_r), speed:Math.sqrt(T_k/298)*1.1};
        } else {
            const V=val, P=getP_V(V);
            const n_r = Math.min(1.0, V/V_CRIT2);
            return {val:V, P, gasCount:Math.round(TOT_P2*n_r), liqFrac:Math.max(0, 1.0-n_r), speed:1.0};
        }
    }

    function animate2() {
        const st = getState2();

        // 介面文字更新
        if(mode2==='temp') {
            document.getElementById('sliderValLabel2').textContent = st.val.toFixed(1) + " °C";
            document.getElementById('mVal1').textContent = st.val.toFixed(1) + " °C";
            document.getElementById('mVal2').textContent = Math.round(st.P) + " mmHg";
            document.getElementById('mVal3').textContent = `${st.gasCount} / 45 顆`;
            document.getElementById('mVal4').textContent = st.liqFrac>0.005 ? `${Math.round(st.liqFrac*100)}%` : `0% (完汽)`;
            
            if(Math.abs(st.val - T_CRIT2) < 0.8) document.getElementById('statusBanner2').innerHTML = "<b>★ 轉折點：液體恰好完全汽化 (80°C)</b> — 最後一滴液態水剛好蒸發完畢，之後轉為斜直線[cite: 2]。";
            else if(st.val < T_CRIT2) document.getElementById('statusBanner2').innerHTML = "<b>線段 ①：液-氣共存</b> — 溫度愈高，飽和蒸氣壓愈大（非正比曲線上升）[cite: 2]。";
            else document.getElementById('statusBanner2').innerHTML = "<b>線段 ②：氣體獨存</b> — 遵守理想氣體定律，壓力與絕對溫度成正比[cite: 2]。";
        } else {
            document.getElementById('sliderValLabel2').textContent = st.val.toFixed(2) + " L";
            document.getElementById('mVal1').textContent = st.val.toFixed(2) + " L";
            document.getElementById('mVal2').textContent = Math.round(st.P) + " mmHg";
            document.getElementById('mVal3').textContent = `${st.gasCount} / 45 顆`;
            document.getElementById('mVal4').textContent = st.liqFrac>0.005 ? `${Math.round(st.liqFrac*100)}%` : `0% (完汽)`;

            if(Math.abs(st.val - V_CRIT2) < 0.12) document.getElementById('statusBanner2').innerHTML = "<b>★ 狀態 C：恰好完全汽化 (6.0 L)</b> — 液態水剛好全變成蒸氣[cite: 2]。";
            else if(st.val < V_CRIT2) document.getElementById('statusBanner2').innerHTML = "<b>線段 ③：液-氣共存</b> — 只要有液體存在，定溫下飽和蒸氣壓恆為定值[cite: 2]。";
            else document.getElementById('statusBanner2').innerHTML = "<b>線段 ④：氣體獨存</b> — 遵守波以耳定律，體積愈大壓力愈小[cite: 2]。";
        }

        // 1. 繪製左側圖表 (440x350 邏輯坐標)
        gCtx2.clearRect(0,0,440,350);
        if(mode2==='temp') {
            const ox=135, zX=30, oy=290, mX=420, h=240, maxP=600;
            const tX = tc => tc>=0 ? ox + (tc/140)*(mX-ox) : ox + (tc/273)*(ox-zX);
            const pY = p => oy - (p/maxP)*h;

            gCtx2.strokeStyle="#334155"; gCtx2.lineWidth=2; gCtx2.beginPath();
            gCtx2.moveTo(zX-5, oy); gCtx2.lineTo(mX+10, oy); gCtx2.moveTo(ox, oy-h-15); gCtx2.lineTo(ox, oy); gCtx2.stroke();
            gCtx2.fillStyle="#334155"; gCtx2.font="bold 11.5px sans-serif";
            gCtx2.fillText("壓力", ox-45, 20); gCtx2.fillText("溫度 (°C)", mX-45, oy+22);
            gCtx2.fillText("-273°C", zX-12, oy+18); gCtx2.fillText("0", ox-4, oy+18);

            const cX = tX(T_CRIT2), cY = pY(P_CRIT2);
            gCtx2.setLineDash([4,4]); gCtx2.strokeStyle="#64748b"; gCtx2.beginPath(); gCtx2.moveTo(zX, oy); gCtx2.lineTo(cX, cY); gCtx2.stroke(); gCtx2.setLineDash([]);

            // 線段①
            gCtx2.strokeStyle="#16a34a"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            for(let tc=0; tc<=T_CRIT2; tc+=1) { let px=tX(tc), py=pY(getP_T(tc)); if(tc===0)gCtx2.moveTo(px,py); else gCtx2.lineTo(px,py); }
            gCtx2.stroke();
            // 線段②
            gCtx2.strokeStyle="#0284c7"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            gCtx2.moveTo(cX, cY); gCtx2.lineTo(tX(140), pY(getP_T(140))); gCtx2.stroke();

            // 當前點
            const curX = tX(st.val), curY = pY(st.P);
            gCtx2.fillStyle="#dc2626"; gCtx2.beginPath(); gCtx2.arc(curX, curY, 6, 0, Math.PI*2); gCtx2.fill();
            gCtx2.strokeStyle="#fff"; gCtx2.lineWidth=2; gCtx2.stroke();
        } else {
            const ox=55, oy=290, w=365, h=230, maxV=10.5, maxP=500;
            const vX = v => ox + (v/maxV)*w;
            const pY = p => oy - (p/maxP)*h;

            gCtx2.strokeStyle="#334155"; gCtx2.lineWidth=2; gCtx2.beginPath();
            gCtx2.moveTo(ox, oy-h-15); gCtx2.lineTo(ox, oy); gCtx2.lineTo(ox+w+10, oy); gCtx2.stroke();
            gCtx2.fillStyle="#334155"; gCtx2.font="bold 11.5px sans-serif";
            gCtx2.fillText("壓力", 10, 20); gCtx2.fillText("體積 (L)", ox+w-45, oy+22);

            const cX = vX(V_CRIT2), sY = pY(P_SAT2);
            // 線段③
            gCtx2.strokeStyle="#16a34a"; gCtx2.lineWidth=3.5; gCtx2.beginPath(); gCtx2.moveTo(ox, sY); gCtx2.lineTo(cX, sY); gCtx2.stroke();
            // 線段④
            gCtx2.strokeStyle="#ea580c"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            for(let v=V_CRIT2; v<=10; v+=0.1) { let px=vX(v), py=pY(getP_V(v)); if(v===V_CRIT2)gCtx2.moveTo(px,py); else gCtx2.lineTo(px,py); }
            gCtx2.stroke();

            // 當前點
            const curX = vX(st.val), curY = pY(st.P);
            gCtx2.fillStyle="#2563eb"; gCtx2.beginPath(); gCtx2.arc(curX, curY, 6, 0, Math.PI*2); gCtx2.fill();
            gCtx2.strokeStyle="#fff"; gCtx2.lineWidth=2; gCtx2.stroke();
        }

        // 2. 繪製右側微觀容器 (440x350 邏輯坐標)
        sCtx2.clearRect(0,0,440,350);
        const BL=85, BR=315;
        let BT=45, BB=290;
        if(mode2==='vol') {
            const gH = 45 + ((st.val - 1.5)/8.5)*175;
            BT = (290 - 24*st.liqFrac) - gH;
        }
        const waterY = BB - 24*st.liqFrac;

        while(gasP2.length < st.gasCount) {
            gasP2.push({x:BL+15+Math.random()*(BR-BL-30), y:waterY-10-Math.random()*25, vx:(Math.random()-0.5)*3, vy:(Math.random()-0.5)*3});
        }
        while(gasP2.length > st.gasCount) gasP2.pop();

        if(st.liqFrac > 0.005) {
            sCtx2.fillStyle="rgba(56, 189, 248, 0.4)"; sCtx2.fillRect(BL, waterY, BR-BL, BB-waterY);
            sCtx2.strokeStyle="#0284c7"; sCtx2.lineWidth=2; sCtx2.beginPath(); sCtx2.moveTo(BL, waterY); sCtx2.lineTo(BR, waterY); sCtx2.stroke();

            sCtx2.fillStyle="rgba(2, 132, 199, 0.55)";
            for(let i=0; i<Math.round(50*st.liqFrac); i++) {
                let lp = liqP2[i];
                lp.rx += lp.vx*st.speed; lp.ry += lp.vy*st.speed;
                if(lp.rx<0.05||lp.rx>0.95)lp.vx*=-1; if(lp.ry<0.1||lp.ry>0.9)lp.vy*=-1;
                sCtx2.beginPath(); sCtx2.arc(BL + lp.rx*(BR-BL), waterY + lp.ry*(BB-waterY), 3, 0, Math.PI*2); sCtx2.fill();
            }
        }

        for(let p of gasP2) {
            p.x += p.vx*st.speed; p.y += p.vy*st.speed;
            if(p.x < BL+6 || p.x > BR-6) { p.x = Math.max(BL+6, Math.min(BR-6, p.x)); p.vx *= -1; }
            if(p.y < BT+6) { p.y = BT+6; p.vy *= -1; }
            if(p.y > waterY-6) { p.y = waterY-6; p.vy *= -1; }

            sCtx2.beginPath(); sCtx2.arc(p.x, p.y, 5, 0, Math.PI*2);
            sCtx2.fillStyle="#f59e0b"; sCtx2.strokeStyle="#b45309"; sCtx2.lineWidth=1.2;
            sCtx2.fill(); sCtx2.stroke();
        }

        if(mode2==='temp') {
            sCtx2.strokeStyle="#475569"; sCtx2.lineWidth=3.5; sCtx2.strokeRect(BL, BT, BR-BL, BB-BT);
            sCtx2.fillStyle="#64748b"; sCtx2.fillRect(BL-8, BT-8, (BR-BL)+16, 8);
            // 本生燈
            sCtx2.fillStyle="#475569"; sCtx2.fillRect(188, 292, 24, 25);
            sCtx2.fillStyle="rgba(239,68,68,0.85)"; sCtx2.beginPath(); sCtx2.moveTo(182, 292); sCtx2.quadraticCurveTo(200, 260, 218, 292); sCtx2.fill();
        } else {
            sCtx2.strokeStyle="#475569"; sCtx2.lineWidth=3.5; sCtx2.beginPath(); sCtx2.moveTo(BL, 40); sCtx2.lineTo(BL, BB); sCtx2.lineTo(BR, BB); sCtx2.lineTo(BR, 40); sCtx2.stroke();
            sCtx2.fillStyle="#94a3b8"; sCtx2.fillRect(BL+2, BT-12, BR-BL-4, 12);
            sCtx2.fillStyle="#64748b"; sCtx2.fillRect(194, 12, 12, BT-20);
        }

        requestAnimationFrame(animate2);
    }
    animate2();
    </script>
    </body>
    </html>
    """
    components.html(html_tab2, height=730, scrolling=True)
