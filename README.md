<p align="center">
  <img src="ALIGN_logo_final.png" alt="ALIGN Logo" width="75%">
</p>


# **ALIGNing Learned Representations: Domain-General Models Triangulate Physicochemical Interactions in Analytical Separations**

# General
ALIGN is an extension of our previous work, Graphormer-RT, and the Graphormer package. The [documentation](https://graphormer.readthedocs.io/) and the original code on [Github](https://github.com/microsoft/Graphormer/) contain additional usage examples. If you use this code, **please cite our work that led to the development of this platform and the original Graphormer**.

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
To take the headache out of environment management, we’ve provided a pre-configured Docker Image for ALIGN. We recommend using **VS Code Dev Containers**; it gives you a full graphical interface to interact with the containerized code and files just like a local project, all while maintaining full GPU support. For more details, you can consult the documentations on [Docker](https://docker-curriculum.com/) and [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers). 

## 🧰 Prerequisites
To install and run ALIGN, you will need the following:
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Visual Studio Code (VS Code)](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Access to a machine with [NVIDIA GPU](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) and [drivers](https://www.nvidia.com/Download/index.aspx) properly installed

You can verify Docker and NVIDIA installation on **GPU** via the following commands:

```bash
docker --version
```
```bash
nvidia-smi
```
```bash
nvidia-container-cli --version
```

Since Dev Containers allow you to drag-and-drop or edit files directly through the VS Code sidebar, you won't need the command line for most tasks. However, if you ever need to quickly move data or results via the terminal, you can use these "just in case" commands:
- To find your active `<container_id>` after building the container:
```bash
docker ps
```
- To **UPLOAD** files (_e.g._, new data) to the docker container:
```bash
docker cp <path_to_local_file> <container_id>:<destination_directory_inside_container>
```
- To **DOWNLOAD** files (_e.g._, checkpoints, results) from this container, use:
```bash
docker cp <container_id>:<path_inside_container> <path_on_host>
```

## 📁 Folder Structure

Your main project folder (e.g. `ALIGN/`) should look like this

- If you **clone** directly from GitHub:

<pre lang="markdown"> <code> ALIGN/ 
  ├── .devcontainer/        ← From 'git_clone_installation' (see Setup Step 2)
  │ ├── devcontainer.json    
  │ ├── Dockerfile       
  ├── ALIGN_Weights/         (see Setup Step 3)  </code> </pre>

- If you **download** the repository and manually mount it to the docker container from your local machine:

<pre lang="markdown"> <code> ALIGN/ 
  ├── .devcontainer/        ← From 'local_mount_installation' (see Setup Step 2)
  │ ├── devcontainer.json    
  │ ├── Dockerfile 
  │ └── setup.sh      
  ├── ALIGN-main/
  ├── ALIGN_Weights/         (see Setup Step 3)  </code> </pre>

## 🚀 Setup Steps

### 1. Clone or download this repository

You may choose to **clone** the repository automatically from GitHub via `git clone`. 

Alternatively, you may also choose to **download** and extract the repository manually. If this is the case, place it inside `ALIGN/` for local mounting (here named `ALIGN-main/`) when we build the docker container.

### 2. Prepare the `.devcontainer` folder

Please note that installation steps slightly differ depending on whether you're cloning from GitHub or mounting the repository locally. Use the configuration files in `git_clone_installation/` or `local_mount_installation/` accordingly. Create a `.devcontainer/` folder inside the big `ALIGN/` directory with the following files:
- `devcontainer.json` 
- `Dockerfile`
- `setup.sh` (only if you're mounting from a local download)
  
### 3. Prepare model weights

Sample RP and fused models that were pretrained for our study are freely available online at XXXXXXX. These can be used for model evaluation or for finetuning using the requisite scripts. Download our model weights and place them in an `ALIGN_Weights/` folder inside `ALIGN/`. If everything is installed correctly, there would be a bind mount for the weights to the container under `/workspace/align/model_weights/`.

### 4. Build container

1. In VS Code, install the **Dev Containers extension** if you haven't already.
3. Open the `ALIGN/` folder in a **new window**.
4. Press `F1` and select
   
   ➜ `Dev Containers: Reopen in Container`

   ***NOTE:*** if the environment is broken or if you simply want to rebuild to the latest version, select

   ➜ `Dev Containers: Rebuild Container without Cache and Reopen in Container`
   
6. Once the container finishes building, run `bash setup.sh` to finish setting up the environment (if mounting locally). You may skip this step if you are cloning the repository.
7. To test whether the installation is working properly, navigate to the example directory and execute:
   
   ```bash
   cd examples/property_prediction
   bash RP.sh
   ```
   
8. If it runs for an epoch and saves `.pt` files inside `checkpoints_RP/`, you know you’ve succeeded.

# Usage

## 🔍 Overview
The repository is structured into distinct functional modules for data processing, training, and evaluation:
- `examples/property_prediction/`: contains the primary scripts and data loaders for pre-training and fine-tuning models
- `graphormer/evaluate/`: contains specialized scripts and data loaders for model evaluation
- `sample_data/`: includes template datasets in `.csv` format

The pipeline automatically infers the data source based on the executed script name. To run the pipeline with a custom dataset, update the data pathways directly within the relevant data loader:
1. Navigate to the targeted chromatography mode folder `*_loader` (_e.g._, CCS, RP) in either `examples/property_prediction/` or `graphormer/evaluate/`.
2. Open `*_loader_train.py` and update the `DATA_PATH` variable to point to your data file.

## 🛠️ Hyperparameters & Configuration Flags
Model training and evaluation are executed via bash scripts (`.sh`). For a complete discussion on recommended hyperparameter configurations, refer to Supplementary Note 6 in the Supplementary Information.

Key command-line arguments include:
- `--user-data-dir` and `--dataset-name`: point to the corresponding dataloader and dataset registered in `*_loader_train.py`
- `--encoder-attention-heads`: adjust to 64 for an RP specialist model and 128 for a fused model
- `--pretrained-model-name` and `--finetune_from_model`: paths to model weights
- `--save-dir`: saves the best performing epoch (optimized on MAE) and the last epoch checkpoint to the specified directory as `checkpoint_best.pt` and `checkpoint_last.pt`, respectively
- `--save-path`: saves predictions alongside method data, SMILES strings, and uncertainty values as `.csv` files when evaluating models

## ❄️ Freezing Layers
The `--freeze-level` argument operates on the graph encoder and multi-layer perceptron (MLP) blocks. 
- **Negative freeze-level**: freeze layers of the _graph encoder_ starting from the front (_e.g._, `-4` freezes the first 4 layers)
- **Positive freeze level**: freeze layers of the _MLP_ starting from the front (_e.g._, `2` freezes the first two layers of the MLP)

Additional flags are available for independently freezing the atomic feature encoders and graph feature encoders.

## 🤖 Execution Scripts

### 🏗️ Pretraining
To fully pretrain a model from scratch:

```bash
cd examples/property_prediction
bash pretrain_RP.sh  # alternative: pretrain_fused.sh
```

### 🎯 Finetuning
To finetune a pre-existing model on a specific chromatographic mode:

```bash
cd examples/property_prediction
bash RP.sh  # alternatives: CCS.sh, DMS.sh, GC.sh, fused.sh
```

### 📊 Evaluation
To evaluate trained checkpoints, utilize the corresponding evaluation scripts located in the model evaluation directory:

```bash
cd graphormer/evaluate
bash evaluate_RP.sh  # alternatives: evaluate_CCS.sh, evaluate_DMS.sh, evaluate_GC.sh, evaluate_fused.sh
```

## 🧠 Model Architecture
For users looking to modify underlying model layers, the core components are located at:
- Pre-graph (chromatographic and atom feature) encoders: `graphormer/modules/graphormer_layers.py`
- Graph layers and MLPs: `graphormer/models/`

# Data and Chromatographic Gradients
All in-house benchmarking datasets in this study are publically available at **INSERT ZENODO LINK WHEN AVAILABLE**.

All data used to pretrain the RP specialist and fused ALIGN models are publically available at the [RepoRT GitHub](https://github.com/michaelwitting/RepoRT/). Those using these data should cite this work as follows:

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

The visualization below illustrates how the model interprets chromatographic gradients. Red dots indicate experimental retention times, while green markers identify gradient inflection points. Additional column parameters, derived using the RepoRT workflow, are also shown.

The void volume ($t_0$), for instance, is determined by:

$$t_0 = \frac{0.0005 \cdot l \cdot ID^2}{fl}$$

where $l$ is the column length (mm), $ID$ is the column inner diameter (mm), and $fl$ is the flow rate (mL/min).

<p align="center">
  <img src="GradientFormalisms.png" alt="Gradient Info" width="75%">
</p>

To support downstream finetuning, we have provided a utility script (`scripts/update_method_dictionary.py`) to append new gradients to our method dictionary (`sample_data/all_col_metadata_20260512.pickle`). This file includes consolidated column metadata, including RepoRT-calculated metrics like $t_0$ and HSMB/Tanaka parameters, structured with the following headers:

```python
['company_name', 'usp_code', 'col_length', 'col_innerdiam', 'col_part_size', 'temp', 'col_fl', 'col_dead', 'HPLC_type','A_solv', 'B_solv', 'time1', 'grad1', 'time2', 'grad2', 'time3', 'grad3', 'time4', 'grad4', 'A_pH', 'B_pH', 'A_start', 'A_end', 'B_start', 'B_end',  'eluent_A_formic', 'eluent_A_formic_unit', 'eluent_A_acetic', 'eluent_A_acetic_unit','eluent_A_trifluoroacetic', 'eluent_A_trifluoroacetic_unit','eluent_A_phosphor', 'eluent_A_phosphor_unit','eluent_A_nh4ac','eluent_A_nh4ac_unit', 'eluent_A_nh4form','eluent_A_nh4form_unit','eluent_A_nh4carb', 'eluent_A_nh4carb_unit','eluent_A_nh4bicarb','eluent_A_nh4bicarb_unit', 'eluent_A_nh4f','eluent_A_nh4f_unit','eluent_A_nh4oh', 'eluent_A_nh4oh_unit','eluent_A_trieth','eluent_A_trieth_unit','eluent_A_triprop','eluent_A_triprop_unit','eluent_A_tribut', 'eluent_A_tribut_unit','eluent_A_nndimethylhex', 'eluent_A_nndimethylhex_unit','eluent_A_medronic', 'eluent_A_medronic_unit','eluent_B_formic', 'eluent_B_formic_unit', 'eluent_B_acetic', 'eluent_B_acetic_unit','eluent_B_trifluoroacetic', 'eluent_B_trifluoroacetic_unit','eluent_B_phosphor', 'eluent_B_phosphor_unit','eluent_B_nh4ac','eluent_B_nh4ac_unit', 'eluent_B_nh4form','eluent_B_nh4form_unit','eluent_B_nh4carb', 'eluent_B_nh4carb_unit','eluent_B_nh4bicarb','eluent_B_nh4bicarb_unit', 'eluent_B_nh4f','eluent_B_nh4f_unit','eluent_B_nh4oh', 'eluent_B_nh4oh_unit','eluent_B_trieth','eluent_B_trieth_unit', 'eluent_B_triprop','eluent_B_triprop_unit','eluent_B_tribut', 'eluent_B_tribut_unit','eluent_B_nndimethylhex', 'eluent_B_nndimethylhex_unit','eluent_B_medronic', 'eluent_B_medronic_unit', 'kPB', 'alpha_CH2', 'alpha_T_O', 'alpha_C_P', 'alpha_B_P', 'alpha_B_P1', 'particle_size', 'pore_size', 'H', 'S_star', 'A', 'B', 'C_pH_28)', 'C_pH_7)', 'EB_ret_factor']
```

# Common Errors

"Segmentation Fault... Core Dumped" may indicate that you have installed the incorrect version of [PyTorch Geometric](https://data.pyg.org/whl/). This can be further tested by checking the package import (_e.g._, `from pytorch_geometric.data import data`)

If gradients explode in training, it is recommended that you lower learning rates or increase the `fp16-scale-tolerance` value in the bash script

# Contact

If you require further assistance with developing your own model or have any questions about its implementaton, the authors can be contacted at 

- cmkstien@uwaterloo.ca
- scott.hopkins@uwaterloo.ca

# License

ALIGN is licensed under the GNU General Public License v3.0. See the `LICENSE` file for the full license text and `LICENSE_NOTICE.md` for a project-specific summary.

If you use ALIGN in academic work, please cite the publications listed above.

