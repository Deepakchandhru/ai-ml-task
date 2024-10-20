###Image Text Processing with PaddleOCR
##Overview
This program processes images to extract text using the PaddleOCR library. It analyzes the text to classify it into headings and content based on font size and boldness.

##Features
Text Extraction: Uses Optical Character Recognition (OCR) to extract text from images.
Heading Classification: Differentiates between headings and regular content based on font size and boldness.
Organized Output: Returns the extracted text in a structured format.

##Requirements
Before running the code, ensure you have the following libraries installed:

#OpenCV (cv2)
#NumPy (numpy)
#PaddleOCR

#Explanation
My process_fontsize.py file analyses the text and analyses the font size of all the text and make a threshold size as height above 0.3 times the average height. If the font size exceeds threshold, then it identifies it as header.

In my flagprocess.py file, the image text is analysed using the combined score of text boldness and font size. It gives more accuracy for complex images.
