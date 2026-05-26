# import cv2
# import os
# import time
# import pygame
#
#
# def slideshow(photo_folder, music_file, delay=3):
#     """
#     Runs a photo slideshow with background music.
#
#     Args:
#         photo_folder (str): Path to the folder containing photos.
#         music_file (str): Path to the music file (e.g., .mp3, .wav).
#         delay (int): Delay in seconds between each photo (default is 3 seconds).
#     """
#
#     # --- 1. Load Images ---
#     image_paths = []
#     valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
#     for filename in os.listdir(photo_folder):
#         if filename.lower().endswith(valid_extensions):
#             image_paths.append(os.path.join(photo_folder, filename))
#
#     if not image_paths:
#         print(f"No valid images found in the folder: {photo_folder}")
#         return
#
#     image_paths.sort()  # Optional: Sort images by name
#
#     # --- 2. Initialize Pygame Mixer for Music ---
#     try:
#         pygame.mixer.init()
#         pygame.mixer.music.load(music_file)
#         pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
#         print(f"Playing music: {music_file}")
#     except pygame.error as e:
#         print(f"Could not load or play music: {e}")
#         print("Make sure the music file path is correct and it's a supported format.")
#         print("You might need to install pygame: pip install pygame")
#         # Continue without music if there's an error
#
#     # --- 3. Run Slideshow ---
#     cv2.namedWindow('Slideshow', cv2.WINDOW_NORMAL)  # Create a resizable window
#
#     for image_path in image_paths:
#         img = cv2.imread(image_path)
#
#         if img is None:
#             print(f"Could not load image: {image_path}")
#             continue
#
#         # Resize image to fit screen or a reasonable size if it's too large
#         screen_res = 1280, 720  # Example screen resolution
#         scale_width = screen_res[0] / img.shape[1]
#         scale_height = screen_res[1] / img.shape[0]
#         scale = min(scale_width, scale_height)
#
#         if scale < 1:  # Only resize if image is larger than screen_res
#             width = int(img.shape[1] * scale)
#             height = int(img.shape[0] * scale)
#             img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
#
#         cv2.imshow('Slideshow', img)
#
#         # Wait for 'delay' seconds or until 'q' is pressed
#         # cv2.waitKey returns the ASCII value of the pressed key
#         key = cv2.waitKey(delay * 1000) & 0xFF
#         if key == ord('q'):  # Check if 'q' key is pressed
#             print("Slideshow stopped by user.")
#             break
#
#     # --- 4. Cleanup ---
#     cv2.destroyAllWindows()
#     if pygame.mixer.get_init():
#         pygame.mixer.music.stop()
#         pygame.mixer.quit()
#     print("Slideshow finished.")
#
#
# if __name__ == "__main__":
#     # --- Configuration ---
#     # IMPORTANT: Replace these with your actual local paths
#     PHOTO_FOLDER_PATH = "C://Users//kwcte//PycharmProjects//Encounter//bird_photos"  # Example: "C:/Users/YourUser/Pictures/SlideshowPhotos"
#     MUSIC_FILE_PATH = "C://Users//kwcte//PycharmProjects//Encounter//bird_photos//Maple - Dyalla.mp3"  # Example: "C:/Users/YourUser/Music/MyBackgroundMusic.mp3"
#     SLIDESHOW_DELAY_SECONDS = 5  # Time each photo is displayed
#
#     # --- Run the Slideshow ---
#     slideshow(PHOTO_FOLDER_PATH, MUSIC_FILE_PATH, SLIDESHOW_DELAY_SECONDS)
#
#



import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

def create_slideshow_video(photo_folder, music_file, output_file, slide_duration=5, video_size=(1280, 720)):
    # 1. Collect image files
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    image_files = sorted([
        os.path.join(photo_folder, f)
        for f in os.listdir(photo_folder)
        if f.lower().endswith(valid_extensions)
    ])

    if not image_files:
        print(f"No images found in {photo_folder}")
        return

    # 2. Create ImageClips for each image
    clips = []
    for img_path in image_files:
        clip = ImageClip(img_path).set_duration(slide_duration)
        # Resize to fit video_size while keeping aspect ratio
        clip = clip.resize(height=video_size[1])
        clips.append(clip)

    # 3. Concatenate all clips into one video
    video = concatenate_videoclips(clips, method="compose")

    # 4. Load the audio file
    audio = AudioFileClip(music_file)

    # 5. Set audio to video (loop if audio shorter than video)
    audio = audio.audio_loop(duration=video.duration)
    video = video.set_audio(audio)

    # 6. Write the video file
    print(f"Rendering video to {output_file} ...")
    video.write_videofile(output_file, fps=24)

    print("Video created successfully!")

if __name__ == "__main__":
    PHOTO_FOLDER = r"C:\Users\kwcte\PycharmProjects\Encounter\birdbabies"
    MUSIC_FILE = r"C:\Users\kwcte\PycharmProjects\Encounter\bird_photos\Maple - Dyalla.mp3"
    OUTPUT_FILE = "slideshow_video.mp4"
    SLIDE_DURATION = 5  # seconds per image
    VIDEO_SIZE = (1280, 720)

    create_slideshow_video(PHOTO_FOLDER, MUSIC_FILE, OUTPUT_FILE, SLIDE_DURATION, VIDEO_SIZE)
