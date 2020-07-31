#!/usr/bin/env python3

import os
import sys
import hashlib
import time

from PIL import Image


def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128):
    h = hash_factory()
    with open(filename, "rb") as f: 
        while chunk := f.read(chunk_num_blocks*h.block_size): 
            h.update(chunk)
    return h.hexdigest()


workdir = os.getcwd()
start = time.time()

if len(sys.argv) > 1:
    exportdir = sys.argv[1]
else:
    exportdir = workdir

print("Searching for exported photos from Telegram chat export...")
print("Export path: " + exportdir)

photodir = os.path.join(exportdir, "photos")

if not os.path.exists(photodir):
    print("Could not find Telegram chat export data, check path and try again.")
    exit(1)

print("Deleting duplicate photos...")

checksums = []

for filename in os.listdir(photodir):
    path = os.path.join(photodir, filename)
    md5_hash = checksum(path)
    
    if md5_hash in checksums:
        os.remove(os.path.join(photodir, filename))
    else:
        checksums.append(md5_hash)

photos = []

for filename in sorted(os.listdir(photodir), key=str):
    if filename.endswith("_thumb.jpg"):
        os.remove(os.path.join(photodir, filename))
    else:
        photos.append(os.path.join(photodir, filename))

print(f"Found {len(photos)} exported photos to be converted to webp!")

imagedir = os.path.join(workdir, "images")
count = 1

for photo in photos:
    image = Image.open(photo)
    image = image.convert("RGB")
    image.save(os.path.join(imagedir, "{:04d}.webp".format(count)))
    
    os.remove(photo)
    count += 1

print(f"Done! Took {time.time() - start} ms")
