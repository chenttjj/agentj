from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from studio_shell.page_shell import page_shell
from studio_shell.shell_ui import inject_style

st.set_page_config(page_title="Layout Practice", page_icon="📐", layout="wide")
inject_style()

TRACK_NAMES = [
    "Drums",
    "Bass",
    "Synth",
    "Lead",
    "Pad",
    "Vocal",
    "FX",
    "Perc",
]

DEFAULT_LEVELS = [82, 68, 74, 71, 63, 59, 48, 66]

CLIP_ROWS = {
    "Drums": ["Kick", "Snare", "Hat", "Hat", "Kick", "Snare", "Hat", "Fill"],
    "Bass": ["C2", "-", "C2", "-", "G1", "-", "A1", "-"],
    "Synth": ["Pad", "Pad", "-", "Chord", "-", "Lead", "Lead", "-"],
    "Lead": ["-", "Hook", "-", "Hook", "Run", "-", "Run", "-"],
    "Pad": ["Warm", "Warm", "Warm", "-", "Air", "Air", "-", "-"],
    "Vocal": ["-", "Verse", "Verse", "-", "Hook", "Hook", "-", "Adlib"],
    "FX": ["Rise", "-", "Down", "-", "Hit", "-", "Noise", "-"],
    "Perc": ["Shaker", "-", "Clap", "-", "Tom", "-", "Clap", "-"],
}

INSTRUMENT_ROLLS = {
    "鋼琴": {
        "labels": ["C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"],
        "grid": [
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 0],
        ],
    },
    "吉他": {
        "labels": ["E5", "B4", "G4", "D4", "A3", "E3", "Mute", "Palm"],
        "grid": [
            [0, 1, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
        ],
    },
    "貝斯": {
        "labels": ["C3", "A2", "G2", "F2", "E2", "D2", "C2", "A1"],
        "grid": [
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0],
        ],
    },
    "鼓組": {
        "labels": ["Crash", "Open Hat", "Closed Hat", "Clap", "Snare", "Kick 2", "Kick 1", "Sub Kick"],
        "grid": [
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
        ],
    },
    "弦樂": {
        "labels": ["Violin 1", "Violin 2", "Viola", "Cello Hi", "Cello Lo", "Bass Hi", "Bass Lo", "Drone"],
        "grid": [
            [0, 0, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 1],
            [0, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0],
        ],
    },
}


