import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

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

# ======= Main Application =======
st.title("🩺 Smart Anemia Diagnosis Application")

def reset_form():
    keys_to_reset = ["patient_name", "sex", "age", "hb", "hct", "mcv", "mch", "mchc", "rdw",
                     "rbc", "iron", "ferritin", "tibc", "transf", "retic", "b12", "folate",
                     "ldh", "bilirubin", "hapto", "morphology"]
    for key in keys_to_reset:
        if key in st.session_state:
            st.session_state[key] = ""
    st.experimental_rerun()

# Patient Information
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

# Iron Studies
st.header("🧪 Iron Studies")
serum_iron = st.text_input("Serum Iron (µg/dL)", value="", placeholder="Enter Serum Iron...", key="iron")
ferritin = st.text_input("Ferritin (ng/mL)", value="", placeholder="Enter Ferritin...", key="ferritin")
tibc = st.text_input("TIBC (µg/dL)", value="", placeholder="Enter TIBC...", key="tibc")
transferrin_sat = st.text_input("Transferrin Saturation (%)", value="", placeholder="Enter Transferrin Saturation...", key="transf")

# Additional Blood Tests
st.header("🧬 Additional Blood Tests")
retic = st.text_input("Reticulocyte Count (%)", value="", placeholder="Enter Reticulocyte Count...", key="retic")
vit_b12 = st.text_input("Vitamin B12 (pg/mL)", value="", placeholder="Enter Vitamin B12...", key="b12")
folate = st.text_input("Folate (ng/mL)", value="", placeholder="Enter Folate...", key="folate")
ldh = st.text_input("LDH (U/L)", value="", placeholder="Enter LDH...", key="ldh")
indirect_bilirubin = st.text_input("Indirect Bilirubin (mg/dL)", value="", placeholder="Enter Indirect Bilirubin...", key="bilirubin")
haptoglobin = st.text_input("Haptoglobin (mg/dL)", value="", placeholder="Enter Haptoglobin...", key="hapto")

# Peripheral Blood Morphology
st.header("🔬 Peripheral Blood Morphology")
morphology = st.selectbox("Select Blood Cell Morphology:", (
    "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
    "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
), key="morphology")

# Diagnose Button
if st.button("🔍 Diagnose Anemia"):
    try:
        hb_val = float(hb) if hb else 0.0
        mcv_val = float(mcv) if mcv else 0.0
        ferritin_val = float(ferritin) if ferritin else 0.0
        serum_iron_val = float(serum_iron) if serum_iron else 0.0
        tibc_val = float(tibc) if tibc else 0.0
        transferrin_sat_val = float(transferrin_sat) if transferrin_sat else 0.0
        retic_val = float(retic) if retic else 0.0
        vit_b12_val = float(vit_b12) if vit_b12 else 0.0
        folate_val = float(folate) if folate else 0.0

        diagnosis = []
        recommendations = []

        if hb_val < 13 and hb_val > 0:
            if mcv_val < 80:
                if ferritin_val < 30:
                    diagnosis.append("Iron Deficiency Anemia")
                    recommendations.append("Recommend iron supplementation and search for bleeding sources.")
                elif morphology == "Target Cells":
                    diagnosis.append("Thalassemia Minor")
                    recommendations.append("Suggest hemoglobin electrophoresis.")
                else:
                    diagnosis.append("Microcytic Anemia - Further tests needed.")
                    recommendations.append("Suggest iron studies and hemoglobin analysis.")
            elif mcv_val > 100:
                if vit_b12_val < 200:
                    diagnosis.append("Vitamin B12 Deficiency Anemia")
                    recommendations.append("Start Vitamin B12 replacement.")
                elif folate_val < 3:
                    diagnosis.append("Folate Deficiency Anemia")
                    recommendations.append("Start folate replacement.")
                else:
                    diagnosis.append("Macrocytic Anemia (Other causes)")
                    recommendations.append("Investigate liver disease, hypothyroidism, alcoholism.")
            else:
                if retic_val > 2.5:
                    diagnosis.append("Hemolytic Anemia")
                    recommendations.append("Check Coombs test, LDH, Bilirubin.")
                else:
                    diagnosis.append("Normocytic Anemia - Further investigation needed.")
                    recommendations.append("Suggest clinical evaluation.")
        else:
            diagnosis.append("No Anemia Detected")
            recommendations.append("No further action needed.")

        st.subheader("📝 Diagnosis Result:")
        for d in diagnosis:
            st.success(f"✅ {d}")

        st.subheader("📌 Recommendations:")
        for rec in recommendations:
            st.markdown(f"<span style='color:#007BFF;'>➡️ {rec}</span>", unsafe_allow_html=True)

    except Exception as e:
        st.error("Error in diagnosis. Please ensure all fields are filled correctly.")

# Reset Form Button
if st.button("➕ Enter New Patient"):
    reset_form()

st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; font-size:22px; color:#007BFF; font-weight:bold;'>"
    "Coder: Jk"
    "</div>",
    unsafe_allow_html=True
)
