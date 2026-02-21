// ═══════════════ DISH DATABASE ═══════════════
const DISH_DB = {
  "Palak Paneer":{emoji:"🥬",cuisine:"North Indian",isIndian:true,prepTime:"15 min",cookTime:"25 min",servings:"3-4",difficulty:"Easy",about:"Palak Paneer is a beloved North Indian curry made with a velvety spinach gravy and soft cubes of paneer. Rich in iron and protein, it pairs perfectly with roti, naan, or rice.",ingredients:["Spinach (palak) 500g","Paneer 200g","Onion 1 large","Tomato 2 medium","Garlic 5 cloves","Ginger 1 inch","Cumin seeds 1 tsp","Garam masala ½ tsp","Fresh cream 2 tbsp","Salt, Oil"],tips:["Blanch spinach in hot water 2 min to retain colour","Lightly fry paneer before adding to prevent breaking","Blend smooth for restaurant-style gravy","Add cream at the end off the heat"],steps:[{title:"Blanch the Spinach",body:"Wash <span class='kw-ingredient'>500g fresh spinach</span> thoroughly. Boil a pot of water, add spinach and <span class='kw-action'>blanch</span> for <span class='kw-time'>2 minutes</span>. Immediately transfer to ice-cold water to lock in bright green colour.",timer:120,tip:"The ice-water bath is the secret to vibrant green palak — never skip it!"},{title:"Blend the Palak",body:"Drain blanched spinach. Transfer to a blender with <span class='kw-ingredient'>2 green chillies</span>. <span class='kw-action'>Blend</span> to a completely smooth puree. Set aside.",tip:"Don't add water while blending — the moisture in the leaves is enough."},{title:"Fry the Paneer",body:"Cut <span class='kw-ingredient'>200g paneer</span> into 1.5-inch cubes. Heat 2 tbsp oil on <span class='kw-time'>medium heat</span>. <span class='kw-action'>Shallow fry</span> paneer until lightly golden on all sides. Remove and keep aside.",timer:240,tip:"Soaking fried paneer in warm water for 5 min makes it extra soft inside."},{title:"Make the Masala Base",body:"In the same pan, heat 1 tbsp oil. Add <span class='kw-ingredient'>1 tsp cumin seeds</span> — let them <span class='kw-action'>splutter</span>. Add finely chopped <span class='kw-ingredient'>onion</span>, <span class='kw-action'>sauté</span> until golden — about <span class='kw-time'>8 minutes</span>. Add ginger-garlic paste, cook <span class='kw-time'>2 minutes</span>.",timer:600,tip:"Patience here is key — properly browned onions build the curry's deep flavour."},{title:"Add Tomatoes & Spices",body:"Add <span class='kw-ingredient'>2 pureed tomatoes</span>. <span class='kw-action'>Cook</span> until oil separates — about <span class='kw-time'>6 minutes</span>. Add <span class='kw-ingredient'>½ tsp turmeric, 1 tsp coriander powder, ½ tsp red chilli powder</span>. Mix and cook <span class='kw-time'>2 minutes</span>.",timer:480,tip:"Oil separating from masala means the tomatoes are fully cooked."},{title:"Add Spinach & Simmer",body:"Pour the spinach puree into the masala. <span class='kw-action'>Stir well</span> and <span class='kw-action'>simmer</span> on low heat for <span class='kw-time'>5 minutes</span>. Add salt and a pinch of <span class='kw-ingredient'>garam masala</span>.",timer:300,tip:"Don't overcook after adding palak or it loses its bright green colour."},{title:"Add Paneer & Finish",body:"Add the fried paneer cubes. <span class='kw-action'>Simmer</span> on low heat for <span class='kw-time'>3 minutes</span>. Drizzle <span class='kw-ingredient'>2 tbsp fresh cream</span> on top. Your Palak Paneer is ready to serve!",timer:180,tip:"Serve hot with butter naan, phulka roti, or steamed basmati rice."}]},

  "Dal Tadka":{emoji:"🍲",cuisine:"North Indian",isIndian:true,prepTime:"10 min",cookTime:"30 min",servings:"4",difficulty:"Easy",about:"Dal Tadka is a comforting everyday Indian lentil dish finished with a sizzling ghee tempering of cumin, garlic, and dried red chillies. The 'tadka' is what gives this humble dish its irresistible aroma.",ingredients:["Yellow toor dal 200g","Onion 1","Tomato 2","Garlic 6 cloves","Ginger 1 inch","Cumin seeds 1 tsp","Dried red chillies 2","Ghee 2 tbsp","Turmeric ½ tsp","Salt"],tips:["Pressure cook dal for creamy texture","Always make tadka in very hot ghee for the sizzle","Add lemon squeeze before serving","Wash dal 2-3 times before cooking"],steps:[{title:"Pressure Cook the Dal",body:"Rinse <span class='kw-ingredient'>200g toor dal</span> 2-3 times. Add to pressure cooker with <span class='kw-ingredient'>600ml water</span>, <span class='kw-ingredient'>½ tsp turmeric</span>, and salt. <span class='kw-action'>Pressure cook</span> for <span class='kw-time'>4-5 whistles</span> on medium heat.",timer:600,tip:"Soaking dal for 30 min before cooking gives a creamier, faster result."},{title:"Prepare the Base",body:"Heat 1 tbsp oil. Add <span class='kw-ingredient'>chopped onions</span>, <span class='kw-action'>sauté</span> until translucent — <span class='kw-time'>5 minutes</span>. Add ginger-garlic paste, cook <span class='kw-time'>2 minutes</span>. Add <span class='kw-ingredient'>chopped tomatoes</span>, cook until soft — <span class='kw-time'>4 minutes</span>.",timer:660},{title:"Combine & Simmer",body:"Open cooker after steam releases. <span class='kw-action'>Mash</span> dal lightly. Pour into onion-tomato base. Adjust water for consistency. <span class='kw-action'>Simmer</span> for <span class='kw-time'>8 minutes</span>.",timer:480,tip:"Dal thickens as it cools — keep it slightly thinner than desired."},{title:"Make the Tadka",body:"In a small pan, heat <span class='kw-ingredient'>2 tbsp ghee</span> until very hot. Add <span class='kw-ingredient'>1 tsp cumin seeds</span> — let them <span class='kw-action'>splutter</span>. Add <span class='kw-ingredient'>4 sliced garlic cloves</span> and <span class='kw-ingredient'>2 dried red chillies</span>. <span class='kw-action'>Fry</span> until garlic is golden — <span class='kw-time'>30 seconds</span>.",timer:30,tip:"The ghee must be very hot when poured — that dramatic sizzle is the soul of tadka!"},{title:"Pour Tadka & Serve",body:"<span class='kw-action'>Pour</span> the sizzling tadka immediately over the dal. Do not stir — let it infuse for <span class='kw-time'>1 minute</span>. Garnish with fresh coriander and a squeeze of lemon. Serve hot with rice or roti.",timer:60,tip:"Dal Tadka tastes even better the next day as flavours deepen overnight."}]},

  "Baingan Bharta":{emoji:"🍆",cuisine:"North Indian",isIndian:true,prepTime:"10 min",cookTime:"35 min",servings:"3",difficulty:"Medium",about:"Baingan Bharta is a smoky North Indian dish of roasted mashed eggplant cooked with spiced onions and tomatoes. The direct-flame char gives it an unforgettable depth.",ingredients:["Large eggplant 2","Onion 2","Tomato 2","Garlic 6 cloves","Ginger 1 inch","Green chillies 2","Cumin seeds","Garam masala","Fresh coriander","Ghee 2 tbsp"],tips:["Roast eggplant directly over gas flame for smokiness","Peel while hot — the skin comes off easily","Don't skip the charring — that's the soul of this dish","Finish with a knob of butter for richness"],steps:[{title:"Roast the Eggplant",body:"Rub <span class='kw-ingredient'>2 large eggplants</span> all over with oil. Place directly on a gas flame or under a broiler. <span class='kw-action'>Roast</span>, turning occasionally, for <span class='kw-time'>20 minutes</span> until completely charred outside and very soft inside.",timer:1200,tip:"The more charred the skin, the smokier the final dish. Don't be afraid of the blackness!"},{title:"Peel & Mash",body:"Let eggplant cool slightly. <span class='kw-action'>Peel off</span> all charred skin under running water. <span class='kw-action'>Mash</span> the soft flesh well with a fork. Set aside.",tip:"Remove any large seed clusters if you prefer a smoother texture."},{title:"Build the Masala",body:"Heat 2 tbsp ghee. Add <span class='kw-ingredient'>cumin seeds</span> and let them splutter. Add <span class='kw-ingredient'>chopped onions</span>, <span class='kw-action'>fry</span> until golden — <span class='kw-time'>8 minutes</span>. Add ginger-garlic paste and green chillies, cook <span class='kw-time'>2 minutes</span>.",timer:600},{title:"Add Tomatoes & Spices",body:"Add <span class='kw-ingredient'>chopped tomatoes</span>, <span class='kw-action'>cook</span> until mushy — <span class='kw-time'>5 minutes</span>. Add <span class='kw-ingredient'>½ tsp turmeric, 1 tsp coriander powder, ½ tsp chilli powder</span>. Mix well.",timer:300},{title:"Combine & Finish",body:"Add mashed eggplant to masala. <span class='kw-action'>Mix and cook</span> together for <span class='kw-time'>5 minutes</span>. Add <span class='kw-ingredient'>½ tsp garam masala</span> and fresh <span class='kw-ingredient'>coriander</span>. Serve hot with roti.",timer:300,tip:"A swirl of raw onion and green chutney on top adds wonderful freshness."}]},

  "Mushroom Masala":{emoji:"🍄",cuisine:"Indian",isIndian:true,prepTime:"10 min",cookTime:"20 min",servings:"3",difficulty:"Easy",about:"A rich, restaurant-style tomato-onion gravy packed with plump button mushrooms. Deeply flavourful and surprisingly fast to make.",ingredients:["Button mushrooms 300g","Onion 2","Tomato 2","Garlic 5 cloves","Ginger 1 inch","Cashews 10 (optional)","Coriander powder, Cumin","Garam masala","Kasuri methi 1 tsp","Cream 2 tbsp"],tips:["Wipe mushrooms with a damp cloth, don't wash","Cook mushrooms on high heat to avoid wateriness","Kasuri methi at the end is a flavour game-changer","Soaked cashews in the gravy give it a creamy body"],steps:[{title:"Make Onion-Tomato Paste",body:"<span class='kw-action'>Roughly chop</span> <span class='kw-ingredient'>2 onions, 2 tomatoes, ginger, garlic</span>. Sauté in oil until golden — <span class='kw-time'>8 minutes</span>. Cool and <span class='kw-action'>blend</span> with soaked cashews to a smooth paste.",timer:600,tip:"Cashews in the paste create the creamy texture without any cream."},{title:"Cook the Paste",body:"Heat 2 tbsp oil. Pour paste back into pan. Add all <span class='kw-ingredient'>dry spices</span>. <span class='kw-action'>Cook</span>, stirring often, until oil separates — <span class='kw-time'>7 minutes</span>.",timer:420},{title:"Add Mushrooms",body:"Add <span class='kw-ingredient'>300g cleaned mushrooms</span>. <span class='kw-action'>Stir well</span> to coat. <span class='kw-action'>Cook</span> on medium-high heat for <span class='kw-time'>8 minutes</span> — mushrooms release water then absorb masala.",timer:480,tip:"Don't cover the pan — let moisture evaporate for a thick gravy."},{title:"Finish & Serve",body:"Add <span class='kw-ingredient'>2 tbsp cream</span>. Crush <span class='kw-ingredient'>1 tsp kasuri methi</span> between palms and add. <span class='kw-action'>Simmer</span> <span class='kw-time'>2 minutes</span>. Serve with naan or rice.",timer:120,tip:"Kasuri methi is the secret behind the restaurant-style flavour."}]},

  "Aloo Matar":{emoji:"🥔",cuisine:"North Indian",isIndian:true,prepTime:"10 min",cookTime:"25 min",servings:"3-4",difficulty:"Easy",about:"Aloo Matar is a classic North Indian dry curry with soft potatoes and sweet green peas in a fragrant tomato-onion masala. Simple, hearty, and loved across India.",ingredients:["Potato 3 medium","Green peas 1 cup","Onion 1","Tomato 2","Ginger-garlic paste 1 tbsp","Cumin seeds","Turmeric, Coriander powder","Garam masala","Fresh coriander","Oil, Salt"],tips:["Parboil potatoes slightly for faster cooking","Add peas in last 5 minutes to keep them vibrant","A pinch of amchur adds nice tang"],steps:[{title:"Prep Vegetables",body:"<span class='kw-action'>Peel and cube</span> <span class='kw-ingredient'>3 potatoes</span> into 1-inch pieces. If using frozen peas, thaw them.",tip:"Consistent cube size ensures even cooking."},{title:"Make Masala",body:"Heat 3 tbsp oil. Add <span class='kw-ingredient'>1 tsp cumin seeds</span>, let them splutter. Add <span class='kw-ingredient'>chopped onions</span>, <span class='kw-action'>sauté</span> golden — <span class='kw-time'>7 minutes</span>. Add ginger-garlic paste, cook <span class='kw-time'>1 minute</span>.",timer:480},{title:"Add Spices & Tomato",body:"Add <span class='kw-ingredient'>½ tsp turmeric, 1 tsp coriander powder, ½ tsp chilli powder</span>. Stir <span class='kw-time'>30 sec</span>. Add <span class='kw-ingredient'>2 chopped tomatoes</span>, cook until mushy — <span class='kw-time'>4 minutes</span>.",timer:270},{title:"Cook Potatoes",body:"Add potatoes, mix well. Add ¼ cup water. Cover and <span class='kw-action'>cook</span> on medium-low for <span class='kw-time'>12 minutes</span> stirring occasionally.",timer:720,tip:"Add water in small splashes if sticking — don't drown the masala."},{title:"Add Peas & Finish",body:"Add <span class='kw-ingredient'>green peas</span>. Cook uncovered on medium heat for <span class='kw-time'>4 minutes</span>. Add <span class='kw-ingredient'>½ tsp garam masala</span> and fresh <span class='kw-ingredient'>coriander</span>. Serve hot!",timer:240,tip:"Serve with phulka roti, poori, or as a side with dal-rice."}]},

  "Jeera Rice":{emoji:"🍚",cuisine:"Indian",isIndian:true,prepTime:"5 min",cookTime:"20 min",servings:"3-4",difficulty:"Very Easy",about:"Jeera Rice is fragrant basmati rice tempered with cumin seeds and ghee — simple, aromatic, and the perfect companion to any Indian curry or dal.",ingredients:["Basmati rice 1.5 cups","Cumin seeds 1 tsp","Ghee 2 tbsp","Water 3 cups","Salt","Bay leaf (optional)"],tips:["Rinse rice 3 times for fluffy grains","Soak for 20 min before cooking","Exact 1:2 rice-to-water ratio is key","Never lift the lid during steaming"],steps:[{title:"Wash & Soak Rice",body:"<span class='kw-action'>Rinse</span> <span class='kw-ingredient'>1.5 cups basmati rice</span> 3 times until water runs clear. Soak in cold water for <span class='kw-time'>20 minutes</span>, then drain completely.",timer:1200,tip:"Soaking reduces cooking time and gives fluffier, separate grains."},{title:"Temper with Jeera",body:"Heat <span class='kw-ingredient'>2 tbsp ghee</span> in a heavy pot on medium. Add <span class='kw-ingredient'>1 tsp cumin seeds</span> — let them sizzle and turn aromatic, about <span class='kw-time'>30 seconds</span>.",timer:30,tip:"When cumin starts to pop and turn a shade darker — that's the moment!"},{title:"Cook the Rice",body:"Add drained rice, gently <span class='kw-action'>stir</span> for <span class='kw-time'>1 minute</span> to coat with ghee. Add <span class='kw-ingredient'>3 cups hot water</span> and salt. Bring to boil, then cover tightly and <span class='kw-action'>cook</span> on lowest heat for <span class='kw-time'>15 minutes</span>.",timer:960,tip:"Never lift the lid during steaming — the trapped steam is what cooks the rice."},{title:"Rest & Fluff",body:"Turn off heat. Leave covered for <span class='kw-time'>5 minutes</span>. Then gently <span class='kw-action'>fluff</span> with a fork. Serve hot alongside any curry.",timer:300,tip:"Each grain should be separate and fragrant — perfect jeera rice!"}]},

  "Veg Biryani":{emoji:"🍛",cuisine:"Indian",isIndian:true,prepTime:"20 min",cookTime:"40 min",servings:"4-5",difficulty:"Medium",about:"A celebration rice dish layered with spiced vegetables, saffron, fried onions, and fragrant basmati rice. Vegetable Biryani is a feast in every single grain.",ingredients:["Basmati rice 2 cups","Mixed vegetables 400g","Onion 3","Yogurt ½ cup","Tomato 2","Biryani masala 2 tsp","Whole spices (bay leaf, cardamom, cloves, cinnamon)","Saffron + warm milk","Ghee, Mint leaves","Fried onions (birista)"],tips:["Par-cook rice to exactly 70% before layering","Dum cooking (sealed pot) is the secret","Saffron milk gives the beautiful golden colour","Don't skip fried onions — they're flavour bombs"],steps:[{title:"Par-Cook the Rice",body:"Soak <span class='kw-ingredient'>2 cups basmati rice</span> for 30 min. Boil water with <span class='kw-ingredient'>whole spices</span>, salt. Add rice and <span class='kw-action'>cook</span> until 70% done — about <span class='kw-time'>7 minutes</span>. Drain immediately.",timer:420,tip:"70% cooked: the grain bends slightly but doesn't break. It finishes in the dum."},{title:"Make Vegetable Masala",body:"Heat 3 tbsp ghee. <span class='kw-action'>Fry</span> <span class='kw-ingredient'>sliced onions</span> until deep golden. Remove half for topping. Add ginger-garlic paste, <span class='kw-ingredient'>tomatoes</span>, <span class='kw-ingredient'>biryani masala, yogurt, mixed vegetables</span>. <span class='kw-action'>Cook</span> <span class='kw-time'>10 minutes</span>.",timer:600},{title:"Layer the Biryani",body:"In a heavy pot, spread vegetable masala as base. Layer par-cooked rice on top. Add <span class='kw-ingredient'>saffron milk, fried onions, mint leaves</span>, and a drizzle of <span class='kw-ingredient'>ghee</span> on top.",tip:"Don't mix the layers — they are part of the beautiful biryani experience."},{title:"Dum Cook (Sealed Steam)",body:"Seal pot with a tight lid or dough rope. <span class='kw-action'>Cook</span> on high for <span class='kw-time'>5 minutes</span>, then reduce to lowest heat for <span class='kw-time'>20 minutes</span>.",timer:1500,tip:"Place a tawa (griddle) under the pot to prevent the bottom burning."},{title:"Rest & Serve",body:"Turn off heat. Let it <span class='kw-action'>rest</span> covered for <span class='kw-time'>10 minutes</span>. Open at the table for full aroma effect! Gently mix from bottom to top. Serve with raita.",timer:600,tip:"Opening biryani at the table is the most magical moment — the fragrance fills the room."}]},

  "Gajar Ka Halwa":{emoji:"🥕",cuisine:"Indian Dessert",isIndian:true,prepTime:"15 min",cookTime:"45 min",servings:"6",difficulty:"Medium",about:"Gajar Ka Halwa is a traditional Indian dessert made with slow-cooked grated carrots, milk, sugar, ghee, and cardamom. Beloved across India, especially in winters.",ingredients:["Carrots 1 kg (grated)","Full fat milk 1 litre","Sugar ½ cup","Ghee 4 tbsp","Cardamom powder ½ tsp","Khoya/mawa 100g (optional)","Nuts for garnish (cashew, almond, raisin)"],tips:["Use fresh red Delhi carrots for authentic flavour","Slow cooking makes all the difference — don't rush","Khoya at the end gives richness","Halwa improves in flavour the next day"],steps:[{title:"Grate the Carrots",body:"<span class='kw-action'>Peel and grate</span> <span class='kw-ingredient'>1 kg carrots</span> on a coarse grater. Keep ready.",tip:"Fresh red/Delhi carrots make far superior halwa to orange ones."},{title:"Cook in Milk",body:"Add grated carrots to a heavy wide pan. Pour <span class='kw-ingredient'>1 litre full fat milk</span>. <span class='kw-action'>Cook</span> on medium heat, stirring every few minutes, until milk is fully absorbed — about <span class='kw-time'>25-30 minutes</span>.",timer:1800,tip:"This is the longest step — be patient. The milk slowly caramelises into the carrots."},{title:"Add Sugar",body:"Once milk is absorbed, add <span class='kw-ingredient'>½ cup sugar</span>. <span class='kw-action'>Stir continuously</span> for <span class='kw-time'>8 minutes</span> on medium heat. Sugar will release water — cook until it evaporates.",timer:480},{title:"Add Ghee & Flavour",body:"Add <span class='kw-ingredient'>4 tbsp ghee</span> and <span class='kw-ingredient'>½ tsp cardamom powder</span>. Add <span class='kw-ingredient'>khoya</span> if using. <span class='kw-action'>Stir and cook</span> for <span class='kw-time'>5 more minutes</span> until glossy and fragrant.",timer:300,tip:"The halwa is ready when it leaves the sides of the pan and looks glossy."},{title:"Garnish & Serve",body:"Transfer to serving dish. Garnish with <span class='kw-ingredient'>fried cashews, almonds, and raisins</span>. Serve warm or at room temperature.",tip:"Serve with a scoop of vanilla ice cream for a modern twist — it's amazing!"}]},

  "Tomato Sabzi":{emoji:"🍅",cuisine:"Indian",isIndian:true,prepTime:"5 min",cookTime:"15 min",servings:"2-3",difficulty:"Very Easy",about:"A simple tangy tomato curry that comes together in minutes. Made with ripe tomatoes, mustard seed tadka, and a few spices — everyday Indian comfort food.",ingredients:["Tomatoes 4 large","Mustard seeds 1 tsp","Curry leaves 8-10","Garlic 3 cloves","Onion 1 small","Turmeric ½ tsp","Red chilli powder ½ tsp","Salt, Oil 2 tbsp"],tips:["Use ripe, juicy tomatoes for best flavour","Mustard seeds must pop before adding other things","A pinch of jaggery beautifully balances acidity"],steps:[{title:"Make the Tadka",body:"Heat 2 tbsp oil. Add <span class='kw-ingredient'>1 tsp mustard seeds</span> — wait for them to <span class='kw-action'>pop and splutter</span>. Add <span class='kw-ingredient'>curry leaves, a pinch of hing, sliced garlic</span>. Fry <span class='kw-time'>30 seconds</span>.",timer:30},{title:"Sauté Onion & Spices",body:"Add <span class='kw-ingredient'>chopped onion</span> and <span class='kw-action'>sauté</span> until pink — <span class='kw-time'>4 minutes</span>. Add <span class='kw-ingredient'>½ tsp turmeric</span> and <span class='kw-ingredient'>½ tsp chilli powder</span>. Stir.",timer:240},{title:"Cook Tomatoes",body:"Add <span class='kw-ingredient'>4 chopped tomatoes</span>. <span class='kw-action'>Mash slightly</span> as they cook. Cover and <span class='kw-action'>simmer</span> on medium heat for <span class='kw-time'>8 minutes</span> until oil separates.",timer:480,tip:"A pinch of jaggery or sugar beautifully balances the acidity."},{title:"Season & Serve",body:"Add salt to taste. Garnish with fresh <span class='kw-ingredient'>coriander leaves</span>. Serve hot with roti or as a side with rice and dal.",tip:"This pairs wonderfully with plain dal and rice as a quick side."}]},

  "Stir-fried Broccoli":{emoji:"🥦",cuisine:"Asian",isIndian:false,prepTime:"5 min",cookTime:"10 min",servings:"2",difficulty:"Very Easy",about:"A quick healthy Asian-style broccoli stir-fry with garlic, soy sauce and sesame. Ready in 10 minutes and packed with nutrients.",ingredients:["Broccoli 1 head","Garlic 4 cloves","Soy sauce 2 tbsp","Sesame oil 1 tsp","Ginger","Red chilli flakes","Oil"],tips:["High heat is essential for stir-fry","Don't overcook — broccoli should have a slight bite","Blanch first for vibrant green colour"],steps:[{title:"Blanch Broccoli",body:"Cut <span class='kw-ingredient'>broccoli</span> into even florets. <span class='kw-action'>Blanch</span> in boiling salted water for <span class='kw-time'>2 minutes</span>. Drain and set aside.",timer:120,tip:"Ice bath after blanching keeps the colour bright green."},{title:"Garlic & Ginger Oil",body:"Heat 2 tbsp oil in a wok on <span class='kw-action'>high heat</span>. Add <span class='kw-ingredient'>sliced garlic and ginger</span>. <span class='kw-action'>Stir fry</span> for <span class='kw-time'>30 seconds</span> until fragrant.",timer:30},{title:"Stir Fry",body:"Add broccoli to wok. <span class='kw-action'>Toss</span> on high heat for <span class='kw-time'>3 minutes</span>. Add <span class='kw-ingredient'>soy sauce, chilli flakes</span>. Toss well <span class='kw-time'>1 more minute</span>.",timer:240,tip:"Keep heat high throughout — low heat steams rather than fries."},{title:"Finish",body:"Drizzle with <span class='kw-ingredient'>sesame oil</span>. <span class='kw-action'>Toss once</span> and serve immediately over steamed rice.",tip:"Sesame oil is a finishing oil — always add at the very end."}]}
};

