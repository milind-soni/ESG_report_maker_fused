import micropip
await micropip.install('streamlit-quill')
await micropip.install('reportlab')
await micropip.install('streamlit_pdf_viewer')
await micropip.install('pillow')
await micropip.install('requests')

import streamlit as st
from streamlit_quill import st_quill
from streamlit_pdf_viewer import pdf_viewer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from bs4 import BeautifulSoup
import io
import requests
from PIL import Image as PILImage

def download_image(url):
    """Download image from URL and convert to ReportLab-compatible format"""
    response = requests.get(url)
    img_data = io.BytesIO(response.content)
    img = PILImage.open(img_data)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Save as JPEG in memory
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    return img_buffer

def html_to_pdf(html_content):
    """Convert HTML content to PDF using ReportLab with image support"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CenteredTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER
    ))
    
    elements = []
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process each element
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
        if element.name == 'img':
            try:
                # Handle image
                img_url = element.get('src', '')
                if img_url:
                    img_buffer = download_image(img_url)
                    img = Image(img_buffer)
                    
                    # Scale image to fit page width while maintaining aspect ratio
                    img.drawWidth = 400
                    img.drawHeight = 200
                    
                    elements.append(img)
                    elements.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error processing image: {e}")
                continue
        else:
            # Handle text elements
            if element.name == 'h1':
                style = styles['CenteredTitle']
            elif element.name == 'h2':
                style = styles['Heading2']
            elif element.name == 'h3':
                style = styles['Heading3']
            else:
                style = styles['Normal']
            
            if element.text.strip():
                elements.append(Paragraph(element.text.strip(), style))
                elements.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

st.title("ESG Report Maker")

# Sample ESG report template
esg_template = """
<h1>Environmental, Social, and Governance Report</h1>
<h2>Executive Summary</h2>
<p>This report outlines our commitment to sustainability and responsible business practices...</p>

<h2>Environmental Impact</h2>
<h3>Carbon Footprint</h3>
<p>Insert your carbon emissions data and reduction targets here...</p>
<img src="https://picsum.photos/id/1043/400/200" alt="Environmental Impact Visualization">

<h3>Resource Management</h3>
<p>Detail your resource conservation initiatives...</p>

<h2>Social Responsibility</h2>
<h3>Workforce Diversity</h3>
<p>Include your diversity metrics and initiatives...</p>
<img src="https://picsum.photos/id/1025/400/200" alt="Diversity Visualization">

<h3>Community Engagement</h3>
<p>Describe your community programs and impact...</p>

<h2>Governance</h2>
<h3>Board Structure</h3>
<p>Outline your governance framework...</p>
<img src="https://picsum.photos/id/1070/400/200" alt="Governance Structure">

<h3>Ethics and Compliance</h3>
<p>Detail your ethical business practices...</p>
"""

# Create tabs
editor_tab, pdf_tab = st.tabs(["ESG Editor", "PDF Preview"])

with editor_tab:
    # Quill editor
    edited_content = st_quill(
        value=st.session_state.get('editor_content', esg_template),
        placeholder="Start creating your ESG report...",
        html=True,
        toolbar=[
            [{'font': []}, {'size': []}],
            ['bold', 'italic', 'underline'],
            [{'color': []}, {'background': []}],
            [{'align': ['', 'center', 'right', 'justify']}],
            [{'header': [1, 2, 3, False]}],
            ['link', 'image'],
            ['clean']
        ],
        key="esg_editor"
    )
    
    if edited_content:
        st.session_state['editor_content'] = edited_content

with pdf_tab:
    if st.session_state.get('editor_content'):
        try:
            # Add a loading message
            with st.spinner('Generating PDF preview...'):
                pdf_bytes = html_to_pdf(st.session_state['editor_content'])
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="esg_report.pdf",
                    mime="application/pdf"
                )
            
            pdf_viewer(pdf_bytes)
            
        except Exception as e:
            st.error(f"Error generating PDF preview: {str(e)}")
    else:
        st.info("Start editing in the ESG Editor tab to see PDF preview")
