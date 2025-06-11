# workout_generator.py
from data_loader import load_workout_tailoring_vector
from delta_utils import calculate_trait_deltas

def generate_tailored_workout_snippets(current_vector, future_vector, archetype):
    workout_data = load_workout_tailoring_vector()
    tailored_snippets = []

    trait_data = workout_data.get(archetype, {})
    for trait, strategies in trait_data.items():
        current_score = current_vector.get(trait)
        future_score = future_vector.get(trait)

        if current_score is None or future_score is None:
            continue

        # If user needs to "improve" trait, use low strategy; else use high
        if future_score > current_score:
            strategy = strategies.get("low_score_strategy", {}).get("workout_tailoring_text")
        else:
            strategy = strategies.get("high_score_strategy", {}).get("workout_tailoring_text")

        if strategy:
            tailored_snippets.append(f"- **{trait}**: {strategy}")

    return tailored_snippets

def build_gpt_prompt(archetype, tailored_snippets):
    intro = f"You are a virtual fitness coach. Write a detailed, practical 1-week workout plan for a user with the '{archetype}' archetype. " \
            "The plan must take into account the following tailored requirements:\n"
    requirements = "\n".join(tailored_snippets)
    ending = "\nStructure each week, and clearly mention special adjustments based on each requirement. Use bullet points and keep it actionable."
    return intro + requirements + ending
