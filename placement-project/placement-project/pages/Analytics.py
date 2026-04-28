import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.prediction import load_data

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='rgba(255,255,255,0.8)'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)'),
    margin=dict(l=20, r=20, t=40, b=20),
)

COLOR_PLACED = '#34d399'
COLOR_NOT_PLACED = '#f87171'

def show():
    st.markdown("## 📊 Dataset Analytics")
    st.markdown("<div style='color:rgba(255,255,255,0.6); margin-bottom:24px;'>Explore insights from 150,000 student placement records</div>", unsafe_allow_html=True)

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "📈 CGPA Analysis", "🔬 Skills Analysis", "📦 Distributions"])

    # ── TAB 1: Overview ──────────────────────────────────────────────────────
    with tab1:
        st.markdown("#### 📋 Dataset Preview")
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        n_rows = st.slider("Rows to display", 5, 50, 10)
        st.dataframe(
            df.head(n_rows).style.background_gradient(subset=['cgpa'], cmap='Purples')
                                  .background_gradient(subset=['placement'], cmap='RdYlGn'),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            # Pie chart – Placed vs Not Placed
            placed_counts = df['placement'].value_counts().reset_index()
            placed_counts.columns = ['Status', 'Count']
            placed_counts['Status'] = placed_counts['Status'].map({1: 'Placed ✅', 0: 'Not Placed ❌'})
            fig = px.pie(placed_counts, values='Count', names='Status',
                         color_discrete_sequence=[COLOR_PLACED, COLOR_NOT_PLACED],
                         hole=0.5, title='Placement Distribution')
            fig.update_layout(**PLOTLY_LAYOUT)
            fig.update_traces(textinfo='percent+label', textfont_color='white')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with c2:
            # Basic statistics
            st.markdown("**📊 Dataset Statistics**")
            stats = df[['cgpa','aptitude_score','technical_score','communication_score',
                         'internships','projects','certifications','backlogs']].describe().round(2)
            st.dataframe(stats, use_container_width=True)

    # ── TAB 2: CGPA Analysis ─────────────────────────────────────────────────
    with tab2:
        st.markdown("#### 📈 CGPA vs Placement")
        df['Placement Status'] = df['placement'].map({1: 'Placed ✅', 0: 'Not Placed ❌'})

        # CGPA distribution by placement
        fig = px.histogram(
            df, x='cgpa', color='Placement Status',
            nbins=50, barmode='overlay', opacity=0.75,
            color_discrete_map={'Placed ✅': COLOR_PLACED, 'Not Placed ❌': COLOR_NOT_PLACED},
            title='CGPA Distribution by Placement Status',
            labels={'cgpa': 'CGPA', 'count': 'Number of Students'}
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # CGPA bins analysis
        st.markdown("<br>", unsafe_allow_html=True)
        df['cgpa_bin'] = pd.cut(df['cgpa'], bins=[0,5,6,7,8,9,10], labels=['<5','5-6','6-7','7-8','8-9','9-10'])
        cgpa_group = df.groupby('cgpa_bin')['placement'].agg(['mean','count']).reset_index()
        cgpa_group.columns = ['CGPA Range', 'Placement Rate', 'Count']
        cgpa_group['Placement Rate %'] = (cgpa_group['Placement Rate'] * 100).round(1)

        fig2 = px.bar(cgpa_group, x='CGPA Range', y='Placement Rate %',
                      color='Placement Rate %',
                      color_continuous_scale=['#f87171','#f59e0b','#34d399'],
                      title='Placement Rate by CGPA Range',
                      text='Placement Rate %')
        fig2.update_traces(texttemplate='%{text}%', textposition='outside', textfont_color='white')
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        # Box plot
        fig3 = px.box(df, x='Placement Status', y='cgpa',
                      color='Placement Status',
                      color_discrete_map={'Placed ✅': COLOR_PLACED, 'Not Placed ❌': COLOR_NOT_PLACED},
                      title='CGPA Box Plot by Placement Status')
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    # ── TAB 3: Skills Analysis ───────────────────────────────────────────────
    with tab3:
        st.markdown("#### 🔬 Skills vs Placement")
        skill_cols = ['aptitude_score', 'technical_score', 'communication_score']
        skill_labels = ['Aptitude Score', 'Technical Score', 'Communication Score']

        c1, c2 = st.columns(2)
        skill_data = df.groupby('placement')[skill_cols].mean().reset_index()
        skill_data['placement'] = skill_data['placement'].map({1: 'Placed ✅', 0: 'Not Placed ❌'})

        fig = go.Figure()
        colors_bar = [COLOR_PLACED, COLOR_NOT_PLACED]
        for i, row in skill_data.iterrows():
            fig.add_trace(go.Bar(
                name=row['placement'],
                x=skill_labels,
                y=[row['aptitude_score'], row['technical_score'], row['communication_score']],
                marker_color=colors_bar[i]
            ))
        fig.update_layout(barmode='group', title='Average Skill Scores by Placement Status', **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Internships vs placement
        internship_data = df.groupby('internships')['placement'].mean().reset_index()
        internship_data['Placement Rate %'] = (internship_data['placement'] * 100).round(1)
        fig2 = px.line(internship_data, x='internships', y='Placement Rate %',
                       markers=True, title='Placement Rate vs Number of Internships',
                       labels={'internships': 'Number of Internships'})
        fig2.update_traces(line=dict(color='#a78bfa', width=3), marker=dict(color='#a78bfa', size=10))
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        # Correlation heatmap
        st.markdown("#### 🔥 Correlation Heatmap")
        corr_df = df[['cgpa','aptitude_score','technical_score','communication_score',
                       'internships','projects','certifications','backlogs','placement']].corr().round(2)
        fig3 = px.imshow(corr_df,
                         color_continuous_scale='RdBu_r',
                         zmin=-1, zmax=1,
                         title='Feature Correlation Matrix',
                         text_auto=True)
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    # ── TAB 4: Distributions ─────────────────────────────────────────────────
    with tab4:
        st.markdown("#### 📦 Feature Distributions")
        feature = st.selectbox("Select feature", ['cgpa','aptitude_score','technical_score',
                                                    'communication_score','internships',
                                                    'projects','certifications','backlogs'])
        fig = px.histogram(df, x=feature, color='Placement Status',
                           nbins=40, barmode='overlay', opacity=0.75,
                           color_discrete_map={'Placed ✅': COLOR_PLACED, 'Not Placed ❌': COLOR_NOT_PLACED},
                           title=f'{feature.replace("_"," ").title()} Distribution')
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Scatter: CGPA vs Technical
        fig2 = px.scatter(df.sample(5000, random_state=42), x='cgpa', y='technical_score',
                          color='Placement Status',
                          color_discrete_map={'Placed ✅': COLOR_PLACED, 'Not Placed ❌': COLOR_NOT_PLACED},
                          opacity=0.5, title='CGPA vs Technical Score (5k sample)',
                          labels={'cgpa': 'CGPA', 'technical_score': 'Technical Score'})
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
