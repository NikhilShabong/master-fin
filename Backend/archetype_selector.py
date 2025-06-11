# archetype_selector.py

KPI_TO_ARCHETYPE = {
    "KPI 14 (Strength Benchmarks)": "Powerlifting",
    "KPI 12 (Muscle Mass Gain)": "Powerlifting",  # or "Hypertrophy Training" if more nuanced
    "KPI 11 (Body Fat %)": "Hypertrophy",  # or "HIIT / Fat Loss Focused"
    "KPI 1 (Body Positivity)": "Hypertrophy",
    "KPI 13 (Weight Management)": "HIIT / Fat Loss Focused",
    "KPI 5 (Increased Energy Levels)": "HIIT / Fat Loss Focused",
    "KPI 15 (Cardiovascular Endurance)": "Cardiovascular Endurance",
    "KPI 4 (Mood Improvement)": "Cardiovascular Endurance",
    "KPI 3 (Stress Reduction)": "Cardiovascular Endurance",
    "KPI 18 (Sport enhancement - Speed & Agility)": "Athletic Functional",
    "KPI 17 (Sport enhancement - Balance & Coordination)": "Athletic Functional",
    "KPI 16 (Sport enhancement - Flexibility & Mobility)": "Athletic Functional",
    "KPI 6 (Improved Sleep Quality)": "Rehab (Recovery)",
    "KPI 2 (Self-Esteem Enhancement)": "Rehab (Recovery)",
}

def select_archetype_from_kpis(selected_kpis):
    """
    Accepts a list of user KPIs and returns the most relevant archetype (by majority or by predefined priority).
    """
    if not selected_kpis:
        return "Hypertrophy Training"  # Default fallback

    counts = {}
    for kpi in selected_kpis:
        archetype = KPI_TO_ARCHETYPE.get(kpi)
        if archetype:
            counts[archetype] = counts.get(archetype, 0) + 1

    # Return the archetype with the highest count
    if counts:
        return max(counts.items(), key=lambda x: x[1])[0]
    else:
        return "Powerlifting Beginner"  # Fallback

# Example usage:
# selected = ["Body Fat %", "Energy Levels"]
# archetype = select_archetype_from_kpis(selected)