function getGenericDish(name){return{emoji:"🍽️",cuisine:"Indian",isIndian:true,prepTime:"20 min",cookTime:"30 min",servings:"3-4",difficulty:"Medium",about:`${name} is a classic Indian dish made with fresh vegetables, aromatic spices, and a rich masala base. Perfect with roti or rice.`,ingredients:["Main vegetables","Onion 2","Tomato 2","Ginger-garlic paste 1 tbsp","Cumin seeds 1 tsp","Garam masala ½ tsp","Oil, Salt","Fresh coriander"],tips:["Cook onions until golden for best flavour base","Oil separating from masala means it's ready","Finish with garam masala for aroma"],steps:[{title:"Build the Base",body:"Heat oil. Add <span class='kw-ingredient'>cumin seeds</span>, let them splutter. <span class='kw-action'>Sauté</span> <span class='kw-ingredient'>chopped onions</span> until golden — <span class='kw-time'>7 minutes</span>. Add ginger-garlic paste.",timer:420},{title:"Add Tomatoes & Spices",body:"Add <span class='kw-ingredient'>chopped tomatoes</span> and dry spices. <span class='kw-action'>Cook</span> until oil separates — <span class='kw-time'>5 minutes</span>.",timer:300},{title:"Add Vegetables",body:"Add your primary vegetables. Mix well. <span class='kw-action'>Cook</span> covered on medium for <span class='kw-time'>15 minutes</span>, stirring occasionally.",timer:900},{title:"Finish & Serve",body:"Add <span class='kw-ingredient'>garam masala</span> and fresh <span class='kw-ingredient'>coriander</span>. <span class='kw-action'>Simmer</span> uncovered <span class='kw-time'>3 minutes</span>. Serve hot!",timer:180}]}}

