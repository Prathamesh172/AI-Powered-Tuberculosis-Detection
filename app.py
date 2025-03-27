from flask import Flask, render_template, request
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
model = tf.keras.models.load_model("TB_Detection_ResNet50.h5")
class_labels = ['Negative for Tuberculosis', 'Positive for Tuberculosis']

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize
    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('predict.html', prediction="No file uploaded!")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('predict.html', prediction="No file selected!")
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        img = preprocess_image(file_path)
        prediction = model.predict(img)[0][0]
        predicted_class = class_labels[int(round(prediction))]
        
        return render_template('predict.html', prediction=predicted_class, image_path=file_path)
    
    return render_template('predict.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)