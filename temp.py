import streamlit as st

# Define section names
sections = ["Section 1", "Section 2", "Section 3"]

st.title("Streamlit Scroll Indicator Sidebar")

# Create a sidebar for the scroll indicator
st.sidebar.title("Scroll Indicator")

# Create a list to store the markers
markers = []

# Add section names to the sidebar and create markers for each section
for section_name in sections:
    marker = st.sidebar.markdown(f" - [{section_name}](#{section_name.replace(' ', '-').lower()})")
    markers.append(marker)

# Create the content of your app with corresponding section headers
st.markdown("## Section 1", key="Section 1")
st.write("Content for Section 1")

st.markdown("## Section 2", key="Section 2")
st.write("Content for Section 2")

st.markdown("## Section 3", key="Section 3")
st.write("Content for Section 3")
