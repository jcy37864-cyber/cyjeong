import streamlit as st
import time

st.set_page_config(page_title="For You 💖", page_icon="💌")

# 상태 관리
if "stage" not in st.session_state:
    st.session_state.stage = 0

# 공통 스타일
st.markdown("""
    <style>
    .center {text-align: center;}
    .big {font-size: 30px; font-weight: bold;}
    .heart {font-size: 50px; color: red;}
    </style>
""", unsafe_allow_html=True)

# 단계별 연출
if st.session_state.stage == 0:
    st.markdown('<div class="center big">너에게 작은 게임을 준비했어 🎮</div>', unsafe_allow_html=True)
    if st.button("시작하기"):
        st.session_state.stage = 1

elif st.session_state.stage == 1:
    st.markdown('<div class="center">Q1. 우리가 처음 만난 계절은?</div>', unsafe_allow_html=True)
    answer = st.radio("", ["봄", "여름", "가을", "겨울"])

    if st.button("다음"):
        if answer == "봄":
            st.session_state.stage = 2
        else:
            st.warning("힌트: 벚꽃 🌸")

elif st.session_state.stage == 2:
    st.markdown('<div class="center">Q2. 내가 제일 좋아하는 너의 모습은?</div>', unsafe_allow_html=True)
    answer = st.radio("", ["웃는 모습", "화난 모습", "졸린 모습"])

    if st.button("다음"):
        if answer == "웃는 모습":
            st.session_state.stage = 3
        else:
            st.warning("다시 생각해봐 😊")

elif st.session_state.stage == 3:
    st.markdown('<div class="center big">마지막 질문이야...</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="center">나와 함께한 시간, 어땠어?</div>', unsafe_allow_html=True)
    answer = st.radio("", ["행복했어", "그럭저럭", "별로야"])

    if st.button("결과 보기"):
        if answer == "행복했어":
            st.session_state.stage = 4
        else:
            st.session_state.stage = 4

elif st.session_state.stage == 4:
    st.markdown('<div class="center heart">❤️</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="center big">사실 이건 고백이야</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="center">너를 정말 좋아해.</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.markdown('<div class="center">앞으로도 나와 함께해줄래?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES 💖"):
            st.balloons()
            st.success("정말 고마워... 평생 잘할게 💍")
    with col2:
        if st.button("NO 😢"):
            st.warning("다시 생각해줄래...? 🥺")

# 하단 메시지
st.markdown('<div class="center">Made with ❤️</div>', unsafe_allow_html=True)
