import numpy as np
from paddleocr import PaddleOCR

def process_images_in_directory(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  
    result = ocr.ocr(image_path, cls=True)

    extracted_text = []
    font_sizes = []
    boldness_scores = []

    # First pass: Extract text and calculate font size and boldness
    for line in result:
        for word_info in line:
            text = word_info[1][0]  # Extract text
            confidence = word_info[1][1]  # Confidence score
            box = word_info[0]  # Bounding box
            height = np.abs(box[0][1] - box[2][1])  # Font size based on box height
            area = np.abs((box[2][0] - box[0][0]) * (box[2][1] - box[0][1]))  # Bounding box area
            boldness_score = confidence * area  # Boldness estimate

            # Store all attributes
            extracted_text.append((text, height, boldness_score))
            font_sizes.append(height)
            boldness_scores.append(boldness_score)

    # Normalize and weigh the two factors: font size and boldness
    max_font_size = max(font_sizes) if font_sizes else 1
    max_boldness = max(boldness_scores) if boldness_scores else 1

    font_weight = 0.6
    bold_weight = 0.4

    organized_dict = {}
    current_heading = None

    # Second pass: Combine font size and boldness to classify headings and content
    for i, (text, font_size, boldness_score) in enumerate(extracted_text):
        normalized_font_size = font_size / max_font_size
        normalized_boldness = boldness_score / max_boldness

        # Combined score to classify the text
        combined_score = (normalized_font_size * font_weight +
                          normalized_boldness * bold_weight)

        # Threshold for heading classification (adjust based on the project needs)
        if combined_score > 0.6:  # Higher combined score means more likely to be a heading
            current_heading = text
            organized_dict[current_heading] = ""
        else:  # Consider it content under the current heading
            if current_heading:
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
    print(f"Heading: {heading}")
    print(f"Content: {content}\n")