// ═══════════════ STATE ═══════════════
let currentFile=null,webcamStream=null,activeDish=null;
let recipeSteps=[],currentStep=0,timerInterval=null,timerRemaining=0;

// ═══════════════ DOM ═══════════════
const $=id=>document.getElementById(id);
const fileInput=$('fileInput'),previewContainer=$('previewContainer');
const inputPlaceholder=$('inputPlaceholder');
const previewImg=$('previewImg'),previewName=$('previewName'),previewSize=$('previewSize');
const analyzeBtn=$('analyzeBtn'),clearBtn=$('clearBtn'),loader=$('loader');
const resultsContainer=$('resultsContainer'),resultsEl=$('results'),errorBox=$('errorBox');
const newAnalysisBtn=$('newAnalysisBtn'),feedbackMsg=$('feedbackMsg'),placeholderText=$('placeholderText');
const drawerOverlay=$('drawerOverlay'),dishDrawer=$('dishDrawer');
const drawerClose=$('drawerClose'),drawerClose2=$('drawerClose2'),startCookingBtn=$('startCookingBtn');
const recipeModal=$('recipeModal'),recipeClose=$('recipeClose');
const prevBtn=$('prevBtn'),nextBtn=$('nextBtn'),repeatBtn=$('repeatBtn'),jumpBtn=$('jumpBtn');
const jumpModal=$('jumpModal'),jumpClose=$('jumpClose');
const webcamModal=$('webcamModal'),webcamBtn=$('webcamBtn'),webcamVideo=$('webcamVideo');
const captureBtn=$('captureBtn'),closeWebcamBtn=$('closeWebcamBtn');

