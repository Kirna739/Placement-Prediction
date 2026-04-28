import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.prediction import predict_placement, get_placement_readiness_score, get_career_suggestions

def radar_chart(values, labels):
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor='rgba(167,139,250,0.25)',
        line=dict(color='#a78bfa', width=2),
        marker=dict(color='#a78bfa', size=6)
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], color='rgba(255,255,255,0.4)', gridcolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(color='rgba(255,255,255,0.7)', gridcolor='rgba(255,255,255,0.1)')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=320,
    )
    return fig

def gauge_chart(prob):
    color = "#34d399" if prob >= 0.6 else "#f59e0b" if prob >= 0.4 else "#f87171"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number={'suffix': "%", 'font': {'size': 36, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'rgba(255,255,255,0.4)', 'tickfont': {'color': 'rgba(255,255,255,0.6)'}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'bordercolor': 'rgba(255,255,255,0.1)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(248,113,113,0.15)'},
                {'range': [40, 70], 'color': 'rgba(245,158,11,0.15)'},
                {'range': [70, 100], 'color': 'rgba(52,211,153,0.15)'},
            ],
            'threshold': {'line': {'color': color, 'width': 4}, 'thickness': 0.75, 'value': round(prob * 100, 1)}
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=220,
        margin=dict(l=20, r=20, t=20, b=10)
    )
    return fig

