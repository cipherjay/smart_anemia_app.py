import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

# إعداد الصفحة
st.set_page_config(page_title="Smart Anemia Diagnosis", page_icon="🩺", layout="centered")

# ======= Password Protection =======
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
        unsafe_allow_html=True
    )
    st.stop()

# ======= Start the main application after correct password =======

st.title("🩺 Smart Anemia Diagnosis Application")

# Reset all fields
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_form():
    st.session_state.clear()
    st.session_state.reset = True
    st.experimental_rerun()

# Patient Information
st.header("👤 Patient Basic Information")
sex = st.selectbox("Sex", ("Male", "Female"), key="sex")
age = st.number_input("Age (years)", min_value=0, max_value=120, value=0, step=1, key="age")

# CBC Section
st.header("🩸 Complete Blood Count (CBC)")
hb = st.number_input("Hemoglobin (g/dL)", value=0.0, key="hb", placeholder="Enter Hemoglobin...")
hct = st.number_input("Hematocrit (%)", value=0.0, key="hct", placeholder="Enter Hematocrit...")
mcv = st.number_input("MCV (fL)", value=0.0, key="mcv", placeholder="Enter MCV...")
mch = st.number_input("MCH (pg)", value=0.0, key="mch", placeholder="Enter MCH...")
mchc = st.number_input("MCHC (g/dL)", value=0.0, key="mchc", placeholder="Enter MCHC...")
rdw = st.number_input("RDW (%)", value=0.0, key="rdw", placeholder="Enter RDW...")
rbc = st.number_input("RBC Count (million/µL)", value=0.0, key="rbc", placeholder="Enter RBC Count...")

# Iron Studies
st.header("🧪 Iron Studies")
serum_iron = st.number_input("Serum Iron (µg/dL)", value=0.0, key="iron", placeholder="Enter Serum Iron...")
ferritin = st.number_input("Ferritin (ng/mL)", value=0.0, key="ferritin", placeholder="Enter Ferritin...")
tibc = st.number_input("TIBC (µg/dL)", value=0.0, key="tibc", placeholder="Enter TIBC...")
transferrin_sat = st.number_input("Transferrin Saturation (%)", value=0.0, key="transf", placeholder="Enter Transferrin Saturation...")

# Additional Blood Tests
st.header("🧬 Additional Blood Tests")
retic = st.number_input("Reticulocyte Count (%)", value=0.0, key="retic", placeholder="Enter Reticulocyte Count...")
vit_b12 = st.number_input("Vitamin B12 (pg/mL)", value=0.0, key="b12", placeholder="Enter Vitamin B12...")
folate = st.number_input("Folate (ng/mL)", value=0.0, key="folate", placeholder="Enter Folate...")
ldh = st.number_input("LDH (U/L)", value=0.0, key="ldh", placeholder="Enter LDH...")
indirect_bilirubin = st.number_input("Indirect Bilirubin (mg/dL)", value=0.0, key="bilirubin", placeholder="Enter Indirect Bilirubin...")
haptoglobin = st.number_input("Haptoglobin (mg/dL)", value=0.0, key="hapto", placeholder="Enter Haptoglobin...")

# Peripheral Blood Morphology
st.header("🔬 Peripheral Blood Morphology")
morphology = st.selectbox("Select Blood Cell Morphology:", (
    "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
    "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
), key="morphology")

# CBC parameter evaluation based on sex and age
st.header("📈 Parameter Evaluation")

# Determine normal ranges based on sex and age
if age < 12:
    hb_low, hb_high = 11, 13.5
elif sex == "Male":
    hb_low, hb_high = 13, 17
else:
    hb_low, hb_high = 12, 16

# Normal ranges for other parameters
normal_ranges = {
    "MCV": (80, 100),
    "MCH": (27, 33),
    "MCHC": (31, 36),
    "RDW": (11.5, 14.5),
    "RBC": (4.5, 6.0),
    "Serum Iron": (60, 170),
    "Ferritin": (30, 300),
    "TIBC": (250, 400),
    "Transferrin Saturation": (20, 50)
}

# Function to show indicator arrows
def show_indicator(value, low, high, label):
    if value != 0.0:
        if value < low:
            st.write(f"{label}: ⬇️ Low")
        elif value > high:
            st.write(f"{label}: ⬆️ High")
        else:
            st.write(f"{label}: ✅ Normal")

# Apply indicators
show_indicator(hb, hb_low, hb_high, "Hemoglobin")
show_indicator(mcv, *normal_ranges["MCV"], "MCV")
show_indicator(mch, *normal_ranges["MCH"], "MCH")
show_indicator(mchc, *normal_ranges["MCHC"], "MCHC")
show_indicator(rdw, *normal_ranges["RDW"], "RDW")
show_indicator(rbc, *normal_ranges["RBC"], "RBC Count")
show_indicator(serum_iron, *normal_ranges["Serum Iron"], "Serum Iron")
show_indicator(ferritin, *normal_ranges["Ferritin"], "Ferritin")
show_indicator(tibc, *normal_ranges["TIBC"], "TIBC")
show_indicator(transferrin_sat, *normal_ranges["Transferrin Saturation"], "Transferrin Saturation")

# Button to reset the form
if st.button("➕ Enter New Patient"):
    reset_form()

# Footer
st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; font-size:22px; color:#007BFF; font-weight:bold;'>"
    "Coder: Jk"
    "</div>",
    unsafe_allow_html=True
)
