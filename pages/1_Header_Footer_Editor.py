import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import helpers
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.template_manager import TemplateManager
from helpers.header_footer_processor import create_processor_from_preset

# Page configuration
st.set_page_config(page_title="Header/Footer Editor", page_icon="✏️", layout="wide")

# Title
st.title("✏️ Header & Footer Template Editor")
st.write("Create and customize header/footer templates with logo support")

# Initialize template manager
template_manager = TemplateManager()

# Sidebar - Preset selection and management
with st.sidebar:
    st.header("📋 Template Presets")

    preset_names = template_manager.get_preset_names()
    current_preset = template_manager.get_current_preset()

    selected_preset = st.selectbox(
        "Select preset to edit:",
        preset_names,
        index=preset_names.index(current_preset) if current_preset in preset_names else 0
    )

    st.divider()

    # Preset actions
    st.subheader("Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True, help="Save changes to template"):
            if template_manager.save_template():
                st.success("✅ Saved!")
            else:
                st.error("❌ Save failed")

    with col2:
        if st.button("↩️ Reset", use_container_width=True, help="Reload from file"):
            template_manager.template_data = template_manager._load_template()
            st.success("↩️ Reset!")
            st.rerun()

    st.divider()

    # Set as default
    if st.button("⭐ Set as Default Preset", use_container_width=True):
        template_manager.set_current_preset(selected_preset)
        template_manager.save_template()
        st.success(f"✅ '{selected_preset}' is now the default!")

# Main content - Edit preset
st.header(f"Editing: {selected_preset}")

# Get preset configuration
preset = template_manager.get_preset(selected_preset)

# Preset metadata
col1, col2 = st.columns([3, 1])
with col1:
    preset_description = st.text_input(
        "Description",
        value=preset.get('description', ''),
        help="Brief description of this preset"
    )
    preset['description'] = preset_description

with col2:
    preset_enabled = st.checkbox(
        "Enabled",
        value=preset.get('enabled', True),
        help="Enable headers/footers for this preset"
    )
    preset['enabled'] = preset_enabled

st.divider()

# Header configuration
st.subheader("📄 Header Configuration")
header_cols = st.columns(3)

with header_cols[0]:
    st.caption("**Left**")
    header_left = st.text_input(
        "Header Left",
        value=preset.get('header', {}).get('left', ''),
        label_visibility="collapsed",
        placeholder="e.g., {title}",
        key="header_left"
    )

with header_cols[1]:
    st.caption("**Center**")
    header_center = st.text_input(
        "Header Center",
        value=preset.get('header', {}).get('center', ''),
        label_visibility="collapsed",
        placeholder="e.g., {subtitle}",
        key="header_center"
    )

with header_cols[2]:
    st.caption("**Right**")
    header_right = st.text_input(
        "Header Right",
        value=preset.get('header', {}).get('right', ''),
        label_visibility="collapsed",
        placeholder="e.g., {date}",
        key="header_right"
    )

st.divider()

# Footer configuration
st.subheader("📄 Footer Configuration")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.caption("**Left**")
    footer_left = st.text_input(
        "Footer Left",
        value=preset.get('footer', {}).get('left', ''),
        label_visibility="collapsed",
        placeholder="e.g., Page {page} of {total}",
        key="footer_left"
    )

with footer_cols[1]:
    st.caption("**Center**")
    footer_center = st.text_input(
        "Footer Center",
        value=preset.get('footer', {}).get('center', ''),
        label_visibility="collapsed",
        placeholder="e.g., {company}",
        key="footer_center"
    )

with footer_cols[2]:
    st.caption("**Right**")
    footer_right = st.text_input(
        "Footer Right",
        value=preset.get('footer', {}).get('right', ''),
        label_visibility="collapsed",
        placeholder="e.g., {author}",
        key="footer_right"
    )

st.divider()

# Logo configuration
st.subheader("🖼️ Logo Configuration")

logo_config = preset.get('logo', {})

col1, col2 = st.columns([1, 3])
with col1:
    logo_enabled = st.checkbox(
        "Enable Logo",
        value=logo_config.get('enabled', False),
        help="Include logo in header/footer"
    )

with col2:
    if logo_enabled:
        logo_path = st.text_input(
            "Logo Path",
            value=logo_config.get('path', 'helpers/logo.svg'),
            help="Relative path to logo file (SVG, PNG, JPG supported)"
        )
    else:
        logo_path = logo_config.get('path', 'helpers/logo.svg')

if logo_enabled:
    col1, col2, col3 = st.columns(3)

    with col1:
        logo_position_area = st.selectbox(
            "Position Area",
            ["Header", "Footer"],
            index=0 if logo_config.get('position', 'header_left').startswith('header') else 1
        )

    with col2:
        logo_position_side = st.selectbox(
            "Position Side",
            ["Left", "Center", "Right"],
            index=["Left", "Center", "Right"].index(
                logo_config.get('position', 'header_left').split('_')[1].capitalize()
                if '_' in logo_config.get('position', 'header_left') else "Left"
            )
        )

    # Construct position string
    logo_position = f"{logo_position_area.lower()}_{logo_position_side.lower()}"

    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer
        st.info(f"Position: `{logo_position}`")

    col1, col2 = st.columns(2)
    with col1:
        logo_height = st.text_input(
            "Logo Height",
            value=logo_config.get('height', '0.5cm'),
            help="Height in LaTeX units (e.g., 0.5cm, 10mm, 0.2in)"
        )

    with col2:
        logo_width = st.text_input(
            "Logo Width",
            value=logo_config.get('width', ''),
            help="Width in LaTeX units (leave empty for auto)"
        )
else:
    logo_path = logo_config.get('path', 'helpers/logo.svg')
    logo_position = logo_config.get('position', 'header_left')
    logo_height = logo_config.get('height', '0.5cm')
    logo_width = logo_config.get('width', '')

st.divider()

# Style configuration
st.subheader("🎨 Style Configuration")

style_config = preset.get('style', {})

col1, col2 = st.columns(2)
with col1:
    separator_line = st.checkbox(
        "Separator Lines",
        value=style_config.get('separator_line', True),
        help="Add separator lines above header and below footer"
    )

with col2:
    font_size = st.selectbox(
        "Font Size",
        ["8pt", "9pt", "10pt", "11pt", "12pt"],
        index=["8pt", "9pt", "10pt", "11pt", "12pt"].index(style_config.get('font_size', '10pt'))
    )

st.divider()

# Available variables reference
with st.expander("📖 Available Variables Reference"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Document Variables:**
        - `{title}` - Document title
        - `{subtitle}` - Document subtitle
        - `{author}` - Author name
        - `{company}` - Company/organization
        - `{version}` - Document version
        """)

    with col2:
        st.markdown("""
        **Auto Variables:**
        - `{date}` - Current date (YYYY-MM-DD)
        - `{time}` - Current time (HH:MM)
        - `{page}` - Current page number
        - `{total}` - Total page count
        """)

st.divider()

# Preview section
st.subheader("👁️ Preview")

# Get default variables for preview
default_vars = template_manager.get_default_variables()
preview_vars = {
    'title': st.session_state.get('preview_title', default_vars.get('title', 'My Document')),
    'author': st.session_state.get('preview_author', default_vars.get('author', 'John Doe')),
    'company': st.session_state.get('preview_company', default_vars.get('company', 'Acme Corp')),
}

# Update preset with current values before preview
preset['header'] = {'left': header_left, 'center': header_center, 'right': header_right}
preset['footer'] = {'left': footer_left, 'center': footer_center, 'right': footer_right}
preset['logo'] = {
    'enabled': logo_enabled,
    'path': logo_path,
    'position': logo_position,
    'height': logo_height,
    'width': logo_width
}
preset['style'] = {'separator_line': separator_line, 'font_size': font_size}

# Generate preview
processor = create_processor_from_preset(selected_preset, template_manager)
preview = processor.preview_header_footer(preview_vars)

# Display preview
col1, col2 = st.columns(2)

with col1:
    st.write("**Header:**")
    header_preview_cols = st.columns(3)
    with header_preview_cols[0]:
        st.caption("Left")
        st.code(preview['header_left'] or "(empty)", language=None)
    with header_preview_cols[1]:
        st.caption("Center")
        st.code(preview['header_center'] or "(empty)", language=None)
    with header_preview_cols[2]:
        st.caption("Right")
        st.code(preview['header_right'] or "(empty)", language=None)

with col2:
    st.write("**Footer:**")
    footer_preview_cols = st.columns(3)
    with footer_preview_cols[0]:
        st.caption("Left")
        st.code(preview['footer_left'] or "(empty)", language=None)
    with footer_preview_cols[1]:
        st.caption("Center")
        st.code(preview['footer_center'] or "(empty)", language=None)
    with footer_preview_cols[2]:
        st.caption("Right")
        st.code(preview['footer_right'] or "(empty)", language=None)

# Update preset in template manager
template_manager.update_preset(selected_preset, preset)

# Save button at the bottom
st.divider()
if st.button("💾 Save All Changes", type="primary", use_container_width=True):
    if template_manager.save_template():
        st.success("✅ Template saved successfully!")
    else:
        st.error("❌ Failed to save template")
