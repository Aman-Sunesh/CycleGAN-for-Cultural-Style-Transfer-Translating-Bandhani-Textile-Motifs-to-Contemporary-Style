# GANDhani: CycleGAN for Cultural Style Transfer

## Overview

GANDhani is a CycleGAN-based project to translate traditional Bandhani textile motifs into contemporary modern-art–style patterns, and vice versa. Using unpaired image-to-image translation, the model learns two mappings:

- **A → B**: Bandhani → Modern Art  
- **B → A**: Modern Art → Bandhani

This repo includes:

- **Data collection & preprocessing** scripts to scrape, deduplicate, resize, and rename images.  
- **CycleGAN implementation** (Discriminator, Generator, training loop) in PyTorch.  
- **Jupyter notebooks** for exploratory data visualization and model training.  
- **Gradio app** for interactive inference.

## Directory Structure

```bash
├── bandhani_scraper_cleaner.py     # Scrape & clean Bandhani images
├── modern_scraper_cleaner.py       # Scrape & clean Modern Art images
├── random_rename_images.py         # Uniformly rename images in a folder
├── data/                           # Local datasets (train/val splits)
│   ├── train/
│   │   ├── bandhani/
│   │   └── modern/
│   └── val/
│       ├── bandhani/
│       └── modern/
├── notebooks/
│   └── GANDhani_CycleGAN.ipynb     # Full training & evaluation pipeline
├── models/                         # Saved model checkpoints
├── generated/                      # A2B & B2A sample images
├── scripts/                        # Helper scripts & utilities
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Prerequisites

- Python 3.8+  
- CUDA 10.2+/cuDNN (for GPU training) or CPU-only  
- Kaggle API credentials (for downloading curated datasets)

Install the required packages:

```bash
pip install -r requirements.txt
```

## Data Collection & Preprocessing

- **Scrape Bandhani images:**
  ```bash
  python bandhani_scraper_cleaner.py
  ```

  - Downloads up to 1000 images per keyword variant.
  - Removes near-duplicates via perceptual hashing. 
  - Resizes all images to 256×256.

- **Scrape Modern Art images:**

  ```bash
  python modern_scraper_cleaner.py
  ```
    
  - Downloads up to 1000 images per keyword variant.
  - Removes near-duplicates via perceptual hashing. 
  - Resizes all images to 256×256.

- **Rename images (optional):**

  ```bash
  python random_rename_images.py /path/to/your/folder
  ```

- **Alternative:** Use Curated Kaggle Datasets Uploaded on Kaggle.
  - If you'd rather skip scraping, you can use pre-cleaned datasets I published on Kaggle:
  
  - - **Bandhani Dataset**: [https://www.kaggle.com/datasets/amansunesh/bandhani-design-dataset](https://www.kaggle.com/datasets/amansunesh/bandhani-design-dataset)  
  - **Modern Art Dataset**: [https://www.kaggle.com/datasets/amansunesh/modern-art-dataset](https://www.kaggle.com/datasets/amansunesh/modern-art-dataset)

These datasets are already deduplicated, resized to 256×256, and split into `train/` and `val/`.

#### Set up your Kaggle API credentials:

1. Go to [https://www.kaggle.com/account](https://www.kaggle.com/account)
2. Create a new API token.
3. Place the downloaded `kaggle.json` in your local machine at:

  ```bash
   ~/.kaggle/kaggle.json
  ```

4. Download the modern dataset using kagglehub

```python
import kagglehub

# Download the latest version
path = kagglehub.dataset_download("amansunesh/modern-art-dataset")

print("Path to dataset files:", path)
```

5. Repeat the same for the Bandhani dataset by changing the dataset slug:

```python
path = kagglehub.dataset_download("amansunesh/bandhani-design-dataset")
```

## Training the CycleGAN


- **Launch the notebook**:
  ```bash
  jupyter notebook notebooks/GANDhani_CycleGAN.ipynb
  ```

  - Walks through data transforms, model definitions, and training loop.
  - If you open the notebook, you'll also see my fully trained model with sample images showing both Bandhani → Modern and Modern → Bandhani conversions. The notebook file is large, so you may need to download it locally to view the outputs properly.

- **Training Parameters**:
  - `epochs`: up to **200–300**
  - `batch_size`: **1** (default)
  - **Optimizers**:  
    `Adam` with learning rate `2e-4` and betas `(0.5, 0.999)`
  - **Losses**:  
    - LSGAN (MSE)  
    - L1 cycle-consistency loss (λ = 10)  
    - Identity loss (λ_id = 0.5)
  - **Replay buffer** of size **50** for discriminators
  - **Learning rate scheduler**:  
    Linearly decays the learning rate after half the epochs

- **Monitoring**: Generated samples saved every epoch under generated/A2B_epoch###.png and generated/B2A_epoch###.png.

- **Checkpoints**:
  - Generator and discriminator weights saved every 5 epochs in models/.
  - To resume training, load state dicts and continue the loop.


## Inference & Interactive Demo

After training (e.g., epoch 200), load your generators:

```python
from your_module import Generator, denorm
gen_A2B = Generator().to(device)
gen_B2A = Generator().to(device)

gen_A2B.load_state_dict(torch.load('models/gen_A2B_epoch200.pth'))
gen_B2A.load_state_dict(torch.load('models/gen_B2A_epoch200.pth'))
```

### Scripted Inference
Use helper functions in the notebook:

```python
convert_to_modern('data/val/bandhani/img15.jpg')   # Bandhani → Modern
convert_to_bandhani('data/val/modern/img107.jpg')  # Modern → Bandhani
```

### Gradio Web App
Launch an interactive demo:

```bash
python app.py  # or `python notebooks/GANDhani_CycleGAN.ipynb` contains demo code
```

Open the provided URL or public share link to upload your own images.


## Tips & Troubleshooting
- **Unstable losses**? Try lowering the learning rate to 1e-4 or adding a history buffer for the discriminator.
- **Mode collapse**? Increase cycle weight (λ_cycle) or add stronger identity loss.
- **Artifacts**? Check your data balance and augmentations. Ensure both domains have sufficient variety.
