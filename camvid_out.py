# # import cv2
# # import time
# #
# # def camvid(file_path):
# #     # Set up video capture
# #     cap = cv2.VideoCapture(0)  # 0 for default camera
# #     if not cap.isOpened():
# #         print("Error: Could not open camera.")
# #         exit()
# #
# #     # Define the codec using VideoWriter_fourcc and set video writer settings
# #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # specify the video codec
# #     fps = 20.0
# #     frame_width = int(cap.get(3))
# #     frame_height = int(cap.get(4))
# #     out = cv2.VideoWriter('static/output.mp4', fourcc, fps, (frame_width, frame_height))
# #
# #     start_time = time.time()
# #     while True:
# #         ret, frame = cap.read()
# #         if ret:
# #             # Write the frame into the output file
# #             out.write(frame)
# #
# #             # Display the frame
# #             cv2.imshow('Recording', frame)
# #
# #             # Exit if 'q' is pressed or 10 minutes have passed
# #             if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 60:
# #                 break
# #         else:
# #             break
# #
# #     # Release everything and close windows
# #     cap.release()
# #     out.release()
# #     cv2.destroyAllWindows()
# import cv2
# import time
#
# def camvid(file_path='static/video.mp4'):
#     # Set up video capture
#     cap = cv2.VideoCapture(0)  # 0 for default camera
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         exit()
#
#     # Define the codec using VideoWriter_fourcc and set video writer settings
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # specify the video codec
#     fps = 20.0
#     frame_width = int(cap.get(3))
#     frame_height = int(cap.get(4))
#     out = cv2.VideoWriter(file_path, fourcc, fps, (frame_width, frame_height))
#
#     start_time = time.time()
#     while True:
#         ret, frame = cap.read()
#         if ret:
#             # Write the frame into the output file
#             out.write(frame)
#
#             # Display the frame
#             cv2.imshow('Recording', frame)
#
#             # Exit if 'q' is pressed or 10 minutes have passed
#             if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 60: # adjusted to 600 seconds for 10 minutes
#                 break
#         else:
#             break
#
#     # Release everything and close windows
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
#
# # To run the function
# camvid()
import imageio
import os
import Send_SMS_Alert

def rec_vid():
    # Ensure the static directory exists
    if not os.path.exists("static"):
        os.mkdir("static")

    # Parameters for recording
    duration = 120  # 1 minute in seconds
    fps = 20  # frames per second

    # Create a reader object to capture video from the webcam
    reader = imageio.get_reader('<video0>')

    # Create a writer object to save the video
    writer = imageio.get_writer('static/video.mp4', fps=fps)

    # Capture and write frames to the video file
    for i, frame in enumerate(reader):
        writer.append_data(frame)
        if i == fps * duration - 1:
            break

    writer.close()
    Send_SMS_Alert.send_sms('+16785201149')