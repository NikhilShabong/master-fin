from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
from router import router
import json
import os               
import uuid            

app = FastAPI()
app.include_router(router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Responses(BaseModel):
    # Physical
    sleep: int = None
    nutrition: int = None
    pain: int = None
    exercise_enjoyment_during: int = None
    exercise_enjoyment_post: int = None
    exercise_preference: int = None
    exercise_tolerance: int = None

    # Environmental
    weather_impact: int = None
    chronotype: str = None

    # Social
    social_extraversion: int = None
    agreeableness: int = None
    social_exercise_orientation: int = None

    # Mental
    neuroticism: int = None
    positive_emotion: int = None
    accomplishment: int = None
    negative_affectivity: int = None
    social_inhibition: int = None

    # Psychological
    openness: int = None
    conscientiousness: int = None
    judging_perceiving: int = None
    sdt_autonomy: int = None
    sdt_competence: int = None
    mental_toughness: int = None
    habit_formation: int = None
    stage_of_change: str = None
    obliger_tendency: int = None

    # Learning Usability
    learning_style: str = None
    mbti_learning: int = None
    vark: str = None

    # Thinking Style
    thinking_style: str = None
    sensing_intuition: str = None

    # Fitness Specific
    fitness_experience: str = None
    weight: float = None
    meals_macros: str = None
    fitness_confidence: int = None


RESPONSES_FILE = os.path.join(os.path.dirname(__file__), "responses.json")


@app.post("/submit")
async def submit_responses(responses: dict):
    response_data = responses  # it's already a dict, no conversion needed


    # ✅ Add unique ID and timestamp to each response
    entry = {
        "user_id": str(uuid.uuid4()),  # random unique ID
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "responses": response_data
    }

    # Load existing responses
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "r") as f:
            all_responses = json.load(f)
    else:
        all_responses = []

    # Append new entry
    all_responses.append(entry)

    # Save updated list
    with open(RESPONSES_FILE, "w") as f:
        json.dump(all_responses, f, indent=2)

    return {"message": "Response saved", "user_id": entry["user_id"]}