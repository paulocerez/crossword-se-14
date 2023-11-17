from crossword import Variable, Crossword


class CrosswordCreator():

	def __init__(self, crossword):
		"""
		Create new CSP crossword generate.
		"""
		self.crossword = crossword
		self.domains = {
			var: self.crossword.words.copy()
			for var in self.crossword.variables
			for var in self.crossword.variables
		}

	# helper functions

	def print(self, assignment):
			"""
			Print crossword assignment to the terminal.
			"""
			letters = self.letter_grid(assignment)
			for i in range(self.crossword.height):
				for j in range(self.crossword.width):
					if self.crossword.structure[i][j]:
						print(letters[i][j] or " ", end="")
					else:
						print("█", end="")
				print()


	def save(self, assignment, filename):
			"""
			Save crossword assignment to an image file.
			"""
			from PIL import Image, ImageDraw, ImageFont
			cell_size = 100
			cell_border = 2
			interior_size = cell_size - 2 * cell_border
			letters = self.letter_grid(assignment)
			# Create a blank canvas
			img = Image.new(
				"RGBA",
				(self.crossword.width * cell_size,
				self.crossword.height * cell_size),
				"black"
			)
			font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
			draw = ImageDraw.Draw(img)
			for i in range(self.crossword.height):
				for j in range(self.crossword.width):
					rect = [
						(j * cell_size + cell_border,
						i * cell_size + cell_border),
						((j + 1) * cell_size - cell_border,
						(i + 1) * cell_size - cell_border)
					]
					if self.crossword.structure[i][j]:
						draw.rectangle(rect, fill="white")
						if letters[i][j]:
							_, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
							draw.text(
								(rect[0][0] + ((interior_size - w) / 2),
								rect[0][1] + ((interior_size - h) / 2) - 10),
								letters[i][j], fill="black", font=font
							)

				img.save(filename)


	def letter_grid(self, assignment):
		"""
		Return 2D array representing a given assignment.
		"""
		letters = [
			[None for _ in range(self.crossword.width)]
			for _ in range(self.crossword.height)
		]
		for variable, word in assignment.items():
			direction = variable.direction
			for k in range(len(word)):
				i = variable.i + (k if direction == Variable.DOWN else 0)
				j = variable.j + (k if direction == Variable.ACROSS else 0)
				letters[i][j] = word[k]
		return letters


	# solver functions


	# Enforce node and arc consistency -> then solve the CSP
	def solve(self):
		self.enforce_node_consistency()
		self.ac3()
		return self.backtrack(dict())

	# iterating over each variable in the puzzle, checking every word in the domain to compare the length and remove those that don't fit
	def enforce_node_consistency(self):
		for variable in self.crossword.variables:
			# iteration over a copy of the domain set to avoid modification
			for word in set(self.domains[variable]):
				if len(word) != variable.length:
					self.domains[variable].remove(word)


	# checking for overlaps between variables x and y
	# x and y as specific word slots (variables) in the puzzles -> y having a constraint relationship with x
	def revise(self, x, y):
		isRevised = False
		overlap = self.crossword.overlaps[x, y]
		# check for an overlap
		if overlap is None:
				return False
		index_x, index_y = overlap
		# iterates through words in domain of x -> checks for words in domain of y that have an overlap with the respective word of the x domain at the given indices, 
		for word_x in set(self.domains[x]):
			match = any(word_x[index_x] == word_y[index_y] for word_y in self.domains[y])
		# remove word on domain of x if no word exists that matches the overlap
			if not match:
				self.domains[x].remove(word_x)
				isRevised = True
		return isRevised


	# arc consistency algorithm
	def ac3(self, arcs=None):
		# Initialize queue with all arcs
		queue = []
		for x in self.crossword.variables:
			for y in self.crossword.neighbors(x):
				queue.append((x, y))

		# Process the queue
		while queue:
			# remove first arc from the queue
			x, y = queue.pop(0)

			# Revise x's domain
			if self.revise(x, y):
				# Check if it is empty
				if not self.domains[x]:
					return False

				# Re-add arcs involving x's neighbors
				for neighbor in self.crossword.neighbors(x) - {y}:
					queue.append((neighbor, x))

		# if no empty domains
		return True
	
	# check for completion of assignments -> assigning one value to each crossword variable
	def assignment_complete(self, assignment):
		return all(variable in assignment for variable in self.crossword.variables)


	# checking for consistency of assignments -> following all constraints (length, distinct values, no overlap conflicts)
	def consistent(self, assignment):

		for variable, value in assignment.items():
			if variable.length != len(value):
				# if assignment is not consistent -> length difference
				return False
			
		for neighbor in self.crossword.neighbors(variable):
			if neighbor in assignment and assignment[neighbor] == value:
				# if assignment is not consistent -> same values
				return False
			
		for neighbor in self.crossword.neighbors(variable):
			overlap = self.crossword.overlaps[variable, neighbor]
			if neighbor in assignment and overlap:
				i, j = overlap
				if value[i] != assignment[neighbor][j]:
					# if assignment is not consistent -> overlap conflicts
					return False

		# if assignment is consistent
		return True

	# returning list of all values of var's domain -> ordered for least-constraining (lowest conflicts)
	def order_domain_values(self, var, assignment):
		def count_conflicts(value):
			conflict_count = 0
			for neighbor in self.crossword.neighbors(var):
				if neighbor not in assignment:
					overlap = self.crossword.overlaps[var, neighbor]
					if overlap:
						i, j = overlap
						conflict_count += sum(value[i] == word[j] for word in self.domains[neighbor])
			return conflict_count
		return sorted(self.domains[var], key=count_conflicts)


	# returns an unassigned variable that is not included in the assignment yet
	def select_unassigned_variable(self, assignment):
		unassigned_variables = []

		for variable in self.crossword.variables:
			if variable not in assignment:
				unassigned_variables.append(variable)

		# minimum of the remaining values
		return min(unassigned_variables, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

	# backtracking algorithm -> receive partial assignment for the crossword, return complete one if possible, otherwise returning None
	def backtrack(self, assignment):
		
		# assignment` is a mapping from variables (keys) to words (values)
		# Check if assignment is complete
		if self.assignment_complete(assignment):
			return assignment
		
		# Selecting an unassigned variable
		var = self.select_unassigned_variable(assignment)
		for value in self.order_domain_values(var, assignment):
			new_assignment = assignment.copy()
			new_assignment[var] = value
			if self.consistent(new_assignment):
				result = self.backtrack(new_assignment)
				if result:
					return result
		return None