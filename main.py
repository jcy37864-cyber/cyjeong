import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2),
        "loading_done": False,
        "trust_count": 0,
        "roulette_done": False
    })

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    if st.session_state.stage >= 4:
        bg, text, accent, btn_bg = "#FFFFFF", "#333333", "#FF4B4B", "#FFF0F0"
    else:
        bg, text, accent, btn_bg = "#000000", "#FF0000", "#8B0000", "#1A1A1A"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 0.8s ease; }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    .warning-text {{ color: red; font-size: 22px; font-weight: bold; animation: blink 0.8s infinite; text-align: center; }}
    .center {{ text-align: center; }}
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

# [Stage 0] 로딩
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            bar = st.progress(0)
            status_text = st.empty()
            loading_msgs = ["서버 접속 중...", "이소연 분석 중...", "보안 우회 중...", "시스템 장악 완료."]
            for i in range(101):
                time.sleep(0.08)
                bar.progress(i)
                if i % 25 == 0:
                    status_text.markdown(f'<div class="center" style="color:gray;">{loading_msgs[i//25 % len(loading_msgs)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 접속이 승인되었습니다.")
        if st.button("깊은 곳으로 들어가기"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 서막
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    show_img("scary.jpg")
    typewriter("소연아... 절대 뒤돌아보지 마.")
    if st.button("도망치기"):
        st.session_state.stage = 2
        st.rerun()

# [Stage 2] 죽음의 선택 (3회)
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">죽음의 선택 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if random.random() > 0.5: show_img("scary2.jpg")
    else: st.markdown('<p class="warning-text">망설이면 잡힌다.</p>', unsafe_allow_html=True)
    
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
        if st.button("다음 통로로!"):
            st.session_state.stage = 2.5  # 룰렛 스테이지로 이동
            st.rerun()

# [Stage 2.5] 공포의 룰렛 (NEW!)
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:30px; color:red;">💀 공포의 룰렛 💀</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">길이 막혔어... 룰렛을 돌려 "통과"가 나와야 해.</div>', unsafe_allow_html=True)
    
    if not st.session_state.roulette_done:
        if st.button("룰렛 돌리기 🎡"):
            with st.spinner("회전 중..."):
                time.sleep(2)
                result = random.choice(["꽝", "통과", "꽝", "꽝", "통과"]) # 40% 확률로 통과
                if result == "통과":
                    st.success("운이 좋았어. 길이 열렸다.")
                    st.session_state.roulette_done = True
                else:
                    st.error("꽝! 유령의 비명이 들린다!")
                    show_img("jumpscare.jpg") # 꽝 나오면 깜놀 이미지
                    time.sleep(1)
            st.rerun()
    else:
        if st.button("열린 길로 전진하기"):
            st.session_state.stage = 3
            st.rerun()

# [Stage 3] 믿음 테스트
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    show_img("scary.jpg")
    msgs = ["소연아, 정말 나를 믿어?", "진심이야? 정말로?", "마지막이야. 내 손 잡을 거야?"]
    btns = ["믿는다", "진짜 믿는다니까!", "끝까지 믿어!"]
    typewriter(msgs[st.session_state.trust_count])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(btns[st.session_state.trust_count]):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("못 믿겠어"):
            st.error("어둠 속에 홀로 남겨졌습니다.")
            if st.button("다시 대답하기"): st.session_state.trust_count = 0; st.rerun()

# [Stage 4] 반전 고백
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B; font-weight:bold;">🎉 서프라이즈! 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("소연아 미안해! 전부 널 위해 준비한 이벤트야!")
    if st.button("진짜 마음 확인하기"):
        st.session_state.stage = 5
        st.rerun()

# [Stage 5~7] 하트 잡기 및 최종 고백 (생략 없이 로직 유지)
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px; color:#FF4B4B;">내 마음을 잡아줘 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
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
                if st.button("🤍", key=f"e_{i}"): st.session_state.heart_choice = random.randint(0, 2); st.rerun()
    if st.session_state.heart >= 5:
        if st.button("진심 확인 ✨"):
            with st.spinner("준비 중..."): time.sleep(2)
            st.session_state.stage = 6
            st.rerun()

elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    typewriter("소연씨, 나랑 평생 함께해줄래? 🌹", speed=0.1)
    if st.button("YES! 💖"): st.session_state.stage = 7; st.rerun()

elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    show_img("final.jpg")
    if st.button("처음으로"): st.session_state.clear(); st.rerun()
