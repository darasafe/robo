import cv2
import depthai as dai
import mediapipe as mp
import numpy as np

# Create DepthAI pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(15)  # Adjust FPS as needed

xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")

# Linking
cam_rgb.preview.link(xout_video.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the frames from the output defined above
    q_video = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Initialize MediaPipe Hand module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    while True:
        in_video = q_video.get()
        frame = in_video.getCvFrame()

        # Convert the BGR image to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and find hands
        results = hands.process(rgb_frame)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Uncomment below to print the coordinates of each landmark
                # for idx, landmark in enumerate(hand_landmarks.landmark):
                #     print(f"Landmark {idx}: x={landmark.x}, y={landmark.y}, z={landmark.z}")

        # Display the resulting frame
        cv2.imshow('Hand Tracking', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    hands.close()
    cv2.destroyAllWindows()
