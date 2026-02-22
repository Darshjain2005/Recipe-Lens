import re

# 1. Update database_setup.py
filepath = r"c:\recipe-lens\backend\database_setup.py"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_ing = """
                # Insert Ingredients
                for ing in r['ingredients']:
                    if isinstance(ing, dict):
                        item = ing.get('item', '').lower()
                        qty = ing.get('quantity', 'as needed')
                        cursor.execute(
                            'INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                            (recipe_id, item, qty)
                        )
                    elif isinstance(r['ingredients'], dict):
                        item = ing.lower()
                        qty = str(r['ingredients'][ing])
                        cursor.execute(
                            'INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                            (recipe_id, item, qty)
                        )
                    else:
                        item = str(ing).lower()
                        qty = 'as needed'
                        cursor.execute(
                            'INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                            (recipe_id, item, qty)
                        )
"""
# Replace the old ingredients loop
pattern = re.compile(r"                # Insert Ingredients\s*for ing in r\['ingredients'\]:.*?\(recipe_id, item, qty\)\n\s*\)", re.DOTALL)
content = pattern.sub(new_ing.strip(), content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated database_setup.py")

# 2. Update voice.js
filepath = r"c:\recipe-lens\frontend\home\voice.js"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_extract = r"""function extractServings(text) {
    const m = text.match(/\b(\d+)\b/);
    if (m) {
        let num = parseInt(m[1]);
        if (num > 10 && num % 11 === 0) { // Catch "22", "33"
            num = parseInt(String(num)[0]);
        } else if (num > 10) { // Catch other unrealistic "2 3" combinations Chrome might make
            num = parseInt(String(num)[0]);
        }
        return num;
    }
    return null;
}"""
content = re.sub(r"function extractServings\(text\) \{.*?return null;\n\}", new_extract, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated voice.js")