// ═══════════════ UPLOAD ═══════════════
fileInput.addEventListener('change',e=>{if(e.target.files[0])loadFile(e.target.files[0])});

function loadFile(file){
  currentFile=file;
  previewImg.src=URL.createObjectURL(file);
  previewName.textContent=file.name;
  previewSize.textContent=`${(file.size/1024).toFixed(1)} KB`;
  previewContainer.classList.add('show');
  inputPlaceholder.classList.add('hidden');
  feedbackMsg.textContent='Great! Hit 🔍 Detect to analyse your image.';
  hideResults();
}

clearBtn.addEventListener('click',resetAll);
newAnalysisBtn.addEventListener('click',resetAll);

function resetAll(){
  currentFile=null;
  fileInput.value='';
  previewContainer.classList.remove('show');
  inputPlaceholder.classList.remove('hidden');
  feedbackMsg.textContent="What's in your kitchen today?";
  placeholderText.style.display='';
  hideResults();
}

// ═══════════════ ANALYZE ═══════════════
analyzeBtn.addEventListener('click',()=>{
  if(!currentFile)return;
  const fd=new FormData();
  fd.append('image',currentFile);
  runDetection('/detect',fd);
});

function runDetection(endpoint,body){
  hideResults();
  showError('');
  loader.style.display='block';
  feedbackMsg.textContent='Analysing… this will take a moment 🔍';
  const opts=typeof body==='string'
    ?{method:'POST',headers:{'Content-Type':'application/json'},body}
    :{method:'POST',body};
  fetch(endpoint,opts)
    .then(r=>r.json())
    .then(data=>{
      loader.style.display='none';
      if(data.error){showError(data.error);return;}
      renderResults(data);
      feedbackMsg.textContent='Here are your results! Click any dish to explore 🍛';
    })
    .catch(err=>{
      loader.style.display='none';
      showError('Detection failed: '+err.message);
      feedbackMsg.textContent="Something went wrong. Please try again.";
    });
}

