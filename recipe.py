"""Module to generate recipe string and JSON from recipe files."""

import re

DIRECTIONS_KEY = 'directions'
INGREDIENT_AMOUNT_KEY = 'amount'
INGREDIENT_NAME_KEY = 'name'
INGREDIENT_NOTE_KEY = 'note'
INGREDIENT_PREPARATION_KEY = 'prep'
INGREDIENT_UNIT_KEY = 'unit'
INGREDIENTS_KEY = 'ingredients'
TITLE_KEY = 'title'

acceptedUnits = ['clove', 'cloves', 'cup', 'cups', 'floz', 'fluid ounce',
        'fluid ounces', 'g', 'gram', 'grams', 'lb', 'pound', 'pounds', 'oz',
        'ounce', 'ounces', 'slice', 'slices', 'tbsp', 'tablespoon',
        'tablespoons', 'tsp', 'teaspoon', 'teaspoons']

unitShorts = {
        'fluid ounce': 'floz', 'fluid ounces': 'floz',
        'gram': 'g'          , 'grams': 'g',
        'pound': 'lb'        , 'pounds': 'lbs',
        'ounce': 'oz'        , 'ounces': 'oz',
        'tablespoon': 'tbsp' , 'tablespoons': 'tbsp',
        'teaspoon': 'tsp'    , 'teaspoons': 'tsp'}

_ingredientPat = re.compile('\s*(?P<amount>\d+(\.\d+)?)\s+'
    '(?P<unit>{0})\s+'
    '(?P<name>(\w(\s*)?)+)\s*'
    '(,\s*(?P<prep>(\w(\s)??)+))?\s*'
    '(\((?P<note>.+)\))?'.format(
    '|'.join(acceptedUnits)))

def findFirstEmptyLine(lines, start):
    """Return the index of the line in the list `lines`, starting at `lines[start]`, that is empty. A line is considered empty if it is only whitespace. If no empty lines are found, `-1` is returned."""
    for idx, line in enumerate(lines[start:]):
        if line.strip() != '':
            return idx + start

    return -1

def findFirstNonEmptyLine(lines, start):
    """Return the index of the line in the list `lines`, starting at `lines[start]`, that is not empty. A line is considered not empty if it contains something other than whitespace. If no such line can be found, return `-1`."""
    for idx, line in enumerate(lines[start:]):
        if line.strip() == '':
            return idx + start

    return -1

def getTitle(line):
    return line[line.find(']') + 1:].strip()

def getIngredients(lines):
    ingredients = []

    for line in lines:
        match = _ingredientPat.search(line)

        if match is None:
            # Ingredient can't be parsed
            ingredient = {}
            ingredient[INGREDIENT_AMOUNT_KEY] = '?'
            ingredient[INGREDIENT_UNIT_KEY] = '?'
            ingredient[INGREDIENT_NAME_KEY] = '?'
            ingredient[INGREDIENT_PREPARATION_KEY] = '?'
            ingredient[INGREDIENT_NOTE_KEY] = (
                    'Cannot parse "{}".'
                    ' Perhaps the unit doesn\'t exist in the list ({})'.format(
                        line, ', '.join(acceptedUnits)))

            ingredients.append(ingredient)
            continue

        ingredient = {}
        ingredient[INGREDIENT_AMOUNT_KEY] = float(match.group('amount'))

        # Normalize unit
        unit = match.group('unit')
        if unit in unitShorts.keys():
            unit = unitShorts[unit]
        ingredient[INGREDIENT_UNIT_KEY] = unit

        ingredient[INGREDIENT_NAME_KEY] = match.group('name')
        ingredient[INGREDIENT_PREPARATION_KEY] = match.group('prep')
        ingredient[INGREDIENT_NOTE_KEY] = match.group('note')

        # Strip strings
        for key, value in ingredient.iteritems():
            ingredient[key] = (
                    value.strip() if value and type(value) is str else value)

        ingredients.append(ingredient)
    return ingredients

def getDirections(lines):
    directions = filter(lambda line : line.strip() != '', lines)
    return directions

def extractRecipe(lines):
    recipe = {}

    recipe[TITLE_KEY] = getTitle(lines[0])

    # Find the start of the ingredients
    # Ignore empty lines between title and ingredients
    start = findFirstEmptyLine(lines, 1)
    end = findFirstNonEmptyLine(lines, start)

    recipe[INGREDIENTS_KEY] = getIngredients(lines[start:end])

    # Find the start of the directions
    # Ignore empty lines between ingredients and directions
    start = findFirstEmptyLine(lines, end)
    recipe[DIRECTIONS_KEY] = getDirections(lines[start:])

    return recipe

def fromString(s):
    """Return a list of recipes from the string `s`. If there are no recipes in the string, an empty list is returned."""
    recipes = []
    inRecipe = False # One-time flag to skip initial file contents until first
                     # recipe title

    lines = s.split('\n')
    recipeLines = [] # Lines determined to be part of a recipe

    for line in lines:
        if not inRecipe:
            if line.lstrip().startswith(']'):
                inRecipe = True
                recipeLines.append(line)

        else:
            if line.lstrip().startswith(']'):
                # New recipe
                recipe = extractRecipe(recipeLines)
                if recipe:
                    recipes.append(recipe)

                # Reset recipeLines
                recipeLines = [line]

            else:
                # The line is part of the recipe
                recipeLines.append(line)

    # Handle last recipe found
    recipe = extractRecipe(recipeLines)
    if recipe:
        recipes.append(recipe)

    return recipes

def toString(recipes):
    """Return a string representation of the recipes given in `recipes`."""
    recipeStrings = []

    for recipe in recipes:
        output = '] {}\n\n'.format(recipe[TITLE_KEY])

        for ingredient in recipe[INGREDIENTS_KEY]:
            output += '{} {} {}'.format(
                    ingredient[INGREDIENT_AMOUNT_KEY],
                    ingredient[INGREDIENT_UNIT_KEY],
                    ingredient[INGREDIENT_NAME_KEY])

            if ingredient[INGREDIENT_PREPARATION_KEY]:
                output += ', {}'.format(ingredient[INGREDIENT_PREPARATION_KEY])

            if ingredient[INGREDIENT_NOTE_KEY]:
                output += ' ({})'.format(ingredient[INGREDIENT_NOTE_KEY])

            output += '\n'

        output += '\n'

        recipeStrings.append(output + '\n\n'.join(recipe[DIRECTIONS_KEY]))

    return '\n'.join(recipeStrings)
