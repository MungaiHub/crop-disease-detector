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

# --- Supplier Database by Constituency & Ward ---
suppliers = {
    "Kinangop": {
        "Engineer": [{"name": "Engineer Agrovet", "phone": "07XX111222", "location": "Engineer Town"}],
        "Gathara": [{"name": "Gathara Agrovet", "phone": "07XX222333", "location": "Gathara Center"}],
        "Githabai": [{"name": "Githabai Agrovet", "phone": "07XX333444", "location": "Githabai"}],
        "Magumu": [{"name": "Magumu Agrovet", "phone": "07XX444555", "location": "Magumu Market"}],
        "Murungaru": [{"name": "Murungaru Agrovet", "phone": "07XX555666", "location": "Murungaru"}],
        "Njabini/Kiburu": [{"name": "Njabini Agrovet", "phone": "07XX666777", "location": "Njabini"}],
        "North Kinangop": [{"name": "North Kinangop Agrovet", "phone": "07XX777888", "location": "North Kinangop"}],
        "Nyakio": [{"name": "Nyakio Agrovet", "phone": "07XX888999", "location": "Nyakio"}]
    },
    "Kipipiri": {
        "Wanjohi": [{"name": "Wanjohi Agrovet", "phone": "07XX111444", "location": "Wanjohi"}],
        "Kipipiri": [{"name": "Kipipiri Agrovet", "phone": "07XX222555", "location": "Kipipiri Center"}],
        "Geta": [{"name": "Geta Agrovet", "phone": "07XX333666", "location": "Geta"}],
        "Githioro": [{"name": "Githioro Agrovet", "phone": "07XX444777", "location": "Githioro"}]
    },
    "Ol Kalou": {
        "Karau": [{"name": "Karau Agrovet", "phone": "07XX555111", "location": "Karau Market"}],
        "Kanjuiri Range": [{"name": "Kanjuiri Agrovet", "phone": "07XX666222", "location": "Kanjuiri"}],
        "Mirangine": [{"name": "Mirangine Agrovet", "phone": "07XX777333", "location": "Mirangine Center"}],
        "Kaimbaga": [{"name": "Kaimbaga Agrovet", "phone": "07XX888444", "location": "Kaimbaga"}],
        "Rurii": [{"name": "Rurii Agrovet", "phone": "07XX999555", "location": "Rurii"}]
    },
    "Ol Jorok": {
        "Gathanji": [{"name": "Gathanji Agrovet", "phone": "07XX123456", "location": "Gathanji"}],
        "Gatimu": [{"name": "Gatimu Agrovet", "phone": "07XX234567", "location": "Gatimu"}],
        "Weru": [{"name": "Weru Agrovet", "phone": "07XX345678", "location": "Weru"}],
        "Charagita": [{"name": "Charagita Agrovet", "phone": "07XX456789", "location": "Charagita"}]
    },
    "Ndaragwa": {
        "Leshau/Pondo": [{"name": "Leshau Agrovet", "phone": "07XX567890", "location": "Leshau"}],
        "Kiriita": [{"name": "Kiriita Agrovet", "phone": "07XX678901", "location": "Kiriita"}],
        "Central": [{"name": "Central Agrovet", "phone": "07XX789012", "location": "Central Ndaragwa"}],
        "Shamata": [{"name": "Shamata Agrovet", "phone": "07XX890123", "location": "Shamata"}]
    }
}

# --- App Title ---
st.title("🌱 AI-Powered Crop Disease & Recommendation System")

# --- Step 1: Image Input ---
st.subheader("📸 Provide a leaf image")
option = st.radio("Select input method:", ["Upload from computer", "Use webcam"])

uploaded_image = None
if option == "Upload from computer":
    uploaded_file = st.file_uploader("📂 Upload a leaf image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Leaf", use_column_width=True)
elif option == "Use webcam":
    img_file_buffer = st.camera_input("📸 Take a picture of the leaf")
    if img_file_buffer:
        uploaded_image = Image.open(img_file_buffer)
        st.image(uploaded_image, caption="Captured Leaf", use_column_width=True)

# --- Step 2: Detection Simulation ---
if uploaded_image:
    st.write("🔍 Scanning leaf for possible diseases...")
    predicted_disease = random.choice(list(disease_db.keys()))  # Simulated detection
    info = disease_db[predicted_disease]

    st.subheader(f"✅ Detected Disease: {predicted_disease}")
    st.write(f"**Crop:** {info['Crop']}")
    st.write(f"**Symptoms:** {info['Symptoms']}")
    st.write(f"**Chemical Control:** {info['Chemical']}")
    st.write(f"**Trade Names:** {info['Trade Names']}")
    st.write(f"**Dosage & Interval:** {info['Dosage']}")
    st.write(f"**Alternative Practices:** {info['Alternatives']}")
    st.success("ℹ️ Always follow official label instructions approved by regulators.")

    # --- Step 3: Location & Suppliers ---
    st.subheader("📍 Find Agrovet Suppliers Near You")
    constituency = st.selectbox("Select your Constituency:", list(suppliers.keys()))
    ward = st.selectbox("Select your Ward:", list(suppliers[constituency].keys()))

    st.write("### Available Agrovets:")
    for agrovet in suppliers[constituency][ward]:
        st.write(f"**{agrovet['name']}** - 📍 {agrovet['location']} - 📞 {agrovet['phone']}")
