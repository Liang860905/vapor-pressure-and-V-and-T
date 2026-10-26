import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="蒸氣壓與溫度、容器體積的關係", layout="wide")

# 移除 Streamlit 預設過多的上下留白
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.subheader("蒸氣壓與溫度、容器體積的關係互動模擬")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * { box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 8px;
        background-color: #ffffff;
        color: #1f2937;
    }
    .tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
    }
    .tab-btn {
        flex: 1;
        padding: 10px 14px;
        font-size: 14px;
        font-weight: 700;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        background: #f8fafc;
        color: #475569;
        cursor: pointer;
    }
    .tab-btn.active {
        background: #eff6ff;
        border-color: #2563eb;
        color: #1d4ed8;
    }
    .control-bar {
        background: #f8fafc;
        padding: 10px 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }
    .quick-btns {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }
    .q-btn {
        background: #e2e8f0;
        color: #334155;
        border: none;
        padding: 6px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        cursor: pointer;
    }
    .q-btn:hover { background: #cbd5e1; }
    .slider-wrap {
        flex-grow: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 240px;
    }
    input[type=range] {
        flex-grow: 1;
        height: 6px;
        cursor: pointer;
        accent-color: #2563eb;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 10px;
    }
    .metric-card {
        background: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    .metric-title { font-size: 12px; color: #64748b; margin-bottom: 2px; font-weight: 600; }
    .metric-value { font-size: 18px; font-weight: 700; }
    .status-banner {
        grid-column: span 4;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 13.5px;
        line-height: 1.45;
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
    }
    .canvas-grid {
        display: grid;
        grid-template-columns: 1.15fr 1fr;
        gap: 12px;
        width: 100%;
    }
    @media (max-width: 768px) {
        .canvas-grid { grid-template-columns: 1fr; }
        .metrics-grid { grid-template-columns: repeat(2, 1fr); }
        .status-banner { grid-column: span 2; }
    }
    .canvas-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    canvas {
        width: 100%;
        height: auto;
        max-height: 350px;
        display: block;
    }
    .box-title {
        font-size: 14px;
        font-weight: 700;
        color: #334155;
        margin-bottom: 6px;
    }
    .legend-bar {
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: #475569;
        margin-top: 6px;
        flex-wrap: wrap;
        justify-content: center;
    }
    .dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 4px; }
</style>
</head>
<body>

<div class="tabs">
    <button id="tabTemp" class="tab-btn active" onclick="switchMode('temp')">
        🔥 (1) 定容，改變溫度 (P - T 圖)
    </button>
    <button id="tabVol" class="tab-btn" onclick="switchMode('vol')">
        🧪 (2) 定溫，改變容器體積 (P - V 圖)
    </button>
</div>

<div class="control-bar">
    <div class="slider-wrap">
        <span id="sliderTitle" style="font-weight: 700; font-size: 13px;">調整溫度 (T)：</span>
        <input type="range" id="mainSlider" min="0" max="140" step="0.5" value="25">
        <span id="sliderValLabel" style="font-weight: 700; min-width: 68px; color: #2563eb;">25.0 °C</span>
    </div>
    <div id="quickBtns" class="quick-btns">
        <button class="q-btn" onclick="setSliderVal(30)">線段① 液氣共存</button>
        <button class="q-btn" onclick="setSliderVal(80)">★ 液體恰好完全汽化</button>
        <button class="q-btn" onclick="setSliderVal(120)">線段② 氣體獨存</button>
    </div>
</div>

<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-title" id="mTitle1">當前溫度 (T)</div>
        <div class="metric-value" id="mVal1" style="color: #dc2626;">25.0 °C (298 K)</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">容器內蒸氣壓力 (P)</div>
        <div class="metric-value" id="mVal2" style="color: #2563eb;">110 mmHg</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">氣相粒子數 / 總水量</div>
        <div class="metric-value" id="mVal3" style="color: #d97706;">10 / 45 顆</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">殘留液態水量</div>
        <div class="metric-value" id="mVal4" style="color: #0284c7;">78% (尚有液體)</div>
    </div>
    <div class="status-banner" id="statusBanner"></div>
</div>

<div class="canvas-grid">
    <div class="canvas-box">
        <div class="box-title" id="graphTitle">(1) 定容，改變溫度：壓力對溫度關係圖 (P - T 圖)</div>
        <canvas id="graphCanvas" width="500" height="350"></canvas>
    </div>
    <div class="canvas-box">
        <div class="box-title" id="beakerTitle">定容加熱裝置與粒子動態 (60 FPS)</div>
        <canvas id="simCanvas" width="400" height="350"></canvas>
        <div class="legend-bar">
            <span><span class="dot" style="background:#f59e0b; border:1px solid #b45309;"></span>氣相水蒸氣 H₂O(g)</span>
            <span><span class="dot" style="background:#0284c7;"></span>液態水 H₂O(l)</span>
            <span><span class="dot" style="background:#16a34a;"></span>蒸發與凝結動態交換</span>
        </div>
    </div>
</div>

<script>
let mode = 'temp';
const slider = document.getElementById('mainSlider');
const sliderTitle = document.getElementById('sliderTitle');
const sliderValLabel = document.getElementById('sliderValLabel');
const quickBtns = document.getElementById('quickBtns');

const mTitle1 = document.getElementById('mTitle1');
const mVal1 = document.getElementById('mVal1');
const mVal2 = document.getElementById('mVal2');
const mVal3 = document.getElementById('mVal3');
const mVal4 = document.getElementById('mVal4');
const statusBanner = document.getElementById('statusBanner');
const graphTitle = document.getElementById('graphTitle');
const beakerTitle = document.getElementById('beakerTitle');

const gCanvas = document.getElementById('graphCanvas');
const gCtx = gCanvas.getContext('2d');
const sCanvas = document.getElementById('simCanvas');
const sCtx = sCanvas.getContext('2d');

const TOTAL_PARTICLES = 45;
const T_CRIT = 80.0;
const P_CRIT = 450.0;

function getPsat_TempMode(T_c) {
    return 70 * Math.exp(Math.log(P_CRIT / 70) * (T_c / T_CRIT));
}
function getP_TempMode(T_c) {
    if (T_c <= T_CRIT) return getPsat_TempMode(T_c);
    return P_CRIT * ((T_c + 273) / (T_CRIT + 273));
}

const V_CRIT = 6.0;
const P_SAT_VOL = 380.0;
function getP_VolMode(V) {
    if (V <= V_CRIT) return P_SAT_VOL;
    return P_SAT_VOL * (V_CRIT / V);
}

let gasParticles = [];
let liquidParticles = [];
let effects = [];

for (let i = 0; i < 65; i++) {
    liquidParticles.push({
        rx: Math.random(),
        ry: Math.random(),
        vx: (Math.random() - 0.5) * 0.01,
        vy: (Math.random() - 0.5) * 0.01
    });
}

function switchMode(newMode) {
    mode = newMode;
    document.getElementById('tabTemp').className = mode === 'temp' ? 'tab-btn active' : 'tab-btn';
    document.getElementById('tabVol').className = mode === 'vol' ? 'tab-btn active' : 'tab-btn';
    effects = [];

    if (mode === 'temp') {
        sliderTitle.textContent = "調整溫度 (T)：";
        slider.min = 0; slider.max = 140; slider.step = 0.5; slider.value = 30;
        mTitle1.textContent = "當前溫度 (T)";
        graphTitle.textContent = "(1) 定容，改變溫度：壓力對溫度關係圖 (P - T 圖)";
        beakerTitle.textContent = "定容密閉容器與本生燈加熱模擬";
        quickBtns.innerHTML = `
            <button class="q-btn" onclick="setSliderVal(30)">線段① 液-氣共存</button>
            <button class="q-btn" onclick="setSliderVal(80)">★ 液體恰好完全汽化</button>
            <button class="q-btn" onclick="setSliderVal(120)">線段② 氣體獨存</button>
        `;
    } else {
        sliderTitle.textContent = "拉動活塞改變容器體積 (V)：";
        slider.min = 1.5; slider.max = 10.0; slider.step = 0.05; slider.value = 2.0;
        mTitle1.textContent = "容器體積 (V)";
        graphTitle.textContent = "(2) 定溫，改變容器體積：壓力對體積關係圖 (P - V 圖)";
        beakerTitle.textContent = "定溫附活塞汽缸動態模擬 (A ➔ B ➔ C ➔ D)";
        quickBtns.innerHTML = `
            <button class="q-btn" onclick="setSliderVal(2.0)">狀態 A</button>
            <button class="q-btn" onclick="setSliderVal(4.0)">狀態 B (液氣共存)</button>
            <button class="q-btn" onclick="setSliderVal(6.0)">★ 狀態 C (恰好完全汽化)</button>
            <button class="q-btn" onclick="setSliderVal(9.0)">狀態 D (氣體獨存)</button>
        `;
    }
}

function setSliderVal(val) { slider.value = val; }

function getCurrentState() {
    const val = parseFloat(slider.value);
    if (mode === 'temp') {
        const T_c = val;
        const T_k = T_c + 273;
        const P = getP_TempMode(T_c);
        const n_ratio = Math.min(1.0, (P / T_k) / (P_CRIT / (T_CRIT + 273)));
        const gasCount = Math.round(TOTAL_PARTICLES * n_ratio);
        const liqFraction = Math.max(0, 1.0 - n_ratio);
        const speedMult = Math.sqrt(T_k / 298) * 1.15;
        return { T_c, T_k, P, gasCount, liqFraction, speedMult };
    } else {
        const V = val;
        const P = getP_VolMode(V);
        const n_ratio = Math.min(1.0, V / V_CRIT);
        const gasCount = Math.round(TOTAL_PARTICLES * n_ratio);
        const liqFraction = Math.max(0, 1.0 - n_ratio);
        const speedMult = 1.0;
        return { V, P, gasCount, liqFraction, speedMult };
    }
}

function updateUI(st) {
    if (mode === 'temp') {
        sliderValLabel.textContent = `${st.T_c.toFixed(1)} °C`;
        mVal1.textContent = `${st.T_c.toFixed(1)} °C (${Math.round(st.T_k)} K)`;
        mVal2.textContent = `${Math.round(st.P)} mmHg`;
        mVal3.textContent = `${st.gasCount} / ${TOTAL_PARTICLES} 顆`;
        mVal4.textContent = st.liqFraction > 0.005 ? `${Math.round(st.liqFraction * 100)}% (尚有液體)` : `0% (完全汽化)`;

        if (Math.abs(st.T_c - T_CRIT) < 0.8) {
            statusBanner.style.borderLeftColor = "#dc2626";
            statusBanner.style.background = "#fef2f2";
            statusBanner.innerHTML = "<b>★ 轉折點：液體恰好完全汽化 (T = 80°C)</b> — 此時最後一滴液態水剛好汽化完畢[cite: 2]。若再繼續升溫，將沒有液體可提供蒸發，圖形將從曲線轉折為斜直線（理想氣體定律）[cite: 2]。";
        } else if (st.T_c < T_CRIT) {
            statusBanner.style.borderLeftColor = "#16a34a";
            statusBanner.style.background = "#f0fdf4";
            statusBanner.innerHTML = "<b>線段 ①：液-氣共存（飽和蒸氣壓曲線）</b> — 底部仍有液態水，<b>溫度愈高，飽和蒸氣壓愈大，但兩者非正比（呈曲線上升）</b>[cite: 2]。";
        } else {
            statusBanner.style.borderLeftColor = "#0284c7";
            statusBanner.style.background = "#f0f9ff";
            statusBanner.innerHTML = "<b>線段 ②：氣體獨存（遵守 PV = nRT）</b> — 液體已完全汽化，n、V 固定，<b>壓力與絕對溫度 T(K) 成正比（延伸虛線通過 -273°C 原點）</b>[cite: 2]。";
        }
    } else {
        sliderValLabel.textContent = `${st.V.toFixed(2)} L`;
        mVal1.textContent = `${st.V.toFixed(2)} L`;
        mVal2.textContent = `${Math.round(st.P)} mmHg`;
        mVal3.textContent = `${st.gasCount} / ${TOTAL_PARTICLES} 顆`;
        mVal4.textContent = st.liqFraction > 0.005 ? `${Math.round(st.liqFraction * 100)}% (尚有液體)` : `0% (完全汽化)`;

        if (Math.abs(st.V - V_CRIT) < 0.12) {
            statusBanner.style.borderLeftColor = "#dc2626";
            statusBanner.style.background = "#fef2f2";
            statusBanner.innerHTML = "<b>★ 狀態 C：液體恰好完全汽化 (V = 6.0 L)</b> — 活塞拉至此位置時，底部液態水剛好全部變成水蒸氣，壓力仍為飽和蒸氣壓[cite: 2]；若再往上拉，壓力將開始下降[cite: 2]。";
        } else if (st.V < V_CRIT) {
            statusBanner.style.borderLeftColor = "#16a34a";
            statusBanner.style.background = "#f0fdf4";
            statusBanner.innerHTML = "<b>線段 ③ (狀態 A ~ B)：液-氣共存</b> — 當容器體積逐漸變大，仍有液體存在便可液-氣共存達平衡，<b>定溫下的飽和蒸氣壓恆為定值（水平線）</b>[cite: 2]。";
        } else {
            statusBanner.style.borderLeftColor = "#0284c7";
            statusBanner.style.background = "#f0f9ff";
            statusBanner.innerHTML = "<b>線段 ④ (狀態 C ~ D)：氣體獨存（波以耳定律 PV = 定值）</b> — 液體已耗盡，n、T 固定，<b>體積愈大、壓力愈小（成反比）</b>[cite: 2]。";
        }
    }
}

function drawGraph(st) {
    gCtx.clearRect(0, 0, gCanvas.width, gCanvas.height);

    if (mode === 'temp') {
        const ox = 155, zeroK_X = 35, oy = 305, maxT_X = 465, h = 260, maxP = 600;
        function tToX(tc) {
            if (tc >= 0) return ox + (tc / 140) * (maxT_X - ox);
            return ox + (tc / 273) * (ox - zeroK_X);
        }
        function pToY(p) { return oy - (p / maxP) * h; }

        gCtx.strokeStyle = "#334155";
        gCtx.lineWidth = 2;
        gCtx.beginPath();
        gCtx.moveTo(zeroK_X - 10, oy);
        gCtx.lineTo(maxT_X + 15, oy);
        gCtx.moveTo(ox, oy - h - 15);
        gCtx.lineTo(ox, oy);
        gCtx.stroke();

        gCtx.fillStyle = "#334155";
        gCtx.font = "bold 13px sans-serif";
        gCtx.fillText("壓力 (mmHg)", ox - 85, 28);
        gCtx.fillText("溫度 (°C)", maxT_X - 50, oy + 30);
        gCtx.fillText("-273", zeroK_X - 12, oy + 20);
        gCtx.fillText("0", ox - 4, oy + 20);

        const critX = tToX(T_CRIT), critY = pToY(P_CRIT);
        gCtx.setLineDash([5, 5]);
        gCtx.strokeStyle = "#64748b";
        gCtx.lineWidth = 1.8;
        gCtx.beginPath();
        gCtx.moveTo(zeroK_X, oy);
        gCtx.lineTo(critX, critY);
        gCtx.stroke();

        gCtx.beginPath();
        for (let tc = T_CRIT; tc <= 105; tc += 2) {
            let px = tToX(tc), py = pToY(getPsat_TempMode(tc));
            if (tc === T_CRIT) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();
        gCtx.setLineDash([]);

        gCtx.strokeStyle = "#16a34a";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        for (let tc = 0; tc <= T_CRIT; tc += 1) {
            let px = tToX(tc), py = pToY(getPsat_TempMode(tc));
            if (tc === 0) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();

        gCtx.strokeStyle = "#0284c7";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        gCtx.moveTo(critX, critY);
        gCtx.lineTo(tToX(140), pToY(getP_TempMode(140)));
        gCtx.stroke();

        gCtx.fillStyle = "#dc2626";
        gCtx.beginPath(); gCtx.arc(critX, critY, 5.5, 0, Math.PI * 2); gCtx.fill();
        gCtx.fillStyle = "#1e293b";
        gCtx.font = "bold 12px sans-serif";
        gCtx.fillText("液體恰好完全汽化", critX - 105, critY - 12);

        gCtx.fillStyle = "#16a34a";
        gCtx.fillText("線段① 液-氣共存", ox + 45, oy - 70);
        gCtx.fillStyle = "#0284c7";
        gCtx.fillText("線段② 氣體獨存 (P ∝ T)", critX + 15, critY - 28);

        const curX = tToX(st.T_c), curY = pToY(st.P);
        gCtx.setLineDash([3, 3]);
        gCtx.strokeStyle = "#94a3b8";
        gCtx.lineWidth = 1.5;
        gCtx.beginPath();
        gCtx.moveTo(curX, oy); gCtx.lineTo(curX, curY);
        gCtx.moveTo(ox, curY); gCtx.lineTo(curX, curY);
        gCtx.stroke();
        gCtx.setLineDash([]);

        gCtx.fillStyle = "#dc2626";
        gCtx.beginPath(); gCtx.arc(curX, curY, 7, 0, Math.PI * 2); gCtx.fill();
        gCtx.strokeStyle = "#ffffff"; gCtx.lineWidth = 2; gCtx.stroke();
    } else {
        const ox = 70, oy = 305, w = 395, h = 255, maxV = 10.5, maxP = 500;
        function vToX(v) { return ox + (v / maxV) * w; }
        function pToY(p) { return oy - (p / maxP) * h; }

        gCtx.strokeStyle = "#334155";
        gCtx.lineWidth = 2;
        gCtx.beginPath();
        gCtx.moveTo(ox, oy - h - 15);
        gCtx.lineTo(ox, oy);
        gCtx.lineTo(ox + w + 15, oy);
        gCtx.stroke();

        gCtx.fillStyle = "#334155";
        gCtx.font = "bold 13px sans-serif";
        gCtx.fillText("壓力 (mmHg)", 10, 28);
        gCtx.fillText("容器體積 (L)", ox + w - 65, oy + 30);

        const critX = vToX(V_CRIT), satY = pToY(P_SAT_VOL);

        gCtx.strokeStyle = "#16a34a";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        gCtx.moveTo(ox, satY);
        gCtx.lineTo(critX, satY);
        gCtx.stroke();

        gCtx.strokeStyle = "#ea580c";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        for (let v = V_CRIT; v <= 10.0; v += 0.1) {
            let px = vToX(v), py = pToY(getP_VolMode(v));
            if (v === V_CRIT) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();

        gCtx.fillStyle = "#15803d";
        gCtx.font = "bold 12px sans-serif";
        gCtx.fillText("飽和蒸氣壓", ox - 65, satY + 4);
        gCtx.fillText("線段③ 液-氣共存 (P 定值)", ox + 35, satY + 24);
        gCtx.fillStyle = "#c2410c";
        gCtx.fillText("線段④ 氣體獨存 (PV = k)", critX + 20, satY + 42);

        const pts = [
            { label: 'A', v: 2.0 },
            { label: 'B', v: 4.0 },
            { label: 'C (恰好完全汽化)', v: 6.0 },
            { label: 'D', v: 9.0 }
        ];
        for (let pt of pts) {
            let px = vToX(pt.v), py = pToY(getP_VolMode(pt.v));
            gCtx.fillStyle = "#dc2626";
            gCtx.beginPath(); gCtx.arc(px, py, 4.5, 0, Math.PI * 2); gCtx.fill();
            gCtx.fillStyle = "#334155";
            gCtx.font = "bold 12px sans-serif";
            gCtx.fillText(pt.label, px - 8, py - 10);
        }

        const curX = vToX(st.V), curY = pToY(st.P);
        gCtx.setLineDash([3, 3]);
        gCtx.strokeStyle = "#94a3b8";
        gCtx.lineWidth = 1.5;
        gCtx.beginPath();
        gCtx.moveTo(curX, oy); gCtx.lineTo(curX, curY);
        gCtx.moveTo(ox, curY); gCtx.lineTo(curX, curY);
        gCtx.stroke();
        gCtx.setLineDash([]);

        gCtx.fillStyle = "#2563eb";
        gCtx.beginPath(); gCtx.arc(curX, curY, 7, 0, Math.PI * 2); gCtx.fill();
        gCtx.strokeStyle = "#ffffff"; gCtx.lineWidth = 2; gCtx.stroke();
    }
}

function drawSim(st) {
    sCtx.clearRect(0, 0, sCanvas.width, sCanvas.height);
    const B_LEFT = 85, B_RIGHT = 315;
    let B_TOP, B_BOTTOM;

    if (mode === 'temp') {
        B_TOP = 50; B_BOTTOM = 250;
    } else {
        B_BOTTOM = 310;
        const gasHeight = 40 + ((st.V - 1.5) / 8.5) * 205;
        const curLiqHeight = 26 * st.liqFraction;
        const waterY = B_BOTTOM - curLiqHeight;
        B_TOP = waterY - gasHeight;
    }

    const maxLiqH = mode === 'temp' ? 42 : 26;
    const liqH = maxLiqH * st.liqFraction;
    const waterY = B_BOTTOM - liqH;

    while (gasParticles.length < st.gasCount) {
        gasParticles.push({
            x: B_LEFT + 12 + Math.random() * (B_RIGHT - B_LEFT - 24),
            y: waterY - 8 - Math.random() * Math.max(10, (waterY - B_TOP - 20)),
            vx: (Math.random() - 0.5) * 3.2,
            vy: (Math.random() - 0.5) * 3.2
        });
    }
    while (gasParticles.length > st.gasCount) gasParticles.pop();

    if (st.liqFraction > 0.005) {
        sCtx.fillStyle = "rgba(56, 189, 248, 0.4)";
        sCtx.fillRect(B_LEFT, waterY, B_RIGHT - B_LEFT, B_BOTTOM - waterY);

        sCtx.strokeStyle = "#0284c7";
        sCtx.lineWidth = 2.5;
        sCtx.beginPath();
        sCtx.moveTo(B_LEFT, waterY);
        sCtx.lineTo(B_RIGHT, waterY);
        sCtx.stroke();

        const activeLiqCount = Math.round(60 * st.liqFraction);
        sCtx.fillStyle = "rgba(2, 132, 199, 0.55)";
        for (let i = 0; i < activeLiqCount; i++) {
            let lp = liquidParticles[i];
            lp.rx += lp.vx * st.speedMult;
            lp.ry += lp.vy * st.speedMult;
            if (lp.rx < 0.05 || lp.rx > 0.95) lp.vx *= -1;
            if (lp.ry < 0.1 || lp.ry > 0.9) lp.vy *= -1;
            let px = B_LEFT + lp.rx * (B_RIGHT - B_LEFT);
            let py = waterY + lp.ry * (B_BOTTOM - waterY);
            sCtx.beginPath(); sCtx.arc(px, py, 3.5, 0, Math.PI * 2); sCtx.fill();
        }

        if (Math.random() < 0.12 * st.speedMult) {
            let ex = B_LEFT + 20 + Math.random() * (B_RIGHT - B_LEFT - 40);
            effects.push({ x: ex, y: waterY, type: Math.random() < 0.5 ? 'evap' : 'cond', age: 0 });
        }
    }

    for (let p of gasParticles) {
        p.x += p.vx * st.speedMult;
        p.y += p.vy * st.speedMult;
        if (p.x < B_LEFT + 6) { p.x = B_LEFT + 6; p.vx = Math.abs(p.vx); }
        if (p.x > B_RIGHT - 6) { p.x = B_RIGHT - 6; p.vx = -Math.abs(p.vx); }
        if (p.y < B_TOP + 6) { p.y = B_TOP + 6; p.vy = Math.abs(p.vy); }
        if (p.y > waterY - 6) { p.y = waterY - 6; p.vy = -Math.abs(p.vy); }

        sCtx.beginPath();
        sCtx.arc(p.x, p.y, 5.5, 0, Math.PI * 2);
        sCtx.fillStyle = "#f59e0b";
        sCtx.strokeStyle = "#b45309";
        sCtx.lineWidth = 1.5;
        sCtx.fill(); sCtx.stroke();
    }

    for (let i = effects.length - 1; i >= 0; i--) {
        let ef = effects[i];
        ef.age++;
        let alpha = 1 - ef.age / 22;
        sCtx.font = "bold 11px sans-serif";
        if (ef.type === 'evap') {
            sCtx.fillStyle = `rgba(22, 163, 74, ${alpha})`;
            sCtx.fillText("↑蒸發", ef.x - 14, ef.y - ef.age * 0.8);
        } else {
            sCtx.fillStyle = `rgba(234, 88, 12, ${alpha})`;
            sCtx.fillText("↓凝結", ef.x - 14, ef.y + ef.age * 0.6 + 8);
        }
        if (ef.age >= 22) effects.splice(i, 1);
    }

    if (mode === 'temp') {
        sCtx.strokeStyle = "#475569";
        sCtx.lineWidth = 4;
        sCtx.strokeRect(B_LEFT, B_TOP, B_RIGHT - B_LEFT, B_BOTTOM - B_TOP);
        sCtx.fillStyle = "#64748b";
        sCtx.fillRect(B_LEFT - 10, B_TOP - 8, B_RIGHT - B_LEFT + 20, 8);

        sCtx.strokeStyle = "#64748b";
        sCtx.lineWidth = 3;
        sCtx.beginPath();
        sCtx.moveTo(B_LEFT - 20, B_BOTTOM + 3);
        sCtx.lineTo(B_RIGHT + 20, B_BOTTOM + 3);
        sCtx.moveTo(B_LEFT + 10, B_BOTTOM + 3);
        sCtx.lineTo(B_LEFT - 10, 338);
        sCtx.moveTo(B_RIGHT - 10, B_BOTTOM + 3);
        sCtx.lineTo(B_RIGHT + 10, 338);
        sCtx.stroke();
