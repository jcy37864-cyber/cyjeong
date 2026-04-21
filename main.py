st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: black !important;
    color: white !important;
}

/* 버튼 */
.stButton>button {
    background-color: black;
    color: red;
    border: 1px solid red;
    font-size: 18px;
}

/* 라디오 */
.stRadio label {
    color: white !important;
}

/* 텍스트 */
.center {text-align: center;}
.big {font-size: 42px; font-weight: bold;}
.scary {color: red; font-size:36px; letter-spacing:3px;}
.cute {font-size:28px; color:pink;}

/* 깜빡임 */
.blink {animation: blinker 0.2s linear infinite;}
@keyframes blinker {50% {opacity: 0;}}

/* 흔들림 */
.shake {animation: shake 0.3s;}
@keyframes shake {
0% { transform: translate(5px, 5px); }
25% { transform: translate(-5px, -5px); }
50% { transform: translate(5px, -5px); }
75% { transform: translate(-5px, 5px); }
100% { transform: translate(0px, 0px); }
}
</style>
""", unsafe_allow_html=True)
