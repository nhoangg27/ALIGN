<img width="5679" height="2871" alt="ALIGN_logo" src="https://github.com/user-attachments/assets/d82836d7-2458-4001-9415-8c02e38b3497" />


# **ALIGNing Learned Representations: Domain-General Models Triangulate Physicochemical Interactions in Analytical Separations**

# General
ALIGN is an extension to our previous work, Graphormer-RT, and the Graphormer package. The [documentation](https://graphormer.readthedocs.io/) and the original code on [Github](https://github.com/microsoft/Graphormer/) contain additional usage examples. If you use this code, **please cite our work that led to the development of this platform and the original Graphormer**.

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

## Via Docker 
We have developed a Docker Image to make installation and management of environments easier for Graphormer-RT. Installation instructions are as follows:

📦 How to Install and Run Graphormer-RT Using Docker Image

1. Install the following software (if not already installed):
- Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- NVIDIA GPU drivers: [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)
- NVIDIA Container Toolkit: [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

You can verify installation via the following commands:
```bash
docker --version
```
```bash
nvidia-smi
```
```bash
nvidia-container-cli --version
```

2. Save the Dockerfile (the name should be “Dockerfile”).
3. Open a terminal in the same folder as Dockerfile.
4. Build the Docker image by running:
```bash
docker build --no-cache -t graphormer-rt .
```
5. Run the Docker container with GPU support:
```bash
docker run -it --gpus all graphormer-rt bash
```
6. Inside the container, navigate to the example directory, make the example script executable, and run the example script:
```bash
cd /workspace/Graphormer-RT/examples/property_prediction
chmod +x HILIC.sh  
./HILIC.sh
```
7. If it runs for an epoch and saves .pt files, you know you’ve succeeded.

A beginner's guide to Docker usage can be found [HERE](https://docker-curriculum.com/).
- To UPLOAD files (_e.g._, new data) to the docker container, use:
```bash
docker cp ./local_file.txt container_id:/app/local_file.txt
```
- To DOWNLOAD files (_e.g._, checkpoints, results) from this container, use:
```bash
docker cp <container_id>:<path_inside_container> <path_on_host>
```

## Via VS Code Dev Containers
Alternatively, to make it easier to edit and organize files, you can also install ALIGN using the **Dev Containers extension** in VS Code with GPU support.

### 🧰 Prerequisites

- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Visual Studio Code (VS Code)](https://code.visualstudio.com/)
- [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Access to a machine with [**NVIDIA GPU**](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) and [drivers](https://www.nvidia.com/Download/index.aspx) properly installed.

### 📁 Folder Structure

Your main project folder (e.g. `ALIGN/`) should look like this:

<pre lang="markdown"> <code> ALIGN/ 
  ├── .devcontainer/        ← Option 1 or Option 2 (see below)
  │ ├── devcontainer.json    
  │ ├── Dockerfile 
  │ └── setup.sh       
  ├── ALIGN_repo/           ← Your project code (from GitHub or manual download) 
  ├── ALIGN_Weights/         </code> </pre>

### 🚀 Setup Steps

#### 1. Clone or download this repository

You may choose to **download** and extract the repository manually. Place it inside `ALIGN/` (here named `ALIGN_repo/`) for local mounting when we build the docker container.

Alternatively, you may also choose to **clone** it automatically via `git clone`.

#### 2. Prepare the `.devcontainer` folder

Please note that installation steps slightly differ depending on whether you're cloning from GitHub or mounting the repo locally. Use the files in `git_clone_installation/` or `local_mount_installation/` accordingly. Create a `.devcontainer/` folder inside the big `ALIGN/` directory with the following files:
- `devcontainer.json` 
- `Dockerfile`
- `setup.sh`
  
#### 3. Prepare model weights

Download our model weights from XXXX and place them in an `ALIGN_Weights/` folder inside `ALIGN/`. If everything is installed correctly, there would be a bind mount for the weights to the container under `/workspaces/align/model_weights/`.

#### 4. Open in VS Code

1. Open VS Code.
2. Install the **Dev Containers extension** if you haven't already.
3. Open the `ALIGN/` folder in a **new VS Code window**.
4. Press `F1` and select:  
   ➜ `Dev Containers: Rebuild Container without Cache and Reopen in Container`

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

The pickle file (```/home/nhi/A-RT/A-RT_fused/sample_data/all_col_metadata_20260512.pickle```) contain processed column metada generated from RepoRT with the following headers, some of which (_e.g.,_ void volume or HSMB/Tanaka parameters) are calculated directly using RepoRT scripts:
```python
['company_name', 'usp_code', 'col_length', 'col_innerdiam', 'col_part_size', 'temp', 'col_fl', 'col_dead', 'HPLC_type','A_solv', 'B_solv', 'time1', 'grad1', 'time2', 'grad2', 'time3', 'grad3', 'time4', 'grad4', 'A_pH', 'B_pH', 'A_start', 'A_end', 'B_start', 'B_end',  'eluent_A_formic', 'eluent_A_formic_unit', 'eluent_A_acetic', 'eluent_A_acetic_unit','eluent_A_trifluoroacetic', 'eluent_A_trifluoroacetic_unit','eluent_A_phosphor', 'eluent_A_phosphor_unit','eluent_A_nh4ac','eluent_A_nh4ac_unit', 'eluent_A_nh4form','eluent_A_nh4form_unit','eluent_A_nh4carb', 'eluent_A_nh4carb_unit','eluent_A_nh4bicarb','eluent_A_nh4bicarb_unit', 'eluent_A_nh4f','eluent_A_nh4f_unit','eluent_A_nh4oh', 'eluent_A_nh4oh_unit','eluent_A_trieth','eluent_A_trieth_unit','eluent_A_triprop','eluent_A_triprop_unit','eluent_A_tribut', 'eluent_A_tribut_unit','eluent_A_nndimethylhex', 'eluent_A_nndimethylhex_unit','eluent_A_medronic', 'eluent_A_medronic_unit','eluent_B_formic', 'eluent_B_formic_unit', 'eluent_B_acetic', 'eluent_B_acetic_unit','eluent_B_trifluoroacetic', 'eluent_B_trifluoroacetic_unit','eluent_B_phosphor', 'eluent_B_phosphor_unit','eluent_B_nh4ac','eluent_B_nh4ac_unit', 'eluent_B_nh4form','eluent_B_nh4form_unit','eluent_B_nh4carb', 'eluent_B_nh4carb_unit','eluent_B_nh4bicarb','eluent_B_nh4bicarb_unit', 'eluent_B_nh4f','eluent_B_nh4f_unit','eluent_B_nh4oh', 'eluent_B_nh4oh_unit','eluent_B_trieth','eluent_B_trieth_unit', 'eluent_B_triprop','eluent_B_triprop_unit','eluent_B_tribut', 'eluent_B_tribut_unit','eluent_B_nndimethylhex', 'eluent_B_nndimethylhex_unit','eluent_B_medronic', 'eluent_B_medronic_unit', 'kPB', 'alpha_CH2', 'alpha_T_O', 'alpha_C_P', 'alpha_B_P', 'alpha_B_P1', 'particle_size', 'pore_size', 'H', 'S_star', 'A', 'B', 'C_pH_28)', 'C_pH_7)', 'EB_ret_factor']
```

# Usage
Sample data for generating 'RP specialist' and 'fused' models are found in the ```sample_data/``` folder and demonstrates the intended structure. RP specialist models have 64 attention heads, while fused models have 128.

The ```example/property_prediction/``` folder contains scripts and dataloaders to a) pre-train a model and b) finetune a pre-existing model. If you want to change the data source, you will need to edit code in the dataloader. Details for recommended hyperparameters are found in the Supplementary Information XXXXXXX.

To fully pre-train a model, use the following script. Adjust ```--encoder-attention-heads``` to 64 for an RP specialist model and 128 for a fused model:
```bash
bash ../../examples/property_prediction/fused.sh
```

To finetune a model, use the following script. Ensure that you have the correct paths for ```--pretrained-model-name``` and ```--finetune_from_model```:
```bash
bash ../../examples/property_prediction/finetune_RP.sh
```

Models can then be evaluated using the corresponding scripts in ```graphormer/evaluate/```. The flag ```--save-dir``` will allow you to save predictions alongside method data and SMILES strings:
```bash
bash ../../graphormer/evaluate_RP.sh
```

Pre-graph encoders are found in ```graphormer/modules/graphormer_layers.py```. Graph layers and MLPs are found in ```graphormer/models/```.

There are command line tools available for freezing layers of the graph encoder of MLP (see ```--freeze-level```). A negative freeze-level will freeze layers of the graph encoder starting from the front (-4 freezes the first 4 layers of the graph encoder). A positive freeze level will freeze layers in the MLP starting from the front (2 will freeze the first two layers of the MLP). There are additional flags for freezing the atomic feature encoders and graph feature encoders.

# Models

Sample RP and HILIC models that were pretrained for our study are freely available online at XXXXXXX. These can be used for model evaluation or for finetuning using the requisite scripts. 

# Common Errors

"Segmentation Fault... Core Dumped" may indicate that you have installed the incorrect version of [PyTorch Geometric](https://data.pyg.org/whl/). This can be further tested by checking the package import (_e.g._, ```from pytorch_geometric.data import data```)

If gradients explode in training, it is recommended that you lower learning rates or increase the ```fp16-scale-tolerance``` value in the bash script

# Contact

If you require further assistance with developing your own model or have any questions about its implementaton, the authors can be contacted at 

- cmkstien@uwaterloo.ca
- scott.hopkins@uwaterloo.ca 

