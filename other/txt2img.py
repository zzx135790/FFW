import os
from PIL import Image, ImageDraw
from detect.common import output_file

def draw_bounding_boxes(image_folder, output_folder):
    """
    Draw bounding boxes on images based on the annotations provided.
    This version supports multiple bounding boxes per image.

    :param image_folder: Folder containing the images.
    :param annotations_folder: Folder containing the annotations in txt format.
    :param output_folder: Folder to save the images with bounding boxes.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dictionary to hold image data
    image_data = {}

    with open(output_file, 'r') as file:
        lines = file.readlines()

    # Process each line in the current annotation file
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 6:
            image_file, _, xmin, ymin, xmax, ymax = parts
            xmin, ymin, xmax, ymax = map(float, [xmin, ymin, xmax, ymax])

            # Accumulate bounding boxes for each image
            if image_file not in image_data:
                image_data[image_file] = []
            image_data[image_file].append((xmin, ymin, xmax, ymax))

    # Draw bounding boxes for each image
    for image_file, boxes in image_data.items():
        image_path = os.path.join(image_folder, image_file)
        if os.path.exists(image_path):
            # Open the image
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            # Draw all rectangles for the current image
            for xmin, ymin, xmax, ymax in boxes:
                draw.rectangle([xmin, ymin, xmax, ymax], outline='red', width=2)

            # Save the image with bounding boxes
            output_image_path = os.path.join(output_folder, image_file)
            image.save(output_image_path)
            print(f"Processed {image_file}")


# Example usage
image_folder = 'F:/ffwb/we_data/data_xml/ori_val_rotate'
output_folder = './results/2'
draw_bounding_boxes(image_folder, output_folder)
