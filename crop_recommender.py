import streamlit as st
import pandas as pd
from PIL import Image
import random

# --- Step 1: Disease Database ---
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

# --- Step 2: Streamlit UI ---
st.title("🌱 Plant Disease Scanner & Treatment Recommender")

uploaded_file = st.file_uploader("📸 Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf", use_column_width=True)

    st.write("🔍 Scanning leaf for possible diseases...")

    # --- Step 3: Simulated ML Model Prediction ---
    # In reality, you would load a trained CNN model here
    predicted_disease = random.choice(list(disease_db.keys()))

    st.subheader(f"✅ Detected Disease: {predicted_disease}")

    # --- Step 4: Show Recommendation ---
    info = disease_db[predicted_disease]
    st.write(f"**Crop:** {info['Crop']}")
    st.write(f"**Symptoms:** {info['Symptoms']}")
    st.write(f"**Chemical Control:** {info['Chemical']}")
    st.write(f"**Trade Names:** {info['Trade Names']}")
    st.write(f"**Dosage & Interval:** {info['Dosage']}")
    st.write(f"**Alternative Practices:** {info['Alternatives']}")

    st.success("ℹ️ Always follow official label instructions approved by regulators (e.g., PCPB in Kenya).")
