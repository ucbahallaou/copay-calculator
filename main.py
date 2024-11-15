import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv('MDFS.csv')

data = load_data()

if 'CPT' not in data.columns or 'Modifier' not in data.columns:
    st.error("The CSV file is missing required columns: 'CPT' or 'Modifier'. Please check the file.")
else:
    if 'cpt_codes' not in st.session_state:
        st.session_state.cpt_codes = []
    if 'modifiers' not in st.session_state:
        st.session_state.modifiers = []
    if 'responsibilities' not in st.session_state:
        st.session_state.responsibilities = []

    st.title('Patient Responsibility Calculator')

    with st.expander("How to use this tool"):
        st.write("""
            1. Select the CPT code from the dropdown.
            2. Select the appropriate modifier, if available. The first modifier option is selected by default.
            3. Enter the patient's responsibility percentage in the 'Enter % Patient Responsibility' field.
            4. Enter any copay or deductible amounts due, if applicable.
            5. Click 'Add CPT Code' to add this entry to the list.
            6. Click 'Calculate Total Responsibility' to see the total patient responsibility amount.
            7. The entered data will be displayed below the inputs.
        """)

    col1, col2 = st.columns(2)
    with col1:
        all_cpt_codes = data['CPT'].astype(str).unique().tolist()
        cpt_code = st.selectbox('Select CPT Code', all_cpt_codes)

        modifiers = data[data['CPT'] == cpt_code]['Modifier'].unique().tolist()
        default_modifier = modifiers[0] if modifiers else 'No Modifier'  # Set the first modifier as default
        modifier = st.selectbox('Select Modifier', modifiers, index=0) if modifiers else default_modifier

        patient_responsibility = st.number_input('Enter % Patient Responsibility', min_value=0, max_value=100, step=1)

        copay_amount = st.number_input("Copay Amount due (if applicable)", min_value=0.0, value=0.0, step=0.01)
        deductible_amount = st.number_input("Deductible amount due (if applicable)", min_value=0.0, value=0.0, step=0.01)

        if st.button('Add CPT Code'):
            if cpt_code and patient_responsibility is not None:
                # Append values to session state lists
                st.session_state.cpt_codes.append(cpt_code)
                st.session_state.modifiers.append(modifier)
                st.session_state.responsibilities.append(patient_responsibility)

        if st.session_state.cpt_codes:
            if st.button('Remove All Rows'):
                st.session_state.cpt_codes = []
                st.session_state.modifiers = []
                st.session_state.responsibilities = []

    with col2:
        if len(st.session_state.cpt_codes) == len(st.session_state.modifiers) == len(st.session_state.responsibilities):
            if st.session_state.cpt_codes:
                input_data = pd.DataFrame({
                    'CPT Code': st.session_state.cpt_codes,
                    'Modifier': st.session_state.modifiers,
                    '% Patient Responsibility': st.session_state.responsibilities
                })

                merged_input_data = input_data.merge(data[['CPT', 'Modifier', 'Non Facility Fee']],
                                                     left_on=['CPT Code', 'Modifier'],
                                                     right_on=['CPT', 'Modifier'],
                                                     how='left')
                merged_input_data['% pts'] = merged_input_data['% Patient Responsibility'].astype(str) + '%'
                merged_input_data.set_index(['CPT Code', 'Modifier'], inplace=True)

                st.write('### Patient Responsibility Table')
                st.write(merged_input_data[['% pts', 'Non Facility Fee']])

                merged_data = input_data.merge(data, left_on=['CPT Code', 'Modifier'], right_on=['CPT', 'Modifier'])
                merged_data['Patient Responsibility'] = (merged_data['% Patient Responsibility'] / 100) * merged_data['Non Facility Fee']
                total_responsibility = merged_data['Patient Responsibility'].sum()

                total_responsibility += copay_amount + deductible_amount

                if st.button('Calculate Total Responsibility'):
                    st.write(f'### Total Patient Responsibility: ${total_responsibility:.2f}')

    if st.session_state.cpt_codes:
        st.write('### MDFS Data for Selected CPT Codes and Modifiers')
        merged_data.set_index(['CPT Code', 'Modifier'], inplace=True)
        st.write(merged_data)



 
