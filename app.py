
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(
    page_title="FitLife | Online Fitness Platform",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #f7f9fc;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.hero {
    padding: 2.2rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #111827 0%, #243b53 55%, #1f6f5b 100%);
    color: white;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
    font-weight: 800;
}
.hero p {
    font-size: 17px;
    opacity: .9;
    max-width: 720px;
}
.card {
    background: white;
    border: 1px solid #e7ebf0;
    border-radius: 18px;
    padding: 1.15rem;
    box-shadow: 0 5px 18px rgba(15, 23, 42, .05);
    height: 100%;
}
.metric-card {
    background: white;
    border: 1px solid #e7ebf0;
    border-radius: 18px;
    padding: 1rem 1.1rem;
}
.metric-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}
.metric-value {
    color: #111827;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}
.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #e7f6ef;
    color: #177245;
    font-size: 12px;
    font-weight: 700;
}
.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #111827;
    margin: 1.3rem 0 .8rem;
}
.small {
    color: #64748b;
    font-size: 14px;
}
.exercise {
    background: #fff;
    border: 1px solid #e7ebf0;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
}
.exercise b {
    font-size: 16px;
}
.quote {
    border-left: 4px solid #1f6f5b;
    background: #eef8f4;
    padding: 13px 17px;
    border-radius: 8px;
    color: #27483d;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
workouts = {
    "Full Body Beginner": [
        ("Bodyweight Squats", "3 sets × 12 reps", "Legs • Beginner"),
        ("Push-ups", "3 sets × 8–12 reps", "Chest • Beginner"),
        ("Glute Bridges", "3 sets × 15 reps", "Glutes • Beginner"),
        ("Plank", "3 × 30 seconds", "Core • Beginner"),
        ("Jumping Jacks", "3 × 30 seconds", "Cardio • Beginner"),
    ],
    "Fat Burn": [
        ("Jumping Jacks", "4 × 45 seconds", "Cardio"),
        ("Mountain Climbers", "4 × 30 seconds", "Cardio • Core"),
        ("Bodyweight Squats", "4 × 15 reps", "Legs"),
        ("High Knees", "4 × 30 seconds", "Cardio"),
        ("Burpees", "3 × 10 reps", "Full Body"),
    ],
    "Strength Builder": [
        ("Push-ups", "4 × 10 reps", "Chest • Triceps"),
        ("Lunges", "4 × 10 each leg", "Legs"),
        ("Pike Push-ups", "3 × 8 reps", "Shoulders"),
        ("Glute Bridges", "4 × 15 reps", "Glutes"),
        ("Plank", "3 × 45 seconds", "Core"),
    ],
    "Core & Flexibility": [
        ("Plank", "3 × 45 seconds", "Core"),
        ("Bicycle Crunches", "3 × 15 each side", "Core"),
        ("Bird Dog", "3 × 12 each side", "Core"),
        ("Cat-Cow Stretch", "3 × 30 seconds", "Mobility"),
        ("Child's Pose", "3 × 30 seconds", "Flexibility"),
    ],
}

exercises = pd.DataFrame([
    ["Bodyweight Squats", "Legs", "Beginner", "3 × 12", "Build lower-body strength"],
    ["Push-ups", "Chest", "Beginner", "3 × 8–12", "Strengthen chest and triceps"],
    ["Plank", "Core", "Beginner", "3 × 30–45 sec", "Improve core stability"],
    ["Lunges", "Legs", "Intermediate", "3 × 10/leg", "Improve leg strength and balance"],
    ["Mountain Climbers", "Cardio", "Intermediate", "3 × 30 sec", "Increase heart rate and conditioning"],
    ["Burpees", "Full Body", "Advanced", "3 × 10", "Full-body conditioning"],
    ["Glute Bridges", "Glutes", "Beginner", "3 × 15", "Activate glutes and posterior chain"],
    ["Bicycle Crunches", "Core", "Intermediate", "3 × 15/side", "Train abdominal muscles"],
], columns=["Exercise", "Category", "Level", "Suggested Sets", "Purpose"])

if "completed" not in st.session_state:
    st.session_state.completed = 0
if "weight" not in st.session_state:
    st.session_state.weight = 70.0
if "progress" not in st.session_state:
    st.session_state.progress = [72, 71.4, 70.8, 70.5, 70.0]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 💪 FitLife")
    st.caption("Online Fitness Platform")
    st.divider()
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🏋️ Workouts", "📚 Exercise Library",
         "📈 Progress", "🧮 Fitness Calculator", "👤 Profile"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("**Today's Goal**")
    st.progress(min(st.session_state.completed / 5, 1.0))
    st.caption(f"{st.session_state.completed}/5 exercises completed")

# ---------- Dashboard ----------
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>Train smarter. Feel stronger. 💪</h1>
        <p>Build healthy habits with guided workouts, simple fitness tracking,
        progress insights and personalized tools — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("🔥 Current Streak", "7 days"),
        ("🏋️ Workouts", "18"),
        ("⏱️ Minutes", "425"),
        ("🎯 Weekly Goal", "80%"),
    ]
    for col, (label, value) in zip([c1,c2,c3,c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recommended for you</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    cards = [
        ("🔥 Fat Burn", "25 min", "Intermediate", "Boost cardio and burn calories."),
        ("💪 Full Body Beginner", "20 min", "Beginner", "A balanced workout for the whole body."),
        ("🧘 Core & Flexibility", "18 min", "Beginner", "Strengthen your core and improve mobility.")
    ]
    for col, (title, duration, level, desc) in zip([a,b,c], cards):
        with col:
            st.markdown(f"""
            <div class="card">
                <span class="badge">{level}</span>
                <h3>{title}</h3>
                <p class="small">⏱️ {duration}</p>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class=\"section-title\">Today's workout</div>", unsafe_allow_html=True)
    selected = st.selectbox("Choose a plan", list(workouts.keys()))
    for name, reps, info in workouts[selected]:
        st.markdown(f"""
        <div class="exercise">
            <b>{name}</b><br>
            <span class="small">{reps} &nbsp; • &nbsp; {info}</span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("✅ Complete today's workout", type="primary", use_container_width=True):
        st.session_state.completed = min(st.session_state.completed + 1, 5)
        st.success("Great job! Your workout progress has been updated.")

    st.markdown("""
    <div class="quote">
    <b>Today's motivation:</b> Small steps every day create big results. Keep going!
    </div>
    """, unsafe_allow_html=True)

# ---------- Workouts ----------
elif page == "🏋️ Workouts":
    st.title("🏋️ Workout Plans")
    st.caption("Choose a workout based on your current goal and fitness level.")

    plan = st.selectbox("Workout plan", list(workouts.keys()))
    data = workouts[plan]

    st.markdown(f"### {plan}")
    st.write(f"**{len(data)} exercises** • Designed for home training")

    for i, (name, reps, info) in enumerate(data, 1):
        with st.container(border=True):
            x, y = st.columns([3, 2])
            with x:
                st.markdown(f"**{i}. {name}**")
                st.caption(info)
            with y:
                st.write(reps)

    if st.button("🔥 Start Workout", type="primary"):
        st.success(f"{plan} started! Focus on controlled movement and good form.")

# ---------- Exercise Library ----------
elif page == "📚 Exercise Library":
    st.title("📚 Exercise Library")
    st.caption("Search exercises and filter them by category or difficulty.")

    q = st.text_input("🔎 Search exercise", placeholder="e.g. squat, core, cardio")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["All"] + sorted(exercises["Category"].unique()))
    with col2:
        level = st.selectbox("Level", ["All"] + sorted(exercises["Level"].unique()))

    filtered = exercises.copy()
    if q:
        filtered = filtered[filtered["Exercise"].str.contains(q, case=False, na=False)]
    if category != "All":
        filtered = filtered[filtered["Category"] == category]
    if level != "All":
        filtered = filtered[filtered["Level"] == level]

    for _, row in filtered.iterrows():
        st.markdown(f"""
        <div class="exercise">
            <b>{row['Exercise']}</b>
            <span class="badge">{row['Level']}</span>
            <br><span class="small">{row['Category']} • {row['Suggested Sets']}</span>
            <p style="margin-bottom:0;">{row['Purpose']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- Progress ----------
elif page == "📈 Progress":
    st.title("📈 Progress Tracking")
    st.caption("Monitor your fitness journey and celebrate consistency.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Starting Weight", "72 kg")
    with c2:
        st.metric("Current Weight", f"{st.session_state.weight:.1f} kg", "-2.0 kg")
    with c3:
        st.metric("Workouts Completed", "18", "+4")

    weeks = pd.date_range(end=pd.Timestamp.today(), periods=5, freq="W")
    progress_df = pd.DataFrame({"Week": weeks, "Weight (kg)": st.session_state.progress})
    st.line_chart(progress_df.set_index("Week"))

    st.markdown("### Update today's weight")
    new_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0,
                                  value=float(st.session_state.weight), step=0.1)
    if st.button("Save progress"):
        st.session_state.weight = new_weight
        st.session_state.progress[-1] = new_weight
        st.success("Progress saved successfully!")

# ---------- Calculator ----------
elif page == "🧮 Fitness Calculator":
    st.title("🧮 Fitness Calculator")
    st.caption("Use these simple tools to understand your basic fitness numbers.")

    tab1, tab2 = st.tabs(["BMI Calculator", "Daily Calorie Estimate"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            weight = st.number_input("Weight (kg)", 30.0, 250.0, 70.0)
        with c2:
            height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)

        if st.button("Calculate BMI", type="primary"):
            bmi = weight / ((height / 100) ** 2)
            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Healthy range"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obesity range"
            st.metric("Your BMI", f"{bmi:.1f}")
            st.info(f"Category: **{status}**")
            st.caption("BMI is a general screening measure and does not diagnose health conditions.")

    with tab2:
        age = st.number_input("Age", 13, 100, 21)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight2 = st.number_input("Weight (kg)", 30.0, 250.0, 70.0, key="cal_w")
        height2 = st.number_input("Height (cm)", 100.0, 220.0, 170.0, key="cal_h")
        activity = st.selectbox("Activity level",
                                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        if st.button("Estimate Calories", type="primary"):
            if gender == "Male":
                bmr = 10*weight2 + 6.25*height2 - 5*age + 5
            else:
                bmr = 10*weight2 + 6.25*height2 - 5*age - 161
            factors = {"Sedentary":1.2, "Lightly Active":1.375,
                       "Moderately Active":1.55, "Very Active":1.725}
            calories = bmr * factors[activity]
            st.metric("Estimated daily calories", f"{calories:,.0f} kcal")
            st.caption("This is an estimate for general informational use, not medical or nutritional advice.")

# ---------- Profile ----------
elif page == "👤 Profile":
    st.title("👤 My Profile")
    st.caption("Set your fitness preferences.")

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name", "Fitness User")
        age = st.number_input("Age", 13, 100, 21)
        goal = st.selectbox("Primary goal",
                            ["Build Strength", "Lose Weight", "Improve Fitness",
                             "Increase Flexibility", "Stay Active"])
    with c2:
        level = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
        days = st.slider("Workout days per week", 1, 7, 4)
        minutes = st.slider("Preferred workout duration", 10, 90, 30, 5)

    if st.button("Save Profile", type="primary"):
        st.success(f"Profile saved for {name}. Goal: {goal}.")

    st.markdown("### Weekly target")
    st.progress(days / 7)
    st.write(f"Target: **{days} workout days/week**, around **{minutes} minutes/session**.")

st.divider()
st.caption("FitLife • Online Fitness Platform • Built with Python + Streamlit")