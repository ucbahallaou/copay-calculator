# Patient Co-Pay Responsibility Calculator

This is a **Patient Responsibility Calculator** designed to help healthcare staff quickly calculate patient responsibility for specific services based on CPT codes and modifiers. The tool pulls fee data from the Medicare Fee Schedule (MDFS) from cms.gov to provide an accurate co-pay calculation based on the patient's responsibility percentage.

## Features
- Autocomplete functionality for easy CPT code selection.
- Dynamic modifier options based on selected CPT codes.
- Automatic calculation of total patient responsibility.
- Displays relevant MDFS data for transparency.

## Usage

### Step-by-Step Instructions
1. **Select CPT Code**: Begin typing the desired CPT code and select the appropriate option from the dropdown.
2. **Select Modifier**: Choose the applicable modifier for the selected CPT code, if available. If no modifier applies, select "No Modifier" (this is the default).
3. **Enter Patient Responsibility Percentage**: Input the percentage that represents the patient's co-pay responsibility.
4. **Add CPT Code**: Click **Add CPT Code** to add this entry to the list.
5. **Calculate Total Responsibility**: After adding all CPT codes and modifiers for the patient, click **Calculate Total Responsibility** to see the total co-pay amount.
6. **View Results**: The tool will display:
   - A **Patient Responsibility Table** summarizing each CPT code, modifier, responsibility percentage, and non-facility fee.
   - **MDFS Data** relevant to the selected CPT codes and modifiers for further reference.

### Example Scenario
If a patient has two CPT codes for different procedures, each with a different modifier and patient responsibility percentage, the tool will provide a cumulative responsibility amount based on these individual entries.

## Access the Tool
Click the link below to access the calculator:

👉 [Patient Responsibility Calculator](https://cls-copay-tool.streamlit.app/)
