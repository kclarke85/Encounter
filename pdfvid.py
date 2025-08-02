# import os
# import fitz  # PyMuPDF
# from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
# from PIL import Image  # Import Pillow for image manipulation
#
#
# def pdf_to_video_with_music(pdf_path, audio_path, output_video_path, fps=1, image_dpi=200):
#     """
#     Converts a PDF file to a video with a background music track using PyMuPDF.
#
#     Args:
#         pdf_path (str): The path to the input PDF file.
#         audio_path (str): The path to the audio file (.mp3, .wav, etc.).
#         output_video_path (str): The desired path for the output video file (.mp4).
#         fps (int): Frames per second for the video (how long each PDF page is displayed).
#                    A value of 1 means each page is shown for 1 second.
#         image_dpi (int): DPI (Dots Per Inch) for rendering PDF pages to images.
#                          Higher DPI means better image quality but larger files.
#     """
#     if not os.path.exists(pdf_path):
#         print(f"Error: PDF file not found at '{pdf_path}'")
#         return
#     if not os.path.exists(audio_path):
#         print(f"Error: Audio file not found at '{audio_path}'")
#         return
#
#     # Define target video resolution (e.g., 1920x1080 for Full HD)
#     # You can change these values if you need a different output resolution
#     target_width = 1920
#     target_height = 1080
#     target_resolution = (target_width, target_height)
#
#     # --- Step 1: Convert PDF pages to images using PyMuPDF and standardize size ---
#     print("Converting PDF pages to images using PyMuPDF and standardizing size...")
#     image_files = []
#     temp_img_dir = "temp_pdf_images"
#     os.makedirs(temp_img_dir, exist_ok=True)
#
#     try:
#         # Open the PDF document
#         document = fitz.open(pdf_path)
#         num_pages = document.page_count
#
#         if num_pages == 0:
#             print("Error: The PDF document contains no pages.")
#             document.close()
#             return
#
#         # Iterate through each page and render it to a PNG image
#         for i in range(num_pages):
#             page = document.load_page(i)  # Load page by index
#             # Render page to a pixmap (pixel map) using the specified DPI
#             pix = page.get_pixmap(matrix=fitz.Matrix(image_dpi / 72, image_dpi / 72))
#
#             # Convert pixmap to PIL Image
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#
#             # Resize and pad the image to the target resolution
#             # Calculate aspect ratios
#             img_aspect = img.width / img.height
#             target_aspect = target_width / target_height
#
#             if img_aspect > target_aspect:
#                 # Image is wider than target aspect, fit to width
#                 new_width = target_width
#                 new_height = int(target_width / img_aspect)
#             else:
#                 # Image is taller or same aspect, fit to height
#                 new_height = target_height
#                 new_width = int(target_height * img_aspect)
#
#             # Resize the image
#             resized_img = img.resize((new_width, new_height), Image.LANCZOS)
#
#             # Create a new blank image with the target resolution (black background)
#             final_img = Image.new("RGB", target_resolution, (0, 0, 0))
#
#             # Calculate paste position to center the resized image
#             paste_x = (target_width - new_width) // 2
#             paste_y = (target_height - new_height) // 2
#
#             # Paste the resized image onto the black background
#             final_img.paste(resized_img, (paste_x, paste_y))
#
#             image_path = os.path.join(temp_img_dir, f"page_{i + 1}.png")
#             final_img.save(image_path, 'PNG')  # Save the processed PIL image as a PNG file
#             image_files.append(image_path)
#             print(f"  Generated and resized image for page {i + 1}: {image_path}")
#
#         document.close()  # Close the PDF document
#
#         if not image_files:
#             print("Error: No images were generated from the PDF.")
#             return
#
#     except Exception as e:
#         print(f"Error during PDF to image conversion with PyMuPDF: {e}")
#         return
#
#     # --- Step 2: Combine images into a video ---
#     print("Creating video from images...")
#     try:
#         # Calculate duration of each image based on total audio duration
#         audio_duration = AudioFileClip(audio_path).duration
#         if audio_duration == 0:
#             print("Warning: Audio file has zero duration. Video will be silent.")
#             page_duration = 1 / fps if fps > 0 else 1  # Default to 1 second per page
#         else:
#             # Ensure each page is displayed for an equal duration to match the audio
#             page_duration = audio_duration / len(image_files)
#             print(f"  Each page will be displayed for {page_duration:.2f} seconds to match audio duration.")
#
#         # Create ImageSequenceClip from the generated image files
#         # All images are now guaranteed to be of target_resolution
#         video_clip = ImageSequenceClip(image_files, durations=[page_duration] * len(image_files))
#
#     except Exception as e:
#         print(f"Error creating video from images: {e}")
#         return
#
#     # --- Step 3: Add music to the video ---
#     print("Adding music to the video...")
#     try:
#         audio_clip = AudioFileClip(audio_path)
#
#         # Ensure audio clip matches video duration
#         if audio_clip.duration < video_clip.duration:
#             # Loop audio if it's shorter than the video
#             print("  Audio is shorter than video, looping audio.")
#             audio_clip = concatenate_audioclips([audio_clip] * (int(video_clip.duration / audio_clip.duration) + 1))
#             audio_clip = audio_clip.set_duration(video_clip.duration)
#         elif audio_clip.duration > video_clip.duration:
#             # Trim audio if it's longer than the video
#             print("  Audio is longer than video, trimming audio.")
#             audio_clip = audio_clip.set_duration(video_clip.duration)
#
#         final_clip = video_clip.set_audio(audio_clip)
#
#     except Exception as e:
#         print(f"Error adding music to video: {e}")
#         return
#
#     # --- Step 4: Write the final video file ---
#     print(f"Writing final video to '{output_video_path}'...")
#     try:
#         # Using libx264 for video codec and aac for audio codec for broad compatibility
#         final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=fps)
#         print(f"Video created successfully at '{output_video_path}'")
#     except Exception as e:
#         print(f"Error writing video file: {e}")
#     finally:
#         # Clean up temporary image files
#         for img_file in image_files:
#             if os.path.exists(img_file):
#                 os.remove(img_file)
#         if os.path.exists(temp_img_dir):
#             os.rmdir(temp_img_dir)
#         print("Cleaned up temporary image files.")
#
#
# # --- Example Usage ---
# if __name__ == "__main__":
#     # Ensure 'slide.pdf' and 'music.mp3' exist in the same directory as this script,
#     # or provide their full paths.
#
#     pdf_file_path = "slide.pdf"
#     audio_file_path = "music.mp3"
#     output_video_file = "output_presentation.mp4"
#
#     print("\n--- Starting PDF to Video Conversion Process ---")
#     # Set fps to 0.5 to display each image for 2 seconds (1/0.5 = 2)
#     pdf_to_video_with_music(pdf_file_path, audio_file_path, output_video_file, fps=0.5)
#     print("--- Process Finished ---")


