

import streamlit as st
import requests
import json


API_BASE = "http://localhost:8000"   # Change to your deployed URL later
st.set_page_config(page_title="Fitness Coach", page_icon="💪", layout="wide")


st.markdown("""
    <style>
    .stButton > button {
        background: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
    }
    .card {
        padding: 1.4rem;
        border-radius: 12px;
        background: #1e2538;
        border: 1px solid #2d3748;
        margin: 1rem 0;
    }
    .metric-card {
        background: #1a1f2e;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None


def get_headers():
    return {"Content-Type": "application/json"}


with st.sidebar:
    st.title("Fitness Coach 💪")

    if st.session_state.current_user is None:
        choice = st.radio("Action", ["Login", "Register"])

        if choice == "Register":
            new_username = st.text_input("Choose username")
            new_password = st.text_input("Choose password", type="password")

            if st.button("Create Account"):
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE}/register",
                            json={"username": new_username, "password": new_password},
                            headers=get_headers()
                        )
                        if response.status_code == 200:
                            st.success("Account created! Please login.")
                        else:
                            st.error(response.json().get("detail", "Registration failed."))
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend. Is FastAPI running on port 8000?")

        else:  # Login
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if not username or not password:
                    st.error("Please fill username and password.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE}/login",
                            params={"username": username, "password": password}
                        )
                        if response.status_code == 200:
                            st.session_state.current_user = username
                            # Load user profile right after login
                            profile_resp = requests.get(f"{API_BASE}/user/{username}")
                            if profile_resp.status_code == 200:
                                st.session_state.user_data = profile_resp.json()
                            st.success(f"Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error(response.json().get("detail", "Login failed."))
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend. Start FastAPI first.")

    else:
        st.success(f"Logged in as: **{st.session_state.current_user}**")
        if st.button("Logout"):
            st.session_state.current_user = None
            st.session_state.user_data = None
            st.rerun()

# ── Main content ────────────────────────────────────────────────────────
if st.session_state.current_user is None:
    st.title("Welcome to Fitness Coach")
    st.info("Please login or register in the sidebar to continue.")
    st.caption("Backend should be running → uvicorn api:app --reload --port 8000")
else:
    username = st.session_state.current_user
    user_data = st.session_state.user_data or {}

    tab_profile, tab_plan = st.tabs(["📋 Profile", "🏋️ My Plan"])

    # ── Profile Tab ─────────────────────────────────────────────────────
    with tab_profile:
        st.subheader("Your Information")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 14, 90, value=user_data.get("age") or 25)
            gender = st.selectbox("Gender", ["male", "female"],
                                 index=0 if user_data.get("gender") == "male" else 1)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, value=user_data.get("weight") or 70.0)
            height = st.number_input("Height (cm)", 120.0, 220.0, value=user_data.get("height") or 170.0)

        with col2:
            goal_options = ["lose", "gain", "maintain"]
            goal_index = goal_options.index(user_data.get("goal")) if user_data.get("goal") in goal_options else 0
            goal = st.selectbox("Goal", goal_options, index=goal_index)

            diet_options = ["vegetarian", "vegan", "non-vegetarian"]
            diet_index = diet_options.index(user_data.get("diet_type")) if user_data.get("diet_type") in diet_options else 0
            diet_type = st.selectbox("Diet type", diet_options, index=diet_index)

            activity_options = ["low", "medium", "high"]
            activity_index = activity_options.index(user_data.get("activity_level")) if user_data.get("activity_level") in activity_options else 1
            activity_level = st.selectbox("Activity level", activity_options, index=activity_index)

        if st.button("Save Profile", type="primary"):
            update_payload = {
                "age": age,
                "gender": gender,
                "weight": weight,
                "height": height,
                "goal": goal,
                "diet_type": diet_type,
                "activity_level": activity_level
            }

            try:
                response = requests.put(
                    f"{API_BASE}/user/{username}",
                    json=update_payload,
                    headers=get_headers()
                )
                if response.status_code == 200:
                    st.session_state.user_data = response.json()
                    st.success("Profile saved successfully!")
                else:
                    st.error(response.json().get("detail", "Failed to save profile."))
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is FastAPI running?")

    # ── Plan Tab ────────────────────────────────────────────────────────
    with tab_plan:
        st.subheader("Your Personalized Plan")

        if st.button("Generate / Refresh Plan", type="primary"):
            if not all([user_data.get("age"), user_data.get("weight"), user_data.get("height"),
                        user_data.get("goal"), user_data.get("diet_type"), user_data.get("activity_level")]):
                st.warning("Please complete your profile first (age, weight, height, goal, diet, activity).")
            else:
                with st.spinner("Generating your plan..."):
                    try:
                        response = requests.post(f"{API_BASE}/generate_plan/{username}")
                        if response.status_code == 200:
                            plan_data = response.json()

                            col_metric1, col_metric2 = st.columns(2)
                            with col_metric1:
                                st.markdown(
                                    f'<div class="metric-card"><h3>BMI</h3><h1>{plan_data["bmi"]:.1f}</h1></div>',
                                    unsafe_allow_html=True
                                )
                            with col_metric2:
                                st.markdown(
                                    f'<div class="metric-card"><h3>Daily Calories</h3><h1>{plan_data["daily_calories"]}</h1><small>(goal adjusted)</small></div>',
                                    unsafe_allow_html=True
                                )

                            col_w, col_m = st.columns(2)

                            with col_w:
                                st.markdown("### Workout Recommendations")
                                for item in plan_data["workouts"]:
                                    st.markdown(f'<div class="card">{item}</div>', unsafe_allow_html=True)

                            with col_m:
                                st.markdown("### Nutrition Recommendations")
                                for item in plan_data["meals"]:
                                    st.markdown(f'<div class="card">{item}</div>', unsafe_allow_html=True)

                        else:
                            st.error(response.json().get("detail", "Failed to generate plan."))
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot reach backend server. Make sure FastAPI is running.")

st.caption("Fitness Recommendation System • Educational project • 2026")