import cv2
import numpy as np
from seaborn import color_palette
from PIL import Image, ImageDraw, ImageFont


def load_class_names(file_name):
    """
        Returns a list of class names read from `file_name`.
    """
    with open(file_name, 'r') as f:
        class_names = f.read().splitlines()
    return class_names


def draw_boxes(img_array, boxes_dicts, class_names, model_size):
    """
        Draws detected boxes.

        Args:
            img_names: A list of input images names.
            boxes_dict: A class-to-boxes dictionary.
            class_names: A class names list.
            model_size: The input size of the model.
    """
    colors = ((np.array(color_palette("hls", 80)) * 255)).astype(np.uint8)
    for num, img, boxes_dict in zip(range(len(img_array)), img_array,
                                    boxes_dicts):
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font='./detector/fonts/futur.ttf',
                                  size=(img.size[0] + img.size[1]) // 100)
        resize_factor = (
            (img.size[0] / model_size[0], img.size[1] / model_size[1])
        )
        for cls in range(len(class_names)):
            boxes = boxes_dict[cls]
            if np.size(boxes) != 0:
                color = colors[cls]
                for box in boxes:
                    xy, confidence = box[:4], box[4]
                    xy = [xy[i] * resize_factor[i % 2] for i in range(4)]
                    x0, y0 = xy[0], xy[1]
                    thickness = (img.size[0] + img.size[1]) // 200
                    for t in np.linspace(0, 1, thickness):
                        xy[0], xy[1] = xy[0] + t, xy[1] + t
                        xy[2], xy[3] = xy[2] - t, xy[3] - t
                        draw.rectangle(xy, outline=tuple(color))
                    text = '{} {:.1f}%'.format(class_names[cls],
                                               confidence * 100)
                    text_size = draw.textsize(text, font=font)
                    draw.rectangle(
                        [x0, y0 - text_size[1], x0 + text_size[0], y0],
                        fill=tuple(color))
                    draw.text((x0, y0 - text_size[1]), text, fill='black',
                              font=font)

        cv2.imshow('screen', np.array(img))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
