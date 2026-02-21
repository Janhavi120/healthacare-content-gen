import streamlit as st
from model import generate_medical_report
from utils.history_manager import save_report, get_all_reports, clear_all_reports
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MediGen - AI Medical Report Generator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS to remove whitespace
st.markdown("""
<style>
    /* Remove all default padding and margins */
    .main > div {
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    
    /* Remove top padding from the main content area */
    .css-18e3th9 {
        padding-top: 0 !important;
    }
    
    .css-1d391kg {
        padding-top: 0 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%) !important;
        min-width: 300px !important;
        padding-top: 0 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }
    
    /* Sidebar button styling */
    section[data-testid="stSidebar"] .stButton button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        margin: 3px 10px !important;
        width: calc(100% - 20px) !important;
        text-align: left !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
        padding: 0 10px !important;
    }
    
    /* Main content area - remove top padding */
    .main-content {
        padding: 0px 20px 20px 20px !important;
        background-color: #ffffff;
        min-height: 100vh;
        margin-top: 0 !important;
    }
    
    /* Opaque logo background */
    .logo-background {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 400px;
        opacity: 0.03;
        pointer-events: none;
        z-index: 0;
        color: #1e40af;
    }
    
    /* Welcome banner - remove top margin */
    .welcome-banner {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 30px 40px;
        border-radius: 0 0 20px 20px;
        margin: 0 0 30px 0;
        width: 100%;
    }
    
    .welcome-banner h1 {
        margin: 0;
        font-size: 42px;
    }
    
    .welcome-banner p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 18px;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        height: 100%;
        margin-top: 0;
    }
    
    .feature-icon {
        font-size: 45px;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #1e40af;
        font-size: 22px;
        font-weight: bold;
        margin: 5px 0;
    }
    
    /* Form container */
    .form-container {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 15px;
        padding: 25px;
        margin-top: 0;
    }
    
    .form-container h2 {
        margin-top: 0;
        margin-bottom: 20px;
        color: #1e40af;
    }
    
    /* History card */
    .history-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }
    
    /* Report container */
    .report-container {
        background: #f8fafc;
        border: 2px solid #dbeafe;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }
    
    /* Remove top padding from all columns */
    .row-widget.stHorizontal {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Adjust spacing for headers */
    h1, h2, h3 {
        margin-top: 0 !important;
    }
    
    /* Remove any extra space at the very top */
    .appview-container .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'selected_report' not in st.session_state:
    st.session_state.selected_report = None
if 'reports' not in st.session_state:
    st.session_state.reports = get_all_reports()

# Opaque logo background
st.markdown('<div class="logo-background">🏥</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo and title
    st.markdown("## 🏥 **MediGen**")
    st.markdown("---")
    
    # Navigation
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.session_state.selected_report = None
        st.rerun()
    
    if st.button("📝 Report Generation", use_container_width=True):
        st.session_state.page = "Report Generation"
        st.session_state.selected_report = None
        st.rerun()
    
    if st.button("📋 History", use_container_width=True):
        st.session_state.page = "History"
        st.session_state.selected_report = None
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    total_reports = len(st.session_state.reports)
    st.markdown("### 📊 Statistics")
    st.markdown(f"**Total Reports:** {total_reports}")
    
    if total_reports > 0:
        latest = st.session_state.reports[0]
        if isinstance(latest['timestamp'], datetime):
            st.markdown(f"**Latest:** {latest['timestamp'].strftime('%Y-%m-%d')}")

# Main content - removed the extra div that might be causing spacing
# Home Page
if st.session_state.page == "Home":
    # Welcome banner - no extra div wrapper
    st.markdown("""
    <div class="welcome-banner">
        <h1>Welcome to MediGen</h1>
        <p>AI-Powered Medical Documentation Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">AI-Powered</h3>
            <p style="color: #666;">Generate professional medical reports instantly using AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Structured</h3>
            <p style="color: #666;">Comprehensive reports with all essential medical sections</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💾</div>
            <h3 class="feature-title">History</h3>
            <p style="color: #666;">Automatically save and access all previous reports</p>
        </div>
        """, unsafe_allow_html=True)

# Report Generation Page
elif st.session_state.page == "Report Generation":
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("## 📝 Generate New Medical Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.text_input("Age", placeholder="Enter patient age")
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    symptoms = st.text_area("Primary Symptoms", placeholder="Describe the symptoms...", height=150)
    
    doctor_type = st.selectbox(
    "Doctor Type / Specialty",
    [
        "General Physician",
        "Cardiologist", 
        "Orthopedist",
        "Gynecologist",
        "Physiotherapist",
        "Neurologist",
        "Pediatrician",
        "Dermatologist",
        "Psychiatrist"
    ]
)

    report_type = st.selectbox(
        "Report Type",
        ["Initial Consultation", "Follow-Up", "Emergency Visit", "Routine Checkup"]
    )
    
    if st.button("🚀 Generate Report", use_container_width=True):
        if not age or not symptoms:
            st.error("⚠️ Please fill in all required fields!")
        else:
            with st.spinner("Generating report..."):
                try:
                    report = generate_medical_report(age, gender, symptoms, report_type,doctor_type)
                    
                    # Save to history
                    report_data = {
                        'age': age,
                        'gender': gender,
                        'symptoms': symptoms,
                        'type': report_type,
                        'report': report,
                        'Doctor Type': doctor_type,
                        'timestamp': datetime.now()
                    }
                    save_report(report_data)
                    st.session_state.reports = get_all_reports()
                    
                    st.success("✅ Report generated!")
                    st.markdown("---")
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(report)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.download_button("📥 Download", report, file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# History Page
elif st.session_state.page == "History":
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 📋 Report History")
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            if clear_all_reports():
                st.session_state.reports = []
                st.rerun()
    
    if st.session_state.reports:
        st.markdown(f"**Total Reports:** {len(st.session_state.reports)}")
        
        for idx, report in enumerate(st.session_state.reports):
            timestamp = report['timestamp']
            if isinstance(timestamp, datetime):
                date_str = timestamp.strftime('%B %d, %Y at %I:%M %p')
            else:
                date_str = str(timestamp)
            
            st.markdown(f"""
            <div class="history-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #1e40af; font-weight: bold;">{date_str}</span>
                    <span style="background: #1e40af; color: white; padding: 5px 10px; border-radius: 20px;">{report['type']}</span>
                </div>
                <p style="margin: 5px 0;"><strong>Patient:</strong> {report['age']} years, {report['gender']}</p>
                <p style="margin: 5px 0;"><strong>Symptoms:</strong> {report['symptoms'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 8])
            with col1:
                if st.button(f"👁️ View", key=f"view_{idx}"):
                    st.session_state.selected_report = report
                    st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Show selected report
        if st.session_state.selected_report:
            st.markdown("---")
            st.markdown("### 📄 Selected Report")
            report = st.session_state.selected_report
            
            timestamp = report['timestamp']
            if isinstance(timestamp, datetime):
                date_str = timestamp.strftime('%B %d, %Y at %I:%M %p')
            else:
                date_str = str(timestamp)
            
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #dbeafe;">
                <p style="margin: 5px 0;"><strong>📅 Generated:</strong> {date_str}</p>
                <p style="margin: 5px 0;"><strong>👤 Patient:</strong> {report['age']} years, {report['gender']}</p>
                <p style="margin: 5px 0;"><strong>📋 Type:</strong> {report['type']}</p>
                <p style="margin: 5px 0;"><strong>💭 Symptoms:</strong> {report['symptoms']}</p>
                <p style="margin: 5px 0;"><strong>💭 Symptoms:</strong> {report['doctor_type']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(report['report'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button("📥 Download", report['report'], file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt")
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h3 style="color: #666; margin: 0;">No reports yet</h3>
            <p style="margin: 10px 0 0 0;">Generate your first report to see it here.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)