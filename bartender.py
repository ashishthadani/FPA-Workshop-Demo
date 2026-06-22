import streamlit as st
import requests
from openai import OpenAI
 
# =========================
# CONFIG
# =========================
OPENAI_API_KEY = "PASTE_YOUR_API_KEY_HERE"
client = OpenAI(api_key=OPENAI_API_KEY)
 
st.set_page_config(
    page_title="AI Bartender",
    page_icon="🍸",
    layout="wide"
)
 
# =========================
# HEADER
# =========================
st.title("🍸 AI Bartender – Powered by AB InBev")
st.markdown(
    "Transform your available ingredients into a high-quality drink — "
    "and unlock a tailored AB InBev alternative."
)
 
# =========================
# INPUT
# =========================
col1, col2 = st.columns([3, 1])
 
with col1:
    user_input = st.text_input(
        "Enter ingredients (comma-separated):",
        "vodka, lime, sugar"
    )
 
with col2:
    generate = st.button("Generate Drink")
 
# =========================
# API FUNCTIONS
# =========================
def search_cocktails(ingredient):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"
    return requests.get(url).json().get("drinks", [])
 
def get_details(cocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    return requests.get(url).json()["drinks"][0]
 
def extract_ingredients(cocktail):
    ingredients = []
    for i in range(1, 16):
        ing = cocktail.get(f"strIngredient{i}")
        if ing:
            ingredients.append(ing.lower())
    return ingredients
 
# =========================
# AI FUNCTION (ENGLISH ENFORCED)
# =========================
def generate_ai(prompt):
    full_prompt = f"""
    All outputs MUST be in English.
 
    {prompt}
    """
 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content
 
# =========================
# MAIN LOGIC
# =========================
if generate:
 
    ingredients = [i.strip().lower() for i in user_input.split(",")]
 
    best_match = None
    best_score = 0
 
    # -------------------------
    # MATCHING ENGINE
    # -------------------------
    for ing in ingredients:
        cocktails = search_cocktails(ing)
 
        for c in cocktails[:5]:
            details = get_details(c["idDrink"])
            recipe_ings = extract_ingredients(details)
 
            overlap = len(set(recipe_ings) & set(ingredients)) / len(recipe_ings)
 
            if overlap > best_score:
                best_score = overlap
                best_match = details
 
    # =========================
    # METRICS
    # =========================
    m1, m2, m3 = st.columns(3)
 
    with m1:
        st.metric("Ingredients Provided", len(ingredients))
 
    with m2:
        st.metric("Match Score", f"{round(best_score * 100)}%")
 
    with m3:
        st.metric(
            "Recommendation Type",
            "Classic Recipe" if best_match and best_score > 0.6 else "AI-Generated"
        )
 
    st.divider()
 
    # =========================
    # MAIN RECIPE CARD
    # =========================
    st.markdown("## 🍹 Recommended Drink")
 
    if best_match and best_score > 0.6:
        st.success("Classic cocktail identified")
 
        colA, colB = st.columns([1, 2])
 
        with colA:
            if best_match["strDrinkThumb"]:
                st.image(best_match["strDrinkThumb"])
 
        with colB:
            st.subheader(best_match["strDrink"])
            st.write(best_match["strInstructions"])
 
            st.markdown("**Ingredients:**")
            for i in range(1, 16):
                ing = best_match.get(f"strIngredient{i}")
                measure = best_match.get(f"strMeasure{i}")
                if ing:
                    st.write(f"- {measure} {ing}")
 
        recipe_name = best_match["strDrink"]
 
    else:
        st.warning("No strong match found — generating a new cocktail")
 
        recipe_name = "custom cocktail"
 
        ai_recipe = generate_ai(f"""
        Create a realistic, bar-quality cocktail using these ingredients: {ingredients}.
 
        Keep it simple and credible.
 
        Provide:
        - Drink name
        - Ingredients (with quantities)
        - Instructions
        """)
 
        st.markdown(ai_recipe)
 
    st.divider()
 
    # =========================
    # IMPROVEMENTS CARD
    # =========================
    st.markdown("## 🔧 Improvement Suggestions")
 
    improvements = generate_ai(f"""
    Given this drink: {recipe_name}
 
    Provide 3 concise improvements to enhance balance and overall quality.
    Focus on sweetness, acidity, bitterness, and texture.
    """)
 
    st.info(improvements)
 
    st.divider()
 
    # =========================
    # ABI ALTERNATIVE (HIGHLIGHT)
    # =========================
    st.markdown("## 🍺 AB InBev Alternative")
 
    abi = generate_ai(f"""
    Suggest a variation of this drink using ONE AB InBev brand.
 
    Available brands: Budweiser, Corona, Stella Artois, Beck's.
 
    Provide:
    - New drink name
    - Ingredients
    - Instructions
    - Why this AB InBev product enhances the experience
 
    Keep it realistic and commercially relevant.
    """)
 
    st.success(abi)
