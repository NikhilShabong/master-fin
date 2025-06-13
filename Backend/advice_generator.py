from data_loader import load_kpi_habits, load_habit_specialisation
from delta_utils import calculate_trait_deltas
from gpt_caller import call_gpt_advice, call_gpt_aftermath, call_gpt_habit_blueprint
from tone_style_builder import build_tone_style

KPI_HABITS = load_kpi_habits()
HABIT_SPEC = load_habit_specialisation()

def find_blueprint_traits_for_advice(kpis, traits, habit_spec, trait_deltas):
    """
    For each KPI/trait pair in the advice, check if a blueprint exists for the right score status.
    Returns a list of (kpi, trait, strat) tuples.
    """
    result = []
    for kpi in kpis:
        for trait in traits:
            if kpi in habit_spec and trait in habit_spec[kpi]:
                status = trait_deltas.get(trait, {}).get("status", "low")
                strat = "low_score_strategy" if status == "low" else "high_score_strategy"
                bp = habit_spec[kpi][trait].get(strat, {}).get("habit_blueprint", [])
                if bp and isinstance(bp, list) and bp:
                    result.append((kpi, trait, strat))
    return result

def generate_habit_blueprint_response(last_traits, last_kpis, user_vectors):
    """
    For each trait/KPI, returns a GPT-formatted habit blueprint (max 2).
    """
    trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
    blueprint_outputs = []
    for kpi in last_kpis:
        for trait in last_traits:
            status = trait_deltas.get(trait, {}).get("status", "low")
            strat = "low_score_strategy" if status == "low" else "high_score_strategy"
            bp_block = HABIT_SPEC.get(kpi, {}).get(trait, {}).get(strat, {})
            steps = bp_block.get("habit_blueprint", [])
            source = bp_block.get("source", "")
            if steps:
                gpt_plan = call_gpt_habit_blueprint(trait, kpi, steps, source)
                blueprint_outputs.append(gpt_plan)
            if len(blueprint_outputs) == 2:
                break
    if not blueprint_outputs:
        return "Sorry, no habit blueprints available for these traits/KPIs."
    return "\n\n".join(blueprint_outputs)

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
    # Try to get from HABIT_SPEC first for normal habits
    if kpi in HABIT_SPEC and trait in HABIT_SPEC[kpi]:
        spec = HABIT_SPEC[kpi][trait]
        if not wants_identity:
            if delta_status == "low":
                return spec['low_score_strategy']['habit_prompt_text']
            else:
                return spec['high_score_strategy']['habit_prompt_text']
    # For perspective output or fallback
    for obj in KPI_HABITS[kpi]:
        if obj['trait'] == trait:
            if wants_identity and 'perspective' in obj:
                return obj['perspective']
            elif not wants_identity and 'habit' in obj:
                return obj['habit']
    return None


def generate_advice(context, entities, wants_identity, user_vectors, user_message):
    advice_snippets = []
    trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
    trait_deltas = {k: v for k, v in trait_deltas.items()}
    tone_style = build_tone_style(user_vectors['current'], user_vectors['future'])

    if context == "context_1":
        last_traits = []
        last_kpis = []
        last_kpis = [entities['kpis'][0]]
        kpi = entities['kpis'][0]
        traits = filter_direct_traits(kpi, [obj['trait'] for obj in KPI_HABITS[kpi]])
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        for t in traits[:2]:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
            if snippet:
                advice_snippets.append(snippet)
                if t in trait_deltas and len(last_traits) < 2: last_traits.append(t)

    elif context == "context_2":
        last_traits = []
        last_kpis = []
        last_kpis = user_vectors['active_kpis'][:2]
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        last_traits = [t for t in entities['traits'][:2] if t in trait_deltas]
        for t in entities['traits'][:2]:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            for kpi in user_vectors['active_kpis']:
                snippet = get_snippet_for_trait(kpi, t, trait_deltas[t]['status'], wants_identity)
                if snippet:
                    advice_snippets.append(f"{kpi} - {snippet}")

    elif context == "context_3":
        last_traits = []
        last_kpis = []
        last_kpis = [k for k in entities['kpis'][:2] if k in KPI_HABITS]
        trait_deltas = calculate_trait_deltas(user_vectors['current'], user_vectors['future'])
        trait_deltas = {k: v for k, v in trait_deltas.items()}
        last_traits = [t for t in entities['traits'][:2] if t in trait_deltas]
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
        last_traits = []
        last_kpis = []
        advice_given = False
        for t in shared_traits:
            if t not in trait_deltas:
                print(f"[DEBUG] Trait '{t}' missing from trait_deltas, skipping...")
                continue
            if all(obj['impact'] == 'direct' for k in entities['kpis'] for obj in KPI_HABITS[k] if obj['trait'] == t):
                last_traits.append(t)
                last_kpis.extend([k for k in entities['kpis'] if k not in last_kpis])
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
                    if snippet: 
                        advice_snippets.append(f"{kpi} - {snippet}")
                        # Only add unique traits/kpis
                        if t not in last_traits and len(last_traits) < 2:
                            last_traits.append(t)
                        if kpi not in last_kpis and len(last_kpis) < 2:
                            last_kpis.append(kpi)

    elif context == "context_5":
        # MVP: Treat ambiguous as context_2 (trait-specific)
        context = "context_2"
        # (Let the existing context_2 code below handle advice_snippets, etc.)

    # Aftermath mode: purely conversational follow-up with no extra advice
    elif context == "context_6":
        gpt_reply = call_gpt_aftermath(user_message, tone_style)
        return {"raw_advice": tone_style, "gpt_advice": gpt_reply}
    
    if context == "context_7":
        last_traits = entities.get("last_traits", [])
        last_kpis = entities.get("last_kpis", [])
        blueprint_output = generate_habit_blueprint_response(last_traits, last_kpis, user_vectors)
        if not last_traits or not last_kpis:
            return {
        "raw_advice": "Sorry, no habit blueprints are available for your last question. Try asking about a specific goal or trait first!",
        "gpt_advice": "Sorry, no habit blueprints are available for your last question. Try asking about a specific goal or trait first!"
        }
        return {
            "raw_advice": blueprint_output,
            "gpt_advice": blueprint_output
        }

    # Check blueprints for these trait/KPI pairs
    blueprint_pairs = find_blueprint_traits_for_advice(last_kpis, last_traits, HABIT_SPEC, trait_deltas)
    show_habit_blueprint_prompt = bool(blueprint_pairs)

    prompt_addition = ""
    if show_habit_blueprint_prompt:
        prompt_addition = "\n\nWould you like a detailed habit blueprint? Type 'habit blueprint' to see more."
    
    final_prompt = tone_style + "\n\n" + "\n".join(advice_snippets) + prompt_addition
    gpt_reply = call_gpt_advice(tone_style, [*advice_snippets, prompt_addition], wants_identity, kpi_name=last_kpis[0] if last_kpis else None)
    return {
        "raw_advice": final_prompt.strip(),
        "gpt_advice": gpt_reply,
        "last_traits": last_traits,
        "last_kpis": last_kpis,
        "show_habit_blueprint_prompt": show_habit_blueprint_prompt
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