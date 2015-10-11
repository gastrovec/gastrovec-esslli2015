import json
import sys
import re

from collections import Counter

unwanted = re.compile(r'^[x0-9¼½⅓¾⅛⅔](.*[0-9¼½⅓¾⅛⅔])?')
number = re.compile(r'[0-9¼½⅓¾⅛⅔]+')
tosomething = re.compile(r'^[^A-Za-z]+ to [^A-Za-z]+')
parens = re.compile(r'\(.*?\)')
possessive = re.compile(r"^.*?[']s ")
reciperegex = re.compile(r"\b(recipe|how to( make| cook| roast| handle)?|diy:?|tutorial:?|\w+ 101:?|homemade|a|(really )?easy([ -]peasy)?|quick( (&amp;|and) easy)?|best|very|everything|everyday|my|own|your|(the )?easiest( ever)?|(the )?most \w+|part|i+)\b")
units = re.compile(r'\b(cups?|a|l|handful|x|tb|lbs?|oz|mls?|g|tablespoons?|teaspoons?|pounds?|pinch|box|cans?|liters?|litres?|packages?|whole|bags?|tbsps?|tbs|tsps?|ounces?|dash|bunch|pieces?|slices?|sticks?|fl|gallons?|squares?|kgs?|kilograms?|tins?|%|chunks?|inch(es)?)\b')

matrix = Counter()
#recipe matrix
r_matrix = Counter()

def addLocalIngredients(ingredients, recipe_name, recipe_file):
    for ingredient in ingredients:
        if recipe_name:
            r_matrix[(recipe_name, ingredient)] += 1
        for ingredient2 in ingredients:
            matrix[(ingredient, ingredient2)] += 1
    if recipe_name:
        recipe_file.write(recipe_name + " " + " ".join(ingredients) + "\n")

def saveToFile(lst, filename):
    with open(filename, "w") as f:
        for item in lst:
            f.write(item + "\n")

def filterRecipe(recipe):
    recipe = recipe.lower()
    if recipe[0] == "(" and recipe[-1] == ")":
        recipe = recipe[1:-1]
    recipe = parens.sub("",recipe.replace("’","'"))
    recipe = possessive.sub("",recipe)
    recipe = reciperegex.sub("",recipe)
    if " with " in recipe:
        recipe = recipe.split(" with ")[0]
    if " from " in recipe:
        recipe = recipe.split(" from ")[0]
    if " - " in recipe:
        recipe = recipe.split(" - ")[0]
    recipe = " ".join(recipe.split())
    recipe = recipe.strip().replace(" ","_").replace("\t","").replace("\n","")
    return recipe

def filterIngredient(ingredient):
    orig = ingredient[:]
    ingredient = parens.sub("",ingredient)
    ingredient = ingredient.replace("less,","less")
    ingredient = ingredient.split(",")[0] #only before first comma, if present
    ingredient = unwanted.sub("",ingredient)
    ingredient = ingredient.replace("\t"," ")
    ingredient = ingredient.strip().lower()
    ingredient = ingredient.replace("ed, ","ed ")
    ingredient = ingredient.replace("&amp;","and")
    ingredient = ingredient.replace(" -","-")
    ingredient = ingredient.replace("(","").replace(")","").replace(".","")
    if " for " in ingredient:
        ingredient = ingredient.split(" for ")[0]
    ingredient = ingredient.replace("to taste","")
    ingredient = ingredient.replace("to season","")
    ingredient = units.sub("",ingredient)
    """ingredient = ingredient.replace("cups","")
    ingredient = ingredient.replace("cup","")
    ingredient = ingredient.replace(" x ","")
    ingredient = ingredient.replace(" ml ","")
    ingredient = ingredient.replace("oz ","")
    ingredient = ingredient.replace(" mls ","")
    ingredient = ingredient.replace(" g ","")
    ingredient = ingredient.replace("tablespoons","")
    ingredient = ingredient.replace("ounce","")
    ingredient = ingredient.replace("ounces","")
    ingredient = ingredient.replace("pinch","")
    ingredient = ingredient.replace("pound","")
    ingredient = ingredient.replace("box","")
    ingredient = ingredient.replace("can","")
    ingredient = ingredient.replace("pounds","")
    ingredient = ingredient.replace("package","")
    ingredient = ingredient.replace("packages","")
    ingredient = ingredient.replace("whole","")
    ingredient = ingredient.replace("tablespoon","")
    ingredient = ingredient.replace("teaspoons","")
    ingredient = ingredient.replace("teaspoon","")
    ingredient = ingredient.replace("tsp","")
    ingredient = ingredient.replace("tbsp","")"""
    ingredient = tosomething.sub("", ingredient)
    ingredient = ingredient.strip()
    ingredient = tosomething.sub("", ingredient)

    if ingredient[:4] == "and ":
        ingredient = ingredient[4:]
    if ingredient[:2] == "g ":
        ingredient = ingredient[2:]
    if ingredient[:3] == "of ":
        ingredient = ingredient[3:]
    if ingredient[:4] == "for ":
        return
    if " of " in ingredient:
        ingredient = ingredient.split(" of ")[1]
    if number.search(ingredient):
        ingredient = number.split(ingredient)[0]
    # if ingredient and ingredient[-1] == "s":
        # ingredient = ingredient[:-1]
    ingredient = " ".join(ingredient.split())
    ingredient = ingredient.replace(" ","_")
    if len(ingredient) < 3:
        return
    if ingredient == "and_freshly_ground_saltblack_pepper":
        print(orig)
    return ingredient

