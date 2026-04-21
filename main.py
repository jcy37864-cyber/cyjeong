import streamlit as st
import time
import os
import random
import base64

# ================= 기본 설정 =================
st.set_page_config(
    page_title="???",
    page_icon="👁️",
    initial_sidebar_state="collapsed"
)

# ================= 오디오 함수 =================
def play_audio(file, loop=True):
    if os.path.exists(file):
        audio_file = open(file, "rb")
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()

        loop_attr = "loop" if loop else ""

        st.markdown(f"""
        <audio autoplay {loop_attr}>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

# ================= 배경 =================
def set_bg(image):
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("{image}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

if os.path.exists("bg.jpg"):
    set_bg("bg.jpg")

# ================= 스타일 =================
st.markdown("""
<style>
html, body, .stApp {
    background-color: black !important;
    color: white !important;
}
#MainMenu, footer, header {visibility: hidden;}

.stButton>button {
    background-color: black;
    color: red;
    border: 1px solid red;
}

.center {text-align:center;}
.big {font-size:42px;}
.scary {color:red; font-size:36px;}
.cute {color:pink; font-size:28px;}

.blink {animation: blinker 0.2s infinite;}
@keyframes blinker {50% {opacity:0;}}

.shake {animation: shake 0.3s;}
@keyframes shake {
0% { transform: translate(5px, 5px); }
25% { transform: translate(-5px, -5px); }
50% { transform: translate(5px, -5px); }
75% { transform: translate(-5px, 5px); }
100% { transform: translate(0, 0); }
}
</style>
""", unsafe_allow_html=True)

# ================= 상태 =================
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "survive" not in st.session_state:
    st.session_state.survive = 0
if "heart" not in st.session_state:
    st.session_state.heart = 0
if "fail" not in st.session_state:
    st.session_state.fail = 0

# ================= 🎧 BGM 제어 =================
# 0~3단계 = 공포 / 4~7단계 = 사랑
if st.session_state.stage <= 3:
    play_audio("bgm_scary.mp3")
else:
    play_audio("bgm_love.mp3")

# ================= 효과 =================
def glitch(text):
    for _ in range(3):
        st.markdown(f'<div class="center scary blink">{text}</div>', unsafe_allow_html=True)
        time.sleep(0.1)

# ================= 0 =================
if st.session_state.stage == 0:
    glitch("들어오면 안됐어...")
    if st.button("들어간다..."):
        st.session_state.stage = 1

# ================= 1 =================
elif st.session_state.stage == 1:
    glitch("누가 보고 있어")
    if st.button("계속 간다"):
        st.session_state.stage = 2

# ================= 2 =================
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">살고 싶어?</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    safe = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if st.button(f"{i+1}", key=f"s{i}"):
                if i == safe:
                    st.session_state.survive += 1
                    st.success("살았다...")
                else:
                    st.session_state.fail += 1
                    st.error("틀렸다...")

    if st.session_state.fail >= 3:
        st.warning("나가는게 쉽진 않지 하하하핳하하")
        if st.button("다시"):
            st.session_state.stage = 0
            st.session_state.fail = 0
            st.session_state.survive = 0

    if st.session_state.survive >= 3:
        if st.button("도망친다"):
            st.session_state.stage = 3

# ================= 3 =================
elif st.session_state.stage == 3:
    st.markdown('<div class="center scary">정말 나를 믿어?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("믿는다"):
            st.warning("후회할걸 하하하")
            if st.button("계속"):
                st.session_state.stage = 4

    with col2:
        if st.button("안 믿는다"):
            st.markdown('<div class="big scary shake">💥 BOOM 💥</div>', unsafe_allow_html=True)
            if st.button("다음"):
                st.session_state.stage = 4

# ================= 4 =================
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋㅋㅋ 놀랐지 😆</div>', unsafe_allow_html=True)
    if st.button("다음"):
        st.session_state.stage = 5

# ================= 5 =================
elif st.session_state.stage == 5:
    st.markdown('<div class="center cute">하트 모아줘 💖</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    heart_pos = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if i == heart_pos:
                if st.button("💖", key=f"h{i}"):
                    st.session_state.heart += 1
            else:
                if st.button("🖤", key=f"b{i}"):
                    st.warning("꽝 😆")

    if st.session_state.heart >= 5:
        if st.button("다음"):
            st.session_state.stage = 6

# ================= 6 =================
elif st.session_state.stage == 6:
    st.markdown('<div class="center big">사실은...</div>', unsafe_allow_html=True)
    if st.button("확인"):
        st.session_state.stage = 7

# ================= 7 =================
elif st.session_state.stage == 7:
    st.markdown('<div class="center big">나랑 계속 함께해줄래?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💖"):
            st.balloons()
            st.success("진짜 행복하다 💖")
            if os.path.exists("qr.png"):
                st.image("qr.png")

    with col2:
        if st.button("NO 😢"):
            st.warning("다시 생각해줘...")
