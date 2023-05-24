#allows us to upload pict, will be imported to our views
import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pi(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1] #grabs extension type of the file
    storage_filename = str(username) + '.' + ext_type #converts upload into unique username
    filepath = os.path.join(current_app.root_path, 'static/profile_pics',storage_filename)

    output_size = (150,150)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename