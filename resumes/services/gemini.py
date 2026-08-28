import json

from django.conf import settings
from groq import Groq


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def analyze_resume(text):

    prompt = f"""
You are an expert ATS resume parser.

Analyze the following resume and extract ONLY the information below.

Return ONLY valid JSON.

Do not include explanations.
Do not use markdown.
Do not wrap the JSON inside ```.

Return exactly in this format:

{{
    "skills": [],
    "projects": [],
    "education": [],
    "certifications": []
}}

Resume:

{text}
"""

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS resume parser."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            max_tokens=1500
        )

        result = response.choices[0].message.content.strip()

        print("\n" + "=" * 60)
        print("RAW GROQ RESPONSE")
        print("=" * 60)
        print(result)
        print("=" * 60 + "\n")

        # Remove markdown if the model returns it
        if result.startswith("```"):

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        data = json.loads(result)

        return {
            "skills": data.get("skills", []),
            "projects": data.get("projects", []),
            "education": data.get("education", []),
            "certifications": data.get("certifications", [])
        }

    except json.JSONDecodeError as e:

        print("JSON Decode Error:")
        print(e)

    except Exception as e:

        print("Groq API Error:")
        print(e)

    return {
        "skills": [],
        "projects": [],
        "education": [],
        "certifications": []
    }