import cv2
from math import ceil

font_scale = 1.25  # Adjust font size as needed
font_thickness = 2  # Adjust font thickness as needed


def putText(img, text, x_min, y_min, x_max, y_max, padding, font_scale=1.25):
    text = text.strip()
    cv2.rectangle(img, (x_min - padding[3], y_min - (padding[0])), (x_max + padding[2], y_max + padding[1]),
                  (255, 0, 255), -1)  # Green rectangle
    cv2.rectangle(img, (x_min - (padding[3] + 2), y_min - (padding[0] + 2)), (x_max + padding[2], y_max + padding[1]),
                  (0, 255, 0), 5)  # blur border

    text_position = (x_min, y_max)

    cv2.putText(img, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)


def calcMaxPosition(text, x_min, y_min):
    text = text.strip()
    (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]

    x_max = x_min + text_width
    y_max = y_min + text_height

    return (x_max, y_max)


def addRectText(img, text, x_min, y_min, padding=[25, 25, 25, 25]):
    text = text.strip()
    (x_max, y_max) = calcMaxPosition(text, x_min, y_min)

    # Get image width
    image_width = img.shape[1]

    font_scale = 1.25
    if x_max + padding[2] > image_width:
        font_scale = font_scale * 0.6

        (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        x_max = ceil(x_min + text_width)
        y_max = ceil(y_min + text_height)

    putText(img, text, x_min, y_min, x_max, y_max, padding, font_scale)

    return (x_max, y_max)
