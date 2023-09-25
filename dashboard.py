# import dropbox
# import requests
#
# # Replace with your Dropbox API access token
# access_token = 'sl.BjToKVOqdXXTd5K91Eih73yML7OJcBJoWAkoYmz4Xf7M4lUnf8WquAjGrfOX10OsCxRz6opx23Pzy9fRSVnr3RM0HWua0QsTS2wnF0UPh-p-11wrNBSNeZMdW9BPhKH3AdHblMI_jMgci2UJZwRNlPA'
# dbx = dropbox.Dropbox(access_token)
#
# # The path of the Dropbox folder you want to access
# folder_path = '/Your/Dropbox/Folder'
#
# # Get a list of all files in the folder
# result = dbx.files_list_folder(folder_path)
# files = result.entries
#
# html_string = """
# <!DOCTYPE html>
# <html>
# <body>
# """
#
# for file in files:
#     # Get a temporary link for the file
#     file_path = file.path_lower
#     link = dbx.files_get_temporary_link(file_path).link
#
#     # Replace the 'www.dropbox.com' with 'dl.dropboxusercontent.com' in the link
#     direct_link = link.replace("https://www.dropbox.com/s/n271fy42za8lr9q/image_1690853985.jpg?dl=0", "dl.dropboxusercontent.com")
#
#     # Check the file extension and create the appropriate HTML tag
#     if file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.gif'):
#         html_string += f'<img src="{direct_link}" alt="{file.name}" style="float: left;">\n'
#     elif file.name.endswith('.mp4'):
#         html_string += f"""
#         <video width="320" height="240" controls style="float: left;">
#         <source src="{direct_link}" type="video/mp4">
#         Your browser does not support the video tag.
#         </video>\n
#         """
#
# html_string += """
# </body>
# </html>
# """
#
# # Write the HTML string to a file
# with open('dashboard.py', 'w') as f:
#     f.write(html_string)
# import dropbox
# import requests
#
# # Replace with your Dropbox API access token
# access_token = 'sl.BjToKVOqdXXTd5K91Eih73yML7OJcBJoWAkoYmz4Xf7M4lUnf8WquAjGrfOX10OsCxRz6opx23Pzy9fRSVnr3RM0HWua0QsTS2wnF0UPh-p-11wrNBSNeZMdW9BPhKH3AdHblMI_jMgci2UJZwRNlPA'
# dbx = dropbox.Dropbox(access_token)
#
# # The path of the Dropbox folder you want to access
# folder_path = '/Your/Dropbox/Folder'
#
# # Get a list of all files in the folder
# result = dbx.files_list_folder(folder_path)
# files = result.entries
#
# html_string = """
# <!DOCTYPE html>
# <html>
# <head>
# <style>
# body {
#   display: flex;
#   margin: 0;
#   padding: 0;
# }
# .sidebar {
#   width: 30%;
#   height: 100vh;
#   overflow: auto;
# }
# .main {
#   width: 70%;
# }
# img {
#   width: 100%;
#   height: auto;
# }
# </style>
# </head>
# <body>
# <div class="sidebar">
# """
#
# for file in files:
#     # Get a temporary link for the file
#     file_path = file.path_lower
#     link = dbx.files_get_temporary_link(file_path).link
#
#     # Replace the 'www.dropbox.com' with 'dl.dropboxusercontent.com' in the link
#     direct_link = link.replace("https://www.dropbox.com/s/n271fy42za8lr9q/image_1690853985.jpg?dl=0", "dl.dropboxusercontent.com", "dl.dropboxusercontent.com")
#
#     # Check the file extension and create the appropriate HTML tag
#     if file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.gif'):
#         html_string += f'<img src="{direct_link}" alt="{file.name}">\n'
#
# html_string += """
# </div>
# <div class="main">
# <!-- Content goes here -->
# </div>
# </body>
# </html>
# """
#
# # Write the HTML string to a file
# with open('dashboard.py', 'w') as f:
#     f.write(html_string)
# from flask import Flask, render_template, request
# import dropbox
# import matplotlib.pyplot as plt
# import mplleaflet
#
# app = Flask(__name__)
# dbx = dropbox.Dropbox('sl.Bjc6aXudAX68Gho0Y9g0R8UidyzOLDPXenafw_oxRsgXZxWhh5S21ISo9AgLLXSR8A8XCm1vu_iwek-JXZDBUqreEuIUL7PRdQkjQ7AheMC07VPpMywbgRrAGA614mdgVj_6I2zJq6j0MPz8FpWUULA')
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         dbx.files_upload(file.read(), '/' + file.filename)
#         return 'File uploaded successfully'
#     else:
#         return '''
#                 <html>
#                     <body>
#                         <form method="post" enctype="multipart/form-data">
#                             <p><input type="file" name="file"></p>
#                             <p><input type="submit" value="Upload"></p>
#                         </form>
#                     </body>
#                 </html>
#             '''
#
# @app.route('/bubble')
# def bubble_chart():
#     x = [1, 2, 3, 4]
#     y = [10, 15, 7, 10]
#     size = [100, 250, 50, 100]
#
#     plt.scatter(x, y, s=size)
#     plt.savefig('static/bubble.png')
#     plt.clf()
#
#     return '''
#             <html>
#                 <body>
#                     <img src="/static/bubble.png" alt="Bubble Chart">
#                 </body>
#             </html>
#             '''
#
# @app.route('/map')
# def geo_chart():
#     latitude = 34.0754
#     longitude = -84.2941
#     plt.figure(figsize=(8,8))
#
#     plt.plot([longitude], [latitude], 'rs')
#     mplleaflet.show(path='templates/map.html')
#
#     return render_template('map.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
# from flask import Flask, render_template
# import dropbox
#
# app = Flask(__name__)
#
# # Access token from your Dropbox account
# access_token = 'sl.Bjc6aXudAX68Gho0Y9g0R8UidyzOLDPXenafw_oxRsgXZxWhh5S21ISo9AgLLXSR8A8XCm1vu_iwek-JXZDBUqreEuIUL7PRdQkjQ7AheMC07VPpMywbgRrAGA614mdgVj_6I2zJq6j0MPz8FpWUULA'
#
# dbx = dropbox.Dropbox(access_token)
#
# @app.route('/')
# def home():
#     files = []
#     for entry in dbx.files_list_folder('').entries:
#         files.append(entry.name)
#     return render_template('dashboard.py', files=files)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
import os
import os
import dropbox
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace with your Dropbox access token
DROPBOX_ACCESS_TOKEN = "sl.Bjc6aXudAX68Gho0Y9g0R8UidyzOLDPXenafw_oxRsgXZxWhh5S21ISo9AgLLXSR8A8XCm1vu_iwek-JXZDBUqreEuIUL7PRdQkjQ7AheMC07VPpMywbgRrAGA614mdgVj_6I2zJq6j0MPz8FpWUULA"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        if file and allowed_file(file.filename):
            upload_file_to_dropbox(file)
            return "File successfully uploaded to Dropbox!"
        else:
            return "Invalid file type. Only .mp4 files are allowed.", 400

    return render_template("dashboard.py")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "mp4"

def upload_file_to_dropbox(file):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    filename = secure_filename(file.filename)
    file_path = f"/{filename}"
    dbx.files_upload(file.read(), file_path)

def secure_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)

if __name__ == "__main__":
    app.run(debug=True)
