from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
import os 
from Image_Processing.main import solve_image
from Image_Processing.image_methods import *
app = Flask(__name__, template_folder='C:\\Users\\nicky\\OneDrive\\Desktop\\Sudoku_Solver\\templates')
app.config['SECRET_KEY'] = 'akjflkwj'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, "Only Images are allowed"),
            FileRequired("File Field shound not be empty")
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename )
        uploaded_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        modified_file_path = solve_image(uploaded_file_path)
    else:
        file_url = None
        modified_file_path = None

    return render_template('index.html', form=form, file_url=file_url, modified_file_path=modified_file_path)

if __name__ == '__main__':
    app.run(debug=True)