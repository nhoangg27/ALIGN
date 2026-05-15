import pickle
import os
import numpy as np

## STATE DICT = THESE ARE THE CURRENTLY INITIAZLED EMBEDDINGS FOR ONE HOT ENCODED VALUES. 
## spelling and case matter here, if not the code will use the 'Other' embedding 
## float values theoretically have no limit, empty values are set to 0
companies = ['', 'Waters', 'Thermo', 'Agilent', 'Restek', 'Merck', 'Phenomenex', 'HILICON','GL','Advanced', 'Other']
USPs = ['', 'L1', 'L10', 'L109', 'L11', 'L43', 'L68', 'L3','L114', 'L112', 'L122', 'L7', 'L10', 'Other']
solvs = ['h2o','meoh', 'acn', 'iproh', 'Other']
HPLCs = ['RP', 'HILIC', 'PFP', 'Other']

method_name = 'Fiehn_HILIC'
company_name = 'Waters'
usp_code = 'L68'
col_length = 150 ## 0 for non-defined float values
col_innerdiam = 2.1
col_part_size = 1.7
temp = 45 ##
col_fl = 0.6
col_dead = 0.8268749999999999  ## calculated by RepoRT, col_dead = 0.0005 * col_length * col_innerdiam**2 / col_fl
HPLC_type = 'HILIC'
A_solv = 'acn'
B_solv = 'h2o'
## Gradient inflection points
time1 = 2.0
grad1 = 0.0
time2 = 7.7
grad2 = 30.0
time3 = 9.5
grad3 = 60.0
time4 = 12.75
grad4 = 60.0
A_pH = '9.8'
B_pH = '0'
A_start = 100
A_end = 100
B_start = 0
B_end = 0
## Additive concentrations and units (see re)
eluent_A_formic = 0.1
eluent_A_formic_unit = '%'
eluent_A_acetic = 0
eluent_A_acetic_unit =  ''
eluent_A_trifluoroacetic = 0
eluent_A_trifluoroacetic_unit = ''
eluent_A_phosphor = 0
eluent_A_phosphor_unit = ''
eluent_A_nh4ac = 0
eluent_A_nh4ac_unit = ''
eluent_A_nh4form = 10
eluent_A_nh4form_unit = 'mM'
eluent_A_nh4carb = 0
eluent_A_nh4carb_unit = ''
eluent_A_nh4bicarb = 0
eluent_A_nh4bicarb_unit = ''
eluent_A_nh4f = 0
eluent_A_nh4f_unit = ''
eluent_A_nh4oh = 0
eluent_A_nh4oh_unit = ''
eluent_A_trieth = 0
eluent_A_trieth_unit = ''
eluent_A_triprop = 0
eluent_A_triprop_unit = ''
eluent_A_tribut = 0
eluent_A_tribut_unit = ''
eluent_A_nndimethylhex = 0
eluent_A_nndimethylhex_unit = '' 
eluent_A_medronic = 0
eluent_A_medronic_unit = ''
eluent_B_formic = 0.1
eluent_B_formic_unit = '%'
eluent_B_acetic = 0
eluent_B_acetic_unit = ''
eluent_B_trifluoroacetic = 0
eluent_B_trifluoroacetic_unit = ''
eluent_B_phosphor = 0
eluent_B_phosphor_unit = ''
eluent_B_nh4ac = 0
eluent_B_nh4ac_unit = ''
eluent_B_nh4form = 10
eluent_B_nh4form_unit = 'mM'
eluent_B_nh4carb = 0
eluent_B_nh4carb_unit = ''
eluent_B_nh4bicarb = 0
eluent_B_nh4bicarb_unit = ''
eluent_B_nh4f = 0
eluent_B_nh4f_unit = ''
eluent_B_nh4oh = 0
eluent_B_nh4oh_unit = ''
eluent_B_trieth = 0
eluent_B_trieth_unit = ''
eluent_B_triprop = 0
eluent_B_triprop_unit = ''
eluent_B_tribut = 0
eluent_B_tribut_unit = ''
eluent_B_nndimethylhex = 0
eluent_B_nndimethylhex_unit = '' 
eluent_B_medronic = 0
eluent_B_medronic_unit = ''

