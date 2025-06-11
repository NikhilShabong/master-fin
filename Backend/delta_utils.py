from data_loader import load_kpi_habits

def calculate_trait_deltas(current_vector, future_vector):
    """
    Both vectors are dicts: {trait_name: score}
    Returns dict: {trait_name: {'delta': Δ, 'status': 'low' or 'high'}}
    """
    output = {}
    for trait in current_vector:
        curr = current_vector[trait]
        future = future_vector.get(trait, curr)  # fallback if missing
        delta = future - curr
        status = "low" if abs(delta) >= 2 else "high"
        output[trait] = {'delta': delta, 'status': status}
    return output

def calculate_future_vector(selected_kpis, kpi_habits):
    """
    selected_kpis: list of KPI names (e.g., ["KPI 1 (Body Positivity)", ...])
    kpi_habits: dict loaded from KPI_specific_Habits_and_Perspectives.json
    Returns: dict {trait_name: averaged_score}
    """
    # Prepare an empty dict to sum scores per trait
    trait_totals = {}
    count_per_trait = {}

    for kpi in selected_kpis:
        for trait_obj in kpi_habits[kpi]:
            trait = trait_obj["trait"]
            score = trait_obj["score"]
            trait_totals[trait] = trait_totals.get(trait, 0) + score
            count_per_trait[trait] = count_per_trait.get(trait, 0) + 1

    # Calculate average per trait (avoid division by zero)
    future_vector = {}
    for trait, total in trait_totals.items():
        count = count_per_trait[trait]
        future_vector[trait] = total / count if count > 0 else 0

    return future_vector

#if __name__ == "__main__":

#    kpi_habits = load_kpi_habits()
#    selected_kpis = ["KPI 1 (Body Positivity)"]
#    current_vector = {"Sleep": 2, "Nutrition": 3, "Self-confidence": 5}

#    future_vector = calculate_future_vector(selected_kpis, kpi_habits)
#    print("Future vector:", future_vector)

#    deltas = calculate_trait_deltas(current_vector, future_vector)
#    print("Trait deltas:", deltas)
