from __future__ import annotations

import random
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SHELL_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from studio_shell.page_shell import page_shell
from studio_shell.shell_ui import (
    format_extra_context,
    inject_style,
)

PAGE_NAME = "Mood Beat"
DATA_PATH = SHELL_ROOT / "data" / "mood beat.json"

st.set_page_config(page_title="Mood Beat", page_icon="🫧", layout="wide")
inject_style()

MOOD_OPTIONS = ["平靜", "有點累", "焦慮", "低落", "開心", "充滿能量", "煩躁", "想專心"]
BEAT_OPTIONS = ["Lo-fi", "Ambient", "Focus", "R&B", "Soft Hip-hop", "Future Chill"]
SOUND_OPTIONS = ["雨聲", "海浪", "咖啡廳", "夜晚蟲鳴", "風聲", "營火白噪音"]
BREATH_PATTERNS = {
    "快速安定": {"inhale": 4, "hold": 2, "exhale": 6, "rounds": 4},
    "放鬆入門": {"inhale": 4, "hold": 4, "exhale": 4, "rounds": 4},
    "深層舒壓": {"inhale": 4, "hold": 7, "exhale": 8, "rounds": 3},
}
COMFORT_LINES = {
    "平靜": "你不需要逼自己更有感覺，平靜本身就很珍貴。",
    "有點累": "今天先不用衝，慢慢把自己接住就很好。",
    "焦慮": "先不用急著解決全部，先把呼吸找回來就可以了。",
    "低落": "你不是沒用，只是今天真的比較重一點。",
    "開心": "這份好狀態值得被好好留住，讓節奏陪你延長它。",
    "充滿能量": "把這股能量用在你想珍惜的事上，會很漂亮。",
    "煩躁": "先讓身體鬆一點，再決定要不要和世界交手。",
    "想專心": "你不需要完美專注，只要比剛剛更穩一點就好。",
}
RITUAL_SUGGESTIONS = {
    "平靜": "把手放在胸口上，慢慢吐一口氣，記住這個穩定感。",
    "有點累": "喝一口水，讓眼睛離開螢幕 10 秒鐘。",
    "焦慮": "把肩膀放下來，再做一次更長的吐氣。",
    "低落": "寫一句今天想對自己溫柔一點的話。",
    "開心": "把這份好心情記下來，留給晚點的自己看。",
    "充滿能量": "趁現在做一件最小但最重要的事。",
    "煩躁": "捏捏手指，確認一下你此刻站得很穩。",
    "想專心": "把下一步縮小成 5 分鐘內能完成的小任務。",
}
AURA_STYLE_OPTIONS = ["柔光", "霓虹", "雲霧", "星塵", "極光", "水波"]
AURA_COLOR_PRESETS = {
    "天空藍": "#38bdf8",
    "薄荷綠": "#34d399",
    "薰衣草紫": "#a78bfa",
    "蜜桃粉": "#fb7185",
    "暖陽金": "#f59e0b",
    "月光銀": "#cbd5e1",
}
AURA_RANDOM = "隨機"


def mood_profile(mood: str, energy: int, stress: int) -> dict[str, str | int]:
    if stress >= 75:
        return {
            "label": "需要先安定一下",
            "color": "#f59e0b",
            "beat_style": "soft ambient lofi",
            "tempo": 68,
            "focus": "先降低壓力、讓呼吸慢下來",
        }
    if energy <= 30:
        return {
            "label": "低能量修復模式",
            "color": "#60a5fa",
            "beat_style": "warm lofi chill",
            "tempo": 72,
            "focus": "補充安全感與穩定節奏",
        }
    if mood == "開心" or energy >= 80:
        return {
            "label": "高能量推進模式",
            "color": "#34d399",
            "beat_style": "uplifting future beats",
            "tempo": 108,
            "focus": "放大好心情與行動力",
        }
    if mood in {"焦慮", "煩躁"}:
        return {
            "label": "降噪舒緩模式",
            "color": "#c084fc",
            "beat_style": "calm lofi with soft pads",
            "tempo": 76,
            "focus": "減少緊張感與內在噪音",
        }
    if mood == "想專心":
        return {
            "label": "專注陪伴模式",
            "color": "#22d3ee",
            "beat_style": "minimal focus beat",
            "tempo": 88,
            "focus": "穩定節拍、減少分心",
        }
    return {
        "label": "平衡日常模式",
        "color": "#f472b6",
        "beat_style": "gentle chill beat",
        "tempo": 84,
        "focus": "維持穩定心情與舒服節奏",
    }


