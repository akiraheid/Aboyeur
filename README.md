# Aboyeur
Aboyeur is the specification for a way to write recipes in a way that is easy to read by humans and easy to parse for importing into software.

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

## To HTML

In the repository is a parser that translates Aboyeur formatted recipes into HTML.

```
$ python aboyeur.py file.rcp
```

Titles are translated into HTML as

```html
<h1 class="recipe-title">Recipe Title</h1>
```

Ingredient lists become

```html
<div class="ingredients">
	<div class="ingredient">
		<span class="ingredient-amount">amount</span><span class="ingredient-unit">unit</span><span class="ingredient-name">ingredient name</span><span class="ingredient-prep">preparation method</span><span class="ingredient-note">notes</span>
	</div>
</div>
```

Directions become

```html
<div class="recipe-directions">
	<p class="recipe-direction">Directions.</p>
</div>
```

With their powers combined :globe_with_meridians:

```html
<h1 class="recipe-title">Grilled Cheese</h1>
<div class="ingredients">
	<div class="ingredient">
		<span class="ingredient-amount">2</span><span class="ingredient-unit">slices</span><span class="ingredient-name">bread</span><span class="ingredient-note">(whatever kind, preferably potato)</span>
	</div>
	<div class="ingredient">
		<span class="ingredient-amount">2</span><span class="ingredient-unit">slices</span><span class="ingredient-name">munster</span>
	</div>
	<div class="ingredient">
		<span class="ingredient-amount">1</span><span class="ingredient-unit">tbsp</span><span class="ingredient-name">butter</span><span class="ingredient-prep">divided</span><span class="ingredient-note">(0.5 tbsp per slice of bread)</span>
	</div>
</div>
<div class="recipe-directions">
	<p class="recipe-direction">Heat a pan to medium heat. Butter one side of each slice of bread and place cheese between slices of bread so that the buttered sides are facing outward.</p>
	<p class="recipe-direction">Place sandwich into pan and wait until golden brown, about 2 minutes. Flip and repeat. Serve hot.</p>
</div>
```

## TODO
- [ ] Support parts of Markdown in description.
