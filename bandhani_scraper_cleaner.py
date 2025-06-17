from icrawler.builtin import BingImageCrawler
from pathlib import Path
from PIL import Image
import imagehash

# Create output folders
output_dir = Path("bandhani_dataset")
resized_dir = output_dir / "resized"
output_dir.mkdir(parents=True, exist_ok=True)
resized_dir.mkdir(exist_ok=True)

# Download Bandhani images from Bing using multiple keyword variants
keywords = [
    "bandhani print",
    "bandhani fabric",
    "bandhani art",
    "bandhani royalty free",
    "bandhani background",
    # Add more as needed. I ran it on 40-50 other keywords
]

crawler = BingImageCrawler(
    feeder_threads=1,
    parser_threads=2,
    downloader_threads=4,
    storage={'root_dir': str(output_dir)}
)

for kw in keywords:
    try:
        crawler.crawl(
            keyword=kw,
            max_num=1000,       # download up to 1000 images per keyword
            file_idx_offset='auto'  # continue numbering across keywords
        )
    except Exception as e:
        print(f"[Warning] failed on keyword '{kw}': {e}")

# Remove near-duplicate or corrupt images
hashes = set()
for img_file in list(output_dir.rglob("*.jpg")) + list(output_dir.rglob("*.png")):
    if resized_dir in img_file.parents:
        continue
    try:
        img = Image.open(img_file).convert("RGB")
        h = imagehash.average_hash(img)
        if h in hashes:
            img_file.unlink()  # duplicate
        else:
            hashes.add(h)
    except Exception:
        img_file.unlink()  # corrupt or unreadable

# Resize all images to 256×256 and save into `resized/`
for img_file in output_dir.rglob("*.*"):
    if resized_dir in img_file.parents:
        continue
    if img_file.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
        continue
    try:
        img = Image.open(img_file).convert("RGB")
        img = img.resize((256, 256), Image.LANCZOS)
        img.save(resized_dir / img_file.name)
    except Exception:
        # skip any file that can't be opened or written
        pass