def show():
    st.markdown("## 🎯 Placement Prediction")
    st.markdown("<div style='color:rgba(255,255,255,0.6); margin-bottom:24px;'>Fill in your academic profile to get an AI-powered placement prediction</div>", unsafe_allow_html=True)

    # ── Input Form ───────────────────────────────────────────────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Your Academic Profile")

        col1, col2 = st.columns(2)

        with col1:
            cgpa = st.slider("🎓 CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1, help="Your current cumulative GPA out of 10")
            aptitude = st.slider("🧠 Aptitude Score", min_value=0, max_value=100, value=65, help="Logical reasoning & quantitative aptitude (0–100)")
            technical = st.slider("💻 Technical Score", min_value=0, max_value=100, value=60, help="Programming, DSA, technical knowledge (0–100)")
            communication = st.slider("🗣️ Communication Score", min_value=0, max_value=100, value=65, help="Written & verbal communication skills (0–100)")

        with col2:
            internships = st.number_input("🏢 Number of Internships", min_value=0, max_value=10, value=1, help="Total internship experiences")
            projects = st.number_input("🛠️ Number of Projects", min_value=0, max_value=20, value=3, help="Academic or personal projects completed")
            certifications = st.number_input("📜 Number of Certifications", min_value=0, max_value=20, value=2, help="Online or offline course certifications")
            backlogs = st.number_input("⚠️ Number of Backlogs", min_value=0, max_value=10, value=0, help="Current active backlogs/arrears")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Predict Button ───────────────────────────────────────────────────────
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        predict_clicked = st.button("🔮 Predict Placement", use_container_width=True)

    # ── Live readiness score (always visible) ────────────────────────────────
    readiness = get_placement_readiness_score(cgpa, aptitude, technical, communication, internships, projects, certifications, backlogs)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🧭 Placement Readiness Score")
    progress_color = "#34d399" if readiness >= 70 else "#f59e0b" if readiness >= 45 else "#f87171"

    if readiness >= 70:
        badge = "<span class='badge-ready'>🏆 Placement Ready</span>"
    elif readiness >= 45:
        badge = "<span class='badge-improve'>⚡ Needs Improvement</span>"
    else:
        badge = "<span class='badge-risk'>🔴 High Risk</span>"

    st.markdown(f"""
    <div class='glass-card'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
            <div style='font-size:1.5rem; font-weight:800; color:{progress_color};'>{readiness} / 100</div>
            {badge}
        </div>
        <div style='background:rgba(255,255,255,0.1); border-radius:999px; height:12px; overflow:hidden;'>
            <div style='width:{readiness}%; height:100%; background:linear-gradient(90deg, {progress_color}, rgba(167,139,250,0.8)); border-radius:999px; transition:width 0.5s ease;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; margin-top:6px; color:rgba(255,255,255,0.4); font-size:0.75rem;'>
            <span>0 - At Risk</span><span>50 - Average</span><span>100 - Excellent</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Results ──────────────────────────────────────────────────────────────
    if predict_clicked:
        pred, prob = predict_placement(cgpa, aptitude, technical, communication, internships, projects, certifications, backlogs)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔮 Prediction Result")

        r_col1, r_col2 = st.columns([1.2, 1])

        with r_col1:
            if pred == 1:
                st.markdown(f"""
                <div class='result-placed'>
                    <div style='font-size:3.5rem; margin-bottom:10px;'>🎉</div>
                    <div style='font-size:1.8rem; font-weight:800; color:#34d399;'>PLACED!</div>
                    <div style='color:rgba(255,255,255,0.8); margin-top:8px; font-size:1.05rem;'>
                        You have a <strong style='color:#34d399; font-size:1.3rem;'>{round(prob*100,1)}%</strong> chance of getting placed
                    </div>
                    <div style='margin-top:16px; color:rgba(255,255,255,0.5); font-size:0.85rem;'>
                        Great job! Your profile looks competitive. Keep refining your skills.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-not-placed'>
                    <div style='font-size:3.5rem; margin-bottom:10px;'>💪</div>
                    <div style='font-size:1.8rem; font-weight:800; color:#f87171;'>NOT PLACED</div>
                    <div style='color:rgba(255,255,255,0.8); margin-top:8px; font-size:1.05rem;'>
                        You have a <strong style='color:#f87171; font-size:1.3rem;'>{round(prob*100,1)}%</strong> chance of getting placed
                    </div>
                    <div style='margin-top:16px; color:rgba(255,255,255,0.5); font-size:0.85rem;'>
                        Don't give up! Focus on the improvement areas below to boost your chances.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with r_col2:
            st.markdown("**Placement Probability**")
            st.plotly_chart(gauge_chart(prob), use_container_width=True, config={'displayModeBar': False})

        # Skill Radar
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Skill Radar Chart")

        radar_vals = [
            min(cgpa / 10 * 100, 100),
            aptitude,
            technical,
            communication,
            min(internships / 5 * 100, 100),
            min(projects / 10 * 100, 100),
            min(certifications / 8 * 100, 100),
        ]
        radar_labels = ["CGPA", "Aptitude", "Technical", "Communication", "Internships", "Projects", "Certifications"]

        rc1, rc2 = st.columns([1, 1])
        with rc1:
            st.plotly_chart(radar_chart(radar_vals, radar_labels), use_container_width=True, config={'displayModeBar': False})

        with rc2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("**📊 Score Breakdown**")
            for label, val in zip(radar_labels, radar_vals):
                color = "#34d399" if val >= 70 else "#f59e0b" if val >= 45 else "#f87171"
                st.markdown(f"""
                <div style='margin:8px 0;'>
                    <div style='display:flex; justify-content:space-between; color:rgba(255,255,255,0.85); font-size:0.85rem; margin-bottom:3px;'>
                        <span>{label}</span><span style='color:{color}; font-weight:600;'>{round(val)}%</span>
                    </div>
                    <div style='background:rgba(255,255,255,0.1); border-radius:999px; height:6px;'>
                        <div style='width:{val}%; height:100%; background:{color}; border-radius:999px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Career Suggestions
        suggestions, courses = get_career_suggestions(readiness, cgpa, technical, communication, internships)
        if suggestions:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 💡 Career Suggestions")
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("**📌 Action Items**")
                for s in suggestions:
                    st.markdown(f"<div style='color:rgba(255,255,255,0.8); margin:6px 0; font-size:0.88rem;'>{s}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with sc2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("**📚 Recommended Resources**")
                for c in courses:
                    st.markdown(f"<div style='color:rgba(167,139,250,0.9); margin:6px 0; font-size:0.88rem;'>🔗 {c}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # Feedback
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("**💬 Was this prediction helpful?**")
        fb_col1, fb_col2, fb_col3, _ = st.columns([1,1,1,4])
        with fb_col1:
            if st.button("👍 Yes"):
                st.success("Thank you for your feedback!")
        with fb_col2:
            if st.button("👎 No"):
                st.info("We'll work to improve. Thanks!")
        with fb_col3:
            if st.button("🤔 Maybe"):
                st.info("Noted! Keep working on your profile.")
        st.markdown("</div>", unsafe_allow_html=True)
