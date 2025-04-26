import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

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

# Diagnose Button
if st.button("🔍 Diagnose Anemia"):
    diagnosis = []
    recommendations = []

    if hb < 13 and hb > 0:
        if mcv < 80:
            if ferritin < 30 and serum_iron < 60 and tibc > 400:
                diagnosis.append("Iron Deficiency Anemia")
                recommendations.append("Recommend iron supplementation, dietary counseling, and investigation for chronic blood loss.")
            elif morphology == "Target Cells" or rbc > 5.5:
                diagnosis.append("Possible Thalassemia")
                recommendations.append("Suggest hemoglobin electrophoresis and genetic counseling.")
            elif morphology == "Basophilic Stippling":
                diagnosis.append("Possible Lead Poisoning")
                recommendations.append("Recommend blood lead level testing and environmental assessment.")
            else:
                diagnosis.append("Microcytic Anemia - Further investigation needed.")
                recommendations.append("Suggest iron studies and hemoglobin analysis.")
        elif mcv > 100:
            if vit_b12 < 200 or folate < 3:
                diagnosis.append("Megaloblastic Anemia (Vitamin B12 or Folate Deficiency)")
                recommendations.append("Initiate Vitamin B12 or Folate supplementation and evaluate gastrointestinal absorption disorders.")
            else:
                diagnosis.append("Macrocytic Anemia - Further investigation needed.")
                recommendations.append("Investigate liver disease, alcoholism, or hypothyroidism.")
        else:
            if retic > 2.5:
                if morphology == "Schistocytes":
                    diagnosis.append("Hemolytic Anemia")
                    recommendations.append("Perform Direct Coombs test, reticulocyte count, LDH, and peripheral smear review.")
                elif morphology == "Spherocytes":
                    diagnosis.append("Hereditary Spherocytosis or Autoimmune Hemolytic Anemia")
                    recommendations.append("Recommend Direct Antiglobulin Test (DAT) and osmotic fragility test.")
                else:
                    diagnosis.append("Normocytic Anemia with High Reticulocytes - Possible hemolysis or acute blood loss.")
                    recommendations.append("Evaluate for hemolysis or bleeding sources.")
            else:
                if ferritin > 100 and serum_iron < 60:
                    diagnosis.append("Anemia of Chronic Disease")
                    recommendations.append("Manage underlying chronic inflammation, infection, or malignancy.")
                else:
                    diagnosis.append("Normocytic Anemia - Further investigation needed.")
                    recommendations.append("Full clinical evaluation recommended.")
    elif hb >= 13:
        diagnosis.append("No Anemia Detected")
        recommendations.append("No action needed unless clinically indicated. Follow-up as appropriate.")

    st.subheader("📝 Diagnosis Result:")
    for d in diagnosis:
        st.success(f"✔️ {d}")

    st.subheader("📌 Recommendations:")
    for rec in recommendations:
        st.info(f"ℹ️ {rec}")

# Reset button
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
