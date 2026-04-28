import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.prediction import load_data

def show():
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div style='font-size:4rem; margin-bottom:10px;'>🎓</div>
        <div class='hero-title'>AI Placement Predictor</div>
        <div class='hero-subtitle'>Machine Learning-powered career readiness assessment for students</div>
        <div style='color:rgba(255,255,255,0.5); font-size:0.9rem; margin-top:8px;'>
            Trained on 150,000 student records · Random Forest Classifier · Real-time predictions
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats Row
    df = load_data()
    total = len(df)
    placed = df['placement'].sum()
    not_placed = total - placed
    placement_rate = round(placed / total * 100, 1)
    avg_cgpa = round(df['cgpa'].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("👥", f"{total:,}", "Total Students"),
        ("✅", f"{placed:,}", "Placed Students"),
        (f"📈", f"{placement_rate}%", "Placement Rate"),
        ("🎓", f"{avg_cgpa}", "Avg. CGPA"),
    ]
    for col, (icon, val, label) in zip([col1,col2,col3,col4], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-size:1.8rem; font-weight:800; color:white; margin:6px 0;'>{val}</div>
                <div style='font-size:0.85rem; color:rgba(255,255,255,0.6);'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features Section
    st.markdown("### 🚀 What Can You Do Here?")
    col1, col2, col3 = st.columns(3)

    features = [
        ("🎯", "Predict Placement", "Enter your academic profile and get instant AI-powered placement prediction with probability score."),
        ("📊", "Explore Analytics", "Visualize dataset insights — CGPA trends, skill distributions, salary correlations and more."),
        ("📈", "Model Performance", "Compare Logistic Regression vs Random Forest, view confusion matrix, ROC curve & feature importance."),
    ]

    for col, (icon, title, desc) in zip([col1,col2,col3], features):
        with col:
            st.markdown(f"""
            <div class='glass-card' style='height:180px;'>
                <div style='font-size:2rem; margin-bottom:10px;'>{icon}</div>
                <div style='font-size:1.05rem; font-weight:700; color:white; margin-bottom:8px;'>{title}</div>
                <div style='font-size:0.85rem; color:rgba(255,255,255,0.65); line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick guide
    st.markdown("### 📋 How It Works")
    steps = [
        ("1️⃣", "Enter your profile", "Fill in your CGPA, aptitude scores, technical skills, internships, and more."),
        ("2️⃣", "AI analyzes data", "Our Random Forest model (trained on 150k records) processes your inputs instantly."),
        ("3️⃣", "Get your result", "See your placement prediction, probability score, readiness badge, and career tips."),
    ]
    cols = st.columns(3)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size:2rem; margin-bottom:8px;'>{num}</div>
                <div style='font-size:1rem; font-weight:600; color:white; margin-bottom:6px;'>{title}</div>
                <div style='font-size:0.84rem; color:rgba(255,255,255,0.6); line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;'>
        <div style='color:rgba(255,255,255,0.4); font-size:0.8rem;'>
            ⚡ Navigate to <b style='color:#a78bfa;'>Predict Placement</b> from the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)
