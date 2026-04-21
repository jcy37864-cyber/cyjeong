import streamlit as st
import random
import os
import base64
import time

# 1. 초기화 (AttributeError 완벽 방어)
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

defaults = {"stage": 0, "survive": 0, "fail": 0, "heart": 0, 
            "safe_choice": random.randint(0, 2), "heart_choice": random.randint(0, 2), 
            "loading_done": False}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 2. 스타일링
def apply_theme():
    if st.session_state.stage >= 4:
        bg, text, accent = "#FFFFFF", "#333333", "#FF4B4B"
    else:
        bg, text, accent = "#000000", "#FF0000", "#8B0000"
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 1.5s ease; }}
    div.stButton > button {{
        background-color: {"#1A1A1A" if st.session_state.stage < 4 else "#FFF0F0"} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 15px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    .center {{ text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# 3. 유틸리티
def typewriter(text, speed=0.07):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center" style="font-size:20px; font-family:monospace;">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# 4. 게임 로직
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:40px; font-weight:bold;">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 20초 카운트다운 (시간 끌기)
            steps = ["서버 연결 중...", "데이터베이스 침투 중...", "이소연 감정 데이터 분석 중...", 
                     "공포 지수 계산 중...", "보안 우회 완료...", "시스템 장악 중..."]
            
            for i in range(101):
                time.sleep(0.15) # 속도 조절로 시간 조절 가능
                progress_bar.progress(i)
                if i % 17 == 0:
                    status_text.markdown(f'<div class="center">{steps[i//17 % len(steps)]}</div>', unsafe_allow_html=True)
            
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 시스템이 이소연의 접속을 허용했습니다.")
        if st.button("깊은 곳으로 들어가기"):
            st.session_state.stage = 1
            st.rerun()

# [이후 단계는 기존과 동일하게 유지하되, 하트 단계에서 로딩 추가]
elif st.session_state.stage == 5:
    # (생략: 하트 잡기 로직)
    if st.session_state.heart >= 5:
        st.success("모든 마음을 획득했습니다.")
        if st.button("최종 승인 요청"):
            with st.status("이소연님에게 전할 메시지를 암호화 중...", expanded=True) as status:
                st.write("진심을 담는 중...")
                time.sleep(2)
                st.write("용기를 쥐어짜는 중...")
                time.sleep(2)
                st.write("꽃향기를 첨가하는 중...")
                time.sleep(2)
                status.update(label="준비 완료!", state="complete", expanded=False)
            st.session_state.stage = 6
            st.rerun()

# (기존 코드의 나머지 부분...)