def render_main() -> str:
    st.markdown(
        """
        <style>
        .daw-panel {
            background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 0 0 1px rgba(34, 211, 238, 0.08), 0 12px 30px rgba(2, 6, 23, 0.45);
            margin-bottom: 14px;
        }
        .daw-title {
            color: #e2e8f0;
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: 8px;
        }
        .daw-subtitle {
            color: #94a3b8;
            font-size: 0.92rem;
            margin-bottom: 10px;
        }
        .ruler-wrap {
            display: grid;
            grid-template-columns: 110px repeat(8, 1fr);
            gap: 6px;
            margin: 8px 0 14px 0;
        }
        .ruler-cell {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: #67e8f9;
            border: 1px solid rgba(34, 211, 238, 0.22);
            border-radius: 10px;
            text-align: center;
            padding: 8px 0;
            font-size: 0.84rem;
            letter-spacing: 0.04em;
        }
        .ruler-label {
            background: #0b1220;
            color: #94a3b8;
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 10px;
            text-align: center;
            padding: 8px 0;
            font-size: 0.84rem;
        }
        .piano-grid {
            display: grid;
            grid-template-columns: 90px repeat(8, 1fr);
            gap: 6px;
            margin-top: 8px;
        }
        .note-label {
            background: #111827;
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 8px;
            padding: 7px 8px;
            font-size: 0.82rem;
            text-align: center;
        }
        .note-off {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(51, 65, 85, 0.9);
            border-radius: 8px;
            min-height: 34px;
        }
        .note-on {
            background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
            border: 1px solid rgba(125, 211, 252, 0.9);
            border-radius: 8px;
            min-height: 34px;
            box-shadow: 0 0 18px rgba(14, 165, 233, 0.28);
        }
        .tech-chip {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(6, 182, 212, 0.12);
            color: #67e8f9;
            border: 1px solid rgba(34, 211, 238, 0.3);
            font-size: 0.8rem;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🎚️ Layout Practice：深色科技風 DAW 介面")
    st.info("已加入時間軸尺規、可切換樂器的軌域編輯區、8 軌 Mixer，並用深色科技風呈現。")

    left_col, right_col = st.columns([1.65, 1], gap="large")

    with left_col:
        st.markdown('<div class="daw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="daw-title">🎛️ DAW Mixer / Sequencer</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="daw-subtitle">Transport、時間軸尺規、Clip 區與可切換樂器 Roll 的整合示範</div>',
            unsafe_allow_html=True,
        )

        transport1, transport2, transport3, transport4, transport5, transport6 = st.columns(6)
        transport1.button("⏮️", use_container_width=True)
        transport2.button("▶️", use_container_width=True)
        transport3.button("⏸️", use_container_width=True)
        transport4.button("⏹️", use_container_width=True)
        transport5.button("⏺️", use_container_width=True)
        transport6.button("🔁", use_container_width=True)

        info1, info2, info3, info4 = st.columns(4)
        bpm = info1.number_input("BPM", min_value=60, max_value=200, value=128, step=1)
        info2.selectbox("Key", ["C", "Dm", "Em", "F", "G", "Am", "Bm"], index=0)
        info3.selectbox("Swing", ["0%", "10%", "20%", "30%", "40%"], index=1)
        info4.selectbox("Quantize", ["1/4", "1/8", "1/16", "1/32"], index=2)

        st.markdown("##### ⏱️ 時間軸尺規")
        ruler_html = ['<div class="ruler-wrap">', '<div class="ruler-label">Bar</div>']
        for i in range(1, 9):
            ruler_html.append(f'<div class="ruler-cell">{i}</div>')
        ruler_html.append('</div>')
        st.markdown("".join(ruler_html), unsafe_allow_html=True)

        st.markdown("##### 🎚️ 8-Track Mixer")
        mixer_cols = st.columns(8)
        for idx, col in enumerate(mixer_cols):
            with col:
                st.caption(TRACK_NAMES[idx])
                st.toggle("M", key=f"mute_{idx}")
                st.toggle("S", key=f"solo_{idx}")
                pan = st.slider(
                    "Pan",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    key=f"pan_{idx}",
                    label_visibility="collapsed",
                )
                volume = st.slider(
                    "Volume",
                    min_value=0,
                    max_value=100,
                    value=DEFAULT_LEVELS[idx],
                    key=f"vol_{idx}",
                    label_visibility="collapsed",
                )
                st.progress(volume / 100)
                st.caption(f"Pan {pan:+d}")

        st.markdown("##### 🧱 Pattern / Clip 區")
        header = st.columns([1.2] + [1] * 8)
        header[0].markdown("**Track**")
        for i in range(8):
            header[i + 1].markdown(f"**Bar {i + 1}**")

        for track, clips in CLIP_ROWS.items():
            row_cols = st.columns([1.2] + [1] * 8)
            row_cols[0].markdown(f"**{track}**")
            for i, clip in enumerate(clips):
                label = "·" if clip == "-" else f"▣ {clip}"
                row_cols[i + 1].button(label, key=f"clip_{track}_{i}", use_container_width=True)

        instrument = st.selectbox(
            "選擇軌域樂器",
            list(INSTRUMENT_ROLLS.keys()),
            index=0,
            key="instrument_roll_select",
        )
        roll_data = INSTRUMENT_ROLLS[instrument]

        st.markdown(f"##### 🎼 {instrument} Roll")
        piano_html = ['<div class="piano-grid">']
        piano_html.append('<div class="note-label">Lane</div>')
        for i in range(1, 9):
            piano_html.append(f'<div class="ruler-cell">{i}</div>')

        for label, row in zip(roll_data["labels"], roll_data["grid"]):
            piano_html.append(f'<div class="note-label">{label}</div>')
            for cell in row:
                piano_html.append('<div class="note-on"></div>' if cell else '<div class="note-off"></div>')

        piano_html.append('</div>')
        st.markdown("".join(piano_html), unsafe_allow_html=True)

        st.markdown(
            f"<span class='tech-chip'>BPM {bpm}</span>"
            "<span class='tech-chip'>Dark Tech Theme</span>"
            "<span class='tech-chip'>8 Tracks</span>"
            f"<span class='tech-chip'>{instrument} Roll</span>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="daw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="daw-title">🧪 專案控制區</div>', unsafe_allow_html=True)
        st.text_input("專案名稱", key="project_name", placeholder="例如：Midnight Circuit")
        st.selectbox("風格", ["Lo-fi", "House", "Synthwave", "Hip-hop", "Ambient", "Techno"], index=2)
        st.selectbox("主題模式", ["Dark Neon", "Cyber Blue", "Midnight Purple"], index=0)
        st.slider("母帶亮度", 0, 100, 55)
        st.slider("空間感", 0, 100, 62)
        st.slider("Stereo Width", 0, 200, 118)
        st.metric("CPU Load", "37%", "+4%")
        st.metric("Tracks", "8", "+4")
        st.metric("Scene", "A-01", "+1")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="daw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="daw-title">📝 建議怎麼問 Agent</div>', unsafe_allow_html=True)
        st.markdown(
            """
- 幫我把這個 DAW 介面再加上時間軸尺規。
- 幫我新增一個可切換 Piano / Guitar / Bass / Drums / Strings 的樂器軌域。
- 幫我把 Mixer 改成 8 軌。
- 幫我做成深色科技風。
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### 2. 分頁標籤練習 (Tabs)")
    tab1, tab2, tab3 = st.tabs(["📊 專案總覽", "📝 備註區", "⚙️ 設定區"])

    with tab1:
        st.write("這裡可以放專案摘要、音軌資訊、素材統計或圖表。")
        st.bar_chart([8, 6, 7, 5, 9, 4])

    with tab2:
        st.write("這裡可以放編曲想法、歌詞草稿、混音備忘錄。")
        st.text_area("輸入一些製作筆記...", height=120)

    with tab3:
        st.write("這裡可以放更細的設定，例如 buffer size、輸出裝置、主題等。")
        st.slider("調整參數", 0, 100, 50)

    st.divider()
    st.markdown("### 💡 練習任務")
    st.markdown(
        """
- [x] 加入時間軸尺規。
- [x] 新增可切換樂器的軌域編輯區。
- [x] Mixer 擴充為 8 軌。
- [x] 套用深色科技風介面。
        """
    )

    return ""


page_shell(
    "Layout Practice",
    "練習使用 Columns 與 Tabs 來建立複雜的 UI 佈局。",
    render_main,
    page_name="Layout Practice",
)
