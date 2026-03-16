"""
nutrition_data.py
─────────────────
Standalone calorie + key vitamin reference data per 100g of raw ingredient.
Covers all ingredients in NUTRITION_MAP from detector.py.

Usage:
    from nutrition_data import CALORIE_MAP, VITAMIN_MAP, get_nutrition_detail

Keys match the raw_label / NUTRITION_MAP keys in detector.py exactly.
"""

# ── CALORIES per 100g (kcal) ──────────────────────────────────────────────────
CALORIE_MAP = {
    # Leafy Greens
    "spinach":          23,
    "lettuce":          15,
    "kale":             49,
    "cabbage":          25,
    "bok_choy":         13,
    "fenugreek":        49,
    "methi":            49,

    # Root Vegetables
    "potato":           77,
    "sweet_potato":     86,
    "carrot":           41,
    "beet":             43,
    "turnip":           28,
    "radish":           16,

    # Aromatics
    "ginger":           80,
    "turmeric":        354,   # dried/powder
    "onion":            40,
    "garlic":          149,
    "leek":             61,
    "shallot":          72,
    "spring_onion":     32,

    # Fruiting Vegetables
    "tomato":           18,
    "bell_pepper":      31,
    "red_pepper":       31,
    "green_pepper":     20,
    "yellow_pepper":    27,
    "eggplant":         25,
    "cucumber":         16,
    "zucchini":         17,
    "pumpkin":          26,
    "squash":           16,
    "bitter_gourd":     17,
    "bottle_gourd":     14,
    "okra":             33,
    "corn":             86,
    "chilli":           40,
    "green_chilli":     40,

    # Cruciferous
    "broccoli":         34,
    "cauliflower":      25,
    "brussels_sprouts": 43,

    # Mushrooms
    "mushroom":         22,
    "shiitake":         34,

    # Legumes & Pulses
    "green_beans":      31,
    "peas":             81,
    "chickpeas":       164,
    "lentils":         116,
    "moong_dal":       347,   # dry
    "toor_dal":        343,   # dry

    # Fruits
    "mango":            60,
    "lemon":            29,
    "lime":             30,
    "orange":           47,
    "coconut":         354,
    "banana":           89,
    "avocado":         160,
    "apple":            52,
    "pomegranate":      83,
    "guava":            68,
    "jackfruit":        95,
    "strawberry":       32,
    "watermelon":       30,

    # Herbs
    "coriander":        23,
    "mint":             70,
    "basil":            23,

    # Nuts & Seeds
    "cashew":          553,
    "almond":          579,
    "peanut":          567,
    "sesame":          573,

    # Protein & Dairy
    "egg":             155,
    "paneer":          265,
    "tofu":             76,
    "yogurt":           61,
    "ghee":            900,
}


