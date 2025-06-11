import re
from embedding_utils import fuzzy_match_hybrid, KPI_EMBEDS, TRAIT_EMBEDS
from embedding_utils import KPI_SYNONYMS, TRAIT_SYNONYMS   # Adjust import as needed



def classify_user_input(user_msg, user_active_kpis):

    """
    Determines the question context, returns context tag,
    matched KPIs, traits, and if it's identity- or action-based.
    """

    msg_lower = user_msg.lower()
    kpi_hits   = fuzzy_match_hybrid(msg_lower, KPI_EMBEDS)
    trait_hits = fuzzy_match_hybrid(msg_lower, TRAIT_EMBEDS)

    wants_identity = bool(re.search(r"\b(be|become|feel|mindset|identity)\b", msg_lower))

    # Build ambiguous terms set dynamically (intersection of all synonyms)
    all_kpi_terms = set([s for syns in KPI_SYNONYMS.values() for s in syns] + list(KPI_SYNONYMS.keys()))
    all_trait_terms = set([s for syns in TRAIT_SYNONYMS.values() for s in syns] + list(TRAIT_SYNONYMS.keys()))
    AMBIG_TERMS = all_kpi_terms & all_trait_terms

    # Ambiguity: if input contains any ambiguous term AND you got both a KPI and trait hit
    if kpi_hits and trait_hits:
        for word in AMBIG_TERMS:
            if word in msg_lower:
                return "context_5", {"ambig_token": word}, wants_identity

    if not kpi_hits and not trait_hits:
        return "context_6", {}, wants_identity

    if kpi_hits and trait_hits:
        return "context_3", {"kpis": kpi_hits, "traits": trait_hits}, wants_identity

    if len(kpi_hits) > 1:
        return "context_4", {"kpis": kpi_hits}, wants_identity

    if kpi_hits:
        return "context_1", {"kpis": kpi_hits}, wants_identity

    return "context_2", {"traits": trait_hits, "user_kpis": user_active_kpis}, wants_identity



# ------------ TEST HARNESS -------------
#if __name__ == "__main__":
#    test_cases = [
#        "I want more energy",                       # Should go to context_1 (KPI only, not ambiguous)
#        "How do I sleep better?",                   # Should go to context_5 (ambiguity)
#        "I want to improve nutrition",              # Should go to context_5 (ambiguity if in both)
#        "How do I boost my mood and sleep?",        # context_3 or context_5 depending on synonyms
#        "How do I stick to habits?",                # trait-only context_2
#        "I want to lose fat and gain muscle",       # context_4 (multi-KPI)
#        "How do I become more resilient?",          # trait-only context_2
#        "What's the best protein powder?"           # context_6 (none)
#    ]
#    active_kpis = ["body positivity", "muscle mass gain"]

#    print("AMBIG_TERMS being used:", set(KPI_SYNONYMS.keys()) & set(TRAIT_SYNONYMS.keys()))

#    for msg in test_cases:
#        context, entities, wants_identity = classify_user_input(msg, active_kpis)
#        print(f"\nInput: {msg}")
#        print(f"Context: {context}")
#        print(f"Entities: {entities}")
#        print(f"Wants identity advice? {wants_identity}")
