from image_encoder import *
from search_image import search
from sentence_transformers import SentenceTransformer
import os
import traceback
from pydantic import BaseModel
from imagehash import phash
import save_image
import hashlib
from PIL import Image


class Detection(BaseModel):
    search_file_hash: str
    match_file_hash: str
    percentage: str
    hamming_rate: str


class DetectionModel:
    def __init__(self):
        self._detection_model = SentenceTransformer('./model')    # open source pre-trained model

    def api_detect(self, image_file_path, threshold, saved_hashes, saved_tensors):
        # Check that search image path is real
        if not os.path.exists(image_file_path):
            return saved_hashes, saved_tensors, None

        try:
            # Get the hashes of the image you are searching for
            search_image = Image.open(image_file_path)
            search_file_perc = phash(search_image)                            # used to get the hamming distance
            search_file_md5 = hashlib.md5(search_image.tobytes()).hexdigest() # used to identify image

            # Get the tensor encoding of the image you are searching for
            query_emb = encode_image(self._detection_model, Image.open(image_file_path))

            # If this is the first image, save the tensors and hashes to memory straight away and return empty dict
            if saved_hashes == []:
                saved_hashes, saved_tensors = save_image.add_tensor_to_dictionary(search_file_perc, search_file_md5, query_emb, saved_hashes, saved_tensors)
                return saved_hashes, saved_tensors, []

            # Search the saved tensors to see if there is a duplicate of the search image
            results_dict = search(saved_hashes, saved_tensors, query_emb, threshold, search_file_perc, search_file_md5)

            # If it is not a duplicate, add the search tensor and hash to the list of saved tensors and hashes
            if results_dict == [] or results_dict[0]['percentage'] != 100:
                saved_hashes, saved_tensors = save_image.add_tensor_to_dictionary(search_file_perc, search_file_md5, query_emb, saved_hashes, saved_tensors)

        except:
            print("CAUGHT EXCEPTION 2: \n" + traceback.format_exc())
            return saved_hashes, saved_tensors, []

        return saved_hashes, saved_tensors, results_dict
