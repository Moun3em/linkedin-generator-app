import streamlit as st
import openai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        color: #0A66C2;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #0A66C2;
        color: white;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-title'>LinkedIn Post Generator</h1>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Enter your OpenAI API key
    2. Fill in your content details
    3. Generate your post
    4. Edit and refine
    5. Use additional tools
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Post Details")
    topic = st.text_input("Topic", placeholder="e.g., Impact of Food on Leadership")
    industry = st.text_input("Industry", placeholder="e.g., Business Management")
    expertise = st.text_input("Expertise Areas (optional)", placeholder="e.g., Leadership Development")
    story = st.text_area("Personal Story (optional)", placeholder="Share a relevant experience...")

    if st.button("✨ Generate Post", use_container_width=True):
        if not api_key:
            st.error("Please enter your OpenAI API key")
        elif not topic or not industry:
            st.error("Please enter both topic and industry")
        else:
            try:
                openai.api_key = api_key
                with st.spinner("Creating your LinkedIn post..."):
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a LinkedIn content expert specializing in creating engaging, professional posts."},
                            {"role": "user", "content": f"""
                            Create an engaging LinkedIn post about:
                            Topic: {topic}
                            Industry: {industry}
                            Expertise: {expertise if expertise else 'General'}
                            Personal Story: {story if story else 'None'}
                            
                            Include:
                            1. Attention-grabbing hook
                            2. Key insights with data points
                            3. Personal perspective
                            4. Call to action
                            5. 3-5 relevant hashtags
                            
                            Format with proper spacing and emojis for better readability.
                            """}
                        ]
                    )
                    st.session_state.content = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.subheader("Generated Content")
    if "content" in st.session_state:
        content = st.session_state.content
        st.text_area("Your LinkedIn Post", content, height=300)
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if st.button("✍️ Check Grammar"):
                st.markdown("[Open in Grammarly](https://app.grammarly.com/)", unsafe_allow_html=True)
        
        with col4:
            if st.button("🎨 Create Visual"):
                st.markdown("[Design in Canva](https://www.canva.com/create/social-media/)", unsafe_allow_html=True)
        
        with col5:
            st.download_button(
                "💾 Download",
                content,
                f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                "text/plain",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Made with ❤️ by Your LinkedIn Content Assistant"
    "</div>",
    unsafe_allow_html=True
)