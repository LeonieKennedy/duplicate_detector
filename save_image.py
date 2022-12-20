import torch
import pickle

# Save hashes and tensors to memory
def add_tensor_to_dictionary(image_hash_perc, image_hash_MD5, tensor_values, saved_hashes, saved_tensors):
    # If first image
    if saved_tensors == []:
        saved_tensors = tensor_values
        saved_hashes = [{"MD5": image_hash_MD5, "perceptual_hash": image_hash_perc}]
    else:
        saved_tensors = torch.concat([saved_tensors, tensor_values])
        saved_hashes.append({"MD5": image_hash_MD5, "perceptual_hash": image_hash_perc})

    return saved_hashes, saved_tensors


# Save hashes and tensors to disk
def persist(saved_hashes, saved_tensors):
    torch.save(saved_tensors, './hashes_and_tensors/saved_tensors.pt')
    pickle.dump(saved_hashes, open('./hashes_and_tensors/saved_hashes.pkl', 'wb'))

# Load hashes and tensors from disk
def load_image_hash_and_tensors():
    # Load tensors and hashes
    saved_tensors = torch.load('./hashes_and_tensors/saved_tensors.pt')
    saved_hashes = pickle.load(open('./hashes_and_tensors/saved_hashes.pkl', 'rb'))

    return saved_hashes, saved_tensors
