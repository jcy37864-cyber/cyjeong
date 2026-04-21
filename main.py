import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# 세션 상태 초기화
if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2),
        "loading_done": False,
        "trust_count": 0  # 믿음 테스트용 카운터
    })

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    if st.session_state.stage >= 4:
        bg, text, accent, btn_bg = "#FFFFFF", "#333333", "#FF4B4B", "#FFF0F0"
    else:
        bg, text, accent, btn_bg = "#000000", "#FF0000", "#8B0000", "#1A1A1A"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 1.5s ease; }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 15px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    .center {{ text-align: center; }}
    .big-text {{ font-size: 35px; font-weight: bold; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 유틸리티 함수 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

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

# ================= 4. 메인 게임 로직 =================

# [Stage 0] 입장 카운트다운
if st.session_state.stage == 0:
    st.markdown('<div class="center big-text">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            bar = st.progress(0)
            for i in range(101):
                time.sleep(0.1) 
                bar.progress(i)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 접속 승인됨.")
        if st.button("깊은 곳으로 들어가기"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 서막
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">누군가 널 지켜보고 있어...</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    typewriter("소연아... 절대 뒤돌아보지 마...")
    if st.button("도망치기"):
        st.session_state.stage = 2
        st.rerun()

# [Stage 2] 문 고르기
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center big-text">죽음의 선택 ({st.session_state.survive}/5)</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"d_{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                else:
                    st.session_state.fail += 1
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()
    if st.session_state.fail >= 3:
        st.error("갇혔습니다.")
        if st.button("재도전"): st.session_state.clear(); st.rerun()
    if st.session_state.survive >= 5:
        if st.button("탈출구로 뛰기"):
            st.session_state.stage = 3
            st.rerun()

# [Stage 3] 믿음 테스트 (유도 질문 추가)
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">마지막 질문이야.</div>', unsafe_allow_html=True)
    show_img("scary2.jpg")
    
    # 클릭 횟수에 따른 멘트 변화
    if st.session_state.trust_count == 0:
        msg = "소연아, 너 정말 나를 믿어?"
        btn_label = "믿는다"
    elif st.session_state.trust_count == 1:
        msg = "거짓말 아니지? 다시 한번 물을게. 정말 믿어?"
        btn_label = "진짜 믿는다니까!"
    else:
        msg = "마지막이야. 내 손을 잡을 용기가 있어?"
        btn_label = "끝까지 믿어!"

    typewriter(msg)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(btn_label):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3:
                st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("못 믿겠어"):
            st.markdown('<h1 class="center">💥 GAME OVER 💥</h1>', unsafe_allow_html=True)
            if st.button("부활"): st.session_state.clear(); st.rerun()

# [Stage 4] 반전 고백
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">🎉 서프라이즈! 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("많이 무서웠지? 사실 널 위해 준비한 이벤트야!")
    if st.button("내 진심을 확인해볼래?"):
        st.session_state.stage = 5
        st.rerun()

# [Stage 5] 하트 잡기
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center big-text" style="color:#FF4B4B;">내 마음을 받아줘 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 5)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"e_{i}"):
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
    if st.session_state.heart >= 5:
        if st.button("모든 마음을 모았어! 클릭! ✨"):
            with st.spinner("진심을 담는 중..."): time.sleep(3)
            st.session_state.stage = 6
            st.rerun()

# [Stage 6] 최종 고백
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center big-text">소연아...</div>', unsafe_allow_html=True)
    typewriter("나랑 평생 함께해줄래? 🌹", speed=0.1)
    if st.button("YES! 💖"):
        st.session_state.stage = 7
        st.rerun()

# [Stage 7] 엔딩
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    show_img("final.jpg")
    st.markdown('<div class="center">위의 사진을 확인해봐!</div>', unsafe_allow_html=True)
    if st.button("다시 하기"): st.session_state.clear(); st.rerun()
