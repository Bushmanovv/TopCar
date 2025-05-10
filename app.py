import streamlit as st
from pathlib import Path
import base64
from tables import (
    CarTable, SupplierTable, BranchTable,
    EmployeeTable, CustomerTable,
    SalaryReportTable, SellsTable
)
from style import apply_custom_styles

def render_dashboard():
    apply_custom_styles()

    # ---------- Session State ----------
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "entity" not in st.session_state:
        st.session_state.entity = None
    if "action" not in st.session_state:
        st.session_state.action = None

    for btn_key in ["insert_btn", "view_btn", "update_btn", "delete_btn", "back_btn"]:
        if btn_key not in st.session_state:
            st.session_state[btn_key] = False

    # ---------- Unified Icon Button Function ----------
    def icon_button(label, icon_path, key, action=None, back=False):
        with open(icon_path, "rb") as img_file:
            b64_icon = base64.b64encode(img_file.read()).decode()

        st.markdown(f"""
            <style>
            .stButton > button {{
                display: flex;
                align-items: center;
                gap: 10px;
                justify-content: flex-start;
                background-color: transparent;
                color: #C5C6C7;
                border: 2px solid #66FCF1;
                font-weight: bold;
                letter-spacing: 1px;
                font-family: 'Orbitron', sans-serif;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}
            .stButton > button:hover {{
                background-color: #45A29E;
                color: #0B0C10;
                border: 2px solid #45A29E;
            }}
            </style>
        """, unsafe_allow_html=True)

        button_label = f'![](data:image/png;base64,{b64_icon}) {label}'

        if st.button(button_label, key=key):
            if back:
                st.session_state.page = "Home"
                st.session_state.entity = None
                st.session_state.action = None
                st.rerun()
            else:
                st.session_state.action = action

    # ---------- Sidebar Navigation ----------
    with st.sidebar:
        st.title("TopCar Admin")

        if st.session_state.page == "Home":
            options = {
                "Car Table": CarTable,
                "Supplier Table": SupplierTable,
                "Branch Table": BranchTable,
                "Employee Table": EmployeeTable,
                "Customer Table": CustomerTable,
                "Salary Report Table": SalaryReportTable,
                "Sells Table": SellsTable
            }
            for label, cls in options.items():
                if st.button(label):
                    st.session_state.page = label
                    st.session_state.entity = cls()
                    st.session_state.action = None
                    st.rerun()
        else:
            icon_button("Back to Tables", "assets/back.png", "back_btn", back=True)
            st.markdown("---")
            icon_button("Insert", "assets/insert.png", "insert_btn", "insert")
            icon_button("View", "assets/view.png", "view_btn", "view")
            icon_button("Update", "assets/update.png", "update_btn", "update")
            icon_button("Delete", "assets/delete.png", "delete_btn", "delete")

    # ---------- Main Content ----------
    if st.session_state.page == "Home":
        st.markdown("<div class='neon-title'>Welcome to TopCar Admin Dashboard</div>", unsafe_allow_html=True)
        st.markdown("""
            Use the sidebar to select any table. After selecting one,
            you'll be able to insert, view, update, or delete records.
        """)
    elif st.session_state.entity:
        action = st.session_state.get("action")
        if action == "insert":
            st.session_state.entity.insert_form()
        elif action == "view":
            st.session_state.entity.view_records()
        elif action == "update":
            st.session_state.entity.update_record()
        elif action == "delete":
            st.session_state.entity.delete_record()
        else:
            st.markdown("<div class='neon-title'>Select an action from the sidebar</div>", unsafe_allow_html=True)
