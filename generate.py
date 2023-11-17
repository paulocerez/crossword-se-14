
# GOAL: Generate a program that automatically generates crossword puzzles that fulfill the constraint satisfaction problem


import sys
from crossword import *
from functions.utils import CrosswordCreator

from crossword import *





def main():

	# Check usage
	if len(sys.argv) not in [3, 4]:
		sys.exit("Usage: python generate.py structure words [output]")

	# Parse command-line arguments
	structure = sys.argv[1]
	words = sys.argv[2]
	output = sys.argv[3] if len(sys.argv) == 4 else None

	# Generate crossword
	crossword = Crossword(structure, words)
	creator = CrosswordCreator(crossword)
	assignment = creator.solve()

	# Print result
	if assignment is None:
		print("No solution.")
	else:
		creator.print(assignment)
		if output:
			creator.save(assignment, output)


if __name__ == "__main__":
	main()
