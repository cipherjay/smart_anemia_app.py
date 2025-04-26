import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# Configure the page settings
st.set_page_config(page_title="Smart Anemia Diagnosis", page_icon="🩺", layout="centered")

# ======= Password Protection =======
def authenticate_user():
    password = st.text_input("Enter Password to Access:", type="password")
    correct_password = "J2M2"

    if not password:
        st.stop()

    if password != correct_password:
        st.markdown(
            """
            <h1 style='text-align: center; color: red; font-size: 60px;'>
            ACCESS DENIED
            </h1>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

authenticate_user()

# ======= Main Application =======
st.title("🩺 Smart Anemia Diagnosis Application")

# Function to reset the form
def reset_form():
    keys_to_reset = [
        "patient_name", "sex", "age", "hb", "hct", "mcv", "mch", "mchc", "rdw",
        "rbc", "iron", "ferritin", "tibc", "transf", "retic", "b12", "folate",
        "ldh", "bilirubin", "hapto", "morphology"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            st.session_state[key] = ""
    st.experimental_rerun()

# Patient Information Section
st.header("👤 Patient Basic Information")
patient_name = st.text_input("Patient Name", value="", placeholder="Enter patient name", key="patient_name")
sex = st.selectbox("Sex", ("Male", "Female"), key="sex")
age = st.text_input("Age (years)", value="", placeholder="Enter age", key="age")

# CBC Section
st.header("🩸 Complete Blood Count (CBC)")
hb = st.text_input("Hemoglobin (g/dL)", value="", placeholder="Enter Hemoglobin...", key="hb")
hct = st.text_input("Hematocrit (%)", value="", placeholder="Enter Hematocrit...", key="hct")
mcv = st.text_input("MCV (fL)", value="", placeholder="Enter MCV...", key="mcv")
mch = st.text_input("MCH (pg)", value="", placeholder="Enter MCH...", key="mch")
mchc = st.text_input("MCHC (g/dL)", value="", placeholder="Enter MCHC...", key="mchc")
rdw = st.text_input("RDW (%)", value="", placeholder="Enter RDW...", key="rdw")
rbc = st.text_input("RBC Count (million/µL)", value="", placeholder="Enter RBC Count...", key="rbc")

# Iron Studies Section
st.header("🧪 Iron Studies")
serum_iron = st.text_input("Serum Iron (µg/dL)", value="", placeholder="Enter Serum Iron...", key="iron")
ferritin = st.text_input("Ferritin (ng/mL)", value="", placeholder="Enter Ferritin...", key="ferritin")
tibc = st.text_input("TIBC (µg/dL)", value="", placeholder="Enter TIBC...", key="tibc")
transferrin_sat = st.text_input("Transferrin Saturation (%)", value="", placeholder="Enter Transferrin Saturation...", key="transf")

# Additional Blood Tests Section
st.header("🧬 Additional Blood Tests")
retic = st.text_input("Reticulocyte Count (%)", value="", placeholder="Enter Reticulocyte Count...", key="retic")
vit_b12 = st.text_input("Vitamin B12 (pg/mL)", value="", placeholder="Enter Vitamin B12...", key="b12")
folate = st.text_input("Folate (ng/mL)", value="", placeholder="Enter Folate...", key="folate")
ldh = st.text_input("LDH (U/L)", value="", placeholder="Enter LDH...", key="ldh")
indirect_bilirubin = st.text_input("Indirect Bilirubin (mg/dL)", value="", placeholder="Enter Indirect Bilirubin...", key="bilirubin")
haptoglobin = st.text_input("Haptoglobin (mg/dL)", value="", placeholder="Enter Haptoglobin...", key="hapto")

# Peripheral Blood Morphology Section
st.header("🔬 Peripheral Blood Morphology")
morphology = st.selectbox(
    "Select Blood Cell Morphology:",
    (
        "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
        "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
    ),
    key="morphology",
)

# Diagnosis Section
if st.button("🔍 Diagnose Anemia"):
    try:
        # Convert input values to float if available
        hb_val = float(hb) if hb else None
        mcv_val = float(mcv) if mcv else None
        ferritin_val = float(ferritin) if ferritin else None
        vit_b12_val = float(vit_b12) if vit_b12 else None
        folate_val = float(folate) if folate else None
        retic_val = float(retic) if retic else None
        tibc_val = float(tibc) if tibc else None
        serum_iron_val = float(serum_iron) if serum_iron else None

        diagnosis = []
        recommendations = []
        abnormal_values = {}

        # Helper to record abnormal values
        def record_abnormal(name, value, low=None, high=None):
            if value is not None:
                if (low is not None and value < low) or (high is not None and value > high):
                    abnormal_values[name] = value

        # Determine thresholds based on age and sex
        def get_thresholds(test_name):
            thresholds = {
                "hb": {"Male": (13, 17), "Female": (12, 15), "Child": (11, 16)},
                "mcv": (80, 100),
                "ferritin": {"Male": (30, 300), "Female": (20, 120)},
                # Add additional test thresholds here
            }
            return thresholds.get(test_name, (None, None))

        # Check for abnormal values based on thresholds
        for test_name, value in [("hb", hb_val), ("mcv", mcv_val), ("ferritin", ferritin_val)]:
            low, high = get_thresholds(test_name)
            if isinstance(low, dict):  # Age/Sex-based thresholds
                low, high = low.get(sex, (None, None))
            record_abnormal(test_name, value, low, high)

        # Diagnosis logic (can remain as-is or be enhanced)
        if hb_val and hb_val < 13:
            if mcv_val and mcv_val < 80:
                if ferritin_val and ferritin_val < 30:
                    diagnosis.append("Iron Deficiency Anemia")
                    recommendations.append("Recommend iron supplementation and search for bleeding sources.")
                else:
                    diagnosis.append("Microcytic Anemia - Further tests needed.")
            elif mcv_val and mcv_val > 100:
                diagnosis.append("Macrocytic Anemia - Investigate further.")
            else:
                diagnosis.append("Normocytic Anemia - Further investigation needed.")
        else:
            diagnosis.append("No Anemia Detected")

        # Display abnormal values
        if abnormal_values:
            st.subheader("⚠️ Abnormal Values:")
            for key, value in abnormal_values.items():
                st.warning(f"{key}: {value}")

        # Display diagnosis and recommendations
        st.subheader("📝 Diagnosis Result:")
        for d in diagnosis:
            st.success(f"✅ {d}")

        st.subheader("📌 Recommendations:")
        for rec in recommendations:
            st.markdown(f"<span style='color:#007BFF;'>➡️ {rec}</span>", unsafe_allow_html=True)

    except ValueError:
        st.error("Invalid input. Please ensure all numeric fields are filled with valid numbers.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Footer Section
st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; font-size:22px; color:#007BFF; font-weight:bold;'>"
    "Coder: Jk"
    "</div>",
    unsafe_allow_html=True,
)
