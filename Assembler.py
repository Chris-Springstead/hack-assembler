# Project 6 Assembler written in Python3

import sys

def main():
	#getting argument from command line
	path_to_file = sys.argv[1]
	input_file = open(path_to_file, 'r')
	for line in input_file:
		# gets rid of the extra lines that are occuring when printing
		print(line, end="")

	# symbol tabel which will hold values for labels and variables 
	symbol_tabel = {"R0" : 0, "R1": 1, "R2" : 2} 

	# first pass used for finding labels
	'''
	def firstPass():

	# second pass used for reading asm code
	def secondPass():

	def main():
		firstPass()
		secondPass()
	'''	
if __name__ == '__main__':
	main()