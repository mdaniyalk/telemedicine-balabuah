from fastembed import TextEmbedding


def get_embeddings(text):
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embeddings = list(model.embed([text]))
    return embeddings[0]
