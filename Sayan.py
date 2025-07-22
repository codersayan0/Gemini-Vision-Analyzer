import streamlit as st
import google.generativeai as genai
from PIL import Image
from typing import Optional, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini analyzer class
class GeminiVisionAnalyzer:
    """
    A class to handle Gemini API interactions for image analysis using the Gemini 1.5 Flash model.
    """
    def __init__(self, api_key: str):
        """
        Initialize the Gemini client with the provided API key.
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini model initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise

    def analyze_image(self, image: Image.Image, question: str) -> Tuple[bool, str]:
        """
        Analyze an image with a specific question using the Gemini API.
        """
        try:
            prompt = f"Please analyze this image and answer the following question: {question}"
            response = self.model.generate_content([prompt, image])
            if response.text:
                return True, response.text
            else:
                return False, "No response generated from the model."
        except Exception as e:
            error_msg = f"Error during image analysis: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

# Image validator
def validate_image(uploaded_file) -> Tuple[bool, Optional[Image.Image], str]:
    if uploaded_file is None:
        return False, None, "No file uploaded."

    try:
        if uploaded_file.size > 10 * 1024 * 1024:
            return False, None, "File size exceeds 10MB limit."

        image = Image.open(uploaded_file)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')

        return True, image, "Image validated successfully."

    except Exception as e:
        return False, None, f"Invalid image file: {str(e)}"

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="Gemini Vision Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1e3a8a;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #374151;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .info-box {
            background-color: #000000;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3b82f6;
            margin: 1rem 0;
            color: white;
        }
        .error-box {
            background-color: #fef2f2;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ef4444;
            margin: 1rem 0;
            color: #991b1b;
        }
        .success-box {
            background-color: #f0fdf4;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #22c55e;
            margin: 1rem 0;
            color: #166534;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">Gemini Vision Analyzer</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="section-header">Configuration</h2>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Enter your Google API key to access the Gemini model.",
        )
        if api_key:
            st.markdown('<div class="success-box">✅ API key configured</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-box">
                    <strong>🔧 Setup Instructions:</strong><br><br>
                    1. Visit <a href="https://makersuite.google.com/app" target="_blank">Google AI Studio</a><br>
                    2. Create or select a project<br>
                    3. Generate an API key<br>
                    4. Enter the key above to begin
                </div>
            """, unsafe_allow_html=True)

    # Upload and input
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg", "webp"],
            help="Supported formats: PNG, JPG, JPEG, WebP (Max size: 10MB)"
        )

        if uploaded_file:
            is_valid, image, message = validate_image(uploaded_file)
            if is_valid:
                st.image(image, caption="Uploaded Image", use_column_width=True)
                st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h2 class="section-header">Question & Analysis</h2>', unsafe_allow_html=True)
        question = st.text_area(
            "Enter your question about the image",
            placeholder="What do you see in this image? Describe the main objects, colors, and activity.",
            help="Be specific with your question for better results.",
            height=100
        )

    # Analyze button
    analyze_button = st.button(
        "Analyze Image",
        type="primary",
        use_container_width=True,
        disabled=not (api_key and uploaded_file and question.strip())
    )

    if analyze_button:
        if not api_key:
            st.markdown('<div class="error-box">Please provide a valid API key.</div>', unsafe_allow_html=True)
        elif not uploaded_file:
            st.markdown('<div class="error-box">Please upload an image.</div>', unsafe_allow_html=True)
        elif not question.strip():
            st.markdown('<div class="error-box">Please enter a question.</div>', unsafe_allow_html=True)
        else:
            is_valid, image, message = validate_image(uploaded_file)
            if not is_valid:
                st.markdown('<div class="error-box">Invalid image file.</div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("🔄 Initializing Gemini model..."):
                        analyzer = GeminiVisionAnalyzer(api_key)

                    with st.spinner("🔍 Analyzing image..."):
                        success, response = analyzer.analyze_image(image, question)

                    if success:
                        st.markdown(f'<div class="success-box">{response}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">Analysis failed: {response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">Application error: {str(e)}</div>', unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("Application Information"):
        st.markdown("""
        **Gemini Vision Analyzer**
        
        This application uses Google's Gemini 1.5 Flash model to analyze images and answer questions about them.
        
        **Features:**
        - Image upload and validation
        - Custom question input
        - Professional error handling
        - Responsive design
        
        **Supported Image Formats:** PNG, JPG, JPEG, WebP  
        **Maximum File Size:** 10MB
        
        **Note:** This application requires a valid Google API key to function.
        """)

# Run app
if __name__ == "__main__":
    main()
