from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os
from supabase_utils import fetch_cached_embedding, store_cached_embedding
#print("Current working directory:", os.getcwd())
#print("File exists?", os.path.isfile("Backend/Full_synonyms.json"))
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    cached = fetch_cached_embedding(text)
    if cached:
        return cached['embedding_vector']
    embedding = model.encode(text).tolist()
    store_cached_embedding(text, embedding)
    return embedding

# Paste your synonym dicts here or import them if in another file
import json
with open('Full_syn.json') as f:
    synonyms = json.load(f)
KPI_SYNONYMS = synonyms['KPI_SYNONYMS']
TRAIT_SYNONYMS = synonyms['TRAIT_SYNONYMS']



MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def build_embedding_dict(synonym_dict):
    """
    For each canonical name, build a list of embeddings for the canonical + all synonyms.
    Returns: {canonical_name: [emb_vec1, emb_vec2, ...]}
    """
    emb_dict = {}
    for canon, synonyms in synonym_dict.items():
        texts = [canon] + synonyms
        vectors = MODEL.encode(texts)
        emb_dict[canon] = vectors
    return emb_dict

KPI_EMBEDS = build_embedding_dict(KPI_SYNONYMS)
TRAIT_EMBEDS = build_embedding_dict(TRAIT_SYNONYMS)

def fuzzy_match_hybrid(user_input, emb_dict, thresh_full=0.84, thresh_partial=0.78):
    """
    Combines full sentence + keyword phrase matching.
    1. Run full sentence match (high precision).
    2. Split into bigrams + keywords; run fuzzy match on each (higher recall).
    3. Return all unique matches, sorted by max sim.
    """
    q_vec = get_embedding(user_input)
    hits = {}

    # 1. Full-sentence match
    for canon, vecs in emb_dict.items():
        sims = cosine_similarity([q_vec], vecs)
        max_sim = np.max(sims)
        if max_sim >= thresh_full:
            hits[canon] = max_sim

    # 2. Partial-phrase match (bigrams)
    import re
    words = re.findall(r"\b\w+\b", user_input.lower())
    phrases = words + [' '.join(words[i:i+2]) for i in range(len(words)-1)]

    for phrase in phrases:
        p_vec = get_embedding(phrase)
        for canon, vecs in emb_dict.items():
            sims = cosine_similarity([p_vec], vecs)
            max_sim = np.max(sims)
            if max_sim >= thresh_partial:
                hits[canon] = max(hits.get(canon, 0), max_sim)

    # Sort and return
    return [canon for canon, _ in sorted(hits.items(), key=lambda x: -x[1])]

# --- Test example ---
#if __name__ == "__main__":
#    print("KPI hit test:")
#    print(fuzzy_match_hybrid("I want to get a lean body and increase muscle growth and also increase self confidence", KPI_EMBEDS))
#    print("Trait hit test:")
#    print(fuzzy_match_hybrid("Sometimes I get too stressed and I can't bounce back", TRAIT_EMBEDS))

if __name__ == "__main__":
    print("Testing trait matcher for 'stick to habits':")
    print(fuzzy_match_hybrid("stick to habits", TRAIT_EMBEDS))


