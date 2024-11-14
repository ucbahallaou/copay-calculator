# import streamlit as st 
# import pandas as pd 

# # Load the CSV file into a DataFrame 
# @st.cache_data 
# def load_data(): 
#     return pd.read_csv('MDFS.csv') 

# data = load_data()

# # Ensure columns needed for merge are present in data
# if 'CPT' not in data.columns or 'Modifier' not in data.columns:
#     st.error("The CSV file is missing required columns: 'CPT' or 'Modifier'. Please check the file.")
# else:
#     # Initialize session state for storing CPT codes, modifiers, and patient responsibilities 
#     if 'cpt_codes' not in st.session_state: 
#         st.session_state.cpt_codes = [] 
#     if 'modifiers' not in st.session_state: 
#         st.session_state.modifiers = [] 
#     if 'responsibilities' not in st.session_state: 
#         st.session_state.responsibilities = [] 

#     st.title('Patient Responsibility Calculator') 

#     with st.expander("How to use this tool"): 
#         st.write(""" 
#             1. Enter the CPT code you see from a billing note in the 'Enter CPT Code' field. 
#             2. Select the appropriate modifier, if available. Default is 'No Modifier'.
#             3. Enter the patient's responsibility percentage in the 'Enter % Patient Responsibility' field. 
#             4. Click 'Add CPT Code' to add the CPT code, modifier, and responsibility to the list. 
#             5. If needed, you can remove all entered CPT codes and responsibilities by clicking 'Remove All Rows'. 
#             6. The entered data will be displayed on the right side, along with the corresponding 'Non Facility Fee' from the MDFS data. 
#             7. Click 'Calculate Total Responsibility' to see the total patient responsibility amount. 
#         """)

#     # Layout the app with input fields on the left and data on the right 
#     col1, col2 = st.columns(2) 
#     with col1: 
#         # Input fields for CPT code, modifier, and patient responsibility 
#         cpt_code = st.text_input('Enter CPT Code')
        
#         # Get unique modifiers for the selected CPT code
#         modifiers = data[data['CPT'] == cpt_code]['Modifier'].unique().tolist() if cpt_code in data['CPT'].values else []
#         modifiers.insert(0, 'No Modifier')  # Add a 'No Modifier' option by default
#         modifier = st.selectbox('Select Modifier', modifiers)
        
#         patient_responsibility = st.number_input('Enter % Patient Responsibility', min_value=0, max_value=100, step=1) 

#         # Button to add the CPT code, modifier, and responsibility to the list 
#         if st.button('Add CPT Code'): 
#             if cpt_code and patient_responsibility is not None: 
#                 # Append values to session state lists
#                 st.session_state.cpt_codes.append(cpt_code)
#                 st.session_state.modifiers.append(modifier)
#                 st.session_state.responsibilities.append(patient_responsibility) 

#         # Button to remove all rows 
#         if st.session_state.cpt_codes: 
#             if st.button('Remove All Rows'): 
#                 st.session_state.cpt_codes = [] 
#                 st.session_state.modifiers = []
#                 st.session_state.responsibilities = []

#     with col2: 
#         # Ensure lists are of the same length before creating the DataFrame
#         if len(st.session_state.cpt_codes) == len(st.session_state.modifiers) == len(st.session_state.responsibilities):
#             if st.session_state.cpt_codes: 
#                 input_data = pd.DataFrame({ 
#                     'CPT Code': st.session_state.cpt_codes, 
#                     'Modifier': st.session_state.modifiers,
#                     '% Patient Responsibility': st.session_state.responsibilities 
#                 })

#                 # Merge input data with MDFS data to get 'Non Facility Fee' 
#                 merged_input_data = input_data.merge(data[['CPT', 'Modifier', 'Non Facility Fee']], 
#                                                      left_on=['CPT Code', 'Modifier'], 
#                                                      right_on=['CPT', 'Modifier'], 
#                                                      how='left') 
#                 merged_input_data['% pts'] = merged_input_data['% Patient Responsibility'].astype(str) + '%' 
#                 merged_input_data.set_index(['CPT Code', 'Modifier'], inplace=True) 
#                 st.write(merged_input_data[['% pts', 'Non Facility Fee']]) 
                
#                 # Calculate total responsibility
#                 merged_data = input_data.merge(data, left_on=['CPT Code', 'Modifier'], right_on=['CPT', 'Modifier'])
#                 merged_data['Patient Responsibility'] = (merged_data['% Patient Responsibility'] / 100) * merged_data['Non Facility Fee'] 
#                 total_responsibility = merged_data['Patient Responsibility'].sum() 

