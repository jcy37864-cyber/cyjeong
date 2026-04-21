import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="For Soyeon", page_icon="💖", layout="centered")

# 세션 상태 초기화
for key, val in {
    "stage": 0, "survive": 0, "fail": 0, "heart": 0,
    "safe_choice": random.randint(0, 2), "heart_choice": random.randint(0, 2),
    "loading_done": False, "trust_count": 0, "roulette_score": 0,
    "roulette_done": False, "dist": 100, "current_track": "", "last_result": "",
    "red_thread": random.randint(0, 4)
}.items():
    if key not in st.session_state: st.session_state[key] = val

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    # 4단계(반전) 이후로는 따뜻한 색감으로 변경
    is_love = st.session_state.stage >= 4
    bg, txt, btn_c = ("#FFFFFF", "#333333", "#FF4B4B") if is_love else ("#000000", "#FF0000", "#8B0000")
    
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 1.0s ease; }}
    div.stButton > button {{
        width: 100% !important; height: 85px !important; font-size: 22px !important;
        font-weight: bold !important; border-radius: 15px !important;
        border: 3px solid {btn_c} !important;
        background-color: {"#FFF0F0" if is_love else "#111111"} !important;
        color: {btn_c} !important; margin-bottom: 15px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 38px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(3px, 3px);}} 50% {{transform: translate(-4px, -3px);}} 100% {{transform: translate(3px, 3px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    .letter-box {{ background-color: #FFF0F0; padding: 40px; border-radius: 25px; border: 2px dashed #FF4B4B; color: #333; box-shadow: 0px 10px 20px rgba(0,0,0,0.1); }}
    .status-box {{ padding: 20px; border: 3px solid red; background: #000; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 오디오 & 🖼️ 이미지 함수 =================
def play_audio(file_name):
    if st.session_state.get("current_track") == file_name: return
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            audio_id = f"audio_{int(time.time())}"
            st.markdown(f"""
                <audio id="{audio_id}" loop autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mpeg"></audio>
                <script>document.addEventListener('click', function() {{ document.getElementById('{audio_id}').play(); }}, {{ once: true }});</script>
            """, unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    if os.path.exists(file_name): st.image(file_name, use_container_width=True)
    else: st.error(f"🖼️ [이미지 확인 필요] {file_name} 파일이 없습니다.")

# ================= 4. 게임 메인 로직 =================

# [Stage 0] 로딩 (시간 2배)
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM BREACH</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0); status_text = st.empty()
            msgs = ["접속 우회 중...", "심박수 동기화 중...", "보안 해제 중...", "성공."]
            for i in range(101):
                time.sleep(0.08); bar.progress(i)
                status_text.markdown(f'<div class="center">{msgs[min(i//26, len(msgs)-1)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True; st.rerun()
    else:
        st.error("⚠️ 데이터 복구 완료. 클릭 시 소리가 들립니다.")
        if st.button("💀 어둠의 심연으로 입장"): st.session_state.stage = 1; st.rerun()

# [Stage 1] 추격전
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3"); show_img("scary.jpg")
    st.markdown('<div class="center shake-text">🔪 소연아!! 도망쳐!! 🔪</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="center" style="font-size:25px;">놈과의 거리: {st.session_state.dist}m</div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 숨이 멎을 때까지 달리기!!"): st.session_state.dist -= 20; st.rerun()
    else:
        if st.button("🚪 다음 통로로 탈출"): st.session_state.stage = 2; st.rerun()

# [Stage 2] 문 선택
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 당신을 살릴까? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        if st.button("🩸 재도전하기"):
            st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    elif st.session_state.survive < 3:
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                if st.button(f"👁️ 문 {i+1}", key=f"door_{i}"):
                    if i == st.session_state.safe_choice: st.session_state.survive += 1
                    else: st.session_state.fail += 1
                    st.session_state.safe_choice = random.randint(0, 2); st.rerun()
    else:
        if st.button("🔦 황금빛 탈출구로 필사적으로 뛰기 🔦"): st.session_state.stage = 2.5; st.rerun()

# [Stage 2.5] 룰렛
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">💀 죽음의 룰렛 💀</div>', unsafe_allow_html=True)
    if st.session_state.last_result: st.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    if not st.session_state.roulette_done:
        if st.button("🎰 룰렛을 돌려라 (2연속 성공)"):
            with st.spinner("운명 결정 중..."):
                time.sleep(1.2)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    st.session_state.last_result = f"🎉 {st.session_state.roulette_score}회 통과!"
                    if st.session_state.roulette_score >= 2: st.session_state.roulette_done = True
                else:
                    st.session_state.roulette_score = 0; st.session_state.last_result = "💀 [꽝]"; show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 열린 문으로 기어나가기"): st.session_state.stage = 3; st.rerun()

# [Stage 3] 믿음
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3"); show_img("scary.jpg")
    st.markdown('<div class="center" style="font-size:25px;">소연아, 나 정말 믿지?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔪 믿어..."):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("🕯️ 못 믿겠어"): st.rerun()

# [Stage 4] 반전 (감동 시작)
elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3"); st.balloons()
    st.markdown('<div class="center"
