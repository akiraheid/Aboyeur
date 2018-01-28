# Script to convert Aboyeur files into HTML

import argparse
import re

acceptedUnits = ['clove', 'cloves', 'cup', 'cups', 'floz', 'fluid ounce',
        'fluid ounces', 'g', 'gram', 'grams', 'lb', 'pound', 'pounds', 'oz',
        'ounce', 'ounces', 'slice', 'slices', 'tbsp', 'tablespoon',
        'tablespoons', 'tsp', 'teaspoon', 'teaspoons']

ingredientPat = re.compile('\s*(?P<amount>\d+(\.\d+)?)\s+'
    '(?P<unit>{0})\s+'
    '(?P<name>(\w(\s*)??)+)\s*'
    '(,\s*(?P<prep>(\w(\s)??)+))?\s*'
    '(\((?P<note>.+)\))?'.format(
    '|'.join(acceptedUnits)))

def findFirstEmptyLine(lines, index):
    for line in lines[index:]:
        if line.strip() != '':
            break
        else:
            index = index + 1

    return index

def findFirstNonEmptyLine(lines, index):
    for line in lines[index:]:
        if line.strip() == '':
            break
        else:
            index = index + 1

    return index

def getTitle(line):
    return line[line.find(']') + 1:].strip()

def getIngredients(lines):
    ingredients = []

    for line in lines:
        match = ingredientPat.search(line)

        if match is None:
            # Ingredient can't be parsed
            ingredient = {}
            ingredient['amount'] = '?'
            ingredient['unit'] = '?'
            ingredient['name'] = '?'
            ingredient['prep'] = '?'
            ingredient['note'] = 'Cannot parse "{0}". Perhaps the unit doesn\'t exist in the list ({1})'.format(line, ', '.join(acceptedUnits))
            ingredients.append(ingredient)
            continue

        ingredient = {}
        ingredient['amount'] = match.group('amount')
        ingredient['unit'] = match.group('unit')
        ingredient['name'] = match.group('name')
        ingredient['prep'] = match.group('prep')
        ingredient['note'] = match.group('note')
        ingredients.append(ingredient)

    return ingredients

def getDirections(lines):
    directions = filter(lambda line : line.strip() != '', lines)
    return directions

def readRecipe(lines):
    recipe = {}

    recipe['title'] = getTitle(lines[0])

    # Find the start of the ingredients
    # Ignore empty lines between title and ingredients
    start = findFirstEmptyLine(lines, 1)
    end = findFirstNonEmptyLine(lines, start)

    recipe['ingredients'] = getIngredients(lines[start:end])

    # Find the start of the directions
    # Ignore empty lines between ingredients and directions
    start = findFirstEmptyLine(lines, end)
    recipe['directions'] = getDirections(lines[start:])

    return recipe

def generateHTML(recipe):
    if len(recipe) == 0:
        return 'No recipe'

    recipe = readRecipe(recipeLines)
    htmlString = '<h1 class="recipe-title">' + recipe['title'] + '</h1>'

    htmlString = htmlString + '<div class="ingredients">'
    for ingredient in recipe['ingredients']:
        htmlString = (''
            '{0}<div class="ingredient">'
                '<span class="ingredient-amount">{1}</span>'
                '<span class="ingredient-unit">{2}</span>'
                '<span class="ingredient-name">{3}</span>'
                '{4}'
                '{5}'
            '</div>'.format(htmlString, ingredient['amount'],
                ingredient['unit'], ingredient['name'],
                ('' if ingredient['prep'] is None else
                    '<span class="ingredient-prep">{0}</span>'.format(
                        ingredient['prep'])),
                ('' if ingredient['note'] is None else
                    '<span class="ingredient-note">({0})</span>'.format(
                        ingredient['note']))
                )
            )

    htmlString = htmlString + '</div>'

    htmlString = htmlString + '<div class="recipe-directions">'
    for direction in recipe['directions']:
        htmlString = (''
            '{0}<p class="recipe-direction">{1}</p>'.format(htmlString, direction))

    htmlString = htmlString + '</div>'

    return htmlString

# Start script
parser = argparse.ArgumentParser()
parser.add_argument('FILE', metavar='FILE', nargs=1)

args = parser.parse_args()

lines = ''
with open(args.FILE[0], 'r') as file:
    lines = file.read().split('\n')

inRecipe = False
recipeLines = []
htmlString = ''
for line in lines:
    if not inRecipe:
        if line.lstrip().startswith(']'):
            inRecipe = True
            recipeLines.append(line)

        # Ignore lines at the beginning of the file that aren't part of a recipe

    else:
        if line.lstrip().startswith(']'):
            # Generate html for recipe
            htmlString = htmlString + generateHTML(recipeLines)

            # Reset recipeLines
            recipeLines = [line]

        else:
            # The line is part of the recipe
            recipeLines.append(line)

# Generate the HTML for the last recipe read
htmlString = htmlString + generateHTML(recipeLines)

print htmlString