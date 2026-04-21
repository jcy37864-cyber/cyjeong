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
        "roulette_score": 0, # 룰렛 성공 횟수 관리
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
    .stApp {{ background-color: {bg}; color: {text}; transition: all 0.5s ease; }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    .warning-text {{ color: red; font-size: 22px; font-weight: bold; animation: blink 0.6s infinite; text-align: center; }}
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

# [Stage 0] 로딩 (긴장 유발)
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            bar = st.progress(0)
            status_text = st.empty()
            loading_msgs = ["보안 우회 중...", "기록 말소 중...", "이소연 위치 추적...", "최종 승인 대기..."]
            for i in range(101):
                time.sleep(0.08)
                bar.progress(i)
                if i % 25 == 0:
                    status_text.markdown(f'<div class="center" style="color:gray;">{loading_msgs[i//25 % len(loading_msgs)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 이소연의 접속이 승인되었습니다.")
        if st.button("어둠 속으로 입장"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 서막
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    show_img("scary.jpg")
    typewriter("소연아... 도망쳐... 아니면 숨든가.")
    if st.button("앞으로 가기"):
        st.session_state.stage = 2
        st.rerun()

# [Stage 2] 죽음의 선택 (3회)
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">문 선택 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if random.random() > 0.4: show_img("scary2.jpg")
    
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
        if st.button("영혼을 되찾고 다시 시작"):
            st.session_state.survive = 0
            st.session_state.fail = 0
            st.rerun()
    if st.session_state.survive >= 3:
        if st.button("살아남았다... 다음으로."):
            st.session_state.stage = 2.5
            st.rerun()

# [Stage 2.5] 강화된 공포의 룰렛 (2번 성공해야 함)
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:30px; color:red;">🔴 강화된 공포의 룰렛 🔴</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="center">길이 완전히 막혔어. <b>2번의 "통과"</b>를 얻어야 해! ({st.session_state.roulette_score}/2)</div>', unsafe_allow_html=True)
    
    if not st.session_state.roulette_done:
        if st.button("운명에 맡기기 (룰렛 회전)"):
            with st.spinner("운명을 결정하는 중..."):
                time.sleep(1.5)
                # 난이도 조절: 1/3 확률로 성공
                res = random.choice(["꽝", "통과", "꽝"])
                if res == "통과":
                    st.session_state.roulette_score += 1
                    st.success("한 걸음 더 나아갔어!")
                    if st.session_state.roulette_score >= 2:
                        st.session_state.roulette_done = True
                else:
                    st.error("꽝! 무언가 너의 발목을 잡았어!")
                    show_img("jumpscare.jpg")
                    st.session_state.roulette_score = 0 # 실패하면 다시 0점부터 (강화)
            st.rerun()
    else:
        st.balloons()
        st.markdown('<div class="center" style="color:cyan;">탈출구가 열렸다!</div>', unsafe_allow_html=True)
        if st.button("믿음을 증명하러 가기"):
            st.session_state.stage = 3
            st.rerun()

# [Stage 3] 믿음 테스트
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    show_img("scary.jpg")
    msgs = ["소연아, 정말 나를 믿어?", "진짜야? 대답해.", "마지막 기회야. 내 손 잡을 거야?"]
    btns = ["믿는다", "진짜 믿는다니까!", "끝까지 믿어!"]
    typewriter(msgs[st.session_state.trust_count])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(btns[st.session_state.trust_count]):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("포기할래"):
            st.error("어둠 속에 갇혔습니다.")
            if st.button("다시 도전"): st.session_state.trust_count = 0; st.rerun()

# [Stage 4] 반전 (화이트 테마)
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B; font-weight:bold;">🎉 서프라이즈! 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("소연아 미안! 여기까지 오느라 고생 많았어. 사실 이건 다 널 위한 서프라이즈야!")
    if st.button("내 진심을 확인해볼래?"):
        st.session_state.stage = 5
        st.rerun()

# [Stage 5] 하트 잡기 (10개로 강화!)
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px; color:#FF4B4B;">내 마음을 잡아줘 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 10)
    
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
                    
    if st.session_state.heart >= 10:
        st.markdown("---")
        if st.button("모든 마음을 다 모았어! 클릭! ✨"):
            with st.spinner("최종 고백을 준비 중..."): time.sleep(3)
            st.session_state.stage = 6
            st.rerun()

# [Stage 6] 최종 고백
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:30px;">소연아...</div>', unsafe_allow_html=True)
    typewriter("나랑 평생 행복하게 함께해줄래? 🌹", speed=0.1)
    if st.button("YES! 나도 좋아 💖"): st.session_state.stage = 7; st.rerun()

# [Stage 7] 엔딩
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    show_img("final.jpg")
    st.markdown('<div class="center">사진 속의 메시지를 확인해줘!</div>', unsafe_allow_html=True)
    if st.button("다시 하기"): st.session_state.clear(); st.rerun()
