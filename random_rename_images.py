import os
import random
from pathlib import Path

# Code to randomly rename all the images in your folder to a uniform naming format -> img1.jpg, img2.jpg, ......

def random_rename_images(folder_path):
    folder = Path(folder_path)
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # Gather all image files
    imgs = [p for p in folder.iterdir() if p.suffix.lower() in exts and p.is_file()]
    random.shuffle(imgs)

    # Move each to a unique temp name in the same folder
    tmp_paths = []
    for i, old in enumerate(imgs):
        tmp_name = f"__tmp__{i}{old.suffix.lower()}"
        tmp = folder / tmp_name
        old.rename(tmp)
        tmp_paths.append(tmp)

    # Rename temps to final img1…imgN
    for idx, tmp in enumerate(tmp_paths, start=1):
        final_name = f"img{idx}{tmp.suffix.lower()}"
        final = folder / final_name
        tmp.rename(final)

    print(f"Successfully renamed {len(tmp_paths)} images in {folder!r}")

if __name__ == "__main__":
    folder_to_rename = r"C:\Users\asust\Downloads\Modern"  # <-- put the path to your folder here
    random_rename_images(folder_to_rename)



