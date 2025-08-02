import fitz  # PyMuPDF

def embed_video_with_drawn_play_button(pdf_path, video_file, output_pdf):
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Get bottom of existing text block
    blocks = page.get_text("blocks")
    bottom_y = max([b[3] for b in blocks]) if blocks else 200

    # Position for play button
    center_x = 120
    center_y = bottom_y + 70
    radius = 30

    # Draw circle (gray background)
    page.draw_circle(center=(center_x, center_y), radius=radius, color=(0, 0, 0), fill=(0.8, 0.8, 0.8))

    # Draw triangle (white play icon) using path
    triangle = [
        fitz.Point(center_x - 10, center_y - 15),
        fitz.Point(center_x - 10, center_y + 15),
        fitz.Point(center_x + 15, center_y)
    ]

    path = page.new_shape()
    path.move_to(triangle[0].x, triangle[0].y)
    path.line_to(triangle[1].x, triangle[1].y)
    path.line_to(triangle[2].x, triangle[2].y)
    path.close_path()
    path.finish(color=(1, 1, 1), fill=(1, 1, 1))
    path.commit()

    # Add description text below
    page.insert_text((center_x - 30, center_y + radius + 10), "Terms and acronyms", fontsize=12, fontname="helv")

    # Embed video
    doc.embfile_add(video_file, name=video_file, desc="AEDT video")
