import streamlit as st
from googletrans import LANGUAGES
from modules.text_module import text_translation_ui
from modules.voice_module import voice_translation_ui
from modules.image_module import image_translation_ui

st.set_page_config(
    page_title="Multilingua AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = "Home"

SUPPORTED_LANGUAGES = {code: name.capitalize() for code, name in LANGUAGES.items()}
LANGUAGE_OPTIONS = sorted(SUPPORTED_LANGUAGES.values())
LANGUAGE_CODE_MAP = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

NAV_PAGES = [
    ("🏠", "Home"),
    ("📝", "Text"),
    ("🎤", "Voice"),
    ("🖼️", "Image"),
    ("🤚", "Gesture"),
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #e2e8f0; }

.stApp {
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(99,102,241,0.18) 0%, transparent 60%),
              linear-gradient(160deg, #020617 0%, #0b1120 50%, #130d2e 100%);
  min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.09) !important;
  border-radius: 14px !important;
  color: #e2e8f0 !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color: rgba(99,102,241,0.55) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

.stButton > button {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  color: #fff !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  padding: 10px 24px !important;
  width: 100% !important;
  letter-spacing: 0.01em !important;
  transition: transform 0.18s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.18s ease,
              opacity 0.15s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.01) !important;
  box-shadow: 0 12px 32px rgba(99,102,241,0.45) !important;
  opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

.nav-btn-wrap .stButton > button {
  background: transparent !important;
  border: none !important;
  border-radius: 9999px !important;
  color: #4e5d78 !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  padding: 8px 16px !important;
  box-shadow: none !important;
  letter-spacing: 0.025em !important;
  transition: background 0.18s ease, color 0.18s ease !important;
}
.nav-btn-wrap .stButton > button:hover {
  background: rgba(255,255,255,0.08) !important;
  color: #cbd5e1 !important;
  transform: none !important;
  box-shadow: none !important;
}
.nav-btn-wrap.active .stButton > button {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.45),
              inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.nav-btn-wrap.active .stButton > button:hover {
  transform: none !important;
  opacity: 0.92 !important;
}

.home-card-wrap .stButton > button {
  background: rgba(255,255,255,0.035) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 22px !important;
  color: #94a3b8 !important;
  font-weight: 400 !important;
  font-size: 0.875rem !important;
  height: 120px !important;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
  white-space: pre-line !important;
  line-height: 1.7 !important;
  transition: transform 0.22s cubic-bezier(0.34,1.4,0.64,1),
              box-shadow 0.22s ease,
              border-color 0.22s ease,
              background 0.22s ease !important;
}
.home-card-wrap .stButton > button:hover {
  background: rgba(99,102,241,0.08) !important;
  border-color: rgba(139,92,246,0.4) !important;
  color: #e2e8f0 !important;
  transform: translateY(-5px) scale(1.02) !important;
  box-shadow: 0 20px 48px rgba(0,0,0,0.3),
              0 0 0 1px rgba(139,92,246,0.2),
              0 0 32px rgba(99,102,241,0.12) !important;
}
.home-card-wrap .stButton > button:active {
  transform: translateY(-2px) scale(1.01) !important;
}

.nav-container {
  display: flex;
  justify-content: center;
  padding: 28px 0 4px;
}
.nav-pill {
  display: inline-flex;
  align-items: center;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 9999px;
  padding: 5px 8px;
  gap: 2px;
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: 0 8px 40px rgba(0,0,0,0.4),
              inset 0 1px 0 rgba(255,255,255,0.06);
}

.home-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 100px 24px 48px;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #a78bfa;
  background: rgba(167,139,250,0.08);
  border: 1px solid rgba(167,139,250,0.2);
  border-radius: 9999px;
  padding: 6px 16px;
  margin-bottom: 36px;
  box-shadow: 0 0 20px rgba(167,139,250,0.1);
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(3rem, 5.5vw, 5rem);
  font-weight: 800;
  line-height: 1.06;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #f8fafc 20%, #c4b5fd 55%, #67e8f9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 24px;
  filter: drop-shadow(0 0 40px rgba(167,139,250,0.3));
}
.hero-subtitle {
  font-size: 1.05rem;
  font-weight: 300;
  color: #3d4f66;
  max-width: 460px;
  line-height: 1.8;
  margin: 0 0 60px;
  letter-spacing: 0.01em;
}

.glass-card {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 28px;
  padding: 44px 48px 52px;
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  box-shadow: 0 32px 80px rgba(0,0,0,0.5),
              inset 0 1px 0 rgba(255,255,255,0.07),
              inset 0 -1px 0 rgba(0,0,0,0.2);
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.page-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #f1f5f9 35%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 8px;
  line-height: 1.2;
}
.page-desc {
  font-size: 0.875rem;
  color: #3d4f66;
  font-weight: 400;
  margin: 0;
  letter-spacing: 0.01em;
}

.placeholder-box {
  background: rgba(99,102,241,0.04);
  border: 1.5px dashed rgba(99,102,241,0.22);
  border-radius: 20px;
  padding: 80px 32px;
  text-align: center;
}
.placeholder-icon { font-size: 3.2rem; margin-bottom: 20px; display: block; }
.placeholder-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #475569;
  margin: 0 0 12px;
}
.placeholder-desc {
  color: #2d3a4a;
  font-size: 0.875rem;
  line-height: 1.7;
  margin: 0;
  max-width: 360px;
  margin-inline: auto;
}

