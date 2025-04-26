import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Anemia Assistant", page_icon="🩺", layout="centered")

password = st.text_input("Enter Password to Access:", type="password")
correct_password = "J2M2"

if not password:
    st.stop()

if password != correct_password:
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>ACCESS DENIED</h1>", unsafe_allow_html=True)
    st.stop()

st.title("🩺 Smart Anemia Assistant")

tab1, tab2, tab3 = st.tabs(["🧑‍⚕️ Patient Information", "🧬 Lab Results", "📝 Diagnosis & Plan"])

with tab1:
    st.header("Patient Information")
    patient_name = st.text_input("Patient Name")
    sex = st.selectbox("Sex", ("Male", "Female"))
    age = st.text_input("Age (years)")

with tab2:
    st.header("Lab Results")
    hb = st.text_input("Hemoglobin (g/dL)")
    mcv = st.text_input("MCV (fL)")
    mch = st.text_input("MCH (pg)")
    mchc = st.text_input("MCHC (g/dL)")
    ferritin = st.text_input("Ferritin (ng/mL)")
    serum_iron = st.text_input("Serum Iron (µg/dL)")
    tibc = st.text_input("TIBC (µg/dL)")
    retic = st.text_input("Reticulocyte Count (%)")
    vit_b12 = st.text_input("Vitamin B12 (pg/mL)")
    folate = st.text_input("Folate (ng/mL)")
    morphology = st.selectbox("Morphology findings", (
        "None", "Microcytic Hypochromic", "Macrocytic", "Normocytic",
        "Target Cells", "Sickle Cells", "Spherocytes", "Basophilic Stippling", "Schistocytes"
    ))

def diagnose_anemia(hb_val, mcv_val, mch_val, mchc_val, ferritin_val, serum_iron_val, tibc_val, retic_val, vit_b12_val, folate_val, morphology, sex, age_val):
    if mcv_val < 80:
        cell_size = "Microcytic"
    elif mcv_val > 100:
        cell_size = "Macrocytic"
    else:
        cell_size = "Normocytic"

    if mch_val < 27 or mchc_val < 32:
        chromia = "Hypochromic"
    elif mchc_val > 36:
        chromia = "Hyperchromic"
    else:
        chromia = "Normochromic"

    if age_val < 12:
        normal_hb = 11.5
    elif age_val >= 65:
        normal_hb = 12.5 if sex == "Male" else 11.5
    else:
        normal_hb = 13.5 if sex == "Male" else 12.0

    if hb_val >= normal_hb:
        severity = "No Anemia"
    elif hb_val >= 10:
        severity = "Mild"
    elif hb_val >= 7:
        severity = "Moderate"
    else:
        severity = "Severe"

    cause = "Unknown cause"
    if ferritin_val < 30 and serum_iron_val < 60 and tibc_val > 400:
        cause = "Iron Deficiency Anemia"
    elif morphology == "Target Cells":
        cause = "Thalassemia Minor"
    elif morphology == "Basophilic Stippling":
        cause = "Lead Poisoning"
    elif morphology == "Sickle Cells":
        cause = "Sickle Cell Disease"
    elif retic_val < 1 and hb_val < 8:
        cause = "Possible Aplastic Anemia"
    elif vit_b12_val < 200:
        cause = "Vitamin B12 Deficiency"
    elif folate_val < 3:
        cause = "Folate Deficiency"
    elif retic_val > 2.5:
        cause = "Hemolytic Anemia"
    elif ferritin_val > 100 and serum_iron_val < 60:
        cause = "Anemia of Chronic Disease"

    return severity, cell_size, chromia, cause

