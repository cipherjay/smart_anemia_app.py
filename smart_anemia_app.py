import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Smart Anemia Assistant", page_icon="🩺", layout="centered")

# User input for password
password = st.text_input("🔒 Enter Password to Access:", type="password", help="Enter the correct password to access the application.")
correct_password = "J2M2"

if not password:
    st.stop()

if password != correct_password:
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>ACCESS DENIED</h1>", unsafe_allow_html=True)
    st.stop()

st.title("🩺 Smart Anemia Assistant")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🧑‍⚕️ Patient Information", "🧬 Lab Results", "📝 Diagnosis & Plan"])

# Patient Information Section
with tab1:
    st.header("Patient Information 👤")
    patient_name = st.text_input("Patient Name", placeholder="Enter the patient's name here")
    sex = st.selectbox("Sex 🧑‍🤝‍🧑", ("Male", "Female"))
    age = st.text_input("Age (years) 👶👵", placeholder="Enter the patient's age")

# Lab Results Section
with tab2:
    st.header("Lab Results 🧪")
    hb = st.text_input("Hemoglobin (g/dL) 💉", placeholder="Enter Hemoglobin level")
    mcv = st.text_input("MCV (fL) 🧫", placeholder="Enter MCV value")
    mch = st.text_input("MCH (pg) 🧬", placeholder="Enter MCH value")
    mchc = st.text_input("MCHC (g/dL) 🩸", placeholder="Enter MCHC value")
    ferritin = st.text_input("Ferritin (ng/mL) 💊", placeholder="Enter Ferritin value")
    serum_iron = st.text_input("Serum Iron (µg/dL) 💪", placeholder="Enter Serum Iron level")
    tibc = st.text_input("TIBC (µg/dL) 🏋️", placeholder="Enter TIBC value")
    retic = st.text_input("Reticulocyte Count (%) 🔬", placeholder="Enter Reticulocyte Count")
    vit_b12 = st.text_input("Vitamin B12 (pg/mL) 💊", placeholder="Enter Vitamin B12 level")
    folate = st.text_input("Folate (ng/mL) 🥦", placeholder="Enter Folate level")
    rbc_count = st.text_input("RBC Count (Million cells/µL) 🔴", placeholder="Enter RBC Count")
    rdw = st.text_input("RDW (%) 📊", placeholder="Enter RDW percentage")
    hct = st.text_input("Hematocrit (%) 💉", placeholder="Enter Hematocrit percentage")
    morphology = st.text_input("Morphology (e.g., Target Cells, Sickle Cells, etc.) 🔬", placeholder="Enter morphology findings")

# Diagnosis and Plan Section
with tab3:
    st.header("Diagnosis & Plan 🧑‍⚕️📋")

    if st.button("🔍 Diagnose", key=f"diagnose_button_{age}_{sex}"):

        try:
            # Ensure that inputs are not empty
            hb_val = float(hb) if hb else None
            mcv_val = float(mcv) if mcv else None
            mch_val = float(mch) if mch else None
            mchc_val = float(mchc) if mchc else None
            ferritin_val = float(ferritin) if ferritin else None
            serum_iron_val = float(serum_iron) if serum_iron else None
            tibc_val = float(tibc) if tibc else None
            retic_val = float(retic) if retic else None
            vit_b12_val = float(vit_b12) if vit_b12 else None
            folate_val = float(folate) if folate else None
            rbc_count_val = float(rbc_count) if rbc_count else None
            rdw_val = float(rdw) if rdw else None
            hct_val = float(hct) if hct else None
            age_val = int(age) if age else 0
            morphology_val = morphology.lower() if morphology else ""

            # Initialize diagnosis list
            diagnosis = []

            # Disease Diagnosis Logic

            # 1. Iron Deficiency Anemia
            if ferritin_val and serum_iron_val and tibc_val:
                if ferritin_val < 30 and serum_iron_val < 30 and tibc_val > 400:
                    diagnosis.append("Iron Deficiency Anemia: Low Ferritin, Low Serum Iron, High TIBC")

            # 2. Thalassemia Minor
            if morphology_val and mcv_val:
                if "target cells" in morphology_val and mcv_val < 80:
                    diagnosis.append("Thalassemia Minor: Target Cells in Morphology, Microcytic MCV")

            # 3. Vitamin B12 Deficiency
            if vit_b12_val and mcv_val:
                if vit_b12_val < 200 and mcv_val > 100:
                    diagnosis.append("Vitamin B12 Deficiency: Low Vitamin B12, Macrocytic MCV")

            # 4. Folate Deficiency
            if folate_val and mcv_val:
                if folate_val < 3 and mcv_val > 100:
                    diagnosis.append("Folate Deficiency: Low Folate, Macrocytic MCV")

            # 5. Hemolytic Anemia
            if retic_val:
                if retic_val > 2.5:
                    diagnosis.append("Hemolytic Anemia: High Reticulocyte Count")

            # 6. Anemia of Chronic Disease
            if serum_iron_val and ferritin_val:
                if serum_iron_val < 30 and ferritin_val >= 30:
                    diagnosis.append("Anemia of Chronic Disease: Low Serum Iron, Normal or High Ferritin")

            # 7. Sickle Cell Disease
            if "sickle cells" in morphology_val:
                diagnosis.append("Sickle Cell Disease: Sickle Cells in Morphology")

            # 8. Lead Poisoning
            if "basophilic stippling" in morphology_val:
                diagnosis.append("Lead Poisoning: Basophilic Stippling in Morphology")

            # 9. Aplastic Anemia
            if hb_val and retic_val:
                if hb_val < 7.0 and retic_val < 1.0:
                    diagnosis.append("Aplastic Anemia: Very Low Hemoglobin and Reticulocyte Count")

            # 10. Normocytic Normochromic Anemia
            if hb_val and mcv_val and mch_val:
                if mcv_val >= 80 and mcv_val <= 100 and mch_val >= 27 and hb_val < 12.0:
                    diagnosis.append("Normocytic Normochromic Anemia: Low Hemoglobin with Normal MCV and MCH")

            # 11. Macrocytic Anemia (Other causes)
            if mcv_val and (not vit_b12_val or not folate_val):
                if mcv_val > 100:
                    diagnosis.append("Macrocytic Anemia: High MCV, Other causes (not B12 or Folate deficiency)")

            # 12. Microcytic Anemia (Unknown cause)
            if mcv_val and ferritin_val:
                if mcv_val < 80 and ferritin_val > 30:
                    diagnosis.append("Microcytic Anemia: Low MCV without obvious Iron Deficiency")

            # Display results
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
