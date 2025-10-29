import streamlit as st
import random
from PIL import Image
import pandas as pd
from streamlit_geolocation import streamlit_geolocation


# --- Disease Database (Sample for Potato) ---
disease_db = {
    "Early Blight": {
        "Crop": "Potato",
        "Symptoms": "Dark concentric rings on older leaves, yellowing and defoliation",
        "Chemical": "Mancozeb, Chlorothalonil",
        "Trade Names": "Dithane M-45, Bravo",
        "Dosage": "20–30 g / 20L every 7–10 days",
        "Alternatives": "Crop rotation, remove debris, resistant varieties"
    },
    "Late Blight": {
        "Crop": "Potato",
        "Symptoms": "Water-soaked lesions, white mold underside of leaves",
        "Chemical": "Metalaxyl + Mancozeb",
        "Trade Names": "Ridomil Gold",
        "Dosage": "25 g / 20L every 7–10 days",
        "Alternatives": "Ensure good drainage, avoid overhead irrigation"
    },
    "Black Scurf": {
        "Crop": "Potato",
        "Symptoms": "Dark hard patches on tubers, poor sprouting",
        "Chemical": "Flutolanil, Pencycuron",
        "Trade Names": "Monceren, Emesto Silver",
        "Dosage": "Use as seed treatment before planting",
        "Alternatives": "Use certified seed, rotate with non-host crops"
    }
}

# --- Agrovet Supplier Database (Simplified Example) ---
suppliers = {
    "Kinangop": [
        {"name": "Engineer Agrovet", "phone": "07XX111222", "lat": -0.682, "lon": 36.650},
        {"name": "Gathara Agrovet", "phone": "07XX222333", "lat": -0.690, "lon": 36.660},
        {"name": "Magumu Agrovet", "phone": "07XX333444", "lat": -0.700, "lon": 36.640}
    ],
    "Ol Kalou": [
        {"name": "Karau Agrovet", "phone": "07XX444555", "lat": -0.270, "lon": 36.380},
        {"name": "Mirangine Agrovet", "phone": "07XX555666", "lat": -0.330, "lon": 36.400},
        {"name": "Rurii Agrovet", "phone": "07XX666777", "lat": -0.310, "lon": 36.420}
    ],
    "Ndaragwa": [
        {"name": "Shamata Agrovet", "phone": "07XX777888", "lat": -0.050, "lon": 36.600},
        {"name": "Leshau Agrovet", "phone": "07XX888999", "lat": -0.040, "lon": 36.590},
        {"name": "Kiriita Agrovet", "phone": "07XX999000", "lat": -0.060, "lon": 36.620}
    ]
}

# --- App Title ---
st.title("🥔 Image Classification System for Potato Disease Detection, Chemical Recommendation, and Agrovet Connection in Nyandarua County")

st.markdown("This system helps farmers detect potato leaf diseases, get chemical recommendations, and locate nearby agrovets in Nyandarua County.")

# --- Step 1: Image Input ---
st.subheader("📸 Provide a Potato Leaf Image")
option = st.radio("Select input method:", ["Upload from computer", "Use webcam"])

uploaded_image = None
if option == "Upload from computer":
    uploaded_file = st.file_uploader("📂 Upload a leaf image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Leaf", use_column_width=True)
elif option == "Use webcam":
    img_file_buffer = st.camera_input("📸 Take a picture of the potato leaf")
    if img_file_buffer:
        uploaded_image = Image.open(img_file_buffer)
        st.image(uploaded_image, caption="Captured Leaf", use_column_width=True)

# --- Step 2: Disease Detection Simulation ---
if uploaded_image:
    st.write("🔍 Scanning leaf for possible diseases...")
    predicted_disease = random.choice(list(disease_db.keys()))  # Simulated classification
    info = disease_db[predicted_disease]

    st.subheader(f"✅ Detected Disease: {predicted_disease}")
    st.write(f"**Crop:** {info['Crop']}")
    st.write(f"**Symptoms:** {info['Symptoms']}")
    st.write(f"**Chemical Control:** {info['Chemical']}")
    st.write(f"**Trade Names:** {info['Trade Names']}")
    st.write(f"**Dosage & Interval:** {info['Dosage']}")
    st.write(f"**Alternative Practices:** {info['Alternatives']}")
    st.success("ℹ️ Always follow official label instructions and local agricultural guidelines.")

    st.divider()

    # --- Step 3: Detect GPS Location ---
    st.subheader("📍 Detect My Location Using GPS")
    st.write("Click the button below to get your current location:")
    location = streamlit_geolocation()

    if location and location.get("latitude") and location.get("longitude"):
        lat = location["latitude"]
        lon = location["longitude"]

    # ✅ Show coordinates
        st.success(f"📍 Your Coordinates: Latitude {lat:.4f}, Longitude {lon:.4f}")

        # ✅ Display user location on map
        df = pd.DataFrame([[lat, lon]], columns=["lat", "lon"])
        st.map(df, zoom=10)

        # --- Step 4: Find Nearby Agrovets (Simulated) ---
        st.subheader("🏪 Nearby Agrovets in Nyandarua County")

        # ✅ Choose a random constituency
        random_constituency = random.choice(list(suppliers.keys()))
        available_agrovets = suppliers[random_constituency]

        # ✅ Select up to 4 agrovets (if fewer exist, show all)
        num_to_show = min(4, len(available_agrovets))
        nearby_agrovets = random.sample(available_agrovets, k=num_to_show)

        for i, agrovet in enumerate(nearby_agrovets, start=1):
            st.markdown(f"**{i}. {agrovet['name']}**  \n📞 {agrovet['phone']}  \n📍 Constituency: {random_constituency}")

    else:
        st.info("⚠️ Click the button above to detect your location.")
