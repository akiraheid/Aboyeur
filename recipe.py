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

ACCEPTED_UNITS = ['clove', 'cloves', 'cup', 'cups', 'floz', 'fluid ounce',
                  'fluid ounces', 'g', 'gram', 'grams', 'lb', 'pound', 'pounds',
                  'oz', 'ounce', 'ounces', 'slice', 'slices', 'tbsp',
                  'tablespoon', 'tablespoons', 'tsp', 'teaspoon', 'teaspoons']

UNIT_SHORTS = {
    'fluid ounce': 'floz', 'fluid ounces': 'floz',
    'gram': 'g', 'grams': 'g',
    'pound': 'lb', 'pounds': 'lbs',
    'ounce': 'oz', 'ounces': 'oz',
    'tablespoon': 'tbsp', 'tablespoons': 'tbsp',
    'teaspoon': 'tsp', 'teaspoons': 'tsp'}

_INGREDIENT_PAT = re.compile(r'\s*(?P<amount>\d+(\.\d+)?)\s+'
                             r'(?P<unit>{0})\s+'
                             r'(?P<name>(\w(\s*)?)+)\s*'
                             r'(,\s*(?P<prep>(\w(\s)??)+))?\s*'
                             r'(\((?P<note>.+)\))?'.format(
                                 '|'.join(ACCEPTED_UNITS)))

def findFirstEmptyLine(lines, start):
    """Return the index of the line in the list `lines`, starting at
    `lines[start]`, that is empty. A line is considered empty if it is only
    whitespace. If no empty lines are found, `-1` is returned."""
    for idx, line in enumerate(lines[start:]):
        if line.strip() != '':
            return idx + start

    return -1

def findFirstNonEmptyLine(lines, start):
    """Return the index of the line in the list `lines`, starting at
    `lines[start]`, that is not empty. A line is considered not empty if it
    contains something other than whitespace. If no such line can be found,
    return `-1`."""
    for idx, line in enumerate(lines[start:]):
        if line.strip() == '':
            return idx + start

    return -1

def _getTitle(line):
    """Return the title string. This function will return `line` if the string
    does not contain ']'."""
    return line[line.find(']') + 1:].strip()

def _getIngredients(lines):
    """Return a list of dictionaries for ingredients parsed from the list of
    ingredient strings, `lines`."""
    ingredients = []

    for line in lines:
        match = _INGREDIENT_PAT.search(line.strip())

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
                    line, ', '.join(ACCEPTED_UNITS)))

            ingredients.append(ingredient)
            continue

        ingredient = {}
        ingredient[INGREDIENT_AMOUNT_KEY] = float(match.group('amount'))

        # Normalize unit
        unit = match.group('unit')
        if unit in UNIT_SHORTS.keys():
            unit = UNIT_SHORTS[unit]
        ingredient[INGREDIENT_UNIT_KEY] = unit

        ingredient[INGREDIENT_NAME_KEY] = match.group('name')
        ingredient[INGREDIENT_PREPARATION_KEY] = match.group('prep')
        ingredient[INGREDIENT_NOTE_KEY] = match.group('note')

        # Strip strings
        for key, value in ingredient.iteritems():
            ingredient[key] = (
                value.strip() if value and isinstance(value, str) else value)

        ingredients.append(ingredient)
    return ingredients

def _getDirections(lines):
    """Return a list of strings where empty strings are removed from the list of
    strings, `lines`."""
    directions = [line.strip() for line in lines if line.strip() != '']
    return directions

def _extractRecipe(lines):
    """Return a recipe dictionary from the list of strings, `lines`, determined
    to be part of the recipe. A partial dictionary (dictionary with not all
    expected elements of a recipe) can be returned if parsing fails."""
    recipe = {}

    recipe[TITLE_KEY] = _getTitle(lines[0])

    # Find the start of the ingredients
    # Ignore empty lines between title and ingredients
    start = findFirstEmptyLine(lines, 1)
    end = findFirstNonEmptyLine(lines, start)

    recipe[INGREDIENTS_KEY] = _getIngredients(lines[start:end])

    # Find the start of the directions
    # Ignore empty lines between ingredients and directions
    start = findFirstEmptyLine(lines, end)
    recipe[DIRECTIONS_KEY] = _getDirections(lines[start:])

    return recipe

def fromString(recipeString):
    """Return a list of recipes from the string `recipeString`. If there are no
    recipes in the string, an empty list is returned.

    Recipes are represented by a dictionary of the format:
    ```
    {
        'title': string,
        'ingredients': [
            {
                'amount': float,
                'unit': string,
                'name': string,
                'prep': string,
                'note': string
            },
            ...,
        'directions': [string, ...]
    }
    ```"""
    recipes = []
    inRecipe = False # One-time flag to skip initial file contents until first
                     # recipe title

    lines = recipeString.split('\n')
    recipeLines = [] # Lines determined to be part of a recipe

    for line in lines:
        if not inRecipe:
            if line.lstrip().startswith(']'):
                inRecipe = True
                recipeLines.append(line)

        else:
            if line.lstrip().startswith(']'):
                # New recipe
                recipe = _extractRecipe(recipeLines)
                if recipe:
                    recipes.append(recipe)

                # Reset recipeLines
                recipeLines = [line]

            else:
                # The line is part of the recipe
                recipeLines.append(line)

    # Handle last recipe found
    recipe = _extractRecipe(recipeLines)
    if recipe:
        recipes.append(recipe)

    return recipes

def toString(recipes):
    """Return a string representation of the recipes given in `recipes` in
    Recipe-compliant format."""
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

if __name__ == '__main__':
    import argparse
    import json
    import pprint as pp
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='.rcp files to convert to JSON')
    parser.add_argument('--output', help='File to output to. Default recipes.json')

    args = parser.parse_args()

    output = args.output
    recipes = []
    for f in args.files:
        with open(f, 'r') as tmp:
            recipes.extend(fromString(tmp.read()))

    data = {"recipes": recipes}
    if output:
        with open(output, 'w') as tmp:
            json.dump(data, tmp)
    else:
        pp.pprint(json.dumps(data))
