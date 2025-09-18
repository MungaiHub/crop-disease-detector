
import streamlit as st
from PIL import Image, ImageStat
import numpy as np
import io

st.set_page_config(page_title="Nyandarua Crop Disease Demo", layout="centered")

st.title("AI Crop Disease Detection — Nyandarua Prototype (Demo)")
st.markdown(
    """
This is a **prototype** demo built for your 4th-year project. It shows the full user flow:
1. Choose crop (potato, tomato, cabbage, maize)  
2. Upload a leaf / plant image (phone photo)  
3. The app runs a **mock classifier** (color/texture heuristic) to simulate detection  
4. The app shows **locally‑tailored management recommendations** and next steps.

**Note:** This demo does NOT use a trained CNN. Replace the `mock_predict()` function with your real model inference code (TensorFlow/TFLite/PyTorch) later.
"""
)

st.sidebar.header("Project settings (demo)")
st.sidebar.info("Replace the mock classifier with your trained model later.")

# --- Helper: mock predictor based on simple image stats ---
def mock_predict(image: Image.Image, crop: str):
    """
    Deterministic heuristic to give a mock 'prediction' based on image color and variance.
    Returns (label, confidence_score, explanation)
    This is only for prototype UI / workflow demonstration.
    """
    # convert to RGB and compute statistics
    img = image.convert("RGB").resize((224,224))
    stats = ImageStat.Stat(img)
    r_mean, g_mean, b_mean = stats.mean
    stddev = np.mean(stats.stddev)
    # simple rules tuned for demo only
    # High green -> likely healthy or nutrient issue; high redness or brownish -> fungal/bacterial lesion
    if r_mean > g_mean + 15 and r_mean > b_mean:
        label = "Likely: Leaf Blight / Necrosis"
        explanation = "Reddish/brown lesions detected by color heuristic."
        confidence = min(0.89, 0.6 + (r_mean - g_mean)/100)
    elif stddev > 60 and (g_mean < 100):
        label = "Likely: Severe Spotting / Early Blight"
        explanation = "High variance and low green suggests spots or lesions."
        confidence = min(0.92, 0.55 + (stddev-40)/200)
    elif g_mean > r_mean + 15:
        label = "Likely: Healthy or Nutrient Deficiency"
        explanation = "Leaf is relatively green — may be healthy or minor nutrient issues."
        confidence = min(0.8, 0.5 + (g_mean - r_mean)/120)
    else:
        label = "Likely: General Pest Damage / Unsure"
        explanation = "Mixed signals; further inspection recommended."
        confidence = 0.45 + abs(g_mean - r_mean)/400
    return label, round(float(confidence),2), explanation

# --- Recommendations database (simple, local-tailored examples) ---
RECOMMENDATIONS = {
    "potato": {
        "Likely: Leaf Blight / Necrosis": [
            ("Disease", "Late Blight (Phytophthora infestans) is common in Nyandarua's cool, wet climate."),
            ("Immediate action", "Remove and destroy heavily infected plants. Avoid moving potato material between fields."),
            ("Chemical option", "Use a recommended fungicide such as Mancozeb (follow label). Rotate modes of action."),
            ("Cultural option", "Improve drainage, avoid overhead irrigation, practice crop rotation with non‑solanaceous crops."),
            ("Local tip", "Consult the county agricultural extension officer or local agrovet (e.g., in Ol Kalou/Nyahururu).")
        ],
        "Likely: Severe Spotting / Early Blight": [
            ("Disease", "Early blight or bacterial spot; monitor spread."),
            ("Action", "Prune affected foliage, apply recommended fungicide if confirmed."),
            ("Preventive", "Use certified seed, practice crop rotation, remove volunteer potatoes.")
        ],
        "Likely: Healthy or Nutrient Deficiency": [
            ("Advice", "No immediate disease treatment. Consider soil test for nutrient imbalances."),
            ("Local", "Use organic matter and balanced fertiliser according to extension recommendations.")
        ],
        "Likely: General Pest Damage / Unsure": [
            ("Advice", "Take multiple photos (close-ups of lesions and whole plant) and send to extension agent."),
            ("Next step", "Use the 'Request Expert Review' option or visit a plant clinic.")
        ],
    },
    "tomato": {
        "Likely: Leaf Blight / Necrosis": [
            ("Disease", "Tomato blights and bacterial spots are common."),
            ("Immediate action", "Remove infected leaves, avoid overhead watering."),
            ("Chemical", "Apply approved fungicide/bactericide per label."),
            ("Alternative", "Use copper-based products carefully; integrate with cultural controls.")
        ],
        "Likely: Severe Spotting / Early Blight": [
            ("Advice", "Monitor for concentric rings typical of early blight; consider fungicide application."),
        ],
        "Likely: Healthy or Nutrient Deficiency": [
            ("Advice", "Likely healthy; check for nutrient deficiency signs — yellowing between veins etc."),
        ],
        "Likely: General Pest Damage / Unsure": [
            ("Advice", "Capture close-up images of pests or the underside of leaves. Consider scouting for aphids, whiteflies, or caterpillars."),
        ],
    },
    "cabbage": {
        "Likely: Leaf Blight / Necrosis": [
            ("Disease", "Black rot or bacterial/fungal lesions are possible."),
            ("Action", "Remove affected heads; ensure proper spacing and sanitation."),
        ],
        "Likely: Severe Spotting / Early Blight": [
            ("Action", "Scout for diamondback moth larvae or caterpillars; consider biological control (Bacillus thuringiensis) if pest present."),
        ],
        "Likely: Healthy or Nutrient Deficiency": [
            ("Advice", "Consider soil pH and fertility management; cabbages prefer well-fertilized soils."),
        ],
    },
    "maize": {
        "Likely: Leaf Blight / Necrosis": [
            ("Disease", "Northern leaf blight or other fungal diseases may be present."),
            ("Immediate", "Remove severely affected leaves, check for early signs of MLN or streak virus."),
        ],
        "Likely: Severe Spotting / Early Blight": [
            ("Action", "Scout for fall armyworm; treat according to action thresholds."),
        ],
        "Likely: Healthy or Nutrient Deficiency": [
            ("Advice", "Healthy signs — keep monitoring. Consider top-dressing nitrogen if needed."),
        ],
        "Likely: General Pest Damage / Unsure": [
            ("Advice", "Collect more evidence (photos, videos). Consider contacting county extension.")
        ],
    }
}

