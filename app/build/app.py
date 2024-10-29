from flask import Flask, Response
from adafruit_crickit import crickit
from flask_cors import CORS
import threading
import time
import numpy as np
from depthai_hand_tracker.HandTrackerEdge import HandTracker

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Servos
servo_pan = crickit.servo_1
servo_tilt = crickit.servo_2
servo_pan.set_pulse_width_range(min_pulse=500, max_pulse=2500)
servo_tilt.set_pulse_width_range(min_pulse=500, max_pulse=2500)

# Set initial angles (centered)
servo_pan.angle = 90
servo_tilt.angle = 90

# Control parameters
Kp_pan = 0.03
Kp_tilt = 0.03
deadzone = 30  # Increase to reduce jitter and CPU load

# Global variables for video streaming
output_frame = None
lock = threading.Lock()

# Helper functions
def clamp_angle(angle):
    """Clamp the servo angle between 0 and 180 degrees."""
    return max(0, min(180, angle))

def smooth_movement(current_angle, target_angle, step=1.2):
    """Move the servo smoothly towards the target angle."""
    if abs(target_angle - current_angle) < step:
        return target_angle
    return current_angle + step if target_angle > current_angle else current_angle - step

def adaptive_sleep(start_time, target_fps):
    """Dynamically adjust sleep to maintain target FPS."""
    elapsed_time = time.time() - start_time
    sleep_time = max(0.05, (1.0 / target_fps) - elapsed_time)
    time.sleep(sleep_time)

def hand_tracking():
    global output_frame

    tracker = None

    while True:
        try:
            # Initialize or reinitialize the tracker if needed
            if tracker is None:
                tracker = HandTracker(
                    input_src="rgb_laconic",  # Use laconic mode to reduce data transfer
                    use_lm=True,
                    lm_model="sparse",
                    lm_score_thresh=0.8,
                    solo=True,
                    internal_fps=15,  # Adjust FPS as needed
                    resolution="full",
                    crop=True,
                    use_gesture=False,  # Disable gesture recognition to reduce processing
                    xyz=False,  # Disable depth calculations
                    internal_frame_height=480,
                      # Ensure laconic mode is enabled
                )
                print("Tracker initialized.")

            start_time = time.time()  # Track the start time for FPS management

            # Get hand tracking data without frames
            _, hands, _ = tracker.next_frame()


            if hands:
                hand = hands[0]
                center_x, center_y = hand.landmarks[9][:2]  # Index finger base (more stable)

                # Adjust coordinates for frame size
                frame_height, frame_width = tracker.img_h, tracker.img_w

                # Calculate error for pan and tilt
                error_x = center_x - frame_width / 2
                error_y = center_y - frame_height / 2

                # Ignore small movements to reduce jitter
                if abs(error_x) < deadzone:
                    error_x = 0
                if abs(error_y) < deadzone:
                    error_y = 0

                # Calculate target angles and clamp them
                target_pan_angle = clamp_angle(servo_pan.angle - error_x * Kp_pan)
                target_tilt_angle = clamp_angle(servo_tilt.angle + error_y * Kp_tilt)

                # Move servos smoothly
                servo_pan.angle = smooth_movement(servo_pan.angle, target_pan_angle, step=1.5)
                servo_tilt.angle = smooth_movement(servo_tilt.angle, target_tilt_angle, step=1.5)

            # Since we're not processing frames, we can skip updating output_frame
            # Alternatively, you can request occasional frames if needed

            # Adaptive sleep to maintain stable FPS
            adaptive_sleep(start_time, target_fps=15)

        except ValueError as e:
            print(f"Servo error: {e}")
        except RuntimeError as e:
            print(f"Runtime error: {e}, restarting tracker...")
            if tracker:
                tracker.exit()
                tracker = None  # Reinitialize on error
        except Exception as e:
            print(f"Unexpected error: {e}")
            if tracker:
                tracker.exit()
                tracker = None  # Reinitialize on unexpected errors

@app.route('/video_feed')
def video_feed():
    """Video stream generator."""
    def generate():
        global output_frame
        while True:
            with lock:
                if output_frame is None:
                    time.sleep(0.05)  # Avoid tight loops
                    continue
                # Skip sending frames or send occasional frames if necessary
                # For now, we'll not send frames to reduce CPU load
            yield b''

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the hand tracking thread
    tracking_thread = threading.Thread(target=hand_tracking)
    tracking_thread.daemon = True
    tracking_thread.start()

    # Run the Flask app with fewer threads to reduce CPU load
    app.run(host='0.0.0.0', port=5000, threaded=False)