import os
import fitz  # PyMuPDF
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
from PIL import Image, ImageDraw  # Import Pillow for image manipulation and drawing


def pdf_to_video_with_music(pdf_path, audio_path, output_video_path, fps=1, image_dpi=200):
    """
    Converts a PDF file to a video with a background music track using PyMuPDF.

    Args:
        pdf_path (str): The path to the input PDF file.
        audio_path (str): The path to the audio file (.mp3, .wav, etc.).
        output_video_path (str): The desired path for the output video file (.mp4).
        fps (int): Frames per second for the video (how long each PDF page is displayed).
                   A value of 1 means each page is shown for 1 second.
        image_dpi (int): DPI (Dots Per Inch) for rendering PDF pages to images.
                         Higher DPI means better image quality but larger files.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at '{audio_path}'")
        return

    # Define target video resolution (e.g., 1920x1080 for Full HD)
    # You can change these values if you need a different output resolution
    target_width = 1920
    target_height = 1080
    target_resolution = (target_width, target_height)

    # --- Define area to cover with white (adjust these values as needed) ---
    # These coordinates are relative to the *final_img* (target_resolution)
    # You will need to experiment with these values to precisely cover the watermark.
    # Example: A small rectangle in the top-left corner
    watermark_area_x = 0
    watermark_area_y = 0
    watermark_area_width = int(target_width * 0.2)  # 20% of the width
    watermark_area_height = int(target_height * 0.05)  # 5% of the height
    # You might need to adjust these based on the exact location and size of "Made with Gamma"
    # For example, if it's consistently in the bottom-left, you'd adjust y and height.
    # watermark_area_y = target_height - int(target_height * 0.05) # For bottom-left

    # --- Step 1: Convert PDF pages to images using PyMuPDF and standardize size ---
    print("Converting PDF pages to images using PyMuPDF and standardizing size...")
    image_files = []
    temp_img_dir = "temp_pdf_images"
    os.makedirs(temp_img_dir, exist_ok=True)

    try:
        # Open the PDF document
        document = fitz.open(pdf_path)
        num_pages = document.page_count

        if num_pages == 0:
            print("Error: The PDF document contains no pages.")
            document.close()
            return

        # Iterate through each page and render it to a PNG image
        for i in range(num_pages):
            page = document.load_page(i)  # Load page by index
            # Render page to a pixmap (pixel map) using the specified DPI
            pix = page.get_pixmap(matrix=fitz.Matrix(image_dpi / 72, image_dpi / 72))

            # Convert pixmap to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Resize and pad the image to the target resolution
            # Calculate aspect ratios
            img_aspect = img.width / img.height
            target_aspect = target_width / target_height

            if img_aspect > target_aspect:
                # Image is wider than target aspect, fit to width
                new_width = target_width
                new_height = int(target_width / img_aspect)
            else:
                # Image is taller or same aspect, fit to height
                new_height = target_height
                new_width = int(target_height * img_aspect)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Create a new blank image with the target resolution (black background)
            final_img = Image.new("RGB", target_resolution, (0, 0, 0))

            # Calculate paste position to center the resized image
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2

            # Paste the resized image onto the black background
            final_img.paste(resized_img, (paste_x, paste_y))

            # --- Draw a white rectangle to cover the watermark ---
            draw = ImageDraw.Draw(final_img)
            # Define the bounding box for the rectangle (x1, y1, x2, y2)
            # This will draw a white rectangle from (watermark_area_x, watermark_area_y)
            # to (watermark_area_x + watermark_area_width, watermark_area_y + watermark_area_height)
            draw.rectangle(
                [watermark_area_x, watermark_area_y,
                 watermark_area_x + watermark_area_width,
                 watermark_area_y + watermark_area_height],
                fill="white"
            )
            # --- End of watermark covering ---

            image_path = os.path.join(temp_img_dir, f"page_{i + 1}.png")
            final_img.save(image_path, 'PNG')  # Save the processed PIL image as a PNG file
            image_files.append(image_path)
            print(f"  Generated and resized image for page {i + 1}: {image_path}")

        document.close()  # Close the PDF document

        if not image_files:
            print("Error: No images were generated from the PDF.")
            return

    except Exception as e:
        print(f"Error during PDF to image conversion with PyMuPDF: {e}")
        return

    # --- Step 2: Combine images into a video ---
    print("Creating video from images...")
    try:
        # Calculate duration of each image based on total audio duration
        audio_duration = AudioFileClip(audio_path).duration
        if audio_duration == 0:
            print("Warning: Audio file has zero duration. Video will be silent.")
            page_duration = 1 / fps if fps > 0 else 1  # Default to 1 second per page
        else:
            # Ensure each page is displayed for an equal duration to match the audio
            page_duration = audio_duration / len(image_files)
            print(f"  Each page will be displayed for {page_duration:.2f} seconds to match audio duration.")

        # Create ImageSequenceClip from the generated image files
        # All images are now guaranteed to be of target_resolution
        video_clip = ImageSequenceClip(image_files, durations=[page_duration] * len(image_files))

    except Exception as e:
        print(f"Error creating video from images: {e}")
        return

    # --- Step 3: Add music to the video ---
    print("Adding music to the video...")
    try:
        audio_clip = AudioFileClip(audio_path)

        # Ensure audio clip matches video duration
        if audio_clip.duration < video_clip.duration:
            # Loop audio if it's shorter than the video
            print("  Audio is shorter than video, looping audio.")
            audio_clip = concatenate_audioclips([audio_clip] * (int(video_clip.duration / audio_clip.duration) + 1))
            audio_clip = audio_clip.set_duration(video_clip.duration)
        elif audio_clip.duration > video_clip.duration:
            # Trim audio if it's longer than the video
            print("  Audio is longer than video, trimming audio.")
            audio_clip = audio_clip.set_duration(video_clip.duration)

        final_clip = video_clip.set_audio(audio_clip)

    except Exception as e:
        print(f"Error adding music to video: {e}")
        return

    # --- Step 4: Write the final video file ---
    print(f"Writing final video to '{output_video_path}'...")
    try:
        # Using libx264 for video codec and aac for audio codec for broad compatibility
        final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=fps)
        print(f"Video created successfully at '{output_video_path}'")
    except Exception as e:
        print(f"Error writing video file: {e}")
    finally:
        # Clean up temporary image files
        for img_file in image_files:
            if os.path.exists(img_file):
                os.remove(img_file)
        if os.path.exists(temp_img_dir):
            os.rmdir(temp_img_dir)
        print("Cleaned up temporary image files.")


# --- Example Usage ---
if __name__ == "__main__":
    # Ensure 'slide.pdf' and 'music.mp3' exist in the same directory as this script,
    # or provide their full paths.

    pdf_file_path = "slide.pdf"
    audio_file_path = "music.mp3"
    output_video_file = "output_presentation.mp4"

    print("\n--- Starting PDF to Video Conversion Process ---")
    # Set fps to 0.5 to display each image for 2 seconds (1/0.5 = 2)
    pdf_to_video_with_music(pdf_file_path, audio_file_path, output_video_file, fps=0.5)