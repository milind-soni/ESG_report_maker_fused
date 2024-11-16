import micropip
await micropip.install('streamlit-quill')
await micropip.install('streamlit_pdf_viewer')

import streamlit as st
from streamlit_quill import st_quill
from streamlit_pdf_viewer import pdf_viewer
import fused

st.title("Fused ESG Report Maker")

esg_template = """
<h1>Environmental, Social, and Governance Report</h1>
<h2>Executive Summary</h2>
<p>This report outlines our commitment to sustainability and responsible business practices...</p>

<h2>Environmental Impact</h2>
<h3>Vegetation Analysis (NDVI)</h3>
<p>Below is our NDVI (Normalized Difference Vegetation Index) analysis showing vegetation density in our operational areas:</p>
<img src="https://www.fused.io/server/v1/realtime-shared/fsh_22OJjZ9tNKHaQ9NKVY6ewq/run/tiles/12/1207/1538?dtype_out_raster=png" alt="NDVI Analysis">
<p>The NDVI analysis helps us monitor and maintain green cover in our areas of operation. Higher values (greener areas) indicate healthy vegetation.</p>

<h3>Resource Management</h3>
<p>Detail your resource conservation initiatives...</p>

<h2>Social Responsibility</h2>
<h3>Environmental Impact Assessment</h3>
<p>Our environmental impact assessment includes regular monitoring of vegetation health:</p>
<img src="https://www.fused.io/server/v1/realtime-shared/fsh_22OJjZ9tNKHaQ9NKVY6ewq/run/tiles/12/1207/1538?dtype_out_raster=png" alt="Vegetation Health Analysis">
<p>This data helps us make informed decisions about our environmental initiatives.</p>

<h2>Governance</h2>
<h3>Environmental Monitoring</h3>
<p>Our governance framework includes regular environmental monitoring:</p>
<img src="https://www.fused.io/server/v1/realtime-shared/fsh_22OJjZ9tNKHaQ9NKVY6ewq/run/tiles/12/1207/1538?dtype_out_raster=png" alt="Environmental Monitoring">
<p>We use satellite-based NDVI analysis to ensure compliance with our environmental commitments.</p>

<h3>Ethics and Compliance</h3>
<p>Detail your ethical business practices...</p>
"""

editor_tab, pdf_tab = st.tabs(["Editor", "PDF Preview"])

with editor_tab:
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
            with st.spinner('Generating PDF preview...'):
                html_content = f'''
                <!DOCTYPE html>
                <html lang="en">
                <body>
                    {st.session_state['editor_content']}
                </body>
                </html>
                '''
                pdf = fused.run("fsh_4VG6O74lPFHd2yFet0pyRf", html=html_content)
                content = pdf['pdf_bytes'].iloc[0]
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.download_button(
                    label="Download PDF",
                    data=content,
                    file_name="esg_report.pdf",
                    mime="application/pdf"
                )
            
            pdf_viewer(content)
            
        except Exception as e:
            st.error(f"Error generating PDF preview: {str(e)}")
    else:
        st.info("Start editing in the ESG Editor tab to see PDF preview")
