import os
import re

filepath = r"vision.js"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove DISH_DB and getGenericDish
pattern1 = re.compile(r"// ═══════════════ DISH DATABASE ═══════════════.*?// ═══════════════ STATE ═══════════════", re.DOTALL)
content = pattern1.sub("// ═══════════════ STATE ═══════════════", content)

# 2. Update runDetection to catch JSON errors
pattern2 = re.compile(r"fetch\(endpoint,opts\)\s*\.then\([^)]+\)\s*\.then\(data=>\{.*?\n\s*\}\)\s*\.catch\(err=>\{.*?\n\s*\}\);", re.DOTALL)
new_fetch = """fetch(endpoint,opts)
    .then(async r=>{
      if(!r.ok){
        let t = await r.text();
        try { t = JSON.parse(t).error || t; } catch(e){}
        throw new Error(t || `Server error ${r.status}`);
      }
      return r.json();
    })
    .then(data=>{
      loader.style.display='none';
      if(data.error){showError(data.error);return;}
      renderResults(data);
    })
    .catch(err=>{
      loader.style.display='none';
      showError('Detection failed: '+err.message);
      feedbackMsg.textContent="Something went wrong. Please try again.";
    });"""
content = pattern2.sub(new_fetch, content)

# 3. Update renderResults dishesGrid part
pattern3 = re.compile(r"const dg=\$\('dishesGrid'\);\s*dg\.innerHTML='';\s*\(data\.suggested_dishes\|\|\[\]\)\.forEach\([^}]+\}\);\s*const nl=\$\('nutritionList'\);", re.DOTALL)
new_dishes_grid = """const dg=$('dishesGrid');
  dg.innerHTML='<div style="color:white;padding:1rem;">Finding recipes...</div>';
  feedbackMsg.textContent='Here are your results! Finding recipes...';

  const detectedNames = (data.ingredients||[]).map(i=>i.name.toLowerCase());
  const BACKEND_URL = "http://127.0.0.1:5000";
  fetch(`${BACKEND_URL}/suggest-recipes`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ ingredients: detectedNames })
  }).then(r=>r.json()).then(recipes => {
      dg.innerHTML='';
      if(recipes.length > 0){
          feedbackMsg.textContent='Here are your results! Click any dish to explore 🍛';
          recipes.forEach((r,i)=>{
              const card=document.createElement('div');
              card.className='dish-card indian-badge';
              card.style.animationDelay=(i*70)+'ms';
              card.innerHTML=`<span class="dish-emoji">🍽️</span><div class="dish-name">${r.name}</div><div class="dish-hint">View Details</div>`;
              card.addEventListener('click',()=>openDishDrawer(r.name, r.index));
              dg.appendChild(card);
          });
      } else {
          dg.innerHTML='<div style="color:white;padding:1rem;">No matching recipes found.</div>';
          feedbackMsg.textContent='Detection complete, but no recipes matched.';
      }
  }).catch(e=>{
      console.error(e);
      dg.innerHTML='<div style="color:red;padding:1rem;">Error loading recipes.</div>';
      feedbackMsg.textContent='Detection complete, but failed to load recipes.';
  });

  const nl=$('nutritionList');"""
content = pattern3.sub(new_dishes_grid, content)

# 4. Update openDishDrawer
pattern4 = re.compile(r"function openDishDrawer\(name\)\{.*?document\.body\.style\.overflow='hidden';\n\}", re.DOTALL)
new_drawer = """async function openDishDrawer(name, recipeIndex){
  $('drawerTitle').textContent='🍽️ '+name;
  $('drawerSubtitle').textContent='Loading...';
  $('drawerChips').innerHTML='';
  $('drawerAbout').textContent='';
  $('drawerIngredients').innerHTML='<span style=\"color:white\">Loading ingredients...</span>';
  $('drawerTips').innerHTML='';
  drawerOverlay.classList.add('open');
  dishDrawer.classList.add('open');
  document.body.style.overflow='hidden';

  activeDish={name: name, info: {steps: []}}; // Temp state

  try {
    const BACKEND_URL = "http://127.0.0.1:5000";
    const res = await fetch(`${BACKEND_URL}/start-cooking`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ recipe_index: recipeIndex, servings: 1 })
    });
    if(!res.ok) throw new Error("Failed to load");
    const data = await res.json();

    const stepsObj = data.steps.map((s,i) => ({title: `Step ${i+1}`, body: s}));
    activeDish={name: data.name, info: {steps: stepsObj}};

    $('drawerSubtitle').textContent='Database Recipe';
    $('drawerChips').innerHTML=`<span class="chip chip-green">👥 Serves 1</span>`;
    $('drawerAbout').textContent=`Enjoy this delicious ${data.name} made with fresh ingredients. Click Start Cooking to view step-by-step instructions.`;
    
    let ingsHtml = Object.entries(data.ingredients || {}).map(([ing, qty]) => `<span class="ing-pill">${qty} ${ing}</span>`).join('');
    $('drawerIngredients').innerHTML=ingsHtml || '<span style="color:white">No ingredients listed</span>';
  } catch(e) {
    console.error(e);
    $('drawerSubtitle').textContent='Error loading recipe';
    $('drawerIngredients').innerHTML='';
  }
}"""
content = pattern4.sub(new_drawer, content)

# 5. Update openRecipeModal
pattern5 = re.compile(r"function openRecipeModal\(name,info\)\{.*?document\.body\.style\.overflow='hidden';\n\}", re.DOTALL)
new_modal = """function openRecipeModal(name,info){
  recipeSteps=info.steps||[];currentStep=0;clearTimer();
  $('recipeModalTitle').textContent='🍽️ '+name;
  $('recipeModalSub').textContent=`1 serving`;
  buildStepDots();renderStep(0);
  recipeModal.classList.add('open');
  document.body.style.overflow='hidden';
}"""
content = pattern5.sub(new_modal, content)


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated vision.js")
