from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Paste your synonym dicts here or import them if in another file
KPI_SYNONYMS = {
    "KPI 1 (Body Positivity)": ["body image", "self-body love", "positive body outlook", "body confidence"],
    "KPI 2 (Self-Esteem Enhancement)": ["confidence boost", "feeling worthy", "self-respect", "self-worth", "self-confidence"],
    "KPI 3 (Stress Reduction)": ["less stress", "manage anxiety", "feeling calmer", "stress relief"],
    "KPI 4 (Mood Improvement)": ["better mood", "emotional uplift", "feeling happier", "emotional balance"],
    "KPI 5 (Increased Energy Levels)": ["more energy", "boosted energy", "feeling energetic", "higher vitality"],
    "KPI 6 (Improved Sleep Quality)": ["sleep better","better sleep", "deeper rest", "quality sleep", "restful nights"],
    "KPI 7 (Enhanced Cognitive Function)": ["mental clarity", "focus", "brain performance", "thinking better"],
    "KPI 8 (Sense of Accomplishment)": ["achieving goals", "getting things done", "feeling proud", "daily success"],
    "KPI 9 (Autonomy in Health Management)": ["self-directed health", "independent fitness", "own health choices", "personal health control"],
    "KPI 10 (Social Connectedness)": ["social bonds", "being around others", "relationship depth", "feeling included"],
    "KPI 11 (Body Fat Percentage)": ["fat loss", "lean body", "fat reduction", "shredding"],
    "KPI 12 (Muscle Mass Gain)": ["muscle growth", "bulking", "building muscle", "muscle increase", "muscle mass"],
    "KPI 13 (Weight Management)": ["weight loss", "maintain weight", "cutting or bulking", "weight control"],
    "KPI 14 (Strength Benchmarks)": ["1 rep max", "strength increase", "lift more", "power goal"],
    "KPI 15 (Cardiovascular Endurance)": ["heart health", "aerobic fitness", "run longer", "stamina"],
    "KPI 16 (Sport Enhancement - Flexibility & Mobility)": ["looser body", "joint flexibility", "increased mobility", "yoga performance"],
    "KPI 17 (Sport Enhancement – Balance & Coordination)": ["better balance", "movement control", "agility", "spatial coordination"],
    "KPI 18 (Sport Enhancement – Speed & Agility)": ["move faster", "quick footwork", "explosive speed", "sport quickness"]
}

TRAIT_SYNONYMS = {
    "Sleep": ["rest", "bedtime", "recovery", "quality sleep", "sleep better"],
    "Nutrition": ["diet", "eating habits", "food choices", "balanced meals"],
    "Lingering Pain": ["chronic pain", "body aches", "soreness", "nagging pain"],
    "Exercise Enjoyment (Affective Attitude – during workout)": ["enjoy workout", "fun while training", "pleasure in exercise"],
    "Exercise Enjoyment (Affective Attitude – after workout)": ["post-workout feeling", "after gym satisfaction", "good after exercise"],
    "Exercise Intensity Preference": ["like tough workouts", "intensity craving", "prefer light workouts"],
    "Exercise Intensity Tolerance": ["push through pain", "handle intensity", "workout pain resistance"],

    "Weather Impacts": ["weather effect", "mood vs climate", "weather motivation", "climate impact"],
    "Chronotype (Morningness–Eveningness)": ["morning person", "evening energy", "day rhythm", "energy peak time"],

    "OCEAN Extraversion": ["motivated by people", "extroverted in workouts", "group-driven"],
    "OCEAN Agreeableness": ["empathetic", "get along", "cooperative", "friendly nature"],
    "Social Exercise Orientation (Group-oriented vs Independent)": ["workout with others", "group vs solo", "training preference"],

    "OCEAN Neuroticism (Stress Reactivity)": ["emotional reactivity", "anxious", "easily stressed", "emotionally intense"],
    "PERMA Positive Emotion": ["joy", "hope", "daily happiness", "optimism"],
    "PERMA Accomplishment": ["achievement", "goal completion", "productive feeling"],
    "Negative Affectivity (Type D)": ["pessimism", "low mood", "feeling down", "emotional weight"],
    "Social Inhibition (Type D)": ["shy", "hesitant socially", "avoid strangers", "introverted discomfort"],

    "OCEAN Openness (fitness-adapted)": ["curious workouts", "experimenting routines", "new exercise interest"],
    "OCEAN Conscientiousness (fitness-adapted)": ["disciplined", "follow through", "structured approach"],
    "MBTI Judging/Perceiving": ["structured vs flexible", "organised vs spontaneous", "routine preference"],
    "SDT Autonomy": ["choose my workout", "self-directed exercise", "independent routine"],
    "SDT Competence": ["confidence in workouts", "skill belief", "fitness ability"],
    "Mental Toughness (4Cs simplified)": ["bounce back", "resilience", "handle setbacks"],
    "Habit Formation": ["stick to habits", "routine keeper", "automatic behaviors"],
    "TTM Stage of Change": ["readiness", "preparation stage", "action phase", "fitness phase"],
    "Obliger Tendency (Four Tendencies)": ["need accountability", "external motivator", "social pressure helps"],

    "Workout adherence": ["stick to gym", "exercise consistently", "no skipping workouts"],
    "Weight": ["current weight", "body weight", "scale reading"],
    "Diet adherence": ["follow meal plan", "stick to diet", "no cheat days"],
    "Self-confidence": ["believe in self", "I can do it", "confidence levels"]
}


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

def fuzzy_match_hybrid(user_input, emb_dict, thresh_full=0.82, thresh_partial=0.76):
    """
    Combines full sentence + keyword phrase matching.
    1. Run full sentence match (high precision).
    2. Split into bigrams + keywords; run fuzzy match on each (higher recall).
    3. Return all unique matches, sorted by max sim.
    """
    q_vec = MODEL.encode([user_input])[0]
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
        p_vec = MODEL.encode([phrase])[0]
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
#    print(fuzzy_match_hybrid("Sometimes I get too stressed and I can’t bounce back", TRAIT_EMBEDS))

if __name__ == "__main__":
    print("Testing trait matcher for 'stick to habits':")
    print(fuzzy_match_hybrid("stick to habits", TRAIT_EMBEDS))