#                 if st.button('Calculate Total Responsibility'): 
#                     st.write(f'### Total Patient Responsibility: ${total_responsibility:.2f}') 
              
#                 # Display MDFS data for the entered CPT codes and selected modifiers
#                 merged_data.set_index(['CPT Code', 'Modifier'], inplace=True) 
#                 st.write('### MDFS Data:') 
#                 st.write(merged_data) 

import streamlit as st
import pandas as pd

# Load the CSV file into a DataFrame
@st.cache_data
def load_data():
    return pd.read_csv('MDFS.csv')

data = load_data()

# Ensure columns needed for merge are present in data
if 'CPT' not in data.columns or 'Modifier' not in data.columns:
    st.error("The CSV file is missing required columns: 'CPT' or 'Modifier'. Please check the file.")
else:
    # Initialize session state for storing CPT codes, modifiers, and patient responsibilities
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
            2. Select the appropriate modifier, if available. Default is 'No Modifier'.
            3. Enter the patient's responsibility percentage in the 'Enter % Patient Responsibility' field.
            4. Click 'Add CPT Code' to add the CPT code, modifier, and responsibility to the list.
            5. Click 'Calculate Total Responsibility' to see the total patient responsibility amount.
            6. The entered data will be displayed below the inputs.
        """)

    # Layout the app with input fields on the left and data on the right
    col1, col2 = st.columns(2)
    with col1:
        # Single selectbox for CPT code selection with autocomplete
        all_cpt_codes = data['CPT'].astype(str).unique().tolist()
        cpt_code = st.selectbox('Select CPT Code', all_cpt_codes)

        # Get unique modifiers for the selected CPT code
        modifiers = data[data['CPT'] == cpt_code]['Modifier'].unique().tolist()
        modifiers.insert(0, 'No Modifier')  # Add a 'No Modifier' option by default
        modifier = st.selectbox('Select Modifier', modifiers)

        patient_responsibility = st.number_input('Enter % Patient Responsibility', min_value=0, max_value=100, step=1)

        # Button to add the CPT code, modifier, and responsibility to the list
        if st.button('Add CPT Code'):
            if cpt_code and patient_responsibility is not None:
                # Append values to session state lists
                st.session_state.cpt_codes.append(cpt_code)
                st.session_state.modifiers.append(modifier)
                st.session_state.responsibilities.append(patient_responsibility)

        # Button to remove all rows
        if st.session_state.cpt_codes:
            if st.button('Remove All Rows'):
                st.session_state.cpt_codes = []
                st.session_state.modifiers = []
                st.session_state.responsibilities = []

    # Display the calculated Patient Responsibility Table in the right column
    with col2:
        if len(st.session_state.cpt_codes) == len(st.session_state.modifiers) == len(st.session_state.responsibilities):
            if st.session_state.cpt_codes:
                input_data = pd.DataFrame({
                    'CPT Code': st.session_state.cpt_codes,
                    'Modifier': st.session_state.modifiers,
                    '% Patient Responsibility': st.session_state.responsibilities
                })

                # Merge input data with MDFS data to get 'Non Facility Fee'
                merged_input_data = input_data.merge(data[['CPT', 'Modifier', 'Non Facility Fee']],
                                                     left_on=['CPT Code', 'Modifier'],
                                                     right_on=['CPT', 'Modifier'],
                                                     how='left')
                merged_input_data['% pts'] = merged_input_data['% Patient Responsibility'].astype(str) + '%'
                merged_input_data.set_index(['CPT Code', 'Modifier'], inplace=True)

                st.write('### Patient Responsibility Table')
                st.write(merged_input_data[['% pts', 'Non Facility Fee']])

                # Calculate total responsibility
                merged_data = input_data.merge(data, left_on=['CPT Code', 'Modifier'], right_on=['CPT', 'Modifier'])
                merged_data['Patient Responsibility'] = (merged_data['% Patient Responsibility'] / 100) * merged_data['Non Facility Fee']
                total_responsibility = merged_data['Patient Responsibility'].sum()

                if st.button('Calculate Total Responsibility'):
                    st.write(f'### Total Patient Responsibility: ${total_responsibility:.2f}')

    # Display the MDFS Data Table at the bottom
    if st.session_state.cpt_codes:
        st.write('### MDFS Data for Selected CPT Codes and Modifiers')
        merged_data.set_index(['CPT Code', 'Modifier'], inplace=True)
        st.write(merged_data)


 
