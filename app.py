import streamlit as st
import json
import base64
import random
from io import BytesIO
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🖤 신윤정 생일 축하해!",
    page_icon="🐩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS & Google Fonts ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@300;400;700&family=Noto+Sans+KR:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 3rem; max-width: 880px; }

/* ── background gradient ── */
.stApp {
  background: linear-gradient(160deg, #fffaf4 0%, #fdf4fb 40%, #f4f0ff 100%);
  min-height: 100vh;
}

/* ── poodle rain ── */
.poodle-wrap {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; z-index: 9999; overflow: hidden;
}
.poodle {
  position: absolute; top: -80px;
  animation: poodleFall linear infinite;
  user-select: none;
  filter: brightness(0) saturate(100%); /* makes any emoji black */
}
@keyframes poodleFall {
  0%   { transform: translateY(0)    rotate(-10deg) scale(1);    opacity: 0; }
  5%   { opacity: 1; }
  25%  { transform: translateY(25vh) rotate(10deg)  scale(1.06); }
  50%  { transform: translateY(50vh) rotate(-8deg)  scale(0.94); }
  75%  { transform: translateY(75vh) rotate(8deg)   scale(1.03); }
  95%  { opacity: 0.8; }
  100% { transform: translateY(112vh) rotate(-10deg) scale(1);   opacity: 0; }
}

/* ── hero ── */
.hero {
  text-align: center;
  padding: 2.5rem 1rem 1.5rem;
  position: relative;
  background:
    radial-gradient(ellipse 80% 60% at 15% 10%, #ffd6e780 0%, transparent 65%),
    radial-gradient(ellipse 60% 50% at 85% 15%, #e8d5f590 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 50% 90%, #d0f4e870 0%, transparent 55%);
  border-radius: 0 0 40px 40px;
  margin-bottom: 0.5rem;
}
.hero-cake {
  font-size: 5rem;
  display: inline-block;
  animation: cakeBounce 2s ease-in-out infinite;
  filter: drop-shadow(0 8px 20px rgba(255,127,170,.45));
}
@keyframes cakeBounce {
  0%,100% { transform: translateY(0) rotate(-3deg); }
  50%     { transform: translateY(-14px) rotate(3deg); }
}
.hero-happy {
  font-family: 'Gaegu', cursive;
  font-size: 1.6rem;
  color: #c084fc;
  letter-spacing: 0.1em;
  margin: 0.3rem 0;
}
.hero-name {
  font-family: 'Gaegu', cursive;
  font-size: 3.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff7faa, #c084fc, #ff7faa);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: nameShim 3s linear infinite;
  line-height: 1.1;
  text-shadow: none;
}
@keyframes nameShim { to { background-position: 200% center; } }
.hero-date {
  font-size: 0.88rem; color: #b07090; letter-spacing: 0.12em; margin: 0.3rem 0 0.8rem;
}
.hero-confetti {
  font-size: 1.4rem; letter-spacing: 0.3em;
  animation: cFade 1.5s ease-in-out infinite alternate;
}
@keyframes cFade { from { opacity: .55; } to { opacity: 1; } }

/* ── 설이 section ── */
.seol-card {
  background: linear-gradient(135deg, #1a1a2e, #2d1b4e);
  border-radius: 24px;
  padding: 1.6rem 1.8rem;
  text-align: center;
  margin: 1rem 0;
  position: relative;
  overflow: hidden;
  border: 2px solid #3d2060;
  box-shadow: 0 12px 40px rgba(0,0,0,0.25);
}
.seol-card::before {
  content: '🖤'; font-size: 5rem; opacity: 0.07;
  position: absolute; top: -10px; right: -10px;
}
.seol-poodle {
  font-size: 4.5rem;
  display: inline-block;
  animation: seolWag 1.2s ease-in-out infinite alternate;
  filter: brightness(0) saturate(100%) invert(0);
}
@keyframes seolWag {
  from { transform: rotate(-8deg) scale(1); }
  to   { transform: rotate(8deg) scale(1.08); }
}
.seol-name {
  font-family: 'Gaegu', cursive;
  font-size: 2rem;
  color: #f0c8ff;
  font-weight: 700;
  margin: 0.4rem 0 0.2rem;
  text-shadow: 0 0 20px rgba(192,132,252,.5);
}
.seol-msg {
  font-family: 'Gaegu', cursive;
  font-size: 1.2rem;
  color: #d4a8f8;
  line-height: 1.6;
}

/* ── divider ── */
.pink-div {
  height: 1px;
  background: linear-gradient(90deg, transparent, #f0c0d8, transparent);
  margin: 1.2rem 0; border: none;
}
.doodle-div {
  text-align: center; font-size: 1.1rem; color: #e8a0c8;
  letter-spacing: 0.5em; margin: 0.3rem 0; opacity: 0.7;
}

/* ── section title ── */
.sec-title {
  font-family: 'Gaegu', cursive;
  font-size: 1.7rem;
  color: #8b5e52;
  text-align: center;
  margin-bottom: 1rem;
}

/* ── wish balloons ── */
.balloons {
  display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 0.5rem 0 1rem;
}
.balloon {
  background: linear-gradient(135deg, #ffd6e7, #e8d5f5);
  border: 1.5px solid #ffaecf;
  border-radius: 50px;
  padding: 6px 14px;
  font-family: 'Gaegu', cursive;
  font-size: 0.95rem;
  color: #7a3060;
  display: inline-block;
  animation: floatUp ease-in-out infinite alternate;
}
.balloon:nth-child(odd)  { animation-duration: 2.1s; }
.balloon:nth-child(even) { animation-duration: 2.7s; animation-delay: 0.4s; }
@keyframes floatUp { from { transform: translateY(0); } to { transform: translateY(-7px); } }

/* ── candle bar ── */
.candle-bar {
  background: white;
  border: 2px solid #fff3b0;
  border-radius: 20px;
  padding: 1.2rem 1.5rem;
  text-align: center;
  margin-bottom: 1rem;
}
.candle-bar p {
  font-family: 'Gaegu', cursive;
  font-size: 1.3rem;
  color: #8b5e52;
  margin-bottom: 0.5rem;
}

/* ── write form ── */
.write-box {
  background: white;
  border: 2px dashed #ffaecf;
  border-radius: 22px;
  padding: 1.4rem 1.5rem;
  margin-bottom: 1rem;
}

/* ── msg card ── */
.msg-card {
  background: white;
  border: 2px solid #ffd6e7;
  border-radius: 18px;
  padding: 1rem 1.1rem;
  margin-bottom: 10px;
  position: relative;
  transition: transform .2s, box-shadow .2s;
}
.msg-card:hover { transform: translateY(-3px); box-shadow: 0 10px 28px rgba(255,127,170,.18); }
.msg-card-deco {
  position: absolute; top: -13px; right: 10px; font-size: 1.5rem;
}
.msg-from { font-family: 'Gaegu', cursive; font-size: 1.05rem; color: #c084fc; font-weight: 700; margin-bottom: 3px; }
.msg-text { font-size: 0.85rem; color: #7a5060; line-height: 1.65; white-space: pre-wrap; }

/* ── photo grid ── */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 8px;
}
.photo-item { border-radius: 12px; overflow: hidden; aspect-ratio: 1; background: #f8e0f0; }
.photo-item img { width: 100%; height: 100%; object-fit: cover; display: block; }

/* ── upload zone ── */
.upload-zone {
  border: 2.5px dashed #e8d5f5;
  border-radius: 20px;
  padding: 1.5rem;
  text-align: center;
  background: white;
  margin-bottom: 0.8rem;
  transition: border-color .2s;
}

/* ── Streamlit overrides ── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, #ff7faa, #c084fc);
  color: white; border: none; border-radius: 50px;
  font-family: 'Gaegu', cursive; font-size: 1.1rem;
  padding: 10px 28px;
  box-shadow: 0 4px 16px rgba(255,127,170,.35);
  transition: transform .2s, box-shadow .2s;
  width: 100%;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(192,132,252,.4);
}
div[data-testid="stButton"] > button:active { transform: scale(.98); }

/* small outline button */
.btn-sm-wrap div[data-testid="stButton"] > button {
  background: none !important;
  border: 1.5px solid #f0c0d8 !important;
  color: #c080b0 !important;
  font-size: 0.78rem !important;
  padding: 4px 12px !important;
  box-shadow: none !important;
}
.btn-sm-wrap div[data-testid="stButton"] > button:hover {
  background: #ffd6e7 !important;
  color: #8a3060 !important;
  transform: none !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
  border: 1.5px solid #ffd6e7 !important;
  border-radius: 12px !important;
  font-family: 'Noto Sans KR', sans-serif !important;
  color: #5a2040 !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
  border-color: #c084fc !important;
  box-shadow: 0 0 0 3px rgba(192,132,252,.15) !important;
}

footer-note { text-align: center; color: #c0a0b8; font-family: 'Gaegu', cursive; }
</style>
""", unsafe_allow_html=True)

# ── Black poodle SVG rain (custom SVG approach for true black poodle) ──────────
POODLE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 80 90' width='36' height='40'>
  <!-- body -->
  <ellipse cx='40' cy='58' rx='18' ry='16' fill='#1a1a1a'/>
  <!-- head -->
  <circle cx='40' cy='32' r='14' fill='#1a1a1a'/>
  <!-- snout -->
  <ellipse cx='40' cy='42' rx='7' ry='5' fill='#2a2a2a'/>
  <!-- nose -->
  <ellipse cx='40' cy='40' rx='3.5' ry='2.5' fill='#0a0a0a'/>
  <!-- eyes -->
  <circle cx='34' cy='29' r='2.8' fill='white'/>
  <circle cx='46' cy='29' r='2.8' fill='white'/>
  <circle cx='34.8' cy='29' r='1.6' fill='#111'/>
  <circle cx='46.8' cy='29' r='1.6' fill='#111'/>
  <circle cx='35.3' cy='28.3' r='0.6' fill='white'/>
  <circle cx='47.3' cy='28.3' r='0.6' fill='white'/>
  <!-- ears -->
  <ellipse cx='26' cy='35' rx='8' ry='12' fill='#1a1a1a' transform='rotate(-15 26 35)'/>
  <ellipse cx='54' cy='35' rx='8' ry='12' fill='#1a1a1a' transform='rotate(15 54 35)'/>
  <!-- poodle puffs - head top -->
  <circle cx='34' cy='20' r='7' fill='#222'/>
  <circle cx='46' cy='20' r='7' fill='#222'/>
  <circle cx='40' cy='16' r='7' fill='#222'/>
  <!-- front legs -->
  <rect x='27' y='70' width='8' height='16' rx='4' fill='#1a1a1a'/>
  <rect x='45' y='70' width='8' height='16' rx='4' fill='#1a1a1a'/>
  <!-- paw puffs -->
  <circle cx='31' cy='87' r='5' fill='#222'/>
  <circle cx='49' cy='87' r='5' fill='#222'/>
  <!-- tail -->
  <path d='M58 55 Q72 45 68 38 Q65 32 60 36' stroke='#1a1a1a' stroke-width='5' fill='none' stroke-linecap='round'/>
  <circle cx='64' cy='34' r='6' fill='#222'/>
  <!-- bow on head -->
  <path d='M36 16 Q40 12 44 16 Q40 20 36 16Z' fill='#ff7faa'/>
  <circle cx='40' cy='16' r='2' fill='#ff4488'/>
</svg>"""

poodle_b64 = base64.b64encode(POODLE_SVG.encode()).decode()

# Build rain HTML
rain_items = []
for i in range(26):
    left     = random.uniform(0, 97)
    delay    = random.uniform(0, 12)
    duration = random.uniform(5.5, 13)
    size     = random.uniform(0.7, 1.3)
    # Mix in some paw prints and ribbons too
    icon_choice = random.random()
    if icon_choice < 0.7:
        # SVG poodle
        rain_items.append(
            f'<img src="data:image/svg+xml;base64,{poodle_b64}" '
            f'style="position:absolute;top:-80px;left:{left:.1f}%;'
            f'width:{int(28*size)}px;height:{int(32*size)}px;'
            f'animation:poodleFall {duration:.1f}s {delay:.1f}s linear infinite;'
            f'opacity:0;" />'
        )
    elif icon_choice < 0.85:
        # Paw
        rain_items.append(
            f'<span style="position:absolute;top:-60px;left:{left:.1f}%;'
            f'font-size:{int(20*size)}px;'
            f'animation:poodleFall {duration:.1f}s {delay:.1f}s linear infinite;'
            f'opacity:0;">🐾</span>'
        )
    else:
        # Ribbon
        rain_items.append(
            f'<span style="position:absolute;top:-60px;left:{left:.1f}%;'
            f'font-size:{int(18*size)}px;'
            f'animation:poodleFall {duration:.1f}s {delay:.1f}s linear infinite;'
            f'opacity:0;">🎀</span>'
        )

rain_css = """
<style>
@keyframes poodleFall {
  0%   { transform: translateY(0)     rotate(-10deg) scale(1);    opacity: 0; }
  5%   { opacity: 1; }
  25%  { transform: translateY(25vh)  rotate(10deg)  scale(1.06); }
  50%  { transform: translateY(50vh)  rotate(-8deg)  scale(0.94); }
  75%  { transform: translateY(75vh)  rotate(8deg)   scale(1.03); }
  95%  { opacity: 0.85; }
  100% { transform: translateY(112vh) rotate(-10deg) scale(1);    opacity: 0; }
}
</style>
"""
st.markdown(rain_css + f'<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;overflow:hidden;">{"".join(rain_items)}</div>',
            unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "photos" not in st.session_state:
    st.session_state.photos = []   # list of base64 strings
if "candles" not in st.session_state:
    st.session_state.candles = 5
if "edit_idx" not in st.session_state:
    st.session_state.edit_idx = None

# ── Helpers ───────────────────────────────────────────────────────────────────
def img_to_b64(f) -> str:
    img = Image.open(f)
    img.thumbnail((600, 600))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()

DECOS = ["🎀","🌸","💕","🖤","🎊","🍰","✨","🌷","🎁","💐"]

CARD_BG = ["#fff5f8","#f8f0ff","#f0fbf8","#fffbf0","#f0f5ff"]

def esc(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;"))

# ═════════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-cake">🎂</div>
  <div class="hero-happy">Happy Birthday!</div>
  <div class="hero-name">신윤정</div>
  <div class="hero-date">2026년 3월 24일 🌸</div>
  <div class="hero-confetti">🎉 🖤 🎀 🖤 🎉</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="doodle-div">~ ✿ ~ ✿ ~ ✿ ~ ✿ ~ ✿ ~</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# 설이 SECTION
# ═════════════════════════════════════════════════════════════════════════════
seol_svg_big = POODLE_SVG.replace("width='36'","width='90'").replace("height='40'","height='100'")
seol_b64_big = base64.b64encode(seol_svg_big.encode()).decode()

st.markdown(f"""
<div class="seol-card">
  <div style="display:flex;align-items:center;justify-content:center;gap:1.2rem;flex-wrap:wrap;">
    <img src="data:image/svg+xml;base64,{seol_b64_big}"
         style="width:90px;height:100px;animation:seolWag 1.2s ease-in-out infinite alternate;"/>
    <div>
      <div class="seol-name">🖤 설이 등장! 🖤</div>
      <div class="seol-msg">
        멍멍! 누나 생일 축하해요! 🐾<br>
        설이가 제일 좋아하는 누나잖아요~<br>
        오늘 하루 제일 예쁘고 행복하게 보내요! 🎀
      </div>
    </div>
    <img src="data:image/svg+xml;base64,{seol_b64_big}"
         style="width:90px;height:100px;animation:seolWag 1.2s ease-in-out infinite alternate;animation-delay:.6s;transform:scaleX(-1);"/>
  </div>
</div>
<style>
@keyframes seolWag {{
  from {{ transform: rotate(-8deg) scale(1); }}
  to   {{ transform: rotate(8deg)  scale(1.08); }}
}}
</style>
""", unsafe_allow_html=True)

# ── Wish balloons ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="balloons">
  <span class="balloon">🖤 행복하세요</span>
  <span class="balloon">🎂 건강하게</span>
  <span class="balloon">🌸 꽃길만</span>
  <span class="balloon">✨ 빛나는 하루</span>
  <span class="balloon">🍰 달콤한 하루</span>
  <span class="balloon">💕 사랑받는 날</span>
  <span class="balloon">🐾 설이랑 산책</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# CANDLE SECTION
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">🕯️ 생일 초를 불어봐요!</div>', unsafe_allow_html=True)

candle_display = "🕯️" * st.session_state.candles
if st.session_state.candles == 0:
    candle_display = "✨✨✨✨✨"

msgs = ["","하나 꺼졌다! 🎉","두 개! 아직 더 있어요~","세 개! 거의 다 왔어!",
        "네 개! 마지막 하나!","🎊 모두 껐어요! 설이랑 소원 이루어져라 🖤🐩"]

st.markdown(f"""
<div class="candle-bar">
  <div style="font-size:2.5rem;letter-spacing:6px;margin:.4rem 0 .6rem;">{candle_display}</div>
  <div style="font-family:'Gaegu',cursive;font-size:1rem;color:#c084fc;min-height:1.4rem;">
    {msgs[5 - st.session_state.candles] if st.session_state.candles < 5 else ""}
  </div>
</div>
""", unsafe_allow_html=True)

c_col1, c_col2 = st.columns(2)
with c_col1:
    if st.button("후~ 불기 🌬️", key="blow"):
        if st.session_state.candles > 0:
            st.session_state.candles -= 1
        else:
            st.session_state.candles = 5
        st.rerun()
with c_col2:
    if st.button("🕯️ 다시 켜기", key="relight"):
        st.session_state.candles = 5
        st.rerun()

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MESSAGE BOARD
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">💌 축하 메시지 남기기</div>', unsafe_allow_html=True)

# Edit mode
if st.session_state.edit_idx is not None:
    ei = st.session_state.edit_idx
    st.markdown(f"""
    <div style="background:white;border:2px solid #c084fc;border-radius:20px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
      <div style="font-family:'Gaegu',cursive;font-size:1.2rem;color:#8b5e52;margin-bottom:.6rem;">✏️ 메시지 수정하기</div>
    </div>
    """, unsafe_allow_html=True)
    edit_from = st.text_input("이름", value=st.session_state.messages[ei]["from"], key="edit_from_input")
    edit_text = st.text_area("메시지", value=st.session_state.messages[ei]["text"], key="edit_text_input", height=100)
    ec1, ec2 = st.columns(2)
    with ec1:
        if st.button("💾 저장하기", key="save_edit"):
            if edit_from.strip() and edit_text.strip():
                st.session_state.messages[ei] = {"from": edit_from.strip(), "text": edit_text.strip()}
                st.session_state.edit_idx = None
                st.rerun()
    with ec2:
        if st.button("❌ 취소", key="cancel_edit"):
            st.session_state.edit_idx = None
            st.rerun()
    st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# Write form
with st.container():
    st.markdown('<div class="write-box">', unsafe_allow_html=True)
    new_from = st.text_input("이름 🐾", placeholder="누구누구", key="new_from", max_chars=20,
                             label_visibility="visible")
    new_text = st.text_area("메시지 💬",
                            placeholder="윤정아, 생일 축하해! 올해도 설이랑 꽃길만 걷길 🌸",
                            key="new_text", height=100, label_visibility="visible")
    if st.button("🖤 메시지 올리기!", key="submit_msg"):
        if new_from.strip() and new_text.strip():
            st.session_state.messages.insert(0, {
                "from": new_from.strip(),
                "text": new_text.strip()
            })
            st.rerun()
        else:
            st.warning("이름이랑 메시지 모두 써줘요! 🐾")
    st.markdown('</div>', unsafe_allow_html=True)

# Display cards
if st.session_state.messages:
    for i, msg in enumerate(st.session_state.messages):
        bg   = CARD_BG[i % len(CARD_BG)]
        deco = DECOS[i % len(DECOS)]
        st.markdown(f"""
        <div class="msg-card" style="background:{bg};">
          <div class="msg-card-deco">{deco}</div>
          <div class="msg-from">🐾 {esc(msg['from'])}</div>
          <div class="msg-text">{esc(msg['text'])}</div>
        </div>
        """, unsafe_allow_html=True)

        btn_col1, btn_col2, btn_col3 = st.columns([3, 1, 1])
        with btn_col2:
            st.markdown('<div class="btn-sm-wrap">', unsafe_allow_html=True)
            if st.button("✏️ 수정", key=f"edit_{i}"):
                st.session_state.edit_idx = i
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with btn_col3:
            st.markdown('<div class="btn-sm-wrap">', unsafe_allow_html=True)
            if st.button("🗑️ 삭제", key=f"del_{i}"):
                st.session_state.messages.pop(i)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#c8a0b8;
      font-family:'Gaegu',cursive;font-size:1.2rem;background:white;
      border:2px dashed #ffd6e7;border-radius:18px;">
      🖤 첫 번째 메시지를 남겨봐요!<br>
      <span style="font-size:.85rem;">설이도 기다리고 있어요 🐾</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='pink-div' style='margin:1.5rem 0;'>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PHOTO GALLERY
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">📸 추억 사진 모으기</div>', unsafe_allow_html=True)

st.markdown("""
<div class="upload-zone">
  <div style="font-size:2.2rem;margin-bottom:4px;">🖤</div>
  <div style="font-family:'Gaegu',cursive;font-size:1.1rem;color:#8b5e52;margin-bottom:3px;">
    사진 업로드
  </div>
  <div style="font-size:0.82rem;color:#c0a0c8;">아래 버튼으로 올려봐요 🌸 (여러 장 가능)</div>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "사진 선택", type=["jpg","jpeg","png","webp","gif"],
    accept_multiple_files=True, key="photo_uploader",
    label_visibility="collapsed",
)
if uploaded_files:
    for f in uploaded_files:
        b64 = img_to_b64(f)
        if b64 not in st.session_state.photos:
            st.session_state.photos.append(b64)

# Display photo grid
photos = st.session_state.photos
if photos:
    cols_per_row = 3
    for row_start in range(0, len(photos), cols_per_row):
        row_photos = photos[row_start : row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for j, b64 in enumerate(row_photos):
            with cols[j]:
                st.markdown(
                    f'<div class="photo-item"><img src="data:image/jpeg;base64,{b64}" '
                    f'style="width:100%;height:100%;object-fit:cover;border-radius:12px;"></div>',
                    unsafe_allow_html=True,
                )
                idx = row_start + j
                if st.button("✕", key=f"delpic_{idx}", help="사진 삭제"):
                    st.session_state.photos.pop(idx)
                    st.rerun()

    _, clr_col = st.columns([3,1])
    with clr_col:
        if st.button("🗑️ 전체 삭제", key="clear_photos"):
            st.session_state.photos = []
            st.rerun()
else:
    st.markdown("""
    <div style="text-align:center;padding:1.8rem;color:#d8a0c0;font-size:.9rem;
      background:white;border:1.5px dashed #f0c0d8;border-radius:14px;
      font-family:'Gaegu',cursive;">
      📷 설이랑 찍은 사진도 올려봐요! 🖤
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
seol_small_b64 = base64.b64encode(POODLE_SVG.replace("width='36'","width='48'").replace("height='40'","height='52'").encode()).decode()

st.markdown("<hr class='pink-div' style='margin:2rem 0 1rem;'>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;padding:1.5rem 1rem 2rem;font-family:'Gaegu',cursive;">
  <div style="display:flex;justify-content:center;gap:12px;margin-bottom:.8rem;">
    <img src="data:image/svg+xml;base64,{seol_small_b64}" style="width:48px;height:52px;"/>
    <img src="data:image/svg+xml;base64,{seol_small_b64}" style="width:48px;height:52px;transform:scaleX(-1);"/>
    <img src="data:image/svg+xml;base64,{seol_small_b64}" style="width:48px;height:52px;"/>
  </div>
  <div style="font-size:1.3rem;color:#8b5e52;margin-bottom:4px;">신윤정 생일 축하해요 💕</div>
  <div style="font-size:1rem;color:#c0a0b8;">오늘 하루도 설이처럼 복슬복슬하게 행복하길! 🖤🐾</div>
</div>
""", unsafe_allow_html=True)
