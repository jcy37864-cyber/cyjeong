import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="scare", page_icon="💀", layout="centered")

# 세션 상태 초기화 (AttributeError 방지)
for key, val in {
    "stage": 0, "survive": 0, "fail": 0, "heart": 0,
    "safe_choice": random.randint(0, 2), "heart_choice": random.randint(0, 2),
    "loading_done": False, "trust_count": 0, "roulette_score": 0,
    "roulette_done": False, "dist": 100, "current_track": "", "last_result": ""
}.items():
    if key not in st.session_state: st.session_state[key] = val

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    is_love = st.session_state.stage >= 4
    bg, txt, btn_c = ("#FFFFFF", "#333333", "#FF4B4B") if is_love else ("#000000", "#FF0000", "#8B0000")
    
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 0.5s ease; }}
    div.stButton > button {{
        width: 100% !important; height: 90px !important; font-size: 24px !important;
        font-weight: bold !important; border-radius: 15px !important;
        border: 4px solid {btn_c} !important;
        background-color: {"#FFF0F0" if is_love else "#111111"} !important;
        color: {btn_c} !important; margin-bottom: 20px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 38px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(3px, 3px);}} 50% {{transform: translate(-4px, -3px);}} 100% {{transform: translate(3px, 3px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    .status-box {{ padding: 25px; border: 3px solid red; background: #000; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 22px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 노래 및 🖼️ 이미지 처리 함수 =================
def play_audio(file_name):
    # 노래가 바뀔 때만 새로 렌더링 (이전 노래 유지)
    if st.session_state.get("current_track") == file_name:
        return
    
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            # 고유 ID를 부여하여 오디오 객체 재생
            audio_id = f"audio_{int(time.time())}"
            st.markdown(f"""
                <audio id="{audio_id}" loop autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                </audio>
                <script>
                    var audio = document.getElementById('{audio_id}');
                    audio.volume = 0.5;
                    document.addEventListener('click', function() {{ audio.play(); }}, {{ once: true }});
                </script>
            """, unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    """이미지 출력 보장: 파일이 없으면 경고 메시지 출력"""
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)
    else:
        st.error(f"🖼️ [이미지 유실] '{file_name}' 파일이 폴더에 없습니다!")

# ================= 4. 메인 게임 로직 =================

# [Stage 0] 로딩 (시간 2배 증가)
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM BREACH IN PROGRESS</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0)
            status_text = st.empty()
            # 로딩 멘트
            msgs = ["영혼의 주파수 맞추는 중...", "어둠의 경로 탐색 중...", "보안 필터 파괴 중...", "이소연 데이터 복원 중...", "성공."]
            for i in range(101):
                time.sleep(0.08) # 기존 0.04에서 0.08로 2배 증가!
                bar.progress(i)
                idx = min(i // 20, len(msgs)-1)
                status_text.markdown(f'<div class="center" style="color:gray;">{msgs[idx]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.error("⚠️ 데이터 복원 완료. 화면을 클릭해야 소리가 들립니다.")
        if st.button("💀 어둠의 심연으로 입장"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 도망쳐!
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">🔪 소연아!! 뒤를 봐!! 🔪</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    st.markdown(f'<div class="center" style="font-size:25px;">놈과의 거리: <b style="color:red;">{st.session_state.dist}m</b></div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 숨이 멎을 때까지 달리기!!"):
            st.session_state.dist -= 20
            st.rerun()
    else:
        if st.button("🚪 필사적으로 다음 방으로 탈출"):
            st.session_state.stage = 2
            st.rerun()

# [Stage 2] 문 선택
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 당신을 살릴까? 🚪 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        st.error("💀 잡혔다. 소름 끼치는 웃음소리가 들립니다.")
        if st.button("🩸 생명을 구걸하고 다시 도전"):
            st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    elif st.session_state.survive < 3:
        if random.random() > 0.8: show_img("scary2.jpg")
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                if st.button(f"👁️ 문 {i+1}", key=f"door_{i}"):
                    if i == st.session_state.safe_choice: st.session_state.survive += 1
                    else: st.session_state.fail += 1
                    st.session_state.safe_choice = random.randint(0, 2); st.rerun()
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🎉 탈출구가 보입니다!")
        if st.button("🔦 황금빛 탈출구로 필사적으로 뛰기 🔦"):
            st.session_state.stage = 2.5; st.rerun()

# [Stage 2.5] 죽음의 룰렛
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">💀 죽음의 룰렛 💀</div>', unsafe_allow_html=True)
    
    if st.session_state.last_result:
        st.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    
    if not st.session_state.roulette_done:
        if st.button("🎰 룰렛을 돌려 목숨을 구걸하라 (2연속)"):
            with st.spinner("운명이 소용돌이칩니다..."):
                time.sleep(1.2)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    st.session_state.last_result = f"🎉 {st.session_state.roulette_score}회 통과! 멈추지 마!"
                    if st.session_state.roulette_score >= 2: 
                        st.session_state.roulette_done = True
                        st.session_state.last_result = "🔓 놈의 손아귀에서 벗어났어! 도망쳐!"
                else:
                    st.session_state.roulette_score = 0
                    st.session_state.last_result = "💀 [꽝] 놈이 네 발목을 잡았어!"
                    show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 열린 틈으로 기어나가기"):
            st.session_state.stage = 3; st.rerun()

# [Stage 3] 믿음 테스트
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:28px;">소연아, 여기까지 온 건 우연이 아냐. 날 믿지?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔪 끝까지 믿어..."):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("🕯️ 의심스러워"): st.rerun()

# [Stage 4] 반전 고백
elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3") # 사랑 테마로 자동 전환
    st.balloons()
    st.markdown('<div class="center" style="font-size:38px; color:#FF4B4B; font-weight:bold;">🌹 서프라이즈! 소연아! 🌹</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    if st.button("💖 나의 진심을 확인할래?"):
        st.session_state.stage = 5; st.rerun()

# [Stage 5] 하트 잡기
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px; color:#FF4B4B;">내 마음을 받아줘! 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 10)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2); st.rerun()
            else:
                if st.button("🤍", key=f"e_{i}"): st.session_state.heart_choice = random.randint(0, 2); st.rerun()
    if st.session_state.heart >= 10:
        if st.button("🌹 이제 마지막이야..."): 
            st.session_state.stage = 6; st.rerun()

# [Stage 6~7] 최종 엔딩
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:32px; font-weight:bold;">소연아, 영원히 나랑 함께해줄래?</div>', unsafe_allow_html=True)
    if st.button("✨ 100% YES! ✨"): st.session_state.stage = 7; st.rerun()

elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    show_img("final.jpg")
    st.markdown('<div class="center" style="font-size:25px;">우리의 새로운 시작을 축하해! 💖</div>', unsafe_allow_html=True)
    if st.button("처음으로 돌아가기"): 
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
