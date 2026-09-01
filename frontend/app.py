"""
Streamlit frontend for Role-Level AI Intelligence Platform
MODUS Enterprise AI Build Challenge - Assignment 6
"""
import sys
import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Optional
import json

# Ensure project root is in sys.path for direct imports on Streamlit Cloud
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
backend_dir = os.path.join(ROOT_DIR, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Direct DB and Service Imports for Streamlit Cloud Fallback
from app.db.database import get_db, init_db
from app.repositories import RoleRepository, ResearchSourceRepository
from app.services import RoleAnalysisService, RoleComparisonService, AnalyticsService, RoleCreationService
from app.ai_service import AIService

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Role-Level AI Intelligence Platform | MODUS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern Glassmorphism & High-End Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background & Cards */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    .stApp {
        background-color: #0b0f19;
    }

    /* Button Styling Fix for Dark Mode */
    div.stButton > button {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    div.stButton > button:active {
        background-color: #0369a1 !important;
        color: #ffffff !important;
    }

    /* Primary Accent Button Override */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* Metric Cards */
    .metric-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #38bdf8;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    
    .metric-sub {
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    /* Status Badges */
    .badge-auto {
        background-color: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .badge-aug {
        background-color: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .badge-human {
        background-color: rgba(34, 197, 94, 0.2);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Profile Card */
    .profile-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .profile-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 0.75rem;
    }

    /* Evidence Box */
    .evidence-box {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #38bdf8;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-radius: 0 8px 8px 0;
    }
    
    /* RAG Answer Container */
    .rag-answer-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# ========================
# Helper Functions (API + Standalone Fallback)
# ========================

def get_standalone_db():
    """Ensure DB initialized for standalone Streamlit Cloud execution"""
    init_db()
    return next(get_db())


def fetch_roles():
    """Fetch all roles from API with direct DB fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/roles", timeout=1.5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    roles = RoleRepository.get_all(db)
    return [{"id": r.id, "name": r.name, "department": r.department, "description": r.description} for r in roles]


def fetch_role_detail(role_id: int):
    """Fetch detailed role information with direct service fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/roles/{role_id}", timeout=1.5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return RoleAnalysisService.get_role_detail(db, role_id)


def fetch_role_analysis(role_id: int):
    """Fetch role analysis with direct service fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/roles/{role_id}/analysis", timeout=1.5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return RoleAnalysisService.analyze_role(db, role_id)


def fetch_dashboard_stats():
    """Fetch dashboard statistics with direct service fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard", timeout=1.5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return AnalyticsService.get_dashboard_stats(db)


def fetch_top_ai_impact_roles(limit: int = 5):
    """Fetch top AI impacted roles with direct service fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/top-ai-impact?limit={limit}", timeout=1.5)
        if response.status_code == 200:
            return response.json()["top_roles"]
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return AnalyticsService.get_top_ai_impact_roles(db, limit=limit)


def fetch_research_sources():
    """Fetch research sources with direct repository fallback"""
    try:
        response = requests.get(f"{API_BASE_URL}/research/sources", timeout=1.5)
        if response.status_code == 200:
            return response.json()["sources"]
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    sources = ResearchSourceRepository.get_all(db)
    return [
        {
            "id": s.id, "source_id": s.source_id, "title": s.title,
            "publisher": s.publisher, "url": s.url,
            "publication_date": s.publication_date, "source_type": s.source_type,
            "summary": s.summary, "relevance_score": s.relevance_score
        }
        for s in sources
    ]


def compare_roles_api(role_1_id: int, role_2_id: int):
    """Compare two roles with direct service fallback"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/roles/compare",
            json={"role_1_id": role_1_id, "role_2_id": role_2_id},
            timeout=1.5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return RoleComparisonService.compare_roles(db, role_1_id, role_2_id)


def ask_question_api(question: str, context_role_id: Optional[int] = None):
    """Ask intelligence question with direct AIService fallback"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question, "context_role_id": context_role_id},
            timeout=1.5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    return AIService.answer_question(db, question, context_role_id)


def initialize_seed_data():
    """Initialize database with seed data with direct fallback"""
    try:
        response = requests.post(f"{API_BASE_URL}/seed-data/initialize", timeout=1.5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    from scripts.seed_data import seed_banking_roles
    db = get_standalone_db()
    msg = seed_banking_roles(db)
    return {"status": "success", "message": msg}


def create_new_role_api(role_data: dict):
    """Create new role with direct service fallback"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/roles/new-role/create-and-analyze",
            json=role_data,
            timeout=1.5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Standalone Fallback
    db = get_standalone_db()
    role_name = role_data.get("role_name") or role_data.get("name")
    role_description = role_data.get("role_description") or role_data.get("description", "")
    processes = role_data.get("processes", [])
    
    return RoleCreationService.create_role_with_analysis(
        db=db,
        industry_id=role_data.get("industry_id", 1),
        role_name=role_name,
        role_description=role_description,
        processes_data=processes,
        department=role_data.get("department"),
        current_responsibilities=role_data.get("current_responsibilities"),
        skills_data=role_data.get("skills")
    )


# ========================
# Page: Executive Dashboard
# ========================

def page_dashboard():
    """Executive dashboard view"""
    st.title("📊 Executive AI Intelligence Dashboard")
    st.caption("Banking & Financial Services Industry Intelligence")
    
    stats = fetch_dashboard_stats()
    
    # Auto seed if empty
    if not stats or not stats.get("summary") or stats.get("summary", {}).get("total_roles", 0) == 0:
        st.warning("Database contains no initialized roles. Click below to seed 20 representative banking roles.")
        if st.button("🚀 Initialize Banking Intelligence Database", type="primary"):
            with st.spinner("Seeding 20 banking roles, activity impact matrices, and research evidence..."):
                res = initialize_seed_data()
                if res:
                    st.success("Successfully seeded database!")
                    st.rerun()
        return

    summary = stats.get("summary", {})
    
    # Top KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Representative Roles</div>
            <div class="metric-value">{summary.get('total_roles', 0)}</div>
            <div class="metric-sub">Banking & Capital Markets</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Banking Processes</div>
            <div class="metric-value">{summary.get('total_processes', 0)}</div>
            <div class="metric-sub">Core Operational Workflows</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Activities Analyzed</div>
            <div class="metric-value">{summary.get('total_activities', 0)}</div>
            <div class="metric-sub">Scored on 0–100 Scale</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        avg_exp = summary.get("average_ai_exposure", 0) * 100
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Average AI Exposure</div>
            <div class="metric-value">{avg_exp:.1f}%</div>
            <div class="metric-sub">Weighted Task Exposure</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Visualizations Section
    col_chart, col_skills = st.columns([3, 2])
    
    with col_chart:
        st.subheader("🔥 Top 5 AI-Impacted Banking Roles")
        top_roles = stats.get("top_ai_impacted_roles", [])
        if top_roles:
            roles_df = pd.DataFrame([
                {
                    "Role": r["role"]["name"],
                    "AI Exposure Score (%)": round(r["ai_impact_score"] * 100, 1),
                    "Affected Activities": r["affected_activities"]
                }
                for r in top_roles
            ])
            
            fig = px.bar(
                roles_df, 
                x="AI Exposure Score (%)", 
                y="Role", 
                orientation="h",
                color="AI Exposure Score (%)",
                color_continuous_scale="Reds",
                text="AI Exposure Score (%)"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                yaxis=dict(autorange="reversed"),
                margin=dict(l=0, r=20, t=20, b=20)
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

    with col_skills:
        st.subheader("💡 Key Future Skills in Demand")
        future_skills = stats.get("future_skills", [])
        if future_skills:
            for skill in future_skills[:8]:
                st.info(f"✨ **{skill}**")
        else:
            st.write("• AI Prompt Engineering\n• AI Model Oversight\n• Critical Thinking\n• Strategic Decision Making")

    # Research Sources Quick View
    st.divider()
    st.subheader("📚 Verified Research Evidence Layer")
    sources = fetch_research_sources()
    if sources:
        sc1, sc2, sc3 = st.columns(3)
        for idx, src in enumerate(sources[:3]):
            col = [sc1, sc2, sc3][idx % 3]
            with col:
                st.markdown(f"""
                <div class="evidence-box">
                    <div style="font-weight:700; color:#38bdf8;">{src['title']}</div>
                    <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:6px;">{src['publisher']} • {src['publication_date']}</div>
                    <div style="font-size:0.85rem;">{src['summary'][:130]}...</div>
                    <a href="{src['url']}" target="_blank" style="color:#60a5fa; font-size:0.8rem;">Read Source ↗</a>
                </div>
                """, unsafe_allow_html=True)


# ========================
# Page: Role Explorer
# ========================

def page_role_explorer():
    """Browse and explore roles"""
    st.title("🔍 Role Explorer")
    st.caption("Inspect processes, activities, current skills, and baseline metrics across all banking roles")

    roles = fetch_roles()
    if not roles:
        st.warning("No roles found in database. Please seed the database first.")
        if st.button("🚀 Initialize Banking Intelligence Database", type="primary"):
            res = initialize_seed_data()
            if res:
                st.success("Successfully seeded database!")
                st.rerun()
        return

    # Filter controls
    col_sel, col_info = st.columns([2, 3])
    
    with col_sel:
        selected_role_id = st.selectbox(
            "Select a role to inspect:",
            options=[r["id"] for r in roles],
            format_func=lambda x: next(r["name"] for r in roles if r["id"] == x)
        )

    if selected_role_id:
        role_detail = fetch_role_detail(selected_role_id)
        if role_detail:
            with col_info:
                st.markdown(f"### 📌 {role_detail['name']}")
                st.markdown(f"**Department:** `{role_detail.get('department', 'Banking Operations')}`")
                st.write(role_detail.get("description", ""))
                st.caption(f"**Current Responsibilities:** {role_detail.get('current_responsibilities', 'N/A')}")

            st.divider()

            # Processes & Activities Table
            st.subheader("📋 Processes & Activity Inventory")
            processes = role_detail.get("processes", [])
            for proc in processes:
                with st.expander(f"📂 Process: **{proc['name']}** ({len(proc.get('activities', []))} activities)", expanded=True):
                    st.write(f"*{proc.get('description', '')}*")
                    
                    act_list = proc.get("activities", [])
                    if act_list:
                        act_df = pd.DataFrame([
                            {
                                "Activity Name": a["name"],
                                "Description": a["description"],
                                "AI Exposure Score (%)": a["ai_exposure_score"],
                                "Automation Potential (%)": a["automation_potential"],
                                "Augmentation Potential (%)": a["augmentation_potential"],
                                "Category": a.get("impact_category", "AI Augmented")
                            }
                            for a in act_list
                        ])
                        st.dataframe(act_df, use_container_width=True)


# ========================
# Page: Role Analysis (MAIN DEMO)
# ========================

def page_role_analysis():
    """Deep role analysis view (Main demo for Data Analyst & other roles)"""
    st.title("📈 Comprehensive Role Intelligence & Transformation")
    st.caption("Full 13-stage intelligence breakdown: Processes → Activities → Skills → AI Impact → Future Profile → Evidence")

    roles = fetch_roles()
    if not roles:
        st.warning("No roles found.")
        return

    # Select Role (Default to Data Analyst)
    data_analyst_id = next((r["id"] for r in roles if r["name"] == "Data Analyst"), roles[0]["id"])
    
    selected_role_id = st.selectbox(
        "Select Target Role for Analysis:",
        options=[r["id"] for r in roles],
        index=[r["id"] for r in roles].index(data_analyst_id),
        format_func=lambda x: next(r["name"] for r in roles if r["id"] == x),
        key="analysis_role_select"
    )

    if selected_role_id:
        role_detail = fetch_role_detail(selected_role_id)
        if not role_detail:
            st.error("Failed to load role details.")
            return

        analysis = role_detail.get("analysis", {})
        
        # Header Overview
        st.markdown(f"# 👤 {role_detail['name']}")
        st.markdown(f"**Department:** `{role_detail.get('department', 'Banking Operations')}`")
        st.write(role_detail.get("description", ""))
        st.info(f"**Current Responsibilities:** {role_detail.get('current_responsibilities', 'N/A')}")

        st.divider()

        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        avg_exp = (analysis.get("average_ai_exposure", 0) or 0) * 100
        avg_auto = (analysis.get("average_automation_potential", 0) or 0) * 100
        avg_aug = (analysis.get("average_augmentation_potential", 0) or 0) * 100
        
        with col1:
            st.metric("Overall AI Exposure", f"{avg_exp:.1f}%")
        with col2:
            st.metric("Mostly Automated", analysis.get("activities_likely_automated", 0))
        with col3:
            st.metric("AI Augmented", analysis.get("activities_likely_augmented", 0))
        with col4:
            st.metric("Human Led", analysis.get("activities_human_led", 0))

        st.divider()

        # Activities Classification Breakdown Tabs
        st.subheader("📊 Activity-Level AI Impact Classification")
        tab_auto, tab_aug, tab_human = st.tabs(["🤖 Mostly Automated", "✨ AI Augmented", "👤 Human Led"])

        # Gather activities from processes
        all_activities = []
        for proc in role_detail.get("processes", []):
            for act in proc.get("activities", []):
                all_activities.append(act)

        with tab_auto:
            auto_acts = [a for a in all_activities if a.get("impact_category") == "Mostly Automated" or a.get("automation_potential", 0) >= 65]
            if auto_acts:
                for a in auto_acts:
                    st.markdown(f"""
                    <div style="background:rgba(239,68,68,0.1); border-left:4px solid #ef4444; padding:12px; margin-bottom:8px; border-radius:4px;">
                        <span class="badge-auto">MOSTLY AUTOMATED</span> <b>{a['name']}</b> (Exposure: {a['ai_exposure_score']}%)
                        <br><span style="font-size:0.85rem; color:#cbd5e1;">{a.get('reasoning', a['description'])}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No activities classified as Mostly Automated.")

        with tab_aug:
            aug_acts = [a for a in all_activities if a.get("impact_category") == "AI Augmented" or (35 <= a.get("augmentation_potential", 0) or a.get("ai_exposure_score", 0) >= 45) and a.get("automation_potential", 0) < 65]
            if aug_acts:
                for a in aug_acts:
                    st.markdown(f"""
                    <div style="background:rgba(59,130,246,0.1); border-left:4px solid #3b82f6; padding:12px; margin-bottom:8px; border-radius:4px;">
                        <span class="badge-aug">AI AUGMENTED</span> <b>{a['name']}</b> (Exposure: {a['ai_exposure_score']}%)
                        <br><span style="font-size:0.85rem; color:#cbd5e1;">{a.get('reasoning', a['description'])}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No activities classified as AI Augmented.")

        with tab_human:
            human_acts = [a for a in all_activities if a.get("impact_category") == "Human Led" or (a.get("augmentation_potential", 0) < 35 and a.get("automation_potential", 0) < 35)]
            if human_acts:
                for a in human_acts:
                    st.markdown(f"""
                    <div style="background:rgba(34,197,94,0.1); border-left:4px solid #22c55e; padding:12px; margin-bottom:8px; border-radius:4px;">
                        <span class="badge-human">HUMAN LED</span> <b>{a['name']}</b> (Exposure: {a['ai_exposure_score']}%)
                        <br><span style="font-size:0.85rem; color:#cbd5e1;">{a.get('reasoning', a['description'])}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No activities classified as Human Led.")

        st.divider()

        # Future Role Profile & Responsibilities
        col_resp, col_profile = st.columns([1, 1])

        with col_resp:
            st.subheader("🎯 Future Responsibilities")
            new_resps = analysis.get("new_responsibilities", [])
            for resp in new_resps:
                st.markdown(f"• **{resp}**")

            st.subheader("🎓 Future Skills Profile")
            fut_skills = analysis.get("future_skills", [])
            for sk in fut_skills:
                st.write(f"📌 {sk}")

        with col_profile:
            st.subheader("🔮 Future Role Profile")
            prof_details = role_detail.get("future_profile_details", {})
            title = prof_details.get("future_role_title", f"AI-Augmented {role_detail['name']}")
            summary = prof_details.get("future_role_summary", analysis.get("future_role_profile", ""))
            
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-header">✨ {title}</div>
                <div style="font-size:0.95rem; margin-bottom:12px;">{summary}</div>
                <div style="font-size:0.85rem; color:#94a3b8;">
                    <b>Key Operational Shift:</b> {prof_details.get('key_changes', 'Routine tasks automated; shift toward validation and advisory.')}<br>
                    <b>Human Focus Area:</b> {prof_details.get('human_focus', 'Critical decision making, ethics, and stakeholder trust.')}<br>
                    <b>AI Focus Area:</b> {prof_details.get('ai_focus', 'Automated data ingestion, query drafting, anomaly alerts.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Explainability & Methodology Section
        st.subheader("🧮 Explainability & Scoring Methodology")
        st.markdown("""
        How was the **Overall AI Exposure Score** derived?
        
        1. **Activity-Level Characteristics**: Each activity is scored across 7 factors on a 0–100 scale:
           - *Repetitiveness (30%)*, *Data Availability (25%)*, *Rule-based Nature (20%)*, *Complexity (10%)*, *Human Judgment inverse (10%)*, *Regulatory Sensitivity inverse (5%)*.
        2. **Role-Level Score Aggregation**: The role score is the arithmetic mean of all underlying activity exposure scores.
        3. **Transparent Calculation**: No black-box guesses. Calculated deterministically by application logic.
        """)

        # Research Evidence Section
        st.subheader("📚 Verified Research & Evidence Base")
        evidence = role_detail.get("evidence", [])
        if evidence:
            for ev in evidence:
                st.markdown(f"""
                <div class="evidence-box">
                    <b>{ev['title']}</b> — <i>{ev['publisher']} ({ev['publication_date']})</i><br>
                    <span style="font-size:0.85rem; color:#cbd5e1;">{ev['summary']}</span><br>
                    <a href="{ev['url']}" target="_blank" style="color:#60a5fa; font-size:0.8rem;">Verified Source URL: {ev['url']}</a>
                </div>
                """, unsafe_allow_html=True)


# ========================
# Page: Role Comparison
# ========================

def page_role_comparison():
    """Compare two roles dynamically"""
    st.title("⚖️ Dynamic Role Comparison")
    st.caption("Compare AI exposure, activity impact breakdown, current vs future skills across two roles")

    roles = fetch_roles()
    if not roles:
        st.warning("No roles found.")
        return

    col1, col2 = st.columns(2)
    with col1:
        r1_id = st.selectbox("Select First Role:", options=[r["id"] for r in roles], format_func=lambda x: next(r["name"] for r in roles if r["id"] == x), index=0)
    with col2:
        r2_id = st.selectbox("Select Second Role:", options=[r["id"] for r in roles], format_func=lambda x: next(r["name"] for r in roles if r["id"] == x), index=min(7, len(roles)-1))

    if r1_id and r2_id and r1_id != r2_id:
        comparison = compare_roles_api(r1_id, r2_id)
        if comparison:
            comp_info = comparison.get("comparison", {})
            r1_data = comparison.get("role_1", {})
            r2_data = comparison.get("role_2", {})

            st.success(f"💡 **Analysis Conclusion:** {comp_info.get('key_difference', '')}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"### {r1_data.get('name')}")
                st.metric("AI Exposure", f"{r1_data.get('ai_exposure', 0)*100:.1f}%")
                st.metric("Automation Potential", f"{r1_data.get('automation_potential', 0)*100:.1f}%")
                st.metric("Augmentation Potential", f"{r1_data.get('augmentation_potential', 0)*100:.1f}%")
                st.metric("Affected Activities", r1_data.get("affected_activities", 0))

            with col_b:
                st.markdown(f"### {r2_data.get('name')}")
                st.metric("AI Exposure", f"{r2_data.get('ai_exposure', 0)*100:.1f}%")
                st.metric("Automation Potential", f"{r2_data.get('automation_potential', 0)*100:.1f}%")
                st.metric("Augmentation Potential", f"{r2_data.get('augmentation_potential', 0)*100:.1f}%")
                st.metric("Affected Activities", r2_data.get("affected_activities", 0))


# ========================
# Page: AI Impact Ranking
# ========================

def page_ai_ranking():
    """Top 5 AI Impact Ranking"""
    st.title("🏆 AI Impact Ranking")
    st.caption("Dynamic ranking of banking roles with the highest AI exposure scores")

    limit = st.slider("Select Ranking Count:", min_value=3, max_value=20, value=5)
    top_roles = fetch_top_ai_impact_roles(limit=limit)

    if top_roles:
        rank_df = pd.DataFrame([
            {
                "Rank": r["rank"],
                "Role": r["role"]["name"],
                "AI Impact Score (%)": round(r["ai_impact_score"] * 100, 1),
                "Affected Activities": r["affected_activities"],
                "Reasoning": r.get("reasoning", "")
            }
            for r in top_roles
        ])

        fig = px.bar(
            rank_df, x="Role", y="AI Impact Score (%)",
            color="AI Impact Score (%)", color_continuous_scale="Reds",
            text="AI Impact Score (%)", title=f"Top {limit} Roles by AI Impact Score"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(rank_df, use_container_width=True)


# ========================
# Page: Add New Role (SURPRISE TEST)
# ========================

def page_add_new_role():
    """Add new role dynamically (Surprise test: Supply Chain Analyst)"""
    st.title("➕ Add New Role (Surprise Test Workflow)")
    st.caption("Enter a new role without modifying source code. Dynamically calculates AI impact, future profile, and persists across application restarts.")

    st.markdown("""
    **Test with Supply Chain Analyst**:
    Fill in the form below or use pre-populated values. Click **Create & Analyze Role** to execute the complete dynamic analysis pipeline.
    """)

    col1, col2 = st.columns(2)
    with col1:
        role_name = st.text_input("Role Name *", value="Supply Chain Analyst")
    with col2:
        department = st.text_input("Department", value="Supply Chain & Procurement")

    description = st.text_area("Role Description *", value="Analyzes supply chain operations, tracks vendor delivery schedules, optimizes inventory levels, and mitigates logistics disruptions.")
    current_responsibilities = st.text_area("Current Responsibilities", value="Extracting shipment data, compiling vendor KPI scorecards, reviewing inventory thresholds, and coordinating with freight suppliers.")

    st.subheader("📋 Processes & Activities (JSON Format)")
    default_processes = [
        {
            "name": "Inventory & Logistics Tracking",
            "description": "Monitoring warehouse stock levels and shipment status.",
            "activities": [
                {
                    "name": "Automated Stock Level & Reorder Reconciliation",
                    "description": "Checking daily warehouse inventory against safety stock thresholds.",
                    "repetitiveness": 0.85,
                    "data_availability": 0.90,
                    "rule_based_nature": 0.85,
                    "language_cognitive_complexity": 0.35,
                    "human_judgment_requirement": 0.30,
                    "regulatory_sensitivity": 0.30,
                    "human_interaction_requirement": 0.20
                },
                {
                    "name": "Logistics Disruption Mitigation & Escalation",
                    "description": "Negotiating alternative freight routing during port strikes or severe weather disruptions.",
                    "repetitiveness": 0.30,
                    "data_availability": 0.60,
                    "rule_based_nature": 0.25,
                    "language_cognitive_complexity": 0.75,
                    "human_judgment_requirement": 0.85,
                    "regulatory_sensitivity": 0.50,
                    "human_interaction_requirement": 0.90
                }
            ]
        }
    ]

    processes_json = st.text_area("Processes JSON payload:", value=json.dumps(default_processes, indent=2), height=250)

    if st.button("⚡ Create and Analyze Role", type="primary"):
        if not role_name or not description:
            st.error("Please provide role name and description.")
            return

        try:
            proc_payload = json.loads(processes_json)
            with st.spinner(f"Creating '{role_name}', calculating AI impact, generating future profile, and persisting to DB..."):
                res = create_new_role_api({
                    "role_name": role_name,
                    "department": department,
                    "role_description": description,
                    "current_responsibilities": current_responsibilities,
                    "processes": proc_payload
                })

                if res:
                    st.success(f"✅ Role '{role_name}' successfully created, analyzed, and persisted in database!")
                    st.json(res)
                else:
                    st.error("Error creating role.")
        except json.JSONDecodeError:
            st.error("Invalid JSON format for processes.")


# ========================
# Page: Ask Intelligence (RAG BOT)
# ========================

def page_ask_intelligence():
    """Ask Intelligence RAG Natural Language Chat Bot Engine"""
    st.title("❓ Ask Intelligence (RAG Bot)")
    st.caption("Ask ANY question about enterprise roles, processes, activities, skills, AI exposure, rankings, comparisons, or research evidence.")

    # Initialize Session State for query text
    if "query_text" not in st.session_state:
        st.session_state["query_text"] = ""

    def set_question(text: str):
        st.session_state["query_text"] = text

    # Sample Presets with Callbacks
    st.markdown("**Sample Presets (Click to Auto-fill):**")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.button("❓ Why is Data Analyst exposed?", on_click=set_question, args=("Why is Data Analyst highly exposed to AI?",))
        st.button("❓ Automated Data Analyst activities?", on_click=set_question, args=("Which Data Analyst activities are likely to be automated?",))
    
    with p2:
        st.button("❓ Top 5 AI impact roles?", on_click=set_question, args=("Which five roles have the highest AI impact?",))
        st.button("❓ Compare Data & Procurement Analyst", on_click=set_question, args=("Compare Data Analyst and Procurement Analyst.",))
    
    with p3:
        st.button("❓ What future skills are needed?", on_click=set_question, args=("What future skills will Data Analysts need?",))
        st.button("❓ What evidence supports this?", on_click=set_question, args=("What evidence supports this conclusion?",))

    # Text Input for Custom Question
    query_input = st.text_input("Enter your question:", key="query_text", placeholder="e.g., What tasks are automated for Credit Analyst? Or: What skills does a Risk Analyst need?")

    roles = fetch_roles()
    role_dict = {r["id"]: r["name"] for r in roles}
    context_role = st.selectbox("Context Role (Optional):", options=[None] + list(role_dict.keys()), format_func=lambda x: "Auto-detect from query" if x is None else role_dict.get(x, ""))

    if st.button("🔍 Execute Intelligence Query", type="primary") or (query_input and len(query_input.strip()) > 3):
        if query_input and query_input.strip():
            with st.spinner("Retrieving RAG evidence and synthesizing answer..."):
                res = ask_question_api(query_input.strip(), context_role)
                if res:
                    st.markdown(f"""
                    <div class="rag-answer-card">
                        <div style="font-weight:700; color:#38bdf8; font-size:1.1rem; margin-bottom:10px;">
                            🤖 RAG Bot Response (Confidence: {res.get('confidence', 0.9)*100:.0f}%)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(res.get("answer", ""))

                    if res.get("reasoning"):
                        st.markdown("#### 🧠 Analytical Reasoning")
                        st.info(res.get("reasoning"))

                    evidence = res.get("evidence", [])
                    if evidence:
                        st.markdown("#### 📚 Verified Research Evidence Citations")
                        for ev in evidence:
                            st.markdown(f"""
                            <div class="evidence-box">
                                <b>{ev['title']}</b> — <i>{ev['publisher']} ({ev['publication_date']})</i><br>
                                <span style="font-size:0.85rem; color:#cbd5e1;">{ev['summary']}</span><br>
                                <a href="{ev['url']}" target="_blank" style="color:#60a5fa; font-size:0.8rem;">Verified Source URL: {ev['url']}</a>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question or click one of the preset buttons above.")


# ========================
# Page: Evidence & Research
# ========================

def page_research_evidence():
    """Research & Evidence Base Explorer"""
    st.title("📚 Research Evidence Explorer")
    st.caption("Verified public research reports on AI, automation, and workforce transformation in Banking & Financial Services")

    sources = fetch_research_sources()
    if sources:
        for src in sources:
            with st.expander(f"📌 **{src['title']}** — {src['publisher']} ({src['publication_date']})"):
                st.write(f"**Source Type:** `{src['source_type']}` | **Relevance Score:** `{src['relevance_score']*100:.0f}%`")
                st.write(f"**Summary:** {src['summary']}")
                st.markdown(f"**URL:** [{src['url']}]({src['url']})")


# ========================
# Main Navigation
# ========================

def main():
    st.sidebar.title("⚡ MODUS Role-AI")
    st.sidebar.caption("Role-Level AI Intelligence Platform")

    # Auto-initialize DB on startup if empty (for Streamlit Cloud)
    db = get_standalone_db()
    if db.query(RoleRepository.get_all).count if hasattr(RoleRepository, 'count') else RoleRepository.get_all(db) == []:
        from scripts.seed_data import seed_banking_roles
        seed_banking_roles(db)

    pages = {
        "📊 Executive Dashboard": page_dashboard,
        "🔍 Role Explorer": page_role_explorer,
        "📈 Comprehensive Role Analysis": page_role_analysis,
        "⚖️ Dynamic Role Comparison": page_role_comparison,
        "🏆 AI Impact Ranking": page_ai_ranking,
        "➕ Add New Role (Surprise Test)": page_add_new_role,
        "❓ Ask Intelligence": page_ask_intelligence,
        "📚 Research Evidence Base": page_research_evidence
    }

    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))

    st.sidebar.divider()
    st.sidebar.markdown("""
    **Challenge**: MODUS Enterprise AI Challenge  
    **Assignment**: Assignment 6 — Role-Level AI Intelligence  
    **Industry**: Banking & Financial Services  
    **Demo Role**: Data Analyst
    """)

    pages[selected_page]()


if __name__ == "__main__":
    main()
