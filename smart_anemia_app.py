import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Smart Anemia Diagnosis", page_icon="🩺", layout="centered")

# ======= Password Protection =======
password = st.text_input("Enter Password to Access:", type="password")
correct_password = "J2M2"

if not password:
    st.stop()

if password != correct_password:
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>ACCESS DENIED</h1>", unsafe_allow_html=True)
    st.stop()

# ======= Main Application =======
st.title("🩺 Smart Anemia Diagnosis Application")

# Patient Information Section
st.header("👤 Patient Basic Information")
sex = st.selectbox("Sex", ("Male", "Female"), key="sex")
age = st.number_input("Age", min_value=0, max_value=120, key="age")

# Lab Results Section
st.header("🧪 Lab Results")
hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, key="hb")
mcv = st.number_input("MCV (fL)", min_value=0.0, key="mcv")
mch = st.number_input("MCH (pg)", min_value=0.0, key="mch")
mchc = st.number_input("MCHC (g/dL)", min_value=0.0, key="mchc")
ferritin = st.number_input("Ferritin (ng/mL)", min_value=0.0, key="ferritin")
serum_iron = st.number_input("Serum Iron (µg/dL)", min_value=0.0, key="serum_iron")
tibc = st.number_input("TIBC (µg/dL)", min_value=0.0, key="tibc")
retic = st.number_input("Reticulocyte Count (%)", min_value=0.0, key="retic")
vit_b12 = st.number_input("Vitamin B12 (pg/mL)", min_value=0.0, key="vit_b12")
folate = st.number_input("Folate (ng/mL)", min_value=0.0, key="folate")
rbc_count = st.number_input("RBC Count (Million cells/µL)", min_value=0.0, key="rbc_count")
rdw = st.number_input("RDW (%)", min_value=0.0, key="rdw")
hct = st.number_input("Hematocrit (%)", min_value=0.0, key="hct")
morphology = st.text_input("Morphology (e.g., Target Cells, Sickle Cells, etc.)", key="morphology")

# Diagnosis & Plan Section
st.header("📝 Diagnosis & Plan")

if st.button("🔍 Diagnose", key=f"diagnose_button_{age}_{sex}"):

    try:
        diagnosis = []

        # 1. Iron Deficiency Anemia
        if ferritin < 30 and serum_iron < 30 and tibc > 400:
            diagnosis.append("Iron Deficiency Anemia: Low Ferritin, Low Serum Iron, High TIBC")

        # 2. Thalassemia Minor
        if "target cells" in morphology.lower() and mcv < 80:
            diagnosis.append("Thalassemia Minor: Target Cells in Morphology, Microcytic MCV")

        # 3. Vitamin B12 Deficiency
        if vit_b12 < 200 and mcv > 100:
            diagnosis.append("Vitamin B12 Deficiency: Low Vitamin B12, Macrocytic MCV")

        # 4. Folate Deficiency
        if folate < 3 and mcv > 100:
            diagnosis.append("Folate Deficiency: Low Folate, Macrocytic MCV")

        # 5. Hemolytic Anemia
        if retic > 2.5:
            diagnosis.append("Hemolytic Anemia: High Reticulocyte Count")

        # 6. Anemia of Chronic Disease
        if serum_iron < 30 and ferritin >= 30:
            diagnosis.append("Anemia of Chronic Disease: Low Serum Iron, Normal or High Ferritin")

        # 7. Sickle Cell Disease
        if "sickle cells" in morphology.lower():
            diagnosis.append("Sickle Cell Disease: Sickle Cells in Morphology")

        # 8. Lead Poisoning
        if "basophilic stippling" in morphology.lower():
            diagnosis.append("Lead Poisoning: Basophilic Stippling in Morphology")

        # 9. Aplastic Anemia
        if hb < 7.0 and retic < 1.0:
            diagnosis.append("Aplastic Anemia: Very Low Hemoglobin and Reticulocyte Count")

        # 10. Normocytic Normochromic Anemia
        if mcv >= 80 and mcv <= 100 and mch >= 27 and hb < 12.0:
            diagnosis.append("Normocytic Normochromic Anemia: Low Hemoglobin with Normal MCV and MCH")

        # 11. Macrocytic Anemia (Other causes)
        if mcv > 100 and (vit_b12 >= 200 or folate >= 3):
            diagnosis.append("Macrocytic Anemia: High MCV, Other causes (not B12 or Folate deficiency)")

        # 12. Microcytic Anemia (Unknown cause)
        if mcv < 80 and ferritin > 30:
            diagnosis.append("Microcytic Anemia: Low MCV without obvious Iron Deficiency")

        if diagnosis:
            st.write("Diagnosis based on the available data:")
            for item in diagnosis:
                st.write(f"- {item}")

            st.write("
### Recommendations:")
            st.write("- Consult a doctor for further investigation.")
            st.write("- Follow a balanced diet and consider supplementation.")
        else:
            st.write("No significant abnormalities detected based on the available data.")

    except Exception as e:
        st.write("Error in diagnosis: ", e)

# Adding a personalized signature
st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line separator
st.markdown("<h4 style='text-align: center;'>Jana K</h4>", unsafe_allow_html=True)
