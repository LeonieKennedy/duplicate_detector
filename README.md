# Duplicate Image Detector

---
## Files
- model/
  - Contains pre-downloaded and trained model
- .dockerignore
- docker-compose.yml
- Dockerfile
- duplicate_detector.py
  - Receives image file path and threshold from user and returns results
- hamming_distance.py
  - Receives perceptual hashes of search and match images, calculates hamming distance and returns rating
- image_encoder.py
  - Receives the model and search image, and returns the tensor
- main.py
  - FastAPI stuff
- README.md
- requirements.txt
- save_image.py
  - Saves and loads the image hashes and tensors to/from disk and memory
- search_image.py
  - Receives hashes, tensors and threshold, and returns results dictionary
---
## How to run
Build the docker image:

    sudo docker build -t duplicate_detector_persist:latest . 


Start the container:

    sudo docker-compose up


Go to url:

http://0.0.0.0:8000/docs#/

---
## Output
search_file_hash: 
- MD5 hash of the input file

match_file_hash : 
- MD5 hash of the file input is matched to

percentage:
- Percentage similarity between images

hamming_rate:
- Custom rating based on the hamming distance calculated using perceptual hash
  - HIGH = high chance images are the same 
    - may have been resized, discoloured or blurred
  - MEDIUM = medium chance images are the same 
    - may have been rotated
  - LOW = low chance that the images are the same
