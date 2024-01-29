import gradio as gr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import medfilt

# Function to calculate the skyline in a given mask
def cal_skyline(mask):
    h, w = mask.shape
    for i in range(w):
        raw = mask[:, i]
        after_median = medfilt(raw, 19)
        try:
            first_zero_index = np.where(after_median == 0)[0][0]
            first_one_index = np.where(after_median == 1)[0][0]
            if first_zero_index > 20:
                mask[first_one_index:first_zero_index, i] = 1
                mask[first_zero_index:, i] = 0
                mask[:first_one_index, i] = 0
        except:
            continue
    return mask

# Function to get the skyline region gradient in an image
def get_sky_region_gradient(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply color space conversion (e.g., RGB to HSV)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_channel = hsv_img[:, :, 0]

    # Thresholding Techniques
    _, thresholded_img = cv2.threshold(hue_channel, 100, 255, cv2.THRESH_BINARY)

    # Morphological Operations (e.g., erosion, dilation)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    morph_img = cv2.morphologyEx(thresholded_img, cv2.MORPH_OPEN, kernel)

    # Edge Detection (e.g., Canny edge detector)
    edges = cv2.Canny(img_gray, 50, 150)

    # Combine the results using logical OR
    combined_mask = np.logical_or.reduce([morph_img, edges])

    # Optional: Apply median blur or other filtering if needed
    combined_mask = cv2.medianBlur(combined_mask.astype(np.uint8), 5)

    # Calculate skyline using your existing function
    mask = cal_skyline(combined_mask)

    # Apply the mask to the original image
    after_img = cv2.bitwise_and(img, img, mask=mask)

    return after_img

# Function to process the input image using the above functions
def process_image(input_image):
    img = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
    result_img = get_sky_region_gradient(img)
    return cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

# Gradio Interface
iface = gr.Interface(
    fn=process_image,
    inputs=["image"],
    outputs="image",
)

# Launch the Gradio interface
iface.launch()
