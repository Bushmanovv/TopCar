import streamlit as st
import pandas as pd
from db import get_connection

def apply_custom_styles():
    # Load Orbitron font
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Custom style block
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0B0C10;
            color: #FFFFFF;
            font-family: 'Orbitron', sans-serif;
        }

        .neon-title {
            text-align: center;
            color: #66FCF1;
            font-size: 65px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
            text-shadow: 
                0 0 5px #66FCF1,
                0 0 10px #66FCF1,
                0 0 20px #66FCF1,
                0 0 40px #45A29E,
                0 0 80px #45A29E;
        }

        [data-testid="stSidebar"] {
            background-color: #1F2833;
        }

        .stButton > button {
            background-color: transparent;
            color: #C5C6C7;
            border: 2px solid #66FCF1;
            font-weight: bold;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            justify-content: flex-start;
        }

        .stButton > button:hover {
            background-color: #45A29E;
            color: #0B0C10;
            border: 2px solid #45A29E;
        }

        .stButton > button img {
            width: 18px;
            height: 18px;
            margin-right: 8px;
            vertical-align: middle;
        }

        input, select, textarea {
            background-color: #111111 !important;
            color: #FFFFFF !important;
            font-family: 'Orbitron', sans-serif !important;
        }

        .stTextInput input, 
        .stNumberInput input,
        .stDateInput input,
        .stSlider {
            background-color: #111111 !important;
            color: #FFFFFF !important;
            border: 2px solid #66FCF1 !important;
            border-radius: 10px !important;
            padding: 0.7rem !important;
            box-shadow: 0 0 8px #66FCF1;
        }

        .stSelectbox label,
        .stTextInput label,
        .stNumberInput label,
        .stDateInput label {
            color: #FFFFFF !important;
            font-weight: bold;
        }

        .stDataFrame {
            background-color: #1F2833;
            border-radius: 10px;
            padding: 1rem;
            color: #C5C6C7;
            font-size: 15px;
        }

        .stAlert-success {
            background-color: #45A29E33;
            border-left: 4px solid #45A29E;
            color: #ffffff;
        }

        .stAlert-error, .stAlert-warning {
            background-color: #DC262633;
            border-left: 4px solid #DC2626;
            color: #ffffff;
        }

        /* Selectbox Styling */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #111111;
            border: 2px solid #66FCF1;
            border-radius: 10px;
            box-shadow: 0 0 8px #66FCF1;
        }

        .stSelectbox div[data-baseweb="select"] div[role="combobox"],
        .stSelectbox div[data-baseweb="option"] {
            background-color: #111111;
            color: #FFFFFF;
            border-radius: 10px;
            padding: 0.5rem;
        }

        .stSelectbox div[data-baseweb="option"]:hover {
            background-color: #45A29E;
            color: #0B0C10;
        }

        .stSelectbox div[data-baseweb="select"] svg {
            color: #66FCF1 !important;
        }

        .stSelectbox, .stSelectbox * {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* Slider Styles */
        div[data-testid="stSlider"] {
            width: 100% !important;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }

        div[data-baseweb="slider"] > div:first-child > div {
            height: 16px !important;
            width: 16px !important;
            background-color: #FF3C3C !important;
            border-radius: 50%;
            box-shadow: 0 0 10px #FF3C3C, 0 0 20px #FF3C3C;
        }

        div[data-baseweb="slider"] > div:nth-child(2) {
            background-color: #66FCF1 !important;
            height: 6px !important;
            border-radius: 3px;
            box-shadow: 0 0 5px #66FCF1;
        }

        div[data-baseweb="slider"] > div:nth-child(3) {
            background-color: #222 !important;
            height: 6px !important;
            border-radius: 3px;
        }

        div[data-baseweb="slider"] {
            width: 100% !important;
            display: flex;
            align-items: center;
        }

        </style>
    """, unsafe_allow_html=True)
