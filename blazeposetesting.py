import cv2
import mediapipe as mp
import csv
import tkinter as tk
from tkinter import filedialog

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseLandmarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pose Landmark Detection")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.config(bg="#8718f0")
        self.root.attributes("-alpha", 0.6)

        
        # Create GUI elements
        self.input_label = tk.Label(root, text="Select Input Video:")
        self.input_label.pack()
        
        self.input_button = tk.Button(root, text="Browse", command=self.browse_input)
        self.input_button.pack()
        
        self.process_button = tk.Button(root, text="Process Video", command=self.process_video)
        self.process_button.pack()
        
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def browse_input(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])

    def process_video(self):
        if not hasattr(self, 'input_path'):
            print("Please select an input video.")
            return

        # Open the video file
        cap = cv2.VideoCapture(self.input_path)

        # Create a CSV file to save the pose landmark data
        output_csv_path = 'pose_landmarks.csv'
        with open(output_csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write header row
            header = ['Frame', 'LandmarkID', 'X', 'Y']
            csv_writer.writerow(header)

            # Define the output video settings
            output_video_path = 'output_video.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video output
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

            # Initialize MediaPipe Pose
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                frame_count = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Convert the BGR image to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Process the frame and detect poses
                    results = pose.process(rgb_frame)

                    if results.pose_landmarks:
                        for landmark_id, landmark in enumerate(results.pose_landmarks.landmark):
                            # Write landmark data to the CSV file
                            row = [frame_count, landmark_id, landmark.x, landmark.y]
                            csv_writer.writerow(row)

                        # Render pose landmarks on the frame
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    # Write the processed frame to the output video
                    out.write(frame)

                    frame_count += 1

                # Release the video capture, video writer, and close OpenCV windows
                cap.release()
                out.release()
                cv2.destroyAllWindows()

        print("Processing complete. Pose landmark data saved to pose_landmarks.csv and video saved to output_video.mp4.")

def main():
    root = tk.Tk()
    app = PoseLandmarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
