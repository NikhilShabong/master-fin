from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from input_classifier import classify_user_input   # <-- your classifier logic
from advice_generator import generate_advice       # <-- advice builder
from workout_generator import generate_tailored_workout_snippets, build_gpt_prompt
from gpt_caller import call_gpt_advice, call_gpt_workout
from archetype_selector import select_archetype_from_kpis


router = APIRouter()

class AdviceRequest(BaseModel):
    user_input: str
    current_vector: dict
    future_vector: dict
    active_kpis: list
    last_kpi: str = None
    last_trait: str = None

@router.post("/generate_advice")
async def generate_advice_endpoint(payload: AdviceRequest):
    try:
        # Step 1: Classify the user's message
        context, entities, wants_identity = classify_user_input(payload.user_input, payload.active_kpis)
        # Step 2: Build user_vectors for advice gen
        user_vectors = {
            'current': payload.current_vector,
            'future': payload.future_vector,
            'active_kpis': payload.active_kpis
        }
        # Step 3: Generate the advice
        advice_payload = generate_advice(context, entities, wants_identity, user_vectors, payload.user_input)
        # Step 4: Return everything in a response
        print("Context:", context)
        print("Entities:", entities)
        print("Wants identity:", wants_identity)
        print("Active KPIs:", payload.active_kpis)
        print("Advice (raw):", advice_payload["raw_advice"])
        print("GPT Advice:", advice_payload["gpt_advice"])
        return {
            "context": context,
            "entities": entities,
            "identity": wants_identity,
            "raw_advice": advice_payload["raw_advice"],
            "gpt_advice": advice_payload["gpt_advice"]
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # <-- This will print the FULL traceback in your backend terminal
        raise HTTPException(status_code=500, detail=str(e))

class WorkoutRequest(BaseModel):
    currentVector: dict
    futureVector: dict
    active_kpis: list  # New, to pass user KPIs

@router.post("/generate_workout")
async def generate_workout_plan(req: WorkoutRequest):
    try:
        # Auto-select archetype based on selected KPIs (req.active_kpis)
        # Try req.active_kpis, fallback to req.archetype for legacy support
        user_kpis = getattr(req, "active_kpis", None) or getattr(req, "selectedKpis", None) or []
        archetype = select_archetype_from_kpis(user_kpis)
        tailored_snippets = generate_tailored_workout_snippets(
            req.currentVector, req.futureVector, archetype
        )
        
        # Build the GPT prompt using the tailored snippets
        gpt_prompt = build_gpt_prompt(archetype, tailored_snippets)
        
        # Call GPT with the new workout-specific function
        gpt_response = call_gpt_workout(gpt_prompt)
        
        return {
            "archetype": archetype,
            "tailoring_snippets": tailored_snippets,
            "gpt_prompt": gpt_prompt,
            "plan": gpt_response
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))