import streamlit as st
import time
import os
import random

st.set_page_config(page_title="???", page_icon="👁️", layout="centered")

# ================= 상태 =================
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "survive" not in st.session_state:
    st.session_state.survive = 0
if "heart" not in st.session_state:
    st.session_state.heart = 0
if "jumpscare" not in st.session_state:
    st.session_state.jumpscare = False

# ================= 스타일 =================
st.markdown("""
<style>
body {background-color: black; color: white;}
.center {text-align: center;}
.big {font-size: 42px; font-weight: bold;}
.scary {color: red; font-size:36px; letter-spacing:4px;}
.cute {font-size:28px; color:pink;}
.blink {animation: blinker 0.2s linear infinite;}
@keyframes blinker {50% {opacity: 0;}}
img {border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

# ================= 공포 효과 =================
def glitch(text, repeat=4, speed=0.15):
    for _ in range(repeat):
        st.markdown(f'<div class="center scary blink">{text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 사운드 =================
if os.path.exists("bgm.mp3"):
    st.audio("bgm.mp3", autoplay=True)

# 점프스케어 사운드
if st.session_state.jumpscare and os.path.exists("boom.mp3"):
    st.audio("boom.mp3", autoplay=True)

# ================= 0단계 =================
if st.session_state.stage == 0:
    glitch("들어오면 안됐어...")
    st.markdown('<div class="center">지금이라도 늦지 않았어</div>', unsafe_allow_html=True)
    time.sleep(1)

    if os.path.exists("scary1.jpg"):
        st.image("scary1.jpg")

    st.markdown('<div class="center scary">뒤를 돌아봐...</div>', unsafe_allow_html=True)

    if st.button("들어간다...", key="start"):
        st.session_state.stage = 1

# ================= 1단계 =================
elif st.session_state.stage == 1:
    glitch("누가 보고 있어")
    st.markdown('<div class="center scary">너 혼자가 아니야</div>', unsafe_allow_html=True)

    if os.path.exists("scary2.jpg"):
        st.image("scary2.jpg")

    choice = st.radio("", ["도망친다", "계속 간다"])

    if st.button("선택", key="decide1"):
        st.session_state.stage = 2

# ================= 2단계 =================
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">살고 싶어?</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">틀리면 처음부터야...</div>', unsafe_allow_html=True)

    if "fail_count" not in st.session_state:
        st.session_state.fail_count = 0

    cols = st.columns(3)
    safe = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if st.button(f"{i+1}", key=f"survive_{i}"):
                if i == safe:
                    st.success("...살았다")
                    st.session_state.survive += 1
                else:
                    st.session_state.fail_count += 1
                    st.error("틀렸다...")

    st.write(f"생존: {st.session_state.survive}/3")

    # 3번 연속 실패
    if st.session_state.fail_count >= 3:
        st.warning("나가는게 쉽진 않지 하하하핳하하")
        if st.button("다시 시작", key="restart_game"):
            st.session_state.stage = 0
            st.session_state.survive = 0
            st.session_state.fail_count = 0

    if st.session_state.survive >= 3:
        if st.button("도망친다...", key="next2"):
            st.session_state.stage = 3

# ================= 점프스케어 =================
elif st.session_state.stage == 99:
    st.markdown('<div class="center scary big blink">뒤에 있다</div>', unsafe_allow_html=True)

    if os.path.exists("jumpscare.jpg"):
        st.image("jumpscare.jpg")

    time.sleep(1)
    st.error("잡혔다...")

    if st.button("다시 시도", key="retry"):
        st.session_state.stage = 0
        st.session_state.survive = 0
        st.session_state.jumpscare = False

# ================= 3단계 =================
elif st.session_state.stage == 3:
    st.markdown('<div class="center scary">마지막 질문</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">정말 나를 믿어?</div>', unsafe_allow_html=True)

    choice = st.radio("", ["믿는다", "못 믿는다"])

    if choice == "믿는다":
        if st.button("선택", key="trust_yes"):
            st.warning("후회할걸 하하하핳하")
            if st.button("...", key="continue_trust"):
                st.session_state.stage = 4

    else:
        if st.button("선택", key="trust_no"):
            st.balloons()
            st.error("💥 BOOM 💥")
            if st.button("다음", key="after_boom"):
                st.session_state.stage = 4

# ================= 4단계 (반전) ================= (반전) =================
elif st.session_state.stage == 4:
    glitch("...")
    time.sleep(1)
    glitch("......")
    time.sleep(1)

    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋㅋㅋ 놀랐지 😆</div>', unsafe_allow_html=True)

    if os.path.exists("cute.jpg"):
        st.image("cute.jpg")

    st.markdown('<div class="center">이제 진짜 시작 💖</div>', unsafe_allow_html=True)

    if st.button("다음 💖", key="next4"):
        st.session_state.stage = 5

# ================= 5단계 =================
elif st.session_state.stage == 5:
    st.markdown('<div class="center cute">하트 모아줘 💖</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    heart_pos = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if i == heart_pos:
                if st.button("💖", key=f"heart_{i}"):
                    st.session_state.heart += 1
            else:
                if st.button("🖤", key=f"fake_{i}"):
                    st.warning("꽝 😆")

    st.write(f"하트: {st.session_state.heart}/5")

    if st.session_state.heart >= 5:
        if st.button("다음 👉", key="next5"):
            st.session_state.stage = 6

# ================= 6단계 =================
elif st.session_state.stage == 6:
    st.markdown('<div class="center big">나는 어떤 사람?</div>', unsafe_allow_html=True)

    st.radio("", ["잘생김 😎", "귀여움 🐶", "완벽 💯", "다 맞음"])

    if st.button("확인", key="next6"):
        st.success("정답: 다 맞음 ㅋㅋ")
        st.session_state.stage = 7

# ================= 7단계 (고백) =================
elif st.session_state.stage == 7:
    st.markdown('<div class="center big">사실은...</div>', unsafe_allow_html=True)
    time.sleep(1)

    if os.path.exists("final.jpg"):
        st.image("final.jpg")

    st.markdown('<div class="center">다 너 웃게 해주려고 만든거야</div>', unsafe_allow_html=True)
    st.markdown('<div class="center cute">근데 진짜로 좋아해 💖</div>', unsafe_allow_html=True)

    st.markdown('<div class="center big">나랑 계속 함께해줄래?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💖", key="yes"):
            st.balloons()
            st.success("진짜 행복하다 💖")
            st.markdown("QR 코드 찍어봐 👇")
            st.image("qr.png")

    with col2:
        if st.button("NO 😢", key="no"):
            st.warning("다시 생각해줘...🥺")

st.markdown('<div class="center">Made with 👁️</div>', unsafe_allow_html=True)
