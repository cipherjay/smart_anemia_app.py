import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Smart Anemia Diagnosis App", layout="wide")

# Reset all fields
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_form():
    st.session_state.clear()
    st.session_state.reset = True
    st.experimental_rerun()

st.title("🩺 Smart Anemia Diagnosis Application")

# Patient Info
st.header("👤 Patient Basic Information")
sex = st.selectbox("Sex", ("Male", "Female"), key="sex")
age = st.number_input("Age (years)", min_value=0, max_value=120, value=30, step=1, key="age")

# CBC Section
st.header("🩸 Complete Blood Count (CBC)")
hb = st.number_input("Hemoglobin (g/dL)", value=13.5, key="hb")
hct = st.number_input("Hematocrit (%)", value=40.0, key="hct")
mcv = st.number_input("MCV (fL)", value=85.0, key="mcv")
mch = st.number_input("MCH (pg)", value=28.0, key="mch")
mchc = st.number_input("MCHC (g/dL)", value=33.0, key="mchc")
rdw = st.number_input("RDW (%)", value=13.0, key="rdw")
rbc = st.number_input("RBC Count (million/µL)", value=5.0, key="rbc")

# Iron Studies
st.header("🧪 Iron Studies")
serum_iron = st.number_input("Serum Iron (µg/dL)", value=100.0, key="iron")
ferritin = st.number_input("Ferritin (ng/mL)", value=100.0, key="ferritin")
tibc = st.number_input("TIBC (µg/dL)", value=300.0, key="tibc")
transferrin_sat = st.number_input("Transferrin Saturation (%)", value=30.0, key="transf")

# Additional Tests
st.header("🧬 Additional Blood Tests")
retic = st.number_input("Reticulocyte Count (%)", value=1.5, key="retic")
vit_b12 = st.number_input("Vitamin B12 (pg/mL)", value=400.0, key="b12")
folate = st.number_input("Folate (ng/mL)", value=10.0, key="folate")
ldh = st.number_input("LDH (U/L)", value=200.0, key="ldh")
indirect_bilirubin = st.number_input("Indirect Bilirubin (mg/dL)", value=0.8, key="bilirubin")
haptoglobin = st.number_input("Haptoglobin (mg/dL)", value=150.0, key="hapto")

# Morphology
st.header("🔬 Peripheral Blood Morphology")
morphology = st.selectbox("Select Blood Cell Morphology:", (
    "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
    "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
), key="morphology")

# Classification display
classification = []

if mcv < 80:
    classification.append("Microcytic")
elif mcv > 100:
    classification.append("Macrocytic")
else:
    classification.append("Normocytic")

if mch < 27 or mchc < 31:
    classification.append("Hypochromic")
elif 27 <= mch <= 33 and 31 <= mchc <= 36:
    classification.append("Normochromic")
else:
    classification.append("Hyperchromic")

if classification:
    st.info(f"Based on CBC values, cells appear to be: **{' / '.join(classification)}**")

# Diagnosis
if st.button("🔍 Diagnose Anemia"):
    diagnosis = []
    recommendations = []

    if hb < 13:
        if mcv < 80:
            if ferritin < 30 and serum_iron < 60 and tibc > 400:
                diagnosis.append("🩸 Iron Deficiency Anemia")
                recommendations.append("- Recommend iron supplements and dietary adjustments.")
            elif morphology == "Target Cells" or rbc > 5.5:
                diagnosis.append("🧬 Possible Thalassemia")
                recommendations.append("- Recommend Hemoglobin Electrophoresis test.")
            elif morphology == "Basophilic Stippling":
                diagnosis.append("☠️ Possible Lead Poisoning")
                recommendations.append("- Recommend Blood Lead Level testing and chelation therapy if necessary.")
            else:
                diagnosis.append("📋 Microcytic Anemia - Further Investigation Needed")
                recommendations.append("- Suggest iron studies and hemoglobin analysis.")
        elif mcv > 100:
            if vit_b12 < 200 or folate < 3:
                diagnosis.append("🔬 Megaloblastic Anemia (Vitamin B12 or Folate Deficiency)")
                recommendations.append("- Recommend Vitamin B12 and Folate supplementation.")
            else:
                diagnosis.append("📋 Macrocytic Anemia - Further Investigation Needed")
                recommendations.append("- Investigate for liver disease, alcoholism, or hypothyroidism.")
        else:
            if retic > 2.5:
                if morphology == "Schistocytes":
                    diagnosis.append("⚡ Hemolytic Anemia")
                    recommendations.append("- Suggest Coombs test and hemolysis workup.")
                elif morphology == "Spherocytes":
                    diagnosis.append("⚡ Hereditary Spherocytosis or Autoimmune Hemolytic Anemia")
                    recommendations.append("- Recommend Direct Antiglobulin Test (DAT).")
                else:
                    diagnosis.append("⚡ Normocytic Anemia with High Reticulocytes - Possible Hemolysis or Bleeding")
                    recommendations.append("- Investigate for sources of bleeding or hemolysis.")
            else:
                if ferritin > 100 and serum_iron < 60:
                    diagnosis.append("📋 Anemia of Chronic Disease")
                    recommendations.append("- Investigate for chronic infections, inflammation, or malignancies.")
                else:
                    diagnosis.append("📋 Normocytic Anemia - Further Investigation Needed")
                    recommendations.append("- Full clinical evaluation recommended.")
    else:
        diagnosis.append("✅ No Anemia Detected")
        recommendations.append("No further action needed unless clinically indicated.")

    st.subheader("📝 Diagnosis Result:")
    for d in diagnosis:
        st.success(d)

    st.subheader("📌 Recommendations:")
    for rec in recommendations:
        st.info(rec)

    st.subheader("📊 Blood Parameter Overview")
    parameters = ['Hemoglobin', 'MCV', 'Serum Iron', 'Ferritin']
    values = [hb, mcv, serum_iron, ferritin]
    normal_values = [15, 90, 100, 150]

    fig, ax = plt.subplots()
    ax.bar(parameters, normal_values, label="Normal", alpha=0.5)
    ax.bar(parameters, values, label="Patient", alpha=0.7)
    ax.legend()
    st.pyplot(fig)

    report = StringIO()
    report.write(f"Patient Report\n========================\n")
    report.write(f"Sex: {sex}\nAge: {age} years\n\n")
    report.write(f"Classification: {' / '.join(classification)}\n\n")
    report.write(f"Diagnosis:\n")
    for d in diagnosis:
        report.write(f"- {d}\n")
    report.write(f"\nRecommendations:\n")
    for r in recommendations:
        report.write(f"- {r}\n")

    st.download_button("Download Report", data=report.getvalue(), file_name="patient_report.txt", mime="text/plain")

# Reset form
if st.button("➕ Enter New Patient"):
    reset_form()

# Footer
st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown("<center><small>Coder: Jk</small></center>", unsafe_allow_html=True)