## Tanaka parameters (calculated by RepoRT)
kPB = 0
alpha_CH2 = 0
alpha_T_O = 0
alpha_C_P = 0
alpha_B_P = 0
alpha_B_P1 = 0

## HSMB Parameters (calcualted by RepoRT)
particle_size = 0
pore_size = 0
H = 0
S_star = 0.0
A = 0
B = 0
C_pH_28 = 0
C_pH_7 = 0
EB_ret_factor = 0

column_params = [company_name, usp_code, col_length, col_innerdiam, col_part_size, temp, col_fl, col_dead, HPLC_type, A_solv, B_solv, time1, grad1, time2, grad2, time3, grad3, time4, grad4, \
                 A_pH, B_pH, A_start, A_end, B_start, B_end, eluent_A_formic, eluent_A_formic_unit, eluent_A_acetic, eluent_A_acetic_unit, eluent_A_trifluoroacetic, eluent_A_trifluoroacetic_unit, eluent_A_phosphor, eluent_A_phosphor_unit, eluent_A_nh4ac, eluent_A_nh4ac_unit, eluent_A_nh4form, eluent_A_nh4form_unit, eluent_A_nh4carb, eluent_A_nh4carb_unit, eluent_A_nh4bicarb, eluent_A_nh4bicarb_unit, eluent_A_nh4f, eluent_A_nh4f_unit, eluent_A_nh4oh, eluent_A_nh4oh_unit, eluent_A_trieth, eluent_A_trieth_unit, eluent_A_triprop, eluent_A_triprop_unit, eluent_A_tribut, eluent_A_tribut_unit, eluent_A_nndimethylhex, eluent_A_nndimethylhex_unit, eluent_A_medronic, eluent_A_medronic_unit, eluent_B_formic, eluent_B_formic_unit, eluent_B_acetic, eluent_B_acetic_unit, eluent_B_trifluoroacetic, eluent_B_trifluoroacetic_unit, eluent_B_phosphor, eluent_B_phosphor_unit,eluent_B_nh4ac ,eluent_B_nh4ac_unit ,eluent_B_nh4form ,eluent_B_nh4form_unit ,eluent_B_nh4carb ,eluent_B_nh4carb_unit ,eluent_B_nh4bicarb ,eluent_B_nh4bicarb_unit ,eluent_B_nh4f ,eluent_B_nh4f_unit ,eluent_B_nh4oh ,eluent_B_nh4oh_unit ,eluent_B_trieth ,eluent_B_trieth_unit ,eluent_B_triprop ,eluent_B_triprop_unit ,eluent_B_tribut ,eluent_B_tribut_unit ,eluent_B_nndimethylhex ,eluent_B_nndimethylhex_unit ,eluent_B_medronic ,eluent_B_medronic_unit, \
                 kPB ,alpha_CH2 ,alpha_T_O ,alpha_C_P ,alpha_B_P , alpha_B_P1 ,particle_size ,pore_size ,H ,S_star ,A ,B ,C_pH_28 ,C_pH_7 ,EB_ret_factor]

dict_path = '/workspace/align/sample_data/all_col_metadata_20250512.pickle'

with open(dict_path, 'rb') as f:
    data = pickle.load(f)
    header = data['header']
    f.close()

assert len(header) == len(column_params), f"Header length {len(header)} does not match column params length {len(column_params)}"

data[method_name] = column_params

# Either write to new .pickle file to avoid corrupting the old file, or add on to it
output_path = '/workspace/graphormer-rt/sample_data/all_col_metadata_20250512.pickle'

with open(output_path, 'wb') as f:
    pickle.dump(data, f)
    f.close()

with open(output_path, 'rb') as f:
    data = pickle.load(f)

print(data.keys())
    


