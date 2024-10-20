from paddleocr import PaddleOCR
import numpy as np

def process_images_in_directory(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  
    result = ocr.ocr(image_path, cls=True)

    extracted_text = []
    text_heights = []

    # First pass: Extract text and calculate height (font size)
    for line in result:
        for word_info in line:
            text = word_info[1][0]  
            box = word_info[0]
            height = np.abs(box[0][1] - box[2][1])  # Calculate height (approx. font size)
            extracted_text.append((text, box, height))
            text_heights.append(height)

    # Determine header size threshold
    avg_height = np.mean(text_heights)
    header_threshold = avg_height + 0.3 * avg_height  # Headers are typically larger than average text

    organized_dict = {}
    current_heading = None

    # Second pass: Organize text into headers and content
    for i, (text, box, height) in enumerate(extracted_text):
        if current_heading is None or height > header_threshold:  # Heading detection based on threshold
            current_heading = text
            organized_dict[current_heading] = ""
        elif current_heading is not None and height <= header_threshold:  # Treat as content
            organized_dict[current_heading] += text + " "

    # Clean up whitespace in organized content
    for heading in organized_dict:
        organized_dict[heading] = organized_dict[heading].strip()

    return organized_dict

# Input image path
image_path = input("Enter the image path: ")
result_dict = process_images_in_directory(image_path)

# Display the results
for heading, content in result_dict.items():
    print(f"Header : {heading}")
    print(f"Content: {content}")
