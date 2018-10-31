import cv2
import numpy as np
import os
from PIL import Image
import re

textfile_folder = "text_file"

def isdigit(c):

	try:
		float(c)
		# print(" grade: ", c)
		return True
	except Exception as e:
		return False

def get_sub_grade_credit(text, subject_list):
	subjects = []

	text = [x.strip() for x in text]
	text = [x for x in text if x!='']
	line = [[x] for x in text]

	print("============================================================")
	print(line)


	for x in line:
		for c in x:
			row = c.split(" ")
			if len(row) > 2:
			# print("===== ", row)
				if row[-1].isdigit():
					
		# instances:
		# 	1. the grade is 2 different elements
					if (row[-2].isdigit() and row[-3].isdigit()):
						new_grade = row[-3] + '.' + row[-2]

						# remove 2nd and 3rd to the last element from the list
						# print("old y: ", row, "\n")
						del row[-2]
						del row[-2]
						row.insert(len(row)-1,new_grade)

					if len(row[-2]) < 3:
						row[-2] = row[-2] + '0'
				
					if re.match(r"[a-z]", row[-2]) :
						row[-2] = row[-2].replace(row[-2][1], '0')

					if re.match(r"[',-_]", row[-2]) :
						row[-2] = row[-2].replace(row[-2][1], '.')

				# ========== if grade is has no period =========
					if (row[-1].isdigit() and int(row[-1]) > 5):
						row[-1] = row[-1][:1] + '.' + row[-1][1:]

					if (row[-2].isdigit() and int(row[-2]) > 5):
						row[-2] = row[-2][:1] + '.' + row[-2][1:]

					if isdigit(row[-2]) :
						subject = [row[0], row[-2], row[-1]]
						# print(subject)
						subject = ", ".join(subject)
						subject_list.append(subject)


	return subject_list		
	

def start():

	subject_list = []

	for root, dirs, files in os.walk(textfile_folder):
		
		for file in files:

			textfile_path = os.path.join(root, file)

			with open(textfile_path, encoding='utf-8') as f:
				text = f.readlines()
				subject_list = get_sub_grade_credit(text, subject_list)
			
			print("================================================")
			print(textfile_path, " DONE")

		with open(file + ".csv", "a+") as obj:
			for line in subject_list:
				obj.write(line + "\n")





		



