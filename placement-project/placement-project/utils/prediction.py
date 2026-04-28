import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc
import streamlit as st
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "stu_placement_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "scaler.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "placement_dataset_150k.csv")

FEATURE_COLS = ['student_id', 'cgpa', 'aptitude_score', 'technical_score',
                'communication_score', 'internships', 'projects', 'certifications', 'backlogs']
INPUT_COLS = ['cgpa', 'aptitude_score', 'technical_score',
              'communication_score', 'internships', 'projects', 'certifications', 'backlogs']

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

@st.cache_resource
def load_scaler():
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    return scaler

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def predict_placement(cgpa, aptitude, technical, communication, internships, projects, certifications, backlogs):
    model = load_model()
    scaler = load_scaler()

    # student_id is included in scaler features, use 0 as placeholder
    input_data = np.array([[0, cgpa, aptitude, technical, communication, internships, projects, certifications, backlogs]])
    input_scaled = scaler.transform(input_data)

    prob = model.predict_proba(input_scaled)[0]
    pred = model.predict(input_scaled)[0]
    return int(pred), float(prob[1])

def get_placement_readiness_score(cgpa, aptitude, technical, communication, internships, projects, certifications, backlogs):
    """Compute a composite readiness score out of 100"""
    score = 0
    score += min(cgpa / 10 * 30, 30)           # CGPA: max 30
    score += min((aptitude / 100) * 15, 15)     # Aptitude: max 15
    score += min((technical / 100) * 20, 20)    # Technical: max 20
    score += min((communication / 100) * 10, 10) # Communication: max 10
    score += min(internships * 5, 10)           # Internships: max 10
    score += min(projects * 2, 8)               # Projects: max 8
    score += min(certifications * 2, 6)         # Certifications: max 6
    score -= min(backlogs * 5, 10)              # Backlogs: penalty max -10
    score = max(0, min(100, score))
    return round(score, 1)

@st.cache_data
def get_model_metrics():
    df = load_data()
    X = df[FEATURE_COLS]
    y = df['placement']

    scaler = load_scaler()
    X_scaled = scaler.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    rf_model = load_model()
    rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
    rf_cm = confusion_matrix(y_test, rf_model.predict(X_test))
    rf_probs = rf_model.predict_proba(X_test)[:,1]
    rf_fpr, rf_tpr, _ = roc_curve(y_test, rf_probs)
    rf_auc = auc(rf_fpr, rf_tpr)

    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_acc = accuracy_score(y_test, lr_model.predict(X_test))
    lr_cm = confusion_matrix(y_test, lr_model.predict(X_test))
    lr_probs = lr_model.predict_proba(X_test)[:,1]
    lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
    lr_auc = auc(lr_fpr, lr_tpr)

    feature_importance = dict(zip(INPUT_COLS, rf_model.feature_importances_[1:]))

    return {
        "rf": {"acc": rf_acc, "cm": rf_cm, "fpr": rf_fpr, "tpr": rf_tpr, "auc": rf_auc},
        "lr": {"acc": lr_acc, "cm": lr_cm, "fpr": lr_fpr, "tpr": lr_tpr, "auc": lr_auc},
        "feature_importance": feature_importance,
        "y_test": y_test,
        "X_test": X_test,
    }

def get_career_suggestions(score, cgpa, technical, communication, internships):
    suggestions = []
    courses = []
    if cgpa < 7.0:
        suggestions.append("📚 Focus on improving your CGPA — it's a key screening criterion.")
        courses.append("Study techniques & academic planning courses on Coursera")
    if technical < 60:
        suggestions.append("💻 Strengthen your technical skills with practice and projects.")
        courses.append("DSA on LeetCode / HackerRank, Web Dev on freeCodeCamp")
    if communication < 60:
        suggestions.append("🗣️ Work on communication — join debate clubs or take public speaking courses.")
        courses.append("Communication Skills on Coursera by University of Colorado")
    if internships == 0:
        suggestions.append("🏢 Do at least 1–2 internships to build real-world experience.")
        courses.append("Find internships on LinkedIn, Internshala, or Unstop")
    if score >= 75:
        suggestions.append("🎉 You're well-prepared! Polish your resume and start applying.")
        courses.append("Mock interviews on Pramp or InterviewBit")
    return suggestions, courses
