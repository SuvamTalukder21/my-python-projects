import os
import asyncio
import time
from typing import Dict, Any

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from google import genai
from fastapi.encoders import jsonable_encoder

# ─── Configuration ─────────────────────────────────────────────────────────────

load_dotenv()  # loads GEMINI_API_KEY, MONGO_URI

GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
MONGO_URI        = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME          = "countries_db"
COLLECTION_NAME  = "countries"

# ─── Initialize Clients ─────────────────────────────────────────────────────────

# MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db           = mongo_client[DB_NAME]
collection   = db[COLLECTION_NAME]

# Gemini
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# ─── Prompt Template ────────────────────────────────────────────────────────────

PROMPT_TEMPLATE = """
You are a knowledgeable global encyclopedia. For the country {common_name}, please provide exactly one concise “interesting fact” in JSON format for each of the following categories.
If you cannot find a fact for a category, return "N/A" for that category’s value.

Categories:
1. geography and demographics
2. history and heritage
3. culture and traditions
4. economy and industry
5. religion and philosophy
6. science and technology
7. languages and literature
8. films and sports
9. food and cuisine
10. biodiversity and environment

**Output ONLY valid JSON**, for example:

{{
    "geography and demographics": "...",
    "history and heritage": "...",
    "culture and traditions": "...",
    "economy and industry": "...",
    "religion and philosophy": "...",
    "science and technology": "...",
    "languages and literature": "...",
    "films and sports": "...",
    "food and cuisine": "...",
    "biodiversity and environment": "..."
}}
"""

# ─── Helper: Parse Gemini’s JSON-like text ───────────────────────────────────────

import json
def parse_facts_json(text: str) -> Dict[str, str]:
    """
    Attempts to load Gemini’s response as JSON. Cleans common pitfalls.
    """
    # Sometimes Gemini wraps JSON in markdown fences or escapes quotes
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # remove code fences
        cleaned = cleaned.strip("`").strip("json").strip()
    # now parse
    return json.loads(cleaned)


# ─── Helper: Convert MongoDB documents to JSON-safe format ──────────────────────
def normalize_fact_keys(text: str) -> Dict[str, str]:
    """
    Transforms the long-format keys from Gemini API response to shorter, normalized keys.
    """
    key_mapping = {
        "geography and demographics": "geography",
        "history and heritage": "history",
        "culture and traditions": "culture",
        "economy and industry": "economy",
        "religion and philosophy": "philosophy",
        "science and technology": "science",
        "languages and literature": "literature",
        "films and sports": "entertainment",
        "food and cuisine": "food",
        "biodiversity and environment": "environment"
    }

    # parse the JSON
    facts_json = parse_facts_json(text)

    return {key_mapping.get(k, k): v for k, v in facts_json.items()}


# ─── Main Enrichment Logic ──────────────────────────────────────────────────────

async def enrich_all_countries():
    cursor = collection.find({}, {"_id": 0, "name.common": 1, "cca3": 1})
    countries = await cursor.to_list(length=None)

    # Track request count to manage rate limiting
    request_count = 0

    for country in countries:
        cca3 = country.get("cca3")
        common_name = country["name"]["common"]

        # Add rate limiting: wait after every 10 requests
        if request_count > 0 and request_count % 10 == 0:
            print(f"⏱️ Rate limit protection: Pausing for 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds every 10 requests

        print(f"Enriching {common_name} ({cca3})...")
        prompt = PROMPT_TEMPLATE.format(common_name=common_name)

        try:
            # Gemini API call
            resp = gemini_client.models.generate_content(
                model="gemini-1.5-flash",  # Use a valid model name
                contents=prompt
            )
            request_count += 1  # Increment counter on successful request
            text = resp.text

            # parse JSON
            try:
                facts = normalize_fact_keys(text)
            except Exception as e:
                print(f"  ✗ Failed to parse JSON for {cca3}: {e}")
                continue

            # ensure it's JSON safe
            facts = jsonable_encoder(facts)

            # update MongoDB
            result = await collection.update_one(
                {"cca3": cca3},
                {"$set": {"interestingFacts": facts}}
            )

            if result.modified_count:
                print(f"  ✓ Updated {cca3}")
            else:
                print(f"  ⚠️ No document updated for {cca3}")

        except genai.exceptions.ApiError as e:
            if "429" in str(e):  # Rate limit error
                retry_delay = 65  # Default retry delay in seconds
                print(f"  ⚠️ Rate limit reached. Pausing for {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Try again after waiting
                continue
            else:
                print(f"  ✗ API error for {cca3}: {e}")
                continue
        except Exception as e:
            print(f"  ✗ General error for {cca3}: {e}")
            continue

    print("✅ Enrichment complete.")

# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(enrich_all_countries())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(enrich_all_countries())
    # loop.close()
    # print("Run this script with `python -m app.utils.enrichment` to enrich all countries.")
    # print(parse_facts_json())
    # # Example usage for testing:
    # print(parse_facts_json('{"geography": "N/A", "history": "N/A", "culture": "N/A", "economy": "N/A", "philosophy": "N/A", "science": "N/A", "literature": "N/A", "entertainment": "N/A", "food": "N/A", "environment": "N/A"}'))
    # prompt = PROMPT_TEMPLATE.format(common_name="India")
    #
    # # Gemini API call
    # resp = gemini_client.models.generate_content(
    #     model="gemini-2.0-flash",
    #     contents=prompt
    # )
    # print(resp.text)
    # facts = normalize_fact_keys(resp.text)

    # print(cleaned)
    # now parse
    # print(resp.text)
    # print(normalize_fact_keys(resp.text))

