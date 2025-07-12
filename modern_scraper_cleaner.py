from icrawler.builtin import BingImageCrawler
from pathlib import Path
from PIL import Image
import imagehash

# Create output folders
output_dir = Path("modern")
resized_dir = output_dir / "resized"
output_dir.mkdir(parents=True, exist_ok=True)
resized_dir.mkdir(exist_ok=True)

# Download Modern art images from Bing using multiple keyword variants
keywords = [
    "modern art painting",
    "abstract modern art",
    "contemporary art",
    "modern art gallery",
    "modern art background",
    "minimalist modern art",
    "modern art digital",
    "modern art texture",
    "modern art pattern",
    "modern art illustration",
    "modern art wallpaper",
    "modern art decor",
    "modern art canvas",
    "modern art print",
    "modern art design",
    "modern art photography",
    "modern art portrait",
    "modern art poster",
    "modern art vector",
    "modern art geometric",
    "modern art landscape",
    "modern art urban",
    "modern art pop art",
    "modern art colorful",
    "modern art black and white",
    "modern art graffiti",
    "modern art abstraction",
    "modern art square",
    "modern art minimal",
    "modern art spray paint",
    "modern art cubism",
    "modern art expressionism",
    "modern art surrealism",
    "modern art shapes",
    "modern art lines",
    "modern art dots",
    "modern art brush strokes",
    "modern art collage"
    "modern rock art"
    # …add more variants as needed
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
            max_num=1000,           # up to 1000 images per keyword
            file_idx_offset='auto'  # continue numbering across keywords
        )
    except Exception as e:
        print(f"[Warning] failed on keyword '{kw}': {e}")

# Deduplicate and remove corrupt images
hashes = set()
for img_file in list(output_dir.rglob("*.jpg")) + list(output_dir.rglob("*.png")):
    if resized_dir in img_file.parents:
        continue
    try:
        img = Image.open(img_file).convert("RGB")
        h = imagehash.average_hash(img)
        if h in hashes:
            img_file.unlink()
        else:
            hashes.add(h)
    except Exception:
        img_file.unlink()

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
        pass
