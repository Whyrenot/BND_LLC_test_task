import cv2
from ultralytics import YOLO
import argparse


def draw_tracks(frame, boxes):
    """
    Отрисовка bounding box на кадре

    Параметры:
        frame (ndarray): кадр видео
        boxes (Boxes): bounding boxes

    Returns:
        ndarray: кадр с аннотациями
    """

    annotated = frame.copy()

    if boxes.id is None:
        return annotated

    for xyxy, track_id, conf in zip(boxes.xyxy, boxes.id, boxes.conf):
        x1, y1, x2, y2 = map(int, xyxy)

        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated,
            f"conf:{conf:.2f}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

    return annotated

import argparse

def parse_args():
    """
    Парсит аргументы командной строки для скрипта отслеживания объектов на видео
    с использованием YOLO.

    Поддерживаемые аргументы:
        --video-path: Путь к входному видеофайлу.
            По умолчанию: "data/crowd.mp4".

        --output-path: Путь к выходному видеофайлу с результатами трекинга.
            По умолчанию: "res.mp4".

    Возвращает:
        argparse.Namespace: Объект с проанализированными аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description="YOLO video tracking")

    parser.add_argument(
        "--video-path",
        type=str,
        default="data/crowd.mp4",
        help="Path to input video (default: data/crowd.mp4)",
    )

    parser.add_argument(
        "--output-path",
        type=str,
        default="res.mp4",
        help="Path to output video file (default: res.mp4)",
    )

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    video_path = args.video_path
    output_video_path = args.output_path

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        output_video_path,
        fourcc,
        fps,
        (width, height),
    )

    model = YOLO("tuned_model.pt")

    print("Video processing...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(
            frame,
            tracker="ultralytics/cfg/trackers/bytetrack.yaml",
            persist=True,
            conf=0.2,
            iou=0.6,
            imgsz=928,
            verbose=False,
        )

        annotated = draw_tracks(frame, results[0].boxes)
        writer.write(annotated)

    cap.release()
    writer.release()

    print("Video saved:", output_video_path)

