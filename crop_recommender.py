import streamlit as st
import random
from PIL import Image

# --- Disease Database (Sample) ---
disease_db = {
    "Early Blight": {
        "Crop": "Tomato",
        "Symptoms": "Dark concentric rings on older leaves, defoliation",
        "Chemical": "Mancozeb, Chlorothalonil",
        "Trade Names": "Dithane M-45, Bravo",
        "Dosage": "20–30 g / 20L every 7–10 days",
        "Alternatives": "Crop rotation, remove debris, resistant varieties"
    },
    "Late Blight": {
        "Crop": "Tomato",
        "Symptoms": "Water-soaked lesions, white mold underside of leaves",
        "Chemical": "Metalaxyl + Mancozeb",
        "Trade Names": "Ridomil Gold",
        "Dosage": "25 g / 20L every 7–10 days",
        "Alternatives": "Stake plants, avoid overhead irrigation"
    },
    "Powdery Mildew": {
        "Crop": "Tomato",
        "Symptoms": "White powdery patches on leaves",
        "Chemical": "Sulfur, Trifloxystrobin",
        "Trade Names": "Microthiol, Flint",
        "Dosage": "30 g / 20L",
        "Alternatives": "Improve ventilation, avoid excess nitrogen"
    }
}

# --- App Title ---
st.title("🌱 Plant Disease Scanner (Upload or Webcam)")

# --- Step 1: Input Options ---
st.subheader("📸 Choose how to provide a leaf image")
option = st.radio("Select input method:", ["Upload from computer", "Use webcam"])

uploaded_image = None

if option == "Upload from computer":
    uploaded_file = st.file_uploader("📂 Upload a leaf image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Leaf", use_column_width=True)

elif option == "Use webcam":
    img_file_buffer = st.camera_input("📸 Take a picture of the leaf")
    if img_file_buffer is not None:
        uploaded_image = Image.open(img_file_buffer)
        st.image(uploaded_image, caption="Captured Leaf", use_column_width=True)

# --- Step 2: Run Detection if Image Exists ---
if uploaded_image is not None:
    st.write("🔍 Scanning leaf for possible diseases...")

    # Simulated detection (replace later with CNN model)
    predicted_disease = random.choice(list(disease_db.keys()))

    st.subheader(f"✅ Detected Disease: {predicted_disease}")

    # --- Step 3: Show Recommendation ---
    info = disease_db[predicted_disease]
    st.write(f"**Crop:** {info['Crop']}")
    st.write(f"**Symptoms:** {info['Symptoms']}")
    st.write(f"**Chemical Control:** {info['Chemical']}")
    st.write(f"**Trade Names:** {info['Trade Names']}")
    st.write(f"**Dosage & Interval:** {info['Dosage']}")
    st.write(f"**Alternative Practices:** {info['Alternatives']}")

    st.success("ℹ️ Always follow official label instructions approved by regulators.")

