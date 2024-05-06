# helper functions
from crossword import Variable

def print_crossword(assignment, crossword):
	"""
	Print crossword assignment to the terminal.
	"""
	letters = letter_grid_crossword(assignment, crossword)
	for i in range(crossword.height):
		for j in range(crossword.width):
			if crossword.structure[i][j]:
				print(letters[i][j] or " ", end="")
			else:
				print("█", end="")
		print()


def save_crossword(assignment, filename, crossword):
		"""
		Save crossword assignment to an image file.
		"""
		from PIL import Image, ImageDraw, ImageFont
		cell_size = 100
		cell_border = 2
		interior_size = cell_size - 2 * cell_border
		letters = letter_grid_crossword(assignment)
		# Create a blank canvas
		img = Image.new(
			"RGBA",
			(crossword.width * cell_size,
			crossword.height * cell_size),
			"black"
		)
		font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
		draw = ImageDraw.Draw(img)
		for i in range(crossword.height):
			for j in range(crossword.width):
				rect = [
					(j * cell_size + cell_border,
					i * cell_size + cell_border),
					((j + 1) * cell_size - cell_border,
					(i + 1) * cell_size - cell_border)
				]
				if crossword.structure[i][j]:
					draw.rectangle(rect, fill="white")
					if letters[i][j]:
						_, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
						draw.text(
							(rect[0][0] + ((interior_size - w) / 2),
							rect[0][1] + ((interior_size - h) / 2) - 10),
							letters[i][j], fill="black", font=font
						)
			img.save(filename)

def letter_grid_crossword(assignment, crossword):
	"""
	Return 2D array representing a given assignment.
	"""
	letters = [
		[None for _ in range(crossword.width)]
		for _ in range(crossword.height)
	]
	for variable, word in assignment.items():
		direction = variable.direction
		for k in range(len(word)):
			i = variable.i + (k if direction == Variable.DOWN else 0)
			j = variable.j + (k if direction == Variable.ACROSS else 0)
			letters[i][j] = word[k]
	return letters