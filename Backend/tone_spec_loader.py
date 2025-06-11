import json

def load_tone_spec(path="Tone_spec.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
