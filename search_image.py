from sentence_transformers import util
from hamming_distance import get_hamming_distance

# Retrieve scores for duplicate images
def search(img_hashes, img_emb, query_emb, threshold, search_file_perc, search_file_md5):
    results_dict = []
    # Get the top k results: currently set to 10
    hits = util.semantic_search(query_emb, img_emb, top_k=10)[0]

    # For each hit, add it to a list of dictionaries
    for hit in hits:
        match_file_perc = img_hashes[hit['corpus_id']]["perceptual_hash"]
        score = (hit['score']*100)

        # Only return results above threshold percentage e.g. 80
        if score >= threshold:
            results_dict.append({
                "search_file_hash": str(search_file_md5),
                "match_file_hash": str(img_hashes[hit['corpus_id']]["MD5"]),
                "percentage": round(score, 4),
                "hamming_rate": get_hamming_distance(search_file_perc, match_file_perc),
            })

    return results_dict
