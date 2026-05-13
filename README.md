# **ALIGNing Learned Representations: Domain-General Models Triangulate Physicochemical Interactions in Analytical Separations**

# General
Graphormer-RT is an extension to the Graphormer package, with [documentation](https://graphormer.readthedocs.io/), and the original code on [Github](https://github.com/microsoft/Graphormer/) with additional usage examples. If you use this code, **please cite our work that led to the development of this platform and the original Graphormer**

```bibtex
@article{Stienstra2025,
   author = {Cailum M.K. Stienstra and Emir Nazdrajić and W. Scott Hopkins},
   doi = {10.1021/ACS.ANALCHEM.4C05859},
   issn = {15206882},
   journal = {Analytical Chemistry},
   publisher = {American Chemical Society},
   title = {From Reverse Phase Chromatography to HILIC: Graph Transformers Power Method-Independent Machine Learning of Retention Times},
   url = {https://pubs.acs.org/doi/abs/10.1021/acs.analchem.4c05859},
   year = {2025},
}

@article{Stienstra2025,
   author = {Cailum M.K. Stienstra and Teun van Wieringen and Liam Hebert and Patrick Thomas and Kas J. Houthuijs and Giel Berden and Jos Oomens and Jonathan Martens and W. Scott Hopkins},
   doi = {10.1021/ACS.JCIM.4C02329},
   issn = {1549960X},
   journal = {Journal of Chemical Information and Modeling},
   publisher = {American Chemical Society},
   title = {A Machine-Learned “Chemical Intuition” to Overcome Spectroscopic Data Scarcity},
   volume = {65},
   url = {https://pubs.acs.org/doi/full/10.1021/acs.jcim.4c02329},
   year = {2025},
}

@article{Stienstra2024,
   author = {Cailum M. K. Stienstra and Liam Hebert and Patrick Thomas and Alexander Haack and Jason Guo and W. Scott Hopkins},
   doi = {10.1021/ACS.JCIM.4C00378},
   issn = {1549-9596},
   journal = {Journal of Chemical Information and Modeling},
   month = {6},
   publisher = {American Chemical Society},
   title = {Graphormer-IR: Graph Transformers Predict Experimental IR Spectra Using Highly Specialized Attention},
   url = {https://pubs.acs.org/doi/abs/10.1021/acs.jcim.4c00378},
   year = {2024},
}

@inproceedings{
ying2021do,
title={Do Transformers Really Perform Badly for Graph Representation?},
author={Chengxuan Ying and Tianle Cai and Shengjie Luo and Shuxin Zheng and Guolin Ke and Di He and Yanming Shen and Tie-Yan Liu},
booktitle={Thirty-Fifth Conference on Neural Information Processing Systems},
year={2021},
url={https://openreview.net/forum?id=OeWooOxFwDa}
}
```

# Installation
We highly recommend following the [installation guide](https://graphormer.readthedocs.io/), though we will suggest a few additional notes to make things easier:
- Install fairseq directly from the [Github repository](https://github.com/facebookresearch/fairseq), "pip install -e /path/to/folder" Make sure that you're using an old enough version that's compatible with Graphormer
- Make sure that you're using an old enough version of PyTorch Geometric and the DGL libraries (there's a lookup table for compatibility on their website). These are the things that we found broke the most frequently, and the errors you get don't always tell you that it's these packages. If there are problems inheriting abstract data classes, just modify the class methods to include whatever class methods (e.g., "\_\_len\_\_"), in your install and it should work.
- Refer to "requirement.txt" if you have any problems with version compatability.
- Ensure that your CUDA and pytorch geometric versions are compatabile. 

# Data
All data used in this study is publically available at the RepoRT github (https://github.com/michaelwitting/RepoRT/). **EDIT THIS FOR HUAN & LIT DATA** Those using this data should cite this work as follows:

```bibtex
@article{Kretschmer2024,
   author = {Fleming Kretschmer and Eva Maria Harrieder and Martin A. Hoffmann and Sebastian Böcker and Michael Witting},
   doi = {10.1038/s41592-023-02143-z},
   issn = {1548-7105},
   issue = {2},
   journal = {Nature Methods 2024 21:2},
   keywords = {Analytical biochemistry,Databases,Metabolomics},
   month = {1},
   pages = {153-155},
   pmid = {38191934},
   publisher = {Nature Publishing Group},
   title = {RepoRT: a comprehensive repository for small molecule retention times},
   volume = {21},
   url = {https://www.nature.com/articles/s41592-023-02143-z},
   year = {2024},
}
```

All of our training libraries for this study can be directly obtained from their library, by utilizing the dataprocessing scripts outlined in the folder. These 
scripts need their paths to be manually modified to received a "RepoRT-like" data structure. If you wish to adapt your gradient/LC method to our model, we highly recommend
structuring your data like a RepoRT entry and apply our scripts to generate an entry in our method data dictionary.

The pickle file (/home/nhi/A-RT/A-RT_fused/sample_data/all_col_metadata_20260512.pickle) contain processed column metada generated from RepoRT with the following headers, some of which (_e.g.,_ void volume or HSMB/Tanaka parameters) are calculated directly using RepoRT scripts:
```headers
['company_name', 'usp_code', 'col_length', 'col_innerdiam', 'col_part_size', 'temp', 'col_fl', 'col_dead', 'HPLC_type','A_solv', 'B_solv', 'time1', 'grad1', 'time2', 'grad2', 'time3', 'grad3', 'time4', 'grad4', 'A_pH', 'B_pH', 'A_start', 'A_end', 'B_start', 'B_end',  'eluent_A_formic', 'eluent_A_formic_unit', 'eluent_A_acetic', 'eluent_A_acetic_unit','eluent_A_trifluoroacetic', 'eluent_A_trifluoroacetic_unit','eluent_A_phosphor', 'eluent_A_phosphor_unit','eluent_A_nh4ac','eluent_A_nh4ac_unit', 'eluent_A_nh4form','eluent_A_nh4form_unit','eluent_A_nh4carb', 'eluent_A_nh4carb_unit','eluent_A_nh4bicarb','eluent_A_nh4bicarb_unit', 'eluent_A_nh4f','eluent_A_nh4f_unit','eluent_A_nh4oh', 'eluent_A_nh4oh_unit','eluent_A_trieth','eluent_A_trieth_unit','eluent_A_triprop','eluent_A_triprop_unit','eluent_A_tribut', 'eluent_A_tribut_unit','eluent_A_nndimethylhex', 'eluent_A_nndimethylhex_unit','eluent_A_medronic', 'eluent_A_medronic_unit','eluent_B_formic', 'eluent_B_formic_unit', 'eluent_B_acetic', 'eluent_B_acetic_unit','eluent_B_trifluoroacetic', 'eluent_B_trifluoroacetic_unit','eluent_B_phosphor', 'eluent_B_phosphor_unit','eluent_B_nh4ac','eluent_B_nh4ac_unit', 'eluent_B_nh4form','eluent_B_nh4form_unit','eluent_B_nh4carb', 'eluent_B_nh4carb_unit','eluent_B_nh4bicarb','eluent_B_nh4bicarb_unit', 'eluent_B_nh4f','eluent_B_nh4f_unit','eluent_B_nh4oh', 'eluent_B_nh4oh_unit','eluent_B_trieth','eluent_B_trieth_unit', 'eluent_B_triprop','eluent_B_triprop_unit','eluent_B_tribut', 'eluent_B_tribut_unit','eluent_B_nndimethylhex', 'eluent_B_nndimethylhex_unit','eluent_B_medronic', 'eluent_B_medronic_unit', 'kPB', 'alpha_CH2', 'alpha_T_O', 'alpha_C_P', 'alpha_B_P', 'alpha_B_P1', 'particle_size', 'pore_size', 'H', 'S_star', 'A', 'B', 'C_pH_28)', 'C_pH_7)', 'EB_ret_factor']
```

# Usage
Sample data for generating 'RP specialist' and 'fused' models are found in the ```sample_data/``` folder and demonstrates the intended structure. RP specialist models have 64 attention heads, while fused models have 128.

The ```example/property_prediction/``` folder contains scripts and dataloaders to a) pre-train a model and b) finetune a pre-existing model. If you want to change the data source, you will need to edit code in the dataloader. Details for recommended hyperparameters are found in the Supplementary Information XXXXXXX.
