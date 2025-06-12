from data_loader import load_kpi_habits, load_habit_specialisation
from delta_utils import calculate_trait_deltas
from gpt_caller import call_gpt_advice, call_gpt_aftermath
from tone_style_builder import build_tone_style


# sample_current = {
#     "Sleep": 2,
#     "Nutrition": 3,
#     "Lingering Pain": 2,
#     "Exercise Enjoyment (Affective Attitude) – during workout": 4,
#     "Exercise Enjoyment (Affective Attitude) – after workout": 3,
#     "Exercise Intensity Preference": 2,
#     "Exercise Intensity Tolerance": 3,

#     "Weather Impacts": 3,
#     "Chronotype (Morningness–Eveningness)": 2,

#     "OCEAN Extraversion (Social motivation)": 3,
#     "OCEAN Agreeableness": 4,
#     "Social Exercise Orientation (Group-oriented vs Independent)": 3,

#     "OCEAN Neuroticism (Stress Reactivity)": 4,
#     "PERMA Positive Emotion": 2,
#     "PERMA Accomplishment": 3,
#     "Negative Affectivity (Type D)": 4,
#     "Social Inhibition (Type D)": 3,

#     "OCEAN Openness (fitness-adapted)": 2,
#     "OCEAN Conscientiousness (fitness-adapted)": 3,
#     "MBTI Judging/Perceiving": 3,
#     "SDT Autonomy": 2,
#     "SDT Competence": 3,
#     "Mental Toughness (4Cs simplified)": 2,
#     "Habit Formation": 3,
#     "TTM Stage of Change": 2,
#     "Obliger Tendency (Four Tendencies)": 3,

#     "Workout adherence": 2,
#     "Weight": 3,
#     "Diet adherence": 2,
#     "Self-confidence": 3
# }

# sample_future = {
#     "Sleep": 5,
#     "Nutrition": 4,
#     "Lingering Pain": 3,
#     "Exercise Enjoyment (Affective Attitude) – during workout": 5,
#     "Exercise Enjoyment (Affective Attitude) – after workout": 4,
#     "Exercise Intensity Preference": 4,
#     "Exercise Intensity Tolerance": 4,

#     "Weather Impacts": 2,
#     "Chronotype (Morningness–Eveningness)": 3,

#     "OCEAN Extraversion (Social motivation)": 4,
#     "OCEAN Agreeableness": 5,
#     "Social Exercise Orientation (Group-oriented vs Independent)": 4,

#     "OCEAN Neuroticism (Stress Reactivity)": 2,
#     "PERMA Positive Emotion": 5,
#     "PERMA Accomplishment": 5,
#     "Negative Affectivity (Type D)": 1,
#     "Social Inhibition (Type D)": 2,

#     "OCEAN Openness (fitness-adapted)": 4,
#     "OCEAN Conscientiousness (fitness-adapted)": 5,
#     "MBTI Judging/Perceiving": 4,
#     "SDT Autonomy": 5,
#     "SDT Competence": 4,
#     "Mental Toughness (4Cs simplified)": 5,
#     "Habit Formation": 5,
#     "TTM Stage of Change": 4,
#     "Obliger Tendency (Four Tendencies)": 4,

#     "Workout adherence": 5,
#     "Weight": 2,
#     "Diet adherence": 4,
#     "Self-confidence": 5
# }


# user_vectors = {
#     'current': sample_current,
#     'future': sample_future,
#     'active_kpis': ['KPI 6 (Improved Sleep Quality)', 'KPI 12 (Muscle Mass Gain)']
# }

KPI_HABITS = load_kpi_habits()
HABIT_SPEC = load_habit_specialisation()

# Use a static tone_style for now, or load from user_profile/session
user_profile = {
    "tone_style": "Adopt a calm, supportive, and practical tone, always encouraging the user's progress and resilience."
}

def filter_direct_traits(kpi_name, trait_list):
    direct_traits = []
    for t in trait_list:
        for obj in KPI_HABITS[kpi_name]:
            if obj['trait'] == t and obj['impact'] == "direct":
                direct_traits.append(t)
    return direct_traits

