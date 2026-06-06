import streamlit as st
from PIL import Image
import pytesseract
import tempfile
import os
from io import BytesIO
import pandas as pd

# Configure page
st.set_page_config(
    page_title="PaperText OCR - Screenshot to Text Converter",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📄 PaperText OCR</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert screenshots of papers and articles into clean, searchable text</p>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. Upload a screenshot of a paper/article
    2. Wait for processing
    3. Copy or download the extracted text
    """)
    st.markdown("### ✅ Supported Formats")
    st.markdown("- PNG, JPG, JPEG, BMP, TIFF")
    st.markdown("### ⚙️ Tips")
    st.markdown("- Use high-resolution images")
    st.markdown("- Ensure text is clearly visible")
    st.markdown("- Avoid heavy shadows or glare")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload Screenshot")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload a screenshot of a paper or article"
    )

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot", use_column_width=True)

with col2:
    st.markdown("### 📝 Extracted Text")
    
    if uploaded_file is not None:
        try:
            with st.spinner("🔍 Processing image... This may take a few seconds."):
                # Perform OCR
                extracted_text = pytesseract.image_to_string(image)
                
                if extracted_text.strip():
                    # Display success message
                    st.markdown('<div class="success-box">✅ Text extracted successfully!</div>', unsafe_allow_html=True)
                    
                    # Display extracted text in a text area
                    text_output = st.text_area(
                        "Extracted Text",
                        value=extracted_text,
                        height=300,
                        key="text_output"
                    )
                    
                    # Download button
                    col_dl1, col_dl2 = st.columns([1, 1])
                    with col_dl1:
                        # Create download buffer
                        buffer = BytesIO()
                        buffer.write(extracted_text.encode('utf-8'))
                        buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download as TXT",
                            data=buffer,
                            file_name="extracted_text.txt",
                            mime="text/plain",
                            key="download_txt"
                        )
                    
                    with col_dl2:
                        # Copy to clipboard using JavaScript
                        st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText(`{extracted_text}`)" 
                                style="background-color: #1f77b4; color: white; border: none; 
                                       padding: 0.5rem 1rem; border-radius: 0.25rem; 
                                       cursor: pointer; font-weight: bold;">
                        📋 Copy to Clipboard
                        </button>
                        """, unsafe_allow_html=True)
                    
                    # Show statistics
                    st.markdown("### 📊 Text Statistics")
                    stats_col1, stats_col2, stats_col3 = st.columns(3)
                    with stats_col1:
                        st.metric("Characters", len(extracted_text))
                    with stats_col2:
                        st.metric("Words", len(extracted_text.split()))
                    with stats_col3:
                        st.metric("Lines", len(extracted_text.splitlines()))
                        
                else:
                    st.markdown('<div class="error-box">⚠️ No text could be extracted. Please try a clearer image.</div>', unsafe_allow_html=True)
                    
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Error processing image: {str(e)}</div>', unsafe_allow_html=True)
            st.markdown("Please try uploading a different image or check the file format.")
    else:
        st.info("👆 Upload an image to see extracted text here")

# Footer
st.markdown("---")
st.markdown("### 💡 About PaperText OCR")
st.markdown("""
PaperText OCR is designed specifically for researchers to quickly extract text from screenshots of academic papers and articles. 
It uses Tesseract OCR engine to provide accurate text extraction.
""")

# Requirements
st.markdown("### 📦 Requirements")
st.code("""
streamlit==1.28.0
Pillow==10.0.0
pytesseract==0.3.10
pandas==2.0.3
""", language="text")