import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Smart Anemia Diagnosis App", page_icon="🩺", layout="centered")

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

# ======= Main App with Tabs =======
st.title("🩺 Smart Anemia Diagnosis App")

tab1, tab2, tab3 = st.tabs(["🧑‍⚕️ Patient Information", "🧬 Lab Results", "📝 Diagnosis & Plan"])

# Initialize session state
if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None
if "severity" not in st.session_state:
    st.session_state.severity = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

# TAB 1: Patient Information
with tab1:
    st.header("Patient Information")
    patient_name = st.text_input("Patient Name", key="patient_name")
    sex = st.selectbox("Sex", ("Male", "Female"), key="sex")
    age = st.text_input("Age (years)", key="age")

# TAB 2: Lab Results
with tab2:
    st.header("Complete Blood Count (CBC)")
    hb = st.text_input("Hemoglobin (g/dL)", key="hb")
    mcv = st.text_input("MCV (fL)", key="mcv")
    ferritin = st.text_input("Ferritin (ng/mL)", key="ferritin")
    serum_iron = st.text_input("Serum Iron (µg/dL)", key="iron")
    tibc = st.text_input("TIBC (µg/dL)", key="tibc")
    transferrin_sat = st.text_input("Transferrin Saturation (%)", key="transf")
    retic = st.text_input("Reticulocyte Count (%)", key="retic")
    vit_b12 = st.text_input("Vitamin B12 (pg/mL)", key="b12")
    folate = st.text_input("Folate (ng/mL)", key="folate")
    morphology = st.selectbox("Peripheral Blood Morphology", (
        "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
        "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
    ), key="morphology")

# Diagnosis Logic Function
def diagnose(hb_val, mcv_val, ferritin_val, serum_iron_val, tibc_val, retic_val, vit_b12_val, folate_val, morphology):
    diagnosis = []
    recommendations = []

    if hb_val < 13:
        if mcv_val < 80:
            if ferritin_val < 30:
                diagnosis.append("Iron Deficiency Anemia")
                recommendations.append("Start oral iron therapy and investigate for bleeding sources.")
            elif morphology == "Target Cells":
                diagnosis.append("Thalassemia Minor")
                recommendations.append("Recommend hemoglobin electrophoresis.")
            else:
                diagnosis.append("Microcytic Anemia - Further investigation needed.")
                recommendations.append("Suggest iron studies and hemoglobin analysis.")
        elif mcv_val > 100:
            if vit_b12_val < 200:
                diagnosis.append("Vitamin B12 Deficiency Anemia")
                recommendations.append("Start vitamin B12 replacement therapy.")
            elif folate_val < 3:
                diagnosis.append("Folate Deficiency Anemia")
                recommendations.append("Initiate folate replacement therapy.")
            else:
                diagnosis.append("Macrocytic Anemia - Other causes (Investigate liver, alcohol, thyroid).")
                recommendations.append("Check liver function and thyroid function tests.")
        else:
            if retic_val > 2.5:
                diagnosis.append("Hemolytic Anemia")
                recommendations.append("Order Coombs test, LDH, and peripheral smear.")
            else:
                diagnosis.append("Normocytic Anemia - Possible chronic disease.")
                recommendations.append("Suggest workup for chronic disease, kidney function.")
    else:
        diagnosis.append("No Anemia Detected")
        recommendations.append("No action needed.")

    return diagnosis, recommendations

# Severity Function
def severity_level(hb_val, sex, age_val):
    if age_val < 12:  # Child
        normal = 11.5
    else:
        normal = 13.5 if sex == "Male" else 12.0

    if hb_val >= normal:
        return "No Anemia"
    elif hb_val >= 10:
        return "Mild Anemia"
    elif 7 <= hb_val < 10:
        return "Moderate Anemia"
    else:
        return "Severe Anemia"

# TAB 3: Diagnosis & Plan
with tab3:
    st.header("Diagnosis & Plan")

    if st.button("🔍 Diagnose"):
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
            age_val = int(age) if age else 0

            diagnosis, recommendations = diagnose(hb_val, mcv_val, ferritin_val, serum_iron_val, tibc_val, retic_val, vit_b12_val, folate_val, morphology)
            severity = severity_level(hb_val, sex, age_val)

            st.session_state.diagnosis_result = diagnosis
            st.session_state.recommendations = recommendations
            st.session_state.severity = severity

            st.success(f"✅ Severity: {severity}")
            st.subheader("📝 Diagnosis Result:")
            for d in diagnosis:
                st.success(f"✅ {d}")

            st.subheader("📌 Recommendations:")
            for rec in recommendations:
                st.markdown(f"<span style='color:#007BFF;'>➡️ {rec}</span>", unsafe_allow_html=True)

        except Exception as e:
            st.error("Error during diagnosis. Please make sure all fields are filled correctly!")

st.sidebar.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='text-align:center; font-size:22px; color:#007BFF; font-weight:bold;'>"
    "By JK"
    "</div>",
    unsafe_allow_html=True
)