def get_snippet_for_trait(kpi, trait, delta_status, wants_identity):
    if kpi in HABIT_SPEC and trait in HABIT_SPEC[kpi]:
        spec = HABIT_SPEC[kpi][trait]
        if wants_identity and 'perspective' in spec:
            return spec['perspective']
        elif delta_status == "low":
            return spec['low_score_strategy']['habit_prompt_text']
        else:
            return spec['high_score_strategy']['habit_prompt_text']
    else:
        for obj in KPI_HABITS[kpi]:
            if obj['trait'] == trait:
                if wants_identity and 'perspective' in obj:
                    return obj['perspective']
                else:
                    return obj['habit']
    return None

def generate_advice(context, entities, wants_identity, user_vectors, user_message):
    advice_snippets = []
    trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
    trait_deltas = {k: v for k, v in trait_deltas.items()}
    tone_style = build_tone_style(user_vectors['current'], user_vectors['future'])

    if context == "context_1":
        kpi = entities['kpis'][0]
        traits = filter_direct_traits(kpi, [obj['trait'] for obj in KPI_HABITS[kpi]])
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        for t in traits[:2]:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
            if snippet: advice_snippets.append(snippet)

    elif context == "context_2":
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        for t in entities['traits'][:2]:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            for kpi in user_vectors['active_kpis']:
                snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
                if snippet:
                    advice_snippets.append(f"{kpi} - {snippet}")

    elif context == "context_3":
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        for t in entities['traits'][:2]:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            for kpi in entities['kpis']:
                snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
                if snippet:
                    advice_snippets.append(f"{kpi} - {snippet}")

    elif context == "context_4":
        all_traits = [set([obj['trait'] for obj in KPI_HABITS[k]]) for k in entities['kpis']]
        shared_traits = set.intersection(*all_traits)
        advice_given = False
        for t in shared_traits:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            if all(obj['impact'] == 'direct' for k in entities['kpis'] for obj in KPI_HABITS[k] if obj['trait'] == t):
                for kpi in entities['kpis']:
                    snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
                    if snippet: advice_snippets.append(f"{kpi} - {snippet}")
                advice_given = True
                break
        if not advice_given:
            for kpi in entities['kpis'][:2]:
                traits = filter_direct_traits(kpi, [obj['trait'] for obj in KPI_HABITS[kpi]])
                for t in traits[:2]:
                    if t not in trait_deltas:
                        print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                        continue
                    snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
                    if snippet: advice_snippets.append(f"{kpi} - {snippet}")

    elif context == "context_5":
        # MVP: Treat ambiguous as context_2 (trait-specific)
        context = "context_2"
        # (Let the existing context_2 code below handle advice_snippets, etc.)

    # Aftermath mode: purely conversational follow-up with no extra advice
    elif context == "context_6":
        gpt_reply = call_gpt_aftermath(user_message, tone_style)
        return {"raw_advice": tone_style, "gpt_advice": gpt_reply}

    
    
    final_prompt = tone_style + "\n\n" + "\n".join(advice_snippets)
    gpt_reply = call_gpt_advice(tone_style, "\n".join(advice_snippets))
    return {
        "raw_advice": final_prompt.strip(),
        "gpt_advice": gpt_reply
    }



#if __name__ == "__main__":
#    # Simulated test cases for each context
#    test_cases = [
#        ("context_1", {'kpis': ['KPI 6 (Improved Sleep Quality)']}, False, user_vectors),
#        ("context_2", {'traits': ['Sleep']}, False, user_vectors),
#        ("context_3", {'kpis': ['KPI 6 (Improved Sleep Quality)'], 'traits': ['Sleep']}, False, user_vectors),
#        ("context_4", {'kpis': ['KPI 6 (Improved Sleep Quality)', 'KPI 12 (Muscle Mass Gain)']}, False, user_vectors),
#        ("context_5", {}, False, user_vectors),
#        ("context_6", {}, False, user_vectors)
#    ]

#    for i, (context, entities, wants_id, user_vecs) in enumerate(test_cases):
#        print(f"\nTest Case {i+1} - {context}")
#        print(generate_advice(context, entities, wants_id, user_vecs))