import cv2
import numpy as np
import os
from PIL import Image
import make_csv
from matplotlib import pyplot as plt

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


def remove_watermark(image):
		contrast = 2.0		
		brightness = -160.5	

		image = contrast * image + brightness
		# limit the values in an array
		image = np.clip(image, 0, 255).astype(np.uint8)

		return image

def resize_image(nimage, image):
	h, w = nimage.shape[:2]
	ar = w/h
	nw = 800
	nh = int(nw / ar)
	nimage = cv2.resize(nimage,(nw, nh))
	image = cv2.resize(image,(nw, nh))

	return	nimage, image
	

def otsu_preprocess(image, new_img):
	# gray = cv2.GaussianBlur(gray, (3,3), 0)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	prepimage = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	
	# nimage, image = resize_image(prepimage, new_img)
	
	cv2.imshow("orig", image)
	cv2.imshow("OTSU", prepimage)

	cv2.waitKey(2000)
	# _, contours, hierarchy = cv2.findContours(new_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	return prepimage

def extract_text(image_pil):
	image_pil = Image.open(image_pil)
	text = pytesseract.image_to_string(image_pil)
	return text

def is_gray_scale(image):
	img = Image.open(image_path).convert('RGB')
	w, h = img.size
	for i in range(w):
		for j in range(h):
			r,g,b = img.getpixel((i, j))
			if r != g != b: 
				return False
	return True
	

if __name__ == '__main__':
	
	image_folder = "sample_folder"
	textfile_folder = "text_file"

	kernel = np.ones((3,3), np.uint8)

	for root, dirs, files in os.walk(image_folder):
		
		for file in files:
			text = ''

			# image_path = os.path.join(root, file)
			# os.rename(image_path, filename + ".png")

			image_path = os.path.join(root, file)
			filename, file_extension = os.path.splitext(image_path)

			image = cv2.imread(image_path)
# ========================== 	PREPROCESSING 	========================== 

			# check if image is grayscale, if true extract text
			# # else, preprocess image
			# if not is_gray_scale(image_path):
				# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				# image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
				# image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
		
			# image = otsu_preprocess(image, image)	
			
			# image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
			# image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

			# image = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)


			# 	print(" Image is not grayscale")
			# 	new_img = image
			# 	# image = remove_watermark(image)
			# 	image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7,21)

			# else:
			# 	image = cv2.fastNlMeansDenoising(image, None, 10, 10, 7,21)

			# ====== option 1: ============
			
			# cv2.imshow("img",image)
			# cv2.waitKey(2000)
			
			# ====== option 2: ============
			# image = otsu_preprocess(image, new_img)

			print("pre-processing done. . .")
			cv2.imwrite(image_path, image)

# ===================================================
			print(image_path)

			directory = image_path.split("\\")[1]

			text = extract_text(image_path)

			if not os.path.exists(textfile_folder):
				os.mkdir(textfile_folder)

			if not os.path.exists(textfile_folder + "/" + directory):
				with open(textfile_folder + "/" + directory + ".txt", "a+", encoding='utf-8') as f:
					f.write(text)

			print(directory, " text file DONE")

	make_csv.start()


			# split each line according to subject and grade
			# 	Logic:
			# 		start from the end of the line
