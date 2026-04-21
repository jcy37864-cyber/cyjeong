import streamlit as st
import time
import os
import random

# ================= 기본 설정 =================
st.set_page_config(
    page_title="???",
    page_icon="👁️",
    initial_sidebar_state="collapsed"
)

# ================= 스타일 (공포 UI) =================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: black !important;
    color: white !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stButton>button {
    background-color: black;
    color: red;
    border: 1px solid red;
    font-size: 18px;
}

.center {text-align: center;}
.big {font-size: 42px; font-weight: bold;}
.scary {color: red; font-size:36px; letter-spacing:3px;}
.cute {font-size:28px; color:pink;}

.blink {animation: blinker 0.2s linear infinite;}
@keyframes blinker {50% {opacity: 0;}}

.shake {animation: shake 0.3s;}
@keyframes shake {
0% { transform: translate(5px, 5px); }
25% { transform: translate(-5px, -5px); }
50% { transform: translate(5px, -5px); }
75% { transform: translate(-5px, 5px); }
100% { transform: translate(0px, 0px); }
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

# ================= 효과 함수 =================
def glitch(text):
    for _ in range(3):
        st.markdown(f'<div class="center scary blink">{text}</div>', unsafe_allow_html=True)
        time.sleep(0.15)

# ================= 배경음 =================
if os.path.exists("bgm.mp3"):
    st.audio("bgm.mp3", autoplay=True)

# ================= 0단계 =================
if st.session_state.stage == 0:
    glitch("들어오면 안됐어...")
    st.markdown('<div class="center">지금이라도 늦지 않았어</div>', unsafe_allow_html=True)

    if os.path.exists("scary1.jpg"):
        st.image("scary1.jpg")

    if st.button("들어간다..."):
        st.session_state.stage = 1

# ================= 1단계 =================
elif st.session_state.stage == 1:
    glitch("누가 보고 있어")
    st.markdown('<div class="center scary">너 혼자가 아니야</div>', unsafe_allow_html=True)

    if os.path.exists("scary2.jpg"):
        st.image("scary2.jpg")

    st.radio("", ["도망친다", "계속 간다"], key="choice1")

    if st.button("선택"):
        st.session_state.stage = 2

# ================= 2단계 =================
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">살고 싶어?</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    safe = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if st.button(f"{i+1}", key=f"survive_{i}"):
                if i == safe:
                    st.success("...살았다")
                    st.session_state.survive += 1
                else:
                    st.session_state.fail += 1
                    st.error("틀렸다...")

    st.write(f"생존: {st.session_state.survive}/3")

    if st.session_state.fail >= 3:
        st.warning("나가는게 쉽진 않지 하하하핳하하")
        if st.button("다시 시작"):
            st.session_state.stage = 0
            st.session_state.survive = 0
            st.session_state.fail = 0

    if st.session_state.survive >= 3:
        if st.button("도망친다..."):
            st.session_state.stage = 3

# ================= 3단계 =================
elif st.session_state.stage == 3:
    st.markdown('<div class="center scary">정말 나를 믿어?</div>', unsafe_allow_html=True)

    choice = st.radio("", ["믿는다", "못 믿는다"], key="trust_choice")

    if choice == "믿는다":
        if st.button("선택", key="trust_yes"):
            st.warning("후회할걸 하하하핳하")
            if st.button("계속...", key="go_next"):
                st.session_state.stage = 4

    elif choice == "못 믿는다":
        if st.button("선택", key="trust_no"):
            if os.path.exists("boom.mp3"):
                st.audio("boom.mp3", autoplay=True)

            st.markdown('<div class="big scary shake">💥 BOOM 💥</div>', unsafe_allow_html=True)

            if st.button("다음"):
                st.session_state.stage = 4

# ================= 4단계 =================
elif st.session_state.stage == 4:
    glitch("...")
    time.sleep(0.5)

    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋㅋㅋ 놀랐지 😆</div>', unsafe_allow_html=True)

    if os.path.exists("cute.jpg"):
        st.image("cute.jpg")

    if st.button("다음"):
        st.session_state.stage = 5

# ================= 5단계 =================
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

    st.write(f"하트: {st.session_state.heart}/5")

    if st.session_state.heart >= 5:
        if st.button("다음"):
            st.session_state.stage = 6

# ================= 6단계 =================
elif st.session_state.stage == 6:
    st.markdown('<div class="center big">나는 어떤 사람?</div>', unsafe_allow_html=True)

    st.radio("", ["잘생김 😎", "귀여움 🐶", "완벽 💯", "다 맞음"])

    if st.button("확인"):
        st.success("정답: 다 맞음 ㅋㅋ")
        st.session_state.stage = 7

# ================= 7단계 =================
elif st.session_state.stage == 7:
    st.markdown('<div class="center big">사실은...</div>', unsafe_allow_html=True)

    if os.path.exists("final.jpg"):
        st.image("final.jpg")

    st.markdown('<div class="center">다 너 웃게 해주려고 만든거야</div>', unsafe_allow_html=True)
    st.markdown('<div class="center cute">근데 진짜로 좋아해 💖</div>', unsafe_allow_html=True)

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
            st.warning("다시 생각해줘...🥺")
