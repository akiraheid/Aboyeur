# Recipe
Recipe is the specification for a way to write recipes in a way that is easy to read by humans and parseable for importing into software.

## Format
The recipe starts with the closing bracket (`]`) to signify the recipe title, allowing multiple recipes to be stored in the same file.

```
] Recipe Title
```

Below the title is the ingredient list. Ingredients are listed one after another with no empty lines inbetween. Each ingredient has 5 components:
* Amount
* Unit
* Ingredient name
* Preparation method (optional)
* Notes (optional)

The accepted units are:
clove(s), cup(s), floz, fluid ounce(s), g, gram(s), lb, pound(s), oz, ounce(s), slice(s), tbsp, tablespoon(s), tsp, teaspoon(s)

```
amount unit ingredient name[, preparation method] [(notes)]
```

Directions for the recipe are specified following an empty line after the ingredient list. The text is read as plain text.

```
Directions.

More directions.
```

## Example

Here's an example recipe of grilled cheese, yum!

```
] Grilled Cheese

2 slices bread (whatever kind, preferably potato)
2 slices munster cheese
1 tbsp butter, divided (0.5 tbsp per slice of bread)

Heat a pan to medium heat. Butter one side of each slice of bread and place cheese between slices of bread so that the buttered sides are facing outward.

Place sandwich into pan and wait until golden brown, about 2 minutes. Flip and repeat. Serve hot.
```
