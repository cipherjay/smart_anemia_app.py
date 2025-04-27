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
        "<h1 style='text-align: center; color: red; font-size: 60px;'>ACCESS DENIED</h1>",
        unsafe_allow_html=True
    )
    st.stop()

# ======= Helper Functions =======
def reset_form():
    keys_to_reset = ["patient_name", "sex", "age", "hb", "hct", "mcv", "mch", "mchc", "rdw",
                     "rbc", "iron", "ferritin", "tibc", "transf", "retic", "b12", "folate",
                     "ldh", "bilirubin", "hapto", "morphology"]
    for key in keys_to_reset:
        if key in st.session_state:
            st.session_state[key] = ""
    st.experimental_rerun()

def get_reference_ranges(sex, age):
    age = int(age) if age else 0
    ranges = {}

    if sex == "Male":
        if age >= 18:
            ranges = {
                "Hemoglobin": (13.5, 17.5),
                "MCV": (80, 100),
                "MCHC": (32, 36),
                "Ferritin": (30, 400),
                "Serum Iron": (65, 175),
                "TIBC": (250, 450),
                "Transferrin Saturation": (20, 50),
                "Reticulocyte Count": (0.5, 2.5),
                "Vitamin B12": (200, 900),
                "Folate": (3, 20)
            }
        else:
            ranges = {
                "Hemoglobin": (11.5, 15.5),
                "MCV": (75, 87),
                "MCHC": (32, 36),
                "Ferritin": (7, 140),
                "Serum Iron": (50, 120),
                "TIBC": (240, 450),
                "Transferrin Saturation": (16, 50),
                "Reticulocyte Count": (0.5, 1.5),
                "Vitamin B12": (200, 900),
                "Folate": (5, 21)
            }
    elif sex == "Female":
        if age >= 18:
            ranges = {
                "Hemoglobin": (12.0, 16.0),
                "MCV": (80, 100),
                "MCHC": (32, 36),
                "Ferritin": (12, 150),
                "Serum Iron": (50, 170),
                "TIBC": (250, 450),
                "Transferrin Saturation": (15, 50),
                "Reticulocyte Count": (0.5, 2.5),
                "Vitamin B12": (200, 900),
                "Folate": (3, 20)
            }
        else:
            ranges = {
                "Hemoglobin": (11.5, 15.5),
                "MCV": (75, 87),
                "MCHC": (32, 36),
                "Ferritin": (7, 140),
                "Serum Iron": (50, 120),
                "TIBC": (240, 450),
                "Transferrin Saturation": (16, 50),
                "Reticulocyte Count": (0.5, 1.5),
                "Vitamin B12": (200, 900),
                "Folate": (5, 21)
            }

    return ranges

# ======= Main Application =======
st.title("🩺 Smart Anemia Diagnosis Application")

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
        ranges = get_reference_ranges(sex, age)
        abnormal_results = []
        diagnosis = []
        recommendations = []

        def check_range(name, value):
            low, high = ranges.get(name, (None, None))
            if low is not None and value is not None:
                if value < low:
                    abnormal_results.append(f"{name}: Low")
                elif value > high:
                    abnormal_results.append(f"{name}: High")

        hb_val = float(hb) if hb else None
        mcv_val = float(mcv) if mcv else None
        ferritin_val = float(ferritin) if ferritin else None
        serum_iron_val = float(serum_iron) if serum_iron else None
        tibc_val = float(tibc) if tibc else None
        transferrin_sat_val = float(transferrin_sat) if transferrin_sat else None
        retic_val = float(retic) if retic else None
        vit_b12_val = float(vit_b12) if vit_b12 else None
        folate_val = float(folate) if folate else None
        mchc_val = float(mchc) if mchc else None

        check_range("Hemoglobin", hb_val)
        check_range("MCV", mcv_val)
        check_range("MCHC", mchc_val)
        check_range("Ferritin", ferritin_val)
        check_range("Serum Iron", serum_iron_val)
        check_range("TIBC", tibc_val)
        check_range("Transferrin Saturation", transferrin_sat_val)
        check_range("Reticulocyte Count", retic_val)
        check_range("Vitamin B12", vit_b12_val)
        check_range("Folate", folate_val)

        if hb_val and hb_val < ranges["Hemoglobin"][0]:
            if mcv_val and mcv_val < 80:
                if mchc_val and mchc_val < 32:
                    diagnosis.append("Microcytic Hypochromic Anemia")
                else:
                    diagnosis.append("Microcytic Anemia")

                if ferritin_val and ferritin_val < ranges["Ferritin"][0]:
                    diagnosis.append("Iron Deficiency Anemia")
                    recommendations.append("Recommend iron supplementation and search for bleeding sources.")
                elif morphology == "Target Cells":
                    diagnosis.append("Thalassemia Minor")
                    recommendations.append("Suggest hemoglobin electrophoresis.")
                else:
                    recommendations.append("Suggest iron studies and hemoglobin analysis.")
            elif mcv_val and mcv_val > 100:
                if vit_b12_val and vit_b12_val < 200:
                    diagnosis.append("Vitamin B12 Deficiency Anemia")
                    recommendations.append("Start Vitamin B12 replacement.")
                elif folate_val and folate_val < 3:
                    diagnosis.append("Folate Deficiency Anemia")
                    recommendations.append("Start folate replacement.")
                else:
                    diagnosis.append("Macrocytic Anemia (Other causes)")
                    recommendations.append("Investigate liver disease, hypothyroidism, alcoholism.")
            else:
                if retic_val and retic_val > 2.5:
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

        if abnormal_results:
            st.subheader("⚠️ Abnormal Results:")
            for result in abnormal_results:
                st.warning(result)

        st.subheader("📌 Recommendations:")
        for rec in recommendations:
            st.markdown(f"<span style='color:#007BFF;'>➡️ {rec}</span>", unsafe_allow_html=True)

    except Exception as e:
        st.error("Error in diagnosis. Please ensure all fields are filled correctly.")

st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; font-size:22px; color:#007BFF; font-weight:bold;'>"
    "Coder: Jk"
    "</div>",
    unsafe_allow_html=True
)