with tab3:
    st.header("Diagnosis & Plan")

    if st.button("🔍 Diagnose"):
        try:
            hb_val = float(hb) if hb else 0.0
            mcv_val = float(mcv) if mcv else 0.0
            mch_val = float(mch) if mch else 0.0
            mchc_val = float(mchc) if mchc else 0.0
            ferritin_val = float(ferritin) if ferritin else 0.0
            serum_iron_val = float(serum_iron) if serum_iron else 0.0
            tibc_val = float(tibc) if tibc else 0.0
            retic_val = float(retic) if retic else 0.0
            vit_b12_val = float(vit_b12) if vit_b12 else 0.0
            folate_val = float(folate) if folate else 0.0
            age_val = int(age) if age else 0

            severity, cell_size, chromia, cause = diagnose_anemia(
                hb_val, mcv_val, mch_val, mchc_val,
                ferritin_val, serum_iron_val, tibc_val,
                retic_val, vit_b12_val, folate_val, morphology, sex, age_val
            )

            diagnosis = f"{severity} {cell_size} {chromia} Anemia"

            st.success(f"✅ {diagnosis}")
            st.info(f"🔎 Most Likely Cause: {cause}")

            if severity == "Severe" or cause in ["Sickle Cell Disease", "Possible Aplastic Anemia"]:
                st.error("⚠️ WARNING: Critical Anemia detected! Immediate action required.")

            st.subheader("⚠️ Abnormal Test Results")
            abnormal_results = {}
            if hb_val < 10:
                abnormal_results["Hemoglobin"] = hb_val
            if mcv_val < 80:
                abnormal_results["MCV"] = mcv_val
            if mch_val < 27:
                abnormal_results["MCH"] = mch_val
            if mchc_val < 32:
                abnormal_results["MCHC"] = mchc_val
            if ferritin_val < 30:
                abnormal_results["Ferritin"] = ferritin_val
            if serum_iron_val < 50:
                abnormal_results["Serum Iron"] = serum_iron_val
            if tibc_val > 400:
                abnormal_results["TIBC"] = tibc_val
            if retic_val > 2.5:
                abnormal_results["Reticulocyte Count"] = retic_val
            if vit_b12_val < 200:
                abnormal_results["Vitamin B12"] = vit_b12_val
            if folate_val < 3:
                abnormal_results["Folate"] = folate_val

            if abnormal_results:
                for test, value in abnormal_results.items():
                    st.markdown(f"**{test}:** {value} (Abnormal)", unsafe_allow_html=True)

            st.subheader("💡 Recommendations")
            if cause == "Iron Deficiency Anemia":
                st.info("✅ **Recommendation:** Start oral iron supplementation. Consider gastrointestinal evaluation to check for bleeding sources.")
            elif cause == "Thalassemia Minor":
                st.info("✅ **Recommendation:** No iron therapy required unless deficiency is confirmed. Refer for hemoglobin electrophoresis if needed.")
            elif cause == "Vitamin B12 Deficiency":
                st.info("✅ **Recommendation:** Start Vitamin B12 injections or high-dose oral supplements.")
            elif cause == "Lead Poisoning":
                st.info("✅ **Recommendation:** Order blood lead level and eliminate environmental exposure. Refer to a specialist.")
            elif cause == "Sickle Cell Disease":
                st.info("✅ **Recommendation:** Immediate referral to hematology if crisis suspected. Pain management and hydration are crucial.")
            elif cause == "Aplastic Anemia":
                st.info("✅ **Recommendation:** Urgent referral to hematology. Bone marrow biopsy may be required.")
            elif cause == "Folate Deficiency":
                st.info("✅ **Recommendation:** Start folic acid supplementation.")
            elif cause == "Hemolytic Anemia":
                st.info("✅ **Recommendation:** Perform Coombs test and check LDH and haptoglobin levels.")
            elif cause == "Anemia of Chronic Disease":
                st.info("✅ **Recommendation:** Manage underlying chronic disease (e.g., infection, inflammatory condition).")

            st.subheader("📄 Patient Report")
            report = f"""
Patient Name: {patient_name}
Age/Sex: {age} years / {sex}

Hemoglobin: {hb} g/dL
MCV: {mcv} fL
MCH: {mch} pg
MCHC: {mchc} g/dL
Ferritin: {ferritin} ng/mL
Iron: {serum_iron} µg/dL
TIBC: {tibc} µg/dL
Reticulocyte Count: {retic} %
Vitamin B12: {vit_b12} pg/mL
Folate: {folate} ng/mL
Morphology: {morphology}

Diagnosis: {diagnosis}
Most Likely Cause: {cause}
"""
            st.text_area("Patient Report (Copy if needed)", report, height=400)

        except Exception as e:
            st.error(f"Error during diagnosis: {e}")
