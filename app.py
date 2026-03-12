import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="AI Room Generator", page_icon="🏠", layout="centered")
st.title("🏠 AI Room Generator")
st.markdown("Transform your room or generate new designs using AI.")
st.divider()

HF_TOKEN = st.secrets["HF_TOKEN"]

tab1, tab2 = st.tabs(["🎨 Style Transfer", "✨ Generate Room"])

# ── STYLE TRANSFER ──
with tab1:
    st.subheader("Restyle Your Room")
    st.markdown("Upload a room photo and pick a style to transform it.")
    
    uploaded = st.file_uploader("Upload room image", type=["jpg","jpeg","png"], key="style")
    style = st.selectbox("Choose a style", [
        "modern minimalist", "bohemian", "industrial", "scandinavian",
        "mid-century modern", "rustic farmhouse", "art deco"
    ])
    
    if uploaded and st.button("Restyle Room"):
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Original", use_container_width=True)
        
        with st.spinner("Restyling..."):
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            
            prompt = f"Interior room design in {style} style, professional photography, high quality"
            
            response = requests.post(
                "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"inputs": prompt}
            )
            
            if response.status_code == 200:
                result_image = Image.open(io.BytesIO(response.content))
                st.image(result_image, caption=f"Restyled: {style}", use_container_width=True)
                
                buf2 = io.BytesIO()
                result_image.save(buf2, format="PNG")
                st.download_button("Download Result", buf2.getvalue(), "restyled_room.png", "image/png")
            else:
                st.error(f"Error: {response.text}")

# ── GENERATION ──
with tab2:
    st.subheader("Generate a Room Design")
    st.markdown("Describe your dream room and let AI create it.")
    
    room_type = st.selectbox("Room type", ["living room", "bedroom", "kitchen", "bathroom", "home office"])
    style2 = st.selectbox("Style", [
        "modern minimalist", "bohemian", "industrial", "scandinavian",
        "mid-century modern", "rustic farmhouse", "art deco"
    ], key="style2")
    extra = st.text_input("Any specific details? (optional)", placeholder="e.g. large windows, wood floors, plants")
    
    if st.button("Generate Room"):
        prompt = f"Interior design of a {style2} {room_type}, {extra}, professional photography, 4k, highly detailed"
        
        with st.spinner("Generating your room..."):
            response = requests.post(
                "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"inputs": prompt}
            )
            
            if response.status_code == 200:
                result_image = Image.open(io.BytesIO(response.content))
                st.image(result_image, caption=prompt, use_container_width=True)
                
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                st.download_button("Download Design", buf.getvalue(), "room_design.png", "image/png")
            else:
                st.error(f"Error: {response.text}")