def beat_title(mood: str, beat_mode: str, soundscape: str, stress: int) -> str:
    prefix_map = {
        "平靜": "Quiet",
        "有點累": "Soft",
        "焦慮": "Slow",
        "低落": "Gentle",
        "開心": "Sunny",
        "充滿能量": "Pulse",
        "煩躁": "Mute",
        "想專心": "Focus",
    }
    suffix_map = {
        "雨聲": "Rain Reset",
        "海浪": "Ocean Drift",
        "咖啡廳": "Cafe Loop",
        "夜晚蟲鳴": "Night Air",
        "風聲": "Wind Bloom",
        "營火白噪音": "Ember Glow",
    }
    mode_word = beat_mode.replace("&", "and").replace(" ", "")
    intensity = "Lite" if stress < 55 else "Relief"
    return f"{prefix_map.get(mood, 'Mood')} {mode_word} {suffix_map.get(soundscape, 'Dream')} {intensity}"


def resolve_aura_choice(choice: str, options: list[str], fallback: str) -> str:
    if choice == AURA_RANDOM:
        return random.choice(options)
    if choice in options:
        return choice
    return fallback


def aura_status(
    mood: str,
    energy: int,
    stress: int,
    focus_need: int,
    delta: int,
    good_style_choice: str,
    good_color_choice: str,
    low_style_choice: str,
    low_color_choice: str,
) -> dict[str, str | int | float]:
    calm_score = max(0, min(100, 100 - stress + delta * 3))
    glow_strength = max(35, min(92, int((energy * 0.45) + (focus_need * 0.2) + (calm_score * 0.35))))
    ring_softness = max(20, min(90, int((focus_need * 0.55) + (max(delta, 0) * 6) + 20)))

    if delta >= 10:
        breath_state = "呼吸後正在慢慢穩下來"
    elif delta > 0:
        breath_state = "呼吸後有一點放鬆空間"
    elif delta == 0:
        breath_state = "目前維持原本的節奏"
    else:
        breath_state = "身體還在整理剛剛的感受"

    if stress >= 70:
        aura_tone = "外圈偏緊，提醒你先降噪一下"
    elif energy >= 75:
        aura_tone = "亮度偏高，適合把能量慢慢導出去"
    elif energy <= 35:
        aura_tone = "亮度偏柔，現在比較適合修復模式"
    elif focus_need >= 70:
        aura_tone = "光感很柔，像是在提醒你可以被接住"
    else:
        aura_tone = "整體穩穩的，像是在保留你的日常節奏"

    is_good_state = calm_score >= 60 and stress < 70 and energy >= 45
    selected_style = resolve_aura_choice(
        good_style_choice if is_good_state else low_style_choice,
        AURA_STYLE_OPTIONS,
        "柔光" if is_good_state else "雲霧",
    )
    selected_color_name = resolve_aura_choice(
        good_color_choice if is_good_state else low_color_choice,
        list(AURA_COLOR_PRESETS.keys()),
        "薄荷綠" if is_good_state else "月光銀",
    )
    orb_color = AURA_COLOR_PRESETS[selected_color_name]

    title = "今日狀態光球"
    subtitle = f"{breath_state}｜{aura_tone}｜{selected_style}・{selected_color_name}"
    return {
        "title": title,
        "subtitle": subtitle,
        "glow_strength": glow_strength,
        "ring_softness": ring_softness,
        "calm_score": calm_score,
        "style": selected_style,
        "color_name": selected_color_name,
        "orb_color": orb_color,
        "state_label": "狀態較好" if is_good_state else "狀態較需要被照顧",
    }


