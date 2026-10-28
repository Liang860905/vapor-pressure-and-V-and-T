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
tab1, tab2 = st.tabs(["📊 專案一：蒸發與凝結速率動態平衡 (r - t / P - t 圖)", "🔥 專案二：蒸氣壓與溫度、容器體積關係 (P-T / P-V 圖)"])

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
        <div class="metric-card"><div class="metric-title">蒸氣壓狀態</div><div class="metric-value" id="pressureVal1" style="color:#2563eb;">0% 飽和</div></div>
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
                <span><span class="dot" style="background:#ea580c; border:1px solid #9a3412;"></span>凝結入水分子 (↓
