import streamlit as st
import time

st.set_page_config(page_title="For You 💖", page_icon="💌")

# 상태 관리
if "stage" not in st.session_state:
    st.session_state.stage = 0

# 스타일
st.markdown("""
<style>
.center {text-align: center;}
.big {font-size: 32px; font-weight: bold;}
.small {font-size:18px;}
.heart {font-size: 60px; color: red;}
</style>
""", unsafe_allow_html=True)

# 배경음악
st.audio("bgm.mp3", autoplay=True)

# ===== 0단계 =====
if st.session_state.stage == 0:
    st.image("photo1.jpg", use_column_width=True)
    st.markdown('<div class="center big">너를 위한 작은 게임 🎮</div>', unsafe_allow_html=True)
    st.markdown('<div class="center small">끝까지 가면... 비밀이 있어 💖</div>', unsafe_allow_html=True)

    if st.button("시작하기 💌"):
        st.session_state.stage = 1

# ===== 1단계 =====
elif st.session_state.stage == 1:
    st.image("photo2.jpg", use_column_width=True)
    st.markdown('<div class="center">Q1. 우리가 처음 만난 계절은?</div>', unsafe_allow_html=True)

    answer = st.radio("", ["봄 🌸", "여름 🌊", "가을 🍁", "겨울 ❄️"])

    if st.button("다음 👉"):
        if answer == "봄 🌸":
            st.session_state.stage = 2
        else:
            st.warning("힌트: 벚꽃이 있었어 🌸")

# ===== 2단계 (미니게임) =====
elif st.session_state.stage == 2:
    st.markdown('<div class="center big">하트 잡기 게임 💖</div>', unsafe_allow_html=True)
    st.markdown('<div class="center small">3번 잡으면 성공!</div>', unsafe_allow_html=True)

    if "score" not in st.session_state:
        st.session_state.score = 0

    if st.button("💖 잡기"):
        st.session_state.score += 1

    st.markdown(f'<div class="center">점수: {st.session_state.score} / 3</div>', unsafe_allow_html=True)

    if st.session_state.score >= 3:
        st.success("성공! 🎉")
        if st.button("다음으로 👉"):
            st.session_state.stage = 3

# ===== 3단계 =====
elif st.session_state.stage == 3:
    st.image("photo3.jpg", use_column_width=True)
    st.markdown('<div class="center">Q2. 내가 제일 좋아하는 너의 모습은?</div>', unsafe_allow_html=True)

    answer = st.radio("", ["웃는 모습 😊", "화난 모습 😤", "졸린 모습 😪"])

    if st.button("다음 👉"):
        if answer == "웃는 모습 😊":
            st.session_state.stage = 4
        else:
            st.warning("정답은 항상 웃는 모습 😊")

# ===== 4단계 =====
elif st.session_state.stage == 4:
    st.markdown('<div class="center big">마지막이야...</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center">나와 함께한 시간, 어땠어?</div>', unsafe_allow_html=True)
    answer = st.radio("", ["행복했어 💖", "그럭저럭 🙂", "별로야 😢"])

    if st.button("결과 보기 💌"):
        st.session_state.stage = 5

# ===== 5단계 (고백) =====
elif st.session_state.stage == 5:
    st.image("photo4.jpg", use_column_width=True)
    st.markdown('<div class="center heart">❤️</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center big">사실 이건 게임이 아니라...</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center big">내 마음이야</div>', unsafe_allow_html=True)
    time.sleep(1)

    st.markdown('<div class="center">처음 만난 날부터 계속 좋아했어</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">너랑 있는 시간이 제일 행복해</div>', unsafe_allow_html=True)
    st.markdown('<div class="center big">나랑 계속 함께해줄래? 💍</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💖"):
            st.balloons()
            st.success("고마워... 진짜 잘할게 💖")

    with col2:
        if st.button("NO 😢"):
            st.warning("다시 생각해줄래...? 🥺")

# 하단
st.markdown('<div class="center small">Made with ❤️</div>', unsafe_allow_html=True)
