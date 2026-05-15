from re import L
import numpy as np 
import matplotlib.pyplot as plt
import csv
from rdkit import Chem
import torch
from tqdm import tqdm
import pickle
import gc
import random
import time
import dgl
import os

from .featurizing_helpers import *

import itertools

from graphormer.data import register_dataset
from sklearn.model_selection import train_test_split

from pathlib import Path

# 1. Anchor to the project root (3 levels up from the loader subfolder)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# 2. Dynamically determine 'mode' and 'type' from the filename/folder
# Example: CCS_loader_train.py -> mode='CCS', type='train'
file_name = Path(__file__).stem
parts = file_name.split('_')
mode = parts[0]      # GC, CCS, etc.
data_type = parts[-1] # train, test

# 3. Define the paths relative to the root
DICT_PATH = PROJECT_ROOT / "sample_data" / "all_col_metadata_20260512.pickle"
DATA_PATH = PROJECT_ROOT / "sample_data" / f"{mode}_sample_{data_type}.csv"

print("YOU'RE DEF IN THE CORRECT FILE")
print(f"Loading {mode} {data_type} data from: {DATA_PATH}")


companies = ['', 'Waters', 'Thermo', 'Agilent', 'Restek', 'Merck', 'Phenomenex', 'HILICON','GL','Advanced', 'Other']
USPs = ['', 'L1', 'L10', 'L109', 'L11', 'L43', 'L68', 'L3','L114', 'L112', 'L122', 'L7', 'L10', 'Other']
solvs = ['h2o','meoh', 'acn', 'iproh', 'Other']
HPLCs = ['RP', 'HILIC', 'PFP', 'Other']


def one_hot_HPLC_type(HPLC_type):
    one_hot = [0] * len(HPLCs)
    if HPLC_type in HPLCs:
        one_hot[HPLCs.index(HPLC_type)] = 1
    else:
        one_hot[-1] = 1
    return one_hot


def one_hot_company(company):
    one_hot = [0] * len(companies)
    if company in companies:
        one_hot[companies.index(company)] = 1
    else:
        one_hot[-1] = 1
    return one_hot

  
def one_hot_USP(USP):
    one_hot = [0] * len(USPs)
    if USP in USPs:
        one_hot[USPs.index(USP)] = 1
    else:
        one_hot[-1] = 1
    return one_hot

def one_hot_solvent(solvent):
    one_hot = [0] * len(solvs)
    if solvent in solvs:
        one_hot[solvs.index(solvent)] = 1
    else:
        one_hot[-1] = 1
    return one_hot

  
def featurize_column(column_params, index):

    company = one_hot_company(column_params[0])
    USP = one_hot_USP(column_params[1])

    length = float(column_params[2]) / 250 ## consider mapping these into fixed bins for steps of 50 

    if column_params[3] == '':
        diameter = 0
    else:
        diameter = float(column_params[3]) ## normalizing diameter

    part_size = float(column_params[4])
    temp = float(column_params[5]) / 100 ## normalizing temperature (rethink this maybe)
    fl = float(column_params[6])  ## Double check that fl and col_fl are two different values
    dead = float(column_params[7]) ## dead time - MAYBE REMOVE COLUMN THAT HAS DEAD TIME OF ZERO

    type = one_hot_HPLC_type(column_params[8])

    lc_type = column_params[8]

    solv_A = one_hot_solvent(column_params[9])
    solv_B = one_hot_solvent(column_params[10])

    # time_start_B = float(column_params[11]) ## this is always zero, so redundant
    start_B = float(column_params[12]) / 100
    t1 = float(column_params[13]) 
    B1 = float(column_params[14]) / 100
    t2 = float(column_params[15]) 
    B2 = float(column_params[16]) / 100
    t3 = float(column_params[17]) 
    B3 = float(column_params[18]) / 100


    pH_A = float(column_params[19].replace('', '0')) / 14
    pH_B = float(column_params[20].replace('', '0')) / 14

    add_A = column_params[25:55]
    add_B = column_params[55:85]
    
    add_A = ['0' if val == '' else val for val in column_params[25:55]]
    add_B = ['0' if val == '' else val for val in column_params[55:85]]
    
    tanaka_params = column_params[85:92]
    tanaka_params = [2.7 if param == '2.7 spp' else param for param in tanaka_params]
    tanaka_params = [2.7 if param == '2.6 spp' else param for param in tanaka_params]

    tanaka_params = [0 if param == '' else float(param) for param in tanaka_params] 

    hsmb_params = column_params[92:]
    hsmb_params = [0 if param == '' else float(param) for param in hsmb_params]

    kPB = tanaka_params[1]     
    a_CH2 = tanaka_params[2]
    a_TO = tanaka_params[3]
    a_CP = tanaka_params[4]
    a_BP = tanaka_params[5] 
    a_BP1 = tanaka_params[6]
    # particle_size = tanaka_params[7] #/ 5
    
    tanaka_params = [kPB, a_CH2, a_TO, a_CP, a_BP, a_BP1, part_size]

    add_A_vals = np.ceil(list(map(float, add_A[::2])))
    add_A_vals = np.ceil([float(val) for val in add_A[::2]])
    add_B_vals = np.ceil([float(val) for val in add_B[::2]])
    
    add_A_vals = np.ceil(list(map(float, add_A[::2]))) 
    add_B_vals = np.ceil(list(map(float, add_B[::2])))

    add_A_units = add_A[1::2]
    add_B_units = add_B[1::2]

    float_encodings = [diameter, part_size, start_B, t1, B1, t2, B2, t3, B3, pH_A, pH_B, dead, temp, fl, length] 

    float_encodings += tanaka_params
    float_encodings += hsmb_params

    int_encodings = np.concatenate([[-2],company, USP, solv_A, solv_B, add_A_vals, add_B_vals, type])

    features = np.concatenate((int_encodings, float_encodings))
  
    return features


