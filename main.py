from fastapi import FastAPI, UploadFile, Path
import shutil
from pathlib import Path

import save_image
from duplicate_detector import DetectionModel, Detection
from tempfile import NamedTemporaryFile
from typing import List
from datetime import datetime
from save_image import load_image_hash_and_tensors
import torch

PERSIST_IMAGE_MULTIPLE = 5  # Save tensors and hashes to disk every 100 images

app = FastAPI(
    title="Duplicate Image Detector",
    description="""
    Detects duplicate images
    
    search_file_hash - MD5 hash of the input file
    match_file_hash  - MD5 hash of the file input is matched to
    percentage       - Percentage similarity between images
    hamming_rate     - Custom rating based on the hamming distance calculated using perceptual hash     
                       HIGH = high chance images are the same - may have been resized, discoloured or blurred
                       MEDIUM = medium chance images are the same - may have been rotated
                       LOW = low chance that the images are the same
    """,
)
model = DetectionModel()

# Retrieve previously saved hashes and tensors
try:
    saved_hashes, saved_tensors = load_image_hash_and_tensors()

except FileNotFoundError:
    saved_hashes = []
    saved_tensors = []

count = 0
# Manually persist data to disk - should do this after you have uploaded all image files
@app.post("/persist", tags=["Persist image data"])
def persist():
    print("here")
    save_image.persist(saved_hashes, saved_tensors)
    return "Data saved"

# Detect duplicate images and return scores
@app.post("/detect_duplicate_images", response_model=List[Detection], tags=["Detect duplicate images"])
async def detect_duplicate_images(image_file: UploadFile, threshold: int) -> Detection:
    global saved_tensors, saved_hashes, count

    tmp_path = save_upload_file_tmp(image_file)
    saved_hashes, saved_tensors, result = model.api_detect(str(tmp_path), threshold, saved_hashes, saved_tensors)
    tmp_path.unlink()

    # Persist data every x images to disk
    count += 1
    if count % PERSIST_IMAGE_MULTIPLE == 0:
        print("persisting")
        persist()
    print(count, count % 5)
    return result


# create temp image file
def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()

    return tmp_path