// ═══════════════ RENDER ═══════════════
function renderResults(data){
  const ms=data.model_stats||{};
  $('statYolo').textContent=ms.yolo_detections??'—';
  $('statEffnet').textContent=ms.efficientnet_detections??'—';
  $('statMobile').textContent=ms.mobilenet_detections??'—';
  $('statResnet').textContent=ms.resnet_detections??'—';
  $('statColor').textContent=ms.color_detections??'—';
  $('statTotal').textContent=data.total_found??0;
  $('itemCountBadge').textContent=`${data.total_found} found`;
  $('timeBadge').textContent=`⏱ ${data.processing_time}s`;
  if(data.annotated_url)$('annotatedImg').src=data.annotated_url+'?t='+Date.now();

  const grid=$('ingredientGrid');
  grid.innerHTML='';
  (data.ingredients||[]).forEach((item,i)=>{
    const multi=item.model_count>1,pct=Math.round(item.confidence*100);
    const card=document.createElement('div');
    card.className='ingredient-card'+(multi?' multi':'');
    card.style.animationDelay=(i*55)+'ms';
    card.innerHTML=`<div class="ing-name">${item.name}</div><div class="ing-cat">${item.category}</div><div class="conf-wrap"><div class="conf-bar ${multi?'amber':''}" style="width:0%" data-w="${pct}%"></div></div><div class="conf-lbl"><span>${multi?'⭐ Multi-model':'Single model'}</span><span>${pct}%</span></div><div class="model-tags">${(item.sources||[]).map(s=>`<span class="model-tag">${s}</span>`).join('')}</div>${item.nutrition?`<div class="nut-text">${item.nutrition}</div>`:''}`;
    grid.appendChild(card);
    setTimeout(()=>{card.querySelector('.conf-bar').style.width=pct+'%'},80+i*55);
  });

  const dg=$('dishesGrid');
  dg.innerHTML='';
  (data.suggested_dishes||[]).forEach((name,i)=>{
    const info=DISH_DB[name]||getGenericDish(name);
    const card=document.createElement('div');
    card.className='dish-card'+(info.isIndian?' indian-badge':'');
    card.style.animationDelay=(i*70)+'ms';
    card.innerHTML=`<span class="dish-emoji">${info.emoji}</span><div class="dish-name">${name}</div><div class="dish-hint">${info.cuisine} · ${info.difficulty}</div>`;
    card.addEventListener('click',()=>openDishDrawer(name));
    dg.appendChild(card);
  });

  const nl=$('nutritionList');
  nl.innerHTML='';
  (data.nutrition_summary||[]).forEach((n,i)=>{
    const ingr=(data.ingredients||[])[i];
    const el=document.createElement('div');
    el.className='nutrition-item';
    el.innerHTML=ingr?`<strong>${ingr.name}</strong>${n}`:n;
    nl.appendChild(el);
  });

  placeholderText.style.display='none';
  resultsEl.style.display='block';
  resultsEl.scrollIntoView({behavior:'smooth',block:'start'});
}

