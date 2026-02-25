"""
Streamlit Frontend for Titanic Chatbot
"""
import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Titanic Chatbot",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint - configurable
API_URL = "http://localhost:8000"


def call_api(query: str) -> dict:
    """Call the FastAPI backend"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"answer": "Error: Could not connect to backend. Make sure the API is running on port 8000.", "visualization": None}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "visualization": None}


def display_image(base64_str: str):
    """Display base64 encoded image"""
    if base64_str:
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))
        st.image(image, use_container_width=True)


def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🚢 Titanic Dataset Chatbot")
    st.markdown("""
    Ask me anything about the Titanic passengers! I can analyze:
    - Gender distribution
    - Age statistics  
    - Ticket fares
    - Embarkation ports
    - Survival rates
    """)
    
    # Sidebar with example questions
    st.sidebar.title("💡 Example Questions")
    st.sidebar.markdown("Click on any question to ask:")
    
    example_questions = [
        "What percentage of passengers were male on the Titanic?",
        "Show me a histogram of passenger ages",
        "What was the average ticket fare?",
        "How many passengers embarked from each port?",
        "Show me survival rates by class",
        "What's the overall survival rate?"
    ]
    
    for q in example_questions:
        st.sidebar.markdown(f"- {q}")
    
    # Dataset info in sidebar
    st.sidebar.title("📊 Dataset Info")
    if st.sidebar.button("Load Dataset Info"):
        try:
            info_response = requests.get(f"{API_URL}/info", timeout=10)
            if info_response.status_code == 200:
                info = info_response.json()
                st.sidebar.markdown(f"**Total Passengers:** {info['shape'][0]}")
                st.sidebar.markdown(f"**Columns:** {len(info['columns'])}")
                st.sidebar.markdown("**Features:**")
                for col in info['columns']:
                    st.sidebar.markdown(f"  - {col}")
            else:
                st.sidebar.error("Could not load dataset info")
        except:
            st.sidebar.error("API not available")
    
    # Main chat interface
    st.markdown("### 💬 Ask Your Question")
    
    # Input method 1: Text input
    query = st.text_input(
        "Type your question:",
        placeholder="e.g., What percentage of passengers were male?",
        key="query_input"
    )
    
    # Input method 2: Click on example
    selected_example = st.selectbox(
        "Or select an example:",
        [""] + example_questions
    )
    
    # Use selected example if available
    if selected_example:
        query = selected_example
    
    # Submit button
    if st.button("Ask", type="primary", disabled=not query):
        with st.spinner("Analyzing..."):
            result = call_api(query)
            
            # Display answer
            st.markdown("### 📝 Answer")
            st.markdown(result.get("answer", "No answer received"))
            
            # Display visualization if available
            if result.get("visualization"):
                st.markdown("### 📈 Visualization")
                display_image(result["visualization"])
    
    # Quick stats section
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        info_response = requests.get(f"{API_URL}/info", timeout=5)
        if info_response.status_code == 200:
            info = info_response.json()
            total = info['shape'][0]
            
            # Get gender info
            gender_result = call_api("What percentage were male?")
            if gender_result.get("answer"):
                # Extract male percentage
                import re
                match = re.search(r'Male:.*?\(([\d.]+)%\)', gender_result["answer"])
                male_pct = match.group(1) if match else "N/A"
            else:
                male_pct = "N/A"
            
            # Get survival rate
            survival_result = call_api("What was the survival rate?")
            if survival_result.get("answer"):
                match = re.search(r'Overall Survival Rate: ([\d.]+)%', survival_result["answer"])
                survival_pct = match.group(1) if match else "N/A"
            else:
                survival_pct = "N/A"
            
            col1.metric("Total Passengers", f"{total}")
            col2.metric("Male Percentage", f"{male_pct}%")
            col3.metric("Survival Rate", f"{survival_pct}%")
            col4.metric("Features", f"{len(info['columns'])}")
    except:
        # Show placeholder metrics when API not available
        col1.metric("Total Passengers", "891")
        col2.metric("Male Percentage", "64.76%")
        col3.metric("Survival Rate", "38.38%")
        col4.metric("Features", "12")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        Titanic Chatbot | Built with FastAPI, LangChain & Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