# ── KEY VITAMINS & MINERALS per ingredient ─────────────────────────────────────
# Format: { ingredient: { vitamin_or_mineral: "amount or description" } }
VITAMIN_MAP = {
    "spinach":     {"Vitamin K": "483µg", "Vitamin C": "28mg", "Iron": "2.7mg",    "Folate": "194µg", "Magnesium": "79mg"},
    "lettuce":     {"Vitamin K": "102µg", "Vitamin A": "370µg","Folate": "38µg",   "Vitamin C": "3.7mg"},
    "kale":        {"Vitamin K": "817µg", "Vitamin C": "120mg","Vitamin A": "500µg","Calcium": "150mg", "Iron": "1.5mg"},
    "cabbage":     {"Vitamin C": "36mg",  "Vitamin K": "76µg", "Folate": "43µg",   "Fiber": "2.5g"},
    "bok_choy":    {"Vitamin A": "223µg", "Vitamin C": "45mg", "Calcium": "105mg", "Vitamin K": "45µg"},
    "fenugreek":   {"Iron": "33mg",       "Vitamin C": "3mg",  "Folate": "57µg",   "Protein": "23g"},
    "methi":       {"Iron": "33mg",       "Vitamin C": "3mg",  "Folate": "57µg"},

    "potato":      {"Vitamin C": "19mg",  "Potassium": "425mg","Vitamin B6": "0.3mg","Fiber": "2.2g"},
    "sweet_potato":{"Vitamin A": "961µg", "Vitamin C": "2.4mg","Potassium": "337mg","Fiber": "3g"},
    "carrot":      {"Vitamin A": "835µg", "Vitamin K": "13µg", "Potassium": "320mg","Fiber": "2.8g"},
    "beet":        {"Folate": "109µg",    "Manganese": "0.3mg","Nitrates": "high",  "Vitamin C": "4.9mg"},
    "turnip":      {"Vitamin C": "21mg",  "Vitamin K": "0.1µg","Calcium": "30mg",  "Fiber": "1.8g"},
    "radish":      {"Vitamin C": "14.8mg","Folate": "25µg",    "Fiber": "1.6g"},

    "ginger":      {"Vitamin B6": "0.16mg","Magnesium": "43mg","Potassium": "415mg","Gingerol": "active"},
    "turmeric":    {"Curcumin": "active",  "Iron": "41mg",     "Manganese": "7.8mg","Vitamin B6": "1.8mg"},
    "onion":       {"Vitamin C": "7.4mg",  "Folate": "19µg",   "Potassium": "146mg","Quercetin": "active"},
    "garlic":      {"Vitamin C": "31mg",   "Vitamin B6": "1.2mg","Manganese": "1.7mg","Allicin": "active"},
    "leek":        {"Vitamin K": "47µg",   "Folate": "64µg",   "Manganese": "0.2mg","Vitamin C": "12mg"},
    "shallot":     {"Vitamin B6": "0.3mg", "Manganese": "0.3mg","Folate": "34µg",   "Vitamin C": "8mg"},
    "spring_onion":{"Vitamin K": "207µg",  "Vitamin C": "18.8mg","Folate": "64µg",  "Fiber": "2.6g"},

    "tomato":      {"Lycopene": "2573µg",  "Vitamin C": "14mg", "Potassium": "237mg","Vitamin K": "7.9µg"},
    "bell_pepper": {"Vitamin C": "128mg",  "Vitamin A": "157µg","Vitamin B6": "0.3mg","Folate": "46µg"},
    "red_pepper":  {"Vitamin C": "128mg",  "Vitamin A": "157µg","Capsaicin": "active"},
    "green_pepper":{"Vitamin C": "80mg",   "Vitamin B6": "0.3mg","Folate": "10µg"},
    "yellow_pepper":{"Vitamin C": "184mg", "Lutein": "high",    "Zeaxanthin": "high"},
    "eggplant":    {"Fiber": "3g",         "Vitamin B1": "0.08mg","Manganese": "0.2mg","Nasunin": "active"},
    "cucumber":    {"Vitamin K": "16µg",   "Potassium": "147mg","Water": "96%",      "Vitamin C": "2.8mg"},
    "zucchini":    {"Vitamin C": "17.9mg", "Vitamin B6": "0.2mg","Potassium": "261mg","Manganese": "0.2mg"},
    "pumpkin":     {"Vitamin A": "426µg",  "Vitamin C": "9mg",  "Potassium": "340mg","Fiber": "0.5g"},
    "squash":      {"Vitamin A": "532µg",  "Vitamin C": "12mg", "Folate": "29µg",   "Magnesium": "14mg"},
    "bitter_gourd":{"Vitamin C": "84mg",   "Folate": "72µg",    "Zinc": "0.8mg",    "Iron": "0.4mg"},
    "bottle_gourd":{"Vitamin C": "10mg",   "Iron": "0.2mg",     "Water": "96%"},
    "okra":        {"Vitamin C": "23mg",   "Vitamin K": "31µg", "Folate": "60µg",   "Fiber": "3.2g"},
    "corn":        {"Vitamin B1": "0.2mg", "Folate": "42µg",    "Lutein": "high",   "Fiber": "2.4g"},
    "chilli":      {"Vitamin C": "143mg",  "Capsaicin": "active","Vitamin A": "48µg"},
    "green_chilli":{"Vitamin C": "242mg",  "Capsaicin": "active","Vitamin K": "14µg"},

    "broccoli":    {"Vitamin C": "89mg",   "Vitamin K": "102µg","Folate": "63µg",   "Sulforaphane": "active","Fiber": "2.6g"},
    "cauliflower": {"Vitamin C": "48mg",   "Vitamin K": "16µg", "Folate": "57µg",   "Choline": "44mg"},
    "brussels_sprouts":{"Vitamin C": "85mg","Vitamin K": "177µg","Folate": "61µg",  "Fiber": "3.8g"},

    "mushroom":    {"Vitamin D": "7µg",    "Vitamin B2": "0.3mg","Selenium": "9.3µg","Potassium": "318mg"},
    "shiitake":    {"Vitamin D": "18µg",   "Vitamin B12": "trace","Lentinan": "active","Selenium": "5.7µg"},

    "green_beans": {"Vitamin K": "43µg",   "Vitamin C": "12.2mg","Folate": "33µg",  "Silicon": "active"},
    "peas":        {"Vitamin K": "25µg",   "Vitamin C": "40mg", "Folate": "65µg",   "Protein": "5g"},
    "chickpeas":   {"Protein": "19g",      "Iron": "6.2mg",     "Folate": "557µg",  "Fiber": "17g"},
    "lentils":     {"Protein": "9g",       "Iron": "3.3mg",     "Folate": "181µg",  "Fiber": "7.9g"},
    "moong_dal":   {"Protein": "24g",      "Iron": "6.7mg",     "Vitamin B1": "0.6mg","Fiber": "16g"},
    "toor_dal":    {"Protein": "22g",      "Iron": "5.2mg",     "Vitamin B complex": "present","Fiber": "15g"},

    "mango":       {"Vitamin A": "54µg",   "Vitamin C": "36mg", "Folate": "43µg",   "Fiber": "1.6g"},
    "lemon":       {"Vitamin C": "53mg",   "Citric acid": "active","Potassium": "138mg"},
    "lime":        {"Vitamin C": "29mg",   "Potassium": "102mg","Folate": "8µg"},
    "orange":      {"Vitamin C": "53mg",   "Folate": "30µg",   "Potassium": "181mg","Flavonoids": "active"},
    "coconut":     {"Manganese": "1.5mg",  "MCTs": "active",   "Fiber": "9g",      "Lauric acid": "active"},
    "banana":      {"Potassium": "358mg",  "Vitamin B6": "0.4mg","Vitamin C": "8.7mg","Fiber": "2.6g"},
    "avocado":     {"Vitamin K": "21µg",   "Folate": "81µg",   "Potassium": "485mg","Oleic acid": "active"},
    "apple":       {"Vitamin C": "4.6mg",  "Potassium": "107mg","Fiber": "2.4g",    "Quercetin": "active"},
    "pomegranate": {"Vitamin C": "10.2mg", "Vitamin K": "16µg","Folate": "38µg",   "Punicalagins": "active"},
    "guava":       {"Vitamin C": "228mg",  "Lycopene": "5200µg","Fiber": "5.4g",   "Vitamin A": "31µg"},
    "jackfruit":   {"Vitamin C": "13.7mg", "Potassium": "303mg","Vitamin A": "5µg", "Fiber": "1.5g"},
    "strawberry":  {"Vitamin C": "58.8mg", "Folate": "24µg",   "Potassium": "153mg","Fiber": "2g"},
    "watermelon":  {"Vitamin C": "8.1mg",  "Lycopene": "4532µg","Potassium": "112mg","Water": "92%"},

    "coriander":   {"Vitamin K": "310µg",  "Vitamin C": "27mg","Potassium": "521mg"},
    "mint":        {"Vitamin A": "212µg",  "Iron": "3.75mg",   "Manganese": "1.2mg","Menthol": "active"},
    "basil":       {"Vitamin K": "415µg",  "Vitamin A": "264µg","Iron": "3.2mg",    "Eugenol": "active"},

    "cashew":      {"Copper": "2.2mg",     "Magnesium": "292mg","Zinc": "5.8mg",    "Healthy fats": "44g"},
    "almond":      {"Vitamin E": "25.6mg", "Magnesium": "270mg","Protein": "21g",   "Healthy fats": "50g"},
    "peanut":      {"Vitamin E": "8.3mg",  "Niacin": "12mg",   "Protein": "26g",   "Healthy fats": "49g"},
    "sesame":      {"Calcium": "975mg",    "Vitamin E": "0.25mg","Lignans": "active","Healthy fats": "50g"},

    "egg":         {"Vitamin D": "2µg",    "Vitamin B12": "0.9µg","Choline": "294mg","Protein": "13g"},
    "paneer":      {"Calcium": "480mg",    "Protein": "18g",   "Vitamin B12": "0.5µg","Healthy fats": "22g"},
    "tofu":        {"Calcium": "350mg",    "Iron": "5.4mg",    "Protein": "8g",    "Isoflavones": "active"},
    "yogurt":      {"Calcium": "110mg",    "Vitamin B12": "0.4µg","Probiotics": "active","Protein": "10g"},
    "ghee":        {"Vitamin A": "3069µg", "Vitamin E": "2.8mg","Vitamin K": "8.6µg","Butyrate": "active"},
}


