from enum import Enum


class HammingRange(Enum):
    HIGH = 10
    MEDIUM = 35
    LOW = 64


# Calculate the hamming distance between the two images
#  - used to identify if the image might be a duplicate that has been blurred, resized, discoloured...
def get_hamming_distance(search_hash, match_hash):
    hamming_distance = search_hash - match_hash

    if hamming_distance <= HammingRange.HIGH.value:
        return HammingRange.HIGH.name
    elif hamming_distance <= HammingRange.MEDIUM.value:
        return HammingRange.MEDIUM.name
    else:
        return HammingRange.LOW.name

