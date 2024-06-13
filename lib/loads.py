import cv2
import random
import threading
from lib.utils import *

clear()

# Load your model first
model = './model/frozen_inference_graph_V2.pb'
config = './model/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
net = cv2.dnn.readNetFromTensorflow(model, config)

# Load your labels
labels = openLabels('./model/coco.names')

# Video capture for detection
def video_capture(address, frame_buffer):
    video = cv2.VideoCapture(address)
    while True:
        check, frame = video.read()
        if check:
            frame_buffer.append(frame)
            if len(frame_buffer) > 1:
                frame_buffer.pop(0)
        else:
            break
    video.release()

# Function to process image
def process_image(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Unable to read the image file.")
        return

    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    for detection in detections[0, 0, :, :]:
        confidence = detection[2]
        if confidence > 0.5:
            class_id = int(detection[1])
            x_left_bottom = int(detection[3] * width)
            y_left_bottom = int(detection[4] * height)
            x_right_top = int(detection[5] * width)
            y_right_top = int(detection[6] * height)
            # labeling
            label = labels[class_id]
            cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (255, 0, 0), 2)
            cv2.putText(frame, label, (x_left_bottom, y_left_bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('Image Detection', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to process video from file
def process_video(video_path, scale_percent):
    video = cv2.VideoCapture(video_path)
    while video.isOpened():
        check, frame = video.read()
        if not check:
            break

        # Calculate new dimensions
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        new_dimensions = (width, height)
        
        # Resize frame
        frame = cv2.resize(frame, new_dimensions)
        
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
        net.setInput(blob)
        detections = net.forward()

        for detection in detections[0, 0, :, :]:
            confidence = detection[2]
            if confidence > 0.5:
                class_id = int(detection[1])
                x_left_bottom = int(detection[3] * width)
                y_left_bottom = int(detection[4] * height)
                x_right_top = int(detection[5] * width)
                y_right_top = int(detection[6] * height)
                # labeling
                label = labels[class_id]
                # drakor stuff
                # if label == 'orang' and random.choice([True, False]):
                #     label = 'toilet'
                cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (255, 0, 0), 2)
                cv2.putText(frame, label, (x_left_bottom, y_left_bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('Video Detection', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# Main (load this function)
def main(app_name, source_type, source_path, scale_percent=50):
    if source_type == 'url':
        frame_buffer = []
        capture_thread = threading.Thread(target=video_capture, args=(source_path, frame_buffer))
        capture_thread.daemon = True
        capture_thread.start()

        while True:
            if frame_buffer:
                frame = frame_buffer[-1]
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                new_dimensions = (width, height)
                frame = cv2.resize(frame, new_dimensions)
                height, width, _ = frame.shape
                blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
                net.setInput(blob)
                detections = net.forward()

                for detection in detections[0, 0, :, :]:
                    confidence = detection[2]
                    if confidence > 0.5:
                        class_id = int(detection[1])
                        x_left_bottom = int(detection[3] * width)
                        y_left_bottom = int(detection[4] * height)
                        x_right_top = int(detection[5] * width)
                        y_right_top = int(detection[6] * height)
                        # labeling
                        label = labels[class_id]
                        # drakor stuff
                        if label == 'orang' and random.choice([True, False]):
                            label = 'toilet'
                        cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (255, 0, 0), 2)
                        cv2.putText(frame, label, (x_left_bottom, y_left_bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                cv2.imshow(app_name, frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cv2.destroyAllWindows()
    elif source_type == 'image':
        process_image(source_path)
    elif source_type == 'video':
        process_video(source_path, scale_percent)
    else:
        print("Error: Unknown source type. Use 'url', 'image', or 'video'.")
