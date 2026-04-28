import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.prediction import get_model_metrics

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='rgba(255,255,255,0.8)'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)'),
    margin=dict(l=20, r=20, t=40, b=20),
)

def show():
    st.markdown("## 📈 Model Performance")
    st.markdown("<div style='color:rgba(255,255,255,0.6); margin-bottom:24px;'>Comparing Random Forest vs Logistic Regression</div>", unsafe_allow_html=True)

    with st.spinner("🔄 Running model evaluation on test set..."):
        metrics = get_model_metrics()

    rf = metrics['rf']
    lr = metrics['lr']
    fi = metrics['feature_importance']

    # ── Accuracy Comparison ──────────────────────────────────────────────────
    st.markdown("#### 🏆 Model Accuracy Comparison")
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🌲 Random Forest", f"{rf['acc']*100:.2f}%", "#34d399"),
        ("📉 Logistic Regression", f"{lr['acc']*100:.2f}%", "#60a5fa"),
        ("🎯 RF AUC Score", f"{rf['auc']:.4f}", "#a78bfa"),
        ("🎯 LR AUC Score", f"{lr['auc']:.4f}", "#f59e0b"),
    ]
    for col, (title, val, color) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:0.82rem; color:rgba(255,255,255,0.55); margin-bottom:6px;'>{title}</div>
                <div style='font-size:2rem; font-weight:800; color:{color};'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # Bar comparison
    st.markdown("<br>", unsafe_allow_html=True)
    fig_acc = go.Figure(go.Bar(
        x=['Random Forest', 'Logistic Regression'],
        y=[rf['acc']*100, lr['acc']*100],
        marker=dict(color=['#34d399', '#60a5fa'], line=dict(width=0)),
        text=[f"{rf['acc']*100:.2f}%", f"{lr['acc']*100:.2f}%"],
        textfont=dict(color='white', size=14),
        textposition='outside',
        width=0.4
    ))
    fig_acc.update_layout(title='Accuracy Comparison', yaxis_range=[0, 105], **PLOTLY_LAYOUT)
    st.plotly_chart(fig_acc, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Confusion Matrices ────────────────────────────────────────────────────
    st.markdown("#### 🔲 Confusion Matrices")
    cm1, cm2 = st.columns(2)

    def cm_fig(cm, title, color):
        labels = ['Not Placed', 'Placed']
        fig = px.imshow(cm, text_auto=True, color_continuous_scale=color,
                        x=labels, y=labels, title=title,
                        labels=dict(x="Predicted", y="Actual", color="Count"))
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_traces(textfont_size=14)
        return fig

    with cm1:
        st.plotly_chart(cm_fig(rf['cm'], '🌲 Random Forest', 'Greens'), use_container_width=True, config={'displayModeBar': False})
    with cm2:
        st.plotly_chart(cm_fig(lr['cm'], '📉 Logistic Regression', 'Blues'), use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── ROC Curves ────────────────────────────────────────────────────────────
    st.markdown("#### 📐 ROC Curves")
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=rf['fpr'], y=rf['tpr'], mode='lines',
                                  name=f'Random Forest (AUC = {rf["auc"]:.4f})',
                                  line=dict(color='#34d399', width=2.5)))
    fig_roc.add_trace(go.Scatter(x=lr['fpr'], y=lr['tpr'], mode='lines',
                                  name=f'Logistic Regression (AUC = {lr["auc"]:.4f})',
                                  line=dict(color='#60a5fa', width=2.5)))
    fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', name='Random Classifier',
                                  line=dict(color='rgba(255,255,255,0.3)', width=1.5, dash='dash')))
    fig_roc.update_layout(
        title='ROC Curves – Random Forest vs Logistic Regression',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_roc, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Feature Importance ────────────────────────────────────────────────────
    st.markdown("#### 📌 Feature Importance (Random Forest)")
    fi_sorted = dict(sorted(fi.items(), key=lambda x: x[1], reverse=True))
    labels = [k.replace('_', ' ').title() for k in fi_sorted.keys()]
    values = [round(v*100, 2) for v in fi_sorted.values()]

    fig_fi = go.Figure(go.Bar(
        x=values, y=labels,
        orientation='h',
        marker=dict(
            color=values,
            colorscale='Purples',
            line=dict(width=0)
        ),
        text=[f"{v}%" for v in values],
        textposition='outside',
        textfont=dict(color='white')
    ))
    fig_fi.update_layout(
        title='Feature Importance — Which factors matter most?',
        xaxis_title='Importance (%)',
        xaxis_range=[0, max(values)+5],
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_fi, use_container_width=True, config={'displayModeBar': False})

    # Importance cards
    st.markdown("**🏅 Top 3 Most Important Features**")
    top3 = list(fi_sorted.items())[:3]
    icons = ["🥇", "🥈", "🥉"]
    cols = st.columns(3)
    for col, icon, (feat, imp) in zip(cols, icons, top3):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-size:1rem; font-weight:700; color:white; margin:6px 0;'>{feat.replace("_"," ").title()}</div>
                <div style='font-size:1.4rem; font-weight:800; color:#a78bfa;'>{imp*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
