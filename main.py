import streamlit as st
import time
import random
import os

# ================= 기본 =================
st.set_page_config(page_title="???", page_icon="💀", layout="centered")

# ================= 상태 =================
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "bgm_started" not in st.session_state:
    st.session_state.bgm_started = False
if "bgm_type" not in st.session_state:
    st.session_state.bgm_type = "scary"
if "survive" not in st.session_state:
    st.session_state.survive = 0
if "fail" not in st.session_state:
    st.session_state.fail = 0
if "heart" not in st.session_state:
    st.session_state.heart = 0

# ================= 🎧 음악 =================
def play_bgm():
    if st.session_state.bgm_started:
        file = "bgm_scary.mp3" if st.session_state.bgm_type == "scary" else "bgm_love.mp3"
        if os.path.exists(file):
            st.markdown(f"""
            <audio autoplay loop>
            <source src="{file}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

play_bgm()

# ================= 🎨 스타일 =================
st.markdown("""
<style>
.stApp {
    background-color: black;
    color: white;
}
button {
    background-color: black !important;
    color: red !important;
    border: 1px solid red !important;
}
.center {text-align:center;}
.big {font-size:40px;}
.scary {color:red;}
.cute {color:pink;}
</style>
""", unsafe_allow_html=True)

# ================= 0 시작 =================
if st.session_state.stage == 0:
    st.markdown('<div class="center big">⚠️ 들어오면 안됐어</div>', unsafe_allow_html=True)

    if st.button("시작"):
        st.session_state.stage = 1
        st.session_state.bgm_started = True

# ================= 1 =================
elif st.session_state.stage == 1:
    st.markdown('<div class="center scary">누가 보고 있어</div>', unsafe_allow_html=True)

    if os.path.exists("scary1.jpg"):
        st.image("scary1.jpg")

    if st.button("계속"):
        st.session_state.stage = 2

# ================= 2 =================
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">살고 싶어?</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    safe = random.randint(0,2)

    for i in range(3):
        with cols[i]:
            if st.button(str(i+1), key=f"s{i}"):
                if i == safe:
                    st.success("살았다")
                    st.session_state.survive += 1
                else:
                    st.error("틀렸다")
                    st.session_state.fail += 1

    if st.session_state.fail >= 3:
        st.warning("나가는게 쉽진 않지 하하하")
        if st.button("다시"):
            st.session_state.stage = 0

    if st.session_state.survive >= 3:
        if st.button("도망"):
            st.session_state.stage = 3

# ================= 3 (문제 해결됨) =================
elif st.session_state.stage == 3:
    st.markdown('<div class="center scary">정말 나를 믿어?</div>', unsafe_allow_html=True)

    if st.button("믿는다"):
        st.session_state.stage = 4

    if st.button("안 믿는다"):
        st.markdown("💥 BOOM 💥")

# ================= 4 =================
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋ 놀랐지</div>', unsafe_allow_html=True)

    # 🎧 음악 전환
    if st.button("...사실은"):
        st.session_state.bgm_type = "love"
        st.session_state.stage = 5

# ================= 5 =================
elif st.session_state.stage == 5:
    st.markdown('<div class="center cute">하트 모아줘 💖</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    heart = random.randint(0,2)

    for i in range(3):
        with cols[i]:
            if i == heart:
                if st.button("💖", key=f"h{i}"):
                    st.session_state.heart += 1
            else:
                if st.button("🖤", key=f"b{i}"):
                    st.warning("꽝")

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

    if st.button("YES 💖"):
        st.balloons()
        if os.path.exists("qr.png"):
            st.image("qr.png")

    if st.button("NO 😢"):
        st.warning("다시 생각해줘...")
