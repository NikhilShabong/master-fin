# gpt_caller.py
import os
import openai
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure your OPENAI_API_KEY is set as an environment variable
#openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt_advice(tone, advice_snippets, wants_identity=False, kpi_name=None,  chat_history=None):
    """
    Calls the OpenAI GPT API with a tone and advice prompt.
    Returns the GPT's generated reply.
    """
    system_prompt = f"You are a fitness coach. Always use this style of talking: {tone}"
    if wants_identity:
        user_prompt = (
            f"You're an expert fitness mindset coach. "
            "The user wants to understand the best perspective or mindset for success on their goal. "
            f"Give them a motivating, psychologically supportive insight about {kpi_name if kpi_name else 'their fitness journey'}, "
            "framing it as an internal perspective to hold, not an action plan or set of steps. "
            "Be concise and impactful and give output in a conversational style, not a step-by-step plan.\n"
            "Perspective: " + "\n".join(advice_snippets)
        )
        max_tokens = 130  # (Or whatever is appropriate for concise output)
    else:
        user_prompt = (
            f"You're a fitness coach, Below are the science-backed habits and strategies that people who successfully achieve {kpi_name} should use.\n"
            "Please suggest to the user how they can start applying these steps, even if they haven't begun yet.\n"
            "Give output in a conversational style, not a step-by-step plan.\n"
            "Do not frame the outputs as something they already do, but an action they can try\n"
            "Here are the main points to cover:\n"
            + "\n".join(advice_snippets)
        )
        max_tokens = 220
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    # For future: you can add chat history to messages here if desired
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return "Sorry, I couldn't generate advice at the moment."

# gpt_caller.py

def call_gpt_habit_blueprint(trait, kpi, blueprint_steps, source=None):
    """
    Calls GPT to present the habit blueprint in a user-friendly, step-by-step way.
    """
    system_prompt = (
        "You are a behavioural change coach. "
        "Present the following science-backed habit blueprint as a positive, step-by-step action plan for the user, "
        "explaining why each step helps them with their fitness goal. Make it practical, motivational, and easy to follow."
    )
    steps_bullet = "\n".join(f"{i+1}. {step}" for i, step in enumerate(blueprint_steps))
    user_prompt = (
        f"This is a detailed habit blueprint for {trait} to help the user with {kpi}:\n"
        f"{steps_bullet}\n"
        + (f"\nSource: {source}\n" if source else "")
        + "Write a practical, actionable plan that helps the user implement these steps, include the source if a step refers to it"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    # For future: you can add chat history to messages here if desired
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return "Sorry, I couldn't generate advice at the moment."


def call_gpt_workout(prompt):
    """
    Calls the OpenAI GPT API specifically for workout generation.
    Returns the GPT's generated workout plan.
    """
    system_prompt = "You are a professional fitness coach specializing in creating personalized workout plans."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return "Sorry, I couldn't generate a workout plan at the moment."


def call_gpt_aftermath(user_message, tone_spec):
    """Call GPT for conversational follow-ups without injecting advice.

    Parameters
    ----------
    user_message : str
        The user's last message in the chat.
    tone_spec : str
        A short tone description generated for the user.

    Returns
    -------
    str
        The assistant's conversational reply.
    """

    system_prompt = (
        "You are a friendly, supportive AI fitness mentor. "
        "Respond conversationally without giving specialised advice. "
        f"Maintain this tone always: {tone_spec}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return "Sorry, I couldn't respond at the moment."