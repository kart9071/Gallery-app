from flask import Flask, render_template, request, send_file
import os
import base64
from Database_connection import db

app = Flask(__name__)
app.debug = True


@app.route('/')
def home():
    message = "hello world"
    return render_template('Gallery.html', message=message)


@app.route('/upload/', methods=['POST'])
def uploading():
    file = request.files['image']
    if file.filename == '':
        return 'filename is incorrect'

    image_data = file.read()
    FileName = file.filename

    images = db.images
    document = {
        "filename": FileName,
        "image_data": {
            "$binary": {
                "base64": base64.b64encode(image_data).decode(),
                "subType": "00"  # This represents the binary sub-type (generic binary)
            }
        }
    }

    object_id = images.insert_one(document).inserted_id
    return f'Image is uploaded:{object_id}'

@app.route('/read/')
def read_all():
    images = db.images
    documents = images.find()
    filenames = []
    all_images = []

    for document in documents:
        filename = document.get('filename')
        if filename:
            filenames.append(filename)

        image_data = document.get("image_data")
        if image_data and isinstance(image_data, dict):
            base64_data = image_data.get("$binary", {}).get("base64")
            if base64_data:
                binary_data = base64.b64decode(base64_data)
                all_images.append(binary_data)

    output_folder = 'static/images_output'
    os.makedirs(output_folder, exist_ok=True)
    for deleting_files in os.listdir(output_folder):
        filepath=os.path.join(output_folder,deleting_files)
        os.remove(filepath)
    for file, image in zip(filenames, all_images):
        output_filename = os.path.join(output_folder, file)
        with open(output_filename, "wb") as f:
            f.write(image)
    imagefiles=os.listdir(output_folder)
    imagefiles.sort()
    return render_template('images.html',imagefiles=imagefiles)


@app.route('/delete/<string:filename>/', methods=['GET'])
def delete_image(filename):
    images = db.images
    deleted_document = images.find_one_and_delete({"filename": filename})
    if deleted_document:
        return f'image is deleted successfully {deleted_document}'
    else:
        return f'Image is not deleted {deleted_document}'

@app.route('/edit_image/')
def edit_image_page():
    # Retrieve the imageURL from the query parameters
    imageURL = request.args.get('imageURL', '')

    # Render the edit_image.html template and pass the imageURL to the template
    return render_template('edit_image.html', imagefile=imageURL)


if __name__ == '__main__':
    app.run()
