# Project 6 Assembler written in Python3

import sys
import os

# symbol tabel which will hold values for labels and variables 
symbol_tabel = {"SP" : 0, "LCL" : 1, "ARG" : 2, "THIS" : 3, "THAT" : 4, "R0" : 0,  "R1" : 1,  "R2" : 2,  "R3" : 3,  "R4" : 4,  "R5" : 5,  "R6" : 6, "R7" : 7, "R8" : 8, "R9" : 9, "R10" : 10, "R11" : 11, "R12" : 12, "R13" : 13, "R14" : 14, "R15" : 15, "SCREEN" : 16384, "KBD" : 24576,} 

variable_pointer = 16

comp = {
	"0" : "0101010",
	"1" : "0111111",
	"-1" : "0111010",
	"D" : "0001100",
	"A" : "0110000",
	"!D" : "0001101",
	"!A" : "0110001",
	"-D" : "0001111",
	"-A" : "0110011",
	"D+1" : "0011111",
	"A+1" : "0110111",
	"D-1" : "0001110",
	"A-1" : "0110010",
	"D+A" : "0000010",
	"D-A" : "0010011",
	"A-D" : "0000111",
	"D&A" : "0000000",
	"D|A" : "0010101",
	"M" : "1110000",
	"!M" : "1110001",
	"-M" : "1110011",
	"M+1" : "1110111",
	"M-1" : "1110010",
	"D+M" : "1000010",
	"D-M" : "1010011",
	"M-D" : "1000111",
	"D&M" : "1000000",
	"D|M" : "1010101",
}

dest = {
	"null" : "000",
	"M" : "001",
	"D" : "010",
	"MD" : "011",
	"A" : "100",
	"AM" : "101",
	"AD" : "110",
	"AMD" : "111",
}

jump = {
	"null" : "000",
	"JGT" : "001",
	"JEQ" : "010",
	"JGE" : "011",
	"JLT" : "100",
	"JNE" : "101",
	"JLE" : "110",
	"JMP" : "111",
}

#adds null chars were need in c-instruction
def add_null(line):
	line = line[:-1]
	if not "=" in line:
		line = "null=" + line
	if not ";" in line:
		line = line + ";null"
	return line

# takes out whitespace and commnets
def remove_comments_whitespace(line):
	if line[0] == "/" or line[0] == "\n":
		return ""
	elif line[0] == " ":
		return remove_comments_whitespace(line[1:])
	else:
		return line[0] + remove_comments_whitespace(line[1:])

# determines if a or c instruction
def a_or_c(token):
	if token != "":
		if token[0] == "@":
			return a_to_binary(token)
		elif token[0] != "(":
			c_arr = c_to_binary(token)
			return "111" + c_arr[0] + c_arr[1] + c_arr[2]

# convert c-instruction to binary
def c_to_binary(token):
	#dest bits
	token = add_null(token)
	new_token = token.split("=")
	dest_bits = dest.get(new_token[0], "no-dest")
	#comp bits
	new_token = new_token[1].split(";")
	comp_bits = comp.get(new_token[0], "no-comp")
	jump_bits = jump.get(new_token[1], "no-jump")

	return comp_bits, dest_bits, jump_bits 

# ronvert a-instruction to binary
def a_to_binary(token):
	global variable_pointer
	if token[1].isalpha():
		var = token[1:-1]
		temp = symbol_tabel.get(var, -1)
		if temp == -1:
			symbol_tabel.update({var : variable_pointer})
			variable_pointer = variable_pointer + 1
		# else:
		# 	temp = int(token[1:-1])
		binary = bin(temp)[2:].zfill(16)
		return binary

# first pass used for finding labels
def fristPass():
	path_to_file = sys.argv[1]
	input_file = open(path_to_file, 'r')	
	global variable_pointer
	for line in input_file:
		token = remove_comments_whitespace(line)
		token = token[:-1]
		if token != "":
			if token[0] == "(":
				new_symbol = {token[1:-1] : variable_pointer}
				symbol_tabel.update(new_symbol)
				variable_pointer = variable_pointer + 1

# second pass
def secondPass():
	path_to_file = sys.argv[1]
	input_file = open(path_to_file, 'r')
	file_without_end = path_to_file[:-4]
	for line in input_file:
		token = remove_comments_whitespace(line)
		final_line = a_or_c(token)
		output_file = open(file_without_end + ".hack", "w")
		output_file.write(str(final_line) + "\n")

fristPass()
secondPass()
