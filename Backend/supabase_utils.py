from supabase import create_client
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_embedding(text):
    cached = fetch_cached_embedding(text)
    if cached:
        print(f"[Cache] Hit for: {text}")
        return cached
    embedding = model.encode(text).tolist()
    store_cached_embedding(text, embedding)
    print(f"[Cache] Missed. Stored: {text}")
    return embedding

async def store_session(session_data):
    try:
        supabase.table("sessions").insert(session_data).execute()
        print("[✓] Session stored")
    except Exception as e:
        print(f"[!] Failed to store session: {e}")

async def store_session(session_data):
    try:
        supabase.table("sessions").insert(session_data).execute()
        print("[✓] Session stored")
    except Exception as e:
        print(f"[!] Failed to store session: {e}")

def fetch_cached_embedding(key):
    res = supabase.table("embedding_cache").select("*").eq("embedding_key", key).execute()
    return res.data[0]['embedding_vector'] if res.data else None

def store_cached_embedding(key, vector):
    supabase.table("embedding_cache").upsert({
        "embedding_key": key,
        "embedding_vector": vector
    }).execute()
