from ultralytics import YOLO
import cv2
import time

# Load YOLOv8 model
model = YOLO('yolov8m.pt')

# Load video
video_path = './test.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties for saving output
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
output_path = 'output_with_tracking.mp4'
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

ret = True
pause = False
prev_time = 0
frame_count = 0

while ret:
    if not pause:
        ret, frame = cap.read()

        if not ret:
            break

        # FPS calculation
        current_time = time.time()
        fps_calc = 1 / (current_time - prev_time) if prev_time else 0
        prev_time = current_time

        # Detect and track objects
        results = model.track(frame, persist=True)
        annotated_frame = results[0].plot()

        # Add FPS display
        cv2.putText(annotated_frame, f'FPS: {fps_calc:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show results
        cv2.imshow('Object Tracking', annotated_frame)

        # Write the frame with tracking results to output video
        out.write(annotated_frame)

        # Keyboard controls
        key = cv2.waitKey(25) & 0xFF

        if key == ord('q'):
            break  # Quit the program
        elif key == ord('p'):
            pause = True  # Pause the video
        elif key == ord('s'):
            cv2.imwrite(f'screenshot_{frame_count}.png', annotated_frame)  # Save screenshot
            print(f'Screenshot saved as screenshot_{frame_count}.png')

        frame_count += 1

    else:
        key = cv2.waitKey(25) & 0xFF
        if key == ord('p'):
            pause = False  # Unpause the video
        elif key == ord('q'):
            break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
