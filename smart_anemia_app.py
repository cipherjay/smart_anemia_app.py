
import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Advanced Anemia Diagnosis App", layout="wide")

# Title
st.title("🩺 Advanced Anemia Diagnosis Application")

# 1- Patient Information
st.header("👤 Patient Basic Information")
sex = st.selectbox("Sex", ("Male", "Female"))
age = st.number_input("Age (years)", min_value=0, max_value=120, value=30, step=1)

# 2- CBC Section
st.header("🩸 Complete Blood Count (CBC)")
hb = st.number_input("Hemoglobin (g/dL)", value=13.5)
hct = st.number_input("Hematocrit (%)", value=40.0)
mcv = st.number_input("MCV (fL)", value=85.0)
mch = st.number_input("MCH (pg)", value=28.0)
mchc = st.number_input("MCHC (g/dL)", value=33.0)
rdw = st.number_input("RDW (%)", value=13.0)
rbc = st.number_input("RBC Count (million/µL)", value=5.0)

# 3- Iron Studies Section
st.header("🧪 Iron Studies")
serum_iron = st.number_input("Serum Iron (µg/dL)", value=100.0)
ferritin = st.number_input("Ferritin (ng/mL)", value=100.0)
tibc = st.number_input("TIBC (µg/dL)", value=300.0)
transferrin_sat = st.number_input("Transferrin Saturation (%)", value=30.0)

# 4- Additional Tests
st.header("🧬 Additional Blood Tests")
retic = st.number_input("Reticulocyte Count (%)", value=1.5)
vit_b12 = st.number_input("Vitamin B12 (pg/mL)", value=400.0)
folate = st.number_input("Folate (ng/mL)", value=10.0)
ldh = st.number_input("LDH (U/L)", value=200.0)
indirect_bilirubin = st.number_input("Indirect Bilirubin (mg/dL)", value=0.8)
haptoglobin = st.number_input("Haptoglobin (mg/dL)", value=150.0)

# 5- Peripheral Morphology
st.header("🔬 Peripheral Blood Morphology")
morphology = st.selectbox("Select Blood Cell Morphology:", (
    "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic Normochromic",
    "Target Cells", "Sickle Cells", "Spherocytes", "Schistocytes", "Basophilic Stippling"
))

# 6- Diagnosis Button
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

    # Show Diagnosis
    st.subheader("📝 Diagnosis Result:")
    for d in diagnosis:
        st.success(d)

    # Show Recommendations
    st.subheader("📌 Recommendations:")
    for rec in recommendations:
        st.info(rec)

    # Chart
    st.subheader("📊 Blood Parameter Overview")
    parameters = ['Hemoglobin', 'MCV', 'Serum Iron', 'Ferritin']
    values = [hb, mcv, serum_iron, ferritin]
    normal_values = [15, 90, 100, 150]

    fig, ax = plt.subplots()
    ax.bar(parameters, normal_values, label="Normal", alpha=0.5)
    ax.bar(parameters, values, label="Patient", alpha=0.7)
    ax.legend()
    st.pyplot(fig)

    # Report
    st.subheader("📥 Download Patient Report")
    report = StringIO()
    report.write(f"Patient Report\n")
    report.write(f"========================\n")
    report.write(f"Sex: {sex}\nAge: {age} years\n\n")
    report.write("--- CBC Results ---\n")
    report.write(f"Hemoglobin: {hb} g/dL\nHematocrit: {hct} %\nMCV: {mcv} fL\n")
    report.write(f"MCH: {mch} pg\nMCHC: {mchc} g/dL\nRDW: {rdw} %\nRBC Count: {rbc} million/µL\n\n")
    report.write("--- Iron Studies ---\n")
    report.write(f"Serum Iron: {serum_iron} µg/dL\nFerritin: {ferritin} ng/mL\nTIBC: {tibc} µg/dL\n")
    report.write(f"Transferrin Saturation: {transferrin_sat} %\n\n")
    report.write("--- Additional Tests ---\n")
    report.write(f"Reticulocyte Count: {retic} %\nVitamin B12: {vit_b12} pg/mL\nFolate: {folate} ng/mL\n")
    report.write(f"LDH: {ldh} U/L\nIndirect Bilirubin: {indirect_bilirubin} mg/dL\nHaptoglobin: {haptoglobin} mg/dL\n\n")
    report.write(f"--- Blood Morphology ---\nMorphology: {morphology}\n\n")
    report.write("--- Diagnosis ---\n")
    for d in diagnosis:
        report.write(f"{d}\n")
    report.write("\n--- Recommendations ---\n")
    for rec in recommendations:
        report.write(f"{rec}\n")

    st.download_button(label="Download Report as TXT", data=report.getvalue(),
                       file_name="patient_report.txt", mime="text/plain")

    if st.button("➕ Enter New Patient"):
        st.experimental_rerun()
