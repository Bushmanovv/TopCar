import streamlit as st
import streamlit.components.v1 as components
import json
import base64
from app import render_dashboard

st.set_page_config(page_title="TopCar Admin", layout="wide")

if "entered" not in st.session_state:
    st.session_state.entered = False

with open("assets/landing.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("assets/logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

with open("assets/animation.json", "r") as anim_file:
    animation_data = json.load(anim_file)

if not st.session_state.entered:
    # Logo + Title + Subtitle
    st.markdown(f"""
        <div class="landing-wrapper">
            <img src="data:image/png;base64,{encoded_logo}" class="logo"/>
            <h1 class="title">TopCar Dashboard</h1>
            <p class="subtitle">Manage Cars, Employees, Sales & More — Effortlessly</p>
        </div>
    """, unsafe_allow_html=True)

    # ✅ Styled button using native Streamlit
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Enter Dashboard", key="enter-dashboard"):
        st.session_state.entered = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ Lottie animation
    components.html(f"""
        <div id="bodymovin" class="lottie-box"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.4/lottie.min.js"></script>
        <script>
            var animationData = {json.dumps(animation_data)};
            bodymovin.loadAnimation({{
                container: document.getElementById('bodymovin'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: animationData,
                rendererSettings: {{
                    preserveAspectRatio: 'xMidYMid meet'
                }}
            }});
        </script>
    """, height=300)

else:
    render_dashboard()