// ═══════════════ DRAWER ═══════════════
function openDishDrawer(name){
  const info=DISH_DB[name]||getGenericDish(name);
  activeDish={name,info};
  $('drawerTitle').textContent=info.emoji+' '+name;
  $('drawerSubtitle').textContent=info.cuisine+' Cuisine';
  $('drawerChips').innerHTML=`<span class="chip chip-saffron">⏱ Prep: ${info.prepTime}</span><span class="chip chip-saffron">🔥 Cook: ${info.cookTime}</span><span class="chip chip-green">👥 Serves ${info.servings}</span><span class="chip chip-yellow">📊 ${info.difficulty}</span>`;
  $('drawerAbout').textContent=info.about;
  $('drawerIngredients').innerHTML=(info.ingredients||[]).map(i=>`<span class="ing-pill">${i}</span>`).join('');
  $('drawerTips').innerHTML=(info.tips||[]).map(t=>`<li>${t}</li>`).join('');
  drawerOverlay.classList.add('open');
  dishDrawer.classList.add('open');
  document.body.style.overflow='hidden';
}

function closeDishDrawer(){
  dishDrawer.classList.remove('open');
  drawerOverlay.classList.remove('open');
  document.body.style.overflow='';
}

drawerClose.addEventListener('click',closeDishDrawer);
drawerClose2.addEventListener('click',closeDishDrawer);
drawerOverlay.addEventListener('click',closeDishDrawer);

