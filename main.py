import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# 세션 변수 초기화
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
        "roulette_score": 0,
        "roulette_done": False,
        "dist": 100,
        "current_track": None  # 현재 재생 중인 노래 추적
    })

# ================= 2. 🎨 디자인 및 애니메이션 테마 =================
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

# ================= 3. 🎵 오디오 제어 (중복 및 끊김 방지) =================
def play_audio(file_name):
    # 이미 해당 곡이 재생 중이라면 다시 실행하지 않음 (끊김 방지 핵심)
    if st.session_state.current_track == file_name:
        return 
    
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.session_state.current_track = file_name
        # 오디오 태그를 화면에 출력 (고정된 위치 없이 호출 시점에 생성)
        st.markdown(
            f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', 
            unsafe_allow_html=True
        )

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
            msgs = ["보안 우회 중...", "ID 추적 중...", "DB 침투 중...", "최종 승인 중...", "완료."]
            for i in range(101):
                time.sleep(0.06)
                bar.progress(i)
                idx = min(i // 25, len(msgs) - 1)
                status_text.markdown(f'<div class="center" style="color:gray;">{msgs[idx]}</div>', unsafe_allow_html=True)
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

# [Stage 2] 문 선택 (3회)
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
            st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    if st.session_state.survive >= 3:
        if st.button("탈출구 발견!"):
            st.session_state.stage = 2.5; st.rerun()

# [Stage 2.5] 강화된 룰렛 (2회 성공)
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
            st.session_state.stage = 3; st.rerun()

# [Stage 3] 믿음 테스트
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    show_img("scary.jpg")
    msgs = ["소연아, 나 믿어?", "진짜 믿어?", "내 손 잡을 거지?"]
    btns = ["믿는다", "진짜!", "당연하지!"]
    typewriter(msgs[min(st.session_state.trust_count, 2)])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(btns[min(st.session_state.trust_count, 2)]):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("의심스러워"):
            st.error("어둠 속에 고립되었습니다.")
            if st.button("다시 시도"): st.session_state.trust_count = 0; st.rerun()

# [Stage 4] 반전 고백
elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3") # 노래 교체 (끊김 없이 바뀜)
    st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B; font-weight:bold;">🎉 소연아! 놀랐지? 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("전부 가짜야! 널 위해 준비한 이벤트지.")
    if st.button("내 진심 확인하기"):
        st.session_state.stage = 5; st.rerun()

# [Stage 5] 하트 잡기 (10개)
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px; color:#FF4B4B;">마음을 잡아줘 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
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
                    st.session_state.heart_choice = random.randint(0, 2); st.rerun()
    if st.session_state.heart >= 10:
        if st.button("진심 확인 ✨"):
            with st.spinner("준비 중..."): time.sleep(2)
            st.session_state.stage = 6; st.rerun()

# [Stage 6~7] 최종 고백 및 엔딩
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    typewriter("소연씨, 나랑 평생 함께해줄래? 🌹", speed=0.1)
    if st.button("YES! 💖"): st.session_state.stage = 7; st.rerun()

elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    show_img("final.jpg")
    if st.button("처음으로"): st.session_state.clear(); st.rerun()