# ── HELPER FUNCTION ────────────────────────────────────────────────────────────

def get_nutrition_detail(ingredient_label: str) -> dict:
    """
    Returns a structured nutrition detail dict for a given ingredient raw_label.
    Returns empty placeholders if ingredient is not found.

    Args:
        ingredient_label: raw_label string e.g. "spinach", "bell_pepper"

    Returns:
        {
            "calories_per_100g": int | None,
            "key_vitamins": dict,          # { "Vitamin C": "28mg", ... }
            "has_data": bool
        }
    """
    label = ingredient_label.lower().strip()
    cal = CALORIE_MAP.get(label)
    vit = VITAMIN_MAP.get(label, {})

    return {
        "calories_per_100g": cal,
        "key_vitamins": vit,
        "has_data": cal is not None or bool(vit),
    }


def get_nutrition_for_ingredients(labels: list) -> dict:
    """
    Batch lookup for a list of ingredient raw_labels (as returned by detector.py).

    Args:
        labels: list of raw_label strings e.g. ["spinach", "tomato", "potato"]

    Returns:
        {
            "per_ingredient": {
                "spinach": { "calories_per_100g": 23, "key_vitamins": {...} },
                ...
            },
            "total_calories_estimate": int,   # sum of all per-100g values (rough estimate)
            "combined_vitamins": {             # union of all vitamins detected
                "Vitamin C": ["spinach", "tomato"],
                ...
            }
        }
    """
    per_ingredient = {}
    total_cal = 0
    combined_vitamins: dict = {}

    for label in labels:
        detail = get_nutrition_detail(label)
        per_ingredient[label] = detail

        if detail["calories_per_100g"]:
            total_cal += detail["calories_per_100g"]

        for vit_name in detail["key_vitamins"]:
            if vit_name not in combined_vitamins:
                combined_vitamins[vit_name] = []
            combined_vitamins[vit_name].append(label)

    return {
        "per_ingredient": per_ingredient,
        "total_calories_estimate": total_cal,
        "combined_vitamins": combined_vitamins,
    }
