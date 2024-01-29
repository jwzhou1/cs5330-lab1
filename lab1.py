from scipy.signal import medfilt
import lab1 as gr
import cv2
import numpy as np

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
    h, w, _ = img.shape
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.blur(img_gray, (9, 3))
    cv2.medianBlur(img_gray, 5)
    lap = cv2.Laplacian(img_gray, cv2.CV_8U)
    gradient_mask = (lap < 6).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    mask = cv2.morphologyEx(gradient_mask, cv2.MORPH_ERODE, kernel)
    mask = cal_skyline(mask)
    after_img = cv2.bitwise_and(img, img, mask=mask)
    return after_img

def identify_sky_pixels(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_sky_blue = np.array([100, 50, 50])
    upper_sky_blue = np.array([140, 255, 255])
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([255, 30, 255])
    sky_mask = cv2.inRange(hsv_image, lower_sky_blue, upper_sky_blue)
    cloud_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    sky_mask = cv2.subtract(sky_mask, cloud_mask)
    kernel = np.ones((5, 5), np.uint8)
    morphological_image = cv2.morphologyEx(sky_mask, cv2.MORPH_OPEN, kernel)
    morphological_image = cv2.morphologyEx(morphological_image, cv2.MORPH_CLOSE, kernel)
    return morphological_image

def process_image(input_image):
    image = cv2.imread(input_image)
    sky_pixels = identify_sky_pixels(image)
    return sky_pixels

iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(),
    outputs=gr.Image(),
    live=True,
    capture_session=True,
)

iface.launch()
