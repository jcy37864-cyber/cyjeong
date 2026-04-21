import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# [세션 상태 안전 초기화]
if "stage" not in st.session_state: st.session_state.stage = 0
if "survive" not in st.session_state: st.session_state.survive = 0
if "fail" not in st.session_state: st.session_state.fail = 0
if "heart" not in st.session_state: st.session_state.heart = 0
if "safe_choice" not in st.session_state: st.session_state.safe_choice = random.randint(0, 2)
if "heart_choice" not in st.session_state: st.session_state.heart_choice = random.randint(0, 2)
if "loading_done" not in st.session_state: st.session_state.loading_done = False
if "trust_count" not in st.session_state: st.session_state.trust_count = 0
if "roulette_score" not in st.session_state: st.session_state.roulette_score = 0
if "roulette_done" not in st.session_state: st.session_state.roulette_done = False
if "dist" not in st.session_state: st.session_state.dist = 100
if "current_track" not in st.session_state: st.session_state.current_track = ""

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    is_love = st.session_state.stage >= 4
    bg = "#FFFFFF" if is_love else "#000000"
    txt = "#333333" if is_love else "#FF0000"
    btn = "#FFF0F0" if is_love else "#1A1A1A"
    acc = "#FF4B4B" if is_love else "#8B0000"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 0.5s ease; }}
    div.stButton > button {{
        background-color: {btn} !important;
        color: {acc} !important;
        border: 2px solid {acc} !important;
        border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
        40% {{ transform: translate(1px, -1px) rotate(1deg); }}
        60% {{ transform: translate(-3px, 1px) rotate(-1deg); }}
        100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
    }}
    .shake-text {{ display: inline-block; animation: shake 0.2s infinite; color: red; font-size: 30px; font-weight: bold; }}
    .center {{ text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 기능 함수 =================
def play_audio(file_name):
    current = st.session_state.get("current_track", "")
    if current == file_name:
        return
    
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)
        except:
            pass

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)

def typewriter(text, speed=0.06):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center" style="font-size:20px;">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 4. 메인 로직 =================

# [Stage 0] 로딩
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            bar = st.progress(0)
            status_text = st.empty()
            msgs = ["접속 우회 중...", "데이터 분석 중...", "보안 뚫는 중...", "최종 승인 중...", "완료."]
            for i in range(101):
                time.sleep(0.05)
                bar.progress(i)
                idx = min(i // 25, len(msgs) - 1)
                status_text.markdown(f'<div class="center">{msgs[idx]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 이소연의 접속이 승인되었습니다.")
        if st.button("어둠 속으로 입장"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 도망쳐!
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">소연아 도망쳐!!!</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    st.markdown(f'<div class="center" style="font-size:20px;">거리: <b style="color:red;">{st.session_state.dist}m</b></div>', unsafe_allow_html=True)
    
    if st.session_state.dist > 0:
        if st.button("미친 듯이 뛰기 (클릭!)"):
            st.session_state.dist -= 20
            st.toast("더 빨리!!")
            st.rerun()
    else:
        st.success("따돌린 것 같다...")
        if st.button("다음 통로로 이동하기"):
            st.session_state.stage = 2
            st.rerun()

# [Stage 2] 문 선택
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">문 선택 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if random.random() > 0.5: show_img("scary2.jpg")
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"door_{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                else:
                    st.session_state.fail += 1
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        if st.button("다시 도전"):
            st.session_state.survive = 0
            st.session_state.fail = 0
            st.rerun()
    if st.session_state.survive >= 3:
        if st.button("탈출구 발견!"):
            st.session_state.stage = 2.5
            st.rerun()

# [Stage 2.5] 공포의 룰렛
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:30px; color:red;">💀 공포의 룰렛 💀</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="center">통과 횟수: {st.session_state.roulette_score}/2</div>', unsafe_allow_html=True)
    
    if not st.session_state.roulette_done:
        if st.button("룰렛 돌리기"):
            with st.spinner("운명 결정 중..."):
                time.sleep(1)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    if st.session_state.roulette_score >= 2: st.session_state.roulette_done = True
                else:
                    st.error("꽝! 다시 시작해!")
                    show_img("jumpscare.jpg")
                    st.session_state.roulette_score = 0
            st.rerun()
    else:
        if st.button("빛이 보이는 곳으로"):
            st.session_state.stage
