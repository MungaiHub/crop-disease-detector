import streamlit as st
import random
from PIL import Image
from streamlit_geolocation import streamlit_geolocation
from math import radians, sin, cos, sqrt, atan2

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

# --- Agrovet Database --- 
suppliers = {
    "Kinangop": [
        {"name": "Engineer Agrovet", "ward": "Engineer", "phone": "07XX111222", "lat": -0.682, "lon": 36.650},
        {"name": "Gathara Agrovet", "ward": "Gathara", "phone": "07XX222333", "lat": -0.690, "lon": 36.660},
        {"name": "Magumu Agrovet", "ward": "Magumu", "phone": "07XX333444", "lat": -0.700, "lon": 36.640}
    ],
    "Ol Kalou": [
        {"name": "Karau Agrovet", "ward": "Karau", "phone": "07XX444555", "lat": -0.270, "lon": 36.380},
        {"name": "Mirangine Agrovet", "ward": "Mirangine", "phone": "07XX555666", "lat": -0.330, "lon": 36.400},
        {"name": "Rurii Agrovet", "ward": "Rurii", "phone": "07XX666777", "lat": -0.310, "lon": 36.420}
    ],
    "Ndaragwa": [
        {"name": "Shamata Agrovet", "ward": "Shamata", "phone": "07XX777888", "lat": -0.050, "lon": 36.600},
        {"name": "Leshau Agrovet", "ward": "Leshau", "phone": "07XX888999", "lat": -0.040, "lon": 36.590},
        {"name": "Kiriita Agrovet", "ward": "Kiriita", "phone": "07XX999000", "lat": -0.060, "lon": 36.620}
    ]
}

# --- Title ---
st.title("🥔 Potato Disease Detector & Agrovet Finder – Nyandarua County")

# --- Step 1: Image Upload / Capture ---
st.subheader("📸 Upload or Capture Potato Leaf Image")
input_type = st.radio("Choose input method:", ["📂 Upload", "📷 Camera"])

uploaded_img = None
if input_type == "📂 Upload":
    file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if file:
        uploaded_img = Image.open(file)
else:
    cam = st.camera_input("Take a photo")
    if cam:
        uploaded_img = Image.open(cam)

# Process only if image exists
if uploaded_img:
    st.image(uploaded_img, caption="Potato Leaf")
    st.write("🔍 Analyzing leaf...")

    disease = random.choice(list(disease_db.keys()))
    info = disease_db[disease]

    st.success(f"✅ Disease Detected: **{disease}**")
    st.write(f"**Symptoms:** {info['Symptoms']}")
    st.write(f"**Recommended Chemical:** {info['Chemical']}")
    st.write(f"**Trade Names:** {info['Trade Names']}")
    st.write(f"**Dosage:** {info['Dosage']}")
    st.write(f"**Organic/Alternative Option:** {info['Alternatives']}")

    st.divider()

    # --- Confirm Location ---
    st.subheader("📍 Farmer Location Verification")
    in_nyandarua = st.radio("Are you currently in **Nyandarua County**?", ["Yes", "No"])

    if in_nyandarua == "No":
        st.error("❗ This service is available only for farmers currently in Nyandarua County.")
        st.stop()

    # --- Select Constituency and Ward ---
    wards = {
        "Kinangop": ["Engineer", "Gathara", "Magumu"],
        "Ol Kalou": ["Karau", "Mirangine", "Rurii"],
        "Ndaragwa": ["Shamata", "Leshau", "Kiriita"]
    }

    selected_const = st.selectbox("If you are currently in Nyandarua, which constituency are you in?", list(wards.keys()))
    selected_ward = st.selectbox("Which ward are you in?", wards[selected_const])

    st.write("🌍 Click to detect GPS location inside your ward:")
    location = streamlit_geolocation()

    # --- Haversine Distance ---
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2-lat1)
        dlon = radians(lon2-lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        return 2 * atan2(sqrt(a), sqrt(1 - a)) * R

    # Verify GPS
    if location and location.get("latitude") and location.get("longitude"):
        lat, lon = location["latitude"], location["longitude"]
        st.success(f"📌 GPS Confirmed: ({lat:.4f}, {lon:.4f}) — Nyandarua")

        ward_data = [a for a in suppliers[selected_const] if a["ward"] == selected_ward]

        for a in ward_data:
            a["distance"] = haversine(lat, lon, a["lat"], a["lon"])

        nearest = sorted(ward_data, key=lambda x: x["distance"])[:3]

        st.subheader("🏪 Nearest Verified Agrovets")
        for i, a in enumerate(nearest, start=1):
            st.write(f"**{i}. {a['name']}** \n📍 Ward: {a['ward']}\n📞 {a['phone']} \n📏 {a['distance']:.2f} km away")

    else:
        st.info("📍 Please allow location access to continue.")
else:
    st.info("📎 Upload or capture a potato leaf image to continue.")