def main():
    top_ingredients = Counter()
    all_recipes = []
    print("Opening file",sys.argv[1], file=sys.stderr)
    with open(sys.argv[1]) as f:
        for line in f:
            recipe = json.loads(line)
            all_recipes.append(filterRecipe(recipe["name"]))
            raw_ingredients = recipe["ingredients"].split("\n")
            for ingredient in raw_ingredients:
                ing = ingredient
                ing = filterIngredient(ing)
                if ing:
                    top_ingredients[ing] += 1
    print(top_ingredients.most_common(100),file=sys.stderr)
    print("Number of ingredients:",len(top_ingredients), file=sys.stderr)
    more_than_ten = [ing for ing in top_ingredients if top_ingredients[ing]>10]
    print("More than ten:",len(more_than_ten), file=sys.stderr)
    print("Writing columns and rows to file...", file=sys.stderr, end="")
    sys.stderr.flush()
    saveToFile(more_than_ten,"corpus.cols")
    saveToFile(more_than_ten,"corpus.rows")
    saveToFile(all_recipes,"recipes.rows")
    saveToFile(more_than_ten,"recipes.cols")
    print("done", file=sys.stderr)
    print("Collecting counts...", file=sys.stderr, end="")
    sys.stderr.flush()
    recipe_file = open("recipe_composition_counts.txt","w")
    with open(sys.argv[1]) as f:
        for line in f:
            recipe = json.loads(line)
            raw_ingredients = recipe["ingredients"].split("\n")
            local_ingredients = []
            for ingredient in raw_ingredients:
                ing = ingredient
                ing = filterIngredient(ing)
                if ing:
                    local_ingredients.append(ing)
            addLocalIngredients(local_ingredients, filterRecipe(recipe["name"]), recipe_file)
    recipe_file.close()
    print("done", file=sys.stderr)
    print("Writing ingredient matrix to file...", file=sys.stderr, end="")
    sys.stderr.flush()
    with open("corpus.sm", "w") as f:
        for (ing1, ing2) in matrix:
            f.write(ing1 + " " + ing2 + " " + str(matrix[(ing1, ing2)]) + "\n")
    print("done", file=sys.stderr)
    print("Writing recipe matrix to file...", file=sys.stderr, end="")
    sys.stderr.flush()
    with open("recipes.sm", "w") as f:
        for (rec, ing) in r_matrix:
            f.write(rec + " " + ing + " " + str(r_matrix[(rec, ing)]) + "\n")
    print("done", file=sys.stderr)
    print("All done. Enjoy!", file=sys.stderr)

def inspections():
    print("DEBUG MODE: Running inspections()")
    top_ingredients = Counter()
    print("Opening file",sys.argv[1], file=sys.stderr)
    with open(sys.argv[1]) as f:
        for line in f:
            recipe = json.loads(line)
            raw_ingredients = recipe["ingredients"].split("\n")
            for ingredient in raw_ingredients:
                ingredient = filterIngredient(ingredient)
                if ingredient:
                    top_ingredients[ingredient] += 1
    print("Number of ingredients:",len(top_ingredients))
    more_than_ten = [ing for ing in top_ingredients if top_ingredients[ing]>10]
    print("Number of ingredients:",len(more_than_ten))
    print("ketchup:",top_ingredients["ketchup"])
    print("tomato ketchup:",top_ingredients["tomato_ketchup"])

if len(sys.argv) < 2:
    print("Usage: buildCorpus.py <uncompressed openrecipes dump>", file=sys.stderr)

if __name__ == "__main__":
    inspections()
