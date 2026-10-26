import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="蒸氣壓與溫度、容器體積的關係", layout="wide")

st.title("蒸氣壓與溫度、容器體積的關係互動模擬")
st.markdown("自由切換 **「(1) 定容，改變溫度」** 與 **「(2) 定溫，改變容器體積」** 兩種實驗情境，拉動滑桿觀察**液-氣共存**到**液體恰好完全汽化（氣體獨存）**的轉折過程與微觀粒子動態。")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 10px;
        background-color: #ffffff;
        color: #1f2937;
    }
    .tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 14px;
    }
    .tab-btn {
        flex: 1;
        padding: 12px 16px;
        font-size: 15px;
        font-weight: 700;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        background: #f8fafc;
        color: #475569;
        cursor: pointer;
        transition: all 0.15s;
    }
    .tab-btn.active {
        background: #eff6ff;
        border-color: #2563eb;
        color: #1d4ed8;
        box-shadow: 0 2px 4px rgba(37,99,235,0.1);
    }
    .control-bar {
        background: #f8fafc;
        padding: 14px 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .quick-btns {
        display: flex;
        gap: 6px;
    }
    .q-btn {
        background: #e2e8f0;
        color: #334155;
        border: none;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
    }
    .q-btn:hover { background: #cbd5e1; }
    .slider-wrap {
        flex-grow: 1;
        display: flex;
        align-items: center;
        gap: 12px;
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
        gap: 12px;
        margin-bottom: 14px;
    }
    .metric-card {
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    .metric-title { font-size: 12px; color: #64748b; margin-bottom: 4px; font-weight: 600; }
    .metric-value { font-size: 20px; font-weight: 700; }
    .status-banner {
        grid-column: span 4;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.5;
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
    }
    .canvas-grid {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }
    .canvas-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .box-title {
        font-size: 15px;
        font-weight: 700;
        color: #334155;
        margin-bottom: 6px;
    }
    .legend-bar {
        display: flex;
        gap: 16px;
        font-size: 12px;
        color: #475569;
        margin-top: 6px;
    }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; }
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
        <span id="sliderTitle" style="font-weight: 700; font-size: 14px;">調整溫度 (T)：</span>
        <input type="range" id="mainSlider" min="0" max="140" step="0.5" value="25">
        <span id="sliderValLabel" style="font-weight: 700; min-width: 75px; color: #2563eb;">25.0 °C</span>
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
        <div class="metric-value" id="mVal4" style="color: #0284c7;">78% (尚有液態水)</div>
    </div>
    <div class="status-banner" id="statusBanner"></div>
</div>

<div class="canvas-grid">
    <div class="canvas-box" style="flex: 1.15; min-width: 440px;">
        <div class="box-title" id="graphTitle">蒸氣壓對溫度關係圖 (定容下)</div>
        <canvas id="graphCanvas" width="500" height="370"></canvas>
    </div>
    <div class="canvas-box" style="flex: 1; min-width: 380px;">
        <div class="box-title" id="beakerTitle">定容加熱裝置與粒子動態 (60 FPS)</div>
        <canvas id="simCanvas" width="400" height="370"></canvas>
        <div class="legend-bar">
            <span><span class="dot" style="background:#f59e0b; border:1px solid #b45309;"></span>氣相水蒸氣 H₂O(g)</span>
            <span><span class="dot" style="background:#0284c7;"></span>液態水 H₂O(l)</span>
            <span><span class="dot" style="background:#16a34a;"></span>蒸發與凝結動態交換</span>
        </div>
    </div>
</div>

<script>
let mode = 'temp'; // 'temp' 或 'vol'
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

const TOTAL_PARTICLES = 45; // 系統內水分子總數

// --- 模式 (1)：定容改變溫度的物理參數 ---
const T_CRIT = 80.0; // 在 80°C 時液體恰好完全汽化
const P_CRIT = 450.0; // 80°C 時的飽和蒸氣壓 (mmHg)
function getPsat_TempMode(T_c) {
    // 指數增長曲線模擬飽和蒸氣壓 (在 T = 80°C 時恰為 450 mmHg)
    return 70 * Math.exp(Math.log(P_CRIT / 70) * (T_c / T_CRIT));
}
function getP_TempMode(T_c) {
    if (T_c <= T_CRIT) {
        return getPsat_TempMode(T_c);
    } else {
        // 超過 80°C 液體完全汽化，遵守 PV = nRT，壓力與絕對溫度 (T_c + 273) 成正比
        return P_CRIT * ((T_c + 273) / (T_CRIT + 273));
    }
}

// --- 模式 (2)：定溫改變體積的物理參數 ---
const V_CRIT = 6.0; // 在 V = 6.0 L 時液體恰好完全汽化 (點 C)
const P_SAT_VOL = 380.0; // 定溫下的飽和蒸氣壓定值
function getP_VolMode(V) {
    if (V <= V_CRIT) {
        return P_SAT_VOL;
    } else {
        // 超過 6.0 L 液體完全汽化，遵守波以耳定律 PV = k
        return P_SAT_VOL * (V_CRIT / V);
    }
}

// 氣相與液相粒子陣列
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
        slider.min = 0;
        slider.max = 140;
        slider.step = 0.5;
        slider.value = 30;
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
        slider.min = 1.5;
        slider.max = 10.0;
        slider.step = 0.05;
        slider.value = 2.0;
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

function setSliderVal(val) {
    slider.value = val;
}

// 取得當前狀態參數
function getCurrentState() {
    const val = parseFloat(slider.value);
    if (mode === 'temp') {
        const T_c = val;
        const T_k = T_c + 273;
        const P = getP_TempMode(T_c);
        // 氣相粒子數與 (P / T_k) 成正比 (因定容 V 固定，n ∝ P/T)
        const n_ratio = Math.min(1.0, (P / T_k) / (P_CRIT / (T_CRIT + 273)));
        const gasCount = Math.round(TOTAL_PARTICLES * n_ratio);
        const liqFraction = Math.max(0, 1.0 - n_ratio);
        const speedMult = Math.sqrt(T_k / 298) * 1.15;
        return { T_c, T_k, P, gasCount, liqFraction, speedMult };
    } else {
        const V = val;
        const P = getP_VolMode(V);
        // 定溫下，未超過 V_CRIT 前，氣相粒子數與體積 V 成正比 (維持單位體積粒子濃度固定)
        const n_ratio = Math.min(1.0, V / V_CRIT);
        const gasCount = Math.round(TOTAL_PARTICLES * n_ratio);
        const liqFraction = Math.max(0, 1.0 - n_ratio);
        const speedMult = 1.0; // 定溫下速率固定
        return { V, P, gasCount, liqFraction, speedMult };
    }
}

// 更新上方資訊欄
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
            statusBanner.innerHTML = "<b>★ 轉折點：液體恰好完全汽化 (T = 80°C)</b> — 此時最後一滴液態水剛好看見汽化完畢。若再繼續升溫，將沒有液體可提供蒸發，圖形將從指數曲線轉折為斜直線（理想氣體定律）。";
        } else if (st.T_c < T_CRIT) {
            statusBanner.style.borderLeftColor = "#16a34a";
            statusBanner.style.background = "#f0fdf4";
            statusBanner.innerHTML = "<b>線段 ①：液-氣共存（飽和蒸氣壓曲線）</b> — 底部仍有液態水，<b>溫度愈高，蒸發速率愈快，飽和蒸氣壓愈大，但壓力與溫度並非正比（呈曲線上升）</b>。";
        } else {
            statusBanner.style.borderLeftColor = "#0284c7";
            statusBanner.style.background = "#f0f9ff";
            statusBanner.innerHTML = "<b>線段 ②：氣體獨存（未飽和蒸氣，遵守 PV = nRT）</b> — 液體已完全汽化，氣相粒子數 (n) 與容器體積 (V) 皆固定，<b>壓力與絕對溫度 T(K) 成正比（延伸虛線通過 -273°C 原點）</b>。";
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
            statusBanner.innerHTML = "<b>★ 狀態 C：液體恰好完全汽化 (V = 6.0 L)</b> — 活塞拉至此位置時，底部液態水剛好全部變成水蒸氣，壓力仍維持飽和蒸氣壓；若再往上拉，壓力將開始下降。";
        } else if (st.V < V_CRIT) {
            statusBanner.style.borderLeftColor = "#16a34a";
            statusBanner.style.background = "#f0fdf4";
            statusBanner.innerHTML = "<b>線段 ③ (狀態 A ~ B)：液-氣共存</b> — 當容器體積逐漸變大，液態水會繼續蒸發以填補空間（氣相粒子數變多，但單位體積濃度不變），<b>只要仍有液體存在，定溫下的飽和蒸氣壓恆為定值（水平線）</b>。";
        } else {
            statusBanner.style.borderLeftColor = "#0284c7";
            statusBanner.style.background = "#f0f9ff";
            statusBanner.innerHTML = "<b>線段 ④ (狀態 C ~ D)：氣體獨存（遵守波以耳定律 PV = 定值）</b> — 液態水已耗盡，氣相粒子總數 (n) 固定，<b>體積愈大，粒子碰撞器壁頻率下降，壓力與體積成反比</b>。";
        }
    }
}

