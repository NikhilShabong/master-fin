# gpt_caller.py
import os
import openai

# Ensure your OPENAI_API_KEY is set as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt_advice(tone, advice_snippets, kpi_name=None, chat_history=None):
    """
    Calls the OpenAI GPT API with a tone and advice prompt.
    Returns the GPT's generated reply.
    """
    system_prompt = f"You are a fitness coach. Always use this style: {tone}"
    user_prompt = (
        f"Below are the science-backed habits and strategies that people who successfully achieve {kpi_name} use.\n"
        "Please suggest to the user how they can start applying these steps, even if they haven't begun yet.\n"
        "Frame each suggestion as a positive action they can try—not as something they already do.\n"
        "Advice to consider:\n"
        + "\n".join(advice_snippets)
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
            max_tokens=400
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
        f"Maintain this tone: {tone_spec}"
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