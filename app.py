import streamlit as st
from streamlit.components.v1 import html
import form
import streamlit_app

# Set Page Configuration
st.set_page_config(
    page_title="Neon Glow Professional App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)



# Load Custom CSS
def load_custom_css(css_file):
    """Load custom CSS from a file."""
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file '{css_file}' not found. Please ensure it exists.")

# Main Navigation Function
def main():
    # Load custom CSS for styling
    load_custom_css("style.css")

    # Sidebar Navigation
    page = st.sidebar.radio("Navigation", ["Home", "Interactive Form", "HR Assistant"])

    # Home Page
    if page == "Home":
        render_home_page()

    # Interactive Form Page
    elif page == "Interactive Form":
        form.main()

    # HR Assistant Page
    elif page == "HR Assistant":
        # Custom glowing title
        st.markdown("""
            <div style="text-align: center; padding: 20px; 
                        border-radius: 15px; background-color: transparent; 
                        box-shadow: 0 0 20px rgba(47, 79, 79, 0.8); 
                        animation: glowing 1.5s infinite alternate;
                        font-family: 'Roboto', sans-serif;">
                <h1 style="font-size: 36px; color: white;">AI Team Design Workflow</h1>
                <p style="font-size: 18px; color: white;">Designing a team for iOS app development.</p>
            </div>
            <style>
                @keyframes glowing {
                    0% { box-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00, 0 0 20px #00ff00; }
                    100% { box-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff, 0 0 20px #ff00ff; }
                }

                /* Apply modern font style globally */
                body {
                    font-family: 'Roboto', sans-serif;
                }

                /* Importing Google Font 'Roboto' */
                @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
            </style>
        """, unsafe_allow_html=True)
        streamlit_app.main()

def render_home_page():
    """Render the Home page."""
    st.markdown("<h1 class='title'>Welcome to the Neon Glow App</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Experience professional design with a touch of neon brilliance.</p>", unsafe_allow_html=True)

    # Features Section
    st.markdown("### Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='feature-card'><h2>Modern Design</h2><p>Explore cutting-edge designs.</p></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'><h2>Professional Fonts</h2><p>Experience unmatched readability.</p></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='feature-card'><h2>Interactive Animations</h2><p>Engage users with smooth effects.</p></div>", unsafe_allow_html=True)

    # Call to Action Section
    st.markdown("""
        <div class='cta-section'>
            <button class='neon-button' onclick='alert("Welcome to the future!")'>Get Started</button>
        </div>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
