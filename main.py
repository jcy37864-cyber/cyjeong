import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="scare", page_icon="💀", layout="centered")

# 세션 상태 초기화
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
        width: 100% !important; height: 80px !important; font-size: 22px !important;
        font-weight: bold !important; border-radius: 15px !important;
        border: 3px solid {btn_c} !important;
        background-color: {"#FFF0F0" if is_love else "#1A1A1A"} !important;
        color: {btn_c} !important; margin-bottom: 20px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 35px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(2px, 2px);}} 50% {{transform: translate(-3px, -2px);}} 100% {{transform: translate(2px, 2px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    .status-box {{ padding: 20px; border: 2px solid red; background: #111; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 오디오 함수 =================
def play_audio(file_name):
    if st.session_state.get("current_track") == file_name: return
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            audio_id = f"audio_{random.randint(0, 1000)}"
            st.markdown(f"""
                <audio id="{audio_id}" loop autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mpeg"></audio>
                <script>document.addEventListener('click', function() {{ document.getElementById('{audio_id}').play(); }}, {{ once: true }});</script>
            """, unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    if os.path.exists(file_name): st.image(file_name, use_container_width=True)

# ================= 4. 메인 게임 로직 =================

if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM MALFUNCTION</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0); status_text = st.empty()
            msgs = ["접속 시도...", "보안 파괴...", "성공."]
            for i in range(101):
                time.sleep(0.03); bar.progress(i)
                status_text.markdown(f'<div class="center">{msgs[min(i//35, len(msgs)-1)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True; st.rerun()
    else:
        st.error("⚠️ 접속 승인. 화면 클릭 시 소리가 들립니다.")
        if st.button("💀 어둠 속으로 입장"): st.session_state.stage = 1; st.rerun()

elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">🔪 소연아!! 뒤를 봐!! 🔪</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    st.markdown(f'<div class="center" style="font-size:25px;">거리: <b style="color:red;">{st.session_state.dist}m</b></div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 미친 듯이 질주하기!!"): st.session_state.dist -= 20; st.rerun()
    else:
        if st.button("🚪 다음 통로로 탈출"): st.session_state.stage = 2; st.rerun()

elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 안전할까? 🚪 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        st.error("잡혔다... 놈이 네 뒤에 있어.")
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
        st.write("")
        if st.button("🔦 탈출구 발견! 필사적으로 뛰기 🔦"):
            st.session_state.stage = 2.5; st.rerun()

elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">💀 죽음의 룰렛 💀</div>', unsafe_allow_html=True)
    
    if st.session_state.last_result:
        st.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    
    if not st.session_state.roulette_done:
        if st.button("🎰 룰렛 돌리기 (2연속 성공 필요)"):
            with st.spinner("회전 중..."):
                time.sleep(1)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    st.session_state.last_result = f"🎉 {st.session_state.roulette_score}회 성공! 한 번 더!"
                    if st.session_state.roulette_score >= 2: 
                        st.session_state.roulette_done = True
                        st.session_state.last_result = "🔓 봉인 해제! 이제 나갈 수 있어!"
                else:
                    st.session_state.roulette_score = 0
                    st.session_state.last_result = "💀 [꽝] 다시 시작해!"
                    show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 열린 문으로 기어나가기"):
            st.session_state.stage = 3; st.rerun()

elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:25px;">소연아, 나 정말 믿지?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔪 믿어..."):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("🕯️ 못 믿겠어"): st.rerun()

elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3")
    st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B;">🌹 서프라이즈! 소연아! 🌹</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    if st.button("💝 내 진심을 확인할래?"): st.session_state.stage = 5; st.rerun()

elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">마음을 가득 채워줘! 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
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
        if st.button("🌹 최종 확인 🌹"): st.session_state.stage = 6; st.rerun()

elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:30px;">소연아, 평생 함께해줄래?</div>', unsafe_allow_html=True)
    if st.button("✨ 당연히 YES! ✨"): st.session_state.stage = 7; st.rerun()

elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons(); show_img("final.jpg")
    if st.button("처음으로"): 
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
