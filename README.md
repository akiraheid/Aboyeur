# Aboyeur
Aboyeur is the specification for a way to write recipes in a way that is easy to read by humans and computers. Running a Aboyeur parser on an Aboyeur formatted file will generate HTML.

## Format
The recipe starts with the closing bracket (]) to signify the recipe title, allowing multiple recipes to be stored in the same file.

```
] Recipe Title
```

Titles are generated as `<h1>` as a class of "recipe-title".

```html
<h1 class="recipe-title">Recipe Title</h1>
```

Below, the title is the ingredient list. Ingredients are listed one after another with no empty lines inbetween. Each ingredient has 5 components: amount, unit, ingredient name, preparation method, and notes.

The amount is the numerical amount of the ingredient. The amount can be a decimal.

Following the amount is the optional unit (optional to allow specification of things like 1 peanut instead of exact amounts). Then the ingredient name itself. Following that, an option command and preparation method of the ingredient (ie. chopped, diced, etc.) can be specified. At the end, an optional note in parentheses can be specified.

```
amount [unit] ingredient name[, preparation method] [(notes)]
```

Ingredient lists are generated as children `<div>`s of a `<div>`. The parent `<div>` is a class of "ingredients" and the children `<divs>` are a class of "ingredient". Each ingredient `<div>` is further broken down into `<span>`s for each piece of information about that ingredient.

```html
<div class="ingredients">
	<div class="ingredient">
		<span class="ingredient-amount">amount</span><span class="ingredient-unit">unit</span><span class="ingredient-name">ingredient name</span><span class="ingredient-prep">preparation method</span><span class="ingredient-note">notes</span>
	</div>
</div>
```

Directions for the recipe are specified following an empty line after the ingredient list. The text is read as plain text.

```
Directions.

More directions.
```

Directions are generated as `<p>`s of class "recipe-direction" in a `<div>` tree of class "recipe-directions".

```html
<div class="recipe-directions">
	<p class="recipe-direction">Directions.</p>
</div>
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

## TODO
[ ] Support parts of Markdown in description.
