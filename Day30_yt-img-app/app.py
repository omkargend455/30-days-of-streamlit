import streamlit as st
from urllib.parse import urlparse, parse_qs

# App Title
st.title('🖼️ yt-img-app')
st.header('YouTube Thumbnail Image Extractor')

# About Section
with st.expander('About this app'):
    st.write('Extracts thumbnail images from any YouTube video URL.')

# Sidebar Settings
st.sidebar.header('Settings')
img_dict = {
    'Max': 'maxresdefault',
    'High': 'hqdefault',
    'Medium': 'mqdefault',
    'Standard': 'sddefault'
}

selected_quality = st.sidebar.selectbox(
    'Select image quality',
    list(img_dict.keys())
)

img_quality = img_dict[selected_quality]

# Input
yt_url = st.text_input(
    'Paste YouTube URL',
    'https://youtu.be/JwSS70SZdyM'
)

# Function to extract video ID (robust version)
def get_ytid(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]

    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]

    return None

# Main Logic
if yt_url:
    ytid = get_ytid(yt_url)

    if ytid:
        yt_img = f'https://img.youtube.com/vi/{ytid}/{img_quality}.jpg'
        
        st.image(yt_img, caption="Thumbnail Preview")
        st.success("Thumbnail extracted successfully!")
        st.write("🔗 Image URL:", yt_img)

        # Bonus: Download button
        st.markdown(f"[⬇️ Download Thumbnail]({yt_img})")

    else:
        st.error("❌ Invalid YouTube URL")

else:
    st.info("☝️ Enter a YouTube URL to begin")