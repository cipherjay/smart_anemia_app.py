import streamlit as st
from fpdf import FPDF

st.title("Smart Anemia Diagnosis App")
st.header("Patient Information")

# Patient Data Entry (All fields start empty)
name = st.text_input("Patient Name", key="name")
age = st.text_input("Age", key="age")
gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
hb = st.text_input("Hemoglobin (g/dL)", key="hb")
mcv = st.text_input("MCV (fL)", key="mcv")
ferritin = st.text_input("Ferritin (ng/mL)", key="ferritin")
vitamin_b12 = st.text_input("Vitamin B12 (pg/mL)", key="vitamin_b12")
retic_count = st.text_input("Reticulocyte Count (%)", key="retic_count")

# Diagnosis Logic
def diagnose_anemia(hb, mcv, ferritin, vitamin_b12, retic_count):
    if hb < 12:
        if retic_count < 0.5:
            return "Aplastic Anemia"
        if mcv < 80:
            if ferritin < 30:
                return "Iron Deficiency Anemia"
            else:
                return "Thalassemia Minor"
        elif mcv > 100:
            if vitamin_b12 < 200:
                return "Vitamin B12 Deficiency Anemia"
            else:
                return "Macrocytic Anemia (Other cause)"
        else:
            if retic_count > 2.0:
                return "Hemolytic Anemia"
            elif ferritin > 200:
                return "Anemia due to Chronic Kidney Disease"
            else:
                return "Anemia of Chronic Disease"
    else:
        return "No Anemia"

# Diagnose Button
if st.button("Diagnose"):
    try:
        hb_val = float(hb)
        mcv_val = float(mcv)
        ferritin_val = float(ferritin)
        vitamin_b12_val = float(vitamin_b12)
        retic_count_val = float(retic_count)

        diagnosis = diagnose_anemia(hb_val, mcv_val, ferritin_val, vitamin_b12_val, retic_count_val)
        st.subheader("Diagnosis Result:")
        st.success(f"{diagnosis}")

        # Option to save as PDF
        if st.checkbox("Save Patient Data as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Patient Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
            pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
            pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
            pdf.cell(200, 10, txt=f"Hemoglobin: {hb} g/dL", ln=True)
            pdf.cell(200, 10, txt=f"MCV: {mcv} fL", ln=True)
            pdf.cell(200, 10, txt=f"Ferritin: {ferritin} ng/mL", ln=True)
            pdf.cell(200, 10, txt=f"Vitamin B12: {vitamin_b12} pg/mL", ln=True)
            pdf.cell(200, 10, txt=f"Reticulocyte Count: {retic_count}%", ln=True)
            pdf.cell(200, 10, txt=f"Diagnosis: {diagnosis}", ln=True)

            pdf_output_path = f"/mnt/data/{name}_report.pdf"
            pdf.output(pdf_output_path)
            with open(pdf_output_path, "rb") as file:
                st.download_button(label="Download PDF", data=file, file_name=f"{name}_report.pdf", mime="application/pdf")

    except ValueError:
        st.error("Please fill all numeric fields correctly.")

# Button to reset form
if st.button("Enter New Patient"):
    for key in ["name", "age", "gender", "hb", "mcv", "ferritin", "vitamin_b12", "retic_count"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
