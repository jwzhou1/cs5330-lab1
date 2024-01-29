import cv2
from scipy.signal import medfilt
import numpy as np
from matplotlib import pyplot as plt

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

    # Additional processing if required

    # Calculate skyline using your existing function
    mask = cal_skyline(combined_mask)

    # Apply the mask to the original image
    after_img = cv2.bitwise_and(img, img, mask=mask)

    return after_img

# Load the image
image_path = 'E:/cs5330-lab1/skyImages/hk.webp'
img = cv2.imread(image_path)

# Process the image
result_img = get_sky_region_gradient(img)

# Display the original and processed images
plt.subplot(1, 2, 1), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
plt.subplot(1, 2, 2), plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)), plt.title('Processed Image')
plt.show()