class AtomBondEncd(DGLDataset):
    def __init__(self):
        self.mode = ":("
        ## atom encodings
        atom_type_onehot = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ]

        formal_charge_onehot =[
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ]

        hybridization_onehot =[
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ]

        is_aromatic_onehot = [
            [0], 
            [1]
        ]

        total_num_H_onehot = [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ]

        explicit_valence_onehot = [
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0], 
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]

        total_bonds_onehot = [
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0], 
            [0, 0, 0, 0, 0, 0, 1],
        ]

        i = 0
        self.one_hotatom_to_int_keys = []
        self.one_hotatom_to_int_values = []
        self.hash_dictatom = {}
        self.comb_atom = False

        if self.comb_atom: ## if you want to do combinatoric atom hashing
            for x1 in atom_type_onehot:
                for x2 in formal_charge_onehot:
                    for x3 in hybridization_onehot:
                        for x4 in is_aromatic_onehot:
                            for x5 in total_num_H_onehot: 
                                for x6 in explicit_valence_onehot:
                                    for x7 in total_bonds_onehot:
                                        key = torch.cat([torch.Tensor(y) for y in [x1, x2, x3, x4, x5, x6, x7]])
                                        self.one_hotatom_to_int_keys += [key]
                                        self.one_hotatom_to_int_values += [i]
                                        i+=1
                                                        
            count = 0
            while count < len(self.one_hotatom_to_int_keys):
                h = str(self.one_hotatom_to_int_keys[count])
                self.hash_dictatom[h] = self.one_hotatom_to_int_values[count]
                count +=1

        ## combinatoric bond mapping
        bond_type_onehot = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        is_in_ring_onehot = [
            [0], 
            [1]
        ]

        bond_stereo_onehot = [
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]

        is_global_node = [
            [0],
            [1]
        ]

        i = 0
        self.one_hot_to_int_keys = []
        self.one_hot_to_int_values = []
        self.hash_dict = {}
        for x1 in bond_type_onehot:
            for x3 in is_in_ring_onehot:
                for x4 in bond_stereo_onehot:
                    for x5 in is_global_node:
                        key = torch.cat([torch.Tensor(y) for y in [x1, x3, x4, x5]])
                        self.one_hot_to_int_keys += [key]
                        self.one_hot_to_int_values += [i]
                        i+=1

        count = 0
        while count < len(self.one_hot_to_int_keys):
            h = str(self.one_hot_to_int_keys[count])
            self.hash_dict[h] = self.one_hot_to_int_values[count]
            count +=1

        self.num_classes = 1801
        super().__init__(name='RT', ) 

  
    def process(self):
        
        self.graphs = []
        self.labels = []
        self.smiles = []

        print("I'm in the right file")

        # Change data path accordingly
        x = import_data(str(DATA_PATH))

        # Change method dictionary path accordingly
        with open(DICT_PATH, 'rb') as handle: 
            self.columndict = pickle.load(handle) 

        keys = list(self.columndict.keys())
        index_dict = {}

        for j, key in enumerate(keys):
            index_dict[key] = j

        gnode = True ## Turns off global node
        count = 0
 
        for i in tqdm(x):
            
            sm = str(i[0]).replace("Q", "#") ## Hashtags break some of our preprocessing scripts so we replace them with Qs to make life easier 
            mol = Chem.MolFromSmiles(sm)
            rt = torch.tensor([float(i[1])]) / 10000  #  rescaling CCS by another factor of 10

            # Change method name accordingly
            index = 'CCS'
            col_meta = self.columndict[index]
            
            col_ind = index_dict[index]

            column_params = featurize_column(col_meta, index)
            ablate_info = False
            if ablate_info: 
                column_params = np.zeros_like(column_params)
                column_params[0] = col_ind

            num_atoms = mol.GetNumAtoms()
            add_self_loop = False
            g = mol_to_bigraph(mol, explicit_hydrogens=False, node_featurizer=GraphormerAtomFeaturizer(), edge_featurizer=CanonicalBondFeaturizer(), add_self_loop=False) ## uses DGL featurization function                

            count1 = 0
            count2 = 0

            unif = []
            unifatom = []
          
            ### GLOBAL NODE Encodings
            while count2 < len(g.ndata['h']): ## getting all the parameters needed for the global node generation
                hatom = g.ndata['h'][count2][:]
                unifatom.append(list(np.asarray(hatom)))
                flength = len(list(hatom))
                count2 += 1

            features_gnode = False ## if you want a second global node

            if gnode:
                src_list = list(np.full(num_atoms, num_atoms)) ## node pairs describing edges in heteograph - see DGL documentation
                dst_list = list(np.arange(num_atoms))
                features = torch.tensor([[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]], dtype=torch.float32)
                total_features = features.repeat(num_atoms, 1)

                g_nm = column_params ## custom encoding for the global node
                # g_nm = global_feat #column_params ## custom encoding for the global node
                unifatom.append(g_nm)
                g.add_nodes(1)
                g.ndata['h'] = torch.tensor(np.asarray(unifatom))
                g.add_edges(src_list, dst_list, {'e': total_features}) ## adding all the edges for the global node

            if features_gnode:
                src_list = list(np.full(num_atoms, num_atoms + 1)) ## increasing the global node index by one (second global node)
                dst_list = list(np.arange(num_atoms)) ## no connection to the other global node
                features = torch.tensor([[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]], dtype=torch.float32)
                total_features = features.repeat(num_atoms, 1)
                g.add_nodes(1)
                g_nm = descriptors ## custom encoding for the global node
                unifatom.append(g_nm)
                g.ndata['h'] = torch.tensor(np.asarray(unifatom))
                g.add_edges(src_list, dst_list, {'e': total_features}) ## adding all the edges for the global node
            if g.edata == {}:
                print("We did it mom - one atom molecule doesn't break things")
            else:
                while count1 < len(g.edata['e']): ## doing this for the column metadata
      
                    h = str(g.edata['e'][count1])
                    unif.append(self.hash_dict[h])
                    count1 += 1
                
                count1 = 0
                g.edata['e'] = torch.transpose(torch.tensor(unif), 0, -1) + 1

            self.graphs.append(g)
            self.labels.append(rt)
            self.smiles.append((sm, index))
            count+=1
          

    def __getitem__(self, i):
        # print(i)
        return self.graphs[i], self.labels[i], self.smiles[i]

  
    def __len__(self):
        return len(self.graphs)


# Change dataset-name to match bash script
@register_dataset("CCS_test")
def create_customized_dataset():

    dataset = AtomBondEncd()
    num_graphs = len(dataset)

    train = 0.8
    val = 0.1
    test = 0.1

    return {
        "dataset": dataset,
        "train_idx":  np.arange(0, int(num_graphs * train)),
        "valid_idx": np.arange(int(num_graphs * train), int(num_graphs * (train + val))),
        "test_idx": None, #
        "source": "dgl" 
    }
