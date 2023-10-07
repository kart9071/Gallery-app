from flask import Flask, render_template, request, send_file, jsonify
import os
import base64
from Database_connection import db
import cv2
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

app = Flask(__name__)
app.debug = True

punctuations=['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
    'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
    'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
    'under', 'again', 'further', 'then', 'once'
]



lemmatizer=WordNetLemmatizer()

def tokenize_and_get_tokens(text):
    tokens=word_tokenize(text)  # tokenizing each word in the text
    token_numbers=[]
    for i, token in enumerate(tokens,start=1):
        if token not in punctuations and token.lower() not in stop_words:     #removing the special character that do not have any use on sentiment analysis
            lemma=lemmatizer.lemmatize(token.lower())
            token_numbers.append((i,token))
    return token_numbers


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


#load the sentiment analysis model:
with open("sentiment_model.pkl","rb") as model_file:
    model=pickle.load(model_file)


@app.route("/Sentiment")
def home1():
    return render_template("index.html")

@app.route("/predict_sentiment",methods=["POST"])
def predict_sentiment():
    input_text = request.form["input_text"]
    new_text = tokenize_and_get_tokens(input_text)
    
    # Load the CountVectorizer and model
    with open("sentiment_model.pkl", "rb") as model_file:
        model_and_function = pickle.load(model_file)
        vectorizer = model_and_function["vectorizer"]
        model = model_and_function["model"]
    new_text_string = ' '.join([word for (_, word) in new_text])
    # Transform the new text using the fitted vectorizer
    preprocess = vectorizer.transform([new_text_string])
    
    # Make a prediction
    prediction = model.predict(preprocess)[0]
    
    return render_template("index.html", predicted_sentiment=prediction, input_text=input_text)


#To store the music to the mongo DB database

@app.route('/music/',methods=['POST'])
def add_music():
    '''TO ADD THE MUSIC WE NEED TO USE THIS COMMAND 
************************************************************************************************
    curl.exe -X POST -H "Content-Type: application/json" -d '{
    \"title\": \"Song2\",
    \"genre\": \"song23\",
    \"artist\": \"mahesh\",
    \"duration\": \"2:52\" 
    }' http://localhost:5000/music

************************************************************************************************
'''
    musics={                                                            
        "title":request.json['title'],
        "genre":request.json['genre'],
        "artist":request.json['artist'],
        "duration":request.json['duration']
    }
    db.music.insert_one(musics)
    
    return jsonify({'message':'Music added successfully'})




if __name__ == '__main__':
    app.run()


