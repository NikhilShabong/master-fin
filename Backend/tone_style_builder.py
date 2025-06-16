# tone_style_builder.py
from delta_utils import calculate_trait_deltas
from data_loader import load_tone_spec  # Your tone spec loader
TONE_SPEC = load_tone_spec()

# 1. Mapping from trait to high-level tone style bucket
BUCKET_MAP = {
    "OCEAN Neuroticism (Stress Reactivity)"           : ("calm",  +1),
    "PERMA Positive Emotion"                          : ("energise", +1),
    "Negative Affectivity (Type D)"                   : ("supportive", +1),
    "Mental Toughness (4Cs simplified)"               : ("challenging", +1),
    "OCEAN Conscientiousness (fitness-adapted)"       : ("formal", +1),
    "OCEAN Extraversion"                              : ("casual", +1),
    "SDT Competence"                                  : ("directive", +1),
    "OCEAN Openness (fitness-adapted)"                : ("exploratory", +1),
    # Add other traits here if you want finer-grained buckets
}

def build_tone_style(current_vec, future_vec):
    deltas = calculate_trait_deltas(current_vec, future_vec)
    bucket_best = {}

    for trait, meta in TONE_SPEC.items():
        bucket, _ = BUCKET_MAP.get(trait, (None, None))
        if not bucket: continue
        # MVP: decide high/low based on absolute delta ≥ 2
        status = 'low' if abs(deltas.get(trait, {}).get('delta', 0)) >= 2 else 'high'
        txt = meta.get(f"{status}_score_tone_strategy", {}).get('tone_prompt_text')
        score = abs(deltas.get(trait, {}).get('delta', 0))
        if txt and (bucket not in bucket_best or score > bucket_best[bucket][0]):
            bucket_best[bucket] = (score, txt)

    chosen_snippets = [v[1] for v in bucket_best.values() if v[1]]

    # Synthesize into a single paragraph using LLM (replace with your preferred LLM call if needed)
    from openai import OpenAI
    import os # Ensure os is imported
    prompt_sys  = ("You are a tone-compiler. Merge the following tone "
                   "instructions into at most 60 words, remove clashes, "
                   "return one paragraph only.")
    prompt_user = "\n".join(chosen_snippets)

    # Debugging: Print the API Key being used
    #print(f"OPENAI_API_KEY from os.getenv: {os.getenv('OPENAI_API_KEY')}")

    merged = OpenAI().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":prompt_sys},
                  {"role":"user"  ,"content":prompt_user}]
    ).choices[0].message.content.strip()

    return merged  # <- Save as user_profile['tone_style']
