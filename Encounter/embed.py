import fitz  # PyMuPDF
import os    # Import the os module for path manipulation

def add_video_link_to_pdf(input_pdf_path, output_pdf_path, page_number, link_rect_coords, video_url_or_path, link_text="Watch Video"):
    """
    Adds a clickable link annotation to a specified page of a PDF.
    This link, when clicked, will open the video in an external application
    (web browser for URLs, or local media player for file paths).

    Args:
        input_pdf_path (str): The file path to the existing PDF document.
        output_pdf_path (str): The file path where the modified PDF will be saved.
        page_number (int): The 0-indexed page number where the link will be added.
        link_rect_coords (tuple): A tuple (x0, y0, x1, y1) defining the
                                  bounding box for the clickable link area on the page.
                                  Coordinates are in PDF points (1/72 inch).
        video_url_or_path (str): The URL of the online video (e.g., "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                                 OR the full file path to a local video (e.g., "file:///C:/Users/User/Videos/my_video.mp4").
        link_text (str): Optional text to display near the link, indicating its purpose.
                         This text is added as a separate annotation for clarity.
    """
    try:
        # Open the existing PDF document
        doc = fitz.open(input_pdf_path)

        # Ensure the page number is valid
        if not (0 <= page_number < len(doc)):
            print(f"Error: Page number {page_number} is out of bounds for PDF with {len(doc)} pages.")
            return

        page = doc[page_number]

        # Define the rectangle for the clickable link area
        link_rect = fitz.Rect(link_rect_coords)

        # Add the URI link annotation
        # fitz.LINK_URI is used for both web URLs and local file paths (prefixed with 'file://')
        link_annotation = {
            "kind": fitz.LINK_URI,
            "from": link_rect,
            "uri": video_url_or_path
        }
        page.insert_link(link_annotation)
        print(f"Added link to '{video_url_or_path}' at coordinates {link_rect_coords} on page {page_number}.")

        # Optionally, add some text to make the link visible and descriptive
        # This text will be placed just above or next to the link rectangle
        text_point = fitz.Point(link_rect.x0, link_rect.y0 - 15) # 15 points above the link
        page.insert_text(text_point, link_text, fontsize=10, color=(0, 0, 0)) # Black color
        print(f"Added descriptive text '{link_text}' near the link.")

        # Save the modified PDF to a new file
        doc.save(output_pdf_path)
        doc.close()
        print(f"Modified PDF saved successfully to '{output_pdf_path}'.")

    except FileNotFoundError:
        print(f"Error: Input PDF file not found at '{input_pdf_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create a dummy PDF for demonstration purposes if it doesn't exist
    #    You would replace 'dummy_input.pdf' with your actual PDF file.
    dummy_pdf_name = "dummy_input.pdf"
    try:
        dummy_doc = fitz.open()
        dummy_page = dummy_doc.new_page(width=595, height=842) # A4 size
        dummy_page.insert_text(fitz.Point(50, 50), "This is a dummy PDF.", fontsize=12)
        dummy_page.insert_text(fitz.Point(50, 70), "A video link will be added below.", fontsize=12)
        dummy_doc.save(dummy_pdf_name)
        dummy_doc.close()
        print(f"Created a dummy PDF: {dummy_pdf_name}")
    except Exception as e:
        print(f"Could not create dummy PDF (it might already exist or there's a permission issue): {e}")

    # --- Configuration for adding the link ---
    input_pdf_file = dummy_pdf_name  # Replace with your actual input PDF file
    output_pdf_file_online = "pdf_with_online_video_link.pdf"
    output_pdf_file_local = "pdf_with_local_video_link.pdf"
    target_page = 0  # The first page (0-indexed)

    # Coordinates for the clickable area for the online video (x0, y0, x1, y1)
    online_link_area_coordinates = (100, 100, 300, 150)

    # --- Choose your video source ---
    # Option A: Link to an online video (e.g., YouTube)
    online_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # A classic example!
    add_video_link_to_pdf(input_pdf_file, output_pdf_file_online, target_page,
                          online_link_area_coordinates, online_video_url, "Click to Watch Online Video")

    print("\n--- Testing with a local video file ---")
    # Option B: Link to a local video file named "video" in the current project path
    # IMPORTANT: The 'video' file must exist in the same directory as this script.
    # We construct the 'file:///' URI using os.path.abspath to get the full path.
    local_video_filename = "video" # The name of your video file in the project path
    absolute_local_video_path = os.path.abspath(local_video_filename)
    # Convert local path to a URI format suitable for PDF links
    local_video_uri = f"file:///{absolute_local_video_path.replace('\\', '/')}" # Replace backslashes for Windows paths

    # Coordinates for the clickable area for the local video (distinct from online link)
    local_link_area_coordinates = (100, 200, 300, 250)

    add_video_link_to_pdf(input_pdf_file, output_pdf_file_local, target_page,
                          local_link_area_coordinates, local_video_uri, "Click to Watch Local Video")


    print("\nProgram finished. Check the generated PDF file(s).")
    print(f"Open '{output_pdf_file_online}' and click the designated area to test the online link.")
    print(f"Open '{output_pdf_file_local}' and click the designated area to test the local link.")
    print(f"Ensure your local video file '{local_video_filename}' is in the same directory as this script for the local link to work.")