// 繪製左側教科書圖表
function drawGraph(st) {
    gCtx.clearRect(0, 0, gCanvas.width, gCanvas.height);

    if (mode === 'temp') {
        // P - T 圖 (包含左側 -273°C 虛線延伸區，完全還原講義圖形)
        const ox = 155; // 0°C 縱軸位置
        const zeroK_X = 35; // -273°C 位置
        const oy = 320;
        const maxT_X = 465; // 140°C 位置
        const h = 275;
        const maxP = 600;

        function tToX(tc) {
            if (tc >= 0) return ox + (tc / 140) * (maxT_X - ox);
            return ox + (tc / 273) * (ox - zeroK_X);
        }
        function pToY(p) {
            return oy - (p / maxP) * h;
        }

        // 繪製座標軸
        gCtx.strokeStyle = "#334155";
        gCtx.lineWidth = 2;
        gCtx.beginPath();
        // 橫軸 (從 -273°C 畫到 140°C)
        gCtx.moveTo(zeroK_X - 10, oy);
        gCtx.lineTo(maxT_X + 15, oy);
        // 0°C 縱軸
        gCtx.moveTo(ox, oy - h - 15);
        gCtx.lineTo(ox, oy);
        gCtx.stroke();

        // 座標軸文字
        gCtx.fillStyle = "#334155";
        gCtx.font = "bold 13px sans-serif";
        gCtx.fillText("壓力 (mmHg)", ox - 85, 32);
        gCtx.fillText("溫度 (°C)", maxT_X - 50, oy + 32);
        gCtx.fillText("-273", zeroK_X - 12, oy + 20);
        gCtx.fillText("0", ox - 4, oy + 20);

        // 1. 繪製從 -273°C 到轉折點的查理定律延伸虛線
        const critX = tToX(T_CRIT);
        const critY = pToY(P_CRIT);
        gCtx.setLineDash([5, 5]);
        gCtx.strokeStyle = "#64748b";
        gCtx.lineWidth = 1.8;
        gCtx.beginPath();
        gCtx.moveTo(zeroK_X, oy);
        gCtx.lineTo(critX, critY);
        gCtx.stroke();

        // 2. 繪製超過轉折點後若液體無限的「飽和蒸氣壓延伸虛線」
        gCtx.beginPath();
        for (let tc = T_CRIT; tc <= 105; tc += 2) {
            let px = tToX(tc);
            let py = pToY(getPsat_TempMode(tc));
            if (tc === T_CRIT) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();
        gCtx.setLineDash([]);

        // 3. 繪製線段 ①：液-氣共存 (綠色曲線)
        gCtx.strokeStyle = "#16a34a";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        for (let tc = 0; tc <= T_CRIT; tc += 1) {
            let px = tToX(tc);
            let py = pToY(getPsat_TempMode(tc));
            if (tc === 0) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();

        // 4. 繪製線段 ②：氣體獨存 (藍色斜直線)
        gCtx.strokeStyle = "#0284c7";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        gCtx.moveTo(critX, critY);
        gCtx.lineTo(tToX(140), pToY(getP_TempMode(140)));
        gCtx.stroke();

        // 轉折紅點與標籤
        gCtx.fillStyle = "#dc2626";
        gCtx.beginPath(); gCtx.arc(critX, critY, 5.5, 0, Math.PI * 2); gCtx.fill();
        gCtx.fillStyle = "#1e293b";
        gCtx.font = "bold 12px sans-serif";
        gCtx.fillText("液體恰好完全汽化", critX - 105, critY - 12);

        gCtx.fillStyle = "#16a34a";
        gCtx.fillText("線段① 液-氣共存", ox + 45, oy - 75);
        gCtx.fillStyle = "#0284c7";
        gCtx.fillText("線段② 氣體獨存 (P ∝ T)", critX + 15, critY - 30);

        // 5. 繪製當前滑桿所在位置點
        const curX = tToX(st.T_c);
        const curY = pToY(st.P);
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
        gCtx.strokeStyle = "#ffffff";
        gCtx.lineWidth = 2;
        gCtx.stroke();

    } else {
        // P - V 圖 (完全還原講義 A -> B -> C -> D 圖形)
        const ox = 70, oy = 320, w = 395, h = 270;
        const maxV = 10.5, maxP = 500;

        function vToX(v) { return ox + (v / maxV) * w; }
        function pToY(p) { return oy - (p / maxP) * h; }

        // 座標軸
        gCtx.strokeStyle = "#334155";
        gCtx.lineWidth = 2;
        gCtx.beginPath();
        gCtx.moveTo(ox, oy - h - 15);
        gCtx.lineTo(ox, oy);
        gCtx.lineTo(ox + w + 15, oy);
        gCtx.stroke();

        gCtx.fillStyle = "#334155";
        gCtx.font = "bold 13px sans-serif";
        gCtx.fillText("壓力 (mmHg)", 10, 30);
        gCtx.fillText("容器體積 (L)", ox + w - 65, oy + 32);

        const critX = vToX(V_CRIT);
        const satY = pToY(P_SAT_VOL);

        // 1. 線段 ③：液-氣共存 (綠色水平線)
        gCtx.strokeStyle = "#16a34a";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        gCtx.moveTo(ox, satY);
        gCtx.lineTo(critX, satY);
        gCtx.stroke();

        // 2. 線段 ④：氣體獨存 (紅色波以耳雙曲線)
        gCtx.strokeStyle = "#ea580c";
        gCtx.lineWidth = 4;
        gCtx.beginPath();
        for (let v = V_CRIT; v <= 10.0; v += 0.1) {
            let px = vToX(v);
            let py = pToY(getP_VolMode(v));
            if (v === V_CRIT) gCtx.moveTo(px, py);
            else gCtx.lineTo(px, py);
        }
        gCtx.stroke();

        // 標示飽和蒸氣壓文字與 A, B, C, D 四點
        gCtx.fillStyle = "#15803d";
        gCtx.font = "bold 12px sans-serif";
        gCtx.fillText("飽和蒸氣壓", ox - 65, satY + 4);
        gCtx.fillText("線段③ 液-氣共存 (P 定值)", ox + 35, satY + 25);

        gCtx.fillStyle = "#c2410c";
        gCtx.fillText("線段④ 氣體獨存 (PV = k)", critX + 20, satY + 45);

        const pts = [
            { label: 'A', v: 2.0 },
            { label: 'B', v: 4.0 },
            { label: 'C (恰好完全汽化)', v: 6.0 },
            { label: 'D', v: 9.0 }
        ];
        for (let pt of pts) {
            let px = vToX(pt.v);
            let py = pToY(getP_VolMode(pt.v));
            gCtx.fillStyle = "#dc2626";
            gCtx.beginPath(); gCtx.arc(px, py, 4.5, 0, Math.PI * 2); gCtx.fill();
            gCtx.fillStyle = "#334155";
            gCtx.font = "bold 12px sans-serif";
            gCtx.fillText(pt.label, px - 8, py - 10);
        }

        // 當前滑桿位置點
        const curX = vToX(st.V);
        const curY = pToY(st.P);
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
        gCtx.strokeStyle = "#ffffff";
        gCtx.lineWidth = 2;
        gCtx.stroke();
    }
}

// 繪製右側微觀容器與粒子運動
function drawSim(st) {
    sCtx.clearRect(0, 0, sCanvas.width, sCanvas.height);

    // 決定容器邊界座標
    const B_LEFT = 85, B_RIGHT = 315;
    let B_TOP, B_BOTTOM;

    if (mode === 'temp') {
        B_TOP = 55;
        B_BOTTOM = 265;
    } else {
        B_BOTTOM = 325;
        // 活塞高度隨體積 V (1.5 ~ 10.0) 變化
        const gasHeight = 42 + ((st.V - 1.5) / 8.5) * 215;
        const maxLiqHeight = 28;
        const curLiqHeight = maxLiqHeight * st.liqFraction;
        const waterY = B_BOTTOM - curLiqHeight;
        B_TOP = waterY - gasHeight;
    }

    const maxLiqH = mode === 'temp' ? 45 : 28;
    const liqH = maxLiqH * st.liqFraction;
    const waterY = B_BOTTOM - liqH;

    // 1. 動態調整氣相粒子數目
    while (gasParticles.length < st.gasCount) {
        gasParticles.push({
            x: B_LEFT + 12 + Math.random() * (B_RIGHT - B_LEFT - 24),
            y: waterY - 8 - Math.random() * Math.max(10, (waterY - B_TOP - 20)),
            vx: (Math.random() - 0.5) * 3.2,
            vy: (Math.random() - 0.5) * 3.2
        });
    }
    while (gasParticles.length > st.gasCount) {
        gasParticles.pop();
    }

    // 2. 繪製底部液態水與水中粒子 (僅在尚有液態水時繪製)
    if (st.liqFraction > 0.005) {
        sCtx.fillStyle = "rgba(56, 189, 248, 0.4)";
        sCtx.fillRect(B_LEFT, waterY, B_RIGHT - B_LEFT, B_BOTTOM - waterY);

        sCtx.strokeStyle = "#0284c7";
        sCtx.lineWidth = 2.5;
        sCtx.beginPath();
        sCtx.moveTo(B_LEFT, waterY);
        sCtx.lineTo(B_RIGHT, waterY);
        sCtx.stroke();

        // 水中粒子熱運動
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
            sCtx.beginPath();
            sCtx.arc(px, py, 3.5, 0, Math.PI * 2);
            sCtx.fill();
        }

        // 當液-氣共存時，持續產生「蒸發↑」與「凝結↓」的動態平衡漣漪
        if (Math.random() < 0.12 * st.speedMult) {
            let ex = B_LEFT + 20 + Math.random() * (B_RIGHT - B_LEFT - 40);
            effects.push({ x: ex, y: waterY, type: Math.random() < 0.5 ? 'evap' : 'cond', age: 0 });
        }
    }

    // 3. 更新並繪製氣相水蒸氣粒子
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
        sCtx.fill();
        sCtx.stroke();
    }

    // 4. 繪製液面上的蒸發/凝結動態特效
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

    // 5. 繪製容器外框與實驗配件
    if (mode === 'temp') {
        // 定容密閉容器與頂蓋
        sCtx.strokeStyle = "#475569";
        sCtx.lineWidth = 4;
        sCtx.strokeRect(B_LEFT, B_TOP, B_RIGHT - B_LEFT, B_BOTTOM - B_TOP);
        sCtx.fillStyle = "#64748b";
        sCtx.fillRect(B_LEFT - 10, B_TOP - 8, B_RIGHT - B_LEFT + 20, 8);

        // 繪製鐵架台與本生燈火焰 (火焰大小隨溫度變化)
        sCtx.strokeStyle = "#64748b";
        sCtx.lineWidth = 3;
        sCtx.beginPath();
        sCtx.moveTo(B_LEFT - 20, B_BOTTOM + 3);
        sCtx.lineTo(B_RIGHT + 20, B_BOTTOM + 3);
        sCtx.moveTo(B_LEFT + 10, B_BOTTOM + 3);
        sCtx.lineTo(B_LEFT - 10, 355);
        sCtx.moveTo(B_RIGHT - 10, B_BOTTOM + 3);
        sCtx.lineTo(B_RIGHT + 10, 355);
        sCtx.stroke();

        // 本生燈底座與燈管
        sCtx.fillStyle = "#475569";
        sCtx.fillRect(188, 315, 24, 35);
        sCtx.fillRect(165, 348, 70, 8);

        // 動態火焰
        const flameH = 12 + (st.T_c / 140) * 35 + Math.sin(Date.now() * 0.02) * 3;
        sCtx.fillStyle = "rgba(239, 68, 68, 0.85)";
        sCtx.beginPath();
        sCtx.moveTo(182, 315);
        sCtx.quadraticCurveTo(200, 315 - flameH * 1.4, 218, 315);
        sCtx.fill();

        sCtx.fillStyle = "rgba(250, 204, 21, 0.9)";
        sCtx.beginPath();
        sCtx.moveTo(190, 315);
        sCtx.quadraticCurveTo(200, 315 - flameH * 0.8, 210, 315);
        sCtx.fill();
    } else {
        // 附可動活塞的汽缸
        const CYL_TOP = 35;
        sCtx.strokeStyle = "#475569";
        sCtx.lineWidth = 4;
        sCtx.beginPath();
        sCtx.moveTo(B_LEFT, CYL_TOP);
        sCtx.lineTo(B_LEFT, B_BOTTOM);
        sCtx.lineTo(B_RIGHT, B_BOTTOM);
        sCtx.lineTo(B_RIGHT, CYL_TOP);
        sCtx.stroke();

        // 可動活塞與拉桿
        sCtx.fillStyle = "#94a3b8";
        sCtx.strokeStyle = "#334155";
        sCtx.lineWidth = 2;
        sCtx.fillRect(B_LEFT + 2, B_TOP - 14, B_RIGHT - B_LEFT - 4, 14);
        sCtx.strokeRect(B_LEFT + 2, B_TOP - 14, B_RIGHT - B_LEFT - 4, 14);

        // 活塞推桿
        sCtx.fillStyle = "#64748b";
        sCtx.fillRect(194, 10, 12, B_TOP - 24);
        sCtx.fillRect(170, 8, 60, 6);
    }
}

function animate() {
    const st = getCurrentState();
    updateUI(st);
    drawGraph(st);
    drawSim(st);
    requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
"""

components.html(html_code, height=640, scrolling=False)
