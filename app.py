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
    "📊 專案一：蒸發與凝結動態平衡 (r-t / P-t 圖)", 
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
        .btn:hover { background: #1d4ed8; }
        .btn-reset { background: #64748b; }
        .btn-reset:hover { background: #475569; }
        .speed-select { padding: 5px 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; font-weight: 600; color: #334155; background: #fff; cursor: pointer; }
        .slider-wrap { flex-grow: 1; display: flex; align-items: center; gap: 10px; min-width: 240px; }
        input[type=range] { flex-grow: 1; height: 6px; cursor: pointer; accent-color: #2563eb; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }
        .metric-card { background: #ffffff; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .metric-title { font-size: 11.5px; color: #64748b; margin-bottom: 2px; font-weight: 600; }
        .metric-value { font-size: 17px; font-weight: 700; }
        .status-banner { grid-column: span 4; padding: 10px 14px; border-radius: 8px; font-size: 13px; line-height: 1.4; background: #eff6ff; border-left: 5px solid #2563eb; }
        .canvas-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%; }
        @media (max-width: 768px) { .canvas-grid { grid-template-columns: 1fr; } .metrics-grid { grid-template-columns: repeat(2, 1fr); } .status-banner { grid-column: span 2; } }
        .canvas-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; display: flex; flex-direction: column; align-items: center; width: 100%; position: relative; }
        canvas { width: 100%; max-width: 440px; height: 330px; display: block; }
        .box-title { font-size: 13.5px; font-weight: 700; color: #334155; margin-bottom: 4px; }
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
            <select id="speedSel1" class="speed-select">
                <option value="0.0025">0.5x (慢速觀察)</option>
                <option value="0.005" selected>1.0x (適中教學)</option>
                <option value="0.012">2.0x (快速推進)</option>
            </select>
        </div>
        <div class="slider-wrap">
            <span style="font-weight:600; font-size:13px;">時間軸 (t)：</span>
            <input type="range" id="timeSlider1" min="0" max="10" step="0.02" value="0">
            <span id="timeLabel1" style="font-weight:700; min-width:45px; color:#2563eb;">0.0 s</span>
        </div>
    </div>
    <div class="metrics-grid">
        <div class="metric-card"><div class="metric-title">蒸發速率 (r_蒸發)</div><div class="metric-value" style="color:#16a34a;">10.0 <span style="font-size:12px;font-weight:normal;color:#64748b;">(定溫恆定)</span></div></div>
        <div class="metric-card"><div class="metric-title">凝結速率 (r_凝結)</div><div class="metric-value" id="rCondVal1" style="color:#ea580c;">0.0</div></div>
        <div class="metric-card"><div class="metric-title">氣相水蒸氣粒子數</div><div class="metric-value" id="pCountVal1" style="color:#d97706;">0 / 45</div></div>
        <div class="metric-card"><div class="metric-title">蒸氣壓狀態</div><div class="metric-value" id="pressureVal1" style="color:#2563eb;">0% 飽直</div></div>
        <div class="status-banner" id="statusBanner1"></div>
    </div>
    <div class="canvas-grid">
        <div class="canvas-box">
            <div class="chart-toggles">
                <button id="btnRT" class="c-btn active">📈 速率對時間 (r-t 圖)</button>
                <button id="btnPT" class="c-btn">☁️ 蒸氣壓對時間 (P-t 圖)</button>
            </div>
            <canvas id="gCanvas1" width="880" height="660"></canvas>
        </div>
        <div class="canvas-box">
            <div class="box-title" style="margin-bottom:10px;">密閉容器微觀動態 (一進一出動態平衡觀察)</div>
            <canvas id="bCanvas1" width="880" height="660"></canvas>
            <div class="legend-bar">
                <span><span class="dot" style="background:#f59e0b;"></span>水蒸氣 H₂O(g)</span>
                <span><span class="dot" style="background:#22c55e; border:1px solid #15803d;"></span>剛蒸發分子 (↑)</span>
                <span><span class="dot" style="background:#ea580c; border:1px solid #9a3412;"></span>凝結入水分子 (↓)</span>
            </div>
        </div>
    </div>
    <script>
    const gC1 = document.getElementById('gCanvas1'), gCtx1 = gC1.getContext('2d');
    const bC1 = document.getElementById('bCanvas1'), bCtx1 = bC1.getContext('2d');
    gCtx1.scale(2, 2); bCtx1.scale(2, 2);

    let t1 = 0.0, isPlay1 = true, dt1 = 0.005;
    let currentView = 'rt'; 
    const r_evap1 = 10.0, t_eq1 = 7.0, k1 = 0.45, norm1 = 1 - Math.exp(-k1 * t_eq1), maxP1 = 45;
    const BL1 = 55, BR1 = 385, BT1 = 52, BB1 = 300;

    const EVAP_INTERVAL = 24;
    let evapTimer = 0;
    let condAccumulator = 0;

    function getRC1(time) {
        if (time <= 0) return 0;
        if (time >= t_eq1) return r_evap1;
        return r_evap1 * (1 - Math.exp(-k1 * time)) / norm1;
    }

    let liqP1 = [];
    for(let i=0; i<65; i++) liqP1.push({x: BL1+15+Math.random()*(BR1-BL1-30), y: 210+Math.random()*(BB1-220), vx:(Math.random()-0.5)*0.6, vy:(Math.random()-0.5)*0.6});
    let gasP1 = [], condAnimP1 = [], eff1 = [];

    function spawnGP1(fromSurf=true, waterY=200, customX=null) {
        const x = customX !== null ? customX : (BL1 + 28 + Math.random()*(BR1 - BL1 - 56));
        const y = fromSurf ? waterY - 3 : BT1 + 20 + Math.random()*(waterY - BT1 - 35);
        const angle = -Math.PI/3 - Math.random()*(Math.PI/3);
        const speed = 1.9 + Math.random()*0.9;
        gasP1.push({
            x, y,
            vx: fromSurf ? Math.cos(angle)*speed : (Math.random()-0.5)*2.4,
            vy: fromSurf ? Math.sin(angle)*speed : (Math.random()-0.5)*2.4,
            hGreen: fromSurf ? 42 : 0
        });
    }

    function triggerEvapVisual(waterY) {
        const x = BL1 + 30 + Math.random()*(BR1 - BL1 - 60);
        eff1.push({x, y: waterY, type:'evap', age:0, maxAge:38});
        return x;
    }

    function triggerCondVisual(waterY) {
        let x = BL1 + 30 + Math.random()*(BR1 - BL1 - 60);
        if (gasP1.length > 0) {
            let bestIdx = 0, bestY = -1;
            for (let i = 0; i < gasP1.length; i++) {
                if (gasP1[i].hGreen === 0 && gasP1[i].y > bestY) {
                    bestY = gasP1[i].y;
                    bestIdx = i;
                }
            }
            let p = gasP1.splice(bestIdx, 1)[0];
            x = p.x;
            condAnimP1.push({x: p.x, y: Math.min(p.y, waterY - 18), targetY: waterY + 12, vy: 2.8, age: 0});
        } else {
            condAnimP1.push({x, y: waterY - 20, targetY: waterY + 12, vy: 2.8, age: 0});
        }
        eff1.push({x, y: waterY, type:'cond', age:0, maxAge:38});
    }

    document.getElementById('btnRT').addEventListener('click', () => {
        currentView = 'rt';
        document.getElementById('btnRT').className = 'c-btn active';
        document.getElementById('btnPT').className = 'c-btn';
    });
    document.getElementById('btnPT').addEventListener('click', () => {
        currentView = 'pt';
        document.getElementById('btnPT').className = 'c-btn active';
        document.getElementById('btnRT').className = 'c-btn';
    });

    document.getElementById('speedSel1').addEventListener('change', e => {
        dt1 = parseFloat(e.target.value);
    });
    document.getElementById('timeSlider1').addEventListener('input', e => {
        t1 = parseFloat(e.target.value);
        isPlay1 = false;
        document.getElementById('playBtn1').textContent = "▶ 繼續時間";
    });
    document.getElementById('playBtn1').addEventListener('click', () => {
        if (t1 >= 10) {
            t1 = 0; gasP1 = []; condAnimP1 = []; eff1 = []; evapTimer = 0; condAccumulator = 0;
            isPlay1 = true;
        } else {
            isPlay1 = !isPlay1;
        }
        document.getElementById('playBtn1').textContent = isPlay1 ? "⏸ 暫停時間" : "▶ 繼續時間";
    });
    document.getElementById('resetBtn1').addEventListener('click', () => {
        t1 = 0; document.getElementById('timeSlider1').value = 0;
        gasP1 = []; condAnimP1 = []; eff1 = []; evapTimer = 0; condAccumulator = 0;
        isPlay1 = false;
        document.getElementById('playBtn1').textContent = "▶ 開始播放";
    });

    function drawRateComparisonBar(ctx, ratio, isEq) {
        const bx = 55, by = 0, bw = 330, bh = 32;
        ctx.fillStyle = isEq ? "#f0fdf4" : "#f8fafc";
        ctx.strokeStyle = isEq ? "#16a34a" : "#cbd5e1";
        ctx.lineWidth = isEq ? 1.8 : 1.2;
        ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 6); ctx.fill(); ctx.stroke();

        const midX = bx + bw / 2;
        const maxBarW = 82;
        const evapW = maxBarW;
        const condW = maxBarW * ratio;

        ctx.fillStyle = "#16a34a";
        ctx.fillRect(midX - 38 - evapW, by + 9, evapW, 14);
        ctx.font = "bold 11px sans-serif";
        ctx.textAlign = "right";
        ctx.fillText("↑ 蒸發 10.0", midX - 42, by + 20);

        ctx.textAlign = "center";
        ctx.font = "bold 12px sans-serif";
        ctx.fillStyle = isEq ? "#15803d" : "#475569";
        ctx.fillText(isEq ? "＝" : "＞", midX, by + 21);

        ctx.fillStyle = "#ea580c";
        ctx.fillRect(midX + 38, by + 9, condW, 14);
        ctx.textAlign = "left";
        ctx.font = "bold 11px sans-serif";
        ctx.fillText(`↓ 凝結 ${(10*ratio).toFixed(1)}`, midX + 42, by + 20);
    }

    function animate1() {
        if(isPlay1 && t1 < 10) {
            t1 += dt1;
            if(t1 >= 10) {
                t1 = 10;
                document.getElementById('playBtn1').textContent = "🔄 重新播放時間";
            }
            document.getElementById('timeSlider1').value = t1;
        }
        const rc = getRC1(t1), ratio = rc / r_evap1;
        const isEq = t1 >= t_eq1;

        document.getElementById('timeLabel1').textContent = t1.toFixed(1) + " s";
        document.getElementById('rCondVal1').innerHTML = isEq ? `10.0 <span style="font-size:12px;color:#16a34a;">(= r_蒸發)</span>` : rc.toFixed(1);
        const targetC = Math.round(maxP1 * ratio);
        document.getElementById('pCountVal1').textContent = `${targetC} / ${maxP1}`;
        document.getElementById('pressureVal1').textContent = `${Math.round(ratio*100)}% 飽和`;

        if(t1 === 0) {
            document.getElementById('statusBanner1').style.background = "#eff6ff";
            document.getElementById('statusBanner1').style.borderLeftColor = "#2563eb";
            document.getElementById('statusBanner1').innerHTML = "<b>狀態 ①：初始瞬間 (t = 0)</b> — 容器上方尚無水蒸氣，僅有水分子從液面蒸發（<b>r_蒸發 = 10.0，r_凝結 = 0</b>）。";
        } else if(t1 < t_eq1) {
            document.getElementById('statusBanner1').style.background = "#fffbeb";
            document.getElementById('statusBanner1').style.borderLeftColor = "#f59e0b";
            document.getElementById('statusBanner1').innerHTML = "<b>狀態 ②：未飽和階段 (0 &lt; t &lt; 7s)</b> — 氣相水分子漸增，凝結頻率隨之加快，但<b>每秒蒸發顆數仍多於凝結顆數 (r_蒸發 &gt; r_凝結)</b>。";
        } else {
            document.getElementById('statusBanner1').style.background = "#f0fdf4";
            document.getElementById('statusBanner1').style.borderLeftColor = "#16a34a";
            document.getElementById('statusBanner1').innerHTML = "<b>狀態 ③：達動態平衡 (t ≥ 7s，r_蒸發 = r_凝結 = 10.0)</b> — 請觀察液面：<b>每蒸發 1 顆水分子，同時就有 1 顆水蒸氣凝結回水中</b>，氣相總粒子數維持 45 顆不變！";
        }

        gCtx1.clearRect(0, 0, 440, 330);
        const ox=45, oy=280, w=375, h=230;
        
        gCtx1.strokeStyle="#334155"; gCtx1.lineWidth=2; gCtx1.beginPath();
        gCtx1.moveTo(ox, oy-h-10); gCtx1.lineTo(ox, oy); gCtx1.lineTo(ox+w+10, oy); gCtx1.stroke();
        
        const eqX = ox + (t_eq1/10)*w;
        const evapY = oy - (r_evap1/12)*h;
        const curX = ox + (t1/10)*w;

        if (currentView === 'rt') {
            gCtx1.fillStyle="#334155"; gCtx1.font="bold 12px sans-serif"; gCtx1.fillText("速率 (r)", 8, 25); gCtx1.fillText("時間 (t)", ox+w-20, oy+22);

            if (t1 >= t_eq1) {
                gCtx1.fillStyle = "rgba(22, 163, 74, 0.08)";
                gCtx1.fillRect(eqX, oy-h, (ox+w)-eqX, h);
                gCtx1.fillStyle = "#15803d";
                gCtx1.font = "bold 11.5px sans-serif";
                gCtx1.fillText("動態平衡區 (r_蒸發 = r_凝結)", eqX + 6, oy - h + 18);
            }

            gCtx1.setLineDash([4,4]); gCtx1.strokeStyle="#94a3b8"; gCtx1.beginPath(); gCtx1.moveTo(eqX, oy-h); gCtx1.lineTo(eqX, oy); gCtx1.stroke(); gCtx1.setLineDash([]);
            gCtx1.fillStyle="#64748b"; gCtx1.font="11px sans-serif"; gCtx1.fillText("t_平衡 (7s)", eqX-24, oy+16);

            gCtx1.strokeStyle="rgba(22,163,74,0.22)"; gCtx1.lineWidth=3; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(ox+w, evapY); gCtx1.stroke();
            gCtx1.strokeStyle="rgba(234,88,12,0.22)"; gCtx1.beginPath();
            for(let i=0; i<=80; i++) { let ti=(i/80)*10, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
            gCtx1.stroke();

            gCtx1.strokeStyle="#16a34a"; gCtx1.lineWidth=3.5; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke();

            gCtx1.strokeStyle="#ea580c"; gCtx1.lineWidth=3.2;
            if (t1 > t_eq1) {
                gCtx1.beginPath();
                for(let i=0; i<=60; i++) { let ti=(i/60)*t_eq1, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
                gCtx1.stroke();
                gCtx1.save(); gCtx1.setLineDash([6, 6]); gCtx1.beginPath(); gCtx1.moveTo(eqX, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke(); gCtx1.restore();
            } else {
                gCtx1.beginPath();
                const steps = Math.max(2, Math.floor(t1*12));
                for(let i=0; i<=steps; i++) { let ti=(i/steps)*t1, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
                gCtx1.stroke();
            }

            gCtx1.font="bold 11.5px sans-serif";
            gCtx1.fillStyle="#16a34a"; gCtx1.fillText("r_蒸發 (定值)", ox+10, evapY-8);
            gCtx1.fillStyle="#ea580c"; gCtx1.fillText("r_凝結", ox+45, oy-45);

            gCtx1.fillStyle="#16a34a"; gCtx1.beginPath(); gCtx1.arc(curX, evapY, 5.5, 0, Math.PI*2); gCtx1.fill();
            gCtx1.fillStyle="#ea580c"; gCtx1.beginPath(); gCtx1.arc(curX, oy - (rc/12)*h, 5, 0, Math.PI*2); gCtx1.fill();
        } 
        else if (currentView === 'pt') {
            gCtx1.fillStyle="#334155"; gCtx1.font="bold 12px sans-serif"; gCtx1.fillText("蒸氣壓 (P)", 8, 25); gCtx1.fillText("時間 (t)", ox+w-20, oy+22);
            
            if (t1 >= t_eq1) {
                gCtx1.fillStyle = "rgba(37, 99, 235, 0.05)";
                gCtx1.fillRect(eqX, oy-h, (ox+w)-eqX, h);
                gCtx1.fillStyle = "#1d4ed8";
                gCtx1.font = "bold 11.5px sans-serif";
                gCtx1.fillText("壓力達飽和不變區", eqX + 25, oy - h + 18);
            }

            gCtx1.setLineDash([4,4]); gCtx1.strokeStyle="#94a3b8"; gCtx1.beginPath(); gCtx1.moveTo(eqX, oy-h); gCtx1.lineTo(eqX, oy); gCtx1.stroke(); 
            gCtx1.fillStyle="#64748b"; gCtx1.font="11px sans-serif"; gCtx1.fillText("t_平衡 (7s)", eqX-24, oy+16);

            gCtx1.strokeStyle="#94a3b8"; gCtx1.beginPath(); gCtx1.moveTo(ox, evapY); gCtx1.lineTo(ox+w, evapY); gCtx1.stroke(); gCtx1.setLineDash([]);
            gCtx1.fillStyle="#2563eb"; gCtx1.font="bold 11.5px sans-serif"; gCtx1.fillText("飽和蒸氣壓 (P_sat)", ox+10, evapY-8);

            gCtx1.strokeStyle="rgba(37,99,235,0.22)"; gCtx1.lineWidth=3.2; gCtx1.beginPath();
            for(let i=0; i<=80; i++) { let ti=(i/80)*10, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
            gCtx1.stroke();

            gCtx1.strokeStyle="#2563eb"; gCtx1.lineWidth=3.5;
            if (t1 > t_eq1) {
                gCtx1.beginPath();
                for(let i=0; i<=60; i++) { let ti=(i/60)*t_eq1, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
                gCtx1.stroke();
                gCtx1.beginPath(); gCtx1.moveTo(eqX, evapY); gCtx1.lineTo(curX, evapY); gCtx1.stroke();
            } else {
                gCtx1.beginPath();
                const steps = Math.max(2, Math.floor(t1*12));
                for(let i=0; i<=steps; i++) { let ti=(i/steps)*t1, rc_i=getRC1(ti); let px=ox+(ti/10)*w, py=oy-(rc_i/12)*h; if(i===0)gCtx1.moveTo(px,py); else gCtx1.lineTo(px,py); }
                gCtx1.stroke();
            }

            gCtx1.fillStyle="#2563eb"; gCtx1.beginPath(); gCtx1.arc(curX, oy - (rc/12)*h, 5.5, 0, Math.PI*2); gCtx1.fill();
        }

        bCtx1.clearRect(0, 0, 440, 330);
        const waterY = 200 + ratio * 12;

        drawRateComparisonBar(bCtx1, ratio, isEq);

        const activeMicro = isPlay1 || t1 >= t_eq1;
        if (activeMicro && t1 > 0) {
            evapTimer++;
            if (evapTimer >= EVAP_INTERVAL) {
                evapTimer = 0;
                const spawnX = triggerEvapVisual(waterY);
                spawnGP1(true, waterY, spawnX);

                condAccumulator += ratio;
                if (condAccumulator >= 0.999) {
                    condAccumulator -= 1.0;
                    triggerCondVisual(waterY);
                }
            }
        }

        while(gasP1.length < targetC) spawnGP1(false, waterY);
        while(gasP1.length > targetC) gasP1.pop();

        bCtx1.fillStyle = "rgba(56, 189, 248, 0.35)"; bCtx1.fillRect(BL1, waterY, BR1 - BL1, BB1 - waterY);
        bCtx1.strokeStyle = "#0284c7"; bCtx1.lineWidth = 2; bCtx1.beginPath(); bCtx1.moveTo(BL1, waterY); bCtx1.lineTo(BR1, waterY); bCtx1.stroke();

        bCtx1.fillStyle = "rgba(2, 132, 199, 0.45)";
        for(let lp of liqP1) {
            lp.x += lp.vx; lp.y += lp.vy;
            if(lp.x < BL1+6 || lp.x > BR1-6) lp.vx *= -1;
            if(lp.y < waterY+6) lp.y = waterY+6; if(lp.y > BB1-6) lp.y = BB1-6;
            bCtx1.beginPath(); bCtx1.arc(lp.x, lp.y, 3.5, 0, Math.PI*2); bCtx1.fill();
        }

        for(let p of gasP1) {
            p.x += p.vx; p.y += p.vy;
            if(p.x < BL1+6 || p.x > BR1-6) { p.x = Math.max(BL1+6, Math.min(BR1-6, p.x)); p.vx *= -1; }
            if(p.y < BT1+6) { p.y = BT1+6; p.vy *= -1; }
            if(p.y > waterY - 6) { p.y = waterY - 6; p.vy *= -1; }

            bCtx1.beginPath(); bCtx1.arc(p.x, p.y, 5.5, 0, Math.PI*2);
            bCtx1.fillStyle = p.hGreen > 0 ? "#22c55e" : "#f59e0b";
            bCtx1.strokeStyle = p.hGreen > 0 ? "#15803d" : "#b45309";
            if(p.hGreen > 0) p.hGreen--;
            bCtx1.lineWidth = 1.4; bCtx1.fill(); bCtx1.stroke();
        }

        for(let i = condAnimP1.length - 1; i >= 0; i--) {
            let cp = condAnimP1[i];
            cp.y += cp.vy;
            cp.age++;
            bCtx1.strokeStyle = "rgba(234, 88, 12, 0.65)";
            bCtx1.lineWidth = 2;
            bCtx1.beginPath(); bCtx1.moveTo(cp.x, cp.y - 12); bCtx1.lineTo(cp.x, cp.y); bCtx1.stroke();
            bCtx1.beginPath(); bCtx1.arc(cp.x, cp.y, 5.5, 0, Math.PI*2);
            bCtx1.fillStyle = "#ea580c"; bCtx1.strokeStyle = "#9a3412"; bCtx1.lineWidth = 1.5;
            bCtx1.fill(); bCtx1.stroke();
            if(cp.y >= cp.targetY || cp.age > 20) condAnimP1.splice(i, 1);
        }

        for(let i = eff1.length-1; i>=0; i--) {
            let ef = eff1[i]; ef.age++;
            let a = Math.max(0, 1 - ef.age/ef.maxAge);
            bCtx1.font = "bold 12px sans-serif";
            if(ef.type === 'evap') {
                bCtx1.strokeStyle = `rgba(22, 163, 74, ${a * 0.8})`;
                bCtx1.lineWidth = 1.8;
                bCtx1.beginPath(); bCtx1.ellipse(ef.x, ef.y, 4 + ef.age*0.45, 2 + ef.age*0.15, 0, 0, Math.PI*2); bCtx1.stroke();
                bCtx1.fillStyle = `rgba(21, 128, 61, ${a})`;
                bCtx1.fillText("↑蒸發", ef.x-16, ef.y - 6 - ef.age*0.55);
            } else {
                bCtx1.strokeStyle = `rgba(234, 88, 12, ${a * 0.8})`;
                bCtx1.lineWidth = 1.8;
                bCtx1.beginPath(); bCtx1.ellipse(ef.x, ef.y, 4 + ef.age*0.45, 2 + ef.age*0.15, 0, 0, Math.PI*2); bCtx1.stroke();
                bCtx1.fillStyle = `rgba(194, 65, 12, ${a})`;
                bCtx1.fillText("↓凝結", ef.x-16, ef.y + 14 + ef.age*0.45);
            }
            if(ef.age >= ef.maxAge) eff1.splice(i, 1);
        }

        bCtx1.strokeStyle = "#475569"; bCtx1.lineWidth = 3.5; bCtx1.strokeRect(BL1, BT1, BR1 - BL1, BB1 - BT1);
        bCtx1.fillStyle = "#64748b"; bCtx1.fillRect(BL1 - 10, BT1 - 8, (BR1 - BL1) + 20, 8);

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
    st.markdown("自由切換**「(1) 定容，改變溫度」**與**「(2) 定溫，改變容器體積」**，觀察液-氣共存與完全汽化轉折點。")
    
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
    gCtx2.scale(2, 2); sCtx2.scale(2, 2);

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

        if(mode2==='temp') {
            document.getElementById('sliderValLabel2').textContent = st.val.toFixed(1) + " °C";
            document.getElementById('mVal1').textContent = st.val.toFixed(1) + " °C";
            document.getElementById('mVal2').textContent = Math.round(st.P) + " mmHg";
            document.getElementById('mVal3').textContent = `${st.gasCount} / 45 顆`;
            document.getElementById('mVal4').textContent = st.liqFrac>0.005 ? `${Math.round(st.liqFrac*100)}%` : `0% (完汽)`;
            
            if(Math.abs(st.val - T_CRIT2) < 0.8) document.getElementById('statusBanner2').innerHTML = "<b>★ 轉折點：液體恰好完全汽化 (80°C)</b> — 最後一滴液態水剛好蒸發完畢，之後轉為斜直線。";
            else if(st.val < T_CRIT2) document.getElementById('statusBanner2').innerHTML = "<b>線段 ①：液-氣共存</b> — 溫度愈高，飽和蒸氣壓愈大（非正比曲線上升）。";
            else document.getElementById('statusBanner2').innerHTML = "<b>線段 ②：氣體獨存</b> — 遵守理想氣體定律，壓力與絕對溫度成正比。";
        } else {
            document.getElementById('sliderValLabel2').textContent = st.val.toFixed(2) + " L";
            document.getElementById('mVal1').textContent = st.val.toFixed(2) + " L";
            document.getElementById('mVal2').textContent = Math.round(st.P) + " mmHg";
            document.getElementById('mVal3').textContent = `${st.gasCount} / 45 顆`;
            document.getElementById('mVal4').textContent = st.liqFrac>0.005 ? `${Math.round(st.liqFrac*100)}%` : `0% (完汽)`;

            if(Math.abs(st.val - V_CRIT2) < 0.12) document.getElementById('statusBanner2').innerHTML = "<b>★ 狀態 C：恰好完全汽化 (6.0 L)</b> — 液態水剛好全變成蒸氣。";
            else if(st.val < V_CRIT2) document.getElementById('statusBanner2').innerHTML = "<b>線段 ③：液-氣共存</b> — 只要有液體存在，定溫下飽和蒸氣壓恆為定值。";
            else document.getElementById('statusBanner2').innerHTML = "<b>線段 ④：氣體獨存</b> — 遵守波以耳定律，體積愈大壓力愈小。";
        }

        // 1. 繪製左側圖表
        gCtx2.clearRect(0,0,440,350);
        if(mode2==='temp') {
            const zX = 42;
            const mX = 415;
            const oy = 290;
            const h = 240;
            const maxP = 600;

            const tX = tc => zX + ((tc + 273) / (140 + 273)) * (mX - zX);
            const pY = p => oy - (p / maxP) * h;

            const ox = tX(0);

            gCtx2.strokeStyle="#334155"; gCtx2.lineWidth=2; gCtx2.beginPath();
            gCtx2.moveTo(zX - 12, oy); gCtx2.lineTo(mX + 12, oy);
            gCtx2.moveTo(ox, oy - h - 15); gCtx2.lineTo(ox, oy);
            gCtx2.stroke();

            gCtx2.fillStyle="#334155"; gCtx2.font="bold 11.5px sans-serif";
            gCtx2.fillText("壓力", ox - 38, oy - h - 5);
            gCtx2.fillText("溫度 (°C)", mX - 45, oy + 22);
            gCtx2.fillText("-273°C", zX - 18, oy + 18);
            gCtx2.fillText("0", ox - 4, oy + 18);

            const cX = tX(T_CRIT2), cY = pY(P_CRIT2);
            const endX = tX(140), endY = pY(getP_T(140));

            gCtx2.setLineDash([4, 4]);
            gCtx2.strokeStyle="#64748b";
            gCtx2.lineWidth = 1.8;
            gCtx2.beginPath();
            gCtx2.moveTo(zX, oy);
            gCtx2.lineTo(cX, cY);
            gCtx2.stroke();
            gCtx2.setLineDash([]);

            gCtx2.strokeStyle="#16a34a"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            for(let tc = 0; tc <= T_CRIT2; tc += 1) {
                let px = tX(tc), py = pY(getP_T(tc));
                if(tc === 0) gCtx2.moveTo(px, py);
                else gCtx2.lineTo(px, py);
            }
            gCtx2.stroke();

            gCtx2.strokeStyle="#0284c7"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            gCtx2.moveTo(cX, cY);
            gCtx2.lineTo(endX, endY);
            gCtx2.stroke();

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
            gCtx2.strokeStyle="#16a34a"; gCtx2.lineWidth=3.5; gCtx2.beginPath(); gCtx2.moveTo(ox, sY); gCtx2.lineTo(cX, sY); gCtx2.stroke();
            gCtx2.strokeStyle="#ea580c"; gCtx2.lineWidth=3.5; gCtx2.beginPath();
            for(let v=V_CRIT2; v<=10; v+=0.1) { let px=vX(v), py=pY(getP_V(v)); if(v===V_CRIT2)gCtx2.moveTo(px,py); else gCtx2.lineTo(px,py); }
            gCtx2.stroke();

            const curX = vX(st.val), curY = pY(st.P);
            gCtx2.fillStyle="#2563eb"; gCtx2.beginPath(); gCtx2.arc(curX, curY, 6, 0, Math.PI*2); gCtx2.fill();
            gCtx2.strokeStyle="#fff"; gCtx2.lineWidth=2; gCtx2.stroke();
        }

        // 2. 繪製右側微觀容器
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
    
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    if col_btn1.button("情境 1：0.36g 於 24.6L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 0.36, 24.6
    if col_btn2.button("情境 2：1.80g 於 24.6L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 1.80, 24.6
    if col_btn3.button("情境 3：體積壓縮至 4.92L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 0.36, 4.92
    if col_btn4.button("情境 4：體積擴張至 98.4L", use_container_width=True):
        st.session_state.w_input, st.session_state.v_input = 1.80, 98.4

    if "w_input" not in st.session_state: st.session_state.w_input = 1.80
    if "v_input" not in st.session_state: st.session_state.v_input = 8.20

    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    W = col_in1.number_input("注入水量 $W$ (g)", value=st.session_state.w_input, step=0.1)
    V = col_in2.number_input("容器體積 $V$ (L)", value=st.session_state.v_input, step=1.0)
    T_c = col_in3.number_input("溫度 $T$ (°C)", value=27.0, step=1.0)
    Pv0 = col_in4.number_input("飽和蒸氣壓 $P_v^0$ (atm)", value=0.050, step=0.01, format="%.3f")

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
        st.warning(f"**判斷結果： 理論壓力 $P ({P_theo:.4f}\text{{ atm}}) = P_v^0 ({Pv0:.3f}\text{{ atm}})$**")
        st.markdown('<div class="rule-box">表示氣體<b>恰好蒸乾無液體</b>，達完全汽化點，實際壓力 $P = P_v^0$[cite: 5]。</div>', unsafe_allow_html=True)
        st.markdown("#### 💧 殘留液態水量： **0 g**")

    else:
        st.success(f"**判斷結果： 理論壓力 $P ({P_theo:.4f}\text{{ atm}}) < P_v^0 ({Pv0:.3f}\text{{ atm}})$**")
        st.markdown(f'<div class="rule-box">表示<b>僅有氣體 (未飽和)</b>，水已完全汽化，實際壓力為計算所得之 $P = {P_theo:.4f}\text{{ atm}}$[cite: 5]。</div>', unsafe_allow_html=True)
        st.markdown("#### 💧 殘留液態水量： **0 g**")
```<ElicitationsGroup>
  <FollowUp label="是否需要協助加入更多關於其他氣體（如乙醚）的參數供測試？" query="請問是否可以新增不同液體（例如乙醚、酒精）的飽和蒸氣壓與分子量選項供計算測試？"/>
</ElicitationsGroup>
