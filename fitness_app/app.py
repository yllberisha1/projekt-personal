import streamlit as st
from user import User
from fitness_plan import FitnessPlan
from utils.helpers import load_users, save_users

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

# ── Session state init ────────────────────────────────────────────
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.title("Fitness Coach 💪")

    if st.session_state.current_user is None:
        choice = st.radio("Action", ["Login", "Register"])

        if choice == "Register":
            new_user = st.text_input("Choose username")
            new_pass = st.text_input("Choose password", type="password")
            if st.button("Create Account"):
                if new_user and new_pass and new_user not in st.session_state.users:
                    st.session_state.users[new_user] = User(new_user, new_pass)
                    save_users(st.session_state.users)
                    st.success("Account created! Now login.")
                else:
                    st.error("Username taken or empty fields.")

        else:  # Login
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if username in st.session_state.users:
                    u = st.session_state.users[username]
                    if u.password == password:
                        st.session_state.current_user = u
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Wrong password.")
                else:
                    st.error("User not found.")
    else:
        st.success(f"Logged in as: **{st.session_state.current_user.username}**")
        if st.button("Logout"):
            st.session_state.current_user = None
            st.rerun()

# ── Main content ──────────────────────────────────────────────────
if st.session_state.current_user is None:
    st.title("Welcome to Fitness Coach")
    st.info("Please login or register in the sidebar to continue.")
else:
    user = st.session_state.current_user
    plan = FitnessPlan(user)

    tab_profile, tab_plan = st.tabs(["📋 Profile", "🏋️ My Plan"])

    with tab_profile:
        st.subheader("Your Information")

        col1, col2 = st.columns(2)

        with col1:
            user.age = st.number_input("Age", 14, 90, value=user.age or 25)
            user.gender = st.selectbox("Gender", ["male", "female"], index=0 if user.gender == "male" else 1)
            user.weight = st.number_input("Weight (kg)", 30.0, 200.0, value=user.weight or 70.0)
            user.height = st.number_input("Height (cm)", 120.0, 220.0, value=user.height or 170.0)

        with col2:
            user.goal = st.selectbox("Goal", ["lose", "gain", "maintain"], index=["lose","gain","maintain"].index(user.goal) if user.goal else 0)
            user.diet_type = st.selectbox("Diet type", ["vegetarian", "vegan", "non-vegetarian"],
                                          index=["vegetarian","vegan","non-vegetarian"].index(user.diet_type) if user.diet_type else 0)
            user.activity_level = st.selectbox("Activity level", ["low", "medium", "high"],
                                               index=["low","medium","high"].index(user.activity_level) if user.activity_level else 1)

        if st.button("Save Profile", type="primary"):
            save_users(st.session_state.users)
            st.success("Profile saved!")

    with tab_plan:
        st.subheader("Your Personalized Plan")

        if st.button("Generate / Refresh Plan", type="primary"):
            with st.spinner("Calculating..."):
                bmi = plan.calculate_bmi()
                cals = plan.calculate_calories()

            if bmi and cals:
                st.markdown(f'<div class="metric-card"><h3>BMI</h3><h1>{bmi}</h1></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card"><h3>Daily Calories</h3><h1>{cals}</h1><small>(adjusted for your goal)</small></div>', unsafe_allow_html=True)

                col_w, col_m = st.columns(2)

                with col_w:
                    st.markdown("### Workouts")
                    for item in plan.get_workout_plan():
                        st.markdown(f'<div class="card">{item}</div>', unsafe_allow_html=True)

                with col_m:
                    st.markdown("### Meals & Nutrition")
                    for item in plan.get_meal_plan():
                        st.markdown(f'<div class="card">{item}</div>', unsafe_allow_html=True)

            else:
                st.warning("Please fill all profile fields first.")

st.caption("Educational project • Not medical advice • 2025–2026")