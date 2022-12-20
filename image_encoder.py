def encode_image(model, query):
    query_emb = model.encode([query], convert_to_tensor=True, show_progress_bar=False)

    return query_emb
