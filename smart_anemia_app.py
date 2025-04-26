import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

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
        ldh_val = float(ldh) if ldh else 0.0
        indirect_bilirubin_val = float(indirect_bilirubin) if indirect_bilirubin else 0.0
        haptoglobin_val = float(haptoglobin) if haptoglobin else 0.0

        diagnosis = []
        recommendations = []

        if hb_val < 13 and hb_val > 0:
            if mcv_val < 80:
                if ferritin_val < 30 and serum_iron_val < 60 and tibc_val > 400:
                    diagnosis.append("Iron Deficiency Anemia")
                    recommendations.append("Recommend iron supplementation and search for bleeding sources.")
                elif morphology == "Target Cells" or float(rbc) > 5.5:
                    diagnosis.append("Thalassemia Minor")
                    recommendations.append("Suggest hemoglobin electrophoresis.")
                elif morphology == "Basophilic Stippling":
                    diagnosis.append("Possible Lead Poisoning")
                    recommendations.append("Check blood lead levels.")
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
                    if morphology == "Schistocytes":
                        diagnosis.append("Hemolytic Anemia")
                        recommendations.append("Check Coombs test, LDH, Bilirubin.")
                    elif morphology == "Spherocytes":
                        diagnosis.append("Spherocytosis or Autoimmune Hemolytic Anemia")
                        recommendations.append("Recommend DAT and osmotic fragility testing.")
                    else:
                        diagnosis.append("Normocytic anemia with high reticulocytes - Possible bleeding.")
                        recommendations.append("Evaluate for bleeding sources.")
                else:
                    if retic_val < 1:
                        diagnosis.append("Aplastic Anemia")
                        recommendations.append("Consider bone marrow biopsy.")
                    elif ferritin_val > 200:
                        diagnosis.append("Anemia due to Chronic Kidney Disease")
                        recommendations.append("Assess kidney function.")
                    elif ferritin_val > 100 and serum_iron_val < 60:
                        diagnosis.append("Anemia of Chronic Disease")
                        recommendations.append("Manage underlying disease.")
                    else:
                        diagnosis.append("Normocytic anemia - Further workup needed.")
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


        if diagnosis:
            if st.button("💾 Save Report as PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, "Smart Anemia Diagnosis Report", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Patient Information:", ln=True)
                pdf.set_font("Arial", '', 12)
                pdf.cell(0, 10, f"Name: {patient_name}", ln=True)
                pdf.cell(0, 10, f"Sex: {sex}", ln=True)
                pdf.cell(0, 10, f"Age: {age}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Diagnosis:", ln=True)
                pdf.set_font("Arial", '', 12)
                for d in diagnosis:
                    pdf.cell(0, 10, f"- {d}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "Recommendations:", ln=True)
                pdf.set_font("Arial", '', 12)
                for rec in recommendations:
                    pdf.multi_cell(0, 10, f"- {rec}")

                buffer = BytesIO()
                pdf.output(buffer)
                buffer.seek(0)
                st.download_button("⬇️ Download Report PDF", data=buffer.getvalue(), file_name="anemia_report.pdf", mime="application/pdf")

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
