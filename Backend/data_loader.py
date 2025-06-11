import json

def load_kpi_habits(filepath="KPI_specific_Habits_and_Perspectives.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Load the file
kpi_habits = load_kpi_habits()

# Print all top-level KPIs (keys)
#print("List of KPIs:", list(kpi_habits.keys()))

# Print the first KPI's first trait entry as a sample
first_kpi = list(kpi_habits.keys())[0]
#print(f"\nFirst KPI: {first_kpi}")
#print("Sample trait data:", kpi_habits[first_kpi][0])

def load_habit_specialisation(filepath="Habit_specialisation_vector.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Load and test:
habit_specialisation = load_habit_specialisation()
#print("KPI names:", list(habit_specialisation.keys()))
first_kpi = list(habit_specialisation.keys())[0]
#print(f"First KPI: {first_kpi}")
first_trait = list(habit_specialisation[first_kpi].keys())[0]
#print("Sample trait data:", habit_specialisation[first_kpi][first_trait])

def load_tone_spec(filepath="Tone_spec.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Load and print a sample trait entry to verify:
tone_spec = load_tone_spec()
#print("Tone traits:", list(tone_spec.keys()))
first_trait = list(tone_spec.keys())[0]
#print(f"First tone trait: {first_trait}")
#print("Sample tone data:", tone_spec[first_trait])


import json

def load_workout_tailoring_vector(filepath="Exercise.json"):
    with open(filepath,"r", encoding="utf-8") as f:
        data = json.load(f)
    return data