// ═══════════════ RECIPE MODAL ═══════════════
startCookingBtn.addEventListener('click',()=>{
  if(!activeDish)return;
  closeDishDrawer();
  openRecipeModal(activeDish.name,activeDish.info);
});

function openRecipeModal(name,info){
  recipeSteps=info.steps||[];currentStep=0;clearTimer();
  $('recipeModalTitle').textContent=info.emoji+' '+name;
  $('recipeModalSub').textContent=`${info.prepTime} prep · ${info.cookTime} cook · ${info.servings} servings`;
  buildStepDots();renderStep(0);
  recipeModal.classList.add('open');
  document.body.style.overflow='hidden';
}

function buildStepDots(){
  const dots=$('stepDots');
  dots.innerHTML=recipeSteps.map((s,i)=>`<div class="step-dot ${i===0?'active':''}" data-i="${i}" title="${s.title}"></div>`).join('');
  dots.querySelectorAll('.step-dot').forEach(d=>{d.addEventListener('click',()=>goToStep(parseInt(d.dataset.i)))});
}

function renderStep(idx){
  clearTimer();currentStep=idx;
  const step=recipeSteps[idx],total=recipeSteps.length;
  $('recipeProgress').style.width=((idx+1)/total*100)+'%';
  $('stepLabel').textContent=`Step ${idx+1} of ${total}`;
  document.querySelectorAll('.step-dot').forEach((d,i)=>{d.classList.remove('active','done');if(i<idx)d.classList.add('done');else if(i===idx)d.classList.add('active')});
  prevBtn.disabled=idx===0;
  nextBtn.textContent=idx===total-1?'🎉 Finish!':'Next →';
  const hasTimer=!!step.timer;
  const body=$('recipeBody');
  body.innerHTML=`
    <div class="step-num-pill">Step ${idx+1} <span>of ${total}</span></div>
    <div class="step-title">${step.title}</div>
    <div class="step-body-text">${step.body}</div>
    ${hasTimer?`<div class="step-timer has-timer"><div><div style="font-size:.72rem;color:var(--muted);margin-bottom:.2rem">⏱ SUGGESTED TIME</div><div class="timer-display" id="timerDisplay">${formatTime(step.timer)}</div></div><div class="timer-btns"><button class="btn btn-saffron btn-sm" id="timerStartBtn">▶ Start</button><button class="btn btn-muted btn-sm" id="timerResetBtn">↺ Reset</button></div></div>`:''}
    ${step.tip?`<div class="chef-tip">${step.tip}</div>`:''}
  `;
  if(hasTimer){
    timerRemaining=step.timer;
    $('timerStartBtn').addEventListener('click',startTimer);
    $('timerResetBtn').addEventListener('click',()=>{clearTimer();timerRemaining=step.timer;$('timerDisplay').textContent=formatTime(timerRemaining);$('timerStartBtn').textContent='▶ Start'});
  }
  body.scrollTop=0;
}