.app-footer {
  text-align: center;
  padding: 56px 0 44px;
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #161f2e;
}
</style>
""", unsafe_allow_html=True)


def go_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def render_navbar() -> None:
    current = st.session_state.page
    st.markdown('<div class="nav-container"><div class="nav-pill" id="_nav"></div></div>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2.2, 1])
    with mid:
        cols = st.columns(len(NAV_PAGES))
        for col, (icon, label) in zip(cols, NAV_PAGES):
            with col:
                active_cls = "nav-btn-wrap active" if current == label else "nav-btn-wrap"
                st.markdown(f'<div class="{active_cls}">', unsafe_allow_html=True)
                if st.button(f"{icon} {label}", key=f"nav_{label}"):
                    go_to(label)
                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


def _page_shell(title: str, desc: str, content_fn=None, placeholder: dict | None = None) -> None:
    render_navbar()
    _, center, _ = st.columns([1, 5, 1])
    with center:
        ph_html = ""
        if placeholder:
            ph_html = f"""
            <div class="placeholder-box">
              <span class="placeholder-icon">{placeholder["icon"]}</span>
              <div class="placeholder-title">{placeholder["title"]}</div>
              <p class="placeholder-desc">{placeholder["desc"]}</p>
            </div>"""
        st.markdown(f"""
        <div class="glass-card">
          <div class="page-header">
            <div class="page-title">{title}</div>
            <p class="page-desc">{desc}</p>
          </div>
          {ph_html}
        </div>
        """, unsafe_allow_html=True)
        if content_fn:
            content_fn()


def page_home() -> None:
    st.markdown("""
    <div class="home-hero">
      <div class="hero-badge">✦ &nbsp;AI-Powered Translation</div>
      <h1 class="hero-title">🌐 Multilingual Translator</h1>
      <p class="hero-subtitle">
        Accurate multilingual translation with smart context understanding — powered by AI.
      </p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.8, 1])
    with center:
        st.markdown('<div class="home-card-wrap">', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            if st.button("📝\nText Translation\nType & translate instantly", key="h_text", use_container_width=True):
                go_to("Text")
        with c2:
            if st.button("🎤\nVoice Translation\nSpeak any language", key="h_voice", use_container_width=True):
                go_to("Voice")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c3, c4 = st.columns(2, gap="medium")
        with c3:
            if st.button("🖼️\nImage Translation\nTranslate from photos", key="h_image", use_container_width=True):
                go_to("Image")
        with c4:
            if st.button("🤚\nGesture Translation\nSign language support", key="h_gesture", use_container_width=True):
                go_to("Gesture")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="app-footer">Multilingua AI &nbsp;·&nbsp; Powered by Claude</div>', unsafe_allow_html=True)


def page_text() -> None:
    _page_shell(
        title="📝 Text Translation",
        desc="Type or paste any text and translate across available languages instantly.",
        content_fn=text_translation_ui,
    )


def page_voice() -> None:
    _page_shell(
        title="🎤 Voice Translation",
        desc="Speak naturally and get real-time translation in any language.",
        content_fn=voice_translation_ui,
    )

def page_image() -> None:
    _page_shell(
        title="🖼️ Image Translation",
        desc="Extract and translate text directly from images and photos.",
        content_fn=image_translation_ui,
    )

def page_gesture() -> None:
    render_navbar()

    _, center, _ = st.columns([1, 5, 1])
    with center:
        st.markdown("""
        <div class="glass-card">
          <div class="page-header">
            <div class="page-title">🤚 Gesture Translation</div>
            <p class="page-desc">
              Sign language recognition and translation powered by computer vision.
            </p>
          </div>

          <div class="placeholder-box">
            <span class="placeholder-icon">🚧</span>
            <div class="placeholder-title">Coming Soon</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

_ROUTES: dict = {
    "Home":    page_home,
    "Text":    page_text,
    "Voice":   page_voice,
    "Image":   page_image,
    "Gesture": page_gesture,
}

def main() -> None:
    _ROUTES.get(st.session_state.page, page_home)()

if __name__ == "__main__":
    main()
