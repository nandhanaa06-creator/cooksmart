import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"

SYSTEM_PROMPT = """
You are a professional chef and nutrition assistant.

Rules:
- Give clear, practical answers
- Avoid unnecessary text
- Do not use emojis
- If the ingredients are unsafe or not food items, politely refuse
"""


# ===============================
# CORE AI CALL
# ===============================
import requests

def ask_ai(user_prompt: str) -> str:
    full_prompt = f"""{SYSTEM_PROMPT}

{user_prompt}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": full_prompt,

                # ⚙️ Ollama best practices
                "stream": False,
                "temperature": 0.4,   # stable + less hallucination
                "num_predict": 250    # enough for nutrition, fast
            },
            timeout=90   # avoid hanging UI
        )

        response.raise_for_status()

        result = response.json().get("response", "").strip()

        # 🛡️ Final safety guard (prevents empty modals)
        if not result:
            return "No valid response generated. Please try again."

        return result

    except requests.exceptions.Timeout:
        return "AI is taking too long. Please try again."

    except requests.exceptions.RequestException as e:
        return "AI service error. Please try again later."



# ===============================
# DIET CONVERTER
# ===============================
def convert_recipe_diet(recipe_text: str, diet_type: str) -> str:
    prompt = f"""
Convert this recipe to a {diet_type} version.

Return ONLY:
- Ingredients
- Steps

Recipe:
{recipe_text}
"""
    return ask_ai(prompt)


# ===============================
# STEP IMPROVER
# ===============================
def improve_steps(steps_text: str) -> str:
    prompt = f"""
Improve these cooking steps.

Rules:
- One step per line
- Clear and professional
- Return ONLY steps

Steps:
{steps_text}
"""
    return ask_ai(prompt)

# ===============================
# NUTRITION VERSION (FIXED)
# ===============================
def nutrition_aware_recipe(recipe_text: str) -> str:
    prompt = f"""
Estimate nutrition for ONE serving.

Rules:
- Always give calories
- Use common food assumptions
- Do NOT give recipe or ingredients
- Keep response short
- If items are not edible, politely refuse

Format:

Calories:
- ~<number> kcal

Health Rating:
- Healthy | Moderate | Unhealthy
- Reason: <short>

Notes:
- <note>
- <note>

Tips:
- <tip>
- <tip>

Recipe:
{recipe_text}
"""
    return ask_ai(prompt)




