from detector.utils import load_class_names
from detector.yolov3 import YoloV3, _MODEL_SIZE


def main(debug=False):
    class_names = load_class_names('detector/model_data/coco.names')
    n_classes = len(class_names)
    max_output_size = 10
    iou_threshold = 0.5
    confidence_threshold = 0.5

    model = YoloV3(n_classes=n_classes, model_size=_MODEL_SIZE,
                   max_output_size=max_output_size,
                   iou_threshold=iou_threshold,
                   confidence_threshold=confidence_threshold)

    inputs = model.get_input_placeholder()
    detections = model(inputs, training=False)

    model.run(inputs, detections, class_names, debug=debug)


if __name__ == '__main__':
    main(debug=True)
