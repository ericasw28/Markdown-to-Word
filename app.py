import streamlit as st
import os
from helpers import convert_to_docx, convert_to_pdf
from helpers.template_manager import TemplateManager
from helpers.header_footer_processor import create_processor_from_preset

# Page configuration
st.set_page_config(page_title="Markdown Converter", page_icon="📄", layout="centered")

# Title and description
st.title("📄 Markdown to DOCX/PDF Converter")
st.write("Upload your Markdown files and convert them to DOCX or PDF format")

# File uploader
uploaded_files = st.file_uploader(
    "Choose Markdown file(s)",
    type=['md', 'markdown'],
    accept_multiple_files=True,
    help="Upload one or more Markdown files to convert"
)

# Main app logic
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    # Display file names
    st.subheader("Uploaded Files:")
    for file in uploaded_files:
        st.write(f"- {file.name}")

    st.divider()

    # Conversion options
    st.subheader("Conversion Options")
    output_format = st.radio(
        "Select output format:",
        ["DOCX (Word Document)", "PDF (Portable Document Format)"],
        horizontal=True
    )

    # Header/Footer settings for PDF
    use_header_footer = False
    header_footer_preset = None
    custom_variables = {}

    if "PDF" in output_format:
        st.divider()

        with st.expander("📑 Header & Footer Settings", expanded=False):
            # Initialize template manager
            template_manager = TemplateManager()

            # Enable/disable headers and footers
            use_header_footer = st.checkbox(
                "Enable headers and footers",
                value=True,
                help="Add headers and footers to your PDF document"
            )

            if use_header_footer:
                # Get available presets
                preset_names = template_manager.get_preset_names()
                current_preset = template_manager.get_current_preset()

                # Preset selector
                col1, col2 = st.columns([3, 1])
                with col1:
                    header_footer_preset = st.selectbox(
                        "Select preset:",
                        preset_names,
                        index=preset_names.index(current_preset) if current_preset in preset_names else 0,
                        help="Choose a header/footer template preset"
                    )

                with col2:
                    if st.button("💾 Save as Default", help="Save this preset as default"):
                        template_manager.set_current_preset(header_footer_preset)
                        template_manager.save_template()
                        st.success("✅ Saved!")

                # Show preset description
                preset = template_manager.get_preset(header_footer_preset)
                if preset.get('description'):
                    st.caption(f"*{preset['description']}*")

                st.divider()

                # Custom variables section
                st.write("**Document Variables:**")
                st.caption("These values will be used in the header/footer template")

                col1, col2 = st.columns(2)
                with col1:
                    custom_variables['title'] = st.text_input(
                        "Title",
                        value=template_manager.get_default_variables().get('title', 'Untitled Document'),
                        help="Document title (use {title} in template)"
                    )
                    custom_variables['author'] = st.text_input(
                        "Author",
                        value=template_manager.get_default_variables().get('author', 'Anonymous'),
                        help="Author name (use {author} in template)"
                    )

                with col2:
                    custom_variables['company'] = st.text_input(
                        "Company",
                        value=template_manager.get_default_variables().get('company', ''),
                        help="Company/organization name (use {company} in template)"
                    )
                    custom_variables['version'] = st.text_input(
                        "Version",
                        value=template_manager.get_default_variables().get('version', '1.0'),
                        help="Document version (use {version} in template)"
                    )

                # Preview section
                with st.expander("👁️ Preview Header/Footer", expanded=False):
                    processor = create_processor_from_preset(header_footer_preset, template_manager)
                    preview = processor.preview_header_footer(custom_variables)

                    st.write("**Header:**")
                    header_cols = st.columns(3)
                    with header_cols[0]:
                        st.caption("Left")
                        st.code(preview['header_left'] or "(empty)", language=None)
                    with header_cols[1]:
                        st.caption("Center")
                        st.code(preview['header_center'] or "(empty)", language=None)
                    with header_cols[2]:
                        st.caption("Right")
                        st.code(preview['header_right'] or "(empty)", language=None)

                    st.write("**Footer:**")
                    footer_cols = st.columns(3)
                    with footer_cols[0]:
                        st.caption("Left")
                        st.code(preview['footer_left'] or "(empty)", language=None)
                    with footer_cols[1]:
                        st.caption("Center")
                        st.code(preview['footer_center'] or "(empty)", language=None)
                    with footer_cols[2]:
                        st.caption("Right")
                        st.code(preview['footer_right'] or "(empty)", language=None)

                    st.info("💡 **Note:** {page} and {total} will show actual page numbers in the PDF")

    st.divider()

    # Convert button
    if st.button("🔄 Convert Files", type="primary", use_container_width=True):
        with st.spinner("Converting files..."):
            for uploaded_file in uploaded_files:
                # Read the markdown content
                markdown_content = uploaded_file.read().decode('utf-8')
                file_base_name = os.path.splitext(uploaded_file.name)[0]

                try:
                    if "DOCX" in output_format:
                        # Convert to DOCX
                        output_buffer = convert_to_docx(markdown_content)
                        output_filename = f"{file_base_name}.docx"
                        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    else:
                        # Convert to PDF with header/footer settings
                        output_buffer = convert_to_pdf(
                            markdown_content,
                            use_header_footer=use_header_footer,
                            header_footer_preset=header_footer_preset,
                            custom_variables=custom_variables if custom_variables else None
                        )
                        output_filename = f"{file_base_name}.pdf"
                        mime_type = "application/pdf"

                    # Download button
                    st.download_button(
                        label=f"⬇️ Download {output_filename}",
                        data=output_buffer,
                        file_name=output_filename,
                        mime=mime_type,
                        use_container_width=True
                    )
                    st.success(f"✅ {uploaded_file.name} converted successfully!")

                except Exception as e:
                    st.error(f"❌ Error converting {uploaded_file.name}: {str(e)}")

else:
    st.info("👆 Please upload Markdown file(s) to begin conversion")


# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This app converts Markdown files to:
    - **DOCX**: Microsoft Word format
    - **PDF**: Portable Document Format

    **Supported Markdown features:**
    - Headers (H1-H6)
    - Paragraphs
    - Lists (ordered & unordered)
    - Code blocks
    - Tables
    - Bold & italic text
    - Hyperlinks
    """)

    st.divider()

    st.header("📝 Instructions")
    st.write("""
    1. Upload one or more `.md` files
    2. Select output format (DOCX or PDF)
    3. Click "Convert Files"
    4. Download your converted files
    """)