function showCompletion(){
  $('recipeBody').innerHTML=`<div class="completion"><span class="completion-emoji">🎉</span><h2>Dish is ready!</h2><p>You've completed all the steps. Time to plate up, serve, and enjoy! Share it with loved ones. 🍽️</p><div style="margin-top:1.5rem;display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap"><button class="btn btn-saffron" id="restartBtn">🔁 Cook Again</button><button class="btn btn-outline" id="finishCloseBtn">✓ Done</button></div></div>`;
  $('recipeProgress').style.width='100%';
  $('stepLabel').textContent=`All ${recipeSteps.length} steps done!`;
  $('restartBtn').addEventListener('click',()=>{nextBtn.style.display='';goToStep(0)});
  $('finishCloseBtn').addEventListener('click',closeRecipeModal);
  nextBtn.style.display='none';
  document.querySelectorAll('.step-dot').forEach(d=>d.classList.add('done'));
}

function goToStep(idx){if(idx<0||idx>recipeSteps.length)return;nextBtn.style.display='';renderStep(idx)}
prevBtn.addEventListener('click',()=>goToStep(currentStep-1));
nextBtn.addEventListener('click',()=>{if(currentStep>=recipeSteps.length-1)showCompletion();else goToStep(currentStep+1)});
repeatBtn.addEventListener('click',()=>goToStep(currentStep));
jumpBtn.addEventListener('click',()=>{
  const list=$('jumpStepList');
  list.innerHTML=recipeSteps.map((s,i)=>`<button class="btn btn-sm ${i===currentStep?'btn-saffron':'btn-outline'}" style="text-align:left;border-radius:10px;justify-content:flex-start" data-i="${i}"><span style="font-weight:700;min-width:22px">${i+1}.</span>${s.title}</button>`).join('');
  list.querySelectorAll('button').forEach(b=>{b.addEventListener('click',()=>{goToStep(parseInt(b.dataset.i));jumpModal.classList.remove('open')})});
  jumpModal.classList.add('open');
});
jumpClose.addEventListener('click',()=>jumpModal.classList.remove('open'));
jumpModal.addEventListener('click',e=>{if(e.target===jumpModal)jumpModal.classList.remove('open')});

function closeRecipeModal(){recipeModal.classList.remove('open');document.body.style.overflow='';clearTimer();nextBtn.style.display=''}
recipeClose.addEventListener('click',closeRecipeModal);
recipeModal.addEventListener('click',e=>{if(e.target===recipeModal)closeRecipeModal()});

// ═══════════════ TIMER ═══════════════
function startTimer(){
  const btn=$('timerStartBtn');
  if(timerInterval){clearTimer();btn.textContent='▶ Start';return;}
  btn.textContent='⏸ Pause';
  timerInterval=setInterval(()=>{
    timerRemaining--;
    const d=$('timerDisplay');
    if(d)d.textContent=formatTime(timerRemaining);
    if(timerRemaining<=0){clearTimer();if(d){d.textContent='✅ Done!';d.style.color='var(--cardamom)'}if(btn)btn.textContent='▶ Start';}
  },1000);
}

function clearTimer(){if(timerInterval){clearInterval(timerInterval);timerInterval=null;}}
function formatTime(s){if(s<=0)return"0:00";const m=Math.floor(s/60),sec=s%60;return`${m}:${sec.toString().padStart(2,'0')}`;}

// ═══════════════ WEBCAM ═══════════════
webcamBtn.addEventListener('click',openWebcam);
closeWebcamBtn.addEventListener('click',closeWebcam);

async function openWebcam(){
  try{
    webcamStream=await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'},audio:false});
    webcamVideo.srcObject=webcamStream;
    webcamModal.classList.add('open');
  }catch(e){showError('Camera access failed: '+e.message);}
}

function closeWebcam(){
  if(webcamStream){webcamStream.getTracks().forEach(t=>t.stop());webcamStream=null;}
  webcamModal.classList.remove('open');
}

captureBtn.addEventListener('click',()=>{
  const canvas=$('snapCanvas');
  canvas.width=webcamVideo.videoWidth;
  canvas.height=webcamVideo.videoHeight;
  canvas.getContext('2d').drawImage(webcamVideo,0,0);
  const dataURL=canvas.toDataURL('image/jpeg',.92);
  previewImg.src=dataURL;
  previewName.textContent='webcam_capture.jpg';
  previewSize.textContent='Live capture';
  previewContainer.classList.add('show');
  inputPlaceholder.classList.add('hidden');
  currentFile=null;
  closeWebcam();
  hideResults();
  runDetection('/detect_base64',JSON.stringify({image:dataURL}));
});

// ═══════════════ HELPERS ═══════════════
function showError(msg){errorBox.textContent=msg;errorBox.classList.toggle('show',!!msg);}
function hideResults(){
  resultsEl.style.display='none';
  loader.style.display='none';
  placeholderText.style.display='';
}
