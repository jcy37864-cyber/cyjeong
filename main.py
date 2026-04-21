import streamlit as st
import time
import os
import random

st.set_page_config(page_title="???", page_icon="👁️")

# ================= 상태 =================
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "survive" not in st.session_state:
    st.session_state.survive = 0
if "heart" not in st.session_state:
    st.session_state.heart = 0
if "flash" not in st.session_state:
    st.session_state.flash = False

# ================= 스타일 =================
st.markdown("""
<style>
body {background-color: black; color: white;}
.center {text-align: center;}
.big {font-size: 36px; font-weight: bold;}
.mid {font-size: 24px;}
.small {font-size:18px;}
.scary {color: red; font-size:30px; letter-spacing:2px;}
.cute {font-size:28px; color:pink;}
.btn button {width:100%; height:60px; font-size:20px;}
.blink {animation: blinker 0.7s linear infinite;}
@keyframes blinker {50% {opacity: 0;}}
</style>
""", unsafe_allow_html=True)

# ================= 공통 함수 =================

def play_bgm():
    if os.path.exists("bgm.mp3"):
        st.audio("bgm.mp3", autoplay=True)


def flash_screen():
    st.markdown('<div class="center scary blink">...</div>', unsafe_allow_html=True)
    time.sleep(0.4)

# ================= 배경음 =================
play_bgm()

# ================= 0단계 (공포 시작) =================
if st.session_state.stage == 0:
    st.markdown('<div class="center scary">이곳에 들어오지 말았어야 했어.....</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">이건 단순한 게임이 아니야</div>', unsafe_allow_html=True)

    if st.button("들어간다..."):
        st.session_state.stage = 1

# ================= 1단계 (공포 선택) =================
elif st.session_state.stage == 1:
    flash_screen()
    st.markdown('<div class="center scary">지금 나갈 수 있는 기회를 줄까?? </div>', unsafe_allow_html=True)

    choice = st.radio("", ["나간다", "입장한다"])

    if st.button("선택"):
        st.warning(" 게임 좋아하는 이소연..... 게임은 이미 시작 되었어....(하하) ")
        time.sleep(1)
        st.session_state.stage = 2

# ================= 2단계 (생존 게임) =================
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">자 생존 게임을 시작하겠다.</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">3개의 쥐덧 중 하나만이 안전하다. 눌러! (3번 모두 성공시 탈출.)</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    safe = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if st.button(f"버튼 {i+1}"):
                if i == safe:
                    st.success("휴... 살아 남았다...")
                    st.session_state.survive += 1
                else:
                    st.error("으악!!! 잡혀 버렸다....")
                    st.session_state.survive = 0

    st.write(f"생존(MISSION COMPLTE): {st.session_state.survive}/3")

    if st.session_state.survive >= 3:
        if st.button("자 다음 장소로 이동하지..."):
            st.session_state.stage = 3

# ================= 3단계 (심리 질문) =================
elif st.session_state.stage == 3:
    st.markdown('<div class="center">당신은 "정충용" 나를 믿고있어?</div>', unsafe_allow_html=True)
    ans = st.radio("", ["믿는다", "못 믿는다"])

    if st.button("선택"):
        st.session_state.stage = 4

# ================= 4단계 (반전 연출) =================
elif st.session_state.stage == 4:
    st.markdown('<div class="center">...</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="center">......</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.balloons()
    st.markdown('<div class="center cute">짜잔 😆</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">속았지? 이제부터 진짜야 💖</div>', unsafe_allow_html=True)

    if st.button("다음 💖"):
        st.session_state.stage = 5

# ================= 5단계 (하트 게임) =================
elif st.session_state.stage == 5:
    st.markdown('<div class="center cute">자 하트를 많이 많이 잡아줘 💖</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    heart_pos = random.randint(0, 2)

    for i in range(3):
        with cols[i]:
            if i == heart_pos:
                if st.button("💖💖", key=f"heart_{i}"):
                    st.session_state.heart += 1
            else:
                if st.button("🖤🖤", key=f"fake_{i}"):
                    st.warning("이건 아니야 😆")

    st.write(f"하트: {st.session_state.heart}/5")

    if st.session_state.heart >= 5:
        if st.button("다음 장소로 이동 👉"):
            st.session_state.stage = 6

# ================= 6단계 (웃김) =================
elif st.session_state.stage == 6:
    st.markdown('<div class="center">중요한 질문 이야 😏😏</div>', unsafe_allow_html=True)
    st.markdown('<div class="center big">"정충용"을 어떤 사람이 라고 생각해??</div>', unsafe_allow_html=True)

    ans = st.radio("", ["잘생김 😎", "귀여움 🐶", "섹시보이 💯", "다 맞음"])

    if st.button("정답"):
        st.success("정답: 다 맞음 ㅋㅋ")
        time.sleep(1)
        st.session_state.stage = 7

# ================= 7단계 (고백 연출) =================
elif st.session_state.stage == 7:
    st.markdown('<div class="center big">사실은...</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center">처음부터 너를 위한 거였어</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center">이상한 게임 같았지?</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">근데 전부 내 진심이야</div>', unsafe_allow_html=True)

    time.sleep(1)
    st.markdown('<div class="center cute">너 좋아해 💖</div>', unsafe_allow_html=True)
    st.markdown('<div class="center big">나랑 계속 함께해줄래?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💖"):
            st.balloons()
            st.success("진짜 행복하다 💖")

    with col2:
        if st.button("NO 😢"):
            st.warning("다시 생각해줘...🥺")

# ================= 하단 =================
st.markdown('<div class="center small"> Made with JCY.... 👁️</div>', unsafe_allow_html=True)