# --- UI ---
st.header("1. Choose crop & upload image")
crop = st.selectbox("Select crop", ["potato","tomato","cabbage","maize"])
uploaded = st.file_uploader("Upload a photo of the affected plant (leaf, stem, or whole plant). JPEG/PNG", type=["jpg","jpeg","png"])

if uploaded is None:
    st.info("Upload an image to run the demo. If you don't have one, use the sample images in the repo.")
else:
    # display image
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded image", use_column_width=True)
    st.write("---")
    st.header("2. Model prediction (demo)")
    with st.spinner("Running mock classifier..."):
        label, conf, explanation = mock_predict(image, crop)
    st.subheader(label)
    st.write(f"Confidence: **{conf*100:.0f}%**")
    st.caption(explanation)
    st.write("---")
    st.header("3. Locally‑tailored recommendations (Nyandarua-focused)")
    recs = RECOMMENDATIONS.get(crop, {}).get(label, None)
    if recs:
        for t, msg in recs:
            st.markdown(f"**{t}:** {msg}")
    else:
        st.markdown("No direct match in recommendations. Consider expert review or submitting more images.")
    st.write("---")
    st.header("4. Next steps & export")
    st.markdown(
        """
- **Save this report:** Download a text summary of the diagnosis and recommendations to share with extension officers.  
- **Request expert review:** (Demo) Prepare images and notes to take to your nearest plant clinic.  
- **Replace mock classifier:** See instructions below to plug in your trained model (TFLite/PyTorch).
"""
    )
    if st.button("Generate text report"):
        # create a simple text report and offer for download
        report = io.StringIO()
        report.write("Nyandarua Crop Disease Detection — Demo Report\n")
        report.write("=============================================\n\n")
        report.write(f"Crop: {crop}\n")
        report.write(f"Predicted: {label} (confidence={conf})\n")
        report.write(f"Note: {explanation}\n\n")
        report.write("Recommendations:\n")
        if recs:
            for t,msg in recs:
                report.write(f"- {t}: {msg}\n")
        else:
            report.write("- No recommendations found. Seek expert review.\n")
        b = report.getvalue().encode('utf-8')
        st.download_button("Download report (txt)", data=b, file_name="diagnosis_report.txt", mime="text/plain")


st.write("---")
#st.markdown("**Developer notes:**\n\n- To plug a real model: implement a `predict(image)` function and call it instead of `mock_predict`.\n- For on-device inference on Android, convert your model to TensorFlow Lite (.tflite) and use TensorFlow Lite interpreter in the app.\n- For offline use with Streamlit, bundle the model file and load it locally.\n\n**Commands**:\n\n```bash\npip install streamlit pillow numpy\nstreamlit run crop_disease_prototype_app.py\n```\n