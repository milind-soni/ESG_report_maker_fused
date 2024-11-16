import micropip
await micropip.install('streamlit-quill')

import streamlit as st
from streamlit_quill import st_quill

st.title("Rich Text Editor with Images")

# Example image URLs (replace with your actual images)
sample_images = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/200/300",
]

# Method 1: Using HTML content
html_content = f"""
<h2>Welcome to the Editor</h2>
<p>Here's an image inserted via HTML:</p>
<img src="{sample_images[0]}" alt="Sample image 1">
<p>You can continue editing from here...</p>
"""

# Method 2: Using Delta format (Quill's native format)
delta_content = {
    "ops": [
        {"insert": "Here's another way to insert images:\n"},
        {"insert": {"image": sample_images[1]}},
        {"insert": "\nContinue editing...\n"}
    ]
}

# Add buttons to choose content format
content_type = st.radio("Choose content format:", ["HTML", "Delta", "Empty"])

# Initialize editor with selected content
if content_type == "HTML":
    initial_content = html_content
elif content_type == "Delta":
    initial_content = delta_content
else:
    initial_content = ""

# Create the Quill editor
content = st_quill(
    value=initial_content,
    placeholder="Start typing here...",
    html=content_type == "HTML",  # Set HTML mode based on content type
    toolbar=[
        [{'font': []}, {'size': []}],
        ['bold', 'italic', 'underline', 'strike'],
        [{'color': []}, {'background': []}],
        [{'align': []}, {'direction': 'rtl'}],
        [{'script': 'sub'}, {'script': 'super'}],
        ['blockquote', 'code-block'],
        [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
        [{'header': [1, 2, 3, 4, 5, 6, False]}],
        ['link', 'image', 'video'],
        ['clean']
    ],
    key="quill_editor"
)

# Add a button to programmatically insert an image at cursor position
if st.button("Insert Random Cat Image"):
    st.write("Note: Direct cursor manipulation isn't supported in Streamlit-Quill. "
             "You'll need to refresh with new content to add images programmatically.")
    
    # If using HTML mode
    new_html = f"""
    {content if content else ''}
    <img src="https://placekitten.com/{200 + st.session_state.get('counter', 0)}/200" alt="Random cat">
    """
    
    # Increment counter for different images
    st.session_state['counter'] = st.session_state.get('counter', 0) + 1
    
    # Show the new content that can be copied
    st.code(new_html, language="html")

# Display editor's content as you type
if content:
    st.write("### Preview:")
    st.write(content, unsafe_allow_html=True)

# Add example code for reference
with st.expander("Show Code Examples"):
    st.code("""
# Example HTML insertion:
html_content = '''
<h2>Title</h2>
<p>Text before image</p>
<img src="your_image_url.jpg" alt="Description">
<p>Text after image</p>
'''

# Example Delta format insertion:
delta_content = {
    "ops": [
        {"insert": "Text before image\\n"},
        {"insert": {"image": "your_image_url.jpg"}},
        {"insert": "\\nText after image\\n"}
    ]
}
""", language="python")
