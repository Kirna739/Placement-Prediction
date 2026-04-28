import streamlit as st

def show():
    st.markdown("## ℹ️ About This Project")

    st.markdown("""
    <div class='hero-section' style='padding:40px;'>
        <div style='font-size:3rem; margin-bottom:12px;'>🤖</div>
        <div class='hero-title' style='font-size:2.2rem;'>AI Placement Predictor</div>
        <div class='hero-subtitle'>A complete end-to-end Machine Learning project for student placement prediction</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='glass-card'>
            <div style='font-size:1.3rem; font-weight:700; color:white; margin-bottom:16px;'>🧠 ML Model</div>
            <div style='color:rgba(255,255,255,0.75); line-height:1.9; font-size:0.9rem;'>
                <b style='color:#a78bfa;'>Algorithm:</b> Random Forest Classifier<br>
                <b style='color:#a78bfa;'>Training data:</b> 150,000 student records<br>
                <b style='color:#a78bfa;'>Features:</b> CGPA, Aptitude, Technical, Communication, Internships, Projects, Certifications, Backlogs<br>
                <b style='color:#a78bfa;'>Output:</b> Binary placement prediction + probability score<br>
                <b style='color:#a78bfa;'>Comparison:</b> Also evaluated against Logistic Regression
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
            <div style='font-size:1.3rem; font-weight:700; color:white; margin-bottom:16px;'>🛠️ Tech Stack</div>
            <div style='color:rgba(255,255,255,0.75); line-height:1.9; font-size:0.9rem;'>
                <b style='color:#60a5fa;'>Frontend:</b> Streamlit (Python)<br>
                <b style='color:#60a5fa;'>ML:</b> scikit-learn (Random Forest, Logistic Regression)<br>
                <b style='color:#60a5fa;'>Visualizations:</b> Plotly, Matplotlib, Altair<br>
                <b style='color:#60a5fa;'>Data:</b> Pandas, NumPy<br>
                <b style='color:#60a5fa;'>Deployment:</b> Streamlit Cloud / Render / Heroku
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📁 Project Structure")
    st.code("""
placement-project/
│
├── app.py                     ← Main Streamlit app (navigation)
│
├── model/
│   ├── stu_placement_model.pkl  ← Trained Random Forest model
│   └── scaler.pkl               ← StandardScaler for preprocessing
│
├── pages/
│   ├── Home.py                ← Landing page with stats
│   ├── Prediction.py          ← Prediction form + results
│   ├── Analytics.py           ← Dataset visualizations
│   ├── Performance.py         ← Model metrics & comparison
│   └── About.py               ← This page
│
├── utils/
│   └── prediction.py          ← Core ML logic & helper functions
│
├── placement_dataset_150k.csv ← Dataset (150,000 records)
└── requirements.txt           ← Python dependencies
    """, language="bash")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 How to Run Locally")
    st.code("""
# 1. Clone or download the project
cd placement-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
    """, language="bash")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ☁️ Deploy to Streamlit Cloud")
    st.markdown("""
    <div class='glass-card'>
        <ol style='color:rgba(255,255,255,0.8); line-height:2.2; font-size:0.92rem;'>
            <li>Push your project to a <b style='color:#a78bfa;'>GitHub repository</b></li>
            <li>Go to <b style='color:#60a5fa;'>share.streamlit.io</b> and sign in with GitHub</li>
            <li>Click <b>"New app"</b> → select your repo → set <b>app.py</b> as the main file</li>
            <li>Click <b>"Deploy"</b> — your app will be live in minutes! 🎉</li>
        </ol>
        <div style='color:rgba(255,255,255,0.4); font-size:0.8rem; margin-top:8px;'>
            ⚠️ Make sure model .pkl files and dataset are included in the repo or use Git LFS for large files.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:rgba(255,255,255,0.35); font-size:0.8rem;'>
        Built with ❤️ using Streamlit & scikit-learn &nbsp;·&nbsp; AI Placement Predictor v1.0
    </div>
    """, unsafe_allow_html=True)
