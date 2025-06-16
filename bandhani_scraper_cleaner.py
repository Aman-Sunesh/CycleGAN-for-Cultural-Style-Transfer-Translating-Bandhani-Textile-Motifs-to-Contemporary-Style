from icrawler.builtin import GoogleImageCrawler
import os
from PIL import Image
import imagehash
from pathlib import Path

# 1. Create output folders
output_dir = Path("bandhani_dataset")
resized_dir = output_dir / "resized"
output_dir.mkdir(parents=True, exist_ok=True)
resized_dir.mkdir(exist_ok=True)

# 2. Download Bandhani images from Google using multiple keyword variants
keywords = [
    "Bandhani fabric pattern square -watermark",
    "Bandhani fabric pattern",
    "Bandhani textile red yellow",
    "Bandhani print close up",
    "Bandhani tie-dye fabric design",
    "Bandhej design no watermark",
    "background bandhani pattern"
]

crawler = GoogleImageCrawler(storage={'root_dir': str(output_dir)})
for keyword in keywords:
    crawler.crawl(
        keyword=keyword,
        filters={'type': 'photo'},
        max_num=1000  # Will try to download up to 1000 per keyword
    )

# 3. Remove near-duplicate or corrupt images
hashes = set()
for img_file in list(output_dir.glob("**/*.jpg")) + list(output_dir.glob("**/*.png")):
    try:
        img = Image.open(img_file).convert("RGB")
        h = imagehash.average_hash(img)
        if h in hashes:
            img_file.unlink()  # Remove duplicate
        else:
            hashes.add(h)
    except:
        img_file.unlink()  # Remove unreadable/corrupt images

# 4. Resize all images to 256x256 and save
for img_file in output_dir.glob("*.*"):
    if img_file.parent == resized_dir:
        continue  # Skip already resized files
    try:
        img = Image.open(img_file).convert("RGB")
        img = img.resize((256, 256), Image.ANTIALIAS)
        img.save(resized_dir / img_file.name)
    except:
        continue