def render_main() -> str:
    state = {}
    if DATA_PATH.exists():
        import json

        state = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    st.markdown(
        """
        <style>
        .mood-card {
            border-radius: 18px;
            padding: 18px;
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 10px 30px rgba(2, 6, 23, 0.28);
            margin-bottom: 14px;
        }
        .mood-title {
            color: #f8fafc;
            font-weight: 700;
            font-size: 1.08rem;
            margin-bottom: 6px;
        }
        .mood-sub {
            color: #94a3b8;
            font-size: 0.92rem;
            margin-bottom: 10px;
        }
        .mood-chip {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.84rem;
            margin-right: 8px;
            margin-bottom: 8px;
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.25);
            background: rgba(30, 41, 59, 0.88);
        }
        .breath-step {
            text-align: center;
            border-radius: 16px;
            padding: 14px 10px;
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(125, 211, 252, 0.18);
        }
        .breath-num {
            font-size: 1.6rem;
            font-weight: 700;
            color: #67e8f9;
        }
        .breath-label {
            color: #cbd5e1;
            margin-top: 4px;
        }
        .glow-orb {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            margin: 8px auto 16px auto;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.72), color-mix(in srgb, var(--orb-color) var(--glow-strength), #0f172a));
            box-shadow: 0 0 28px color-mix(in srgb, var(--orb-color) var(--glow-strength), transparent), 0 0 calc(var(--ring-softness) * 1px) color-mix(in srgb, var(--orb-color) 45%, transparent), 0 0 70px rgba(15, 23, 42, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0f172a;
            font-weight: 700;
            text-align: center;
            padding: 18px;
            transition: all 0.25s ease;
        }
        .support-line {
            border-left: 4px solid #67e8f9;
            background: rgba(8, 47, 73, 0.26);
            border-radius: 14px;
            padding: 12px 14px;
            color: #e0f2fe;
            margin-top: 10px;
        }
        .score-box {
            border-radius: 14px;
            padding: 12px;
            text-align: center;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.16);
        }
        .score-label {
            color: #94a3b8;
            font-size: 0.84rem;
        }
        .score-value {
            color: #f8fafc;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🫧 Mood Beat：心情偵測 × 呼吸放鬆 × 今日 Beat")
    st.caption("先描述你今天的狀態，再用呼吸穩定節奏，最後產生適合你的 beat 提示。")

    nickname_preview = state.get("nickname", "")
    mood_preview = state.get("mood", "平靜")
    support_preview = COMFORT_LINES.get(mood_preview, "今天先慢一點，也是一種很好的前進。")
    if nickname_preview.strip():
        support_preview = f"{nickname_preview}，{support_preview}"
    st.markdown(f"<div class='support-line'>💬 {support_preview}</div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1], gap="large")

    with left:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">1) 今天的心情狀態</div>', unsafe_allow_html=True)
        st.markdown('<div class="mood-sub">你可以直接選情緒，也可以用數值描述身體與精神狀態。</div>', unsafe_allow_html=True)

        nickname = st.text_input("今天想怎麼稱呼你", value=state.get("nickname", ""), placeholder="例如：小安")
        mood = st.selectbox(
            "目前最接近的心情",
            MOOD_OPTIONS,
            index=MOOD_OPTIONS.index(state.get("mood", "平靜")) if state.get("mood", "平靜") in MOOD_OPTIONS else 0,
        )
        custom_mood = st.text_input(
            "補充描述你的心情（可選）",
            value=state.get("custom_mood", ""),
            placeholder="例如：平靜裡有一點空、累但還想撐一下",
        )
        energy = st.slider("能量值", 0, 100, int(state.get("energy", 55)))
        stress = st.slider("壓力值", 0, 100, int(state.get("stress", 48)))
        focus_need = st.slider("想被安撫 / 陪伴的程度", 0, 100, int(state.get("focus_need", 60)))
        note = st.text_area(
            "一句話描述今天",
            value=state.get("note", ""),
            placeholder="例如：腦袋很吵，但我想慢慢穩下來。",
            height=90,
        )
        before_stress = st.slider("呼吸前壓力感受", 0, 100, int(state.get("before_stress", stress)), key="before_stress")
        after_stress_default = int(state.get("after_stress", max(before_stress - 8, 0)))
        after_stress = st.slider("呼吸後壓力感受", 0, 100, after_stress_default, key="after_stress")
        delta = before_stress - after_stress
        st.markdown('</div>', unsafe_allow_html=True)

        profile = mood_profile(mood, energy, stress)
        support_text = COMFORT_LINES.get(mood, "今天先慢一點，也是一種很好的前進。")
        mood_display = f"{mood}（{custom_mood}）" if custom_mood.strip() else mood

        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">2) 心情分析結果</div>', unsafe_allow_html=True)
        st.markdown(
            f"<div class='mood-chip' style='border-color:{profile['color']}; color:{profile['color']};'>{profile['label']}</div>"
            f"<div class='mood-chip'>建議節奏 {profile['tempo']} BPM</div>"
            f"<div class='mood-chip'>重點：{profile['focus']}</div>",
            unsafe_allow_html=True,
        )
        stability_score = min(max((100 - stress + energy) / 2 / 100, 0.0), 1.0)
        st.progress(stability_score, text="目前整體穩定度")
        st.info(f"現在比較適合的聲音方向：{profile['beat_style']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">Aura 自訂</div>', unsafe_allow_html=True)
        st.caption("你可以指定自己狀態比較好或比較不好時，Aura 球想呈現的風格與顏色，也可以交給隨機。")
        aura_style_choices = [AURA_RANDOM, *AURA_STYLE_OPTIONS]
        aura_color_choices = [AURA_RANDOM, *AURA_COLOR_PRESETS.keys()]
        good_style = st.selectbox(
            "狀態好時的 Aura 風格",
            aura_style_choices,
            index=aura_style_choices.index(state.get("aura_good_style", AURA_RANDOM)) if state.get("aura_good_style", AURA_RANDOM) in aura_style_choices else 0,
        )
        good_color = st.selectbox(
            "狀態好時的 Aura 顏色",
            aura_color_choices,
            index=aura_color_choices.index(state.get("aura_good_color", AURA_RANDOM)) if state.get("aura_good_color", AURA_RANDOM) in aura_color_choices else 0,
        )
        low_style = st.selectbox(
            "狀態不好時的 Aura 風格",
            aura_style_choices,
            index=aura_style_choices.index(state.get("aura_low_style", AURA_RANDOM)) if state.get("aura_low_style", AURA_RANDOM) in aura_style_choices else 0,
        )
        low_color = st.selectbox(
            "狀態不好時的 Aura 顏色",
            aura_color_choices,
            index=aura_color_choices.index(state.get("aura_low_color", AURA_RANDOM)) if state.get("aura_low_color", AURA_RANDOM) in aura_color_choices else 0,
        )
        aura = aura_status(mood, energy, stress, focus_need, delta, good_style, good_color, low_style, low_color)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">3) 今日 Aura 與收尾小儀式</div>', unsafe_allow_html=True)
        st.markdown(
            f"<div class='glow-orb' style='--orb-color: {aura['orb_color']}; --glow-strength: {aura['glow_strength']}%; --ring-softness: {aura['ring_softness']};'>{aura['title']}<br>{aura['state_label']}</div>",
            unsafe_allow_html=True,
        )
        st.caption(str(aura['subtitle']))
        st.progress(float(aura['calm_score']) / 100, text="Aura 穩定感")
        st.caption(RITUAL_SUGGESTIONS.get(mood, "做一件很小但能讓你覺得被照顧的事。"))
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">4) 呼吸引導</div>', unsafe_allow_html=True)
        st.markdown('<div class="mood-sub">選一種節奏，跟著吸氣、停留、吐氣，先讓身體慢下來。</div>', unsafe_allow_html=True)

        pattern_name = st.selectbox(
            "呼吸模式",
            list(BREATH_PATTERNS.keys()),
            index=list(BREATH_PATTERNS.keys()).index(state.get("breath_pattern", "放鬆入門")) if state.get("breath_pattern", "放鬆入門") in BREATH_PATTERNS else 1,
        )
        pattern = BREATH_PATTERNS[pattern_name]
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='breath-step'><div class='breath-num'>{pattern['inhale']}</div><div class='breath-label'>吸氣</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='breath-step'><div class='breath-num'>{pattern['hold']}</div><div class='breath-label'>停留</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='breath-step'><div class='breath-num'>{pattern['exhale']}</div><div class='breath-label'>吐氣</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='breath-step'><div class='breath-num'>{pattern['rounds']}</div><div class='breath-label'>回合</div></div>", unsafe_allow_html=True)

        st.success("提示：吸氣時肩膀放鬆，吐氣盡量比吸氣長一點。")
        score1, score2, score3 = st.columns(3)
        with score1:
            st.markdown(f"<div class='score-box'><div class='score-label'>呼吸前</div><div class='score-value'>{before_stress}</div></div>", unsafe_allow_html=True)
        with score2:
            st.markdown(f"<div class='score-box'><div class='score-label'>呼吸後</div><div class='score-value'>{after_stress}</div></div>", unsafe_allow_html=True)
        with score3:
            st.markdown(f"<div class='score-box'><div class='score-label'>變化</div><div class='score-value'>{delta:+d}</div></div>", unsafe_allow_html=True)
        if delta > 0:
            st.caption("你有慢慢穩下來一點點，這就很值得了。")
        elif delta == 0:
            st.caption("分數還沒變也沒關係，身體有時候需要多一點時間。")
        else:
            st.caption("如果呼吸後反而更有感，代表你有注意到自己，這也是進步。")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.markdown('<div class="mood-title">5) 今日 Beat 生成器</div>', unsafe_allow_html=True)
        beat_mode = st.selectbox(
            "想要的 beat 類型",
            BEAT_OPTIONS,
            index=BEAT_OPTIONS.index(state.get("beat_mode", "Lo-fi")) if state.get("beat_mode", "Lo-fi") in BEAT_OPTIONS else 0,
        )
        soundscape = st.selectbox(
            "想加入的環境聲",
            SOUND_OPTIONS,
            index=SOUND_OPTIONS.index(state.get("soundscape", "雨聲")) if state.get("soundscape", "雨聲") in SOUND_OPTIONS else 0,
        )
        add_voice = st.toggle("加入自然聲或環境聲", value=bool(state.get("add_voice", True)))
        want_drums = st.toggle("保留明顯鼓點", value=bool(state.get("want_drums", True)))

        texture = f"{soundscape}, vinyl noise" if add_voice else "clean soft texture"
        drums = "gentle drums" if want_drums else "minimal percussion"
        today_title = beat_title(mood, beat_mode, soundscape, stress)
        beat_prompt = (
            f"Create a {beat_mode.lower()} beat called '{today_title}' for someone feeling {mood_display}, "
            f"with energy {energy}/100 and stress {stress}/100. "
            f"Use {profile['beat_style']}, tempo around {profile['tempo']} BPM, {drums}, {texture}, "
            f"and a mood that supports: {profile['focus']}. "
            f"Add a comforting atmosphere inspired by {soundscape}."
        )

        st.text_input("今日專屬 beat 名稱", value=today_title)
        st.text_area("給音樂生成器的 prompt", value=beat_prompt, height=160)
        st.markdown('</div>', unsafe_allow_html=True)

    import json

    DATA_PATH.write_text(
        json.dumps(
            {
                "nickname": nickname,
                "mood": mood,
                "custom_mood": custom_mood,
                "energy": energy,
                "stress": stress,
                "focus_need": focus_need,
                "note": note,
                "breath_pattern": pattern_name,
                "aura_good_style": good_style,
                "aura_good_color": good_color,
                "aura_low_style": low_style,
                "aura_low_color": low_color,
                "before_stress": before_stress,
                "after_stress": after_stress,
                "beat_mode": beat_mode,
                "soundscape": soundscape,
                "add_voice": add_voice,
                "want_drums": want_drums,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    st.divider()
    st.markdown("#### 給 Agent 的摘要")
    extra = format_extra_context(
        PAGE_NAME,
        共享資料檔=str(DATA_PATH),
        左欄暱稱=nickname or "（未填）",
        左欄心情=mood,
        左欄自訂心情描述=custom_mood or "（未填）",
        左欄能量值=energy,
        左欄壓力值=stress,
        左欄想被安撫程度=focus_need,
        左欄呼吸模式=pattern_name,
        左欄呼吸前壓力=before_stress,
        左欄呼吸後壓力=after_stress,
        左欄Beat類型=beat_mode,
        左欄環境聲=soundscape,
        左欄今天一句話=note or "（未填）",
        左欄狀態好Aura風格=good_style,
        左欄狀態好Aura顏色=good_color,
        左欄狀態不好Aura風格=low_style,
        左欄狀態不好Aura顏色=low_color,
    )
    st.code(extra, language="text")

    st.markdown("#### 右欄可以這樣問")
    st.markdown(
        """
- 根據我現在的心情，幫我說一句安定我的話。
- 根據左欄數值，幫我再調整 beat prompt。
- 用更溫柔的方式帶我做一次呼吸。
- 根據我的呼吸前後差異，幫我判斷今天適合哪種節奏。
"""
    )
    return extra


page_shell(
    "Mood Beat",
    "心情偵測、呼吸放鬆與適合今日狀態的 beat 生成頁面。",
    render_main,
    page_name=PAGE_NAME,
)
