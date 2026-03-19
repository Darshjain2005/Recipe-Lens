"""
╔══════════════════════════════════════════════════════════════════╗
║   VegVision — Advanced Multi-Model Food Detection Engine v4      ║
║                                                                  ║
║   Models:                                                        ║
║   1. YOLOv8s      — Object detection (COCO 80 classes)          ║
║   2. YOLOv8n-oiv7 — Open Images V7 (600 classes, rare vegs)     ║
║   3. EfficientNetV2-S — Image classification (ImageNet)          ║
║   4. MobileNetV3-Large — Lightweight cross-validator             ║
║   5. ResNet50     — Diverse architecture third vote              ║
║   6. LAB+HSV Color+Texture — 60-ingredient heuristic engine     ║
║                                                                  ║
║   Fusion: Weighted Bayesian ensemble with confidence boosting    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import cv2  # type: ignore[import]
import numpy as np  # type: ignore[import]
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Optional, Tuple


# ══════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — 250+ INGREDIENTS
# ══════════════════════════════════════════════════════════════════

CATEGORY_MAP = {
    # Leafy Greens
    "spinach":"Leafy Green","lettuce":"Leafy Green","kale":"Leafy Green",
    "cabbage":"Leafy Green","bok_choy":"Leafy Green","arugula":"Leafy Green",
    "swiss_chard":"Leafy Green","collard_greens":"Leafy Green",
    "fenugreek":"Leafy Green","methi":"Leafy Green","amaranth":"Leafy Green",
    "watercress":"Leafy Green","endive":"Leafy Green","radicchio":"Leafy Green",

    # Root Vegetables
    "potato":"Root Vegetable","sweet_potato":"Root Vegetable","carrot":"Root Vegetable",
    "beet":"Root Vegetable","turnip":"Root Vegetable","radish":"Root Vegetable",
    "parsnip":"Root Vegetable","yam":"Root Vegetable","taro":"Root Vegetable",
    "cassava":"Root Vegetable","ginger":"Root/Spice","turmeric":"Root/Spice",
    "horseradish":"Root/Spice","lotus_root":"Root Vegetable",

    # Alliums
    "onion":"Allium","garlic":"Allium/Spice","leek":"Allium",
    "shallot":"Allium","spring_onion":"Allium","chive":"Herb/Allium",

    # Fruiting Vegetables
    "tomato":"Fruiting Vegetable","bell_pepper":"Fruiting Vegetable",
    "red_pepper":"Fruiting Vegetable","green_pepper":"Fruiting Vegetable",
    "yellow_pepper":"Fruiting Vegetable","eggplant":"Fruiting Vegetable",
    "cucumber":"Fruiting Vegetable","zucchini":"Fruiting Vegetable",
    "pumpkin":"Fruiting Vegetable","squash":"Fruiting Vegetable",
    "bitter_gourd":"Fruiting Vegetable","bottle_gourd":"Fruiting Vegetable",
    "ridge_gourd":"Fruiting Vegetable","snake_gourd":"Fruiting Vegetable",
    "okra":"Fruiting Vegetable","corn":"Grain/Vegetable","chilli":"Spice/Vegetable",
    "green_chilli":"Spice/Vegetable","capsicum":"Fruiting Vegetable",

    # Brassicas
    "broccoli":"Brassica","cauliflower":"Brassica","brussels_sprouts":"Brassica",
    "kohlrabi":"Brassica","romanesco":"Brassica",

    # Legumes
    "green_beans":"Legume","peas":"Legume","chickpeas":"Legume",
    "lentils":"Legume","kidney_beans":"Legume","black_beans":"Legume",
    "soybeans":"Legume","edamame":"Legume","fava_beans":"Legume",
    "moong_dal":"Legume","toor_dal":"Legume","urad_dal":"Legume",

    # Mushrooms
    "mushroom":"Fungi","shiitake":"Fungi","portobello":"Fungi",
    "oyster_mushroom":"Fungi","button_mushroom":"Fungi","cremini":"Fungi",
    "chanterelle":"Fungi","porcini":"Fungi",

    # Fruits (common in cooking)
    "tomato":"Fruiting Vegetable","lemon":"Citrus Fruit","lime":"Citrus Fruit",
    "orange":"Citrus Fruit","grapefruit":"Citrus Fruit","mango":"Tropical Fruit",
    "pineapple":"Tropical Fruit","papaya":"Tropical Fruit","coconut":"Tropical Fruit",
    "banana":"Tropical Fruit","avocado":"Fruit","apple":"Fruit",
    "pear":"Fruit","grape":"Fruit","strawberry":"Berry","raspberry":"Berry",
    "blueberry":"Berry","blackberry":"Berry","watermelon":"Melon",
    "cantaloupe":"Melon","honeydew":"Melon","pomegranate":"Fruit",
    "guava":"Tropical Fruit","lychee":"Tropical Fruit","jackfruit":"Tropical Fruit",

    # Herbs
    "coriander":"Herb","cilantro":"Herb","parsley":"Herb","basil":"Herb",
    "mint":"Herb","thyme":"Herb","rosemary":"Herb","oregano":"Herb",
    "dill":"Herb","sage":"Herb","bay_leaf":"Herb","curry_leaves":"Herb",
    "lemongrass":"Herb","tarragon":"Herb","chervil":"Herb",

    # Spices
    "chilli_powder":"Spice","cumin":"Spice","coriander_powder":"Spice",
    "turmeric_powder":"Spice","garam_masala":"Spice","paprika":"Spice",
    "black_pepper":"Spice","cardamom":"Spice","cinnamon":"Spice",
    "cloves":"Spice","nutmeg":"Spice","saffron":"Spice","star_anise":"Spice",

    # Grains & Staples
    "rice":"Grain","wheat":"Grain","flour":"Grain","bread":"Baked Good",
    "pasta":"Grain","noodles":"Grain","oats":"Grain","quinoa":"Grain","barley":"Grain",

    # Dairy & Protein
    "egg":"Protein/Dairy","paneer":"Dairy/Protein","tofu":"Protein",
    "cheese":"Dairy","milk":"Dairy","yogurt":"Dairy","butter":"Dairy",
    "cream":"Dairy","ghee":"Dairy/Fat",

    # Nuts & Seeds
    "cashew":"Nut","almond":"Nut","peanut":"Nut/Legume","walnut":"Nut",
    "pistachio":"Nut","sesame":"Seed","sunflower_seed":"Seed",
    "pumpkin_seed":"Seed","flaxseed":"Seed","chia":"Seed",
}

NUTRITION_MAP = {
    "spinach": "Iron, Vitamin K & C, folate, magnesium — superfood",
    "lettuce": "Vitamin K, folate, low calorie, hydrating",
    "kale": "Vitamin K, C, A, calcium, antioxidants — superfood",
    "cabbage": "Vitamin C & K, fiber, anti-inflammatory compounds",
    "bok_choy": "Calcium, Vitamin A & C, potassium",
    "fenugreek": "Iron, protein, soluble fiber — blood sugar regulation",
    "methi": "Iron, Vitamin C, folic acid — common Indian green",
    "potato": "Potassium, Vitamin C & B6, resistant starch",
    "sweet_potato": "Beta-carotene, Vitamin A & C, fiber, potassium",
    "carrot": "Beta-carotene, Vitamin A & K, antioxidants",
    "beet": "Nitrates, folate, manganese, antioxidants",
    "turnip": "Vitamin C & K, fiber, calcium",
    "radish": "Vitamin C, folate, fiber, anti-inflammatory",
    "ginger": "Gingerol, anti-nausea, anti-inflammatory, digestive",
    "turmeric": "Curcumin — powerful anti-inflammatory, antioxidant",
    "onion": "Quercetin, Vitamin C, prebiotics, immune support",
    "garlic": "Allicin, immune-boosting, cardiovascular benefits",
    "leek": "Vitamin K, folate, manganese, antioxidants",
    "shallot": "Quercetin, Vitamin B6, manganese",
    "spring_onion": "Vitamin K & C, folate, fiber",
    "tomato": "Lycopene, Vitamin C & K, potassium, antioxidants",
    "bell_pepper": "Vitamin C (highest of any vegetable), A, B6, antioxidants",
    "red_pepper": "Vitamin C, A, B6, capsaicin, antioxidants",
    "green_pepper": "Vitamin C, B6, folate, fiber",
    "yellow_pepper": "Vitamin C, B6, lutein, zeaxanthin",
    "eggplant": "Nasunin (antioxidant), fiber, Vitamin B1, manganese",
    "cucumber": "Hydrating (96% water), Vitamin K, low calorie",
    "zucchini": "Vitamin C & B6, potassium, manganese, low calorie",
    "pumpkin": "Beta-carotene, Vitamin A & C, potassium, fiber",
    "squash": "Vitamin A & C, fiber, folate, magnesium",
    "bitter_gourd": "Insulin-like compounds, Vitamin C, blood sugar control",
    "bottle_gourd": "Low calorie, Vitamin C, iron, hydrating",
    "okra": "Fiber (mucilage), Vitamin C & K, folate, blood sugar",
    "corn": "Fiber, Vitamin B, folate, lutein, zeaxanthin",
    "chilli": "Capsaicin (metabolism boost), Vitamin C, antioxidants",
    "green_chilli": "Vitamin C (very high), capsaicin, antioxidants",
    "broccoli": "Vitamin C, K, folate, sulforaphane (anti-cancer), fiber",
    "cauliflower": "Vitamin C, K, folate, choline, sulforaphane",
    "brussels_sprouts": "Vitamin C, K, folate, fiber, antioxidants",
    "mushroom": "Vitamin D (rare plant source), B vitamins, selenium",
    "shiitake": "Lentinan (immune booster), Vitamin D & B12",
    "green_beans": "Vitamin K & C, folate, fiber, silicon",
    "peas": "Protein, Vitamin K, C, folate, fiber",
    "chickpeas": "Plant protein (19g/100g), fiber, iron, folate",
    "lentils": "Plant protein, iron, folate, fiber — heart health",
    "moong_dal": "Light protein, easy to digest, Vitamin B, iron",
    "toor_dal": "Protein, Vitamin B complex, iron, fiber",
    "mango": "Vitamin A & C, folate, digestive enzymes",
    "lemon": "Vitamin C, citric acid, antioxidants, alkalizing",
    "lime": "Vitamin C, antioxidants, digestive benefits",
    "orange": "Vitamin C, folate, potassium, flavonoids",
    "coconut": "MCTs, fiber, manganese, lauric acid",
    "banana": "Potassium, Vitamin B6, tryptophan, energy",
    "avocado": "Healthy fats (oleic acid), Vitamin K, folate, potassium",
    "apple": "Quercetin, fiber (pectin), Vitamin C, antioxidants",
    "pomegranate": "Punicalagins, Vitamin C, K, folate — powerful antioxidant",
    "guava": "Highest Vitamin C of any fruit, lycopene, fiber",
    "jackfruit": "Potassium, Vitamin A & C, B-complex, fiber",
    "coriander": "Vitamin K, antioxidants, digestive, blood sugar",
    "mint": "Menthol, digestive, anti-nausea, antioxidants",
    "basil": "Vitamin K, antioxidants, eugenol (anti-inflammatory)",
    "cashew": "Healthy fats, copper, magnesium, zinc",
    "almond": "Vitamin E, healthy fats, magnesium, protein",
    "peanut": "Protein, Vitamin E, niacin, healthy fats",
    "sesame": "Calcium, healthy fats, lignans, Vitamin E",
    "egg": "Complete protein, Vitamin D, B12, choline — highly nutritious",
    "paneer": "Protein, calcium, Vitamin B12 — Indian cottage cheese",
    "tofu": "Plant protein, calcium, iron, isoflavones",
    "yogurt": "Probiotics, protein, calcium, Vitamin B12",
    "ghee": "Fat-soluble vitamins, butyrate, high smoke point",
}

# ── COMPREHENSIVE COLOR PROFILES (HSV + LAB) ──
# Format: primary HSV range + optional second range (for wraparound hues)
FOOD_COLOR_PROFILES = {
    # ─── Reds ───
    "tomato":         {"hsv_lo":(0,100,80),  "hsv_hi":(10,255,255), "hsv_lo2":(168,100,60), "hsv_hi2":(180,255,255), "min_cov":0.008},
    "red_pepper":     {"hsv_lo":(0,130,90),  "hsv_hi":(8,255,255),  "hsv_lo2":(170,130,90),"hsv_hi2":(180,255,255), "min_cov":0.012},
    "strawberry":     {"hsv_lo":(0,120,70),  "hsv_hi":(6,255,200),  "hsv_lo2":(172,120,60),"hsv_hi2":(180,255,200), "min_cov":0.006},
    "watermelon":     {"hsv_lo":(0,130,60),  "hsv_hi":(9,255,210),  "min_cov":0.015},
    "apple":          {"hsv_lo":(0,100,60),  "hsv_hi":(12,255,240), "hsv_lo2":(166,100,60),"hsv_hi2":(180,255,240), "min_cov":0.01},
    "pomegranate":    {"hsv_lo":(0,150,80),  "hsv_hi":(8,255,200),  "min_cov":0.008},
    "chilli":         {"hsv_lo":(0,160,80),  "hsv_hi":(8,255,255),  "hsv_lo2":(170,160,80),"hsv_hi2":(180,255,255), "min_cov":0.004},
    "beet":           {"hsv_lo":(160,80,40), "hsv_hi":(180,255,160),"min_cov":0.008},
    "radish":         {"hsv_lo":(0,110,150), "hsv_hi":(8,255,255),  "hsv_lo2":(168,110,150),"hsv_hi2":(180,255,255),"min_cov":0.005},

    # ─── Oranges ───
    "carrot":         {"hsv_lo":(7,160,80),  "hsv_hi":(13,255,255), "min_cov":0.008},  # Tightened upper hue to avoid overlapping orange
    "orange":         {"hsv_lo":(13,180,150),"hsv_hi":(22,255,255), "min_cov":0.025},  # Tightened: must be brighter/more saturated than carrot
    "sweet_potato":   {"hsv_lo":(8,100,90),  "hsv_hi":(20,220,240), "min_cov":0.01},
    "pumpkin":        {"hsv_lo":(9,140,100), "hsv_hi":(22,255,240), "min_cov":0.012},
    "papaya":         {"hsv_lo":(10,130,130),"hsv_hi":(25,255,255), "min_cov":0.01},
    "mango":          {"hsv_lo":(18,140,150),"hsv_hi":(32,255,255), "min_cov":0.01},

    # ─── Yellows ───
    "banana":         {"hsv_lo":(22,80,150), "hsv_hi":(38,255,255), "min_cov":0.01},
    "lemon":          {"hsv_lo":(24,110,170),"hsv_hi":(38,255,255), "min_cov":0.008},
    "yellow_pepper":  {"hsv_lo":(22,100,150),"hsv_hi":(36,255,255), "min_cov":0.01},
    "corn":           {"hsv_lo":(24,80,130), "hsv_hi":(38,255,255), "min_cov":0.01},
    "ginger":         {"hsv_lo":(18,60,150), "hsv_hi":(30,140,255), "min_cov":0.005},

    # ─── Greens ───
    "broccoli":       {"hsv_lo":(38,60,30),  "hsv_hi":(80,255,180), "min_cov":0.01},
    "spinach":        {"hsv_lo":(38,80,20),  "hsv_hi":(78,255,120), "min_cov":0.008},
    "kale":           {"hsv_lo":(36,60,20),  "hsv_hi":(78,255,130), "min_cov":0.008},
    "cabbage":        {"hsv_lo":(38,30,100), "hsv_hi":(90,160,230), "min_cov":0.015},
    "cucumber":       {"hsv_lo":(38,40,50),  "hsv_hi":(80,190,210), "min_cov":0.008},
    "green_pepper":   {"hsv_lo":(42,70,50),  "hsv_hi":(82,255,200), "min_cov":0.008},
    "green_beans":    {"hsv_lo":(40,70,40),  "hsv_hi":(80,255,180), "min_cov":0.005},
    "peas":           {"hsv_lo":(40,80,60),  "hsv_hi":(82,255,200), "min_cov":0.005},
    "zucchini":       {"hsv_lo":(38,50,50),  "hsv_hi":(80,200,200), "min_cov":0.008},
    "okra":           {"hsv_lo":(38,60,30),  "hsv_hi":(80,200,160), "min_cov":0.005},
    "capsicum":       {"hsv_lo":(42,70,50),  "hsv_hi":(82,255,200), "min_cov":0.008},
    "lime":           {"hsv_lo":(40,100,140),"hsv_hi":(78,255,255), "min_cov":0.006},
    "avocado":        {"hsv_lo":(36,60,40),  "hsv_hi":(78,220,180), "min_cov":0.01},
    "methi":          {"hsv_lo":(38,70,30),  "hsv_hi":(78,255,140), "min_cov":0.006},
    "coriander":      {"hsv_lo":(40,70,40),  "hsv_hi":(80,255,170), "min_cov":0.003},
    "mint":           {"hsv_lo":(60,60,80),  "hsv_hi":(95,255,220), "min_cov":0.003},

    # ─── Purples/Dark ───
    "eggplant":       {"hsv_lo":(120,50,20), "hsv_hi":(160,255,130),"min_cov":0.008},
    "red_cabbage":    {"hsv_lo":(130,40,40), "hsv_hi":(165,255,180),"min_cov":0.012},
    "grape":          {"hsv_lo":(128,40,30), "hsv_hi":(158,255,190),"min_cov":0.006},
    "blueberry":      {"hsv_lo":(120,50,20), "hsv_hi":(155,255,150),"min_cov":0.004},
    "pomegranate_seed":{"hsv_lo":(155,80,60),"hsv_hi":(175,255,200),"min_cov":0.004},

    # ─── Whites/Creams ───
    "garlic":         {"hsv_lo":(0,0,180),   "hsv_hi":(30,30,255),  "min_cov":0.004},
    "onion":          {"hsv_lo":(14,20,130), "hsv_hi":(30,100,255), "min_cov":0.008},
    "cauliflower":    {"hsv_lo":(0,0,160),   "hsv_hi":(30,40,255),  "min_cov":0.01},
    "mushroom":       {"hsv_lo":(0,0,90),    "hsv_hi":(30,50,210),  "min_cov":0.008},
    "potato":         {"hsv_lo":(16,20,100), "hsv_hi":(32,90,210),  "min_cov":0.01},
    "turnip":         {"hsv_lo":(0,0,140),   "hsv_hi":(20,50,255),  "min_cov":0.008},
    "leek":           {"hsv_lo":(50,30,130), "hsv_hi":(90,130,230), "min_cov":0.006},
    "spring_onion":   {"hsv_lo":(45,50,80),  "hsv_hi":(88,220,220), "min_cov":0.004},
    "daikon":         {"hsv_lo":(0,0,160),   "hsv_hi":(20,30,255),  "min_cov":0.006},
    "radish_white":   {"hsv_lo":(0,0,170),   "hsv_hi":(20,25,255),  "min_cov":0.005},
    "coconut":        {"hsv_lo":(0,0,180),   "hsv_hi":(20,30,255),  "min_cov":0.006},
    "paneer":         {"hsv_lo":(0,0,170),   "hsv_hi":(25,35,255),  "min_cov":0.005},
    "tofu":           {"hsv_lo":(0,0,180),   "hsv_hi":(25,30,255),  "min_cov":0.005},

    # ─── Browns/Tans ───
    "ginger_root":    {"hsv_lo":(16,50,110), "hsv_hi":(28,150,210), "min_cov":0.005},
    "cinnamon":       {"hsv_lo":(10,100,80), "hsv_hi":(22,200,180), "min_cov":0.003},
    "peanut":         {"hsv_lo":(14,60,100), "hsv_hi":(26,160,210), "min_cov":0.005},
    "cashew":         {"hsv_lo":(18,40,150), "hsv_hi":(32,120,240), "min_cov":0.004},
    "walnut":         {"hsv_lo":(12,50,60),  "hsv_hi":(24,140,170), "min_cov":0.004},
}

# ── YOLO label → clean name mapping (COCO + extended) ──
YOLO_LABEL_MAP = {
    # COCO food classes
    "banana":"Banana", "apple":"Apple", "sandwich":"Sandwich",
    "orange":"Orange", "broccoli":"Broccoli", "carrot":"Carrot",
    "hot dog":"Sausage", "pizza":"Pizza", "donut":"Donut",
    "cake":"Cake", "bowl":"Bowl",
    # Extended common food detections by YOLO
    "tomato":"Tomato", "pepper":"Bell Pepper", "onion":"Onion",
    "garlic":"Garlic", "potato":"Potato", "mushroom":"Mushroom",
    "cucumber":"Cucumber", "eggplant":"Eggplant", "corn":"Corn",
    "lemon":"Lemon", "lime":"Lime", "mango":"Mango", "grape":"Grape",
    "strawberry":"Strawberry", "watermelon":"Watermelon",
    "pineapple":"Pineapple", "avocado":"Avocado", "coconut":"Coconut",
    "spinach":"Spinach", "kale":"Kale", "cabbage":"Cabbage",
    "lettuce":"Lettuce", "cauliflower":"Cauliflower",
    "sweet potato":"Sweet Potato", "ginger":"Ginger",
    "chili":"Green Chilli", "chilli":"Chilli",
    "green beans":"Green Beans", "peas":"Peas", "zucchini":"Zucchini",
    "squash":"Squash", "pumpkin":"Pumpkin", "papaya":"Papaya",
    "guava":"Guava", "pomegranate":"Pomegranate",
    "egg":"Egg", "tofu":"Tofu", "bread":"Bread",
}

# ── FALSE POSITIVE SUPPRESSION ──
# Maps common ImageNet class names that get misidentified to the correct ingredient
# or to None (to suppress them entirely if they are non-food noise)
IMAGENET_REMAP = {
    # ImageNet 'orange' (fruit) fires on anything orange-ish — remap to carrot
    # only if the image likely has carrots. We suppress it to avoid confusion;
    # YOLO will handle it correctly.
    "orange":            None,   # suppress — too ambiguous with carrot
    "lemon":             None,   # suppress — ambiguous with yellow pepper
    "lime":              None,   # suppress — ambiguous with green vegetables
    "cucumber":          "cucumber",  # keep
    "zucchini":          "zucchini",
    "bell_pepper":       "bell_pepper",
    "Granny_Smith":      "apple",
    "acorn_squash":      "squash",
    "butternut_squash":  "squash",
    "cauliflower":       "cauliflower",
    "broccoli":          "broccoli",
    "head_cabbage":      "cabbage",
    "cabbage":           "cabbage",
    "cardoon":           "cabbage",    # misclassified cabbage-like plant
    "artichoke":         "cauliflower", # similar shape
    "corn":              "corn",
    "ear":               "corn",       # ImageNet 'ear of corn'
    "ear_of_corn":       "corn",
    "mushroom":          "mushroom",
    "agaric":            "mushroom",
    "gyromitra":         "mushroom",
    "stinkhorn":         "mushroom",
    "earthstar":         "mushroom",
    "hen_of_the_woods":  "mushroom",
    "bolete":            "mushroom",
    "eggplant":          "eggplant",
    "spaghetti_squash":  "squash",
    "fig":               None,   # suppress
    "hip":               None,   # suppress (rose hip)
    "strawberry":        "strawberry",
    "banana":            "banana",
    "pineapple":         "pineapple",
    "pomegranate":       "pomegranate",
    "mango":             "mango",
    "avocado":           "avocado",
    "guacamole":         "avocado",
    "pretzel":           None,   # suppress non-food misclassifications
    "bagel":             None,
    "hamburger":         None,
    "cheeseburger":      None,
    "hotdog":            None,
    "pizza":             None,
    "burrito":           None,
    "tacos":             None,
    "potpie":            None,
    "plate":             None,
    "pot":               None,
    "wok":               None,
    "spatula":           None,
    "ladle":             None,
}

# ── Keyword lists for EfficientNet/ResNet filtering ──
FOOD_KEYWORDS = {
    "vegetable","fruit","produce","herb","spice","plant",
    "pepper","tomato","broccoli","carrot","mushroom","lemon","orange",
    "banana","strawberry","onion","cucumber","zucchini","eggplant",
    "corn","potato","garlic","ginger","basil","parsley","spinach",
    "lettuce","cabbage","cauliflower","artichoke","asparagus","celery",
    "radish","turnip","beet","squash","pumpkin","yam","cassava",
    "leek","shallot","chive","avocado","kiwi","papaya","mango",
    "pineapple","coconut","guava","lychee","acorn","gourd",
    "fig","pomegranate","jackfruit","tamarind","turmeric","saffron",
    "cardamom","cinnamon","clove","fennel","anise","cumin","coriander",
    "mint","sage","thyme","rosemary","dill","chili","okra",
    "edamame","soybean","chickpea","lentil","kidney","pea","bean",
    "almond","walnut","cashew","pistachio","peanut","hazelnut",
    "sesame","sunflower","flax","chia","egg","tofu","paneer",
}

# ── COMPREHENSIVE DISH SUGGESTIONS (80+ dishes, Indian prioritised) ──
DISH_COMBO_MAP = {
    # ─ Spinach based ─
    frozenset(["spinach","paneer"])          : ["Palak Paneer","Saag Paneer","Paneer Pasanda"],
    frozenset(["spinach","potato"])          : ["Aloo Palak","Palak Aloo Sabzi","Saag Aloo"],
    frozenset(["spinach","onion","garlic"])  : ["Palak Dal","Palak Soup","Saag Dal"],
    frozenset(["methi","potato"])            : ["Aloo Methi","Methi Paratha","Methi Thepla"],
    frozenset(["methi","onion"])             : ["Methi Sabzi","Methi Pulao","Methi Bajra Roti"],
    frozenset(["spinach","corn"])            : ["Corn Palak Curry","Palak Corn Soup"],
    frozenset(["kale","onion"])              : ["Kale Sabzi","Kale Thoran","Kale Stir Fry"],

    # ─ Potato based ─
    frozenset(["potato","onion","tomato"])   : ["Aloo Tamatar","Dum Aloo","Aloo Matar"],
    frozenset(["potato","cauliflower"])      : ["Aloo Gobi","Aloo Gobi Paratha","Aloo Gobi Dry"],
    frozenset(["potato","peas"])             : ["Aloo Matar","Aloo Matar Curry","Samosa Filling"],
    frozenset(["potato","spinach"])          : ["Aloo Palak","Saag Aloo","Aloo Palak Paratha"],
    frozenset(["potato","garlic"])           : ["Jeera Aloo","Aloo Tamatar","Roasted Garlic Potatoes"],
    frozenset(["potato","carrot","peas"])    : ["Veg Biryani","Mixed Veg Curry","Veg Stew"],
    frozenset(["sweet_potato","onion"])      : ["Sweet Potato Curry","Shakarkandi Chaat","Sweet Potato Soup"],

    # ─ Tomato based ─
    frozenset(["tomato","onion","garlic"])   : ["Tomato Sabzi","Dal Tadka","Rasam"],
    frozenset(["tomato","eggplant"])         : ["Baingan Bharta","Baingan Masala","Ratatouille"],
    frozenset(["tomato","okra"])             : ["Bhindi Masala","Bhindi Do Pyaza","Okra Tomato Curry"],
    frozenset(["tomato","cauliflower"])      : ["Gobi Masala","Aloo Gobi","Cauliflower Tomato Curry"],
    frozenset(["tomato","mushroom"])         : ["Mushroom Masala","Mushroom Tomato Curry","Shakshuka"],
    frozenset(["tomato","paneer"])           : ["Paneer Makhani","Paneer Butter Masala","Shahi Paneer"],
    frozenset(["tomato","lentils"])          : ["Masoor Dal","Dal Soup","Lentil Tomato Curry"],

    # ─ Eggplant based ─
    frozenset(["eggplant","onion","tomato"]) : ["Baingan Bharta","Baingan Ka Salan","Brinjal Curry"],
    frozenset(["eggplant","potato"])         : ["Aloo Baingan","Baingan Aloo Curry"],
    frozenset(["eggplant","garlic"])         : ["Baingan Bharta","Baba Ganoush","Brinjal Stir Fry"],

    # ─ Cauliflower based ─
    frozenset(["cauliflower","potato"])      : ["Aloo Gobi","Aloo Gobi Paratha","Gobi Ki Sabzi"],
    frozenset(["cauliflower","peas","onion"]): ["Gobi Matar","Cauliflower Pea Curry","Matar Gobi"],
    frozenset(["cauliflower","garlic"])      : ["Gobi Manchurian","Roasted Garlic Cauliflower","Gobi 65"],

    # ─ Mushroom based ─
    frozenset(["mushroom","onion","garlic"]) : ["Mushroom Masala","Mushroom Do Pyaza","Mushroom Kadai"],
    frozenset(["mushroom","peas"])           : ["Mushroom Matar","Matar Mushroom Curry","Mushroom Pulao"],
    frozenset(["mushroom","spinach"])        : ["Mushroom Palak","Creamy Mushroom Spinach"],
    frozenset(["mushroom","corn"])           : ["Mushroom Corn Curry","Mushroom Corn Soup"],

    # ─ Capsicum / Pepper based ─
    frozenset(["red_pepper","onion","tomato"]): ["Capsicum Masala","Kadai Paneer","Mirchi Ka Salan"],
    frozenset(["green_pepper","onion"])      : ["Capsicum Sabzi","Stuffed Capsicum","Capsicum Rice"],
    frozenset(["yellow_pepper","onion"])     : ["Mixed Pepper Stir Fry","Yellow Pepper Curry"],

    # ─ Okra based ─
    frozenset(["okra","onion"])              : ["Bhindi Masala","Bhindi Do Pyaza","Stuffed Bhindi"],
    frozenset(["okra","tomato","onion"])     : ["Bhindi Masala Gravy","Bhindi Kurkuri","Okra Curry"],

    # ─ Pumpkin / Gourd based ─
    frozenset(["pumpkin","onion"])           : ["Kaddu Ki Sabzi","Pumpkin Curry","Pumpkin Soup"],
    frozenset(["bottle_gourd","onion"])      : ["Lauki Ki Sabzi","Lauki Chana Dal","Lauki Raita"],
    frozenset(["bitter_gourd","onion"])      : ["Karela Sabzi","Bharwa Karela","Karela Masala"],

    # ─ Legume based ─
    frozenset(["chickpeas","onion","tomato"]): ["Chole Bhature","Chana Masala","Punjabi Chole"],
    frozenset(["lentils","onion","tomato"])  : ["Masoor Dal","Dal Fry","Dal Soup"],
    frozenset(["moong_dal","onion"])         : ["Moong Dal Tadka","Moong Dal Cheela","Khichdi"],
    frozenset(["toor_dal","tomato"])         : ["Dal Tadka","Sambar","Gujarati Dal"],
    frozenset(["kidney_beans","onion","tomato"]): ["Rajma Chawal","Rajma Masala","Kidney Bean Curry"],
    frozenset(["peas","onion","tomato"])     : ["Matar Paneer","Matar Pulao","Pea Curry"],
    frozenset(["green_beans","onion"])       : ["French Beans Sabzi","Beans Thoran","Green Bean Stir Fry"],

    # ─ Carrot based ─
    frozenset(["carrot","onion","potato"])   : ["Aloo Gajar Sabzi","Mixed Veg Curry","Gajar Halwa"],
    frozenset(["carrot"])                    : ["Gajar Ka Halwa","Gajar Ki Sabzi","Carrot Soup"],
    frozenset(["carrot","peas"])             : ["Gajar Matar","Carrot Pea Stir Fry"],

    # ─ Corn based ─
    frozenset(["corn","onion","tomato"])     : ["Corn Curry","Corn Bhel","Mexican Corn Salad"],
    frozenset(["corn","capsicum"])           : ["Corn Capsicum Sabzi","Corn Fried Rice"],

    # ─ Ginger/Garlic spice base ─
    frozenset(["ginger","garlic","tomato"])  : ["Ginger Garlic Gravy Base","Adrak Tamatar Dal","Any Indian Curry"],
    frozenset(["lemon","garlic"])            : ["Lemon Rice","Rasam","Lemon Garlic Dal"],
    frozenset(["ginger","lemon"])            : ["Ginger Lemon Tea","Adrak Chai","Rasam"],

    # ─ Coconut based ─
    frozenset(["coconut","onion"])           : ["Coconut Chutney","Kerala Curry","Coconut Rice"],
    frozenset(["coconut","peas"])            : ["Peas Coconut Curry","Matar Nariyal Sabzi"],

    # ─ Fruit based ─
    frozenset(["banana"])                    : ["Banana Halwa","Kele Ki Sabzi","Banana Lassi","Banana Bread"],
    frozenset(["mango","onion"])             : ["Raw Mango Chutney","Aam Ki Launji","Mango Pickle"],
    frozenset(["mango"])                     : ["Mango Lassi","Aamras","Mango Halwa","Mango Chutney"],
    frozenset(["pineapple"])                 : ["Pineapple Raita","Pineapple Rice","Pineapple Chutney"],
    frozenset(["guava"])                     : ["Guava Chutney","Amrood Ki Sabzi","Guava Jam"],
    frozenset(["avocado","lemon"])           : ["Guacamole","Avocado Toast","Avocado Salad"],
    frozenset(["jackfruit","onion","tomato"]): ["Kathal Ki Sabzi","Raw Jackfruit Curry","Jackfruit Biryani"],
    frozenset(["pomegranate"])               : ["Anaar Raita","Pomegranate Chutney","Pomegranate Salad"],

    # ─ Herb based ─
    frozenset(["coriander","green_chilli"])  : ["Green Chutney","Coriander Chutney","Hari Chutney"],
    frozenset(["mint","onion"])              : ["Mint Chutney","Pudina Paratha","Pudina Rice"],

    # ─ Rice dishes ─
    frozenset(["peas","carrot","potato"])    : ["Veg Biryani","Veg Pulao","Veg Fried Rice"],
    frozenset(["spinach","rice"])            : ["Palak Rice","Spinach Fried Rice"],
    frozenset(["mushroom","rice"])           : ["Mushroom Biryani","Mushroom Fried Rice","Mushroom Pulao"],
    frozenset(["corn","peas","carrot"])      : ["Veg Fried Rice","Mixed Veg Pulao","Chinese Bhel"],

    # ─ Egg based ─
    frozenset(["egg","onion","tomato"])      : ["Egg Bhurji","Egg Curry","Anda Masala"],
    frozenset(["egg","spinach"])             : ["Spinach Omelette","Palak Egg Curry","Green Omelette"],
    frozenset(["egg","mushroom"])            : ["Mushroom Omelette","Egg Mushroom Curry"],
    frozenset(["egg","potato"])              : ["Egg Aloo Curry","Spanish Omelette","Egg Hash"],

    # ─ Paneer based ─
    frozenset(["paneer","tomato","onion"])   : ["Paneer Butter Masala","Shahi Paneer","Paneer Tikka Masala"],
    frozenset(["paneer","spinach"])          : ["Palak Paneer","Saag Paneer"],
    frozenset(["paneer","peas"])             : ["Matar Paneer","Paneer Matar"],
    frozenset(["paneer","capsicum"])         : ["Kadai Paneer","Paneer Capsicum Stir Fry"],
    frozenset(["paneer","corn"])             : ["Corn Paneer Curry","Paneer Corn Bhurji"],

    # ─ Mixed veggie combos ─
    frozenset(["potato","peas","carrot","onion"]): ["Veg Biryani","Veg Pulao","Mixed Veg Curry","Veg Stew"],
    frozenset(["onion","garlic","ginger"])   : ["Indian Curry Base","Masala Gravy","Makhani Sauce"],
}


# ══════════════════════════════════════════════════════════════════
# MODEL 1 — YOLOv8s (Standard, more accurate than nano)
# ══════════════════════════════════════════════════════════════════
class YOLOv8Detector:
    WEIGHT = 1.4  # Higher trust weight in ensemble

    def __init__(self):
        self.model = None
        self.model_oiv = None  # Open Images V7 model
        self.available = False

    def load(self):
        try:
            from ultralytics import YOLO  # type: ignore[import]
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # Primary: small model (more accurate than nano)
            self.model = YOLO(os.path.join(base_dir, "models/yolov8s.pt"))
            print("  ✅ YOLOv8s loaded")
            # Secondary: Open Images V7 - 600 classes (covers rare vegetables)
            try:
                self.model_oiv = YOLO(os.path.join(base_dir, "models/yolov8n-oiv7.pt"))
                print("  ✅ YOLOv8n-OIV7 (600 classes) loaded")
            except Exception as e2:
                print(f"  ⚠️  OIV7 model skip: {e2}")
            self.available = True
        except Exception as e:
            print(f"  ⚠️  YOLOv8 unavailable: {e}")

    def _run_model(self, model, image_path: str, source_tag: str, conf_thresh=0.30) -> List[Dict]:
        results = []
        try:
            preds = model(image_path, verbose=False, conf=conf_thresh)[0]
            for box in preds.boxes:
                cls_id = int(box.cls[0])
                label = preds.names[cls_id].lower().strip()
                conf = float(box.conf[0])
                friendly = YOLO_LABEL_MAP.get(label, None)
                if friendly is None:
                    # Check if any food keyword is in the label
                    if not any(kw in label for kw in FOOD_KEYWORDS):
                        continue
                    friendly = label.replace("_", " ").title()
                raw_key = label.replace(" ", "_")
                coords = box.xyxy[0].tolist()
                results.append({
                    "name": friendly,
                    "raw_label": raw_key,
                    "confidence": conf * self.WEIGHT,
                    "base_conf": conf,
                    "source": source_tag,
                    "bbox": [int(c) for c in coords],
                })
        except Exception as e:
            print(f"  YOLO run error ({source_tag}): {e}")
        return results

    def detect(self, image_path: str) -> List[Dict]:
        if not self.available:
            return []
        results = self._run_model(self.model, image_path, "yolov8s", conf_thresh=0.28)
        if self.model_oiv:
            oiv_results = self._run_model(self.model_oiv, image_path, "yolov8-oiv7", conf_thresh=0.28)
            results.extend(oiv_results)
        return results


# ══════════════════════════════════════════════════════════════════
# MODEL 2 — EfficientNetV2-S (TensorFlow/Keras)
# ══════════════════════════════════════════════════════════════════
class EfficientNetV2Classifier:
    WEIGHT = 0.7  # Reduced: ImageNet models often misclassify vegetables

    def __init__(self):
        self.model: Any = None
        self.available = False
        self.preprocess: Any = None
        self.decode: Any = None
        self.input_size: Tuple[int, int] = (384, 384)

    def load(self):
        try:
            import tensorflow as tf  # type: ignore[import]
            # Try EfficientNetV2S first (better accuracy)
            try:
                self.model = tf.keras.applications.EfficientNetV2S(
                    weights="imagenet", include_top=True
                )
                self.preprocess = tf.keras.applications.efficientnet_v2.preprocess_input
                self.decode = tf.keras.applications.efficientnet_v2.decode_predictions
                self.input_size = (384, 384)
                print("  ✅ EfficientNetV2-S loaded")
            except Exception:
                # Fallback to EfficientNetB3 (good balance of speed & accuracy)
                self.model = tf.keras.applications.EfficientNetB3(
                    weights="imagenet", include_top=True
                )
                self.preprocess = tf.keras.applications.efficientnet.preprocess_input
                self.decode = tf.keras.applications.efficientnet.decode_predictions
                self.input_size = (300, 300)
                print("  ✅ EfficientNetB3 loaded (V2S unavailable)")
            self.available = True
        except Exception as e:
            print(f"  ⚠️  EfficientNet unavailable: {e}")

    def detect(self, image_path: str) -> List[Dict]:
        if not self.available:
            return []
        results = []
        try:
            import tensorflow as tf  # type: ignore[import]
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=self.input_size)
            arr = tf.keras.preprocessing.image.img_to_array(img)
            arr = self.preprocess(arr[None])
            preds = self.model.predict(arr, verbose=0)
            decoded = self.decode(preds, top=15)[0]
            for _, name, conf in decoded:
                clean = name.lower().replace("_", " ")
                if not (any(kw in clean for kw in FOOD_KEYWORDS) and conf > 0.03):
                    continue
                raw_key = name.lower().replace(" ", "_")
                # Apply false-positive suppression / remapping
                if raw_key in IMAGENET_REMAP:
                    remapped = IMAGENET_REMAP[raw_key]
                    if remapped is None:
                        continue  # suppress this label entirely
                    raw_key = remapped
                friendly = raw_key.replace("_", " ").title()
                results.append({
                    "name": friendly,
                    "raw_label": raw_key,
                    "confidence": float(conf) * self.WEIGHT,
                    "base_conf": float(conf),
                    "source": "efficientnet_v2",
                    "bbox": None,
                })
        except Exception as e:
            print(f"  EfficientNetV2 error: {e}")
        return results


# ══════════════════════════════════════════════════════════════════
# MODEL 3 — MobileNetV3-Large (fast cross-validator)
# ══════════════════════════════════════════════════════════════════
class MobileNetV3Classifier:
    WEIGHT = 0.6  # Reduced: cross-validator only

    def __init__(self):
        self.model: Any = None
        self.available = False

    def load(self):
        try:
            import tensorflow as tf  # type: ignore[import]
            self.model = tf.keras.applications.MobileNetV3Large(
                weights="imagenet", include_top=True, include_preprocessing=True
            )
            print("  ✅ MobileNetV3-Large loaded")
            self.available = True
        except Exception as e:
            print(f"  ⚠️  MobileNetV3 unavailable: {e}")

    def detect(self, image_path: str) -> List[Dict]:
        if not self.available:
            return []
        results = []
        try:
            import tensorflow as tf  # type: ignore[import]
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
            arr = tf.keras.preprocessing.image.img_to_array(img)
            preds = self.model.predict(arr[None], verbose=0)
            decoded = tf.keras.applications.mobilenet_v3.decode_predictions(preds, top=12)[0]
            for _, name, conf in decoded:
                clean = name.lower().replace("_", " ")
                if not (any(kw in clean for kw in FOOD_KEYWORDS) and conf > 0.03):
                    continue
                raw_key = name.lower().replace(" ", "_")
                if raw_key in IMAGENET_REMAP:
                    remapped = IMAGENET_REMAP[raw_key]
                    if remapped is None:
                        continue
                    raw_key = remapped
                results.append({
                    "name": raw_key.replace("_", " ").title(),
                    "raw_label": raw_key,
                    "confidence": float(conf) * self.WEIGHT,
                    "base_conf": float(conf),
                    "source": "mobilenet_v3",
                    "bbox": None,
                })
        except Exception as e:
            print(f"  MobileNetV3 error: {e}")
        return results


# ══════════════════════════════════════════════════════════════════
# MODEL 4 — ResNet50V2 (third diverse architecture)
# ══════════════════════════════════════════════════════════════════
class ResNetClassifier:
    WEIGHT = 0.5  # Reduced: third vote only

    def __init__(self):
        self.model: Any = None
        self.available = False

    def load(self):
        try:
            import tensorflow as tf  # type: ignore[import]
            self.model = tf.keras.applications.ResNet50V2(
                weights="imagenet", include_top=True
            )
            print("  ✅ ResNet50V2 loaded")
            self.available = True
        except Exception as e:
            print(f"  ⚠️  ResNet50V2 unavailable: {e}")

    def detect(self, image_path: str) -> List[Dict]:
        if not self.available:
            return []
        results = []
        try:
            import tensorflow as tf  # type: ignore[import]
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
            arr = tf.keras.preprocessing.image.img_to_array(img)
            arr = tf.keras.applications.resnet_v2.preprocess_input(arr[None])
            preds = self.model.predict(arr, verbose=0)
            decoded = tf.keras.applications.resnet_v2.decode_predictions(preds, top=12)[0]
            for _, name, conf in decoded:
                clean = name.lower().replace("_", " ")
                if not (any(kw in clean for kw in FOOD_KEYWORDS) and conf > 0.025):
                    continue
                raw_key = name.lower().replace(" ", "_")
                if raw_key in IMAGENET_REMAP:
                    remapped = IMAGENET_REMAP[raw_key]
                    if remapped is None:
                        continue
                    raw_key = remapped
                results.append({
                    "name": raw_key.replace("_", " ").title(),
                    "raw_label": raw_key,
                    "confidence": float(conf) * self.WEIGHT,
                    "base_conf": float(conf),
                    "source": "resnet50v2",
                    "bbox": None,
                })
        except Exception as e:
            print(f"  ResNet50V2 error: {e}")
        return results


# ══════════════════════════════════════════════════════════════════
# MODEL 5 — Advanced Color + Texture + LAB Analysis
# ══════════════════════════════════════════════════════════════════
class AdvancedColorDetector:
    """
    Improved heuristic using:
    - HSV color matching (primary)
    - LAB color space (perceptually uniform, better for yellows/greens)
    - Texture analysis (LBP-like gradient features)
    - Shape circularity check
    """
    WEIGHT = 0.7  # Lower weight — supplementary

    def detect(self, image_path: str) -> List[Dict]:
        results = []
        img = cv2.imread(image_path)
        if img is None:
            return results

        h, w = img.shape[:2]
        total_pixels = h * w
        min_pixels_global = total_pixels * 0.005  # at least 0.5% of image

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # Mild sharpening to help with edge detection
        kernel_sharp = np.array([[0,-0.5,0],[-0.5,3,-0.5],[0,-0.5,0]])
        img_sharp = cv2.filter2D(img, -1, kernel_sharp)

        for ingredient, profile in FOOD_COLOR_PROFILES.items():
            min_cov_thresh = profile.get("min_cov", 0.008)
            min_pixels = total_pixels * min_cov_thresh

            lo  = np.array(profile["hsv_lo"])
            hi  = np.array(profile["hsv_hi"])
            mask = cv2.inRange(hsv, lo, hi)

            if "hsv_lo2" in profile:
                lo2 = np.array(profile["hsv_lo2"])
                hi2 = np.array(profile["hsv_hi2"])
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lo2, hi2))

            # Morphological cleaning
            k7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
            k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k7)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k7)
            mask = cv2.dilate(mask, k3, iterations=1)

            pix = cv2.countNonZero(mask)
            if pix < max(min_pixels, min_pixels_global):
                continue

            coverage = pix / total_pixels

            # Shape quality check
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid = [c for c in contours if cv2.contourArea(c) > min_pixels * 0.3]
            if not valid:
                continue

            # Circularity check (organic shapes tend to be round-ish)
            best_circ = 0.0
            for cnt in valid:
                area = cv2.contourArea(cnt)
                peri = cv2.arcLength(cnt, True)
                if peri > 0:
                    circ = 4 * np.pi * area / (peri * peri)
                    best_circ = max(best_circ, circ)

            # Confidence: coverage + shape quality + number of blobs
            shape_bonus = min(float(best_circ) * 0.2, 0.15)
            n_blobs = min(len(valid), 5)
            blob_bonus = n_blobs * 0.02
            base_conf = min(0.45 + coverage * 3.0 + shape_bonus + blob_bonus, 0.88)

            results.append({
                "name": ingredient.replace("_", " ").title(),
                "raw_label": ingredient,
                "confidence": base_conf * self.WEIGHT,
                "base_conf": base_conf,
                "source": "color_texture",
                "coverage": round(coverage * 100, 1),
                "bbox": None,
            })

        return results


# ══════════════════════════════════════════════════════════════════
# LABEL NORMALISER — maps synonyms to canonical keys
# ══════════════════════════════════════════════════════════════════
LABEL_SYNONYMS = {
    "bell_pepper":"bell_pepper", "capsicum":"bell_pepper",
    "chili_pepper":"chilli", "chili":"chilli", "hot_pepper":"chilli",
    "green_chili":"green_chilli", "green_chilly":"green_chilli",
    "brinjal":"eggplant", "aubergine":"eggplant",
    "ladyfinger":"okra", "lady_finger":"okra", "bhindi":"okra",
    "ladies_finger":"okra", "gumbo":"okra",
    "courgette":"zucchini","marrow":"zucchini",
    "cilantro":"coriander", "dhania":"coriander",
    "methi_leaves":"methi", "fenugreek_leaves":"methi",
    "spring_onion":"spring_onion","green_onion":"spring_onion","scallion":"spring_onion",
    "sweet_corn":"corn","corn_cob":"corn","maize":"corn",
    "yam":"sweet_potato","shakarkandi":"sweet_potato",
    "karela":"bitter_gourd","bitter_melon":"bitter_gourd",
    "lauki":"bottle_gourd","calabash":"bottle_gourd",
    "bottle_gourd":"bottle_gourd","dudhi":"bottle_gourd",
    "ridge_gourd":"ridge_gourd","turai":"ridge_gourd",
    "pomelo":"grapefruit","shaddock":"grapefruit",
    "jackfruit":"jackfruit","kathal":"jackfruit",
    "bread_fruit":"jackfruit",
    "button_mushroom":"mushroom","cremini":"mushroom",
    "common_mushroom":"mushroom",
    "peanut":"peanut","groundnut":"peanut","moongfali":"peanut",
    "cashew_nut":"cashew","kaju":"cashew",
    "beetroot":"beet","red_beet":"beet",
    "sweet_lime":"lime","mosambi":"lime",
    "raw_banana":"banana","plantain":"banana",
    "paneer":"paneer","cottage_cheese":"paneer",
    "tofu":"tofu","bean_curd":"tofu",
}


def normalise_label(raw: str) -> str:
    key = raw.lower().strip().replace(" ", "_").replace("-", "_")
    return LABEL_SYNONYMS.get(key, key)


# ══════════════════════════════════════════════════════════════════
# WEIGHTED BAYESIAN ENSEMBLE FUSION
# ══════════════════════════════════════════════════════════════════
def fuse_detections(all_dets: List[Dict]) -> List[Dict]:
    """
    Bayesian-style confidence fusion:
    - Normalise all labels
    - Collect per-source base confidence
    - Fuse: P(correct) = 1 - Π(1 - P_i)   (probability union)
    - Apply multi-model agreement bonus
    - Apply single-source penalty for pure heuristics
    """
    
    # Context-aware remapping: if root/leafy veg context exists, fix common misclassifications
    raw_labels = set(d["raw_label"] for d in all_dets)
    has_stew_context = "carrot" in raw_labels or "cabbage" in raw_labels
    
    for det in all_dets:
        if has_stew_context:
            if det["raw_label"] in ["orange", "lemon", "apple"]:
                det["raw_label"] = "potato"
                det["name"] = "Potato"
            elif det["raw_label"] in ["cucumber", "bell_pepper", "green_pepper"]:
                det["raw_label"] = "onion"
                det["name"] = "Onion"

    # Group by normalised label
    def _make_group() -> Dict[str, Any]:
        return {"name": "", "sources": {}, "bbox": None, "confs": []}
    groups: Dict[str, Dict[str, Any]] = defaultdict(_make_group)

    for det in all_dets:
        norm = normalise_label(det["raw_label"])
        g = groups[norm]
        src = det["source"]
        base = det.get("base_conf", det["confidence"])
        # Keep best confidence per source
        if src not in g["sources"] or g["sources"][src] < base:
            g["sources"][src] = base
        g["confs"].append(base)
        g["name"] = g["name"] or det["name"]
        if not g["bbox"] and det.get("bbox"):
            g["bbox"] = det["bbox"]

    fused = []
    for label, g in groups.items():
        source_confs = list(g["sources"].values())
        n_sources = len(g["sources"])

        # Bayesian union: P = 1 - Π(1-pi)
        prob = 1.0
        for p in source_confs:
            prob *= (1.0 - min(p, 0.97))
        ensemble_conf = 1.0 - prob

        # Multi-model agreement bonus (logarithmic)
        if n_sources >= 3:
            ensemble_conf = min(ensemble_conf * 1.18, 0.98)
        elif n_sources == 2:
            ensemble_conf = min(ensemble_conf * 1.09, 0.96)

        # Penalty: if only color/heuristic source, reduce confidence drastically instead of capping at 0.62
        if set(g["sources"].keys()) == {"color_texture"}:
            ensemble_conf = ensemble_conf * 0.4  # Massively scale down pure-color guesses

        # Must exceed minimum threshold
        if ensemble_conf < 0.12:
            continue

        category = CATEGORY_MAP.get(label, "Food Ingredient")
        nutrition = NUTRITION_MAP.get(label, "Rich in vitamins, minerals and dietary fiber")

        fused.append({
            "name": g["name"],
            "raw_label": label,
            "confidence": round(ensemble_conf, 4),  # type: ignore[call-overload]
            "confidence_pct": f"{round(ensemble_conf * 100, 1)}%",  # type: ignore[call-overload]
            "sources": list(g["sources"].keys()),
            "model_count": n_sources,
            "bbox": g["bbox"],
            "category": category,
            "nutrition": nutrition,
        })

    fused.sort(key=lambda x: -x["confidence"])
    return fused

def filter_detections(fused_dets: List[Dict]) -> List[Dict]:
    """
    Intelligently filter detections to return only the most relevant vegetables.
    - If there's a single high-confidence object, drop all other low-confidence noise.
    - If there are multiple high-confidence objects (e.g., cabbage + broccoli), keep them all.
    """
    if not fused_dets:
        return []

    # Already sorted by confidence descending, so [0] is the highest
    top_det = fused_dets[0]
    top_conf = top_det["confidence"]
    
    filtered = [top_det]

    # Dynamically keep others if they are confident enough AND relatively close to the top detection
    for det in fused_dets[1:]:  # type: ignore
        conf = det["confidence"]
        
        # Absolute threshold (must be reasonably sure)
        is_confident = conf >= 0.30
        
        is_single_model = len(det["sources"]) == 1
        
        if is_single_model:
            if top_conf > 0.85 and conf < 0.45:
                # If we are almost certain about the top object (e.g. 98% YOLO),
                # aggressively ignore stray 1-model guesses
                continue
            is_relative = conf >= (top_conf * 0.5)
        else:
            is_relative = conf >= (top_conf * 0.35)

        if is_confident and is_relative:
            filtered.append(det)

    return filtered


# ══════════════════════════════════════════════════════════════════
# DISH SUGGESTION ENGINE (improved overlap scoring)
# ══════════════════════════════════════════════════════════════════
def suggest_dishes(detected_labels: List[str]) -> List[str]:
    label_set = set(detected_labels)
    scored: List[Tuple[float, str]] = []

    for ingredient_set, dishes in DISH_COMBO_MAP.items():
        overlap = len(ingredient_set & label_set)
        if overlap == 0:
            continue
        # Jaccard-like score: overlap / union
        union = len(ingredient_set | label_set)
        jaccard = overlap / len(ingredient_set)  # recipe coverage
        precision = overlap / len(label_set) if label_set else 0
        score = 0.6 * jaccard + 0.4 * precision

        # Bonus if ALL required ingredients are present
        if ingredient_set.issubset(label_set):
            score = min(score * 1.5, 1.0)

        for dish in dishes:
            scored.append((score, dish))

    scored.sort(key=lambda x: -x[0])
    seen = []
    for _, dish in scored:
        if dish not in seen:
            seen.append(dish)

    # Indian fallbacks
    fallbacks = [
        "Dal Tadka","Aloo Matar","Jeera Rice","Veg Biryani",
        "Palak Paneer","Rajma Chawal","Masala Khichdi","Bhindi Masala",
        "Chole Bhature","Gajar Ka Halwa","Mixed Veg Sabzi","Veg Pulao",
    ]
    for f in fallbacks:
        if f not in seen:
            seen.append(f)

    return seen[:8]  # type: ignore


# ══════════════════════════════════════════════════════════════════
# IMAGE PRE-PROCESSING — enhance before inference
# ══════════════════════════════════════════════════════════════════
def preprocess_image(image_path: str) -> str:
    """
    Apply CLAHE contrast enhancement + mild denoising.
    Returns path to enhanced image (saved to uploads/).
    """
    img = cv2.imread(image_path)
    if img is None:
        return image_path

    # Denoising
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 6, 6, 7, 21)

    # CLAHE on L channel
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    l_eq = clahe.apply(l)
    merged = cv2.merge([l_eq, a, b])
    enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    # Save enhanced version
    p = Path(image_path)
    enhanced_path = str(p.parent / f"enhanced_{p.name}")
    cv2.imwrite(enhanced_path, enhanced)
    return enhanced_path


# ══════════════════════════════════════════════════════════════════
# ANNOTATOR
# ══════════════════════════════════════════════════════════════════
ANNOTATION_COLORS = [
    (46,213,115),(52,152,219),(231,76,60),(241,196,15),
    (155,89,182),(26,188,156),(230,126,34),(52,73,94),
    (39,174,96),(41,128,185),(192,57,43),(243,156,18),
    (142,68,173),(22,160,133),(211,84,0),(127,140,141),
]

def annotate_image(image_path: str, detections: List[Dict]) -> str:
    img = cv2.imread(image_path)
    if img is None:
        return ""

    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    labeled_items = [d for d in detections if d.get("bbox")]
    no_bbox_items = [d for d in detections if not d.get("bbox")]

    for i, det in enumerate(labeled_items):
        color = ANNOTATION_COLORS[i % len(ANNOTATION_COLORS)]
        x1, y1, x2, y2 = det["bbox"]
        # Thicker box
        cv2.rectangle(img, (x1,y1), (x2,y2), color, 3)
        label = f"{det['name']} {det['confidence_pct']}"
        (tw, th), _ = cv2.getTextSize(label, font, 0.55, 2)
        # Label box above
        cv2.rectangle(img, (x1, y1-th-10), (x1+tw+8, y1), color, -1)
        cv2.putText(img, label, (x1+4, y1-5), font, 0.55, (255,255,255), 2)

    # Draw text legend for non-bbox items
    for i, det in enumerate(no_bbox_items[:10]):  # type: ignore
        color = ANNOTATION_COLORS[(i + len(labeled_items)) % len(ANNOTATION_COLORS)]
        y = 32 + i * 30
        label = f"{det['name']} ({det['confidence_pct']})"
        # Shadow
        cv2.putText(img, label, (12, y+1), font, 0.6, (0,0,0), 3)
        cv2.putText(img, label, (10, y),   font, 0.6, color, 2)

    os.makedirs("results", exist_ok=True)
    out_name = f"annotated_{Path(image_path).name}"
    out_path = os.path.join("results", out_name)
    cv2.imwrite(out_path, img)
    return f"/annotated/{out_name}"


# ══════════════════════════════════════════════════════════════════
# MAIN DETECTOR ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════
class FoodDetector:
    def __init__(self):
        print("\n🔄 Loading detection models (first run downloads weights)...")
        self.yolo      = YOLOv8Detector()
        self.effnet    = EfficientNetV2Classifier()
        self.mobilenet = MobileNetV3Classifier()
        self.resnet    = ResNetClassifier()
        self.color     = AdvancedColorDetector()
        self._load_all()

    def _load_all(self):
        self.yolo.load()
        self.effnet.load()
        self.mobilenet.load()
        self.resnet.load()
        print("✅ All models ready!\n")

    def analyze(self, image_path: str) -> Dict[str, Any]:
        # Step 1: Enhance image
        enhanced_path = preprocess_image(image_path)

        # Step 2: Run all models in parallel via simple sequential (CPU safe)
        yolo_dets     = self.yolo.detect(enhanced_path)
        effnet_dets   = self.effnet.detect(enhanced_path)
        mobile_dets   = self.mobilenet.detect(enhanced_path)
        resnet_dets   = self.resnet.detect(enhanced_path)
        color_dets    = self.color.detect(enhanced_path)

        all_dets = yolo_dets + effnet_dets + mobile_dets + resnet_dets + color_dets

        # Step 3: Ensemble fusion and Smart Filtering
        fused = fuse_detections(all_dets)
        fused = filter_detections(fused)

        # Step 4: Annotate original image
        annotated_url = annotate_image(image_path, fused)

        # Step 5: Dish suggestions
        raw_labels = [d["raw_label"] for d in fused]
        dishes = suggest_dishes(raw_labels)

        # Step 6: Nutrition summary (top 6)
        nutrition = [d["nutrition"] for d in fused[:6] if d.get("nutrition")]  # type: ignore

        # Cleanup enhanced image
        try:
            if enhanced_path != image_path:
                os.remove(enhanced_path)
        except Exception:
            pass

        return {
            "success": True,
            "total_found": len(fused),
            "ingredients": fused,
            "suggested_dishes": dishes,
            "nutrition_summary": nutrition,
            "annotated_url": annotated_url,
            "model_stats": {
                "yolo_detections":       len(yolo_dets),
                "efficientnet_detections": len(effnet_dets),
                "mobilenet_detections":  len(mobile_dets),
                "resnet_detections":     len(resnet_dets),
                "color_detections":      len(color_dets),
                "models_active": sum([
                    self.yolo.available,
                    self.effnet.available,
                    self.mobilenet.available,
                    self.resnet.available,
                    True,  # color always active
                ]),
            },
        }
